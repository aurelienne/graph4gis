import datetime
import sys
import data as rd
import graph
from calc import Stats
import output as out
import numpy as np

# Recorte Bacia Tamanduatei (PPI)
nx = 36
ny = 37
dx = 0.00747135
dy = -0.00675451
x1 = -46.665909175
y1 = -23.509574965000002
x2 = x1 + nx*dx
y2 = y1 + ny*dy

# Recorte Bacia Tamanduatei (CAPPI)
#dx = 0.009957
#dy = -0.0090014
#nx = 27
#ny = 29
#x1 = -46.6608
#y1 = -23.514
#x2 = x1 + nx*dx
#y2 = y1 + ny*dy

# RMSP + 10km
#nx = 172
#ny = 120
#x1 = -47.317405
#y1 = -23.092909
#x2 = -45.604801
#y2 = -24.173077
#dx = 0.009957
#dy = -0.0090014

input_list = sys.argv[1]
threshold = float(sys.argv[2])

df = rd.Data(x1, y1, x2, y2, dx, dy, nx, ny)
df.import_bin_from_list(input_list)
#matrix = df.get_pearson_correlation()
matrix = df.get_pearson_correlation_timedelay(datetime.timedelta(minutes=10))

stats = Stats()
#stats.pearson_significance_test(df.time_series)
#stats.shuffle(df.time_series, matrix, 100)
#stats.ttest(len(df.time_series), 0.86, 0.05)

#dists = df.get_euclidean_distances()
#df.get_neighbours()

g = graph.Graph.from_correlation_matrix(matrix, threshold, df.xlist, df.ylist)

plt = out.Plots(g)

graph.Graph.calculate_vertices_metrics(g)
g.vs["shortestPathMean"] = graph.Graph.get_shortest_path_mean(g)
#g.write_graphml('GT.GraphML')
topol_dists = np.array(g.shortest_paths())
avg_cluster = graph.Graph.get_average_clustering(g)
avg_degree = graph.Graph.get_average_degree(g)
diameter = g.diameter(directed=False)
shortpath_mean = graph.Graph.get_average_shortest_path_mean(g)
#graph.Graph.get_manhattan_shortest_paths(g)

"""
print("Regression T-Test:")
idxs = np.triu_indices(dists.shape[0], k=1)
x = dists[idxs].flatten()
y1 = topol_dists[idxs].flatten()
idx = np.isfinite(y1)
x1 = x[idx]
y1 = y1[idx]
reject, pvalues, b, slope = stats.ttest_regression(x1, y1)
print("reject = "+str(reject)+" p-value = "+str(pvalues))
"""

#g.plot("grafo.svg")

out.Shapefile(g, "grafo_"+str(threshold)).create_shape("", dx, dy)
#out_csv = out.TextFiles(g)
#out_csv.create_global_metrics_csv(threshold, "correlation_x_global_metrics.csv", avg_degree, avg_cluster, diameter, shortpath_mean)
#out_csv.create_vertex_metrics_csv("vertex_metrics.csv")
#out_csv.create_adjacency_list("adjacency_list.csv")

plt = out.Plots(g)
#plt.plot_shortpath_histogram()
#plt.plot_correlation_histogram(matrix, threshold=0.86)

#plt.plot_correlation_x_distance(dists, matrix, title='Correlation X Euclidean Distance',
#                                yax='Temporal Correlation',
#                                xax='Geographical Distance between pairs of points (km)')
#plt.plot_grouped_correlation_x_distance(dists, matrix, title='Correlation X Geographical Distance',
#                                        yax='Temporal correlation',
#                                        xax='Geographical distance between pairs of points [km]')
#plt.plot_correlation_x_distance(topol_dists, matrix, title='Correlation X Topological Distance')
#plt.plot_grouped_correlation_x_distance(topol_dists, matrix, title='Correlation X Topological Distance')
