import sys
import pandas as pd
from scipy import stats
import igraph
from matplotlib import pyplot as plt
import numpy as np

data_file = sys.argv[1]

df = pd.read_csv(data_file, index_col='id')

meteo_metrics = ["duration", "peak-reflect_max", "peak-reflect_avg", "peak-area", "avg-speed", "max-speed",
                 "avg-area", "max-area", "avg-reflect_avg", "avg-reflect_max", "delta-reflect"]
netwk_metrics = ["vertices", "edges", "cluster_coef", "avg_degree", "diameter", "shortpath_mean",
                 "num_components", "giant_component", "singletons", "t_delay"]

df1 = df.loc[(df["duration"] <= 2)]
df2 = df.loc[(df["duration"] > 5)]
df5 = df.loc[(df["max-area"] <= 300)]
df6 = df.loc[(df["max-area"] >= 5000)]
df1_5 = pd.merge(df1, df5, how='inner', on=['id'])
df2_6 = pd.merge(df2, df6, how='inner', on=['id'])

print(len(df1))
print(len(df2))
print(len(df5))
print(len(df6))

cont = 0
g = igraph.Graph(directed=False)
g.add_vertices(len(meteo_metrics)+len(netwk_metrics))
g.vs['label'] = meteo_metrics + netwk_metrics
g.vs['color'] = ['grey' for i in range(len(meteo_metrics))] + ['orange' for i in range(len(netwk_metrics))]

weights = []
for meteo_metric in meteo_metrics:
    for netwk_metric in netwk_metrics:
        print(netwk_metric, meteo_metric)
        x1 = df6[meteo_metric].values
        y1 = df6[netwk_metric].values
        corr = stats.pearsonr(x1, y1)
        r = corr[0]
        p = corr[1]

        #print(r, p)
        if p > 0.05:
            continue
        if r <= -0.4 or r >= 0.6:
            print(r)
            print(netwk_metric, meteo_metric, r, p)
            g.add_edge(g.vs.find(label=netwk_metric), g.vs.find(label=meteo_metric))
            plt.scatter(x1, y1, marker='.')
            m, b = np.polyfit(x1, y1, 1)
            plt.title('Network Metric x Meteorological property')
            plt.plot(x1, m * x1 + b, color='darkblue', label='y={:.2f}'.format(m)+'x+{:.2f}'.format(b))
            plt.xlabel(meteo_metric)
            plt.ylabel(netwk_metric)
            plt.grid()
            print(m, b)
            plt.legend()
            plt.show()

            weights.append(r)
            cont = cont + 1

        #plt.scatter(df[meteo_metric].values, df[netwk_metric].values)
        #plt.scatter(df["max-area"].values, df[netwk_metric].values)
        #plt.title(meteo_metric + " x " + netwk_metric)
        #plt.show()
sys.exit()

# Grafo das metricas
g.es['weight'] = weights
g.es['color'] = ['red' if es['weight'] < 0 else 'blue' for es in g.es]
widths = []
for weight in weights:
    if (weight >= 0.3 and weight < 0.4) or (weight > -0.4 and weight <= -0.3):
        widths.append(1)
    elif (weight >= 0.4 and weight < 0.5) or (weight > -0.5 and weight <= -0.4):
        widths.append(2)
    elif (weight >= 0.5 and weight < 0.6) or (weight > -0.6 and weight <= -0.5):
        widths.append(3)
    elif (weight >= 0.6 and weight < 0.7) or (weight > -0.7 and weight <= -0.6):
        widths.append(4)
    elif weight >= 0.7 or weight <= -0.7:
        widths.append(5)

g.es['width'] = widths
layout = g.layout("circular")
for v in g.vs:
    print(v['label'] + '=' + str(g.strength(v, weights=weights, mode='all')))

igraph.plot(g, layout=layout, vertex_size=30, vertex_label_size=12, margin=[40, 40, 40, 40], target='graph_D2.pdf')

# Métricas dos eventos no tempo
"""
for netwk_metric in netwk_metrics:
    for id_evento in df.index.values:
        inicio = df['inicio'].loc[id_evento]
        fim = df['fim'].loc[id_evento]
        x = [inicio, fim]
        y = [df[netwk_metric].loc[id_evento], df[netwk_metric].loc[id_evento]]

        plt.plot(x, y)
        plt.xlim('2019-01-01 00:00', '2019-03-31 23:00')
        plt.show()
"""

# Eventos que intersectam no tempo
"""
ig = 0
for rowi in range(len(df.index.values)):
    id_evento1 = df.index[rowi]
    group = [id_evento1]
    inicio1 = df['inicio'].loc[id_evento1]
    fim1 = df['fim'].loc[id_evento1]
    inicio_dt1 = datetime.datetime.strptime(inicio1, '%Y-%m-%d %H:%M:%S')
    fim_dt1 = datetime.datetime.strptime(fim1, '%Y-%m-%d %H:%M:%S')
    for rowj in range(rowi+1, len(df.index.values)):
        id_evento2 = df.index[rowj]
        inicio2 = df['inicio'].loc[id_evento2]
        fim2 = df['fim'].loc[id_evento2]
        inicio_dt2 = datetime.datetime.strptime(inicio2, '%Y-%m-%d %H:%M:%S')
        fim_dt2 = datetime.datetime.strptime(fim2, '%Y-%m-%d %H:%M:%S')
        if (inicio_dt2 >= inicio_dt1 and inicio_dt2 <= fim_dt1) or (fim_dt2 >= inicio_dt1 and fim_dt2 <= fim_dt1):
            #print(id_evento1, id_evento2, inicio1, fim1, inicio2, fim2)
            group.append(id_evento2)
    if len(group) > 1:
        print(ig, len(group))
        ig = ig + 1
"""