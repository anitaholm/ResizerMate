import os
import sys
import zipfile
from PIL import Image, ImageDraw, ImageFont

def crop_to_ratio(image, ratio):
    width, height = image.size
    img_ratio = width / height
    if img_ratio > ratio:
        # image is wider than the ratio
        new_width = int(height * ratio)
        offset = (width - new_width) // 2
        box = (offset, 0, offset + new_width, height)
    else:
        # image is taller than the ratio
        new_height = int(width / ratio)
        offset = (height - new_height) // 2
        box = (0, offset, width, offset + new_height)

    return image.crop(box)

def add_watermark(image, text="Sample"):
    watermark = image.copy()
    draw = ImageDraw.Draw(watermark)
    width, height = watermark.size

    try:
        font = ImageFont.truetype("arial.ttf", int(height/20))
    except IOError:
        font = ImageFont.load_default()

    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:4]
    position = (width - text_width - 10, height - text_height - 10)
    draw.text(position, text, fill=(255, 255, 255, 128), font=font)
    return watermark

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

def resize_and_save(image, width, height, dpi, output_path, base_name, format, ratio, watermark_text=None):
    size_pixels = (int(width*dpi), int(height*dpi))
    target_ratio = width / height

    cropped_image = crop_to_ratio(image, target_ratio)
    resized = cropped_image.resize(size_pixels, Image.LANCZOS)

    if watermark_text:
        resized = add_watermark(resized, watermark_text)
    
    ratio_folder = os.path.join(output_path, ratio.replace(":", "x"))
    if not os.path.exists(ratio_folder):
        os.makedirs(ratio_folder)
    
    size_str = size_to_str(width, height)
    file_path = os.path.join(ratio_folder, f"{base_name}_{size_str}.{format}")
    resized.save(file_path, dpi=(dpi,dpi))
    print("Saved:", file_path)

def process_image(input_image_path, output_path, watermark_text):
    base_name = os.path.splitext(os.path.basename(input_image_path))[0]
    image = Image.open(input_image_path)

    dpi = 300

    sizes = {
        #"2:3": [(20,30), (16,24), (12,18), (8,12), (4,6)],
        #"4:5": [(16,20), (8,10), (4,5)],
        #"ISO": [(33.1,46.8), (23.4,33.1), (16.5,23.4), (11.7,16.5), (8.3,11.7), (5.8,8.3)],
        "11x4": [(11,14)],
    }

    for ratio, size_list in sizes.items():
        for size in size_list:
            for fmt in ["png", "jpg"]:
                resize_and_save(image, size[0], size[1], dpi, output_path, base_name, fmt, ratio, watermark_text)

def zip_output_folder(output_path):
    zip_filename = os.path.join(output_path, "processed_images.zip")
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(output_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, output_path))

def main(input_path, output_path, watermark_text=None):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if os.path.isfile(input_path):
        process_image(input_path, output_path, watermark_text)
    elif os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            print("Processing:", filename)
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', 'tiff', 'bmp', 'gif')):
                file_path = os.path.join(input_path, filename)
                process_image(file_path, output_path, watermark_text)

    zip_output_folder(output_path)
    print("All images processed and saved to:", output_path)

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python script.py <input_image_or_folder> <output_folder> [watermark_text]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    watermark_text = sys.argv[3] if len(sys.argv) == 4 else None
    
    main(input_path, output_path, watermark_text)