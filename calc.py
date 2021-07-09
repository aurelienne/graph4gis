import datetime

#import sklearn
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import stats
import sys
import csv
import graph
import output as out

class Stats:

    def shuffle(self, time_series, corr_matrix, samples):
        values = time_series.values
        val_array = np.array(values.tolist()).transpose()
        npoints = val_array.shape[0]
        corr_dif = np.zeros((npoints, npoints))
        idxs = np.triu_indices(npoints, k=1)

        for i in range(npoints):
            for j in range(i+1, npoints):
                corr_values = []
                for s in range(samples):
                    shuffled = sklearn.utils.shuffle(val_array[i])
                    corr_coef = np.corrcoef(val_array[j], shuffled)[0, 1]
                    corr_values.append(corr_coef)
                p95 = np.percentile(corr_values, 95)
                real_corr = corr_matrix[i, j]
                if real_corr < p95:
                    corr_dif[i, j] = 1
                plt.cla()
                plt.hist(np.around(corr_values, 4), bins=30, alpha=0.7, rwidth=2, histtype='bar')
                plt.xlabel('Correlation')
                plt.ylabel('Frequency')
                plt.axvline(p95, color='b', label='95 percentile= '+"{:+.4f}".format(p95))
                plt.axvline(real_corr, color='r', label='Real correlation= ' + "{:+.4f}".format(real_corr))
                plt.title('Bootstrap Histogram  - Point (%s,%s)' % (str(i), str(j)))
                plt.legend()
                plt.savefig("/dados/mestrado/bootstrap_%s_%s.png" % (str(i), str(j)))

        plt.close()
        plt.hist(np.around(corr_dif[idxs], 4), bins=30, alpha=0.7, rwidth=2, histtype='bar')
        plt.savefig("/dados/mestrado/bootstrap_dif_corr.png")
        sys.exit()

    def pearson_significance_test(self, time_series):
        with open('corr_test_100319.csv', mode='w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(['r', 'p', 'ci_lo', 'ci_hi'])

            values = time_series.values
            val_array = np.array(values.tolist()).transpose()
            npoints = val_array.shape[0]
            for i in range(npoints):
                for j in range(i+1, npoints):
                    r, p_val, ci_lo, ci_hi = self.pearsonr_ci(val_array[i], val_array[j])
                    if r < ci_lo or r > ci_hi:
                        writer.writerow([r, p_val, ci_lo, ci_hi])

    def pearsonr_ci(self, x, y, alpha=0.05):
        ''' calculate Pearson correlation along with the confidence interval using scipy and numpy
        Parameters
        ----------
        x, y : iterable object such as a list or np.array
          Input for correlation calculation
        alpha : float
          Significance level. 0.05 by default
        Returns
        -------
        r : float
          Pearson's correlation coefficient
        pval : float
          The corresponding p value
        lo, hi : float
          The lower and upper bound of confidence intervals
        '''

        r, p = stats.pearsonr(x,y)
        r_z = np.arctanh(r)
        se = 1/np.sqrt(len(x)-3)
        z = stats.norm.ppf(1-alpha/2)
        lo_z, hi_z = r_z-z*se, r_z+z*se
        lo, hi = np.tanh((lo_z, hi_z))
        return r, p, lo, hi

    def ttest_regression(self, x, y, alfa=0.05):

        '''T-test hypothesis testing for regression. Returns 1 if null Hypthotesis can be rejected and 0 if it can't.
        x and y are the two variables and alfa is the desired statistical significance.'''
        idx = np.isfinite(y)
        x = x[idx]
        y = y[idx]
        n = len(x)
        xmed = np.sum(x) / n;
        ymed = np.sum(y) / n;
        Sxy = 0
        Sxx = 0
        Syy = 0

        for i in range(n):
            Sxy = Sxy + ((x[i] - xmed) * (y[i] - ymed))
            Sxx = Sxx + np.power(x[i] - xmed, 2)

        b1 = Sxy / Sxx
        b0 = ymed - b1 * xmed

        for i in range(n):
            Syy = Syy + np.power(y[i] - ymed, 2)

        R2 = np.power(Sxy, 2) / (Sxx * Syy)
        R2a = 1 - ((n - 1) / (n - 2)) * (1 - R2)
        QME = (Syy - (b1 * Sxy)) / (n - 2)
        bla = (1.0 / n) + (xmed * xmed) / (Sxx)
        t0 = b0 / np.sqrt(QME * bla)
        t = b1 / np.sqrt(QME / Sxx)

        pvalue = 2*(1 - stats.t.cdf(np.abs(t), df=n-2))
        if np.abs(pvalue) <= alfa:
            reject = 1
        else:
            reject = 0

        # Slope and Beta
        m, b = np.polyfit(x, y, 1)

        return reject, pvalue, b, m

    def test_greater_distribution(self, d1, d2):
        x, y = stats.mannwhitneyu(d1, d2, alternative='two-sided')
        print("The statistics: ", x)
        print("The p-value", y)
        #if y <= 0.05:
        #    print(
        #        "Reject the null hypothesis, that the probability of X being greater than Y is equal to the probability of Y being greater than X")
        #else:
        #    print("The null hypothesis cannot be rejected")

    def rewired_graph(self, g, samples, corr_matrix, eucl_dists):
        am_list = []
        am = g.get_adjacency()
        am_list.append(am)
        avgcluster_samples = []
        avgshortpath_samples = []
        diameter_samples = []
        n = len(g.vs)
        num_edges = len(g.es)
        avg_weights = np.zeros(num_edges)
        lf = open('regression_test_RC.log', 'w')

        for i in range(samples):
            new_graph = g.copy()
            new_graph.rewire(n=int(math.floor(num_edges/2)))
            weights = []
            for edge in new_graph.es:
                weights.append(corr_matrix[edge.source, edge.target])
            new_graph.es['weight'] = weights
            avgcluster_samples.append(new_graph.transitivity_avglocal_undirected())
            avgshortpath_samples.append(graph.Graph.get_average_shortest_path_mean(new_graph))
            diameter_samples.append(new_graph.diameter(directed=False))
            #am = new_graph.get_adjacency()
            #am_list.append(am)
            new_graph = graph.Graph.calculate_vertices_metrics(new_graph)
            #if i <= 10:
            #    out.Shapefile(new_graph, "rewired_" + str(i)).create_shape("")
            #    #out.Plots(new_graph).plot_distance_x_distance(eucl_dists, np.array(new_graph.shortest_paths()))
            avg_weights = avg_weights + np.array(weights)

            idxs = np.triu_indices(eucl_dists.shape[0], k=1)
            x = eucl_dists[idxs].flatten()
            y = np.array(new_graph.shortest_paths())[idxs].flatten()
            idx = np.isfinite(y)
            x1 = x[idx]
            y1 = y[idx]
            reject, pvalue, b, slope = self.ttest_regression(x1, y1)
            if reject == 1:
                lf.write(str(reject) + "," + str(pvalue) + "," + str(b) + "," + str(slope) + "\n")

            del new_graph


        """
                # Codigo para testar diferenças no rewire
                idxs = np.triu_indices(am.shape[0], k=1)    
                for i in range(len(am_list)):
                    for j in range(i+1, len(am_list)):
                        a1 = np.array(am_list[i].data)
                        a2 = np.array(am_list[j].data)
                        dif = np.equal(a1[idxs], a2[idxs])
                        count_dif = np.unique(dif, return_counts=True)
                        print(i,j)
                        print(count_dif)
                """
        avg_weights = avg_weights / samples

        return avgshortpath_samples, avgcluster_samples, diameter_samples, avg_weights

    def backbone(g, alpha):
        # Implementação do Iuri Diniz (UFOP)
        print("Starting backbone - "+str(datetime.datetime.now()))

        # pij = (1 - (wij/si))**(ki - 1), onde:
        # w --> weight
        # s --> strength
        # k --> degree
        p = {}
        adj = g.get_adjacency()
        n_nodes = g.vcount()
        strength = g.strength(weights=g.es['weight'])
        for i in range(n_nodes):
            for j in range(n_nodes):
                if (adj[i, j] == 1):  # verificando se há conexão entre o par i,j
                    w = g.es[g.get_eid(i, j)]['weight']
                    s = strength[i]  # calcula o strength de toda a rede e retorna apenas para o nó desejado
                    k = g.vs[i].degree()
                    pij = (1 - (w / s)) ** (k - 1)
                    if (pij < alpha):  # aplicando a relação com o alpha
                        p[i, j] = pij

        # Pegando os pares simétricos e atribuindo -99 ao par com maior valor de probabilidade
        for i in p:
            if ((i[0], i[1]) and (i[1], i[0])) in p.keys():
                if p[i[0], i[1]] <= p[i[1], i[0]]:
                    p[i[1], i[0]] = -99
                else:
                    p[i[0], i[1]] = -99

        # Criando dicionário com os pares válidos
        pij = {}
        for i in p:
            if not (p[i] == -99):
                pij[i] = p[i]

        print("Ending backbone - "+str(datetime.datetime.now()))

        return (pij)

    def test_backbone(self, g, num_edges, corr_matrix):
        prev_dif = 9999
        for alfa in np.arange(0.128, 0.129, 0.001):
        #for alfa in np.arange(0.300, 0.320, 0.001):
            pij = Stats.backbone(g, alfa)
            dif = abs(len(pij) - num_edges)
            if dif > prev_dif:
                break
            prev_dif = dif
            prev_pij = pij.copy()
        print(alfa, prev_dif, dif)

        # Delete edges and add only the most significant ones
        g.es.delete()
        g.add_edges(prev_pij.keys())
        g.es['prob'] = list(prev_pij.values())
        weights = []
        for edge in g.es:
            weights.append(corr_matrix[edge.source, edge.target])
        g.es['weight'] = weights

        return g