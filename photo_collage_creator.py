#!/usr/bin/env python
""" filename: photo_collage_creator.py
Collage Maker Script

This script creates a square collage from images in a specified folder.

Testing using: 
    !python photo_collage_creator.py --debug --input img --filename test.png --remove 2 --size 200

Usage:
    collage_maker.py [--input FOLDER_PATH] [--filename FILENAME] [--remove ROWS] [--size COLLAGE_SIZE] [--debug]

Options:
    --input FOLDER_PATH     Path to folder containing images [default: img].
    --filename FILENAME     Output filename [default: collage.jpg].
    --remove ROWS           Number of rows to remove from the bottom of the collage [default: 2].
    --size COLLAGE_SIZE     Size of each image in the collage in pixels [default: 400].
    --debug                 Enable debug logging.

"""

#%%
# Import required libraries
from PIL import Image, ExifTags
import os
import sys
import logging
from logging import info

def main(args):
    """
    Main function to create a photo collage.
    :param args: List of arguments passed to the script.
    """
    # Configure logging for debug mode
    if ("--debug" in args) or ("-d" in args):
        logging.basicConfig(format="[%(levelname)s] %(message)s")
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        info("mode Debug On")

    # Check for input folder argument
    if "--input" in sys.argv:
        index = sys.argv.index("--input") + 1
        folder_path = str(sys.argv[index])
        info("Using --input: " + folder_path)
    else:
        folder_path = "img"
        info("No input folder specified. Using default: " + folder_path)
    
    # Check for output filename argument
    if "--filename" in sys.argv:
        index = sys.argv.index("--filename") + 1
        output_filename = str(sys.argv[index])
        info("Using output filename: " + output_filename)
    else:
        output_filename = "collage.jpg"
        info("No output filename specified. Using default: " + output_filename)
        

    # Check for number of rows to remove argument
    if "--remove" in sys.argv:
        index = sys.argv.index("--remove") + 1
        remove_row = int(sys.argv[index])
        info("Removing " + str(remove_row) + " last rows.")
    else:
        remove_row = 2
        info("No number of rows to remove specified. Using default: " + str(remove_row))
    
    # Check for collage size argument
    if "--size" in sys.argv:
        index = sys.argv.index("--size") + 1
        collage_size = int(sys.argv[index])
        info("Using collage size: " + str(collage_size))
    else:
        collage_size = 400
        info("No collage size specified. Using default: " + str(collage_size))

    # Get a list of all the images in the input folder
    images = [f for f in os.listdir(folder_path) if f.endswith('.jpg') or f.endswith('.png')]

    # Calculate the number of rows and columns needed for the collage
    num_images = len(images)
    num_cols = int(num_images ** 0.5)
    num_rows = num_images // num_cols + (1 if num_images % num_cols else 0)

    # Adjust the size of the collage canvas to make it square
    max_dim = max(num_cols, num_rows) * collage_size
    collage = Image.new('RGB', (max_dim, max_dim), (0, 0, 0))

    info("")
	# Insertar cada imagen en el collage
    for i, filename in enumerate(images):
        info("Processing " + str(i) + " of " + str(num_images))
        # Abrir la imagen y redimensionarla si es necesario
        with Image.open(os.path.join(folder_path, filename)) as img:
            # Rotar la imagen según su orientación exif
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation]=='Orientation':
                    break
            try:
                exif=dict(img._getexif().items())
                if exif[orientation] == 3:
                    img=img.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    img=img.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    img=img.rotate(90, expand=True)
            except (AttributeError, KeyError, IndexError):
                # No se encontró la orientación exif, no hacer nada
                pass
            info("Resize, Crop")
            # Calcular las dimensiones de la imagen recortada
            aspect_ratio = img.width / img.height
            if aspect_ratio >= 1:
                crop_width = int(img.height * (collage_size / collage_size))
                crop_height = img.height
            else:
                crop_width = img.width
                crop_height = int(img.width * (collage_size / collage_size))
            # Realizar el crop desde el centro de la imagen
            left = (img.width - crop_width) // 2
            top = (img.height - crop_height) // 2
            right = left + crop_width
            bottom = top + crop_height
            img_cropped = img.crop((left, top, right, bottom))
            # Redimensionar la imagen al tamaño del collage
            img_resized = img_cropped.resize((collage_size, collage_size), Image.LANCZOS)
            
            info("Insert image on collage")
            # Insertar la imagen en el collage
            row = i // num_cols
            col = i % num_cols
            x = row * collage_size
            y = col * collage_size
            collage.paste(img_resized, (x ,y))

            # Eliminar las filas negras si no se agregaron imágenes en la última fila

    info("Remove " + str(remove_row) + " last rows")

    if num_images % num_cols != 0:
        collage = collage.crop((0, 0, max_dim, num_rows * collage_size))
    collage = collage.crop((0, 0, max_dim, (num_rows - remove_row) * collage_size))


    # Guardar el collage
    info("Saving collage on file:" + output_filename)
    collage.save(output_filename)
    info("Program finished")

if __name__ == "__main__":
    main(sys.argv[1:])

# %%
