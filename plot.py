from os import sep
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import glob

path = "dados_mensais" # use your path
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=9, sep=';')
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)
frame.data_medicao = pd.to_datetime(frame.data_medicao)

print(frame.head())
print(frame.info())