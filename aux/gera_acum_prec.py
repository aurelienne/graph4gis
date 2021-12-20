import os
from _datetime import datetime, timedelta
import sys
import glob
import numpy as np
import png

NX = 37
NY = 36

dir_input = "/dados/radar/saoroque/ppi/prec_tamanduatei_clip/2015/01"
out = open('acum_prec_hourly.csv','w')
#start = datetime.strptime(sys.argv[1], "%Y%m%d%H")
#end = datetime.strptime(sys.argv[2], "%Y%m%d%H")
start = datetime.strptime("2015010100", "%Y%m%d%H")
end = datetime.strptime("2015013123", "%Y%m%d%H")

dict_hourly = {}
dict_daily = {}
datehour = start
acum = np.full((NX, NY), 0, dtype=np.float32)
acum_total = np.full((NX, NY), 0, dtype=np.float32)

while datehour <= end:
    pattern1 = datetime.strftime(datehour, "*%Y%m%d_%H00*dat")
    pattern2 = datetime.strftime(datehour - timedelta(hours=1), "*%Y%m%d_%H*dat")
    files = glob.glob(os.path.join(dir_input, pattern1)) + glob.glob(os.path.join(dir_input, pattern2))
    nfiles = len(files)
    for file in sorted(files):
        print(file)
        prec = np.fromfile(file.strip(), dtype=np.float32).reshape(NX, NY)
        np.place(prec, prec==-99, 0.0)
        np.place(prec, prec<1, 0.0)
        acum = np.add(prec, acum)

    if len(files) > 0:
        acum = acum/nfiles

        datehour_str = datetime.strftime(datehour, "%Y%m%d%H")
        date_str = datetime.strftime(datehour, "%Y%m%d")

        acum_campo = np.sum(acum)
        acum_total = np.add(acum_total, acum)


    #out.write(datehour_str+","+str(dict[datehour_str])+"\n")
    datehour = datehour + timedelta(hours=1)
    #acum = np.full((NX, NY), 0, dtype=np.float32)

# Convert binary file to raster (PNG)
data = acum_total
data = np.where(data<0, 0, data)
data = np.rint(data).astype(np.uint8)
png.from_array(data, 'L').save("total_prec.png")
