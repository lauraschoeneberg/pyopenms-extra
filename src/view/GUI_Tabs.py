import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from mzTabTableWidget import mzTabTableWidget
from GUI_FastaViewer import Window
from SpectrumWidget import SpectrumWidget
from ErrorWidget import ErrorWidget
sys.path.insert(0, '../apps')
from SpecViewer import App
from XMLViewer import XMLViewer
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
        #setTab3()
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


        

class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.initButton = QPushButton(self) #neu1
        self.initButton.setText("Load Data")
        self.initButton.clicked.connect(self.show_popup) #neu1
        
        self.loadButton = QPushButton(self) #neu
        self.loadButton.setText("Run ProteomicsLFQ")
        self.loadButton.clicked.connect(self.LFQ)

        #initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = XMLViewer()
        self.tab2 = mzMLTableView()
        self.tab3 = mzTabTableWidget()
        self.tab4 = Window()
        self.tab5 = App()

        self.tabs.resize(300,200)

        #add tabs
        self.tabs.addTab(self.tab1, "Ini-Config")
        self.tabs.addTab(self.tab2, "Experimental Design")
        self.tabs.addTab(self.tab3, "PSM/PRT Table")
        self.tabs.addTab(self.tab4, "Fasta-Viewer")
        self.tabs.addTab(self.tab5, "Spectrum Viewer")

        #add tabs to widget
        self.layout.addWidget(self.initButton)
        self.layout.addWidget(self.loadButton)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def show_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Attention!")
        msg.setText("Want data to be loaded automatically?  ")
        msg.setIcon(QMessageBox.Question)
        msg.setDetailedText("If you choose to load data automatically, please enter the file that contains entire data (for different widgets). Otherwise, please enter data manually through widgets. Thank you.")
        msg.setStandardButtons(QMessageBox.Yes|QMessageBox.Cancel)
        msg.buttonClicked.connect(self.popupbutton_clicked)
                
        x = msg.exec_()

    def popupbutton_clicked(self,i):
        #i is either 'Yes' or 'Cancel'
        if not (i == QMessageBox.Cancel):
          options = QFileDialog.Options()
          file, _ = QFileDialog.getOpenFileName(
              self, "QFileDialog.getOpenFileName()", "", "All Files (*);;tsv (*.tsv);;csv (*.csv);;fasta (*.fasta);; mzML (*.mzML);; ini (*.ini)", options=options)
          
            
    def LFQ(self):

        fastapath = self.tab4.path
        tsvpath = self.tab2.path

        print("path to fasta = " + fastapath)
        print("path to tsv = " + tsvpath)

        if (fastapath != "") & (tsvpath != ""):
            self.tab3.readFile("../examples/data/iPRG2015.mzTab")


if __name__== '__main__':
    app = QApplication(sys.argv)
    ex = AppGUITabs()
    sys.exit(app.exec_())
