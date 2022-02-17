import datetime
import sys
import data as rd
import graph
from calc import Stats
import output2 as out
import numpy as np
import configparser
import os

# Receive args
if len(sys.argv) == 3:
    coords_file = sys.argv[1]
    matrix_file = sys.argv[2]
    delay_matrix = None
elif len(sys.argv) == 4:
    coords_file = sys.argv[1]
    corrMatrix_file = sys.argv[2]
    delayMatrix_file = sys.argv[3]
else:
    print("Erro!")

# Import coordinates
x, y, labelList = [], [], []
f = open(coords_file, 'r')
lines = f.readlines()[1:]
for line in lines:
    cols = line.split(',')
    id = cols[0]
    est_name = cols[1]
    lat = cols[2]
    lon = cols[3]
    y.append(lat)
    x.append(lon)
    labelList.append(est_name)

# Read data
matrix = np.loadtxt(corrMatrix_file)
if delayMatrix_file is None:
    delay_matrix = np.zeros((matrix.shape))
else:
    delay_matrix = np.loadtxt(delayMatrix_file)

threshold = 0
g = graph.Graph.from_correlation_matrix(matrix, threshold, x, y, labelList)
#print(g)
#graph.Graph.set_pvalues(g, p_values)
if delayMatrix_file is not None:
    graph.Graph.set_timedelay(g, delay_matrix)
    tdelay = True
else:
    tdelay = False

# Network metrics
#graph.Graph.calculate_vertices_metrics(g)
#g.vs["shortestPathMean"] = graph.Graph.get_shortest_path_mean(g)
#topol_dists = np.array(g.shortest_paths())

out_dir = '/dados/cnmac/'
shp_filename = "grafo_rionegro_nivel_" + "{:3.2f}".format(threshold)
out.Shapefile(g).create_shape(out_dir, shp_filename, tdelay)
