Recommandations
---------------

Vous pouvez préciser les bornes du tableau de signe en paramètre de la classe
*TableauSigne*; c'est une liste de deux valeurs [a,b] à ajouter. Les nombres
peuvent être sympifiés, ils seront alors plus joliment écrits dans le tableau.

*exemple*:
   Au lieu de 0.5, mettre *sympify('0.5')* ou bien
   *Rational(1,2)*. Attention, dans python 2.x le symbole / servait à la
   division euclidienne et on se retrouvait régulièrement avec des 2/3=0. Si
   vous voulez mettre la borne 2/3, sympifiez-la (ou mettez *Rational(2,3)*).

Par défaut les bornes sont à ± oo (oo est le symbole de l'infini dans sympy).

Ce module ne gère pas les facteurs avec d'autres symboles que *x*.

.. important:: 
   Les scripts distribués avec le paquet ne montrent pas *toutes* les possibilités
   du module. Notamment il existe une classe ``TableauFactory`` pour générer en
   chaine une série de tableaux de signe. Vous pouvez la trouver à la fin du
   fichier tableau.py.
