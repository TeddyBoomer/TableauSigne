import unittest
import tableau
import sympy

x = sympy.var('x')
class TestTableauSigne(unittest.TestCase):
    def setUp(self):
        self.tb = tableau.TableauSigne('(2*x+1)*(3*x+2)')
        
    def test_produit(self):
        a = sympy.sympify('(2*x+1)*(3*x+2)')
        z = [ e[0]-e[1] == 0 for e in zip(self.tb.facteurs, a.args)]
        self.assertEqual(z, len(z)*[True])

    def test_latex(self):
        ltx = self.tb.tab2latex()
        model = """$$\\tabvar{%
\\tx{x} & \\tx{-\\infty} &  & \\tx{- \\frac{2}{3}} &  & \\tx{- \\frac{1}{2}} &  & \\tx{+\\infty}\\cr
\\tx{2 x + 1} &  & \\tx{-} & \\trait & \\tx{-} & \\txt{0} & \\tx{+} & \\cr
\\tx{3 x + 2} &  & \\tx{-} & \\txt{0} & \\tx{+} & \\trait & \\tx{+} & \\cr
\\tx{\\text{signe de }f} &  & \\tx{+} & \\txt{0} & \\tx{-} & \\txt{0} & \\tx{+} & \\cr}$$"""
        self.assertEqual(ltx, model)

    def test_tkz(self):
        tkz = self.tb.tab2tkz()
        model = """%\\usepackage{tkz-tab}
\\begin{tikzpicture}
\\tkzTabInit[nocadre,lgt=2.5,espcl=1.5]{$x$ /0.8 ,\n$2 x + 1$ /0.8 ,
$3 x + 2$ /0.8 ,
signe de $f(x)$ /0.8}{$-\\infty$ , $- \\frac{2}{3}$ , $- \\frac{1}{2}$ , $+\\infty$}
\\tkzTabLine{ , - , t , - , z , + , }
\\tkzTabLine{ , - , z , + , t , + , }
\\tkzTabLine{, +, z, -, z, +, }
\\end{tikzpicture}"""
        self.assertEqual(tkz, model)


if __name__ == '__main__':
    unittest.main()
