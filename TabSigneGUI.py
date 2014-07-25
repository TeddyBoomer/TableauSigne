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

        self.createMenu()
        self.createHorizontalGroupBox()
        #self.createGridGroupBox()
        self.createFormGroupBox()

        bigEditor = QTextEdit()
        bigEditor.setPlainText("Création de la sortie latex ici pour un copier/coller "
                "top-level.")

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.setMenuBar(self.menuBar)
        mainLayout.addWidget(self.horizontalGroupBox)
        #mainLayout.addWidget(self.gridGroupBox)
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(bigEditor)
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
        self.horizontalGroupBox = QGroupBox("Horizontal layout")
        layout = QHBoxLayout()
        out = ['LaTeX', 'PST+', 'PAG']
        for i in range(Dialog.NumButtons):
            button = QPushButton(out[i])
            layout.addWidget(button)

        self.horizontalGroupBox.setLayout(layout)

    # def createGridGroupBox(self):
    #      self.gridGroupBox = QGroupBox("Grid layout")
    #      layout = QGridLayout()
    # 
    #      for i in range(Dialog.NumGridRows):
    #          label = QLabel("Fraction rationnelle")
    #          lineEdit = QLineEdit()
    #          layout.addWidget(label, i + 1, 0)
    #          layout.addWidget(lineEdit, i + 1, 1)
    # 
    #      self.smallEditor = QTextEdit()
    #      self.smallEditor.setPlainText("This widget takes up about two thirds "
    #             "of the grid layout.")
    # 
    #      layout.addWidget(self.smallEditor, 0, 2, 4, 1)
    # 
    #      layout.setColumnStretch(1, 10)
    #      layout.setColumnStretch(2, 20)
    #      self.gridGroupBox.setLayout(layout)

    def _createTableau(self):
         ex = self.expr.text()
         self.tableau = TableauSigne(ex)
         self.bigEditor.setPlainText(self.tableau.tab2latex())

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


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    dialog = Dialog()
    sys.exit(dialog.exec_())
