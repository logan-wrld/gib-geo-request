import os
from io import BytesIO
from skimage import io
import requests
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import urllib.request
import urllib.parse
import mapbox_vector_tile
import xml.etree.ElementTree as xmlet
import lxml.etree as xmltree
from PIL import Image as plimg
import numpy as np
from owslib.wms import WebMapService
from IPython.display import Image, display

# Construct Web Mercator projection URL.
proj3857 = 'https://gibs.earthdata.nasa.gov/wms/epsg3857/best/wms.cgi?\
version=1.3.0&service=WMS&\
request=GetMap&format=image/png&STYLE=default&bbox=-8000000,-8000000,8000000,8000000&\
CRS=EPSG:3857&HEIGHT=600&WIDTH=600&TIME=2000-12-01&layers=Landsat_WELD_CorrectedReflectance_Bands157_Global_Annual'

# Request image.
img=io.imread(proj3857)

# Display image on map.
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection = ccrs.Mercator.GOOGLE)
extent = (-8000000, 8000000, -8000000, 8000000)
plt.imshow(img, transform = ccrs.Mercator.GOOGLE, extent = extent, origin = 'upper')

# Draw grid.
gl = ax.gridlines(ccrs.PlateCarree(), linewidth = 1, color = 'blue', alpha = 0.3,  draw_labels = True)
gl.top_labels = False
gl.right_labels = False
gl.xlines = True
gl.ylines = True
gl.xlocator = mticker.FixedLocator([0, 30, -30, 0])
gl.ylocator = mticker.FixedLocator([-30, 0, 30])
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
gl.xlabel_style = {'color': 'blue'}
gl.ylabel_style = {'color': 'blue'}

plt.title('WMS Landsat Reflectance In Web Mercator Projection',
          fontname = "Times New Roman", fontsize = 20, color = 'green')

plt.show()

print('')