import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, \
    QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import glob
from filehandler import FileHandler
from tableDataFrame import TableDataFrame

from mzTabTableWidget import mzTabTableWidget
from GUI_FastaViewer import Window
from ErrorWidget import ErrorWidget

sys.path.insert(0, '../apps')
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
        # setTab3()
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

        self.initButton = QPushButton(self)  # neu1
        self.initButton.setText("Load Data")
        self.initButton.clicked.connect(self.show_popup)  # neu1

        self.loadButton = QPushButton(self)  # neu
        self.loadButton.setText("Run ProteomicsLFQ")
        self.loadButton.clicked.connect(self.LFQ)

        # initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = ConfigView()
        self.tab2 = mzMLTableView()
        self.tab3 = mzTabTableWidget()
        self.tab4 = Window()
        self.tab5 = App()

        self.tabs.resize(300, 200)

        # add tabs
        self.tabs.addTab(self.tab1, "Ini-Config")
        self.tabs.addTab(self.tab2, "Experimental Design")
        self.tabs.addTab(self.tab3, "PSM/PRT Table")
        self.tabs.addTab(self.tab4, "Fasta-Viewer")
        self.tabs.addTab(self.tab5, "Spectrum Viewer")

        # add tabs to widget
        self.layout.addWidget(self.initButton)
        self.layout.addWidget(self.loadButton)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def show_popup(self):
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
        # i is either 'Yes' or 'Cancel'
        if not (i == QMessageBox.Cancel):
            dialog = QFileDialog(self)
            self.loadedFolder = dialog.getExistingDirectory()
            print(self.loadedFolder)

            os.chdir(self.loadedFolder)
            for file in glob.glob("*.fasta"):
                self.tab4.loadFile(file)
                self.loadedFasta = file

            for file in glob.glob("*.ini"):
                self.tab1.generateTreeWidgetItem(file)
                self.loadedIni = file

            for file in glob.glob("*.tsv"):
                TableDataFrame.setTable(self.tab2, FileHandler.importTable(self.tab2, file))
                self.tab2.drawTable()
                self.loadedTsv = file

            if self.loadedTsv == "":
                self.tab2.loadDir(self.loadedFolder)

    def LFQ(self):

        os.chdir(self.loadedFolder)
        mzML = glob.glob("*.mzML")
        idXML = glob.glob("*.idXML")

        if len(mzML) == len(idXML):

            command = "ProteomicsLFQ -in    "

            for file in mzML:
                command += file + " "

            command += "-ids "

            for file in idXML:
                command += file + " "

            command += "-design " + self.loadedTsv + " "
            command += "-fasta " + self.loadedFasta + " "
            command += "-Alignment:max_rt_shift 0 " \
                       "-targeted_only true " \
                       "-transfer_ids false " \
                       "-mass_recalibration false " \
                       "-out_cxml BSA.consensusXML.tmp " \
                       "-out_msstats BSA.csv.tmp " \
                       "-out BSA.mzTab.tmp " \
                       "-threads 1 " \
                       "-proteinFDR 0.3"

            print(command)
            os.chdir(self.loadedFolder)
            os.system(command)

            for file in glob.glob("*.mzTab"):
                self.tab3.readFile(file)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AppGUITabs()
    sys.exit(app.exec_())
