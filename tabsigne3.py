#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2013 Boris MAURICETTE
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; (GNU GPL v3)
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


__doc__ = """
Classe de création de tableau de signe à l'aide de sympy et lxml.
Elle génère au choix la sortie latex ou un tableau xml à lancer dans pst+.

"""
import operator
import re as regexp
from random import choice
from sympy import *
from lxml import etree
from functools import reduce

x = var('x')
version = '0.9.3'

class TableauSigne():
    """
    Classe de creation du tableau de signe.
    Les bornes par défaut sont \pm oo réglable avec le paramètre bornes.

    :param string expr: expression à étudier, sous forme d'un produit ou quotient; avec la syntaxe sympy.
    :param list bornes: liste à deux éléments pour les bornes. [-oo, oo] par défaut

    exemple::

        >>> a = TableauSigne('-1*(3*x+2)*(-5*x +4)')
        >>> b = TableauSigne('(3*x+2)**3 /(2*x - 5)**2 *(5*x+1) * -8')
        >>> b.export_pst(nom="SuperTest", simplif=False, ext='pag')
        >>> c = TableauSigne('(3*x+2)**3 /(2*x - 5)**2 *(5*x+1) * -8', bornes=[-1, 1])
        >>> d = TableauSigne('(-4*x+4)/(-2*x+3)', bornes=[0, sympify('3/2')])
        >>> e = TableauSigne('x*(2-3*x)') # bug sur x factor corrigé.
        >>> f = TableauSigne('3*x+1') # expression du 1er degré prise en compte

    """
    def __init__(self, expr, bornes = [-oo, oo]):
        self.expr = sympify(expr)
        self.bornes = bornes
        self.tab = []
        if self.expr.is_Mul:
            self.facteurs = self.expr.args
            self.fact_cst = [u for u in self.facteurs if u.is_Number]
            ## facteur x seul, non traité ailleurs. en principe 1 seul résultat possible.
            self.fact_x = [u for u in self.facteurs if u.is_Symbol]
            ## facteurs puissance >=2 -> racines
            self.pow_plus = [u for u in self.facteurs if (u.is_Pow and u.args[1]>1)]
            ## facteurs simples ->
            self.pow_simple = [u for u in self.facteurs if u.is_Add]
            ## tous les facteurs positifs rammenés à puissance 1
            self.pow_positif = [u.args[0] for u in self.pow_plus] +list(self.pow_simple) + list(self.fact_x)
            ## facteurs puissance négative -> vi
            self.pow_moins = [u for u in self.facteurs if u.is_Pow and u.args[1]<0]
        elif self.expr.is_Add and (degree(self.expr) == 1): 
            # cas d'un seul facteur de degré 1:
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
        self._arbrepst()

    def _arbrepst(self):
        """Création de l'arbre xml et de l'arbre simplifié selon le format de PST+;
        stockés dans self.xml, self.xmlsimplif

        """
        root = etree.Element("Tableau")
        root_simplif = etree.Element("Tableau")
        ligne = etree.SubElement(root, "Lignes")
        #ligne.text = str(len(self.facteurs)+2)
        ligne.text = str(len(self.tab))
        col = etree.SubElement(root, "Colonnes")
        #col.text = str(2*len(self.racines)+2*len(self.vi)+4)
        col.text = str(len(self.tab[0]["Milieu"]))

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

    def _list2pststring(self, l):
        # disparition du + dans le cas de latex(+oo)
        return reduce(lambda u,v: str(u)+"#"+(latex(v) if (v!=oo) else '+\\infty'), l)
    
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
        out = {"Haut": l*["vide"], "Milieu": l*["vide"],\
                   "Bas":l*["vide"]}
        signe = {1:"+", -1:"-"}
        #grid = filter(lambda u: not (u in ["vide", "x", -oo, oo]+self.bornes), tete)
        grid = [r for r in self.racines+self.vi \
                      if (r >= self.bornes[0]) and (r <= self.bornes[1])]
        # barres de positions
        for v in grid:
            i = tete.index(v)
            out["Haut"][i] ="|"
            out["Milieu"][i] ="|"
            out["Bas"][i] ="|"
        # titre de la ligne
        if facteur.is_Pow:
            out["Milieu"][0] = latex( Pow(facteur.args[0], abs(facteur.args[1])))
        else:
            out["Milieu"][0] = latex(facteur)

        #cas d'une constante
        if facteur.is_Number:
            for i in range(l):
                if tete[i]=="vide":
                    out["Milieu"][i] = signe[int(sign(facteur))]
        #Autres: puissances paires
        elif facteur.is_Pow and facteur.args[1]%2 == 0:
            r = solve(Eq(facteur.args[0],0),x)[0] # solve renvoie une liste (peut-être vide)
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
            # signe coeff dir
            a = sign(diff(f, x))
            try:
                i0 = tete.index(r) # position de la racine r du facteur
                # out["Bas"][i0] = "|" déjà fait à l'initialisation
                out["Milieu"][i0] = 0
                # out["Haut"][i0] = "|"
                # remplissage signe
                for i in range(i0):
                    if tete[i]=="vide":
                        out["Milieu"][i] = signe[int(-a)]
                for i in range(i0+1,l):
                    if tete[i]=="vide":
                        out["Milieu"][i] = signe[int(a)]
            except ValueError:
                if r < self.bornes[0]:
                    for i in range(1,l):
                        if tete[i]=="vide":
                            out["Milieu"][i] = signe[int(a)]
                elif r > self.bornes[1]:
                    for i in range(1,l):
                        if tete[i]=="vide":
                            out["Milieu"][i] = signe[int(-a)]

        return out

    def _fill_last_ligne(self, tete, nom="f"):
        """ Création de la dernière ligne du tableau par la règle des signes.

        """
        signe = {1:"+", -1:"-"}
        l = len(tete)
        out = {"Haut": l*["vide"], "Milieu": l*["vide"],\
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
        #values = self.racines+self.vi + 2eme borne
        # c'est plus pratique pour insérer les vides
        values = [r for r in self.racines+self.vi \
                      if (r > self.bornes[0]) and (r< self.bornes[1])] \
                      + [self.bornes[1]]
        values.sort()
        tete = ["x", self.bornes[0]]+reduce(operator.concat, \
                                    [["vide",u] for u in values])
        self.tab = [{"Haut": len(tete)*["vide"], "Milieu": tete, "Bas": len(tete)*["vide"]}]
        for f in self.facteurs:
            self.tab.append(self._fill_ligne(tete, f))
        self.tab.append(self._fill_last_ligne(tete))
        self.tabsimplif = [self.tab[0]]+[self.tab[-1]]


    def tab2latex(self, simplif = False):
        """Sortie latex du tableau de signe. Il utilise le fichier tabvar.tex comme 
        suggéré par pstplus.

        :param boolean simplif: utiliser le tableau simplifié, par défaut False.

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
        if simplif:
            T = self.tabsimplif
        else:
            T = self.tab
        # appliquer plusieurs substitution sur les éléments d'une ligne
        trad = {'+': '\\tx{+}', \
                     '-': '\\tx{-}',\
                     '|': '\\tx{|}',\
                     '||': '\\dbt',\
                     0: '\\txt{0}',\
                    'vide': ''}
        out = "$$\\tabvar{%"
        #traitement à part pour la 1ere ligne
        out +="\n"
        L = ["\\tx{"+(latex(x) if x!= oo else '+\\infty')+"}" for x in T[0]["Milieu"]]
        # enlever les 'vide'
        L2 = [a if (a != '\\tx{vide}') else '' for a in L]
        out += reduce(lambda u,v:  u + " & " + v , L2)
        out += "\cr"

        #autres lignes
        for i,l in enumerate(T[1:]):
            out +="\n"
            L = ["\\tx{"+l["Milieu"][0]+"}"] + [trad[x] for x in l["Milieu"][1:]]
            out += reduce(lambda u,v:  u + " & " + v , L)
            out += "\cr"
        out += "}$$"
        return out


    def _create_latex_intervalle(self,choix, L, take):
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
        datas = [(self.tab[0]['Milieu'][i-1:i+2:2],\
                        self.tab[-1]['Milieu'][i-1:i+2:2]) for i in positions]
        return datas

    def get_solutions(self, choix):
        """renvoie les solutions d'une inéquation au format latex
        choix est dans ['++', '+0', '-\-', '-0'] pour signifier strictiment positif ou pas

        :param string choix: nature de l'inéquation ['++', '+0', '-\-', '-0']

        exemple::

            >>> a = TableauSigne('-1*(3*x+2)*(-5*x +4)')
            >>> print(a.get_solutions('+0'))
            \left] -\infty;- \\frac{2}{3}\\right]\cup \left[ \\frac{4}{5};+\\infty \\right[

        """

        paires = self._get_pm(choix[0])
        intervs = [self._create_latex_intervalle(choix, x[0], x[1]) for x in paires]
        I = reduce(lambda a,b: a+'\\cup '+b, intervs[1:], intervs[0])
        return I

    def export_pst(self, nom="tableau", ext="pag", simplif = False):
        """Exporter l'arbre xml dans un fichier. Format pag ou pst.

        """
        #self.arbrepst()
        #
        f = nom+"."+ext
        choix ={True: self.xmlsimplif, False: self.xml}
        out = open(f, 'w')
        out.write( etree.tostring(choix[simplif], pretty_print=True).decode("utf-8") )
        out.close()

    def export_latex(self, nom="tableau", simplif = False, ext = "tex"):
        """Exporter la sortie latex dans un fichier. Format tex.
        paramètre ext pour compatibilite avec export_pst
        """
        #
        f = nom+".tex"
        out = open(f, 'w')
        out.write( self.tab2latex(simplif = simplif) )
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
      >>> t.export_pst(simplif = False, ext='pag')
      >>> t.export_latex(simplif = True)
      >>> for e in t: print(e.get_solutions('++'))
      \\left] - \\frac{2}{3};+\\infty \\right[
      \\left] -\\infty;-4\\right[\\cup \\left] - \\frac{4}{5};+\\infty \\right[
      \\left] -\\infty;\\frac{1}{5}\\right[\\cup \\left] \\frac{1}{3};+\\infty \\right[
      >>> t2 = TableauFactory([randExpr(3) for i in range(2)])
      >>> for x in t2: print(latex(x.expr)+'\\n'+ x.tab2latex(simplif = True)+'\\n')
      - \\frac{4 x + 1}{x \\left(- 3 x -2\\right)}
      $$\\tabvar{%
      \\tx{x} & \\tx{-\\infty} &  & \\tx{- \\frac{2}{3}} &  & \\tx{- \\frac{1}{4}} &  & \\tx{0} &  & \\tx{+\\infty}\\cr
      \\tx{\\text{signe de }f} &  & \\tx{-} & \\dbt & \\tx{+} & \\txt{0} & \\tx{-} & \\dbt & \\tx{+} & \\cr}$$
      
      3 \\frac{x}{\\left(x -3\\right) \\left(2 x -4\\right)}
      $$\\tabvar{%
      \\tx{x} & \\tx{-\\infty} &  & \\tx{0} &  & \\tx{2} &  & \\tx{3} &  & \\tx{+\\infty}\\cr
      \\tx{\\text{signe de }f} &  & \\tx{-} & \\txt{0} & \\tx{+} & \\dbt & \\tx{-} & \\dbt & \\tx{+} & \\cr}$$
      
    """
    def __init__(self, L):
        for e in L:
            self.append(TableauSigne(e))

    def export_pst(self, simplif = False, ext = "pag"):
        """créer les fichiers sortie au format pag/pst avec option 
        de simplification (False par défaut)

        :param boolean simplif: simplifier les tableaux ou pas
        :param string ext: extension de la sortie pag (pdfadd) pst (pstplus)

        """
        for i,t in enumerate(self):
            t.export_pst(nom="tableau"+str(i+1), simplif = simplif, ext = ext)

    def export_latex(self, nom="tableaux_liste", simplif = False, ext = "tex"):
        """créer la sortie latex des tableaux dans un seul fichier avec option
        de simplification.

        :param string nom: le nom de la sortie .tex
        :param boolean simplif: simplifier les tableaux ou pas
        :param string ext: extension de la sortie (pour compatibilite)

        """
        f = nom+"."+ext
        out = open(f, 'w')
        for t in self:
            out.write( t.tab2latex(simplif = simplif))
            out.write('\n\n')
        out.close()


def randExpr(n=2, a=-5, b=5, denomin = True):
    """créer aléatoirement une expression avec n facteurs du 1er degré à coef
    entiers compris entre a et b. Le placement au numérateur/dénominateur se
    fait aussi au hasard.

    :param int n: le nombre de facteurs, 2 par défaut
    :param int a: borne inférieure des coefs, -5 par défaut
    :param int b: borne supérieure des coefs, 5 par défaut
    :param boolean denomin: autoriser des expressions au dénominateur, True par défaut

    exemple::

      >>> randExpr(2)
      (-x + 2)/(2*x + 3)
      >>> randExpr(3,-15,15)
      (-3*x + 2)*(14*x - 10)/(5*x - 14)

    """
    ope = (['/','*'] if denomin else ['*'])
    F = [(random_poly(x, 1, a,b, polys=False), choice(ope)) for i in range(n)]
    out = sympify(reduce(lambda a,b: a+b[1]+'('+str(b[0])+')', F, '1'))
    # sadly certains facteurs "colinéaires" pourraient se neutraliser
    while (n>=2 and (degree(Poly(numer(out),x)) + degree(Poly(denom(out),x)) !=n)):
        F = [(random_poly(x, 1, a,b, polys=False), choice(ope)) for i in range(n)]
        out = sympify(reduce(lambda a,b: a+b[1]+'('+str(b[0])+')', F, '1'))
    return out
