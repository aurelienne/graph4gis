import sys
import data as rd
import graph
import output as out

# Recorte SP
#x1 = -46.826
#y1 = -23.3562
#x2 = -46.3648
#y2 = -24.0079
#dx = 0.00747135
#dy = -0.00675451

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

input_list = sys.argv[1]
threshold = float(sys.argv[2])

df = rd.Data(x1, y1, x2, y2, dx, dy, nx, ny)
df.import_bin_from_list(input_list)
matrix = df.get_pearson_correlation()

g = graph.Graph(matrix, threshold, df.xlist, df.ylist)
g.get_degree()
g.get_strength()
g.get_closeness()
g.get_betweenness()
g.get_clustering_coefficient()
g.get_shortest_path_mean()

avg_cluster = g.get_average_clustering()
avg_degree = g.get_average_degree()
diameter = g.get_diameter()
shortpath_mean = g.get_average_shortest_path_mean()

#g.plot("grafo.svg")

out.Shapefile(g.graph,"grafo_"+str(threshold)).create_shape("", -1)

global_file = out.TextFiles(g, "graph_TamanduateiClip_correlation_10032019.csv")
global_file.create_csv(threshold)