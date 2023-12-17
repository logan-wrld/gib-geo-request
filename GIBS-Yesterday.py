import os
import datetime
from owslib.wms import WebMapService
from skimage import io
import shutil
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

# Save the raw PNG image
output_dir = 'images'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
png_output_file = os.path.join(output_dir, 'MODIS_Terra_TrueColor_Texas.png')
with open(png_output_file, 'wb') as out_file:
    out_file.write(img_response.read())

# Read the image data for display and BMP conversion
img_data = io.imread(png_output_file)


# Convert the NumPy array to a Pillow Image for BMP saving
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

def move_bmp_to_esp32(source_folder, target_folder, file_name):
    source_path = os.path.join(source_folder, file_name)
    target_path = os.path.join(target_folder, file_name)

    try:
        # Move the file
        shutil.move(source_path, target_path)
        print(f"File '{file_name}' moved from '{source_folder}' to '{target_folder}'.")
    except FileNotFoundError:
        print(f"File '{file_name}' not found in '{source_folder}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Define the source and target folders and the filename
source_folder = 'images'  # Replace with the path to your converted folder
target_folder = '/Volumes/CIRCUITPY/images'  # Replace with the mounted path of your ESP32
file_name = 'MODIS_Terra_TrueColor_Texas.bmp'  # Replace with your BMP file name

# Move the file
move_bmp_to_esp32(source_folder, target_folder, file_name)
