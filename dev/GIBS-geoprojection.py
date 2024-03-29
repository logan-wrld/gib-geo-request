import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from skimage import io
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import datetime
import ssl

# Create an unverified SSL context
ssl._create_default_https_context = ssl._create_unverified_context

# Get yesterday's date in the format YYYY-MM-DD
yesterday = (datetime.date.today() - datetime.timedelta(days=2)).strftime("%Y-%m-%d")

# Construct global image URL.
#  Construct Geographic projection URL.
proj4326 = 'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?\
version=1.3.0&service=WMS&\
request=GetMap&format=image/png&STYLE=default&bbox=-40,-40,40,40&CRS=EPSG:4326&\
HEIGHT=600&WIDTH=600&TIME=2000-12-01&layers=Landsat_WELD_CorrectedReflectance_Bands157_Global_Annual'

# Request image.
img = io.imread(proj4326)

# Display image on map.
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
extent = (-40, 40, -40, 40)
plt.imshow(img, transform = ccrs.PlateCarree(), extent = extent, origin = 'upper')

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

plt.title('WMS Landsat Reflectance In Geographic Projection',\
          fontname = "Times New Roman", fontsize = 20, color = 'green')

plt.show()

print('')