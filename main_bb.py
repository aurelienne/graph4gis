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
threshold_type = sys.argv[4]    # p - percentile / t - threshold value
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

df = rd.Data(x1, y1, x2, y2, dx, dy, nx, ny)
df.import_bin_from_list(input_list, dbz_min, dt_pos_ini, dt_pos_fim, dt_format)
matrix = df.get_pearson_correlation()
stats = Stats()

"""
data = np.genfromtxt('/dados/redes/2teste.txt', delimiter=',')
#data = np.genfromtxt('/dados/redes/testesMI.txt', delimiter=',')
d_bb0 = data[:, 0]
d_bb1 = data[:, 1]
d_bb2 = data[:, 2]
d_gt = data[:, 3]
print("BB0 X BB1:")
stats.test_greater_distribution(d_bb0[~np.isnan(d_bb0)], d_bb1[~np.isnan(d_bb1)])
print("BB0 X BB2:")
stats.test_greater_distribution(d_bb0[~np.isnan(d_bb0)], d_bb2[~np.isnan(d_bb2)])
print("BB0 X GT:")
stats.test_greater_distribution(d_bb0[~np.isnan(d_bb0)], d_gt[~np.isnan(d_gt)])
print("BB1 X BB2:")
stats.test_greater_distribution(d_bb1[~np.isnan(d_bb1)], d_bb2[~np.isnan(d_bb2)])
print("BB1 X GT:")
stats.test_greater_distribution(d_bb1[~np.isnan(d_bb1)], d_gt[~np.isnan(d_gt)])
print("BB2 X GT:")
stats.test_greater_distribution(d_bb2[~np.isnan(d_bb2)], d_gt[~np.isnan(d_gt)])
sys.exit()
"""

#stats.pearson_significance_test(df.time_series)
#stats.shuffle(df.time_series, matrix, 100)
#stats.ttest(len(df.time_series), 0.86, 0.05)

dists = df.get_euclidean_distances()
#df.get_neighbours()

# Global-Threshold Network
if threshold_type == 'p':
    percentile = threshold
    threshold = df.get_threshold_from_percentile(matrix, percentile)
g = graph.Graph.from_correlation_matrix(matrix, threshold, df.xlist, df.ylist)
graph.Graph.calculate_vertices_metrics(g)
g.vs["shortestPathMean"] = graph.Graph.get_shortest_path_mean(g)
topol_dists = np.array(g.shortest_paths())
avg_cluster = graph.Graph.get_average_clustering(g)
avg_degree = graph.Graph.get_average_degree(g)
diameter = g.diameter(directed=False)
shortpath_mean = graph.Graph.get_average_shortest_path_mean(g)
pcgt_ncomponents, pcgt_maxcomponent_v, pcgt_maxcomponent_e, pcgt_singletons = graph.Graph.get_components_stats(g)
print("pcGT - Components:")
print(pcgt_ncomponents, pcgt_maxcomponent_v, pcgt_maxcomponent_e, pcgt_singletons)
#mdists_gt = graph.Graph.get_manhattan_shortest_paths(g)
pcgt_heter = graph.Graph.heterogeneity2(g)
print("Heterogeneity:")
print(pcgt_heter)
pcgt_heter = graph.Graph.heterogeneity(g)
print("Heterogeneity:")
print(pcgt_heter)

# Backbone - Based on GT
g_backbone = graph.Graph.from_correlation_matrix(matrix, 0, df.xlist, df.ylist)
g_backbone = stats.test_backbone(g_backbone, len(g.es), matrix, 0.127, 0.128, 0.001)
g_backbone = graph.Graph.calculate_vertices_metrics(g_backbone)
#clusters = g.clusters() # get connected components
bkb_avg_shortest_path = graph.Graph.get_average_shortest_path_mean(g_backbone)
bkb_avg_cluster_coef = g_backbone.transitivity_avglocal_undirected()
bkb_diameter = g_backbone.diameter(directed=False)
out.Shapefile(g_backbone, "backbone_"+str(threshold)).create_shape(out_dir, dx, dy)
print("\nbackbone:")
print(bkb_avg_shortest_path, bkb_avg_cluster_coef, bkb_diameter, min(g_backbone.es['weight']), max(g_backbone.es['weight']))
bkb_topol_dists = np.array(g_backbone.shortest_paths())
print(len(g_backbone.clusters()))
pcbb_ncomponents, pcbb_maxcomponent_v, pcbb_maxcomponent_e, pcbb_singletons = graph.Graph.get_components_stats(g_backbone)
print("pcbb - Components:")
print(pcbb_ncomponents, pcbb_maxcomponent_v, pcbb_maxcomponent_e, pcbb_singletons)
pcbb_heter = graph.Graph.heterogeneity2(g_backbone)
print("Heterogeneity:")
print(pcbb_heter)
pcbb_heter = graph.Graph.heterogeneity(g_backbone)
print("Heterogeneity:")
print(pcbb_heter)
#mdists_bb = graph.Graph.get_manhattan_shortest_paths(g_backbone)

# Mutual Information (Iuri)
mi_matrix = np.zeros((587, 587))
with open('/dados/redes/Iuri/MI_complete_graph_edges.csv') as f:
    for line in f.readlines()[1:]:
        cols = line.split(',')
        source = int(cols[1])
        target = int(cols[2])
        weight = float(cols[3])
        mi_matrix[source, target] = weight

g_mi = graph.Graph.from_graphml('/dados/redes/Iuri/GraphML_MI/g_graph_max_diameter_MI.GraphML')
print("migt - Components:")
migt_ncomponents, migt_maxcomponent_v, migt_maxcomponent_e, migt_singletons = graph.Graph.get_components_stats(g_mi)
print(migt_ncomponents, migt_maxcomponent_v, migt_maxcomponent_e, migt_singletons)
migt_heter = graph.Graph.heterogeneity(g_mi)
print("Heterogeneity:")
print(migt_heter)
migt_topol_dists = np.array(g_mi.shortest_paths())
print("<k> = "+str(graph.Graph.get_average_degree(g_mi)))

# Backbone - based on MI
print("mibb:")
g_backbone_mi = graph.Graph.from_correlation_matrix(mi_matrix, 0, df.xlist, df.ylist)
g_backbone_mi = stats.test_backbone(g_backbone_mi, len(g_mi.es), mi_matrix, 0.1124, 0.1125, 0.0001)
mibb_avg_shortest_path = graph.Graph.get_average_shortest_path_mean(g_backbone_mi)
mibb_avg_cluster_coef = g_backbone_mi.transitivity_avglocal_undirected()
mibb_diameter = g_backbone_mi.diameter(directed=False)
print(mibb_avg_shortest_path, mibb_avg_cluster_coef, mibb_diameter)
print("mibb - Components:")
mibb_ncomponents, mibb_maxcomponent_v, mibb_maxcomponent_e, mibb_singletons = graph.Graph.get_components_stats(g_backbone_mi)
print(mibb_ncomponents, mibb_maxcomponent_v, mibb_maxcomponent_e, mibb_singletons)
mibb_heter = graph.Graph.heterogeneity2(g_backbone_mi)
print("Heterogeneity:")
print(mibb_heter)
mibb_heter = graph.Graph.heterogeneity(g_backbone_mi)
print("Heterogeneity:")
print(mibb_heter)
mibb_topol_dists = np.array(g_backbone_mi.shortest_paths())

# Random networks (rewired)
#avgshortpath_samples, avgcluster_samples, diameter_samples, avg_rand_graph_corr = stats.rewired_graph(g, 10, matrix, dists)
#print("Rede Aleatoria:")
#print(np.mean(avgshortpath_samples), np.mean(avgcluster_samples), np.mean(diameter_samples), min(avg_rand_graph_corr), max(avg_rand_graph_corr))

# Random network (Networkx Configuration Model) - GT
"""
avgcluster_samples, avgshortpath_samples, diameter_samples, avg_rand_graph_corr, min_rand_graph_corr, \
max_rand_graph_corr, avg_heter = graph.Graph.randomize_graph(g.degree(), matrix, len(g.es), samples=10000)
print("Rede Aleatoria - Based on GT:")
print(np.mean(avgshortpath_samples), np.mean(avgcluster_samples), np.mean(diameter_samples), min_rand_graph_corr,
      max_rand_graph_corr, avg_heter)
idxs = np.triu_indices(matrix.shape[0], k=1)
corr_matrix = matrix[idxs]
out.Plots.plot_correlation_histogram3(corr_matrix, np.array(g_backbone.es['weight']), avg_rand_graph_corr, 0.86,
                                      "pcGT-network", "#1e82ce", "pcBB-network", "#2d9d3a", "pcCM-networks (average)",
                                      "grey", "Pearson Correlation Coefficient")
"""

# Random network (Networkx Configuration Model) - MI
"""
avgcluster_samples, avgshortpath_samples, diameter_samples, avg_rand_graph_corr, min_rand_graph_corr, \
max_rand_graph_corr, avg_heter = graph.Graph.randomize_graph(g_mi.degree(), mi_matrix, len(g_mi.es), samples=10000)
print("Rede Aleatoria - Based on MI:")
print(np.mean(avgshortpath_samples), np.mean(avgcluster_samples), np.mean(diameter_samples), min_rand_graph_corr,
      max_rand_graph_corr, avg_heter)
out.Plots.plot_correlation_histogram3(mi_matrix[idxs], np.array(g_backbone_mi.es['weight']),
                                      avg_rand_graph_corr, 0.6, "miGT-network", "#1cb8ec", "miBB-network", "#40ef55",
                                      "miCM-networks (average)", "lightgrey", "Mutual Information Index")
"""

#plt = out.Plots(g)
#plt.boxplot_random_samples(avgshortpath_samples, graph.Graph.get_average_shortest_path_mean(g), bkb_avg_shortest_path, 'Average Shortest Path')
#plt.boxplot_random_samples(avgcluster_samples, graph.Graph.get_average_clustering(g), bkb_avg_cluster_coef, 'Average Clustering Coefficient')
#plt.boxplot_random_samples(diameter_samples, g.diameter(directed=False), bkb_diameter, 'Diameter')

#sys.exit()
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

print("Backbone Regression T-test:")
y2 = bkb_topol_dists[idxs].flatten()
idx = np.isfinite(y2)
x2 = x[idx]
y2 = y2[idx]
reject, pvalues, b, slope = stats.ttest_regression(x2, y2)
print("reject = "+str(reject)+" p-value = "+str(pvalues))
np.savetxt("euclid_dists_gt.csv", x1, delimiter=",")
np.savetxt("euclid_dists_bb.csv", x2, delimiter=",")
np.savetxt("gt_topol_dists.csv", y1, delimiter=",")
np.savetxt("bb_topol_dists.csv", y2, delimiter=",")
"""

#g.plot("grafo.svg")

#out.Shapefile(g, "grafo_"+str(threshold)).create_shape("", dx, dy)
#out_csv = out.TextFiles(g)
#out_csv.create_global_metrics_csv(threshold, "correlation_x_global_metrics.csv", avg_degree, avg_cluster, diameter, shortpath_mean)
#out_csv.create_vertex_metrics_csv("vertex_metrics.csv")
#out_csv.create_adjacency_list("adjacency_list.csv")

#out.Plots.plot_degree_histogram(g)
#out.Plots.plot_degree_histogram2(g, g_backbone)
#out.Plots.plot_degree_distribution(g, g_backbone)
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
out.Plots.plot_distance_x_distance2(dists, dists, topol_dists, bkb_topol_dists, "pcGT-Network", "pcBB-Network",
                                    "Geographical Distance [km]",
                                    "Topological Distance [number of edges]")
#out.Plots.clustering_x_degree(g_backbone.vs['degree'], g_backbone.vs['clusterCoeficient'])

#out.Plots.plot_distance_x_distance2(dists, dists, migt_topol_dists, mibb_topol_dists, "miGT-Network", "miBB-Network",
#                                    "Geographical Distance [km]",
#                                    "Topological Distance [number of edges]")
