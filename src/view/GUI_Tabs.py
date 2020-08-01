import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, \
    QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import glob
sys.path.append('../apps')
sys.path.append('../model')
sys.path.append('../controller')

from filehandler import FileHandler
from tableDataFrame import TableDataFrame

from mzTabTableWidget import mzTabTableWidget
from GUI_FastaViewer import GUI_FastaViewer
from ErrorWidget import ErrorWidget
from HomeTabWidget import HomeTabWidget

from SpecViewer import App
from ConfigView import ConfigView
from mzMLTableView import mzMLTableView


class AppGUITabs(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'GUI_Tabs'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        
        self.show()


class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        self.loadedFolder = ""
        self.loadedFasta = ""
        self.loadedIni = ""
        self.loadedTsv = ""
        
        # add button to automatically load data into widgets
        self.initButton = QPushButton(self)  
        self.initButton.setText("Load Data")
        self.initButton.setFixedSize(220,25)
        self.initButton.clicked.connect(self.show_popup)  

        # add button to run proteimicsLFQ command
        self.loadButton = QPushButton(self)  
        self.loadButton.setText("Run ProteomicsLFQ")
        self.loadButton.setFixedSize(220,25)
        self.loadButton.clicked.connect(self.LFQ)

        # initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = HomeTabWidget()
        self.tab2 = ConfigView()
        self.tab3 = mzMLTableView()
        self.tab4 = mzTabTableWidget()
        self.tab5 = GUI_FastaViewer()
        self.tab6 = App()

        self.tabs.resize(300, 200)

        # add tabs
        self.tabs.addTab(self.tab1, "Home")
        self.tabs.addTab(self.tab2, "Ini-Config")
        self.tabs.addTab(self.tab3, "Experimental Design")
        self.tabs.addTab(self.tab4, "PSM/PRT Table")
        self.tabs.addTab(self.tab5, "Fasta-Viewer")
        self.tabs.addTab(self.tab6, "Spectrum Viewer")

        # add tabs to widget
        self.layout.addWidget(self.initButton)
        self.layout.addWidget(self.loadButton)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def show_popup(self):
        """
            displays popup window that questions whether data should be loaded automatically
        """
        msg = QMessageBox()
        msg.setWindowTitle("Attention!")
        msg.setText("Want data to be loaded automatically?  ")
        msg.setIcon(QMessageBox.Question)
        msg.setDetailedText(
            "If you choose to load data automatically, please enter the folder that contains entire data (for different widgets). Otherwise, please enter data manually through widgets. Thank you.")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.buttonClicked.connect(self.popupbutton_clicked)

        x = msg.exec_()

    def popupbutton_clicked(self, i):
        """
            when user selects 'Yes', data is loaded into the widgets based on its file type
        """
        
        if i.text() == "&Yes":
            self.AutoLoadedData = True #neu
            dialog = QFileDialog(self)
            self.loadedFolder = dialog.getExistingDirectory()
            print(self.loadedFolder)

            os.chdir(self.loadedFolder)
            for file in glob.glob("*.fasta"):
                self.tab5.loadFile(file)
                self.loadedFasta = file

            for file in glob.glob("*.ini"):
                self.tab2.openXML(file)
                self.loadedIni = file

            if self.loadedIni == "":
                os.system("ProteomicsLFQ -write_ini generated.ini")
                self.tab2.openXML("generated.ini")
                self.loadedIni = "generated.ini"

            for file in glob.glob("*.tsv"):
                self.loadedTsv = file
                self.tab3.loadDir(self.loadedFolder)


    def PopupFolder(self):
        msg = QMessageBox()
        msg.setWindowTitle("Attention!")
        msg.setText("Please choose a Project Folder \n(must be the one containing the mzML and idXML files)")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(self.loadFolder)

        x = msg.exec_()

    def loadFolder(self):
        dialog = QFileDialog(self)
        self.loadedFolder = dialog.getExistingDirectory()

    def PopupFasta(self):
        msg = QMessageBox()
        msg.setWindowTitle("Attention!")
        msg.setText("Please choose a Fasta file")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(self.loadFasta)

        x = msg.exec_()


    def loadFasta(self):
        fileDialog = QFileDialog.getOpenFileName(self, "Choose Fasta","","Fasta files (*.fasta)",
                                                 "Fasta files (*.fasta)")
        fileName = fileDialog[0]
        self.tab5.loadFile(fileName)
        self.loadedFasta = fileName

    def PopupTsv(self):
        msg = QMessageBox()
        msg.setWindowTitle("Attention!")
        msg.setText("Please choose a .tsv")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(self.loadTsv)

        x = msg.exec_()

    def loadTsv(self):
        fileDialog = QFileDialog.getOpenFileName(self, "Choose .tsv","",".tsv files (*.tsv)",
                                                 ".tsv files (*.tsv)")
        fileName = fileDialog[0]
        self.loadedTsv = fileName
        self.tab3.loadDir(self.loadedFolder)

    def PopupIni(self):
        msg = QMessageBox()
        msg.setWindowTitle("Attention!")
        msg.setText("Do you want to choose a .ini ? \nIf you choose cancel a .ini will be automatically generated")
        msg.setStandardButtons(QMessageBox.Yes|QMessageBox.Cancel)
        msg.buttonClicked.connect(self.loadIni)

        x = msg.exec_()

    def loadIni(self, i):
        if i.text() == "&Yes":
            fileDialog = QFileDialog.getOpenFileName(self, "Choose .ini","",".ini files (*.ini)",
                                                 ".ini files (*.ini)")
            fileName = fileDialog[0]

            self.tab2.generateTreeWidgetItem(fileName)
            self.loadedIni = fileName

        else:
            os.chdir(self.loadedFolder)
            os.system("ProteomicsLFQ -write_ini generated.ini")
            self.tab2.openXML("generated.ini")
            self.loadedIni = "generated.ini"

    def LFQ(self):
        if self.loadedFolder == "":
            self.PopupFolder()

        if self.loadedFasta == "" and self.tab5.path == "":
            self.PopupFasta()

        elif self.tab5.path != "":
            self.loadedFasta = self.tab5.path

        if self.loadedTsv == "" and self.tab3.path == "":
            self.PopupTsv()

        elif self.tab3.path != "":
            self.loadedTsv = self.tab3.path

        if self.loadedIni == "" and self.tab2.path == "":
            self.PopupIni()

        elif self.tab2.path != "":
            self.loadedIni = self.tab2.path

        os.chdir(self.loadedFolder)
        mzML = glob.glob("*.mzML")
        idXML = glob.glob("*.idXML")

        self.tab2.saveTmpFile()

        if len(mzML) == len(idXML):

            command = "ProteomicsLFQ -in    "

            for file in mzML:
                command += file + " "

            command += "-ids "

            for file in idXML:
                command += file + " "

            command += "-design " + self.loadedTsv + " "
            command += "-fasta " + self.loadedFasta + " "
            command += "-ini tmp.ini " \
                       "-out_cxml BSA.consensusXML.tmp " \
                       "-out_msstats BSA.csv.tmp " \
                       "-out BSA.mzTab.tmp " \
                       "-threads " + self.tab1.loadedThreads + " " \
                       "-proteinFDR " + self.tab1.loadedFDR + " "

            print(command)
            os.chdir(self.loadedFolder)
            os.system(command)

            for file in glob.glob("*.mzTab.tmp"):
                self.tab4.readFile(file)

            os.remove("tmp.ini")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AppGUITabs()
    sys.exit(app.exec_())
