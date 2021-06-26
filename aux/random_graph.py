import igraph
import numpy as np

class Graph:

    def __init__(self, nodes, edges):
        self.graph = igraph.Graph.Erdos_Renyi(n=nodes, m=edges)

    def getDiameter(self):
        return self.graph.diameter(directed=False)

    def getShortest_paths(self):
        return self.graph.shortest_paths()

    def getShortestPathMean(self):
        paths = self.graph.shortest_paths()
        nodes = len(paths)
        mean = np.zeros(nodes)
        for i in range(nodes):
            count = 0
            path_length = len(paths[i])
            for j in range(path_length):
                if (paths[i][j] == np.inf):
                    paths[i][j] = 0
                else:
                    # Contabiliza elementos da componente conexa
                    count += 1

            if (count - 1) <= 0:
                mean[i] = 0
            else:
                mean[i] = np.sum(paths[i]) / (count - 1)

        self.graph.vs["shortestPathMean"] = mean
        return mean

    def getAverageShortestPathMean(self):
        sh_paths_mean = self.getShortestPathMean()
        sh_paths_mean = sh_paths_mean[sh_paths_mean > 0]
        return sum(sh_paths_mean) / len(sh_paths_mean)

    def getNumberOfEdges(self):
        return len(self.graph.get_edgelist())

    def getNumberOfVertices(self):
        return len(self.graph.degree())

    def getAverageDegree(self):
        return igraph.mean(self.graph.degree())

    def getDegreeDistribution(self):
        return self.graph.degree_distribution()

    def getAveragePath(self):
        return self.graph.average_path_length()

    def getDegree(self):
        degree = self.graph.degree()
        self.graph.vs["degree"] = degree
        return degree

    def getClusterCoeficient(self):
        clusterCoeficient = self.graph.transitivity_local_undirected()
        self.graph.vs["clusterCoeficient"] = clusterCoeficient

        return clusterCoeficient

    def getAverageClustering(self):
        return self.graph.transitivity_undirected()


#nodes = 1331
#edges = 1515
nodes = 587
edges = 1270
g = Graph(nodes, edges)
print(igraph.mean(g.getDegree()))
print(g.getAverageShortestPathMean())
print(g.getAverageClustering())
print(g.getDiameter())
#igraph.plot(g.graph)