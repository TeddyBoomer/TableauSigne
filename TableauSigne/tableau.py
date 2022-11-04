# -*- coding: utf-8 -*-
"""
Classe de création de tableau de signe à l'aide de sympy et lxml.
Elle génère au choix la sortie latex ou un tableau xml à lancer dans pst+.
"""

import operator
import re as regexp
from random import choice, randint
from lxml import etree
from functools import reduce
from copy import deepcopy
from sympy import var,sympify,oo,sign,det,Matrix,degree,Poly,denom,numer,random_poly,solve,Eq,latex,Pow,diff

x = var('x')

class TableauSigne():
    """
    Classe de creation du tableau de signe.
    Les bornes par défaut sont \pm oo réglable avec le paramètre bornes.

    :param string expr: expression à étudier, sous forme d'un produit ou quotient; 
      avec la syntaxe sympy.
    :param list bornes: liste à deux éléments pour les bornes. [-oo, oo] par défaut
    :param int niveau: niveau de difficulté pour générer un tableau à compléter: 1 \
                - juste les signes à remplir; 2 - aussi les valeurs particulières.

    Regroupez les facteurs du dénominateur ensembles pour éviter les mauvaises surprises.

    exemple::

        >>> a = TableauSigne('-1*(3*x+2)*(-5*x +4)')
        >>> b = TableauSigne('(3*x+2)**3 /(2*x - 5)**2 *(5*x+1) * -8')
        >>> b.export_pst(nom="SuperTest", simplif=False, ext='pag')
        >>> c = TableauSigne('(3*x+2)**3 /(2*x - 5)**2 *(5*x+1) * -8', bornes=[-1, 1])
        >>> d = TableauSigne('(-4*x+4)/(-2*x+3)', bornes=[0, sympify('3/2')])
        >>> e = TableauSigne('x*(2-3*x)') # bug sur x factor corrigé.
        >>> f = TableauSigne('3*x+1') # expression du 1er degré prise en compte
    """
    def _splitDiv(self, a):
        b = a.args
        if (b[0]).is_Mul:
            T = [e**b[1] for e in b[0].args]
            return T
        else:
            return [a]

    def __init__(self, expr, bornes=[-oo, oo], niveau=1):
        self.expr = sympify(expr, evaluate=False)
        self.bornes = bornes
        self.niveau = niveau
        self.tab = []
        if self.expr.is_Mul:
            facteurs = self.expr.args
            self.fact_cst = [u for u in facteurs if u.is_Number]
            ## facteur x seul, non traité ailleurs. en principe 1 seul résultat possible.
            self.fact_x = [u for u in facteurs if u.is_Symbol]
            ## facteurs puissance >=2 -> racines
            self.pow_plus = [u for u in facteurs if (u.is_Pow and u.args[1]>1)]
            ## facteurs simples ->
            self.pow_simple = [u for u in facteurs if u.is_Add]
            self.pow_positif = self.pow_plus +list(self.pow_simple) + list(self.fact_x)
            #[u.args[0] for u in self.pow_plus] +list(self.pow_simple) + list(self.fact_x)
            ## facteurs puissance négative -> vi
            ## ils tombent dans un des arguments avec une puissance -1
            ## on resympify avec evaluate à True par défaut
            tmp = [self._splitDiv(e) for e in facteurs if e.is_Pow and e.args[1]<0]
            self.pow_moins  = reduce(lambda a,b: a+b, tmp)
            self.facteurs = self.fact_cst + self.pow_positif + self.pow_moins
        elif self.expr.is_Add and (degree(self.expr) == 1): 
            # cas d'un seul facteur de degré 1:
            self.facteurs = self.pow_positif = [self.expr]
            self.pow_moins = []
        elif self.expr.is_Symbol:
            # cas de l'expression 'x' tout court, is_Add False, mais is_Symbol True
            self.facteurs = self.pow_positif = [self.expr]
            self.pow_moins = []
        try:
            self.racines = reduce(operator.concat,
                                  [solve(u,x) for u in list(self.pow_positif)])
        except TypeError:
            self.racines = []
        try:
            self.vi = reduce(operator.concat,
                             [solve(u.args[0],x) for u in list(self.pow_moins)]) # valeurs interdites
        except TypeError:
            self.vi = []
            
        self._create_tab()
        self._create_tab_nosign(niveau = niveau)
        self._arbrepst()

    def _arbrepst(self):
        """Création de l'arbre xml, de l'arbre simplifié selon le format de PST+;
        de l'arbre xml version nosign (les +- sont remplacés par …
        stockés dans self.xml, self.xmlsimplif, self.xmlnosign

        """
        root = etree.Element("Tableau")
        root_simplif = etree.Element("Tableau")
        root_nosign =  etree.Element("Tableau")
        ligne = etree.SubElement(root, "Lignes")
        ligne.text = str(len(self.tab))

        ligne_simplif = etree.SubElement(root_simplif, "Lignes")
        ligne_simplif.text = '2'

        ligne_nosign = etree.SubElement(root_nosign, "Lignes")
        ligne_nosign.text = str(len(self.tabnosign))

        col = etree.SubElement(root, "Colonnes")
        col.text = str(len(self.tab[0]["Milieu"]))

        col_simplif = etree.SubElement(root_simplif, "Colonnes")
        col_simplif.text = col.text

        col_nosign = etree.SubElement(root_nosign, "Colonnes")
        col_nosign.text = str(len(self.tabnosign[0]["Milieu"]))

        for l in self.tab:
            for e in ["Bas", "Milieu", "Haut"]:
                etree.SubElement(root, e).text =\
                    regexp.sub(r'\$',
                               r'',
                               self._list2pststring(l[e]))

        self.xml = root
        for l in (self.tab[0], self.tab[-1]):
            for e in ["Bas", "Milieu", "Haut"]:
                etree.SubElement(root_simplif, e).text =\
                    regexp.sub(r'\$',
                               r'',
                               self._list2pststring(l[e]))
        self.xmlsimplif = root_simplif
        for l in self.tabnosign:
            for e in ["Bas", "Milieu", "Haut"]:
                etree.SubElement(root_nosign, e).text =\
                    regexp.sub(r'\$',
                               r'',
                               self._list2pststring(l[e]))

        self.xmlnosign = root_nosign

        
    def _list2pststring(self, l):
        # disparition du + dans le cas de latex(+oo)
        return reduce(lambda u,v: str(u)+"#"+(latex(v)
                                              if (v!=oo) else '+\\infty'), l)
    
    def _fill_ligne(self, tete, facteur):
        """ Construction de la ligne des signes concernant facteur
        relativement à la ligne tete.

        tete contient la ligne d'entete du tableau.
        facteur est l'expression dont on veut étudier le signe.

        On renvoie un dictionnaire avec les clés Haut Milieu Bas pour faciliter
        la traduction dans pst+.

        Le remplissage des signes est traditionnel: observer le coef dir et
        remplir en conséquence.

        """
        l = len(tete)
        out = {"Haut": l*["vide"], "Milieu": l*["vide"],
               "Bas":l*["vide"]}
        signe = {1:"+", -1:"-"}
        grid = [r for r in self.racines+self.vi 
                if (r >= self.bornes[0]) and (r <= self.bornes[1])]
        # barres de positions
        for v in grid:
            i = tete.index(v)
            out["Haut"][i] = "|"
            out["Milieu"][i] = "|"
            out["Bas"][i] = "|"
        # titre de la ligne
        if facteur.is_Pow:
            out["Milieu"][0] = latex( Pow(facteur.args[0],
                                          abs(facteur.args[1])))
        else:
            out["Milieu"][0] = latex(facteur)

        #cas d'une constante
        if facteur.is_Number:
            for i in range(l):
                if tete[i] == "vide":
                    out["Milieu"][i] = signe[int(sign(facteur))]
        #Autres: puissances paires
        elif facteur.is_Pow and facteur.args[1]%2 == 0:
            r = solve(Eq(facteur.args[0],0),x)[0] # solve renvoie une liste
            try:
                i0 = tete.index(r) # position de la racine r du facteur
                out["Milieu"][i0] = 0
                tmp = list(range(1,l))
                tmp.remove(i0)
            except ValueError:
                tmp = list(range(1,l))
            for i in tmp:
                if tete[i]=="vide":
                    out["Milieu"][i] = signe[1]
        #Autres à améliorer suivant puissance
        else:
            if facteur.is_Pow:
                f,p = facteur.args
            elif facteur.is_Add:
                f,p = facteur, 1
            elif facteur.is_Symbol:
                f,p = facteur, 1
            # position du zéro
            r = solve(Eq(f,0),x)[0] # solve renvoie une liste (peut-être vide)
            a = int(sign(diff(f, x))) # signe coeff dir
            try:
                i0 = tete.index(r) # position de la racine r du facteur
                # out["Bas"][i0] = "|" déjà fait à l'initialisation
                out["Milieu"][i0] = 0
                # out["Haut"][i0] = "|"
                # remplissage signe
                for i in range(i0):
                    if tete[i]=="vide":
                        out["Milieu"][i] = signe[-a]
                for i in range(i0+1, l):
                    if tete[i]=="vide":
                        out["Milieu"][i] = signe[a]
            except ValueError:
                if r < self.bornes[0]:
                    for i in range(1,l):
                        if tete[i]=="vide":
                            out["Milieu"][i] = signe[a]
                elif r > self.bornes[1]:
                    for i in range(1,l):
                        if tete[i]=="vide":
                            out["Milieu"][i] = signe[-a]

        return out

    def _fill_last_ligne(self, tete, nom="f"):
        """Création de la dernière ligne du tableau par la règle des signes.
        """
        signe = {1:"+", -1:"-"}
        l = len(tete)
        out = {"Haut": l*["vide"], "Milieu": l*["vide"],
               "Bas":l*["vide"]}
        out["Milieu"][0] = "\\text{signe de }"+nom
        for i in range(1,l):
            if tete[i] == "vide":
                #récupérer les signes sauf 1ere ligne
                tmp = [x["Milieu"][i] for x in self.tab[1:]]
                out["Milieu"][i] = signe[int((-1)**(tmp.count("-")%2))]
            elif tete[i] in self.racines:
                out["Milieu"][i] = 0
                out["Haut"][i] = "|"
                out["Bas"][i] = "|"
            elif tete[i] in self.vi:
                out["Milieu"][i] = "||"
                out["Haut"][i] = "||"
                out["Bas"][i] = "||"
        return out
            
    def _create_tab(self):
        """Création du tableau de signe disponible dans self.tab et 
        du tableau de signe simplifié disponible dans self.tabsimplif
        """
        # c'est plus pratique pour insérer les vides
        values = [r for r in self.racines+self.vi
                  if (r > self.bornes[0]) and (r< self.bornes[1])]\
                     + [self.bornes[1]]
        values.sort()
        tete = ["x", self.bornes[0]]+reduce(operator.concat,
                                            [["vide", u] for u in values])
        self.tab = [{"Haut": len(tete)*["vide"], "Milieu": tete,
                     "Bas": len(tete)*["vide"]}]
        for f in self.facteurs: # self.pow_positif+self.pow_moins
            self.tab.append(self._fill_ligne(tete, f))
        self.tab.append(self._fill_last_ligne(tete))
        self.tabsimplif = [self.tab[0]]+[self.tab[-1]]

    def _create_tab_nosign(self, niveau=1):
        """Création d'un tableau de signe où les signes, les zéros, les vi 
        sont laissés vides pour êtres complétés. 

        À créer après le tableau de create_tab()
        niveau: 1 ou 2 - 1 on enlève les signes; 2 on enlève aussi les valeurs
                d'annulation
        """
        self.tabnosign = deepcopy(self.tab)
        for i,e in enumerate(self.tabnosign):
            if i==0 and niveau==1:
                pass
            elif i==0 and niveau==2:
                # recalcul de l'entête en mettant des … sauf aux bords
                values = [r for r in self.racines+self.vi \
                      if (r > self.bornes[0]) and (r< self.bornes[1])]
                values.sort()
                tete = ["x", self.bornes[0]]+reduce(operator.concat, \
                                    [["vide","\\dots"] for u in values])\
                                    +["vide",self.bornes[1]]
                self.tabnosign[i]["Milieu"] = tete
            else:
                L = e["Milieu"]
                self.tabnosign[i]["Milieu"] = [(x if not(x == '+' or x =='-')
                                                else '\\dots') for x in L]

    def _fill_ligne_tkz(self, tete: list, facteur, grid=[], option='whole',
                        grid_sp=[]):
        """construit une ligne tkzTabLine relativement à facteur

        la tete est une liste avec alternance de valeurs et de vides.
        grid est la liste des écritures latex des positions
        grid_sp est la liste des valeurs sympifiées
        
        Le remplissage des signes est traditionnel: observer le coef dir et
        remplir en conséquence.

        """
        l = len(tete)
        out = [""] +(l-2)*["vide"]+[""]
        if option in ['whole', 'simplif']:
            signe = {1:"+", -1:"-", "z": "z", "t": "t", "d": "d"}
        elif option=='nosign':
            signe = {1:"…", -1:"…", "z": "…", "t": "…", "d": "…"}
        N = len(grid)
        # barres de positions sauf aux bords
        # on analyse la grille des valeurs sympifiées grid_sp
        for j,v in enumerate(grid):
            i = tete.index(v)
            if grid_sp[j] in self.racines:
                out[i] = signe["t"]
            elif grid_sp[j] in self.vi:
                out[i] = signe["d"]
        #cas d'une constante
        if facteur.is_Number:
            for i in range(l):
                if tete[i] == "vide":
                    out[i] = signe[int(sign(facteur))]
        #Autres: puissances paires
        elif facteur.is_Pow and facteur.args[1]%2 == 0:
            r = solve(Eq(facteur.args[0],0),x)[0] # solve renvoie une liste
            try:
                i0 = tete.index(r) # position de la racine r du facteur
                out[i0] = signe["z"]
                tmp = list(range(l))
                tmp.remove(i0)
            except ValueError:
                tmp = list(range(l))
            for i in tmp:
                if tete[i]=="vide":
                    out[i] = signe[1]
        #Autres à améliorer suivant puissance
        else:
            if facteur.is_Pow:
                f,p = facteur.args
            elif facteur.is_Add:
                f,p = facteur, 1
            elif facteur.is_Symbol:
                f,p = facteur, 1
            # position du zéro
            r = solve(Eq(f,0),x)[0] # solve renvoie une liste (peut-être vide)
            # signe coeff dir
            a = sign(diff(f, x))
            try:
                i0 = tete.index(f"${latex(r)}$") # position de la racine r
                out[i0] = signe["z"] if p>0 else signe["d"]
                # remplissage signe
                for i in range(i0):
                    if tete[i]=="vide":
                        out[i] = signe[int(-a)]
                for i in range(i0+1,l):
                    if tete[i]=="vide":
                        out[i] = signe[int(a)]
            except ValueError:
                if r < self.bornes[0]:
                    for i in range(l):
                        if tete[i]=="vide":
                            out[i] = signe[int(a)]
                elif r > self.bornes[1]:
                    for i in range(l):
                        if tete[i]=="vide":
                            out[i] = signe[int(-a)]
        return "\\tkzTabLine{" + ' , '.join(out) + "}\n"

    def _fill_last_ligne_tkz(self, tete, nom="f", option='whole'):
        """Création de la dernière ligne du tableau par la règle des signes pour TiKz
        
        on analyse self.tab complètement créé auparavant, on retire la ligne 0
        et la dernière.

        """
        if option in ['whole', 'simplif']:
            signe = {1:"+", -1:"-", "z": "z", "t": "t", "d": "d"}
        elif option=='nosign':
            signe = {1:"…", -1:"…", "z": "…", "t": "…", "d": "…"}
        l = len(tete)
        out = [""]+(l-2)*["vide"]+[""]
        for i in range(l):
            if tete[i] == "vide":
                #récupérer les signes sauf 1ere ligne
                tmp = [x["Milieu"][i+1] for x in self.tab[1:len(self.tab)-1]]
                out[i] = signe[int((-1)**(tmp.count("-")%2))]
            elif tete[i] in self.racines:
                out[i] = signe['z']
            elif tete[i] in self.vi:
                out[i] = signe["d"]
            else: # vider au niveau des bornes
                out[i] = ''
        return "\\tkzTabLine{" + ', '.join(out) + "}\n"

    def _facto_pos(self, f):
        """fonction technique pour affichage des facteurs
        avec puissance toujours positive.
        """
        if f.is_Pow:
            return f"${latex(Pow(sympify(f.args[0]), abs(f.args[1])).simplify())}$"
        else:
            return  f"${latex(f.simplify())}$"
        
    def tab2tkz(self, option='whole', tabopts="nocadre,lgt=2.5,espcl=1.5",
                **kwargs):
        """sortie latex tkz-tab du tableau de signe
        
        :param string option: in ['whole', 'simplif', 'nosign']

        * 'simplif': utiliser le tableau simplifié
          qui ne comporte que la 1ere et la dernière ligne.
        * 'nosign': générer le tableau avec pointillés à compléter 
          (le niveau de difficulté 1 ou 2 a été réglé à l'initialisation)
        * 'whole': tableau complet normal

        """
        # début construction: Tabinit
        col1 = ["$x$"] + list(map(lambda e: self._facto_pos(e),
                                  self.pow_positif+self.pow_moins))\
            + ['signe de $f(x)$']
        C1 = list(map(lambda e: f"{e} /0.8", col1))

        # c'est plus pratique pour insérer les vides
        values = [r for r in self.racines+self.vi
                  if (r > self.bornes[0]) and (r< self.bornes[1])]
        values.sort()
        # garder une version sympifiée des valeurs
        VALS = [self.bornes[0]] + values + [self.bornes[1]]
        tete = [f"${latex(self.bornes[0])}$"] +\
            list(map(lambda e: f"${latex(e)}$", values)) + \
            [f"${'+' if self.bornes[1]==oo else ''}{latex(self.bornes[1])}$"]
        # tete = [f"${latex(self.bornes[0])}$"]+ values
        V_spc = reduce(lambda a,b: a +[b, "vide"], VALS, [])[:-1]
        # enlever le dernier vide
        tete_spc = reduce(lambda a,b: a +[b, "vide"], tete, [])[:-1]
        # dernier "vide" superflu
        OUT = "%\\usepackage{tkz-tab}\n\\begin{tikzpicture}\n"
        OUT += f"\\tkzTabInit[{tabopts}]{{{(' ,'+chr(10)).join(C1)}}}{{{' , '.join(tete)}}}\n"
        if option in ['whole', 'nosign']:
            for f in self.facteurs: # self.pow_positif+self.pow_moins
                LINE = self._fill_ligne_tkz(tete_spc, f, grid=tete, option=option,
                                            grid_sp=VALS)
                OUT += LINE
        OUT += self._fill_last_ligne_tkz(V_spc, option=option)
        OUT += "\\end{tikzpicture}"
        return OUT
      
    def tab2latex(self, option='whole', **kwargs):
        """Sortie latex tabvar du tableau de signe. 

        Il utilise le fichier tabvar.tex comme suggéré par pstplus.
        
        :param string option: in ['whole', 'simplif', 'nosign']

        * 'simplif': utiliser le tableau simplifié
          qui ne comporte que la 1ere et la dernière ligne.
        * 'nosign': générer le tableau avec pointillés à compléter 
          (le niveau de difficulté 1 ou 2 a été réglé à l'initialisation)
        * 'whole': tableau complet normal

        exemple::

            >>> a = TableauSigne('-1*(3*x+2)*(-5*x +4)')
            >>> print(a.tab2latex())
            $$\\tabvar{%
            \\tx{x} & \\tx{-\\infty} &  & \\tx{- \\frac{2}{3}} &  & \\tx{\\frac{4}{5}} &  & \\tx{+\\infty}\\cr
            \\tx{- 3 x -2} &  & \\tx{+} & \\txt{0} & \\tx{-} & \\tx{|} & \\tx{-} & \\cr
            \\tx{- 5 x + 4} &  & \\tx{+} & \\tx{|} & \\tx{+} & \\txt{0} & \\tx{-} & \\cr
            \\tx{\\text{signe de }f} &  & \\tx{+} & \\txt{0} & \\tx{-} & \\txt{0} & \\tx{+} & \\cr}$$
        """
        # choix du tableau
        if option=='simplif':
            T = self.tabsimplif
        elif option=='nosign':
            T = self.tabnosign
        else: #option=='whole'
            T = self.tab
        # appliquer plusieurs substitution sur les éléments d'une ligne
        trad = {'+': '\\tx{+}',
                '-': '\\tx{-}',
                '|': '\\trait',
                '||': '\\dbt',
                0: '\\txt{0}',
                '\\dots': '\\tx{\\dots}',
                'vide': ''}
        out = "$$\\tabvar{%"
        #traitement à part pour la 1ere ligne
        out +="\n"
        L = ["\\tx{" + (latex(x) if x!= oo else '+\\infty') + "}"
             for x in T[0]["Milieu"]]
        # enlever les 'vide'
        L2 = [a if (a != '\\tx{vide}') else '' for a in L]
        out += reduce(lambda u,v:  u + " & " + v , L2)
        out += "\cr"
        #autres lignes
        for i,l in enumerate(T[1:]):
            out +="\n"
            L = ["\\tx{"+l["Milieu"][0]+"}"] + [trad[x]
                                                for x in l["Milieu"][1:]]
            out += " & ".join(L)
            out += "\cr"
        out += "}$$"
        return out

    def _create_latex_intervalle(self, choix, L, take):
        """renvoie l'intervalle au format latex

        choix est dans la liste ['++' , '+0', '--', '-0']
        L est une liste de taille 2
        take est la liste des || ou 0
        """
        out = ''
        if L[0] == -oo:
            out += '\\left] -\\infty;'
        elif take[0]=="||" or choix[1] in ('+','-'):
            out += '\\left] '+latex(L[0]) + ';'#ne pas prendre la borne si stt+ ou-
        else:
            out += '\\left[ '+latex(L[0]) + ';'
        if L[1] == +oo:
            out += '+\\infty \\right['
        elif take[1] == "||"  or choix[1] in ('+','-'):
            out += latex(L[1])+'\\right[' # ne pas prendre la borne
        else:
            out += latex(L[1])+'\\right]'
        return out

    def _get_pm(self, signe):
        S = self.tab[-1]['Milieu']
        positions = [ i for i,x in enumerate(S) if x==signe]
        datas = [(self.tab[0]['Milieu'][i-1:i+2:2],
                  self.tab[-1]['Milieu'][i-1:i+2:2]) for i in positions]
        return datas

    def get_solutions(self, choix:str) -> str:
        """renvoie les solutions d'une inéquation au format latex
        
        choix est dans ['++', '+0', '-\-', '-0'] pour signifier strictement 
        positif ou pas

        :param string choix: nature de l'inéquation ['++', '+0', '-\-', '-0']

        exemple::

            >>> a = TableauSigne('-1*(3*x+2)*(-5*x +4)')
            >>> print(a.get_solutions('+0'))
            \left] -\infty;- \\frac{2}{3}\\right]\cup \left[ \\frac{4}{5};+\\infty \\right[
        """
        paires = self._get_pm(choix[0])
        if paires == []:
            return "\\emptyset"
        else:
            intervs = [self._create_latex_intervalle(choix, x[0], x[1])
                       for x in paires]
            I = reduce(lambda a,b: a+'\\cup '+b, intervs[1:], intervs[0])
            return I

    def export_pst(self, nom="tableau", ext="pag", option='simplif', sign=True):
        """Exporter l'arbre xml dans un fichier. Format pag ou pst.
        """
        f = f"{nom}.{ext}"
        if not(sign):
            choix = self.xmlnosign
        elif option == 'simplif':
            choix = self.xmlsimplif
        else:
            choix = self.xml
        #choix ={True: self.xmlsimplif, False: self.xml}
        out = open(f, 'w')
        out.write( etree.tostring(choix, pretty_print=True).decode("utf-8") )
        out.close()

    def export_latex(self, nom="tableau", option='whole', ext="tex"):
        """Exporter la sortie latex dans un fichier. Format tex.
        
        :param ext: pour compatibilite avec export_pst
        :type ext: str in 'tex', 'pag', 'pst'
        :param option: 'simplif', 'whole', 'nosign' 

        par défaut on laisse des +- pour mettre des … pour faire un énoncé
        de tableau à compléter.
        """
        f = f"{nom}.{ext}"
        out = open(f, 'w')
        out.write( self.tab2latex(option=option) )
        out.close()

    def export_tikz(self, nom="tableau", option='whole', ext="tkz"):
        """Exporter la sortie dans un fichier. Format tex TikZ.
        
        :param ext: pour compatibilite avec export_pst
        :type ext: str in 'tex', 'pag', 'pst'
        :param option: 'simplif', 'whole', 'nosign' 

        par défaut on laisse des +- pour mettre des … pour faire un énoncé
        de tableau à compléter.
        """
        f = f"{nom}.{ext}"
        out = open(f, 'w')
        out.write( self.tab2tkz(option=option) )
        out.close()
        
# class TableauVariation(TableauSigne):
#     """
#     Classe de creation d'un tableau de variation. Ce n'est qu'une heuristique,
#     l'emplacement des flèches doit être remanié à la main dans pstplus.
#     Les bornes par défaut sont \pm oo réglable avec le paramètre bornes.
# 
#     :param string expr: expression à étudier; avec la syntaxe sympy.
#     :param list bornes: liste à deux éléments pour les bornes. [-oo, oo] par défaut
# 
#     exemple::
# 
# 
#         >>> a = TableauVariation('-1*(3*x+2)*(-5*x +4)')
#         >>> a.arbrepst()
#         >>> print(etree.tostring(a.xml, pretty_print=True))
#     """
# 
#     def __init__(self, expr, *args):
#         """
#         :type expr: string
#         :param expr: l'expression dont on veut dresser le tableau de variation
# 
#         """
#         self.val = sympify(expr)
#         deriv = factor(self.val.diff())
#         TableauSigne.__init__(self, str(deriv), *args)
# 
#     def _sens(self,s):
#         if s == "+":
#             return "/"
#         elif s == "-":
#             return "\\"
#         else:
#             return s
# 
#     def _convert(self, s, i):
#         """indique la position et le symbole / ou \ à partir d'un triplet du tableau de signe
# 
#         """
#         try:
#             return {"+0+": ("Bas", "/"),
#                 "+0-": ("Milieu","/"),
#                 "-0+": ("Milieu", "\\"),
#                 "-0-": ("Haut","\\"),
#                 "0+vide": ("Milieu","f("+latex(self.tab[0]["Milieu"][i])+")"),
#                 "0-vide": ("Milieu","f("+latex(self.tab[0]["Milieu"][i])+")"),
#                 "0+0": ("Milieu","f("+latex(self.tab[0]["Milieu"][i])+")"),
#                 "0-0": ("Milieu","f("+latex(self.tab[0]["Milieu"][i])+")"),
#                 "vide+0": ("Milieu", "vide"),
#                 "vide-0": ("Milieu", "vide")}[s]
#         except KeyError:
#             pass
# 
#     def complete_tab(self):
#         """Création du tableau de signe de f' et ajout des variations de f.
# 
#         """
#         #self._create_tab()
#         signe = self.tab[-1]["Milieu"]
#         #var = {"Haut": len(signe)*["vide"], "Milieu": map(self._sens, signe), "Bas": len(signe)*["vide"]}
#         var = {"Haut": len(signe)*["vide"], "Milieu": len(signe)*["vide"], "Bas": len(signe)*["vide"]}
#         var["Haut"][0] = var["Bas"][0] = ""
#         var["Milieu"][0] = "\\text{sens de }f"
#         # TODO: valeurs extremales locales à configurer
#         for i in range(1, len(signe)-2):
#             position, symbole = self._convert(reduce(lambda x,y: str(x)+str(y), signe[i:i+3]), i)
#             var[position][i] = symbole
#         self.tab.append(var)
# 
#     def export(self, nom="tableau"):
#         """Exporter l'arbre xml dans un fichier
# 
#         """
#         self.complete_tab()
#         self.arbrepst()
#         #
#         f = nom+".pst"
#         out = open(f, 'w')
#         out.write( etree.tostring(self.xml, pretty_print=True) )
#         out.close()


class TableauFactory(list):
    """Génère une liste de tableaux de signe.
    On peut à l'envie générer une liste de solutions d'inéquations ...

    exemple::

      >>> test = ['(3*x+2)', '(5*x+4)*(2*x+8)', '(9*x-3)/(5*x-1)']
      >>> t = TableauFactory(test)
      >>> t.export_pst(option='whole', ext='pag')
      >>> t.export_latex(option='simplif')
      >>> for e in t: print(e.get_solutions('++'))
      \\left] - \\frac{2}{3};+\\infty \\right[
      \\left] -\\infty;-4\\right[\\cup \\left] - \\frac{4}{5};+\\infty \\right[
      \\left] -\\infty;\\frac{1}{5}\\right[\\cup \\left] \\frac{1}{3};+\\infty \\right[
      >>> t2 = TableauFactory([randExpr(3) for i in range(2)])
      >>> for x in t2: print(latex(x.expr)+'\\n'+ x.tab2latex(option='simplif')+'\\n')
      - \\frac{4 x + 1}{x \\left(- 3 x -2\\right)}
      $$\\tabvar{%
      \\tx{x} & \\tx{-\\infty} &  & \\tx{- \\frac{2}{3}} &  & \\tx{- \\frac{1}{4}} &  & \\tx{0} &  & \\tx{+\\infty}\\cr
      \\tx{\\text{signe de }f} &  & \\tx{-} & \\dbt & \\tx{+} & \\txt{0} & \\tx{-} & \\dbt & \\tx{+} & \\cr}$$
      3 \\frac{x}{\\left(x -3\\right) \\left(2 x -4\\right)}
      $$\\tabvar{%
      \\tx{x} & \\tx{-\\infty} &  & \\tx{0} &  & \\tx{2} &  & \\tx{3} &  & \\tx{+\\infty}\\cr
      \\tx{\\text{signe de }f} &  & \\tx{-} & \\txt{0} & \\tx{+} & \\dbt & \\tx{-} & \\dbt & \\tx{+} & \\cr}$$
      
    """

    def __init__(self, L, M=None):
        """initialisation

        L: liste d'expressions
        M: liste de dictionnaires d'options de même taille que L
         notamment on peut y mettre l'option niveau
        """
        if M == None:
            for e in L:
                self.append(TableauSigne(e))
        else:
            for i,e in enumerate(L):
                self.append(TableauSigne(e, **(M[i])))

    def export_pst(self, option='simplif', ext="pag"):
        """créer les fichiers sortie au format pag/pst avec option 
        de simplification (False par défaut)

        :param boolean simplif: simplifier les tableaux ou pas
        :param string ext: extension de la sortie pag (pdfadd) pst (pstplus)

        """
        for i,t in enumerate(self):
            t.export_pst(nom="tableau"+str(i+1), option=simplif, ext=ext)

    def export_latex(self, nom="tableaux_liste", option='whole', ext="tex"):
        """créer la sortie latex des tableaux dans un seul fichier avec option 
        de simplification.

        :param string nom: le nom de la sortie .tex
        :param string option: in ['whole', 'simplif', 'nosign']
        :param string ext: extension de la sortie (pour compatibilité)

        * 'simplif': utiliser le tableau simplifié qui ne comporte que la 1ere 
          et la dernière ligne.
        * 'nosign': générer le tableau avec pointillés à compléter (le niveau 
          de difficulté 1 ou 2 a été réglé à l'initialisation) 
        * 'whole': tableau complet normal
        """
        f = f"{nom}.{ext}"
        out = open(f, 'w')
        for t in self:
            out.write( t.tab2latex(option=option))
            out.write('\n\n')
        out.close()

def _genListeCoef(n=2, a=-5, b=5, nopower=True, vals=None):
    """Constuire la liste des [ai, bi] pour générer les facteurs (ai*x +bi)"""
    # tester toutes les colinéarités 2 à 2
    multiplicateur = 4  
    if nopower:
        nocolin = False
        while not(nocolin):
            if vals:
                tmpC = [choice([-1,1])* randint(1, multiplicateur)
                        for i in range(len(vals))]
                Atmp = [ [tmpC[i], -tmpC[i]*e] for i,e in enumerate(vals)]
                Areste = [[choice([-1,1])* randint(1, b), randint(a,b)]
                          for i in range(n-len(vals))]
                A = Atmp+Areste
            else:
                A = [[choice([-1,1]) * randint(1, b), randint(a,b)]
                     for i in range(n)]
            # tester toutes les colinéarités 2 à 2
            nocolin = True
            for i in range(n):
                for j in range(i+1, n):
                    # calcul de colinéarité
                    if det(Matrix([A[i], A[j]])) == 0:
                        nocolin = False
                        break
    else:
        if vals:
            tmpC = [choice([-1,1])* randint(1, multiplicateur)
                    for i in range(len(vals))]
            Atmp = [ [tmpC[i], -tmpC[i]*e] for i,e in enumerate(vals)]
            Areste = [[choice([-1,1])* randint(1, b), randint(a,b)]
                      for i in range(n-len(vals))]
            A = Atmp+Areste
        else:
            # le 1er terme du couple est un coef directeur, doit être non nul
            A = [[choice([-1,1])*randint(1, b), randint(a,b)]
                 for i in range(n)]
    return A

def randExpr(n=2, a=-5, b=5, denomin=True, nopower=True, vals=None):
    """créer aléatoirement une expression avec n facteurs du 1er degré à coef
    entiers compris entre a et b. Le placement au numérateur/dénominateur se
    fait aussi au hasard.
    Attention, si nopower est activé, il faut b-a>sqrt(n).

    :param int n: le nombre de facteurs, 2 par défaut
    :param int a: borne inférieure des coefs, -5 par défaut
    :param int b: borne supérieure des coefs, 5 par défaut
    :param boolean/int denomin: autoriser des expressions au dénominateur, True par défaut
       on autorise un int entre 0 et n pour désigner le nombre de coefs qu 'on veut au dénominateur
    :param list vals: liste de zéros ou vi de taille <= n. Biensûr, vous savez ce que vous faites, vous
       ne pouvez proposer plusieurs fois la même (en contradiction avec nopower)

    exemple::

      >>> randExpr(2)
      (-x + 2)/(2*x + 3)
      >>> randExpr(3,-15,15)
      (-3*x + 2)*(14*x - 10)/(5*x - 14)
      >>> randExpr(5, denomin=3, vals=[-4,2,3])
      (-3*x - 3)*(4*x - 3)/((8 - 4*x)*(9 - 3*x)*(-4*x - 16))
    """
    ope = (['/','*'] if denomin else ['*'])
    A = _genListeCoef(n, a, b, nopower, vals)
        
    #F = [(random_poly(x, 1, a,b, polys=False), choice(ope)) for i in range(n)]
    if type(denomin)==bool:
        F = [(x*e[0]+e[1], choice(ope)) for e in A]
    elif type(denomin)==int:
        OPS = denomin*['/'] + (n-denomin)*['*']
        F = [(x*e[0]+e[1], OPS[i]) for i,e in enumerate(A)]
    out = sympify(reduce(lambda a,b: f"{a+b[1]}({str(b[0])})", F, '1'))
    # sadly certains facteurs "colinéaires" pourraient se neutraliser
    # ce cas ne se produit pas si nopower est activé
    while (n>=2 and (degree(Poly(numer(out), x))
                     + degree(Poly(denom(out), x)) != n)):
        F = [(random_poly(x, 1, a, b, polys=False), choice(ope))
             for i in range(n)]
        # besoin de sympifier pour des expressions avec fractions…
        #out = sympify(reduce(lambda a,b: a+b[1]+'('+str(b[0])+')', F, '1'))
        out = reduce(lambda a,b: f"{a+b[1]}({str(b[0])})", F, '1')
    return out

