from osgeo import ogr
import matplotlib.pyplot as plt
import os

class Shapefile:

    """Classe baseada no código de Wilson Ceron"""
    def __init__( self, g, filename):
        self.g		= g
        self.filename	= filename

    def	create_lines(self, path):
        csvFile= path+"/"+self.filename+"_lines.csv"
        f = open(csvFile,'w')
        f.write("Label,Lines,weight\n")

        for edge in self.g.get_edgelist():
            f.write('%s_%s,"'	%	(	self.g.vs[edge[0]]["label"], self.g.vs[edge[1]]["label"]	)	)
            f.write("LINESTRING ("																		)
            f.write("%s %s,"	%	(	self.g.vs[edge[0]]["x"],self.g.vs[edge[0]]["y"]				)	)
            f.write('%s %s)",'	%	(	self.g.vs[edge[1]]["x"],self.g.vs[edge[1]]["y"]				)	)
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
        if center == False:
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
            f.write("id,x,y,degree,wDegree,closeness,betweennes,cc,sPathMean\n")
            for v in self.g.vs:
                f.write(	str(v["label"])			+	","	+	str(v["x"] + dx/2.)					+	","		+	str(v["y"] + dy/2.)					+	","	)
                f.write(	str(v["degree"])		+	","	+	str(v["weightedDegree"])	+	","	)
                f.write(	str(v["closeness"])		+	","	+	str(v["betweenness"])		+	","		+	str(v["clusterCoeficient"])	+	","	)
                f.write(	str(v["shortestPathMean"]) +"\n")
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
        current_path 	=	os.getcwd()
        path			=	current_path+path[1:]
        self.create_lines(path)
        self.create_points(path, dx, dy, center=True)
        if dx != None and dy != None:
            self.create_polygons(path, dx, dy)

class TextFiles:

    def __init__(self, g, filename):
        self.filename = filename
        self.g = g

    def create_csv(self, threshold):
        avg_cluster = self.g.get_average_clustering()
        avg_degree = self.g.get_average_degree()
        diameter = self.g.get_diameter()
        shortpath_mean = self.g.get_average_shortest_path_mean()

        f = open(self.filename, "a")
        f.write(str(threshold) + "," + str(avg_cluster) + "," + str(avg_degree) + "," + str(diameter) + "," + str(
            shortpath_mean) + "\n")
        f.close()

class Plots:

    def __init__(self, g):
        self.g = g

    def plot_degree_histogram(self):
        plt.hist(self.g.vs["degree"], bins='auto', alpha=0.7, rwidth=0.85)
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel('Degree Values')
        plt.ylabel('Frequency')
        plt.title('Degree Histogram')
        plt.show()

    def plot_correlation_histogram(self, corr_matrix):
        plt.hist(corr_matrix, bins='auto', alpha=0.7, rwidth=0.85)
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel('Correlation')
        plt.ylabel('Frequency')
        plt.title('Correlation Histogram')
        plt.show()