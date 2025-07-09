import os
import sys
import zipfile
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

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
        # Vertical (portrait) ISO sizes
        (33.1,46.8): "A0",
        (23.4,33.1): "A1", 
        (16.5,23.4): "A2", 
        (11.7,16.5): "A3", 
        (8.3,11.7): "A4", 
        (5.8,8.3): "A5",
        # Horizontal (landscape) ISO sizes
        (46.8,33.1): "A0",
        (33.1,23.4): "A1", 
        (23.4,16.5): "A2", 
        (16.5,11.7): "A3", 
        (11.7,8.3): "A4", 
        (8.3,5.8): "A5",
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

def process_image(input_image_path, output_path, watermark_text, progress_callback=None):
    base_name = os.path.splitext(os.path.basename(input_image_path))[0]
    image = Image.open(input_image_path)

    dpi = 300

    # Detect image orientation
    width, height = image.size
    is_vertical = height > width

    # Define sizes for vertical (portrait) images
    vertical_sizes = {
        "2:3": [(20,30), (16,24), (12,18), (8,12), (4,6)],
        "4:5": [(16,20), (8,10), (4,5)],
        "ISO": [(33.1,46.8), (23.4,33.1), (16.5,23.4), (11.7,16.5), (8.3,11.7), (5.8,8.3)],
        "11x14": [(11,14)],
    }

    # Define sizes for horizontal (landscape) images
    horizontal_sizes = {
        "3:2": [(30,20), (24,16), (18,12), (12,8), (6,4)],
        "5:4": [(20,16), (10,8), (5,4)],
        "ISO": [(46.8,33.1), (33.1,23.4), (23.4,16.5), (16.5,11.7), (11.7,8.3), (8.3,5.8)],
        "14x11": [(14,11)],
    }

    # Choose appropriate sizes based on image orientation
    sizes = vertical_sizes if is_vertical else horizontal_sizes

    total = len(sizes) * 2 * len(next(iter(sizes.values())))
    count = 0

    for ratio, size_list in sizes.items():
        for size in size_list:
            for fmt in ["png", "jpg"]:
                resize_and_save(image, size[0], size[1], dpi, output_path, base_name, fmt, ratio, watermark_text)
                count += 1
                if progress_callback:
                    progress_callback(count/total * 100)

def zip_output_folder(output_path):
    zip_filename = os.path.join(output_path, "processed_images.zip")
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(output_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, output_path))

def run_processing(input_path, output_path, watermark_text=None, progress_callback=None):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    image_files = []
    if os.path.isfile(input_path):
        image_files = [input_path]
    elif os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', 'tiff', 'bmp', 'gif')):
                image_files.append(os.path.join(input_path, filename))
    else:
        messagebox.showerror("Error", "Invalid input path. Please select a valid image file or folder.")
        return
    
    total_files = len(image_files)
    for idx, img_path in enumerate(image_files):
        process_image(img_path, output_path, watermark_text, progress_callback)

    zip_output_folder(output_path)
    messagebox.showinfo("Done", f"All images processed and saved to {output_path}. Output zipped as 'processed_images.zip'.")

def select_input():
    path = filedialog.askopenfilename(
        title="Select an image file",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.tiff;*.bmp;*.gif")]
    )
    if not path:
        path = filedialog.askdirectory(title="Select a folder with images")
    return path

def select_output():
    return filedialog.askdirectory(title="Select output folder")

def start_gui():
    root = tk.Tk()
    root.title("ResizerMate")
    root.geometry("500x400")

    input_path = tk.StringVar()
    output_path = tk.StringVar()
    watermark_text = tk.StringVar()

    def browse_input():
        path = filedialog.askopenfilename(title="Select an image file")
        if not path:
            path = filedialog.askdirectory(title="Or select a folder with images")
        input_path.set(path)

    def browse_output():
        path = filedialog.askdirectory(title="Select a folder with images")
        output_path.set(path)

    def start_processing():
        if not input_path.get() or not output_path.get():
            messagebox.showerror("Error", "Please select both input and output paths.")
            return

        progress_bar['value'] = 0
        run_processing(input_path.get(), output_path.get(), watermark_text.get(), update_progress)

    def update_progress(val):
        progress_bar['value'] = val
        root.update_idletasks()
        
    tk.Label(root, text="Welcome to ResizerMate!", font=("Helvetica", 18)).pack(pady=10)

    tk.Button(root, text="Select Input Image/Folder", command=browse_input).pack(pady=5)
    tk.Entry(root, textvariable=input_path, width=60).pack(pady=5)

    tk.Button(root, text="Select Output Folder", command=browse_output).pack(pady=5)
    tk.Entry(root, textvariable=output_path, width=60).pack(pady=5)

    tk.Label(root, text="Watermark Text (optional):").pack(pady=5)
    tk.Entry(root, textvariable=watermark_text, width=40).pack(pady=5)

    tk.Button(root, text="Start Processing", command=start_processing, height=2, width=20).pack(pady=20)

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode='determinate')
    progress_bar.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    start_gui()
