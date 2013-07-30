Recommandations
---------------

Vous pouvez préciser les bornes du tableau de signe en paramètre de la classe
*TableauSigne*; c'est une liste de deux valeurs [a,b] à ajouter. Les nombres
peuvent être sympifiés, ils seront alors plus joliment écrits dans le tableau.

Ex: au lieu de 0.5, mettre *sympify('0.5')* ou bien *Rational(1,2)*. N'oubliez
pas que dans python le symbole / sert à la division euclidienne et on se
retrouve régulièrement avec des 2/3=0. Si vous voulez mettre la borne 2/3,
sympifiez-la (ou mettez *Rational(2,3)*).

Par défaut les bornes sont à pm oo (oo est le symbole de l'infini dans sympy).

Ce module ne gère pas les facteurs avec d'autres symboles que *x* en raison du
placement des racines et pôles dans le tableau.
