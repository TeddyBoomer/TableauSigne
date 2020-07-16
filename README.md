TableauSigne
============

produire des sorties tex/pst/pag de tableaux de signe


Une petite illustration des capacités du module:

Exemple::

```python
from TableauSigne import *
A = randExpr(3) 
(4*x - 3)/((-3*x + 4)*(5*x + 5))

B = TableauSigne(A)
B.get_solutions('+0')

'\left] -\infty;-1\right[\cup \left[ \frac{3}{4};\frac{4}{3}\\right['

print(B.tab2latex())
B.export_pst()
```

```latex
$$\tabvar{%
\tx{x} & \tx{-\infty} &  & \tx{-1} &  & \tx{\frac{3}{4}} &  & \tx{\frac{4}{3}} &  & \tx{+\infty}\cr
\tx{- 3 x + 4} &  & \tx{+} & \tx{|} & \tx{+} & \tx{|} & \tx{+} & \txt{0} & \tx{-} & \cr
\tx{5 x + 5} &  & \tx{-} & \txt{0} & \tx{+} & \tx{|} & \tx{+} & \tx{|} & \tx{+} & \cr
\tx{4 x -3} &  & \tx{-} & \tx{|} & \tx{-} & \txt{0} & \tx{+} & \tx{|} & \tx{+} & \cr
\tx{\text{signe de }f} &  & \tx{+} & \dbt & \tx{-} & \txt{0} & \tx{+} & \dbt & \tx{-} & \cr}$$
```

Des scripts python TabSigne, TabSigneSimplif et TabSigneGUI utilisent le module pour produire directement des sorties tex/pst/pag. 

Le dernier script est une interface graphique et nécessite l'installation de PyQt5.

voir le site http://www.xm1math.net/pdfadd/index.html
