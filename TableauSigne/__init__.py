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

"""Module de création de tableaux de signe.

Export possible vers LaTeX, pst+, pdfadd (pour modifier le tableau)

.. py:class:: TableauSigne(e [, **kwargs])
   créer le tableau de signe d'une expression e

.. py:function:: randExpr(n, [a=-5, b=5, denom=True, nopower=True])
   générer une expression à n facteurs

   * bornes des coefs: a, b
   * bool denomin: autoriser des facteurs au dénominateur,
   * bool nopower: refuser d'avoir des puissances.

.. py:class:: TableauFactory(L, [M])
   créer une liste de tableaux de signe

   * L est une liste d'expressions (fractions rationnelles)
   * M est une liste de dictionnaires d'options pour les initialisations.
"""


from TableauSigne.tableau import TableauSigne, TableauFactory, randExpr

__version__ = '1.4'

