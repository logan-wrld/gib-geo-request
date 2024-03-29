import shutil
import os

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
source_folder = 'converted'  # Replace with the path to your converted folder
target_folder = '/Volumes/CIRCUITPY/images'  # Replace with the mounted path of your ESP32
file_name = 'converted.bmp'  # Replace with your BMP file name

# Move the file
move_bmp_to_esp32(source_folder, target_folder, file_name)
