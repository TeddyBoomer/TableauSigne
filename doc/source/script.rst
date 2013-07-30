Script
------

Le fichier *TabSigne.py* est un script permettant d'utiliser le module
directement en ligne de commande.

En principe il fonctionne sur toute plateforme.
Signature:

.. function:: TabSigne "expr"  ["[a,b]", nom_sortie]

Arguments:

#. "expr" doit être entre guillemets simples '.' ou doubles "."; elle est au format sympy, les puissances s'écrivent avec ** et non pas ^
#. "[a,b]" est la liste des bornes; vous pouvez mettre des valeurs sympifiées pour avoir des fractions (par ex: sympify('3/2'))
#. nom_sortie est le nom du fichier de sortie (pas nécéssairement entre guillemets);

Le script vous demande le format de sortie tex/pst (tex par défaut)


Ainsi, on peut taper::

       $ ./TabSigne.py '(3*x+2)**3 /(2*x - 5)**2 *(5*x+1) * -8' Sortie
       $ ./TabSigne.py "(3*x+2)**3 /(2*x - 5)**2 *(5*x+1) * -8" "[-5, sympify('4/3')]" Sortie
       $ ./TabSigne.py "(3*x+2)**3 /(2*x - 5)**2 *(5*x+1) * -8" "[-5, +oo]" Sortie

qui vous fera le tableau de signe dans le fichier Sortie.tex ou Sortie.pst. Remarquez aussi dans le dernier exemple que les crochets de l'intervalle de définition n'ont rien à voir avec les crochets mathématiques; ce sont des crochets de liste en Python.

Le fichier *TabSigneSimplif.py* fonctionne sur le même principe et produira un tableau simplifié: il ne contient alors que la ligne de la variable et la ligne finale.

.. important:: Il existe une classe ``TableauFactory`` très pratique pour générer directement une série de tableaux de signe.

