import sys

from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget, QSplitter, QMainWindow, QLabel, QLineEdit, QApplication, QAction, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class HomeTabWidget(QMainWindow):

    
    def __init__(self):
        super().__init__()
        self.title = 'Home'
        self.left = 100
        self.top = 100
        self.width = 600
        self.height = 500
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("background-color:lightgrey;");
        self.HomeWindow()
        
        self.loadedThreads = "1"
        self.loadedFDR = "0.3"
    def HomeWindow(self):
        
        """
        Used to briefly introduce functionality of GUI_Tabs, allows to manually set parameters for cmd command

        """
        self.textwidget = QWidget(self)
        self.vertical = QVBoxLayout(self.textwidget)
        #set margins
        self.vertical.setContentsMargins(5, 15, 100, 15)

        #set labels
        self.HomeTitle = QLabel()
        self.Introduction = QLabel()
        self.EditParameters = QLabel()
        self.Proteomics = QLabel()

        
        self.HomeTitle.setText("<font color = 'darkblue'>Welcome!</font>")
        self.HomeTitle.setFont(QFont("Arial",16))
        self.HomeTitle.move(100,50)
        IntroductionText = """
            This application can be used to display experimental data.
            
            You can choose to manually enter files in each tab or select a folder that contains all data.
            
            For the latter method, simply click 'Load Data'-Button above.
            """
        #TODO: add load data - Button here
        self.Introduction.setText(IntroductionText)
        self.Introduction.setFont(QFont("Arial",12))

        EditText = """
            If you want to edit the parameters 'Threads' or 'proteinFDR', you can do it here:
            """
        self.EditParameters.setText(EditText)
        self.EditParameters.setFont(QFont("Arial",12))

        #set text for textboxes
        self.ThreadText = QLabel()
        self.ThreadText.setText("   Threads:")
        self.ThreadText.setFont(QFont("Arial",12))
        self.FDRText = QLabel()
        self.FDRText.setText("  proteinFDR:")
        self.FDRText.setFont(QFont("Arial",12))

        self.horizontal1 = QHBoxLayout()
        self.horizontal2 = QHBoxLayout()
        self.horizontal3 = QHBoxLayout()
        
        #set Textboxes
        self.ThreadTextBox = QLineEdit(self)
        self.FDRTextBox = QLineEdit(self)
        self.ThreadTextBox.setFixedSize(210,30)
        self.FDRTextBox.setFixedSize(210,30)

        #set button to save parameters
        self.saveButton = QPushButton('Save Parameters!', self)
        self.saveButton.setFont(QFont("Arial",11))
        self.saveButton.setFixedSize(130,40)
        self.saveButton.clicked.connect(self.check_parameters)
        
        ProteomicsText = """
            If you're done, you can execute ProteomicsLFQ by clicking the 'Run ProteomicsLFQ'-Button!
            """
        self.Proteomics.setText(ProteomicsText)
        self.Proteomics.setFont(QFont("Arial",12))

        #add widgets to layouts
        self.textwidget.setLayout(self.vertical)
        
        self.vertical.addWidget(self.HomeTitle)
        self.vertical.addWidget(self.Introduction)
        self.vertical.addWidget(self.EditParameters)
        self.vertical.addLayout(self.horizontal3)
        self.horizontal3.addLayout(self.horizontal1)
        self.horizontal3.addLayout(self.horizontal2)
        
        self.horizontal1.addStretch(4)
        self.horizontal2.addStretch(4)
        self.horizontal3.addStretch(0)
        
        self.horizontal1.addWidget(self.ThreadText)
        self.horizontal1.addWidget(self.ThreadTextBox)

        self.horizontal2.addWidget(self.FDRText)
        self.horizontal2.addWidget(self.FDRTextBox)
        self.horizontal3.addWidget(self.saveButton)

        self.vertical.addWidget(self.Proteomics)

        self.setCentralWidget(self.textwidget)
        self.show()
        
    def check_parameters(self):
        if self.ThreadTextBox.text() == "":
            self.loadedThreads = "1"
        else: self.loadedThreads = self.ThreadTextBox.text()
         
        if self.FDRTextBox.text() == "":
            self.loadedFDR = "0.3"
        else: self.loadedFDR = self.FDRTextBox.text()
        self.ThreadTextBox.clear()
        self.FDRTextBox.clear()
         
        
"""
def main():
        app = QApplication(sys.argv)
        ex = HomeTabWidget()
        sys.exit(app.exec_())

if __name__ == '__main__':
        main()
        
 """       
        
