import os
import sys
from PIL import Image

def resize_and_save(image, width, height, dpi, output_path, base_name, format):
    size_pixels = (int(width*dpi), int(height*dpi))
    resized = image.copy()
    resized = resized.resize(size_pixels, Image.LANCZOS)
    file_path = os.path.join(output_path, base_name + "_" + str(width) + "x" + str(height) + "." + format)
    resized.save(file_path, format=format.upper(), dpi=(dpi,dpi))
    print("Saved:", file_path)

def main(input_image_path, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    base_name = os.path.splitext(os.path.basename(input_image_path))[0]
    image = Image.open(input_image_path)

    resize_and_save(image, 20, 30, 300, output_path, base_name, "png")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_image_path> <output_folder>")
        sys.exit(1)

input_image_path = sys.argv[1]
output_path = sys.argv[2]
main(input_image_path, output_path)
    