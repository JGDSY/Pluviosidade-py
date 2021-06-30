from os import sep
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas.core.frame import DataFrame
import seaborn as sns

class Visualizer():
    periodo = [pd.to_datetime('2020-03-31'), 
                pd.to_datetime('2020-06-30'),
                pd.to_datetime('2020-09-30'),
                pd.to_datetime('2020-12-31')]
    df = pd.DataFrame()
    df_periodo = pd.DataFrame()

    def __init__(self):
        path = "dados_mensais/dados_mensais.csv"
        self.df = pd.read_csv(path, index_col=None, header=0, sep=';')

        self.df.data_medicao = pd.to_datetime(self.df.data_medicao)

    def definir_periodo(self, inicio:int, fim:int):
        if not inicio:
            self.df_periodo = self.df.loc[self.df.precipitacao.notnull()].loc[self.df.data_medicao <= self.periodo[fim]]
        else:
            self.df_periodo = self.df.loc[self.df.precipitacao.notnull()].loc[self.df.data_medicao >= self.periodo[inicio]].loc[self.df.data_medicao <= self.periodo[fim]]
        
    def plot_periodo(self):
        fig = sns.scatterplot(x=self.df_periodo.longitude, y=self.df_periodo.latitude, hue=self.df_periodo.precipitacao, palette=sns.color_palette("ch:s=.25,rot=-.25", as_cmap=True))
        plt.show()
        return fig.get_figure()
    #print(df_periodo)
    #print(df.info())

    #plt.scatter(df_periodo.longitude, df_periodo.latitude)
    #plt.show()

    #fig = sns.FacetGrid(df_periodo, hue=df_periodo.precipitacao, palette=sns.color_palette("ch:s=.25,rot=-.25", as_cmap=True))
