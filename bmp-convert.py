from PIL import Image

def convert_png_to_bmp(source_path, target_path):
    try:
        # Open the source image
        with Image.open(source_path) as img:
            # Resize the image to 250x250 using LANCZOS resampling (formerly ANTIALIAS)
            img = img.resize((250, 250), Image.Resampling.LANCZOS)
            
            # Save the image in BMP format
            img.save(target_path, 'BMP')

        print(f"Image converted and saved as '{target_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")

# Replace 'path/to/source.png' with the path to your PNG file
# Replace 'path/to/target.bmp' with the path where you want to save the BMP file
convert_png_to_bmp('images/MODIS_Terra_TrueColor_Texas2.png', 'converted/converted.bmp')
