#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script d'utilisation du module de tableau de signe simplifié.
Il renvoie le fichier pst avec la ligne des valeurs et la ligne du signe.

"""

import sys
import argparse
from sympy import sympify, oo
from TableauSigne import __version__, TableauSigne

# TabSigneSimplif.py -h
# TabSigneSimplif.py -b '[-3,6]' '8*x+3'
# TabSigneSimplif.py -b '[-3,6]' -o test '8*x+3'
# TabSigneSimplif.py -b '[-3,6]' -o test -f pst '8*x+3'

parser = argparse.ArgumentParser(description="Construit le tableau de signe simplifié d'une expression.")
parser.add_argument('expr', metavar='expression', type=str,
                    help="L'expression dont on doit construire le tableau de signe (format sympy)")
parser.add_argument('--bornes', '-b', type=str, nargs='?', default='[-oo,oo]',
                    help="Liste [a,b] des bornes d'étude. L'infini se note oo.")
parser.add_argument('--format', '-f', type=str, choices=['tex','pst', 'pag'], default='tex', 
                    help="Choix du format de sortie")
parser.add_argument('--out', '-o', type=str, nargs='?', default='tableau_simplif', 
                    help="Nom du fichier de sortie (sans extension)")
parser.add_argument('--version', '-v', action='version', version='%(prog)s '+__version__)

A = parser.parse_args()
# l'expresion est du type "'e'" dans A
tmp = TableauSigne(sympify(A.expr), bornes = eval(A.bornes))
# choix du format dans le dictionnaire fin des 2 méthodes.
fin = {'tex':tmp.export_latex, 'pst':tmp.export_pst, 'pag':tmp.export_pst}
fin[A.format](nom = A.out, simplif = True, ext = A.format)
