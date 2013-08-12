Historique
----------

Versions:

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
* Rationnaliser le code (parfois des fonctions _simplif, parfois un paramètre)
