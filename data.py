import pandas as pd
import os
from datetime import datetime, timedelta
import scipy
import numpy as np
import matplotlib.pyplot as plt


class Data:

    def __init__(self, x1, y1, x2, y2, dx, dy, nx, ny):
        self.time_series = None
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.dx = dx
        self.dy = dy
        x = np.arange(x1, x2, dx)[0:nx]
        y = np.arange(y1, y2, dy)[0:ny]
        xx, yy = np.meshgrid(x,y)
        self.xlist = xx.flatten()
        self.ylist = yy.flatten()
        self.nx = len(self.xlist)
        self.ny = len(self.ylist)

    def import_bin_from_list(self, input_list, dbz_min, dt_pos_ini, dt_pos_fim, dt_format):
        f = open(input_list, 'r')
        files = f.readlines()
        i = 0
        date_list = []
        data_list = []
        print(len(self.xlist))
        print(len(self.ylist))
        for filename in files:
            basename = os.path.basename(filename.strip())
            file_datetime = datetime.strptime(basename[dt_pos_ini:dt_pos_fim], dt_format)
            date_list.append(file_datetime)
            data = np.fromfile(filename.strip(), dtype=np.float32)
            data[data < dbz_min] = 0
            if i == 0:
                self.remove_nodata_points(data, nodata=255)
                i = i + 1
            data = data[data < 255]  # nodata=255 no clip
            data_list.append(data)

        data_list = self.remove_zerostd_points(data_list)
        #data_list = self.remove_lowavg_points(data_list)
        self.nx = len(self.xlist)
        self.ny = len(self.ylist)
        index = pd.DatetimeIndex(date_list)
        self.time_series = pd.Series(data_list, index=index)

    def remove_nodata_points(self, data, nodata):
        # Remove nodata cells
        nodata_idx = np.argwhere(data==nodata)
        self.xlist = np.delete(self.xlist, nodata_idx)
        self.ylist = np.delete(self.ylist, nodata_idx)

    def remove_zerostd_points(self, data_list):
        data = np.array(data_list).transpose()
        idxs = []
        for i in range(data.shape[0]):
            std = np.std(data[i, :])
            if std == 0:
                idxs.append(i)
        self.xlist = np.delete(self.xlist, idxs)
        self.ylist = np.delete(self.ylist, idxs)
        filtered_data = np.delete(data, idxs, axis=0)
        return_data = (filtered_data.transpose()).tolist()
        return return_data

    def remove_lowavg_points(self, data_list):
        data = np.array(data_list).transpose()
        idxs = []
        for i in range(data.shape[0]):
            avg = np.mean(data[i, :])
            if avg < 1:
                idxs.append(i)
        self.xlist = np.delete(self.xlist, idxs)
        self.ylist = np.delete(self.ylist, idxs)
        filtered_data = np.delete(data, idxs, axis=0)
        return_data = (filtered_data.transpose()).tolist()
        return return_data

    def get_pearson_correlation(self):
        values = self.time_series.values
        val_array = np.array(values.tolist()).transpose()
        corr_matrix = np.corrcoef(val_array, rowvar=True)
        #nan_idx = np.argwhere(np.isnan(corr_matrix[:]))
        return corr_matrix

    def get_pearson_correlation_timedelay(self, max_delay):
        values = self.time_series.values
        val_array = np.array(values.tolist()).transpose()

        idx_delay = 1
        initial_datetime = self.time_series.index[0]
        for idx_dt in self.time_series.index:
            if idx_dt > initial_datetime + max_delay:
                break
            idx_delay = idx_delay + 1

        print("idx_delay = "+str(idx_delay))
        corr_matrix = np.zeros((self.nx, self.ny), dtype=np.float16)
        p_values = np.zeros((self.nx, self.ny), dtype=np.float16)
        delay = np.zeros((self.nx, self.ny), dtype=np.float16)
        corr_matrix[:, :] = self.get_pearson_correlation()
        plt.hist(corr_matrix[corr_matrix>=0.75], bins=25)
        plt.savefig('hist_corr.png')
        plt.close()
        for x in range(self.nx):
            for y in range(self.ny):
                for t in range(1, idx_delay):
                    t1_array = val_array[x, :-t]
                    t2_array = val_array[y, t:]
                    corr_value, p_value = scipy.stats.pearsonr(t1_array, t2_array)
                    if corr_value > corr_matrix[x, y]:
                        corr_matrix[x, y] = corr_value
                        p_values[x, y] = p_value
                        delay[x, y] = t

        plt.hist(corr_matrix[corr_matrix>=0.75], bins=25)
        plt.savefig('hist_corr_delay.png')
        plt.close()
        values, count = np.unique(delay, return_counts=True)
        print("Values = "+str(values)+" Counts="+str(count))
        idxs = np.argwhere(corr_matrix>=0.75)
        print(len(idxs))
        delay2=delay[idxs]
        values, count = np.unique(delay2, return_counts=True)
        print("correlation > 0.75:")
        print("Values = "+str(values)+" Counts="+str(count))
        #plt.boxplot(p_values[idxs])
        #plt.savefig('boxplot_pvalues_delayed.png')
        #plt.close()
        return corr_matrix

    def get_threshold_from_percentile(self, corr_matrix, percentile):
        idxs = np.triu_indices(corr_matrix.shape[0], k=1)
        threshold = scipy.stats.scoreatpercentile(corr_matrix[idxs], percentile)
        return threshold

    def get_euclidean_distances(self):
        dists = np.zeros((self.nx, self.nx))
        for i in range(len(self.xlist)):
            for j in range(i+1, len(self.xlist)):
                point1 = np.array((self.xlist[i], self.ylist[i]))
                point2 = np.array((self.xlist[j], self.ylist[j]))
                dists[i, j] = np.linalg.norm(point1 - point2) * 111
        return dists

    def get_neighbours(self, radius=1):
        f = open("neighbours.csv", "w")
        nodes = len(self.xlist)
        radius_x = radius * self.dx
        radius_y = radius * self.dy
        for i in range(nodes):
            lon_i = self.xlist[i]
            lat_i = self.ylist[i]
            neighbours = []
            for j in range(nodes):
                if i == j:
                    continue
                lon_j = self.xlist[j]
                lat_j = self.ylist[j]
                dist_x = float('%.5f'%abs(lon_i - lon_j))
                dist_y = float('%.5f'%abs(lat_i - lat_j))
                if abs(dist_x) <= abs(radius_x) and abs(dist_y) <= abs(radius_y):
                    neighbours.append(j)
            f.write(str(i)+";"+str(neighbours)+"\n")
