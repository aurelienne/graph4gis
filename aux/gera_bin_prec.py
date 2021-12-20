import os
import sys
import numpy as np

dbz_file = sys.argv[1]
path_out = sys.argv[2]
basename = os.path.basename(dbz_file)

#nx = 666
#ny = 666
#nx = 27
#ny = 29
nx = 48
ny = 74
dbz = np.fromfile(dbz_file, dtype=np.float32).reshape(ny, nx)
prec = np.full((ny, nx), -99.0, dtype=np.float32)

for x in range(nx):
    for y in range(ny):
        if dbz[y, x] != -99 and dbz[y, x] <= 36:
            prec[y, x] = ((10**(dbz[y, x]/10))/200)**0.625
        elif dbz[y, x] > 36:
            prec[y, x] = ((10**(dbz[y, x]/10))/300)**0.714

prec_file = os.path.join(path_out, basename)
with open(prec_file, 'wb') as fn:  # Escrita do arquivo como binario
    fn.write(prec)
