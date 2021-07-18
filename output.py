import graph
from osgeo import ogr
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import scipy
import calc
import sys

class Shapefile:

    """Classe baseada no código de Wilson Ceron"""
    def __init__( self, g, filename):
        self.g		= g
        self.filename	= filename

    def	create_lines(self, path, dx, dy, center=True):
        if center == False or dx == None or dy == None:
            dx = 0
            dy = 0
        csvFile= path+"/"+self.filename+"_lines.csv"
        f = open(csvFile,'w')
        f.write("Label,Lines,weight\n")

        for edge in self.g.get_edgelist():
            f.write('%s_%s,"'	%	(	self.g.vs[edge[0]]["label"], self.g.vs[edge[1]]["label"]	)	)
            f.write("LINESTRING ("																		)
            f.write("%s %s,"	%	(	self.g.vs[edge[0]]["x"]+ dx/2.,self.g.vs[edge[0]]["y"]+ dy/2.				)	)
            f.write('%s %s)",'	%	(	self.g.vs[edge[1]]["x"]+ dx/2.,self.g.vs[edge[1]]["y"]+ dy/2.				)	)
            f.write("%f\n" 		%	(	self.g.es.find(_between=((edge[0],), (edge[1],)))['weight']	)	)
        f.close()

        vrt= path+"/"+self.filename+"_lines.vrt"

        f = open(vrt,'w')
        f.write('<OGRVRTDataSource><OGRVRTLayer name="lines">'+'\n')
        f.write("<SrcDataSource>" + csvFile + "</SrcDataSource>" + "\n"+ "<SrcLayer>"+self.filename+"_lines</SrcLayer>" +"\n")
        f.write('<GeometryField encoding="WKT" field="Lines"/>'+"\n")
        f.write('<Field name="Label" src="Label" type="string" width="45" />'+"\n")
        f.write('<Field name="weight" src="weight" type="Real" 			  />'+"\n")
        f.write("</OGRVRTLayer>\n</OGRVRTDataSource>"+"\n")
        f.close()

        in_ds = ogr.Open(vrt)
        lyr = in_ds.GetLayer('lines')
        for feat in lyr:
            geom = feat.GetGeometryRef()

        ogr.GetDriverByName("ESRI Shapefile").CopyDataSource(in_ds, path+"/"+self.filename+"_lines.shp")

    def	create_points(self, path, dx, dy, center=True):
        if center == False or dx == None or dy == None:
            dx = 0
            dy = 0
        csvFile= path+"/"+self.filename+"_points.csv"
        f = open(csvFile,'w')

        if 'group' in self.g.vs.attributes():
            f.write("id,x,y,degree,wDegree,pagerank,closeness,betweennes,cc,eigenvecto,sPathMean,group\n")
            for v in self.g.vs:
                f.write(	str(v["label"])			+	","	+	str(v["x"] + dx/2.)					+	","		+	str(v["y"] + dy/2.)					+	","	)
                f.write(	str(v["degree"])		+	","	+	str(v["weightedDegree"])	+	","		+	str(v["pagerank"])			+	","	)
                f.write(	str(v["closeness"])		+	","	+	str(v["betweenness"])		+	","		+	str(v["clusterCoeficient"])	+	","	)
                f.write(	str(v["eigenvectorCentrality"])+ ","+str(v["shortestPathMean"])	+	"," 	+	str(v["group"])				+	"\n")
            f.close()

            vrt= path+"/"+self.filename+"_points.vrt"

            f = open(vrt,'w')
            f.write('<OGRVRTDataSource><OGRVRTLayer name="points">'+'\n')
            f.write("<SrcDataSource>" + csvFile + "</SrcDataSource>" + "\n"+ "<SrcLayer>"+self.filename+"_points</SrcLayer>" +"\n")
            f.write("<GeometryType>wkbPoint</GeometryType>"+"\n"+"<GeometryField encoding=\'PointFromColumns\' x=\'X\' y=\'Y\'/>")
            f.write('<Field name="id" src="id" type="integer" 						/>'+"\n")
            f.write('<Field name="degree" 		src="degree" 		type="integer"	/>'+"\n")
            f.write('<Field name="wDegree" 		src="wDegree" 		type="real"		/>'+"\n")
            f.write('<Field name="closeness" 	src="closeness" 	type="real"		/>'+"\n")
            f.write('<Field name="betweennes" 	src="betweennes"	type="real"		/>'+"\n")
            f.write('<Field name="cc" 			src="cc"			type="real"		/>'+"\n")
            f.write('<Field name="sPathMean" 	src="sPathMean" 	type="real" 	/>'+"\n")
            f.write('<Field name="group" src="group" 				type="integer"	/>'+"\n")
            f.write("</OGRVRTLayer>\n</OGRVRTDataSource>"+"\n")
            f.close()

        else:
            f.write("id,x,y,degree,wDegree,closeness,betweennes,cc,sPathMean,strength\n")
            for v in self.g.vs:
                f.write(	str(v["label"])			+	","	+	str(v["x"] + dx/2.)					+	","		+	str(v["y"] + dy/2.)					+	","	)
                f.write(	str(v["degree"])		+	","	+	str(v["weightedDegree"])	+	","	)
                f.write(	str(v["closeness"])		+	","	+	str(v["betweenness"])		+	","		+	str(v["clusterCoeficient"])	+	","	)
                #f.write(	str(v["shortestPathMean"]) +","	+	str(v["strength"]) +	"\n")
                f.write(str(v["shortestPathMean"]) + "\n")
            f.close()

            vrt= path+"/"+self.filename+"_points.vrt"

            f = open(vrt,'w')
            f.write('<OGRVRTDataSource><OGRVRTLayer name="points">'+'\n')
            f.write("<SrcDataSource>" + csvFile + "</SrcDataSource>" + "\n"+ "<SrcLayer>"+self.filename+"_points</SrcLayer>" +"\n")
            f.write("<GeometryType>wkbPoint</GeometryType>"+"\n"+"<GeometryField encoding=\'PointFromColumns\' x=\'X\' y=\'Y\'/>")
            f.write('<Field name="id" src="id" type="integer" 						/>'+"\n")
            f.write('<Field name="degree" 		src="degree" 		type="integer"	/>'+"\n")
            f.write('<Field name="wDegree" 		src="wDegree" 		type="real"		/>'+"\n")
            f.write('<Field name="closeness" 	src="closeness" 	type="real"		/>'+"\n")
            f.write('<Field name="betweennes" 	src="betweennes"	type="real"		/>'+"\n")
            f.write('<Field name="cc" 			src="cc"			type="real"		/>'+"\n")
            f.write('<Field name="sPathMean" 	src="sPathMean" 	type="real" 	/>'+"\n")
            f.write('<Field name="strength" 	src="strength" 	    type="real" 	/>' + "\n")
            f.write("</OGRVRTLayer>\n</OGRVRTDataSource>"+"\n")
            f.close()

        in_ds = ogr.Open(vrt)
        lyr = in_ds.GetLayer('points')
        for feat in lyr:
            geom = feat.GetGeometryRef()

        ogr.GetDriverByName("ESRI Shapefile").CopyDataSource(in_ds, path+"/"+self.filename+"_points.shp")

    def	create_polygons(self, path, dx, dy):
        csvFile= path+"/"+self.filename+"_polygons.csv"
        f = open(csvFile,'w')

        if 'group' in self.g.vs.attributes():
            f.write("id,polygons,degree,wDegree,pagerank,closeness,betweennes,cc,eigenvecto,sPathMean,group\n")
            for v in self.g.vs:
                f.write(	str(v["label"])	+																								',"')
                f.write(	"POLYGON ((")
                f.write(	"%s %s,"	%	(	str(	v["x"]					) 	, 	str(	v["y"]					)	)	)
                f.write(	"%s %s,"	%	(	str(	v["x"]	+	dx	)	,	str(	v["y"]					)	)	)
                f.write(	"%s %s,"	%	(	str(	v["x"]	+	dx	)	,	str(	v["y"]	+	dy	)	)	)
                f.write(	"%s %s,"	%	(	str(	v["x"]					)	,	str(	v["y"]	+	dy	)	)	)
                f.write(	'%s %s))",'	%	(	str(	v["x"]					) 	, 	str(	v["y"]					)	)	)
                f.write(	str(v["degree"])		+	","	+	str(v["weightedDegree"])	+	","		+	str(v["pagerank"])			+	","	)
                f.write(	str(v["closeness"])		+	","	+	str(v["betweenness"])		+	","		+	str(v["clusterCoeficient"])	+	","	)
                f.write(	str(v["eigenvectorCentrality"])+ ","+str(v["shortestPathMean"])	+	"," 	+	str(v["group"])				+	"\n")
            f.close()

            vrt= path+"/"+self.filename+"_polygons.vrt"

            f = open(vrt,'w')
            f.write('<OGRVRTDataSource><OGRVRTLayer name="polygons">'+'\n')
            f.write("<SrcDataSource>" + csvFile + "</SrcDataSource>" + "\n"+ "<SrcLayer>"+self.filename+"_polygons</SrcLayer>" +"\n")
            f.write("<GeometryType>wkbPolygon</GeometryType>"+"\n")
            f.write('<Field name="id" src="id" type="integer" 						/>'+"\n")
            f.write('<GeometryField encoding="WKT" field="polygons"					/>'+"\n")
            f.write('<Field name="degree" 		src="degree" 		type="integer"	/>'+"\n")
            f.write('<Field name="wDegree" 		src="wDegree" 		type="real"		/>'+"\n")
            f.write('<Field name="pagerank" 	src="pagerank" 		type="real"		/>'+"\n")
            f.write('<Field name="closeness" 	src="closeness" 	type="real"		/>'+"\n")
            f.write('<Field name="betweennes" 	src="betweennes"	type="real"		/>'+"\n")
            f.write('<Field name="cc" 			src="cc"			type="real"		/>'+"\n")
            f.write('<Field name="eigenvecto" 	src="eigenvecto" 	type="real" 	/>'+"\n")
            f.write('<Field name="sPathMean" 	src="sPathMean" 	type="real" 	/>'+"\n")
            f.write('<Field name="group" src="group" 				type="integer"	/>'+"\n")
            f.write("</OGRVRTLayer>\n</OGRVRTDataSource>"+"\n")
            f.close()

        else:
            f.write("id,polygons,degree,wDegree,closeness,betweennes,cc,sPathMean\n")
            for v in self.g.vs:
                f.write(	str(v["label"])	+																								',"')
                f.write(	"POLYGON ((")
                f.write(	"%s %s,"	%	(	str(	v["x"]					) 	, 	str(	v["y"]					)	)	)
                f.write(	"%s %s,"	%	(	str(	v["x"]	+	dx	)	,	str(	v["y"]					)	)	)
                f.write(	"%s %s,"	%	(	str(	v["x"]	+	dx	)	,	str(	v["y"]	+	dy	)	)	)
                f.write(	"%s %s,"	%	(	str(	v["x"]					)	,	str(	v["y"]	+	dy	)	)	)
                f.write(	'%s %s))",'	%	(	str(	v["x"]					) 	, 	str(	v["y"]					)	)	)
                f.write(	str(v["degree"])		+	","	+	str(v["weightedDegree"])	+	",")
                f.write(	str(v["closeness"])		+	","	+	str(v["betweenness"])		+	","		+	str(v["clusterCoeficient"])	+	","	)
                f.write(	str(v["shortestPathMean"]) +"\n")
            f.close()

            vrt= path+"/"+self.filename+"_polygon.vrt"

            f = open(vrt,'w')
            f.write('<OGRVRTDataSource><OGRVRTLayer name="polygons">'+'\n')
            f.write("<SrcDataSource>" + csvFile + "</SrcDataSource>" + "\n"+ "<SrcLayer>"+self.filename+"_polygons</SrcLayer>" +"\n")
            f.write("<GeometryType>wkbPolygon</GeometryType>"+"\n")
            f.write('<Field name="id" src="id" type="integer" 						/>'+"\n")
            f.write('<GeometryField encoding="WKT" field="polygons"					/>'+"\n")
            f.write('<Field name="degree" 		src="degree" 		type="integer"	/>'+"\n")
            f.write('<Field name="wDegree" 		src="wDegree" 		type="real"		/>'+"\n")
            f.write('<Field name="closeness" 	src="closeness" 	type="real"		/>'+"\n")
            f.write('<Field name="betweennes" 	src="betweennes"	type="real"		/>'+"\n")
            f.write('<Field name="cc" 			src="cc"			type="real"		/>'+"\n")
            f.write('<Field name="sPathMean" 	src="sPathMean" 	type="real" 	/>'+"\n")
            f.write("</OGRVRTLayer>\n</OGRVRTDataSource>"+"\n")
            f.close()

        in_ds = ogr.Open(vrt)
        lyr = in_ds.GetLayer('polygons')
        for feat in lyr:
            geom = feat.GetGeometryRef()
            #print (geom.ExportToWkt())

        ogr.GetDriverByName("ESRI Shapefile").CopyDataSource(in_ds, path+"/"+self.filename+"_polygons.shp")

    def	create_shape(self, path, dx=None, dy=None):
        self.create_lines(path, dx, dy, center=True)
        self.create_points(path, dx, dy, center=True)
        if dx != None and dy != None:
            self.create_polygons(path, dx, dy)

class TextFiles:

    def __init__(self, g):
        self.g = g

    def create_global_metrics_csv(self, threshold, filename):
        num_vertices = self.g.vcount()
        num_edges = self.g.ecount()
        avg_cluster = graph.Graph.get_average_clustering(self.g)
        avg_degree = graph.Graph.get_average_degree(self.g)
        diameter = self.g.diameter(directed=False)
        shortpath_mean = graph.Graph.get_average_shortest_path_mean(self.g)
        avg_betweeness = graph.Graph.get_average_betweenness(self.g)
        num_components, giant_component_v, giant_component_e, singletons = graph.Graph.get_components_stats(self.g)

        f = open(filename, "a")
        f.write("threshold, vertices, edges, cluster_coef, avg_degree, diameter, shortpath_mean, avg_betweeness, "
                "num_components, giant_component_v, giant_component_e, singletons\n")
        f.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" % (threshold, num_vertices, num_edges, avg_cluster,
                                                                      avg_degree, diameter, shortpath_mean,
                                                                      avg_betweeness, num_components, giant_component_v,
                                                                      giant_component_e, singletons))
        f.close()

    def create_vertex_metrics_csv(self, filename):
        f = open(filename, "w")
        f.write("label, lon, lat, degree, closeness, betweenness, shortest_path_mean, clustering_coefficient\n")
        for v in self.g.vs:
            f.write("%s, %s, %s, %s, %s, %s, %s, %s\n" % (v["label"], v["x"], v["y"], v["degree"], v["closeness"], v["betweenness"], v["shortestPathMean"], v["clusterCoeficient"]))
        f.close()

    def create_adjacency_list(self, filename):
        f = open(filename, "w")
        for edge in self.g.get_edgelist():
            f.write("%s, %s\n" % (str(edge[0]), str(edge[1])))
        f.close()


class Plots:

    def __init__(self, g):
        self.g = g

    def plot_degree_histogram(g):
        degree_values = g.vs["degree"]
        binwidth = 2
        plt.hist(degree_values, alpha=0.7, rwidth=2, histtype='bar',
                 bins=np.arange(min(degree_values), max(degree_values) + binwidth, binwidth))
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel('Degree Values')
        plt.ylabel('Frequency')
        plt.title('Degree Histogram')
        plt.show()

    def plot_degree_histogram2(g, g2=None):
        binwidth = 2

        if g2 != None:
            degree_values2 = g2.vs["degree"]
            plt.hist(degree_values2, alpha=0.4, rwidth=2, histtype='bar',
                     bins=np.arange(min(degree_values2), max(degree_values2) + binwidth, binwidth), color='green',
                     label="BB-network")

        degree_values = g.vs["degree"]
        plt.hist(degree_values, alpha=0.4, rwidth=2, histtype='bar',
                 bins=np.arange(min(degree_values), max(degree_values) + binwidth, binwidth),
                 label="GT-network")


        plt.grid(axis='y', alpha=0.75)
        plt.xlabel('Degree Values')
        plt.ylabel('Frequency')
        plt.title('Degree Histogram')
        plt.legend()
        plt.show()

    def plot_degree_distribution(g, g2=None):
        if g2 != None:
            degree_values2 = g2.vs["degree"]
            p_k = np.bincount(degree_values2)
            k = np.array(range(np.amax(degree_values2)+1))
            plt.plot(k, p_k, alpha=0.4,
                     #bins=np.arange(min(degree_values2), max(degree_values2) + binwidth, binwidth),
                     color='green', label="BB-network")

        degree_values = g.vs["degree"]
        p_k = np.bincount(degree_values)
        k = np.array(range(np.amax(degree_values) + 1))
        plt.plot(k, p_k, alpha=0.4,
                 #bins=np.arange(min(degree_values), max(degree_values) + binwidth, binwidth),
                 label="GT-network")

        plt.grid(axis='y', alpha=0.75)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('Log of Degree(k)')
        plt.ylabel('Log of Frequency')
        plt.title('Degree Distribution')
        plt.legend()
        plt.show()

    def plot_shortpath_histogram(self):
        degree_values = self.g.vs["shortestPathMean"]
        plt.hist(degree_values, bins=len(degree_values), alpha=0.7, rwidth=2, histtype='bar')
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel('Average Shortest Path')
        plt.ylabel('Frequency')
        plt.title('Average Shortest Path Histogram')
        plt.show()

    def plot_correlation_histogram(self, corr_matrix, threshold):
        idxs = np.triu_indices(corr_matrix.shape[0], k=1)
        percentile = scipy.stats.percentileofscore(corr_matrix[idxs], threshold)
        plt.hist(corr_matrix[idxs], bins='auto', alpha=0.7, rwidth=0.85)
        plt.grid(axis='y', alpha=0.75)
        plt.axvline(threshold, label='Relevant Threshold = '+str(threshold)+'\n('+str(np.around(percentile,2))+' Percentile)')
        plt.xlabel('Correlation')
        plt.ylabel('Frequency')
        plt.title('Correlation Histogram')
        plt.legend()
        plt.show()

    def plot_correlation_histogram2(corr, rand_corr, threshold, label1, color1):
        binwidth = 0.01
        bins_h1 = np.arange(0, 1+binwidth, binwidth)
        netwk_corr = corr[corr >= threshold]
        print(netwk_corr[netwk_corr>=0.99])
        percentile = scipy.stats.percentileofscore(corr, threshold)
        h1 = plt.hist(netwk_corr, alpha=0.5, rwidth=1, color=color1, label=label1,
                 weights=np.zeros_like(netwk_corr) + 1. / netwk_corr.size,
                 bins=bins_h1)
                 #bins=np.arange(min(netwk_corr), max(netwk_corr) + binwidth, binwidth))

        bins_h2 = rand_corr[0]
        h2_relfreq = rand_corr[1]
        h2 = plt.bar(bins_h2, h2_relfreq, width=rand_corr[0][1]-rand_corr[0][0], alpha=0.5, color='grey',
                     label="RC-networks (average)", align='edge')
                     #weights=np.zeros_like(rand_corr) + 1. / rand_corr[1].size,
                     #bins=rand_corr[0])
        plt.grid(axis='y', alpha=0.75)
        #plt.axvline(threshold, label='Global Threshold = '+str(threshold)+'\n('+str(np.around(percentile, 2))
        #                             + ' Percentile)', color="red")
        plt.xlabel('Correlation')
        plt.ylabel('Relative Frequency')
        plt.legend(fontsize='medium')
        plt.show()

    def plot_correlation_histogram3(corr_matrix, bkb_corr, rand_corr, threshold, label1, color1, label2, color2, label3,
                                    color3, xlabel):
        percentile = scipy.stats.percentileofscore(corr_matrix, threshold)
        netwk_corr = corr_matrix[corr_matrix >= threshold]
        binwidth = 0.01
        bins_h3 = rand_corr[0]
        h3_relfreq = rand_corr[1]
        h1 = plt.hist(netwk_corr, alpha=0.5, rwidth=1, color=color1, label=label1,
                      weights=np.zeros_like(netwk_corr) + 1. / netwk_corr.size,
                      bins=np.arange(min(netwk_corr), max(netwk_corr) + binwidth, binwidth))
        h2 = plt.hist(bkb_corr, alpha=0.5, rwidth=1, color=color2, label=label2,
                      weights=np.zeros_like(bkb_corr) + 1. / bkb_corr.size,
                      bins=np.arange(min(bkb_corr), max(bkb_corr) + binwidth, binwidth))
        #h3 = plt.hist(rand_corr, alpha=0.5, rwidth=0.85, color='grey', label="RC-networks (average)",
        #         weights=np.zeros_like(rand_corr) + 1. / rand_corr.size,
        #         bins=np.arange(min(rand_corr), max(rand_corr) + binwidth, binwidth))
        h3 = plt.bar(bins_h3, h3_relfreq, width=rand_corr[0][1] - rand_corr[0][0], alpha=0.5, color=color3,
                     label=label3, align='edge')
        plt.grid(axis='y', alpha=0.75)
        plt.axvline(threshold, label='Global Threshold = '+str(threshold)+'\n('+str(np.around(percentile, 2))
                                     + ' Percentile)', color="red")
        plt.xlabel(xlabel)
        plt.ylabel('Relative Frequency')
        #plt.title('Correlation Histogram')
        plt.legend(fontsize='medium')
        plt.show()

    def plot_correlation_x_distance(self, dists, corrs, title, yax='', xax=''):
        plt.plot(np.triu(dists), np.triu(corrs), ',r')
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel()
        plt.ylabel()
        plt.title(title)
        plt.show()

    def plot_grouped_correlation_x_distance(self, dists, corrs, title, yax='', xax=''):
        idxs = np.triu_indices(dists.shape[0], k=1)
        dists = dists[idxs] #.reshape(-1)
        corrs = corrs[idxs] #.reshape(-1)
        df = pd.DataFrame({'Distance': dists, 'Correlation': corrs})
        data = df.groupby(df.Distance).Correlation.agg(freq='count', Min='min', Max='max', Mean='mean')
        dist = np.asarray(data.index)
        min = data.Min.values
        max = data.Max.values
        mean = data.Mean.values

        plt.plot(dist, min, '.r')
        plt.plot(dist, mean, '.g')
        plt.plot(dist, max, '.b')
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel(xax)
        plt.ylabel(yax)
        #lt.title(title)
        plt.show()

    def plot_distance_x_distance(euclid_dist, topol_dist):
        idxs = np.triu_indices(euclid_dist.shape[0], k=1)
        x = euclid_dist[idxs].flatten()
        y1 = topol_dist[idxs].flatten()
        idx = np.isfinite(y1)
        x1 = x[idx]
        y1 = y1[idx]
        plt.scatter(x1, y1, s=20, edgecolor=None, alpha=0.5, color='steelblue', label='GT-Network')
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel('Manhattan Distance [km]')
        plt.ylabel('Topological Distance [number of edges]')
        #plt.title('Geographical Distance X Topological Distance')
        m, b = np.polyfit(x1, y1, 1)
        r = np.corrcoef(x1, y1)[0, 1]
        r2 = '{:6.3f}'.format(r * r)
        plt.plot(x, m * x + b, color='darkblue')
        plt.text(20, 12, "R²="+r2)
        plt.text(20, 10, "slope=" + '{:6.2f}'.format(m))
        plt.legend()
        plt.show()

    def plot_distance_x_distance2(geo_dist1, geo_dist2, topol_dist, bkb_topol_dist, label1, label2, xlabel, ylabel):
        idxs = np.triu_indices(geo_dist1.shape[0], k=1)
        x1 = geo_dist1[idxs].flatten()
        x2 = geo_dist2[idxs].flatten()
        y1 = topol_dist[idxs].flatten()
        y2 = bkb_topol_dist[idxs].flatten()
        #y2 = bkb_topol_dist.flatten()
        idx = np.argwhere((y1>0) & (np.isfinite(y1)))
        x1 = x1[idx].flatten()
        y1 = y1[idx].flatten()
        idx = np.argwhere((y2>0) & (np.isfinite(y2)))
        x2 = x2[idx].flatten()
        y2 = y2[idx].flatten()
        #x2 = x[0:len(y2)]
        """
        #idx_dist1 = np.where(y1==1)
        #idx_dist2 = np.where(y2==1)
        #geo1 = x1[idx_dist1]
        #geo2 = x2[idx_dist2]
        #print(np.mean(geo1), np.max(geo1))
        #print(np.mean(geo2), np.max(geo2))
        """
        plt.scatter(x1, y1, s=20, edgecolor=None, alpha=0.5, color='steelblue', marker='.', label=label1)
        plt.scatter(x2, y2, s=20, edgecolor=None, alpha=0.5, color='limegreen', marker='s', label=label2)
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        #plt.title('Geographical Distance X Topological Distance')
        m, b = np.polyfit(x1, y1, 1)
        m2, b2 = np.polyfit(x2, y2, 1)
        r = np.corrcoef(x1, y1)[0, 1]
        rb = np.corrcoef(x2, y2)[0, 1]
        r2 = '{:6.3f}'.format(r * r)
        rb2 = '{:6.3f}'.format(rb * rb)

        p_value_gt = calc.Stats().ttest_regression(x1, y1)
        p_value_bb = calc.Stats().ttest_regression(x2, y2)
        print("p-value - GT: " + str(p_value_gt))
        print("p-value - BB: " + str(p_value_bb))
        print("")
        print("R2:")
        print(r2, rb2)

        plt.plot(x1, m * x1 + b, color='darkblue')
        plt.plot(x2, m2 * x2 + b2, color='darkgreen')
        #plt.text(20, 12, "R²="+r2)
        #plt.text(20, 10, "slope=" + '{:6.2f}'.format(m))
        print("slope:")
        print(m, m2)
        plt.legend()
        plt.show()

    def boxplot_random_samples(self, samples, original_value, backbone_value, title):
        plt.boxplot(samples, patch_artist=True,
                    sym="grey",
                    medianprops=dict(color="black"),
                    capprops=dict(color="grey"),
                    whiskerprops=dict(color="grey"),
                    boxprops=dict(facecolor="grey", color="grey"),
                    labels=["Random Samples", ])
        plt.axhline(original_value, label='Original network', color='blue')
        plt.axhline(backbone_value, label='Backbone network', color='green')
        plt.ylabel(title)
        plt.legend()
        plt.show()

    def correlation_x_zeros(self, time_series, corr_matrix):
        values = time_series.values
        val_array = np.array(values.tolist()).transpose()

        idxs = np.argwhere(corr_matrix>0.5)
        labels = []
        nzeros_list = []
        for corr_threshold in np.arange(0.75, 1, 0.025):
           min_corr = corr_threshold
           max_corr = corr_threshold + 0.0225
           #labels.append(str(min_corr)+' - '+str(max_corr))
           labels.append(str(min_corr))
           idxs = np.argwhere((corr_matrix>min_corr) & (corr_matrix<=max_corr))
           nzeros_sample = []
           for idx in idxs:
               i = idx[0]
               j = idx[1]
               ts1 = val_array[i]
               nzeros = np.count_nonzero(ts1==0)
               nzeros_perc = nzeros/56*100
               nzeros_sample.append(nzeros_perc)
               ts2 = val_array[j]
               nzeros = np.count_nonzero(ts2==0)
               nzeros_perc = nzeros/56*100
               nzeros_sample.append(nzeros_perc)
           nzeros_list.append(nzeros_sample)
        plt.boxplot(nzeros_list)
        plt.xticks(range(len(labels)), labels)
        plt.xlabel('Correlation range')
        plt.ylabel('Percentage of zeros in Time series')
        plt.savefig('/home/aurelienne.jorge/dados/figs/10032019/boxplot_zeros.png')
        plt.close()
        """
        corr_list = []
        nzeros_list = []
        idxs = np.argwhere(corr_matrix>0.5)
        for idx in idxs:
            i = idx[0]
            j = idx[1]
            corr_value = corr_matrix[i, j]
            corr_list.append(corr_value)
            ts1 = val_array[i]
            nzeros = np.count_nonzero(ts1==0)
            nzeros_perc = nzeros/56*100
            nzeros_list.append(nzeros_perc)
            ts2 = val_array[j]
            nzeros = np.count_nonzero(ts2==0)
            nzeros_perc = nzeros/56*100
            corr_list.append(corr_value)
            nzeros_list.append(nzeros_perc)
        plt.scatter(nzeros_list, corr_list, s=10, edgecolor=None, alpha=0.5, color='steelblue')
        plt.xlabel('Number of Zeros in Time series')
        plt.ylabel('Correlation')
        plt.savefig('/home/aurelienne.jorge/dados/figs/10032019/corr_x_zeros.png')
        plt.close()
        """
        nzeros_list = []
        idxs = np.argwhere(corr_matrix>0.95)
        for idx in idxs:
            i = idx[0]
            j = idx[1]
            ts1 = val_array[i]
            nzeros = np.count_nonzero(ts1==0)
            nzeros_perc = nzeros/56*100
            nzeros_list.append(nzeros_perc)
            ts2 = val_array[j]
            nzeros = np.count_nonzero(ts2==0)
            nzeros_perc = nzeros/56*100
            nzeros_list.append(nzeros_perc)
        binwidth = 1
        plt.hist(nzeros_list, bins=np.arange(min(nzeros_list), max(nzeros_list) + binwidth, binwidth))
        plt.savefig('/home/aurelienne.jorge/dados/figs/10032019/hist_zeros.png')
        plt.close()

    def clustering_x_degree(cluster_coeffs, degrees):
        plt.scatter(degrees, cluster_coeffs, s=20, edgecolor=None, alpha=0.5, color='green')
        plt.xlabel('Log of Degree (k)')
        plt.ylabel('Log of Clustering Coefficient (c)')
        plt.xscale('log')
        plt.yscale('log')
        plt.show()
