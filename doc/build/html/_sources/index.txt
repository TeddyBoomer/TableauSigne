.. TableauSigne documentation master file, created by
   sphinx-quickstart on Thu Feb 16 22:34:52 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Bienvenue dans la doc de TableauSigne!
======================================

:Author: Boris Mauricette <Boris point Mauricette at ac - lyon point fr>
:Date: |today| 
:Revision: |version| 
:Description: Voici la documentation du module pour les tableaux de signe.
:Contents: Informations sur le module tabsigne3


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

   >>> from tabsigne3 import *
   >>> A = randExpr(3)
   (4*x - 3)/((-3*x + 4)*(5*x + 5))
   >>> B = TableauSigne(A)
   >>> B.get_solutions('+0')
   '\left] -\infty;-1\right[\cup \left[ \frac{3}{4};\frac{4}{3}\\right['
   >>> print(B.tab2latex())
   $$\tabvar{%
   \tx{x} & \tx{-\infty} &  & \tx{-1} &  & \tx{\frac{3}{4}} &  & \tx{\frac{4}{3}} &  & \tx{+\infty}\cr
   \tx{- 3 x + 4} &  & \tx{+} & \tx{|} & \tx{+} & \tx{|} & \tx{+} & \txt{0} & \tx{-} & \cr
   \tx{5 x + 5} &  & \tx{-} & \txt{0} & \tx{+} & \tx{|} & \tx{+} & \tx{|} & \tx{+} & \cr
   \tx{4 x -3} &  & \tx{-} & \tx{|} & \tx{-} & \txt{0} & \tx{+} & \tx{|} & \tx{+} & \cr
   \tx{\text{signe de }f} &  & \tx{+} & \dbt & \tx{-} & \txt{0} & \tx{+} & \dbt & \tx{-} & \cr}$$
   >>> B.export_pst()

Le logiciel pdfAdd donne le rendu suivant (.pdf converti en .png)

.. image:: ../img/exemple.png
   :scale: 100 %
   :alt: résultat de l'export au format eps (produit par pst+)
   :align: left
