# Photo Collage Creator
This script creates a square collage from images in a specified folder.

## Usage

```bash
collage_maker.py [--input FOLDER_PATH] [--filename FILENAME] [--remove ROWS] [--size COLLAGE_SIZE] [--debug]
```

## Options
- `--input FOLDER_PATH`: Path to the folder containing images. Default value: img.
- `--filename FILENAME`: Output filename. Default value: collage.jpg.
- `--remove ROWS`: Number of rows to remove from the bottom of the collage. Default value: 2.
- `--size COLLAGE_SIZE`: Size of each image in the collage in pixels. Default value: 400.
- `--debug`: Enable debug logging.

## Example
To create a collage with images from the `img` folder, remove 2 rows from the bottom, use a collage size of 200 pixels, and save the output as test.png, run the following command:

```bash
python photo_collage_creator.py --debug --input img --filename test.png --remove 2 --size 200
```
##  Requirements
This script requires the following Python libraries to be installed:

- Pillow


## TODO and Limitations

- Actually, at the end of collage creation add two black rows. The command `--remove` delete a specific length of rows. 
- Add other shapes of collage, i.e.: circles, rectangles, hearts, etc.
- Resize the final collage and specific size.

## License
This script is released under the MIT License. See LICENSE file for more details.