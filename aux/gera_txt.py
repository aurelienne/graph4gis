import os
from _datetime import datetime, timedelta
import sys
import glob
import numpy as np

#NX = 27
#NY = 29
NX = 36
NY = 37

dir_input = "/dados/radar/saoroque/ppi/level1_tamanduatei/2015/01"
dir_output = "/dados/radar/saoroque/ppi/level1_tamanduatei_txt/2015/01"
start = datetime.strptime("201501312310", "%Y%m%d%H%M")
end = datetime.strptime("201501312350", "%Y%m%d%H%M")

datehour = start
while datehour <= end:
    pattern1 = datetime.strftime(datehour, "*%Y%m%d_%H*.dat")
    files = glob.glob(os.path.join(dir_input, pattern1))
    nfiles = len(files)
    for file in sorted(files):
        filename = os.path.basename(file)
        data = np.fromfile(file.strip(), dtype=np.float32).reshape((NY, NX), order='C')
        np.place(data, data==255, -99)
        #np.place(data, data<0, 0.0)

        txt_file = os.path.join(dir_output, filename.replace(".dat", ".txt"))
        np.savetxt(txt_file, data, fmt='%03d')

    #datehour = datehour + timedelta(hours=1)
    datehour = datehour + timedelta(minutes=10)
