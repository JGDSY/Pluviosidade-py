import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QComboBox, QHBoxLayout, QGroupBox, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class App(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.title = 'PY'
        self.left = 300
        self.top = 100
        self.width = 640
        self.height = 400
        #self.UiComponents()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        #mainMenu = self.menuBar()
        #fileMenu = mainMenu.addMenu('File')
        #editMenu = mainMenu.addMenu('Edit')
        #viewMenu = mainMenu.addMenu('View')
        #searchMenu = mainMenu.addMenu('Search')
        #toolsMenu = mainMenu.addMenu('Tools')
        #helpMenu = mainMenu.addMenu('Help')

        self.table_widget = TabsWidget(self)
        self.setCentralWidget(self.table_widget)
        
        #exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        #exitButton.setShortcut('Ctrl+Q')
        #exitButton.setStatusTip('Exit application')
        #exitButton.triggered.connect(self.close)
        #fileMenu.addAction(exitButton)
        
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

class TabsWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Criar abas
        self.tabs = QTabWidget()
        self.tab_mapa = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300,200)

        self.tabs.addTab(self.tab_mapa,"Mapa")
        self.tabs.addTab(self.tab2,"Tab 2")
        
        # Modificar 1a aba
        self.tab_mapa.horizontalGroupBox = QGroupBox("Propriedades")
        tab_mapa_bt_layout = QHBoxLayout()
        
        # Elementos de Input
        self.tab_mapa.cmb_variavel = QComboBox(self)
        cmb_variaveis_list = ["Pluviosidade", "Temperatura", "Nebulosidade", "Vel. Média do Vento"]
        self.tab_mapa.cmb_variavel.addItems(cmb_variaveis_list)
        tab_mapa_bt_layout.addWidget(self.tab_mapa.cmb_variavel)

        self.tab_mapa.cmb_periodo = QComboBox()
        cmb_periodo_list = ["Q1", "Q2", "Q3", "Q4"]
        self.tab_mapa.cmb_periodo.addItems(cmb_periodo_list)
        tab_mapa_bt_layout.addWidget(self.tab_mapa.cmb_periodo)
        
        self.tab_mapa.horizontalGroupBox.setLayout(tab_mapa_bt_layout)

        # Elemento gráfico
        self.tab_mapa.plot_mapa = Figure()

        self.tab_mapa.layout = QVBoxLayout()
        self.tab_mapa.layout.addWidget(self.tab_mapa.horizontalGroupBox)
        self.tab_mapa.setLayout(self.tab_mapa.layout)

        # Adicionar abas
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
