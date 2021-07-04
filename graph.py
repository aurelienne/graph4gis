import igraph
import numpy as np
import networkx
import output as out
import calc
import matplotlib.pyplot as plt

class Graph:

    def from_graphml(gml):
        graph = igraph.Graph.Read_GraphML(gml)
        return graph

    def from_correlation_matrix(matrix, threshold, xlist, ylist):
        matrix = np.nan_to_num(matrix)
        matrix[matrix < threshold] = 0.0
        graph = igraph.Graph.Weighted_Adjacency((matrix).tolist(), mode='undirected', attr="weight", loops=False)
        graph.vs["label"] = np.arange(len(xlist))
        graph.vs["x"] = xlist
        graph.vs["y"] = ylist
        return graph

    def randomize_graph(degree_list, matrix, num_edges, samples):
        avgcluster_samples, avgshortpath_samples, diameter_samples = [], [], []
        avg_min_weight = 0
        avg_max_weight = 0
        avg_weights = np.zeros(num_edges)
        for i in range(samples):
            rg_nx = networkx.generators.degree_seq.configuration_model(degree_list)
            rg = igraph.Graph(directed=False)
            rg.add_vertices(rg_nx.nodes())
            rg.add_edges(rg_nx.edges())
            weights = []
            for edge in rg.es:
                weights.append(matrix[edge.source, edge.target])
            rg.es['weight'] = weights
            rg.vs['degree'] = Graph.get_degree(rg)
            min_weight = np.min(np.array(weights))
            max_weight = np.max(np.array(weights))
            avg_min_weight = avg_min_weight + min_weight
            avg_max_weight = avg_max_weight + max_weight
            avg_weights = np.array(sorted(weights)) + avg_weights
            avgcluster_samples.append(rg.transitivity_avglocal_undirected())
            avgshortpath_samples.append(Graph.get_average_shortest_path_mean(rg))
            diameter_samples.append(rg.diameter(directed=False))

        avg_weights = avg_weights / samples
        avg_min_weight = avg_min_weight / samples
        avg_max_weight = avg_max_weight / samples
        return avgcluster_samples, avgshortpath_samples, diameter_samples, avg_weights, avg_min_weight, avg_max_weight

    def plot(filename, g):
        visual_style = {}
        visual_style["vertex_label_dist"] = 0
        visual_style["vertex_shape"] = "circle"
        visual_style["bbox"] = (2000, 2000)
        visual_style["vertex_size"] = 30
        visual_style["layout"] = "large"
        visual_style["margin"] = 40

        igraph.plot(g, filename + ".svg", **visual_style)

    def get_shortest_path_mean(g):
        paths = g.shortest_paths()
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

        return mean

    def get_average_shortest_path_mean(g):
        sh_paths_mean = Graph.get_shortest_path_mean(g)
        sh_paths_mean = sh_paths_mean[sh_paths_mean>0]
        if len(sh_paths_mean) == 0:
            avg_sh_paths_mean = np.inf
        else:
            avg_sh_paths_mean = sum(sh_paths_mean)/len(sh_paths_mean)
        return avg_sh_paths_mean

    def get_average_degree(g):
        return igraph.mean(g.degree())

    def get_degree_distribution(g):
        return g.degree_distribution()

    def get_average_path(g):
        return g.average_path_length()

    def get_average_clustering(g):
        return g.transitivity_avglocal_undirected()

    def get_degree(g):
        degree = g.degree()
        return degree

    def get_strength(g):
        weightedDegree = g.strength()

        return weightedDegree

    def get_closeness(g):
        closeness = g.closeness()

        return closeness

    def get_betweenness(g):
        betweenness = g.betweenness()

        return betweenness

    def get_clustering_coefficient(g):
        cc = g.transitivity_local_undirected()

        return cc

    def calculate_vertices_metrics(g):
        g.vs["weightedDegree"] = Graph.get_strength(g)
        g.vs["degree"] = Graph.get_degree(g)
        g.vs["clusterCoeficient"] = Graph.get_clustering_coefficient(g)
        g.vs["closeness"] = closeness = Graph.get_closeness(g)
        g.vs["betweenness"] = Graph.get_betweenness(g)
        g.vs["shortestPathMean"] = Graph.get_shortest_path_mean(g)
        #g.vs["strength"] = g.strength(weights=g.es['weight'])

        return g

    def get_manhattan_shortest_paths(g):
        mdists = np.zeros((len(g.vs), len(g.vs)))
        for vi in range(len(g.vs)):
            #print(g.get_all_shortest_paths(vi))
            for p in g.get_all_shortest_paths(vi):
                dest = p[-1]
                if dest < vi:
                    continue
                p_dist = 0
                point1 = np.array((g.vs["x"][vi], g.vs["y"][vi]))
                vj = None
                for pv in range(1, len(p)):
                    vj = p[pv]
                    point2 = np.array((g.vs["x"][vj], g.vs["y"][vj]))
                    dist = np.linalg.norm(point1 - point2) * 111
                    p_dist = p_dist + dist
                    point1 = point2
                if vj is not None:
                    mdists[vi, vj] = p_dist

        return mdists
