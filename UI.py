import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget,
                            QComboBox, QHBoxLayout, QGroupBox, QVBoxLayout,
                            QAction)
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QIcon
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
        
        mainMenu = self.menuBar()
        helpMenu = mainMenu.addMenu('Ajuda')
        
        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        helpMenu.addAction(exitButton)
        
        self.table_widget = TabsWidget(self)
        self.setCentralWidget(self.table_widget)
        self.show()

class TabsWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Objeto com plot e Dataframe
        self.backend = plot.Visualizer()
        self.variavel_mapa = "precipitacao"

        # Criar abas
        self.tabs = QTabWidget()
        self.tab_mapa = QWidget()
        self.tab_associacao = QWidget()
        self.tabs.resize(300,200)

        self.tabs.addTab(self.tab_mapa,"Mapa")
        self.tabs.addTab(self.tab_associacao,"Associação")
        
        ### ABAS

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
        self.backend.definir_periodo(0,1, self.variavel_mapa)

        self.tab_mapa.figure = FigureCanvas()
        self.tab_mapa.figure = self.plot_grafico(self.tab_mapa.figure)

        self.tab_mapa.layout = QVBoxLayout()
        self.tab_mapa.layout.addWidget(self.tab_mapa.horizontalGroupBox)
        self.tab_mapa.layout.addWidget(self.tab_mapa.figure)
        self.tab_mapa.setLayout(self.tab_mapa.layout)



        # Modificar 2a aba
        self.tab_associacao.horizontalGroupBox = QGroupBox("Propriedades")
        tab_associacao_bt_layout = QHBoxLayout()
        
        # Elementos de Input
        self.tab_associacao.cmb_variavel = []
        self.tab_associacao.cmb_variavel.append(QComboBox(self))
        self.tab_associacao.cmb_variavel.append(QComboBox(self))
        self.tab_associacao.cmb_variavel.append(QComboBox(self))
        cmb_variaveis_list = ["Precipitação", "Temperatura", "Nebulosidade", "Vel. Média do Vento"]
        for cmb in self.tab_associacao.cmb_variavel:
            cmb.addItems(cmb_variaveis_list)
            tab_associacao_bt_layout.addWidget(cmb)
            cmb.activated.connect(self.associacao_onchange)
        self.tab_associacao.cmb_variavel[-1].addItems(["Nenhuma"])
        self.tab_associacao.horizontalGroupBox.setLayout(tab_associacao_bt_layout)

        # Elementos gráficos
        self.tab_associacao.figure = FigureCanvas()
        #self.tab_associacao.figure = self.plot_grafico(self.tab_associacao.figure, associacao=True,
        #                                                variaveis=["precipitacao", "precipitacao", "precipitacao"])

        self.tab_associacao.layout = QVBoxLayout()
        self.tab_associacao.layout.addWidget(self.tab_associacao.horizontalGroupBox)
        self.tab_associacao.layout.addWidget(self.tab_associacao.figure)
        self.tab_associacao.setLayout(self.tab_associacao.layout)



        # Adicionar abas
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def plot_grafico(self, figure_canvas:FigureCanvas, associacao=False, variaveis=[]):
        # Elemento gráfico
        if(not associacao): figure = self.backend.plot_periodo_mapa()
        else:
            figure = self.backend.plot_associacao(variaveis)
        figure_canvas = FigureCanvas(figure)
        return figure_canvas

    def periodo_onchange(self):
        # Condição para primeiro periodo ou intervalo
        if(self.tab_mapa.cmb_periodo_inicio.currentIndex() -1 > self.tab_mapa.cmb_periodo_final.currentIndex()):
            self.tab_mapa.cmb_periodo_final.setCurrentIndex(self.tab_mapa.cmb_periodo_inicio.currentIndex() -1)
        if(self.tab_mapa.cmb_periodo_inicio.currentIndex() == 0):
            self.backend.definir_periodo(0,self.tab_mapa.cmb_periodo_final.currentIndex(), self.variavel_mapa)
        else:
            self.backend.definir_periodo(self.tab_mapa.cmb_periodo_inicio.currentIndex() - 1,self.tab_mapa.cmb_periodo_final.currentIndex(), self.variavel_mapa)
        # Limpar o canvas e adicionar novamente
        self.tab_mapa.layout.removeWidget(self.tab_mapa.figure)
        self.tab_mapa.figure = self.plot_grafico(self.tab_mapa.figure)
        self.tab_mapa.figure.draw()
        self.tab_mapa.layout.addWidget(self.tab_mapa.figure)

    def variavel_filter(self,variavel:int):
        if(variavel == 0): return "precipitacao"
        if(variavel == 1): return "temperatura_media"
        if(variavel == 2): return "nebulosidade"
        if(variavel == 3): return "vento_media"
        else: return False

    def variavel_onchange(self):
        variavel_pre = self.tab_mapa.cmb_variavel.currentIndex()
        self.variavel_mapa = self.variavel_filter(variavel_pre)
        self.periodo_onchange()

    def associacao_onchange(self):
        variaveis_list = []
        for cmb in self.tab_associacao.cmb_variavel:
            variaveis_list.append(self.variavel_filter(cmb.currentIndex()))
        self.tab_associacao.layout.removeWidget(self.tab_associacao.figure)
        self.tab_associacao.figure = self.plot_grafico(self.tab_associacao.figure, associacao=True, variaveis=variaveis_list)
        self.tab_associacao.figure.draw()
        self.tab_associacao.layout.addWidget(self.tab_associacao.figure)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
