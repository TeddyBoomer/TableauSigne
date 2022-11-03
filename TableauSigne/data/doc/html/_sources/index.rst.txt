.. TableauSigne documentation master file, created by
   sphinx-quickstart on Thu Feb 16 22:34:52 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Bienvenue dans la doc de TableauSigne!
======================================

:Author: Boris Mauricette <Boris point Mauricette at ac - lyon point fr> ou <teddy_boomer at yahoo point fr>
:Date: |today| 
:Revision: |version| 
:Description: Voici la documentation du paquet pour les tableaux de signe.
:Contents: Informations sur le module TableauSigne


.. toctree::
   :maxdepth: 2
   :numbered:

   install.rst
   script.rst
   recommandations.rst
   history.rst
   interface.rst

Une petite illustration des capacités du module: 

Exemple::

   >>> from TableauSigne import *
   >>> A = randExpr(3)
   (4*x - 3)/((-3*x + 4)*(5*x + 5))
   >>> A2 = randExpr(5, denomin=3, vals=[-4,2,3])
   (-3*x - 3)*(4*x - 3)/((8 - 4*x)*(9 - 3*x)*(-4*x - 16))
   >>> B = TableauSigne(A)
   >>> B.get_solutions('+0')
   '\left] -\infty;-1\right[\cup \left[ \frac{3}{4};\frac{4}{3}\\right['
   >>> print(B.tab2tkz())
   %\usepackage{tkz-tab}
   \begin{tikzpicture}
   \tkzTabInit[nocadre,lgt=2.5,espcl=1.5]{$x$ /0.8 ,
   $4 x - 3$ /0.8 ,
   $5 x + 5$ /0.8 ,
   $4 + \left(-3\right) x$ /0.8 ,
   signe de $f(x)$ /0.8}{$-\infty$ , $-1$ , $\frac{3}{4}$ , $\frac{4}{3}$ , $+\infty$}
   \tkzTabLine{ , - , d , - , z , + , d , + , }
   \tkzTabLine{ , - , d , + , t , + , d , + , }
   \tkzTabLine{ , + , d , + , t , + , d , - , }
   \tkzTabLine{, +, d, -, z, +, d, -, }
   \end{tikzpicture}
   >>> B.export_tkz()
   
La compilation avec XeLaTex donne le rendu suivant. (on observe qu'il y a un
peu de travail manuel à faire sur les facteurs avec un coefficient directeur
négatif)

.. image:: ../img/exemple.png
   :scale: 100 %
   :alt: résultat de l'export au format eps (produit par pst+)
   :align: left
