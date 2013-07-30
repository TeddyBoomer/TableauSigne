Installation
------------

Décompressez le fichier paquet-TableauSigne.7z
Il contient:

* le module btabsigne.py
* l'executable *TabSigne.py*
* l'executable *TabSigneSimplif.py*
* le dossier doc pour la documentation. Commencer par ouvrir *index.html*.

Logiciel  PST+
^^^^^^^^^^^^^^

Ces scripts produisent des fichiers LaTeX et des fichiers xml lisibles dans
`PST+ <http://www.xm1math.net/pstplus/>`_ pour faire des tableaux de signe. Les
outils PST+ permettent de modifier rapidement le tableau pour soigner le rendu
final. On peut insérer la sortie dans un document, moyennant l'ajout du fichier
*tabvar.tex* dans l'entête.

Python
^^^^^^

Les scripts sont écrits en Python3, ils utilisent des modules standards mais
aussi *sympy* et *lxml*.:

* Python: `http://python.org/getit/ <http://python.org/getit/>`_ : sélectionnez votre plateforme (sous linux, débrouillez-vous avec apt, synaptic...)
* Sympy: le plus simple est sous Ubuntu/Debian en faisant::

  # apt-get install python-sympy

Attention, le sympy-0.6.6 présentait un petit bug pénible: les polynômes
étaient affichés par ordre croissant de puissance. C'est une chose corrigée
dans les versions 0.7.x. Si vous avez une ancienne distribution linux et que
votre *python-sympy* est trop ancien, je vous conseille de l'enlever et
d'installer la dernière version de *sympy* avec *easy_install*::

  # easy_install -f http://code.google.com/p/sympy/downloads/detail?name=sympy-0.7.2-py3.2.tar.gz sympy

(à l'heure actuelle une version 0.7.3 va bientôt arriver)
Pour Windows, voici le lien pour `sympy-0.7.2  <http://code.google.com/p/sympy/downloads/detail?name=sympy-0.7.2.win32.exe>`_.

sinon voir `http://code.google.com/p/sympy/downloads/list <http://code.google.com/p/sympy/downloads/list>`_

* lxml: le plus simple est sous Ubuntu/Debian en faisant::

  # apt-get install python-lxml
  # apt-get install python3-lxml

Pour Windows, voici le lien `lxml-3.2.1 <https://pypi.python.org/pypi/lxml/3.2.1>`_.
sinon voir `http://lxml.de/installation.html <http://lxml.de/installation.html>`_ 

