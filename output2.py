import os.path
import sys

import fiona

class Shapefile:

    def __init__(self, g):
        self.g = g

    def create_points(self, outDir, filename):
        schema = {
            'geometry': 'Point',
            'properties': [('Name', 'str')]
        }
        shpFilename = os.path.join(outDir, filename+'_nodes.shp')
        pointShp = fiona.open(shpFilename, mode='w', driver='ESRI Shapefile',
                              schema=schema, crs="EPSG:4326")
        for vs in self.g.vs:
            x = float(vs['x'])
            y = float(vs['y'])
            label = vs['label']
            pointDict = {
                'geometry': {'type': 'Point',
                             'coordinates': (x, y)},
                'properties': {'Name': label},
            }
            pointShp.write(pointDict)
        pointShp.close()

    def create_lines(self, outDir, filename, tdelay=False):
        if tdelay:
            schema = {
                'geometry': 'LineString',
                'properties': [('Name', 'str'),
                               ('Weight', 'float'),
                               ('TDelay', 'float')]
            }
        else:
            schema = {
                'geometry': 'LineString',
                'properties': [('Name', 'str'),
                               ('Weight', 'str')]
            }
        shpFilename = os.path.join(outDir, filename+'_edges.shp')
        lineShp = fiona.open(shpFilename, mode='w', driver='ESRI Shapefile',
                              schema=schema, crs="EPSG:4326")
        edgeList = self.g.get_edgelist()
        for i in range(len(edgeList)):
            es = edgeList[i]
            v1 = self.g.vs[es[0]]
            v2 = self.g.vs[es[1]]
            line = [(float(v1['x']), float(v1['y'])),
                    (float(v2['x']), float(v2['y']))]
            label = str(es[0]) + '_' + str(es[1])
            weight = self.g.es[i]['weight']
            print(weight)
            print(line)
            if tdelay:
                timeDelay = self.g.es[i]['t_delay']
                print(timeDelay)
                lineDict = {
                    'geometry': {'type': 'LineString',
                                 'coordinates': line},
                    'properties': {'Name': label,
                                   'Weight': weight,
                                   'TDelay': timeDelay},
                }
            else:
                lineDict = {
                    'geometry': {'type': 'LineString',
                                 'coordinates': line},
                    'properties': {'Name': label,
                                   'Weight': weight},
                }
            lineShp.write(lineDict)
        lineShp.close()

    def	create_shape(self, outDir, filename, tdelay):
        self.create_lines(outDir, filename, tdelay)
        self.create_points(outDir, filename)