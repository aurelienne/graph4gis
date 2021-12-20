import os
from datetime import datetime, timedelta
import sys
import glob
import numpy as np

#NX = 27
#NY = 29
#NX = 37
#NY = 36
NX = 48
NY = 74

#dir_input = "/dados/radar/saoroque/cappi/prec_tamanduatei/2019/03"
#dir_ouput = "/dados/radar/saoroque/cappi/prec_tamanduatei_hourly/2019/03"
dir_input = sys.argv[1]
dir_output = sys.argv[2]
out = open('acum_prec_hourly.csv', 'w')
#start = datetime.strptime("2019031001", "%Y%m%d%H")
#end = datetime.strptime("2019032000", "%Y%m%d%H")
start = datetime.strptime(sys.argv[3], "%Y%m%d%H")
end = datetime.strptime(sys.argv[4], "%Y%m%d%H")

dict_hourly = {}
dict_daily = {}
datehour = start
#acum = np.full((NY, NX), 0, dtype=np.float32)

while datehour <= end:
    acum = np.full((NY, NX), 0, dtype=np.float32)
    pattern1 = datetime.strftime(datehour, "*%Y%m%d%H00*.*")
    pattern2 = datetime.strftime(datehour - timedelta(hours=1), "*%Y%m%d%H[!00]*.*")
    files = glob.glob(os.path.join(dir_input, pattern1)) + glob.glob(os.path.join(dir_input, pattern2))
    nfiles = len(files)
    for file in sorted(files):
        print(file)
        prec = np.fromfile(file.strip(), dtype=np.float32).reshape(NY, NX)
        np.place(prec, prec==-99, 0.0)
        np.place(prec, prec<1, 0.0)
        acum = np.add(prec, acum)

    if nfiles == 0:
        datehour = datehour + timedelta(hours=1)
        continue

    acum = acum/nfiles

    datehour_str = datetime.strftime(datehour, "%Y%m%d%H")
    date_str = datetime.strftime(datehour, "%Y%m%d")

    np.savetxt(os.path.join(dir_output, datehour_str+"00.txt"), acum, fmt='%03d')
    print(datehour_str)

#    acum_campo = np.sum(acum)
#    dict_hourly[datehour_str] = acum_campo
#    if pattern1[9:11] == '00':
#        dict_daily[date_str] = 0
#    if not np.isnan(acum_campo):
#        dict_daily[date_str] = dict_daily[date_str] + acum_campo

    #out.write(datehour_str+","+str(dict[datehour_str])+"\n")
    datehour = datehour + timedelta(hours=1)


out.close()
#plt.plot(list(dict_daily.keys()), list(dict_daily.values()))
#plt.xticks(list(dict_daily.keys())[::2])
#plt.xticks(rotation=90)
#plt.show()
