Scripts
-------


TabSigneGUI
^^^^^^^^^^^

C'est probablement le plus simple à utiliser car c'est une interface graphique: un double clic dessus devrait le lancer.

Il y a des boutons d'export tex/pst/pag.

Il y a une fenêtre de texte qui donne la sortie tex que vous pouvez directement utiliser pour un copier/coller.
Idem pour produire l'ensemble des solutions d'une inéquation sur le signe.

.. figure:: ../img/GUI.png
   :scale: 100 %
   :alt: interface graphique *TableauSigneGUI*
   :align: center

   Interface graphique *TableauSigneGUI*

   La fonction de chaque élément est relativement intuitive.


TabSigne
^^^^^^^^
Le fichier *TabSigne* est un script permettant d'utiliser le module
directement en ligne de commande.

En principe il fonctionne sur toute plateforme.
Signature:


.. function:: TabSigne [-h] [--bornes [BORNES]] [--format {tex,pst,pag}] [--out [OUT]] [--version] expression

	   Construit le tableau de signe d'une expression.

	   positional arguments:
	      * expression      
		L'expression dont on doit construire le tableau de signe (format sympy)
	   
	   optional arguments:
	     * -h, `- -help`
               show this help message and exit
	     * `- -bornes` [BORNES], -b [BORNES]
	       Liste [a,b] des bornes d'étude. L'infini se note oo.
	     * `- -format` {tex,pst,pag}, -f {tex,pst,pag}
	       Choix du format de sortie
	     * `- -out` [OUT], -o [OUT]
	       Nom du fichier de sortie (sans extension)
	     * `- -version`, -v
               show program's version number and exit

Ainsi, on peut taper::

       $ TabSigne -h
       $ TabSigne -b '[-3,6]' '8*x+3'
       $ TabSigne -b '[-3,6]' -o sortie '8*x+3'
       $ TabSigne -b "[-3,sympify('13/2')]" -o sortie -f pst '8*x+3'


qui vous fera le tableau de signe dans le fichier sortie.tex ou sortie.pst. Remarquez que les crochets de l'intervalle de définition n'ont rien à voir avec les crochets mathématiques; ce sont des crochets de liste en Python.

Attention, la syntaxe de l'expression doit être précise: n'oubliez pas les symboles de produit * et mettez des parenthèses autour des constantes négatives. Par exemple on tapera::

       $ TabSigne -b '[-1,10]' -o DM -f pst '(-2)*x**2*(x+3)/(x+2)**2'

(et non pas '-2*x**2*(x+3)/(x+2)**2' pour l'expression) 


TabSigneSimplif
^^^^^^^^^^^^^^^
Le fichier *TabSigneSimplif* fonctionne sur le même principe et produira un tableau simplifié: il ne contient alors que la ligne de la variable et la ligne finale.

.. important:: Il existe une classe ``TableauFactory`` très pratique pour générer directement une série de tableaux de signe.

