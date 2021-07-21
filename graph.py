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

    def set_pvalues(g, p_values):
        adj_matrix = g.get_adjacency()
        weight_array = np.array(adj_matrix.data)
        idxs = np.where(weight_array == 1)
        g.es["p_value"] = p_values[idxs]
        return g

    def set_timedelay(g, delay):
        adj_matrix = g.get_adjacency()
        weight_array = np.array(adj_matrix.data)
        idxs = np.where(weight_array == 1)
        g.es["t_delay"] = delay[idxs]
        return g

    def randomize_graph(degree_list, matrix, num_edges, samples):
        avgcluster_samples, avgshortpath_samples, diameter_samples = [], [], []
        avg_min_weight = 0
        avg_max_weight = 0
        avg_heterogeneity = 0
        avg_weights = np.zeros(num_edges)
        i = 0
        while i <= samples:
            print("Sample - "+str(i))
            rg_nx = networkx.generators.degree_seq.configuration_model(degree_list)
            rg = igraph.Graph(directed=False)
            rg.add_vertices(rg_nx.nodes())
            rg.add_edges(rg_nx.edges())
            weights = []
            selfloop = False
            for edge in rg.es:
                if edge.source == edge.target:
                    selfloop = True
                    break
                weight = matrix[edge.source, edge.target]
                if weight >= 0.99:
                    print(weight)
                    print(edge.source, edge.target)
                weights.append(weight)
            if selfloop:
                continue
            rg.es['weight'] = weights
            rg.vs['degree'] = Graph.get_degree(rg)
            min_weight = np.min(np.array(weights))
            max_weight = np.max(np.array(weights))
            avg_min_weight = avg_min_weight + min_weight
            avg_max_weight = avg_max_weight + max_weight
            avg_heterogeneity = avg_heterogeneity + Graph.heterogeneity(rg)
            #avg_weights = np.array(sorted(weights)) + avg_weights
            avgcluster_samples.append(rg.transitivity_avglocal_undirected())
            avgshortpath_samples.append(Graph.get_average_shortest_path_mean(rg))
            diameter_samples.append(rg.diameter(directed=False))

            weights = np.array(weights)
            corr_hist = np.histogram(weights, bins=100, range=(0, 1))
            if corr_hist[0][99] > 0:
                print(weights[weights>=0.98])
            if i == 0:
                avg_corr_hist = corr_hist[0]
            else:
                avg_corr_hist = avg_corr_hist + corr_hist[0]

            i = i + 1

        #avg_weights = avg_weights / samples
        avg_corr_bins = np.arange(0, 1, 0.01)
        avg_corr_hist = avg_corr_hist / samples / num_edges
        #plt.bar(bins, avg_corr_hist, color='blue', width=0.01)
        #plt.show()
        avg_min_weight = avg_min_weight / samples
        avg_max_weight = avg_max_weight / samples
        avg_heterogeneity = avg_heterogeneity / samples
        return avgcluster_samples, avgshortpath_samples, diameter_samples, (avg_corr_bins, avg_corr_hist), \
               avg_min_weight, avg_max_weight, avg_heterogeneity

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

    def get_average_betweenness(g):
        avg_betweenness = np.mean(g.betweenness())

        return avg_betweenness

    def get_clustering_coefficient(g):
        cc = g.transitivity_local_undirected()

        return cc

    def get_components_stats(g):
        clusters = g.clusters()  # get connected components
        num_components = len(clusters)
        giant_component_v = clusters.giant().vcount()
        giant_component_e = clusters.giant().ecount()
        singletons = 0
        for cluster in clusters:
            if len(cluster) == 1:
                singletons = singletons + 1

        return num_components, giant_component_v, giant_component_e, singletons

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

    # Aim: Remove links whose weights are below a certain threshold
    # Input: g, w_threshold
    # Output: g
    def remove_edges(g, w_threshold):
        del_edges = []
        for e in g.es():
            if e['weight'] < w_threshold:
                del_edges.append(e)
        g.delete_edges(del_edges)
        return g

    def max_diameter_threshold(g):
        max_threshold = max(g.es['weight'])
        max_diameter = 0
        for threshold in np.arange(0.50, max_threshold, 0.01):
            # print(threshold)
            ng = g.copy()
            ng = Graph.remove_edges(ng, threshold)
            # print(ng)
            diameter = ng.diameter(directed=False)
            # print(diameter)
            if diameter > max_diameter:
                max_diameter = diameter
                threshold_max_diameter = threshold
        return threshold_max_diameter

    def heterogeneity(g):
        degrees = g.degree()
        acc = 0
        for k in degrees:
            acc = acc + k ** 2
        avg = acc / len(degrees)
        het = avg / (Graph.get_average_degree(g) ** 2)
        return het
