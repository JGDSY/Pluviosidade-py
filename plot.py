from os import sep
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas.core.frame import DataFrame
import seaborn as sns

class Visualizer():
    variavel = "precipitacao"
    df = pd.DataFrame()
    df_periodo = pd.DataFrame()

    def __init__(self):
        path = "dados_mensais/dados_mensais.csv"
        self.df = pd.read_csv(path, index_col=None, header=0, sep=';')
        self.df.data_medicao = pd.to_datetime(self.df.data_medicao)

    def definir_periodo(self, inicio:int, fim:int, variavel):
        ano_inicial = '2020-'
        ano_final = '2020-'
        if(inicio != 0 and inicio == fim): inicio -= 1
        if(inicio > 10):
            ano_inicial = '2021-'
            inicio = 1
        if(fim > 10):
            ano_final= '2021-'
            fim = 1
        periodo_inicial = pd.to_datetime(ano_inicial + str(inicio + 2) + '-01')
        periodo_final = pd.to_datetime(ano_final + str(fim + 2) + '-01')
        self.variavel = variavel
        if(inicio == 0):
            self.df_periodo = self.df.loc[self.df[self.variavel].notnull()].loc[self.df.data_medicao <= periodo_final].groupby(["latitude", "longitude"])[self.variavel].mean().reset_index()
        else:
            self.df_periodo = self.df.loc[self.df[self.variavel].notnull()].loc[self.df.data_medicao >= periodo_inicial].loc[self.df.data_medicao <= periodo_final].groupby(["latitude", "longitude"])[self.variavel].mean().reset_index()

    def plot_periodo(self):
        title = ""
        color = ""
        if(self.variavel == "precipitacao"):
            title = "Precipitação (mm)"
            color = "ch:s=.25,rot=-.25"
        if(self.variavel == "temperatura_media"):
            title = "Temperatura Média (ºC)"
            color = "Reds"
        if(self.variavel == "nebulosidade"):
            title = "Nebulosidade (décimos)"
            color = "Greens"
        if(self.variavel == "vento_media"):
            title = "Velocidade do vento(m/s)"
            color = "Greys"
        plt.clf()
        fig = sns.scatterplot(data=self.df_periodo, x="longitude", y="latitude", s=11, hue=self.variavel, palette=sns.color_palette(color, as_cmap=True))
        fig.axis("Off")
        fig.legend(title=title, shadow=True)
        return fig.get_figure()
