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


wms = WebMapService('https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?', version='1.1.1')

# Configure request for MODIS_Terra_CorrectedReflectance_TrueColor
# Adjusting bbox to the coordinates of Texas, USA
texas_bbox = (-106.65, 25.84, -93.51, 36.5)  # Bounding box for Texas

img = wms.getmap(layers=['MODIS_Terra_CorrectedReflectance_TrueColor'],  # Layers
                 srs='epsg:4326',  # Map projection
                 bbox=texas_bbox,  # Bounds for Texas
                 size=(250, 250),  # Image size
                 time='2023-12-13',  # Time of data
                 format='image/png',  # Image format
                 transparent=True)  # Nodata transparency

# Ensure the directory exists
output_dir = 'images'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save output PNG to a file
output_file = os.path.join(output_dir, 'MODIS_Terra_TrueColor_Texas.png')
with open(output_file, 'wb') as out:
    out.write(img.read())

# View image
Image(output_file)