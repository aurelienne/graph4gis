import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
from scipy import stats
import sys


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


    def import_bin_from_list(self, input_list):
        f = open(input_list, 'r')
        files = f.readlines()

        i = 0
        date_list = []
        data_list = []
        for filename in files:
            basename = os.path.basename(filename.strip())
            file_datetime = datetime.strptime(basename[-17:-4], "%Y%m%d_%H%M")
            date_list.append(file_datetime)

            data = np.fromfile(filename.strip(), dtype=np.float32)
            data[data<20] = 0
            if i == 0:
                self.filter_points(data, nodata=255)
                i = i + 1
            data = data[data < 255]  # nodata=255 no clip
            data_list.append(data)

        index = pd.DatetimeIndex(date_list)
        self.time_series = pd.Series(data_list, index=index)


    def filter_points(self, data, nodata):
        nodata_idx = np.argwhere(data==nodata)
        self.xlist = np.delete(self.xlist, nodata_idx)
        self.ylist = np.delete(self.ylist, nodata_idx)


    def get_pearson_correlation(self):
        values = self.time_series.values
        val_array = np.array(values.tolist()).transpose()
        corr_matrix = np.corrcoef(val_array, rowvar=True)

        return corr_matrix
