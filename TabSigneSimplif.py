#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__doc__ = """
Script d'utilisation du module de tableau de signe simplifié.
Il renvoie le fichier pst avec la ligne des valeurs et la ligne du signe.

"""

import sys
from tabsigne3 import *

if len(sys.argv) == 1: # le nom du pgm se trouve tjs en argv[0]
    print("utilisation: ./TabSigneSimplif.py 'produit ou quotient' [sortie]\n",
          "[borne 1, borne2]]\n",
          "par défaut, le fichier de sortie se nomme tableau.pst")
elif len(sys.argv) == 4:
    out = sys.argv[3]
    bornes = eval(sys.argv[2])
    expr = sys.argv[1]
elif len(sys.argv) == 3:
    # cas où le 2em argument est le nom de la sortie
    if sys.argv[2][0] != "[":
        out = sys.argv[2] 
        bornes = [-oo, oo]
    else:
        out = "tableau_simplif"
        bornes = eval(sys.argv[2])
    expr = sys.argv[1]
elif len(sys.argv) == 2:
    out = "tableau_simplif"
    bornes = [-oo, oo]
    expr = sys.argv[1]

tmp = TableauSigne(sys.argv[1], bornes = bornes)

print("Indiquez le type de sortie: tex/pst (tex par défaut)")
choix = input()

fin = {'':tmp.export_latex_simplif, 'tex':tmp.export_latex_simplif,
       'pst':tmp.export_pst_simplif}
fin[choix](nom = out) 
