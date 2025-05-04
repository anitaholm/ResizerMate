import os
import sys
from PIL import Image

def size_to_str(width, height):
    ISO_sizes = {
        (33.1,46.8): "A0",
        (23.4,33.1): "A1", 
        (16.5,23.4): "A2", 
        (11.7,16.5): "A3", 
        (8.3,11.7): "A4", 
        (5.8,8.3): "A5",
    }
    if (width,height) in ISO_sizes:
        return ISO_sizes[(width,height)]
    else:
        return f"{width}x{height}"

def resize_and_save(image, width, height, dpi, output_path, base_name, format):
    size_pixels = (int(width*dpi), int(height*dpi))
    resized = image.copy()
    resized = resized.resize(size_pixels, Image.LANCZOS)
    size_str = size_to_str(width, height)
    file_path = os.path.join(output_path, f"{base_name}_{size_str}.{format}")
    resized.save(file_path, dpi=(dpi,dpi))
    print("Saved:", file_path)

def main(input_image_path, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    base_name = os.path.splitext(os.path.basename(input_image_path))[0]
    image = Image.open(input_image_path)

    dpi = 300

    sizes = {
        "2:3": [(20,30), (16,24), (12,18), (8,12), (4,6)],
        "4:5": [(16,20), (8,10), (4,5)],
        "ISO": [(33.1,46.8), (23.4,33.1), (16.5,23.4), (11.7,16.5), (8.3,11.7), (5.8,8.3)],
        "11x4": [(11,14)],
    }

    for ratio, size_list in sizes.items():
        for size in size_list:
            for fmt in ["png", "jpg"]:
                resize_and_save(image, size[0], size[1], dpi, output_path, base_name, fmt)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_image_path> <output_folder>")
        sys.exit(1)

input_image_path = sys.argv[1]
output_path = sys.argv[2]
main(input_image_path, output_path)
    