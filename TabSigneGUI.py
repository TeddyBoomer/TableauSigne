#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# script adapté de l'exemple basiclayout en qt5

__name__ == '__main__'
from tabsigne3 import *
from PyQt5.QtWidgets import (QAction, QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFileDialog, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QLineEdit, QMainWindow, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
                             QVBoxLayout, QMainWindow, QWidget)
from PyQt5.QtCore import (QSaveFile, QIODevice, QByteArray, pyqtSlot)


class TableauQt(TableauSigne):
    """Réécriture des exports avec un QSaveFile Widget
    """
    def export(self, file, simplif = False):
        """le type d'export est obtenu par analyse de l'extension
        file est un QString: tuple (nom de fichier, filtre)
        """
        # choix pour pst,pag
        choix ={True: self.xmlsimplif, False: self.xml}
        f = file[0]
        ext = f[-3:] #3 derniers caractères
        if ext == "tex":
            o = self.tab2latex(simplif = simplif)
            t = QByteArray(o.encode('utf-8'))
        elif ext in ["pst", "pag"]:
            o = etree.tostring(choix[simplif], pretty_print=True)
            t = QByteArray(o)
        out = QSaveFile(file[0])
        out.open(QIODevice.WriteOnly) # cette constante de classe vaut 2
        out.write( t )
        out.commit()


class QMW(QMainWindow):
    NumGridRows = 1
    NumButtons = 3

    def __init__(self):
        super(Dialog, self).__init__()
        self.tableau = TableauQt('x')
        self.inequations = {"<=0":"-0","<0":"--", ">=0":"+0",">0":"++"}

        self.createMenu()
        self.createHorizontalGroupBox()
        self.createFormGroupBox()
        self.createSolutionBox()

        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                statusTip="Sortir de l'application", triggered=self.close)

        bigEditor = QTextEdit()
        bigEditor.setPlainText("Création de la sortie latex ici pour un copier/coller "
                "top-level.")

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok) #| QDialogButtonBox.Cancel

        buttonBox.accepted.connect(self.close)
        #buttonBox.rejected.connect(self.reject)
        
        widget = QWidget()
        self.setCentralWidget(widget)

        mainLayout = QVBoxLayout()
        mainLayout.setMenuBar(self.menuBar)
        mainLayout.addWidget(self.horizontalGroupBox)
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(bigEditor)
        mainLayout.addWidget(self.solGroupBox)
        mainLayout.addWidget(buttonBox)
        widget.setLayout(mainLayout)
        self.bigEditor = bigEditor

        self.setWindowTitle("Tableau de signe")

    def createMenu(self):
        self.menuBar = QMenuBar()

        self.fileMenu = QMenu("&File", self)
        self.exitAction = self.fileMenu.addAction("E&xit")
        self.menuBar.addMenu(self.fileMenu)

        #self.exitAction.triggered.connect(self.accept)

    def createHorizontalGroupBox(self):
        self.horizontalGroupBox = QGroupBox("Export (indisponible)")
        layout = QHBoxLayout()
        out = [('LaTeX', self._export_latex),\
               ('PST+', self._export_pst),\
               ('PAG',self._export_pag)]
        for i in range(Dialog.NumButtons):
            button = QPushButton(out[i][0])
            button.clicked.connect(out[i][1])
            layout.addWidget(button)

        self.horizontalGroupBox.setLayout(layout)

    @pyqtSlot()
    def _export_latex(self):
        fichier = QFileDialog.getSaveFileName(self, 
                                          "Enregistrer sous…", 
                                          "/home/boris/Documents/tableau.tex", 
                                          "Fichiers LaTeX (*.tex)")
        self.tableau.export(fichier)

    @pyqtSlot()
    def _export_pst(self):
        fichier = QFileDialog.getSaveFileName(self, 
                                          "Enregistrer sous…", 
                                          "/home/boris/Documents/tableau.pst", 
                                          "Fichiers PST+ (*.pst)")
        self.tableau.export(fichier)

    @pyqtSlot()
    def _export_pag(self):
        fichier = QFileDialog.getSaveFileName(self, 
                                          "Enregistrer sous…", 
                                          "tableau.pag", 
                                          "Fichiers PAG (PdfAdd) (*.pag)")
        self.tableau.export(fichier)


    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Entrée")
        self.expression = QLineEdit(str(self.tableau.expr))
        layout = QFormLayout()
        layout.addRow(QLabel("(fraction rationnelle):"), self.expression)
        valid = QPushButton("Valider")
        valid.clicked.connect(self._createTableau)
        layout.addWidget(valid)
        self.formGroupBox.setLayout(layout)

    def _createTableau(self):
         ex = self.expression.text()
         # créer un nouveau TableauQt provoquerait des pointeurs d'actions vides
         self.tableau.__init__(ex) 
         self.bigEditor.setPlainText(self.tableau.tab2latex())
         # voir self.inequations dans __init__
         ineq = self.inequations[ self.choixIneq.currentText() ]
         self.solution.setText(self.tableau.get_solutions(ineq))        

    def _fillbis(self, t):
        """récupérer l'émission du signal lors d'un changement d'inéquation
        """
        self.solution.setText(self.tableau.get_solutions(self.inequations[ t ]))

    def createSolutionBox(self):
        self.solGroupBox = QGroupBox("Ensemble des solutions d'inéquation")
        self.solution = QLineEdit()
        layout = QFormLayout()
        choix = QComboBox()
        # for x in ["<=0","<0", ">=0",">0"]
        for x in self.inequations.keys(): 
            choix.addItem(x)
        self.choixIneq  = choix
        # associer le signal de changement d'inéquation au slot de self.solution.setText
        self.choixIneq.currentTextChanged.connect(self._fillbis)
        self.choixIneq.currentTextChanged.emit(self.choixIneq.currentText())
        layout.addRow(QLabel("Inéquation de la forme f(x)"), self.choixIneq)    
        layout.addRow(QLabel("ens. des solutions:"), self.solution)
        self.solGroupBox.setLayout(layout)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    dialog = QMW()
    dialog.resize(700,500)
    dialog.show()
    #sys.exit(dialog.exec_())
    sys.exit(app.exec_())
