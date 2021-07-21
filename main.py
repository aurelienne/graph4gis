import datetime
import sys
import data as rd
import graph
from calc import Stats
import output as out
import numpy as np
import configparser
import os

# Receive args
config_file = sys.argv[1]
input_list = sys.argv[2]
threshold = float(sys.argv[3])
threshold_type = sys.argv[4]    # p - percentile / t - threshold value / md - max diameter threshold
id_network = sys.argv[5]

# Read config file
config = configparser.ConfigParser()
config.read(config_file)
out_dir = config['PATH']['OUTPUT']
out_dir = os.path.join(out_dir, id_network)
nx = int(config['GEO']['NX'])
ny = int(config['GEO']['NY'])
dx = float(config['GEO']['DX'])
dy = float(config['GEO']['DY'])
x1 = float(config['GEO']['X1'])
y1 = float(config['GEO']['Y1'])
x2 = x1 + nx*dx
y2 = y1 + ny*dy
dbz_min = float(config['PARAM']['DBZ_MIN'])
dt_pos_ini = int(config['PARAM']['dt_pos_ini'])
dt_pos_fim = int(config['PARAM']['dt_pos_fim'])
dt_format = config['PARAM']['dt_format']

# Read data
df = rd.Data(x1, y1, x2, y2, dx, dy, nx, ny)
df.import_bin_from_list(input_list, dbz_min, dt_pos_ini, dt_pos_fim, dt_format)

# Data Correlation
#matrix = df.get_pearson_correlation()
matrix, p_values, delay = df.get_pearson_correlation_timedelay(datetime.timedelta(minutes=10))

# Stats
#stats = Stats()
#p_values = stats.pearson_significance_test(df.time_series)
#stats.shuffle(df.time_series, matrix, 100)
#stats.ttest(len(df.time_series), 0.86, 0.05)

#dists = df.get_euclidean_distances()
#df.get_neighbours()

# Graph construction
if threshold_type == 'p':
    percentile = threshold
    threshold = df.get_threshold_from_percentile(matrix, percentile)
elif threshold_type == 'md':
    g = graph.Graph.from_correlation_matrix(matrix, 0, df.xlist, df.ylist)
    threshold = graph.Graph.max_diameter_threshold(g)
    print(threshold)

g = graph.Graph.from_correlation_matrix(matrix, threshold, df.xlist, df.ylist)
g = graph.Graph.set_pvalues(g, p_values)
g = graph.Graph.set_timedelay(g, delay)
print(g.es["t_delay"])
#g.write_graphml('GT.GraphML')

# Network metrics
graph.Graph.calculate_vertices_metrics(g)
g.vs["shortestPathMean"] = graph.Graph.get_shortest_path_mean(g)
topol_dists = np.array(g.shortest_paths())
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

shp_filename = "grafo_" + "{:3.2f}".format(threshold)
out.Shapefile(g, shp_filename).create_shape(out_dir, dx, dy)
#out_csv = out.TextFiles(g)
#out_csv.create_global_metrics_csv(threshold, os.path.join(out_dir, "correlation_x_global_metrics.csv"))
#out_csv.create_vertex_metrics_csv(os.path.join(out_dir, "vertex_metrics.csv"))
#out_csv.create_adjacency_list(os.path.join(out_dir, "adjacency_list.csv"))

#plt = out.Plots(g)
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
