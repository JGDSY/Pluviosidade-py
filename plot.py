from os import sep
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import glob

periodo_Q1 = pd.to_datetime('2020-03-31')
periodo_Q2 = pd.to_datetime('2020-06-30')
periodo_Q3 = pd.to_datetime('2020-09-30')
periodo_Q4 = pd.to_datetime('2020-12-31')

path = "dados_mensais/dados_mensais.csv"
df = pd.read_csv(path, index_col=None, header=0, sep=';')

df.data_medicao = pd.to_datetime(df.data_medicao)

df_periodo = df.loc[df.precipitacao.notnull()].loc[df.data_medicao <= periodo_Q1]


#print(df_periodo)
#print(df.info())

#plt.scatter(df_periodo.longitude, df_periodo.latitude)
#plt.show()

#fig = sns.FacetGrid(df_periodo, hue=df_periodo.precipitacao, palette=sns.color_palette("ch:s=.25,rot=-.25", as_cmap=True))


fig = sns.scatterplot(x=df_periodo.longitude,y=df_periodo.latitude, hue=df_periodo.precipitacao, palette=sns.color_palette("ch:s=.25,rot=-.25", as_cmap=True))
plt.show()
