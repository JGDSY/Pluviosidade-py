import sys
import PyQt5
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QTabWidget, QWidget,
                             QComboBox, QHBoxLayout, QGroupBox, QVBoxLayout,
                             QAction, QPushButton, QCheckBox)
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import plot
import webbrowser


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PluviosidadePY'
        self.left = 350
        self.top = 50
        self.width = 640
        self.height = 600
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)

        main_menu = self.menuBar()
        help_menu = main_menu.addMenu('Ajuda')

        btn_help = QAction('Ajuda', self)
        btn_help.setShortcut('Ctrl+A')
        btn_help.setStatusTip('Ver detalhes')
        btn_help.triggered.connect(self.show_help)
        help_menu.addAction(btn_help)
        self.help_window = HelpWindow()

        btn_exit = QAction(QIcon('exit24.png'), 'Exit', self)
        btn_exit.setShortcut('Ctrl+Q')
        btn_exit.setStatusTip('Exit application')
        btn_exit.triggered.connect(self.close)
        help_menu.addAction(btn_exit)

        self.table_widget = TabsWidget(self)
        self.setCentralWidget(self.table_widget)
        self.show()

    def show_help(self):
        self.help_window.show()


def variable_filter(variable: int):
    if variable == 0:
        return "precipitacao"
    if variable == 1:
        return "temperatura_media"
    if variable == 2:
        return "temperatura_maxima"
    if variable == 3:
        return "temperatura_minima"
    if variable == 4:
        return "nebulosidade"
    if variable == 5:
        return "umidade_relativa"
    if variable == 6:
        return "vento_media"
    if variable == 7:
        return "vento_maxima"
    else:
        return False


class HelpWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Ajuda'
        self.left = 370
        self.top = 200
        self.width = 640
        self.height = 250
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.layout = QVBoxLayout(self)

        self.lbl_help_text = QLabel()
        self.lbl_help_text.setText("A primeira aba contém a visualização dos dados por geolocação.\n" +
                                   "Um mapa interativo pode ser acessado pelo navegador através do respectivo botão\n" +
                                   "A segunda aba permite a visualização de múltiplas variáveis e suas associações.\n" +
                                   "Os gráficos com modelo de regressão não permitem uma terceira variável representada pela cor, então essa opção é ignorada\n\n" +
                                   "Todos os dados foram utilizados estão disponíveis no portal do INMET")
        self.btn_inmet = QPushButton()
        self.btn_inmet.setText("INMET")
        self.btn_inmet.clicked.connect(self.open_inmet)
        self.btn_exit = QPushButton()
        self.btn_exit.setText("Voltar")
        self.btn_exit.clicked.connect(self.close)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_exit)
        btn_layout.addWidget(self.btn_inmet)
        btn_group_box = QGroupBox()
        btn_group_box.setLayout(btn_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_help_text)
        layout.addWidget(btn_group_box)

        group_box = QGroupBox()
        group_box.setLayout(layout)

        self.setCentralWidget(group_box)


    def open_inmet(self):
        webbrowser.open("https://bdmep.inmet.gov.br/#", new=0)


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
        tab_map_bt_layout = QHBoxLayout(self)
        tab_map_label_layout = []
        tab_map_label_layout.append(QVBoxLayout(self))
        tab_map_label_layout.append(QVBoxLayout(self))
        tab_map_label_layout.append(QVBoxLayout(self))

        # Elementos de Input
        self.tab_map.lbl_variable = QLabel(self)
        self.tab_map.lbl_variable.setText("Variável")
        tab_map_label_layout[0].addWidget(self.tab_map.lbl_variable)
        self.tab_map.cmb_variable = QComboBox(self)
        cmb_variables_list = ["Precipitação", "Temperatura média", "Temperatura máxima",
                              "Temperatura mínima", "Nebulosidade", "Umidade do ar",
                              "Vel. média do Vento", "Vel. máxima do Vento"]
        self.tab_map.cmb_variable.addItems(cmb_variables_list)
        tab_map_label_layout[0].addWidget(self.tab_map.cmb_variable)
        self.tab_map.cmb_variable.activated.connect(self.variable_onchange)

        self.tab_map.lbl_period_start = QLabel(self)
        self.tab_map.lbl_period_start.setText("Início")
        tab_map_label_layout[1].addWidget(self.tab_map.lbl_period_start)
        self.tab_map.cmb_period_start = QComboBox()
        cmb_period_start_list = ["Início do ano", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                                 "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        self.tab_map.cmb_period_start.addItems(cmb_period_start_list)
        tab_map_label_layout[1].addWidget(self.tab_map.cmb_period_start)
        self.tab_map.cmb_period_start.activated.connect(self.period_onchange)

        self.tab_map.lbl_period_end = QLabel(self)
        self.tab_map.lbl_period_end.setText("Fim")
        tab_map_label_layout[2].addWidget(self.tab_map.lbl_period_end)
        self.tab_map.cmb_period_end = QComboBox()
        cmb_period_end_list = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                               "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        self.tab_map.cmb_period_end.addItems(cmb_period_end_list)
        tab_map_label_layout[2].addWidget(self.tab_map.cmb_period_end)
        self.tab_map.cmb_period_end.activated.connect(self.period_onchange)

        self.tab_map.lbl_cmb_group = []
        for index in range(len(tab_map_label_layout)):
            self.tab_map.lbl_cmb_group.append(QGroupBox(self))
            self.tab_map.lbl_cmb_group[index].setLayout(tab_map_label_layout[index])
            tab_map_bt_layout.addWidget(self.tab_map.lbl_cmb_group[index])
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

        self.tab_association.lbl_regression_line = QLabel()
        self.tab_association.lbl_regression_line.setText("")

        self.tab_association.cmb_regression_model = QComboBox()
        self.tab_association.cmb_regression_model.addItems(["Regressão linear", "Regressão de Lowess"])
        self.tab_association.cmb_regression_model.activated.connect(
            lambda: self.association_onchange() if self.tab_association.chb_regression_line.isChecked() else None)
        # inline if para economizar um gráfico se a regressão está desativada

        tab_association_chb_layout.addWidget(self.tab_association.chb_regression_line)
        tab_association_chb_layout.addWidget(self.tab_association.lbl_regression_line)
        tab_association_chb_layout.addWidget(self.tab_association.cmb_regression_model)
        self.tab_association.horizontalGroupBoxOptions.setLayout(tab_association_chb_layout)

        # Elementos gráficos
        self.tab_association.figure = FigureCanvas()
        
        self.tab_association.layout = QVBoxLayout()
        self.tab_association.layout.addWidget(self.tab_association.horizontalGroupBox)
        self.tab_association.layout.addWidget(self.tab_association.horizontalGroupBoxOptions)
        self.tab_association.layout.addWidget(self.tab_association.figure, alignment=PyQt5.QtCore.Qt.AlignCenter)
        self.tab_association.setLayout(self.tab_association.layout)

        # Adicionar abas
        self.layout.addWidget(self.tabs)

    def plot_graph(self, figure_canvas: FigureCanvas, association=False, variables=[]):
        # Elemento gráfico
        if not association:
            figure = self.backend.plot_period_map()
        else:
            figure, regression = self.backend.plot_association(variables)
            self.tab_association.lbl_regression_line.setText(regression)
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
        self.tab_association.layout.addWidget(self.tab_association.figure, alignment=PyQt5.QtCore.Qt.AlignCenter)

    def browser_onclick(self):
        webbrowser.open(self.backend.plot_map_web(), new=0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
