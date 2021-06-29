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

path = "dados_mensais" # use your path
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=9, sep=';')
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)
frame.data_medicao = pd.to_datetime(frame.data_medicao)
frame.precipitacao.notnull()

df_Q1 = frame.loc[frame.precipitacao.notnull()].loc[frame.data_medicao <= periodo_Q1].groupby(['latitude', 'longitude', 'altitude'])

print(df_Q1.head())
#print(frame.info())