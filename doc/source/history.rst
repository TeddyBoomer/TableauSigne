Historique
----------

Versions:

* 1.4 : nettoyage et ajustement du code et de la documentation.
* 1.3.6 : intégration de l'option 'nosign' et ses 2 niveaux dans l'interface graphique TableauSigneGUI.py.
* 1.3.5 : correctif de propagation des options, nettoyage du code;
* 1.3.1 : propagation des options 'whole' 'simplif 'nosign' dans les exports et les scripts;
  l'activation de nosign dans TableauSigneGUI et TableauSigne manque encore.
* 1.3   : Ajout d'un export de tableau à compléter (option 'nosign' dans TableauSigne.tab2latex).
  Niveau de difficulté à choisir à l'initialisation (niveau 1 ou 2: 1 - juste les signes à remplir; 2-remplir aussi les zéros et valeurs interdites)
  Amélioration de randExpr: l'option 'nopower' garanti qu'il n'y aura pas de facteurs se regroupant en puissances (non colinéarité des couples (coef dir, ord. orig.) deux à deux).
* 1.2   : Restructuration du code (merci Serge!). Test d'existence de PyQt5 pour le script TabSigneGUI.
* 1.1   : Restructuration dans une archive *wheel*, prise en compte des paquets requis, simplification de l'installation. Renommage des scripts sans extension .py
* 1.0   : Correction d'un bug d'export pour les tableaux simplifiés.
* 0.9.9 : Ajout de l'option "Simplifier" dans l'interface graphique. Màj de la documentation. Dernière version alpha avant 1.0
* 0.9.4 : Ajout d'une interface graphique Qt5. Correction d'un bug, l'expression 'x' seule n'était pas traitée.
* 0.9.3 : Ajout de l'extension 'pag' pour les sorties vers pdfadd. Ajout du fichier pdftabvar.tex.
* 0.9.2 : Factorisation du code - disparition des fonctions internes en _simplif, ajout d'un paramètre simplif (True/False). Fonction *_degree_good* retirée suite à commentaire `issue #3970 <http://code.google.com/p/sympy/issues/detail?id=3970>`_
* 0.9 : Ajout de la fonction *randExpr* pour générer aléatoirement des produits/quotients.
        Une fonction annexe *_degree_good* ajoutée suite à un défaut sur la fonction degree de sympy (qui lève une exception quand on lui donne une constante).
	Retrait de la classe TableauVariation qui n'est pas opérationnelle
	Correctif sur le symbole +oo dans l'export pst
	Amélioration de la documentation.
* 0.8 : Amélioration des exports LaTeX et pst avec paramètre simplif.
        La classe TableauFactory tient compte de cela.
	Scripts améliorés avec le module argparse.
* 0.7 : Ajout de l'export LaTeX direct (fonction tab2latex) des objets TableauSigne. oo est bien traduit par +\infty.
* 0.6 : Ajout de l'export du tableau simplifié et du script TabSigneSimplif.
      	Ajout de la fonction get_solutions pour lecture des solutions d'une inéquation (sortie latex).
* 0.5 : Correction d'un bug: le script ne gérait pas les expressions de degré 1 (qui ne sont pas des produits/quotients)
* 0.4 : Correction d'un bug: le script ne tenait pas compte d'un facteur x seul (de type Symbol)
* 0.3 : Correction d'un bug sur les tracés aux bornes.
* 0.2 : paramètre bornes ajouté
* 0.1 : les bornes étaient \pm oo sans possibilité de modification

TODO:

* La classe heuristique TableauVariation n'est pas encore opérationnelle.
