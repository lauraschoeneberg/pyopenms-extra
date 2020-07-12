import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout
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
        self.layout.addWidget(self.loadButton)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def LFQ(self):

        fastapath = self.tab4.path

        print("path to fasta = " + fastapath)

        if fastapath != "":
            self.tab3.readFile("/home/taiki/Uni/SS20/PYGUI/test.mzTab")


if __name__== '__main__':
    app = QApplication(sys.argv)
    ex = AppGUITabs()
    sys.exit(app.exec_())
