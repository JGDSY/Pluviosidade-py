import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class App(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 menu - pythonspot.com'
        self.left = 300
        self.top = 100
        self.width = 640
        self.height = 400
        self.UiComponents()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')

        
        
        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)
    
        self.show()

    def UiComponents(self):
        # creating a combo box widget
        self.combo_box = QComboBox(self)
        # setting geometry of combo box
        self.combo_box.setGeometry(200, 150, 150, 30)
        # geek list
        options_list = ["Pluviosidade", "Temperatura"]
        # making it editable
        self.combo_box.setEditable(False)
        # adding list of items to combo box
        self.combo_box.addItems(options_list)
        # setting minimum content length
        self.combo_box.setMinimumContentsLength(3)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
