import os
import datetime
from owslib.wms import WebMapService
from skimage import io
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from PIL import Image
from io import BytesIO  # Import BytesIO

# Initialize WMS service
wms = WebMapService('https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?', version='1.1.1')

# Get the date from two days ago
two_days_ago = (datetime.date.today() - datetime.timedelta(days=2)).strftime("%Y-%m-%d")

# Configure request for MODIS Terra Corrected Reflectance, adjusting to the coordinates of Texas, USA
texas_bbox = (-106.65, 25.84, -93.51, 36.5)  # Bounding box for Texas

# Request image
img_response = wms.getmap(layers=['MODIS_Terra_CorrectedReflectance_TrueColor'], 
                          srs='epsg:4326', 
                          bbox=texas_bbox, 
                          size=(250, 250), 
                          time=two_days_ago, 
                          format='image/png', 
                          transparent=True)

# Read the image data directly from the response
img_data = io.imread(BytesIO(img_response.read()))

# Check if image data is loaded correctly
if img_data.ndim < 2:
    print("Loaded image data is not in expected format.")
    exit()

# Save the image
output_dir = 'images'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
output_file = os.path.join(output_dir, 'MODIS_Terra_TrueColor_Texas_geo.png')
with open(output_file, 'wb') as out_file:
    out_file.write(img_data)

# Display the image
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.set_extent([-106.65, -93.51, 25.84, 36.5], crs=ccrs.PlateCarree())
plt.imshow(img_data, transform=ccrs.PlateCarree(), extent=[-106.65, -93.51, 25.84, 36.5], origin='upper')
plt.show()
# ... [rest of your script] ...

# Display the image
# ... [Matplotlib code for displaying the image] ...

# Convert the NumPy array to a Pillow Image
# Ensure img_data is in RGB format
if img_data.ndim == 2:  # if the image is grayscale
    pil_img = Image.fromarray(img_data, mode='L')
elif img_data.shape[2] == 4:  # if the image has an alpha channel
    pil_img = Image.fromarray(img_data[:, :, :3], mode='RGB')
else:
    pil_img = Image.fromarray(img_data, mode='RGB')

# Save the image in BMP format
bmp_output_file = os.path.join(output_dir, 'MODIS_Terra_TrueColor_Texas.bmp')
pil_img.save(bmp_output_file, format='BMP')

print(f"Image saved as {bmp_output_file}")
