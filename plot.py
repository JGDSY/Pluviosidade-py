from os import sep
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas.core.frame import DataFrame
import seaborn as sns

class Visualizer():
    variavel_mapa = "precipitacao"
    df = pd.DataFrame()
    df_periodo = pd.DataFrame()

    def __init__(self):
        path = "dados_mensais/dados_mensais.csv"
        self.df = pd.read_csv(path, index_col=None, header=0, sep=';')
        self.df.data_medicao = pd.to_datetime(self.df.data_medicao)

    # Plot de variável única por geolocação
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
        self.variavel_mapa = variavel
        if(inicio == 0):
            self.df_periodo = self.df.loc[self.df[self.variavel_mapa].notnull()].loc[self.df.data_medicao <= periodo_final].groupby(["latitude", "longitude"])[self.variavel_mapa].mean().reset_index()
        else:
            self.df_periodo = self.df.loc[self.df[self.variavel_mapa].notnull()].loc[self.df.data_medicao >= periodo_inicial].loc[self.df.data_medicao <= periodo_final].groupby(["latitude", "longitude"])[self.variavel_mapa].mean().reset_index()

    def plot_periodo_mapa(self):
        title = ""
        color = ""
        if(self.variavel_mapa == "precipitacao"):
            title = "Precipitação (mm)"
            color = "ch:s=.25,rot=-.25"
        if(self.variavel_mapa == "temperatura_media"):
            title = "Temperatura Média (ºC)"
            color = "Reds"
        if(self.variavel_mapa == "nebulosidade"):
            title = "Nebulosidade (décimos)"
            color = "Greens"
        if(self.variavel_mapa == "vento_media"):
            title = "Velocidade do vento(m/s)"
            color = "Greys"
        plt.clf()
        fig = sns.scatterplot(data=self.df_periodo, x="longitude", y="latitude", s=11, hue=self.variavel_mapa, palette=sns.color_palette(color, as_cmap=True))
        fig.axis("Off")
        fig.legend(title=title, shadow=True)
        return fig.get_figure()

    # Plot de váriaveis por associação
    def plot_associacao(self, variaveis:list):
        plt.clf()
        if(variaveis[2] == False): fig = sns.scatterplot(data=self.df, x=variaveis[0], y=variaveis[1], s=11)
        else: fig = sns.scatterplot(x=self.df[variaveis[0]].loc[self.df[variaveis[0]].notnull()], y=self.df[variaveis[1]].loc[self.df[variaveis[1]].notnull()], s=11, hue=self.df[variaveis[2]].loc[self.df[variaveis[2]].notnull()], palette=sns.color_palette("ch:s=.25,rot=-.25", as_cmap=True))
        #fig.axis("Off")
        #fig.legend(title=title, shadow=True)
        return fig.get_figure()
