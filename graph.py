import igraph
import numpy as np

class Graph:

    def __init__(self, matrix, threshold, xlist, ylist):
        matrix = np.nan_to_num(matrix)
        matrix[matrix<threshold] = 0.0
        self.graph = igraph.Graph.Weighted_Adjacency((matrix).tolist(), mode='undirected', attr="weight", loops=False)
        self.graph.vs["label"] = np.arange(len(xlist))
        self.graph.vs["x"] = xlist
        self.graph.vs["y"] = ylist

    def plot(self, filename):
        visual_style = {}
        visual_style["vertex_label_dist"] = 0
        visual_style["vertex_shape"] = "circle"
        visual_style["bbox"] = (2000, 2000)
        visual_style["vertex_size"] = 30
        visual_style["layout"] = "large"
        visual_style["margin"] = 40

        igraph.plot(self.graph, filename + ".svg", **visual_style)

    def get_diameter(self):
        return self.graph.diameter(directed=False)

    def get_shortest_paths(self):
        return self.graph.shortest_paths()

    def get_shortest_path_mean(self):
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

    def get_average_shortest_path_mean(self):
        sh_paths_mean = self.get_shortest_path_mean()
        sh_paths_mean = sh_paths_mean[sh_paths_mean>0]
        if len(sh_paths_mean) == 0:
            avg_sh_paths_mean = np.inf
        else:
            avg_sh_paths_mean = sum(sh_paths_mean)/len(sh_paths_mean)
        return avg_sh_paths_mean

    def get_average_degree(self):
        return igraph.mean(self.graph.degree())

    def get_degree_distribution(self):
        return self.graph.degree_distribution()

    def get_average_path(self):
        return self.graph.average_path_length()

    def get_average_clustering(self):
        return self.graph.transitivity_undirected()

    def get_degree(self):
        degree = self.graph.degree()
        self.graph.vs["degree"] = degree
        return degree

    def get_strength(self):
        weightedDegree = self.graph.strength()
        self.graph.vs["weightedDegree"] = weightedDegree

        return weightedDegree

    def get_closeness(self):
        closeness = self.graph.closeness()
        self.graph.vs["closeness"] = closeness

        return closeness

    def get_betweenness(self):
        betweenness = self.graph.betweenness()
        self.graph.vs["betweenness"] = betweenness

        return betweenness

    def get_clustering_coefficient(self):
        cc = self.graph.transitivity_local_undirected()
        self.graph.vs["clusterCoeficient"] = cc

        return cc
