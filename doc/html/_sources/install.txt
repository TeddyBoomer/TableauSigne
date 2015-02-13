Installation
------------

Décompressez le fichier paquet-TableauSigne-x.x.7z
Il contient:

* le module tabsigne3.py
* l'executable *TabSigne.py*
* l'executable *TabSigneSimplif.py*
* l'executable *TabSigneGUI.py*
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

Les scripts sont écrits en Python3 mais *ils fonctionnent aussi avec Python2.7* (au moins les scripts en ligne de commande).
Ils utilisent des modules standards ainsi que **sympy** et **lxml**; 
le script d'interface graphique *TabSigneGUI.py* utilise **Qt5** qui produit de jolies fenêtres.

Attention, (pour Windows) lxml n'est installable que pour python <= 3.2.
Globalement, pour Ububtu/Debian, il y a des paquets disponibles dans la distribution. Vous pourrez essayer::

  # apt-get install python-sympy python-lxml python-qt5
  # apt-get install python3-sympy python3-lxml python3-qt5

Ou de façon encore plus efficace, pour avoir les plus récentes versions des modules grâce à l'installateur python pip/pip3::

  # pip install sympy      
  # pip3 install sympy

et de même pour lxml et PyQt5 (bien respecter la casse)

* Python: `http://python.org/getit/ <http://python.org/getit/>`_ : sélectionnez votre plateforme (sous linux, débrouillez-vous avec apt, synaptic...)
* Sympy:

Attention, le sympy-0.6.6 présentait un petit bug pénible: les polynômes
étaient affichés par ordre croissant de puissance. C'est une chose corrigée
dans les versions 0.7.x. Si vous avez une ancienne distribution linux et que
votre *python-sympy* est trop ancien, je vous conseille de l'enlever et
d'installer la dernière version de *sympy* avec *pip* (voir ci-dessus).

Lien pour `sympy-0.7.5 <https://github.com/sympy/sympy/releases/download/sympy-0.7.5/sympy-0.7.5.win32.exe>`_.

sinon voir `https://github.com/sympy/sympy/releases <https://github.com/sympy/sympy/releases>`_

* lxml: 

Voici le lien `lxml-3.3.5 <https://pypi.python.org/pypi/lxml/3.3.5>`_ (choisissez votre version de python
et votre type de processeur).  sinon voir `http://lxml.de/installation.html
<http://lxml.de/installation.html>`_

* Qt5: Lien `Qt5 <http://www.riverbankcomputing.co.uk/software/pyqt/download5>`_
