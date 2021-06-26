import numpy as np
import os
import matplotlib.pyplot as plt
import rasterio as rio
from rasterio.plot import plotting_extent
from rasterio.mask import mask
from rasterio.io import MemoryFile
from shapely.geometry import mapping
import geopandas as gpd
#import earthpy as et
import png
import sys
plt.ion()

#path_out = "/dados/radar/saoroque/ppi/prec_tamanduatei_clip/2015/01"
#binfile = '/dados/radar/saoroque/ppi/level1/2015/01/ppi_CZ_01_20150131_2350.dat'
binfile = sys.argv[1]
shapefile = sys.argv[2]
path_out = sys.argv[3]


filename = os.path.splitext(binfile)[0]
basename = os.path.basename(binfile)

# Convert binary file to raster (PNG)
data = np.fromfile(binfile.strip(), dtype=np.float32).reshape((666,666),order='C')
data = np.where(data<0, 0, data)
data = np.rint(data).astype(np.uint8)
png.from_array(data, 'L').save(filename+".png")

# Create PGW
pgw = open(filename+".pgw",'w')
pgw.write('0.00747135\n'+
          '0.0000\n'+
          '0.0000\n'+
          '-0.00675451\n'+
          '-49.576\n'+
          '-21.338\n')
pgw.close()


#crop_extent = gpd.read_file('/dados/shapes/ottoTamanduatei/ottoTamanduatei_dissolved_4326.shp')
crop_extent = gpd.read_file(shapefile)

# create geojson object from the shapefile imported above
extent_geojson = mapping(crop_extent['geometry'][0])


with rio.open(filename+".png") as raster:
    radar_crop, radar_crop_affine = mask(raster,
                                         [extent_geojson],
                                         crop=True,
                                         nodata=255)
    radar_meta = raster.profile

# Create spatial plotting extent for the cropped layer
radar_extent = plotting_extent(radar_crop[0], radar_crop_affine)

# Plot your data
fig, ax = plt.subplots(figsize=(10, 8))
ax.imshow(radar_crop[0],
          extent=radar_extent,
          cmap='Greys')
ax.set_title("Cropped Raster Dataset")
ax.set_axis_off()

# Update with the new cropped affine info and the new width and height
radar_meta.update({'transform': radar_crop_affine,
                       'height': radar_crop.shape[1],
                       'width': radar_crop.shape[2],
                       'nodata': -999.99})

# Write data
with rio.open(os.path.join(path_out, basename.replace(".dat", ".png")), 'w', **radar_meta) as ff:
    ff.write(radar_crop[0], 1)

# Create PGW
pgw = open(os.path.join(path_out, basename.replace(".dat",".pgw")),'w')
pgw.write(str(radar_crop_affine.a)+'\n'+
          str(radar_crop_affine.b)+'\n'+
          str(radar_crop_affine.d)+'\n'+
          str(radar_crop_affine.e)+'\n'+
          str(radar_crop_affine.c)+'\n'+
          str(radar_crop_affine.f)+'\n')
pgw.close()

bindata = radar_crop[0].copy(order='C').astype(np.float32)
bin = open(os.path.join(path_out, basename),'wb')
bin.write(bindata)
bin.close()