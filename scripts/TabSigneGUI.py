#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# script adapté des exemples basiclayout, mainwindows.menu en qt5

from TableauSigne import __version__, TableauSigne
try:
    from PyQt5.QtWidgets import (QAction, QApplication, QCheckBox, QComboBox,\
                             QDialogButtonBox, QFileDialog, QFormLayout,\
                             QGroupBox, QHBoxLayout, QLabel, QLineEdit,\
                             QMainWindow, QMenu, QMenuBar, QMessageBox,\
                             QPushButton, QTextEdit, QVBoxLayout, QMainWindow,\
                             QWidget)
    from PyQt5.QtCore import (QSaveFile, QIODevice, QByteArray, pyqtSlot)
except ImportError as i:
    print("Veuillez installer PyQt5 sur le site riverbank: http://www.riverbankcomputing.com/software/pyqt/download5")   


class TableauQt(TableauSigne):
    """Réécriture des exports avec un QSaveFile Widget
    """
    def export(self, file, simplif = False):
        """le type d'export est obtenu par analyse de l'extension
        file est un QString: tuple (nom de fichier, filtre)
        la simplification est lue depuis l'attribut QMW.simple
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

    def __init__(self):
        super(QMW, self).__init__()
        self.tableau = TableauQt('x')
        self.simple = False #doit-on faire un tableau simplifié
        #symboles unicode 2a7d et 2a7e voir 
        # http://fr.wikipedia.org/wiki/Table_des_caract%C3%A8res_Unicode_%282000-2FFF%29#Fl.C3.A8ches
        self.inequations = {"⩽0":"-0","<0":"--", "⩾0":"+0",">0":"++"}
        
        self.createMenu()
        self.createHorizontalGroupBox()
        self.createFormGroupBox()
        self.createBoundBox()
        self.createSolutionBox()

        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                statusTip="Sortir de l'application", triggered=self.close)

        bigEditor = QTextEdit()
        bigEditor.setPlainText("Création de la sortie latex ici pour un copier/coller ")

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok) #| QDialogButtonBox.Cancel

        buttonBox.accepted.connect(self.close)
        
        widget = QWidget()
        self.setCentralWidget(widget)

        mainLayout = QVBoxLayout()
        mainLayout.setMenuBar(self.menuBar)
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.BoundBox)
        mainLayout.addWidget(bigEditor)
        mainLayout.addWidget(self.solGroupBox)
        mainLayout.addWidget(self.horizontalGroupBox)
        mainLayout.addWidget(buttonBox)
        widget.setLayout(mainLayout)
        self.bigEditor = bigEditor

        self.setWindowTitle("Tableau de signe")

    @pyqtSlot()
    def _createApropos(self):
        QMessageBox.information(self,
                                "À propos",\
                                "<p><strong>Tableau de signe</strong> - v"+__version__+"</p>"+\
                                "<p>B. Mauricette - GPLv3</p>")
        

    def createMenu(self):
        self.menuBar = QMenuBar()

        self.fileMenu = QMenu("&Fichier", self)
        self.exitAction = self.fileMenu.addAction("E&xit")
        apropos = QMenu("&Infos", self)
        apro = QAction("À &propos", self)
        apro.triggered.connect(self._createApropos)
        apropos.addAction(apro)

        self.menuBar.addMenu(self.fileMenu)
        self.menuBar.addMenu(apropos)

    def createBoundBox(self):
        self.BoundBox = QGroupBox("Bornes")
        layout = QHBoxLayout()

        self.b_inf = QLineEdit(str(self.tableau.bornes[0]))
        self.b_inf.editingFinished.connect(self._update_inf)
        #self.b_inf.editingFinished.emit(self.b_inf.text())
        self.b_sup = QLineEdit(str(self.tableau.bornes[1]))
        self.b_sup.editingFinished.connect(self._update_sup)
        #self.b_sup.editingFinished.emit(self.b_sup.text())

        layout.addWidget(QLabel("borne inf :"))
        layout.addWidget(self.b_inf)
        layout.addWidget(QLabel("borne sup :"))
        layout.addWidget(self.b_sup)
        
        self.BoundBox.setLayout(layout)

    @pyqtSlot()
    def _update_inf(self):
        """ màj de la borne inférieure
        la valeur est sympifiée

        """
        self.tableau.bornes[0] = sympify(self.b_inf.text())
        self._createTableau()

    @pyqtSlot()
    def _update_sup(self):
        """ màj de la borne supérieure
        la valeur est sympifiée

        """
        self.tableau.bornes[1] = sympify(self.b_sup.text())
        self._createTableau()


    def createHorizontalGroupBox(self):
        self.horizontalGroupBox = QGroupBox("Export")
        layout = QHBoxLayout()
        out = [('LaTeX', self._export_latex),\
               ('PST+', self._export_pst),\
               ('PAG',self._export_pag)]
        for i in range(len(out)):
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
        self.tableau.export(fichier, simplif = self.simple)

    @pyqtSlot()
    def _export_pst(self):
        fichier = QFileDialog.getSaveFileName(self, 
                                          "Enregistrer sous…", 
                                          "/home/boris/Documents/tableau.pst", 
                                          "Fichiers PST+ (*.pst)")
        self.tableau.export(fichier, simplif = self.simple)

    @pyqtSlot()
    def _export_pag(self):
        fichier = QFileDialog.getSaveFileName(self, 
                                          "Enregistrer sous…", 
                                          "tableau.pag", 
                                          "Fichiers PAG (PdfAdd) (*.pag)")
        self.tableau.export(fichier, simplif = self.simple)


    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Entrée")
        simple = QCheckBox("Simplifier (pas de lignes intermédiaires)") # bool à basculer
        simple.clicked.connect(self._simple)
        self.expression = QLineEdit(str(self.tableau.expr))
        layout = QFormLayout()
        layout.addRow(QLabel("(fraction rationnelle):"), self.expression)
        valid = QPushButton("Valider")
        valid.clicked.connect(self._createTableau)
        layout.addWidget(valid)
        layout.addWidget(simple)
        self.formGroupBox.setLayout(layout)

    def _simple(self):
         self.simple = not(self.simple)
         self._createTableau()

    def _createTableau(self):
         ex = self.expression.text()
         # créer un nouveau TableauQt provoquerait des pointeurs d'actions vides
         self.tableau.__init__(ex) 
         self.bigEditor.setPlainText(self.tableau.tab2latex(simplif = self.simple))
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
    d = QMW()
    d.resize(700,500)
    d.show()
    sys.exit(app.exec_())
