import os
from _datetime import datetime, timedelta
import sys
import glob
import numpy as np

#NX = 27
#NY = 29
NX = 36
NY = 37

dir_input = "/dados/radar/saoroque/ppi/level1_tamanduatei_txt/2015/01"
dir_output = "/dados/radar/saoroque/ppi/level1_tamanduatei/2015/01"
start = datetime.strptime("201501010000", "%Y%m%d%H%M")
end = datetime.strptime("201501312350", "%Y%m%d%H%M")

datehour = start
while datehour <= end:
    pattern1 = datetime.strftime(datehour, "*%Y%m%d_%H*.txt")
    files = glob.glob(os.path.join(dir_input, pattern1))
    nfiles = len(files)
    for file in sorted(files):
        filename = os.path.basename(file)

        bin_file = os.path.join(dir_output, filename.replace(".txt", ".dat"))
        f = open(bin_file, "wb")
        data = np.loadtxt(file, dtype=np.float32)
        np.place(data, data == -99, 255)
        f.write(data)
        f.close()
        #np.save(bin_file, data)

    #datehour = datehour + timedelta(hours=1)
    datehour = datehour + timedelta(minutes=10)
