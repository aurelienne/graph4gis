import sys
import data as rd
import graph
from calc import Stats
import output as out
import numpy as np
import configparser

# Receive args
config_file = sys.argv[1]
input_list = sys.argv[2]
threshold = float(sys.argv[3])
threshold_type = sys.argv[4]    # p - percentile / t - threshold value

# Read config file
config = configparser.ConfigParser()
config.read(config_file)
out_dir = config['PATH']['OUTPUT']
nx = int(config['GEO']['NX'])
ny = int(config['GEO']['NY'])
dx = float(config['GEO']['DX'])
dy = float(config['GEO']['DY'])
x1 = float(config['GEO']['X1'])
y1 = float(config['GEO']['Y1'])
x2 = x1 + nx*dx
y2 = y1 + ny*dy
dbz_min = float(config['PARAM']['DBZ_MIN'])
dt_pos_ini = config['PARAM']['dt_pos_ini']
dt_pos_fim = config['PARAM']['dt_pos_fim']
dt_format = config['PARAM']['dt_format']

df = rd.Data(x1, y1, x2, y2, dx, dy, nx, ny)
df.import_bin_from_list(input_list, dbz_min, dt_pos_ini, dt_pos_fim, dt_format)
matrix = df.get_pearson_correlation()
stats = Stats()
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
g.write_graphml('GT.GraphML')
topol_dists = np.array(g.shortest_paths())
avg_cluster = graph.Graph.get_average_clustering(g)
avg_degree = graph.Graph.get_average_degree(g)
diameter = g.diameter(directed=False)
shortpath_mean = graph.Graph.get_average_shortest_path_mean(g)
mdists_gt = graph.Graph.get_manhattan_shortest_paths(g)

# Backbone
g_backbone = graph.Graph.from_correlation_matrix(matrix, 0, df.xlist, df.ylist)
#g_backbone.write_graphml('Original.GraphML')
g_backbone = stats.test_backbone(g_backbone, len(g.es), matrix)
g_backbone = graph.Graph.calculate_vertices_metrics(g_backbone)
#g_backbone.write_graphml('BB.GraphML')
#clusters = g.clusters() # get connected components
bkb_avg_shortest_path = graph.Graph.get_average_shortest_path_mean(g_backbone)
bkb_avg_cluster_coef = g_backbone.transitivity_avglocal_undirected()
bkb_diameter = g_backbone.diameter(directed=False)
out.Shapefile(g_backbone, "backbone_"+str(threshold)).create_shape("", dx, dy)
print("\nbackbone:")
print(bkb_avg_shortest_path, bkb_avg_cluster_coef, bkb_diameter, min(g_backbone.es['weight']), max(g_backbone.es['weight']))
bkb_topol_dists = np.array(g_backbone.shortest_paths())
mdists_bb = graph.Graph.get_manhattan_shortest_paths(g_backbone)

# Random networks (rewired)
#avgshortpath_samples, avgcluster_samples, diameter_samples, avg_rand_graph_corr = stats.rewired_graph(g, 10, matrix, dists)
#print("Rede Aleatoria:")
#print(np.mean(avgshortpath_samples), np.mean(avgcluster_samples), np.mean(diameter_samples), min(avg_rand_graph_corr), max(avg_rand_graph_corr))

# Random network (Networkx Configuration Model) - GT
#avgcluster_samples, avgshortpath_samples, diameter_samples, avg_rand_graph_corr, min_rand_graph_corr, \
#max_rand_graph_corr = graph.Graph.randomize_graph(g.degree(), matrix, samples=30)
#print("Rede Aleatoria - Based on GT:")
#print(np.mean(avgshortpath_samples), np.mean(avgcluster_samples), np.mean(diameter_samples), np.min(avg_rand_graph_corr),
#      np.max(avg_rand_graph_corr))
#idxs = np.triu_indices(matrix.shape[0], k=1)
#corr_matrix = matrix[idxs]
#out.Plots.plot_correlation_histogram2(corr_matrix, avg_rand_graph_corr, 0.86, "GT-network", "steelblue")

# Random network (Networkx Configuration Model) - BB
#avgcluster_samples, avgshortpath_samples, diameter_samples, avg_rand_graph_corr, min_rand_graph_corr, \
#max_rand_graph_corr = graph.Graph.randomize_graph(g_backbone.degree(), matrix, samples=30)
#print("Rede Aleatoria - Based on GT:")
#print(np.mean(avgshortpath_samples), np.mean(avgcluster_samples), np.mean(diameter_samples), np.min(avg_rand_graph_corr),
#      np.max(avg_rand_graph_corr))

# Random network (Networkx Configuration Model) - MI
#avgcluster_samples, avgshortpath_samples, diameter_samples, avg_rand_graph_corr, min_rand_graph_corr, \
#max_rand_graph_corr = graph.Graph.randomize_graph(g.degree(), matrix, samples=30)
#print("Rede Aleatoria - Based on GT:")
#print(np.mean(avgshortpath_samples), np.mean(avgcluster_samples), np.mean(diameter_samples), np.min(avg_rand_graph_corr),
#      np.max(avg_rand_graph_corr))


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
#out.Plots.plot_correlation_histogram2(matrix, np.array(g_backbone.es['weight']), avg_rand_graph_corr, threshold=0.86)

#plt.plot_correlation_x_distance(dists, matrix, title='Correlation X Euclidean Distance',
#                                yax='Temporal Correlation',
#                                xax='Geographical Distance between pairs of points (km)')
#plt.plot_grouped_correlation_x_distance(dists, matrix, title='Correlation X Geographical Distance',
#                                        yax='Temporal correlation',
#                                        xax='Geographical distance between pairs of points [km]')
#plt.plot_correlation_x_distance(topol_dists, matrix, title='Correlation X Topological Distance')
#plt.plot_grouped_correlation_x_distance(topol_dists, matrix, title='Correlation X Topological Distance')
out.Plots.plot_distance_x_distance2(dists, dists, topol_dists, bkb_topol_dists)
#out.Plots.clustering_x_degree(g_backbone.vs['degree'], g_backbone.vs['clusterCoeficient'])
#out.Plots.plot_distance_x_distance2(mdists_gt, mdists_bb, topol_dists, bkb_topol_dists)
