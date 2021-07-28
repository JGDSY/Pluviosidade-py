import pandas as pd
import matplotlib.pyplot as plt
# import numpy as np
import seaborn as sns
import folium
import io
import os
from scipy import stats


class Visualizer:
    variable_map = "precipitacao"
    df = pd.DataFrame()
    df_period = pd.DataFrame()

    def __init__(self):
        path = "dados_mensais/dados_mensais.csv"
        self.df = pd.read_csv(path, index_col=None, header=0, sep=';')
        self.df.data_medicao = pd.to_datetime(self.df.data_medicao)

    # Plot de variável única por geolocação
    def set_period(self, start: int, end: int, variable):
        year_start = '2020-'
        year_end = '2020-'
        if start != 0 and start == end:
            start -= 1
        if start > 10:
            year_start = '2021-'
            start = 1
        if end > 10:
            year_end = '2021-'
            end = 1
        period_start = pd.to_datetime(year_start + str(start + 2) + '-01')
        period_end = pd.to_datetime(year_end + str(end + 2) + '-01')
        self.variable_map = variable
        if start == 0:
            self.df_period = \
                self.df.loc[self.df[self.variable_map].notnull()].loc[self.df.data_medicao <= period_end].groupby(
                    ["latitude", "longitude"])[self.variable_map].mean().reset_index()
        else:
            self.df_period = \
                self.df.loc[self.df[self.variable_map].notnull()].loc[self.df.data_medicao >= period_start].loc[
                    self.df.data_medicao <= period_end].groupby(["latitude", "longitude"])[
                    self.variable_map].mean().reset_index()

    def plot_period_map(self):
        title, color = get_variable_title(self.variable_map)
        plt.clf()
        graph = sns.scatterplot(data=self.df_period, x="longitude", y="latitude", s=11, hue=self.variable_map,
                                palette=sns.color_palette(color, as_cmap=True))
        graph.set_ylim(bottom=-35, top=5)
        graph.set_xlim(left=-72, right=-34)
        graph.axis("Off")
        graph.legend(title=title, shadow=True)
        return graph.get_figure()

    # Plot de variáveis por associação
    def plot_association(self, variables: list):
        plt.clf()
        df_association = self.df[self.df[variables[0]] != 0].loc[self.df[variables[1]] != 0].dropna()
        slope, intercept, r_value, p_value, std_err = stats.linregress(df_association[variables[0]],df_association[variables[1]])
        if variables[-2]:
            graph = sns.lmplot(data=df_association,
                               x=variables[0],
                               y=variables[1],
                               line_kws={'color': 'red'},
                               lowess=variables[-1],
                               height=4,
                               legend="coeficiente: {0:.2f}".format(slope))
            #graph.set_xlabel(get_variable_title(variables[0])[0])
            #graph.set_ylabel(get_variable_title(variables[1])[0])
            return graph.fig
        else:
            if not variables[2]:
                graph = sns.scatterplot(data=df_association,
                                        x=variables[0],
                                        y=variables[1], s=11)
            else:
                graph = sns.scatterplot(data=df_association,
                                        x=variables[0],
                                        y=variables[1], s=11,
                                        hue=variables[2],
                                        palette=sns.color_palette("ch:s=.25,rot=-.25", as_cmap=True))
        graph.set_xlabel(get_variable_title(variables[0])[0])
        graph.set_ylabel(get_variable_title(variables[1])[0])
        return graph.get_figure()

    def plot_map_web(self):
        max_value = self.df_period[self.variable_map].max()
        min_value = self.df_period[self.variable_map].min()

        if self.variable_map == "precipitacao":
            color_str = "rgba(35,100,200,"
        elif self.variable_map == "temperatura_media":
            color_str = "rgba(145,35,10,"
        elif self.variable_map == "nebulosidade":
            color_str = "rgba(35,150,35,"
        elif self.variable_map == "vento_media":
            color_str = "rgba(50,50,50,"

        m = folium.Map(location=[-15.7648084, -47.8878119],
                       zoom_start=5)
        for row in self.df_period.iterrows():
            popup_text = '{}: {}'
            popup_text = popup_text.format(self.variable_map,
                                           row[self.variable_map])
            folium.CircleMarker([row['latitude'], row['longitude']],
                                radius=2,
                                fill=True,
                                color=color_str +
                                      str((row[self.variable_map] - min_value) / (max_value - min_value)) +
                                      ")",
                                popup=popup_text).add_to(m)

        data = io.BytesIO()
        m.save(data, close_file=False)
        f = open("folium_map.html", 'w')
        f.write(data.getvalue().decode())
        f.close()
        return "file:///" + os.getcwd() + '/' + "folium_map.html"

def get_variable_title(variable):
        title = ""
        color = ""
        if variable == "precipitacao":
            title = "Precipitação (mm)"
            color = "ch:s=.25,rot=-.25"
        if variable == "temperatura_media":
            title = "Temperatura Média (ºC)"
            color = "Reds"
        if variable == "nebulosidade":
            title = "Nebulosidade (décimos)"
            color = "Greens"
        if variable == "vento_media":
            title = "Velocidade do vento(m/s)"
            color = "Greys"
        return title, color