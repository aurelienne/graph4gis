import os
from _datetime import datetime, timedelta
import sys
import glob
import numpy as np
from matplotlib import pyplot as plt

NX = 38
NY = 36

dir_input = "/dados/radar/saoroque/ppi/prec_tamanduatei_box/2015/01"
out = open('acum_prec_daily.csv','w')
start = datetime.strptime(sys.argv[1], "%Y%m%d")
end = datetime.strptime(sys.argv[2], "%Y%m%d")

dict = {}
datehour = start
acum = np.full((NX, NY), 0, dtype=np.float32)

while datehour <= end:
    pattern = datetime.strftime(datehour, "*%Y%m%d*")
    files = glob.glob(os.path.join(dir_input, pattern))
    for file in sorted(files):
        prec = np.fromfile(file.strip(), dtype=np.float32).reshape(NX, NY)
        np.place(prec, prec==-99, 0.0)
        np.place(prec, prec<1, 0.0)
        acum = np.add(prec, acum)

    datehour_str = datetime.strftime(datehour, "%Y%m%d")
    dict[datehour_str] = np.sum(acum)
    out.write(datehour_str+","+str(dict[datehour_str])+"\n")
    datehour = datehour + timedelta(days=1)
    acum = np.full((NX, NY), 0, dtype=np.float32)

out.close()
plt.plot(list(dict.keys()), list(dict.values()))
plt.xticks(rotation=90)
plt.show()