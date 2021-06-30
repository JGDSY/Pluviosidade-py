import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QComboBox, QHBoxLayout, QGroupBox, QVBoxLayout
from PyQt5 import QtGui, QtCore
import matplotlib as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import plot

class App(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.title = 'PY'
        self.left = 300
        self.top = 100
        self.width = 640
        self.height = 600
        #self.UiComponents()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        
        #mainMenu = self.menuBar()
        #fileMenu = mainMenu.addMenu('File')
        #editMenu = mainMenu.addMenu('Edit')
        #viewMenu = mainMenu.addMenu('View')
        #searchMenu = mainMenu.addMenu('Search')
        #toolsMenu = mainMenu.addMenu('Tools')
        #helpMenu = mainMenu.addMenu('Help')
        
        #exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        #exitButton.setShortcut('Ctrl+Q')
        #exitButton.setStatusTip('Exit application')
        #exitButton.triggered.connect(self.close)
        #fileMenu.addAction(exitButton)
        
        self.table_widget = TabsWidget(self)
        self.setCentralWidget(self.table_widget)
        self.show()

class TabsWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Objeto com plot e Dataframe
        self.backend = plot.Visualizer()
        self.variavel = "precipitacao"

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
        cmb_variaveis_list = ["Precipitação", "Temperatura", "Nebulosidade", "Vel. Média do Vento"]
        self.tab_mapa.cmb_variavel.addItems(cmb_variaveis_list)
        tab_mapa_bt_layout.addWidget(self.tab_mapa.cmb_variavel)
        self.tab_mapa.cmb_variavel.activated.connect(self.variavel_onchange)

        self.tab_mapa.cmb_periodo_inicio = QComboBox()
        cmb_periodo_inicio_list = ["Início do ano", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                                    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        self.tab_mapa.cmb_periodo_inicio.addItems(cmb_periodo_inicio_list)
        tab_mapa_bt_layout.addWidget(self.tab_mapa.cmb_periodo_inicio)
        self.tab_mapa.cmb_periodo_inicio.activated.connect(self.periodo_onchange)

        self.tab_mapa.cmb_periodo_final = QComboBox()
        cmb_periodo_final_list = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                                    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        self.tab_mapa.cmb_periodo_final.addItems(cmb_periodo_final_list)
        tab_mapa_bt_layout.addWidget(self.tab_mapa.cmb_periodo_final)
        self.tab_mapa.cmb_periodo_final.activated.connect(self.periodo_onchange)
        
        self.tab_mapa.horizontalGroupBox.setLayout(tab_mapa_bt_layout)

        # Elementos gráficos
        self.backend.definir_periodo(0,1, self.variavel)

        self.tab_mapa.figure = FigureCanvas()
        self.tab_mapa.figure = self.plot_grafico(self.tab_mapa.figure)

        self.tab_mapa.layout = QVBoxLayout()
        self.tab_mapa.layout.addWidget(self.tab_mapa.horizontalGroupBox)
        self.tab_mapa.layout.addWidget(self.tab_mapa.figure)
        self.tab_mapa.setLayout(self.tab_mapa.layout)

        # Adicionar abas
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def plot_grafico(self, figure_canvas):
        # Elemento gráfico
        figure = self.backend.plot_periodo()
        figure_canvas = FigureCanvas(figure)
        return figure_canvas

    def periodo_onchange(self):
        # Condição para primeiro periodo ou intervalo
        if(self.tab_mapa.cmb_periodo_inicio.currentIndex() -1 > self.tab_mapa.cmb_periodo_final.currentIndex()):
            self.tab_mapa.cmb_periodo_final.setCurrentIndex(self.tab_mapa.cmb_periodo_inicio.currentIndex() -1)
        if(self.tab_mapa.cmb_periodo_inicio.currentIndex() == 0):
            self.backend.definir_periodo(0,self.tab_mapa.cmb_periodo_final.currentIndex(), self.variavel)
        else:
            self.backend.definir_periodo(self.tab_mapa.cmb_periodo_inicio.currentIndex() - 1,self.tab_mapa.cmb_periodo_final.currentIndex(), self.variavel)
        # Limpar o canvas e adicionar novamente
        self.tab_mapa.layout.removeWidget(self.tab_mapa.figure)
        self.tab_mapa.figure = self.plot_grafico(self.tab_mapa.figure)
        self.tab_mapa.figure.draw()
        self.tab_mapa.layout.addWidget(self.tab_mapa.figure)

    def variavel_onchange(self):
        variavel_pre = self.tab_mapa.cmb_variavel.currentIndex()
        if(variavel_pre == 0): self.variavel = "precipitacao"
        if(variavel_pre == 1): self.variavel = "temperatura_media"
        if(variavel_pre == 2): self.variavel = "nebulosidade"
        if(variavel_pre == 3): self.variavel = "vento_media"
        self.periodo_onchange()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
