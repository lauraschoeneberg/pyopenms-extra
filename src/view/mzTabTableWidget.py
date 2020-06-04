

import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QVBoxLayout, QTableWidgetItem



class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "mzTabTableWidget"
        self.top = 100
        self.left = 100
        self.width = 500
        self.height = 500

        self.PRT = []
        self.PSM = []   

        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        
        self.tableWidget1 = QTableWidget()
        self.createProtTable()
        
        self.tableWidget2 = QTableWidget()
        self.createPSMTable()
        
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.tableWidget1)
        self.vbox.addWidget(self.tableWidget2)
        self.setLayout(self.vbox)
        self.show()

    def parser(self, file): 
        
        with open(file) as inp:
            for line in inp:
                if line.startswith("PRH"):
                    self.PRT.append(line.strip().split('\t'))
                elif line.startswith("PRT") and not line.endswith("protein_details\n"):
                    self.PRT.append(line.strip().split('\t'))
                elif line.startswith("PSH") or line.startswith("PSM"):
                    self.PSM.append(line.strip().split('\t'))

    def createProtTable(self):

        self.parser('../examples/data/iPRG2015.mzTab') 
        self.tableWidget1.setRowCount(len(self.PRT))
        self.tableWidget1.setColumnCount(len(self.PRT[0]))

        j = 0
        k = 0
                                   
        for item in self.PRT:
            while k < (len(self.PRT)):
                while j < (len(item)):
                 self.tableWidget1.setItem(k,j,QTableWidgetItem(item[j]))
                 j+=1
                else:
                    k+=1
                    j=0
                break       
        
    def createPSMTable(self):

        self.parser('../examples/data/iPRG2015.mzTab') 
        self.tableWidget2.setRowCount(len(self.PSM))
        self.tableWidget2.setColumnCount(len(self.PSM[0]))

        m = 0
        n = 0
        
        for item in self.PSM:
            while n < (len(self.PSM)):
                while m < (len(item)):
                 self.tableWidget2.setItem(n,m,QTableWidgetItem(item[m]))
                 m+=1
                else:
                    n+=1
                    m=0
                break
            
            
            

            
App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
