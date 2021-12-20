import sys
import pandas as pd
import numpy as np
import scipy
import calc
from matplotlib import pyplot as plt
import igraph
import datetime

data_file = sys.argv[1]

df = pd.read_csv(data_file, index_col='id')

#meteo_metrics = ["duracao", "pico_pmax", "pico_pmed", "pico_area_km2", "pico_area_px", "vel_min", "vel_med", "vel_max",
#                 "area_min", "area_med", "area_max", "pmed_med", "pmax_med", "num_eventos_simult", "delta_reflet"]
meteo_metrics = ["duration", "peak-reflect_max", "peak-reflect_avg", "peak-area", "avg-speed", "max-speed",
                 "avg-area", "max-area", "avg-reflect_avg", "avg-reflect_max", "delta-reflect"]
#netwk_metrics = ["vertices", "edges", "cluster_coef", "avg_degree", "diameter", "shortpath_mean",
#                 "avg_betweeness", "num_components", "giant_component_v", "singletons"]
netwk_metrics = ["vertices", "edges", "cluster_coef", "avg_degree", "diameter", "shortpath_mean",
                 "num_components", "giant_component", "singletons", "t_delay"]

# Histogramas
"""
for netwk_metric in netwk_metrics:
    pyplot.hist(df[netwk_metric].values, bins=30)
    pyplot.title(netwk_metric)
    pyplot.show()
for meteo_metric in meteo_metrics:
    pyplot.hist(df[meteo_metric].values, bins=30)
    pyplot.title(meteo_metric)
    pyplot.show()
"""

# Dispersão
#for netwk_metric in netwk_metrics:
#    pyplot.scatter(df[netwk_metric].values, df["duracao"].values)
#    pyplot.title(netwk_metric + " x Duração")
#    pyplot.show()
#for meteo_metric in meteo_metrics:
#    pyplot.scatter(df[meteo_metric].values, df["duracao"].values)
#    pyplot.title(meteo_metric + " x Duração")
#    pyplot.show()

df1 = df.loc[(df["duration"] <= 2)]
df2 = df.loc[(df["duration"] > 5)]
df5 = df.loc[(df["max-area"] <= 300)]
df6 = df.loc[(df["max-area"] >= 5000)]
df1_5 = pd.merge(df1, df5, how='inner', on=['id'])
df2_6 = pd.merge(df2, df6, how='inner', on=['id'])
print(df2_6)
sys.exit()

print(len(df1))
print(len(df2))
print(len(df5))
print(len(df6))
#sys.exit()
#print(df["max-area"].values)
#plt.hist(df5["max-area"].values, bins=30)
#plt.title("max-area")
#plt.show()
#plt.hist(df6["max-area"].values, bins=30)
#plt.title("max-area")
#plt.show()
plt.scatter(df5["max-area"].values, df5["diameter"].values)
plt.show()
plt.scatter(df6["max-area"].values, df6["diameter"].values)
plt.show()
#sys.exit()

cont = 0
g = igraph.Graph(directed=False)
g.add_vertices(len(meteo_metrics)+len(netwk_metrics))
g.vs['label'] = meteo_metrics + netwk_metrics
g.vs['color'] = ['grey' for i in range(len(meteo_metrics))] + ['orange' for i in range(len(netwk_metrics))]

weights = []
for meteo_metric in meteo_metrics:
    #for meteo_metric2 in meteo_metrics:
    for netwk_metric in netwk_metrics:
        print(netwk_metric, meteo_metric)
        x1 = df[meteo_metric].values
        y1 = df[netwk_metric].values
        #y2 = df2[netwk_metric].values
        #y3 = df5[netwk_metric].values
        #y4 = df6[netwk_metric].values

        #plt.boxplot([y1, y2, y3, y4])
        #plt.title(netwk_metric)
        #plt.show()

        #reject, pvalue, b, m, R2 = calc.Stats().ttest_regression(df3[meteo_metric].values,
        #                                                         df3[netwk_metric].values)
        corr = scipy.stats.pearsonr(x1, y1)
        r = corr[0]
        p = corr[1]

        #print(r, p)
        if p > 0.05:
            continue
        if r <= -0.4 or r >= 0.4:
            print(netwk_metric, meteo_metric, r, p)
            g.add_edge(g.vs.find(label=netwk_metric), g.vs.find(label=meteo_metric))

            weights.append(r)
            #           print(r, p)
            cont = cont + 1

        #plt.scatter(df[meteo_metric].values, df[netwk_metric].values)
        #plt.scatter(df["max-area"].values, df[netwk_metric].values)
        #plt.title(meteo_metric + " x " + netwk_metric)
        #plt.show()

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
#neg_corr = [es for es in g.es if es['weight'] < 0]
#neg_corr = g.es.select('weight'<0)
#neg_corr['color'] = 'red'
layout = g.layout("circular")
for v in g.vs:
    print(v['label'] + '=' + str(g.strength(v, weights=weights, mode='all')))

#fig, ax = plt.subplots()
#igraph.plot(g, layout=layout, vertex_size=30, vertex_label_size=12, margin=[40, 40, 40, 40], target=ax)
igraph.plot(g, layout=layout, vertex_size=30, vertex_label_size=12, margin=[40, 40, 40, 40], target='graph_D2.pdf')
#plt.show()

#degrees = np.array(g.degree())
#vmax = np.argmax(degrees)
#print(g.vs[vmax]['label'])
for v in g.vs:
    print(v['label'], v.degree(), v.betweenness())

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
#for id_evento in df.index.values:
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