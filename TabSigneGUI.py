#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# script adapté de l'exemple basiclayout en qt5

__name__ == '__main__'
from tabsigne3 import *
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
        QVBoxLayout)


class Dialog(QDialog):
    NumGridRows = 1
    NumButtons = 3

    def __init__(self):
        super(Dialog, self).__init__()

        self.inequations = {"<=0":"-0","<0":"--", ">=0":"+0",">0":"++"}

        self.createMenu()
        self.createHorizontalGroupBox()
        self.createFormGroupBox()
        self.createSolutionBox()

        bigEditor = QTextEdit()
        bigEditor.setPlainText("Création de la sortie latex ici pour un copier/coller "
                "top-level.")

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.setMenuBar(self.menuBar)
        mainLayout.addWidget(self.horizontalGroupBox)
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(bigEditor)
        mainLayout.addWidget(self.solGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        self.bigEditor = bigEditor

        self.setWindowTitle("Tableau de signe")

    def createMenu(self):
        self.menuBar = QMenuBar()

        self.fileMenu = QMenu("&File", self)
        self.exitAction = self.fileMenu.addAction("E&xit")
        self.menuBar.addMenu(self.fileMenu)

        self.exitAction.triggered.connect(self.accept)

    def createHorizontalGroupBox(self):
        self.horizontalGroupBox = QGroupBox("Export (indisponible)")
        layout = QHBoxLayout()
        out = ['LaTeX', 'PST+', 'PAG']
        for i in range(Dialog.NumButtons):
            button = QPushButton(out[i])
            layout.addWidget(button)

        self.horizontalGroupBox.setLayout(layout)

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Entrée")
        self.expr = QLineEdit()
        layout = QFormLayout()
        layout.addRow(QLabel("(fraction rationnelle):"), self.expr)
        #layout.addRow(QLabel("Line 2, long text:"), QComboBox())
        #layout.addRow(QLabel("Line 3:"), QSpinBox())
        valid = QPushButton("Valider")
        valid.clicked.connect(self._createTableau)
        layout.addWidget(valid)
        self.formGroupBox.setLayout(layout)

    def _createTableau(self):
         ex = self.expr.text()
         self.tableau = TableauSigne(ex)
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
    dialog = Dialog()
    dialog.resize(700,500)
    sys.exit(dialog.exec_())
