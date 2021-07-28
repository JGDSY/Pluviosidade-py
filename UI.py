import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget,
                             QComboBox, QHBoxLayout, QGroupBox, QVBoxLayout,
                             QAction, QPushButton, QCheckBox)
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import plot
import webbrowser


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PY'
        self.left = 350
        self.top = 50
        self.width = 640
        self.height = 600
        # self.UiComponents()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)

        main_menu = self.menuBar()
        help_menu = main_menu.addMenu('Ajuda')

        btn_exit = QAction(QIcon('exit24.png'), 'Exit', self)
        btn_exit.setShortcut('Ctrl+Q')
        btn_exit.setStatusTip('Exit application')
        btn_exit.triggered.connect(self.close)
        help_menu.addAction(btn_exit)

        self.table_widget = TabsWidget(self)
        self.setCentralWidget(self.table_widget)
        self.show()


def variable_filter(variable: int):
    if variable == 0:
        return "precipitacao"
    if variable == 1:
        return "temperatura_media"
    if variable == 2:
        return "nebulosidade"
    if variable == 3:
        return "vento_media"
    else:
        return False


class TabsWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Objeto com plot e Dataframe
        self.backend = plot.Visualizer()
        self.variable_map = "precipitacao"

        # Criar abas
        self.tabs = QTabWidget()
        self.tab_map = QWidget()
        self.tab_association = QWidget()
        self.tabs.resize(300, 200)

        self.tabs.addTab(self.tab_map, "Mapa")
        self.tabs.addTab(self.tab_association, "Associação")

        # ABAS

        # Modificar 1a aba
        self.tab_map.horizontalGroupBox = QGroupBox("Propriedades")
        tab_map_bt_layout = QHBoxLayout()

        # Elementos de Input
        self.tab_map.cmb_variable = QComboBox(self)
        cmb_variables_list = ["Precipitação", "Temperatura", "Nebulosidade", "Vel. Média do Vento"]
        self.tab_map.cmb_variable.addItems(cmb_variables_list)
        tab_map_bt_layout.addWidget(self.tab_map.cmb_variable)
        self.tab_map.cmb_variable.activated.connect(self.variable_onchange)

        self.tab_map.cmb_period_start = QComboBox()
        cmb_period_start_list = ["Início do ano", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                                 "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        self.tab_map.cmb_period_start.addItems(cmb_period_start_list)
        tab_map_bt_layout.addWidget(self.tab_map.cmb_period_start)
        self.tab_map.cmb_period_start.activated.connect(self.period_onchange)

        self.tab_map.cmb_period_end = QComboBox()
        cmb_period_end_list = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                               "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        self.tab_map.cmb_period_end.addItems(cmb_period_end_list)
        tab_map_bt_layout.addWidget(self.tab_map.cmb_period_end)
        self.tab_map.cmb_period_end.activated.connect(self.period_onchange)

        self.tab_map.horizontalGroupBox.setLayout(tab_map_bt_layout)

        self.tab_map.btn_browser = QPushButton()
        self.tab_map.btn_browser.setText("Abrir no navegador")
        self.tab_map.btn_browser.clicked.connect(self.browser_onclick)

        # Elementos gráficos
        self.backend.set_period(0, 1, self.variable_map)

        self.tab_map.figure = FigureCanvas()
        self.tab_map.figure = self.plot_graph(self.tab_map.figure)

        self.tab_map.layout = QVBoxLayout()
        self.tab_map.layout.addWidget(self.tab_map.horizontalGroupBox)
        self.tab_map.layout.addWidget(self.tab_map.btn_browser)
        self.tab_map.layout.addWidget(self.tab_map.figure)
        self.tab_map.setLayout(self.tab_map.layout)

        # Modificar 2a aba
        self.tab_association.horizontalGroupBox = QGroupBox("Propriedades")
        tab_association_bt_layout = QHBoxLayout()

        # Elementos de Input
        self.tab_association.cmb_variable = []
        self.tab_association.cmb_variable.append(QComboBox(self))
        self.tab_association.cmb_variable.append(QComboBox(self))
        self.tab_association.cmb_variable.append(QComboBox(self))
        cmb_variables_list = ["Precipitação", "Temperatura", "Nebulosidade", "Vel. Média do Vento"]
        for cmb in self.tab_association.cmb_variable:
            cmb.addItems(cmb_variables_list)
            tab_association_bt_layout.addWidget(cmb)
            cmb.activated.connect(self.association_onchange)
        self.tab_association.cmb_variable[-1].addItems(["Nenhuma"])
        self.tab_association.horizontalGroupBox.setLayout(tab_association_bt_layout)

        self.tab_association.horizontalGroupBoxOptions = QGroupBox("Opções")
        tab_association_chb_layout = QHBoxLayout()
        self.tab_association.chb_regression_line = QCheckBox()
        self.tab_association.chb_regression_line.setText("Modelo de regressão")
        self.tab_association.chb_regression_line.stateChanged.connect(self.association_onchange)

        self.tab_association.cmb_regression_model = QComboBox()
        self.tab_association.cmb_regression_model.addItems(["Regressão linear", "Regressão de Lowess"])
        self.tab_association.cmb_regression_model.activated.connect(
            lambda: self.association_onchange() if self.tab_association.chb_regression_line.isChecked() else None)
        # inline if para economizar um gráfico se a regressão está desativada

        tab_association_chb_layout.addWidget(self.tab_association.chb_regression_line)
        tab_association_chb_layout.addWidget(self.tab_association.cmb_regression_model)
        self.tab_association.horizontalGroupBoxOptions.setLayout(tab_association_chb_layout)

        # Elementos gráficos
        self.tab_association.figure = FigureCanvas()

        self.tab_association.layout = QVBoxLayout()
        self.tab_association.layout.addWidget(self.tab_association.horizontalGroupBox)
        self.tab_association.layout.addWidget(self.tab_association.horizontalGroupBoxOptions)
        self.tab_association.layout.addWidget(self.tab_association.figure)
        self.tab_association.setLayout(self.tab_association.layout)

        # Adicionar abas
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def plot_graph(self, figure_canvas: FigureCanvas, association=False, variables=[]):
        # Elemento gráfico
        if not association:
            figure = self.backend.plot_period_map()
        else:
            figure = self.backend.plot_association(variables)
        figure_canvas = FigureCanvas(figure)
        return figure_canvas

    def period_onchange(self):
        # Condição para primeiro period ou intervalo
        if self.tab_map.cmb_period_start.currentIndex() - 1 > self.tab_map.cmb_period_end.currentIndex():
            self.tab_map.cmb_period_end.setCurrentIndex(self.tab_map.cmb_period_start.currentIndex() - 1)
        if self.tab_map.cmb_period_start.currentIndex() == 0:
            self.backend.set_period(0, self.tab_map.cmb_period_end.currentIndex(), self.variable_map)
        else:
            self.backend.set_period(self.tab_map.cmb_period_start.currentIndex() - 1,
                                    self.tab_map.cmb_period_end.currentIndex(), self.variable_map)
        # Limpar o canvas e adicionar novamente
        self.tab_map.layout.removeWidget(self.tab_map.figure)
        self.tab_map.figure = self.plot_graph(self.tab_map.figure)
        self.tab_map.figure.draw()
        self.tab_map.layout.addWidget(self.tab_map.figure)

    def variable_onchange(self):
        variable_pre = self.tab_map.cmb_variable.currentIndex()
        self.variable_map = variable_filter(variable_pre)
        self.period_onchange()

    def association_onchange(self):
        variables_list = []
        for cmb in self.tab_association.cmb_variable:
            variables_list.append(variable_filter(cmb.currentIndex()))
        # Últimos índices das variáveis são o modelo de regressão
        variables_list.append(self.tab_association.chb_regression_line.isChecked())
        variables_list.append(self.tab_association.cmb_regression_model.currentIndex())
        self.tab_association.layout.removeWidget(self.tab_association.figure)
        self.tab_association.figure = self.plot_graph(self.tab_association.figure, association=True,
                                                      variables=variables_list)
        self.tab_association.figure.draw()
        self.tab_association.layout.addWidget(self.tab_association.figure)

    def browser_onclick(self):
        webbrowser.open(self.backend.plot_map_web(), new=0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
