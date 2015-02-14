Le paquet
---------

Il contient:

* le module lui-même __init__.py
* l'executable *TabSigne*
* l'executable *TabSigneSimplif*
* l'executable *TabSigneGUI*
* une copie de la license GNU GPL v3
* une copie du fichier tabvar.tex
* une copie du fichier pdftabvar.tex
* le dossier doc pour la documentation. Commencer par ouvrir *index.html*.

Logiciels  PST+/PdfAdd
^^^^^^^^^^^^^^^^^^^^^^

Ces scripts produisent des fichiers LaTeX et des fichiers xml lisibles dans
`PST+ <http://www.xm1math.net/pstplus/>`_ et dans `PdfAdd
<http://www.xm1math.net/pdfadd/>`_ pour faire des tableaux de signe. Les outils
PST+/PdfAdd permettent de modifier rapidement le tableau pour soigner le rendu
final. On peut insérer la sortie dans un document, moyennant l'ajout du fichier
*tabvar.tex* (pour PST+) ou *pdftabvar.tex* dans l'entête.

Python
^^^^^^

Les scripts sont écrits en Python3.
Ils utilisent des modules standards ainsi que **sympy** et **lxml**; 
le script d'interface graphique *TabSigneGUI* utilise **Qt5** qui produit de jolies fenêtres.

Il vous est conseillé d'utiliser une version de Python >=3.4. En effet, à
partir de là, l'installateur pip standardise l'installation des modules (et
utilise le pluf récent format d'archive **wheel**)

Pour satisfaire les dépendances vitales, on commence par taper (sous Dos(win)/dans un shell(linux))::

  pip install sympy lxml

Pour l'interface graphique, on installe PyQt5 en choisissant ici `Riverbank Qt5 <http://www.riverbankcomputing.com/software/pyqt/download5>`_ ou, sous linux, en installant le paquet **python3-qt5**::

  sudo apt-get install python3-qt5

Puis on peut installer l'archive::

  pip install TableauSigne-x.x-py3-none-any.whl
