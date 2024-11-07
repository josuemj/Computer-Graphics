

import sys
from PIL import Image  # Ensure Pillow is installed

processed = False

def process_image(image_path):
    img = Image.open(image_path)
    size = img.size[0] // 3  # Expecting a 3x2 layout
    split_and_save(img, 0, 0, size, add_to_filename(image_path, "_right"))
    split_and_save(img, size, 0, size, add_to_filename(image_path, "_back"))
    split_and_save(img, size * 2, 0, size, add_to_filename(image_path, "_left"))
    split_and_save(img, 0, size, size, add_to_filename(image_path, "_down"))
    split_and_save(img, size, size, size, add_to_filename(image_path, "_up"))
    split_and_save(img, size * 2, size, size, add_to_filename(image_path, "_front"))

def add_to_filename(name, suffix):
    parts = name.rsplit('.', 1)
    return f"{parts[0]}{suffix}.{parts[1]}" if len(parts) > 1 else name + suffix

def split_and_save(img, start_x, start_y, size, output_name):
    area = (start_x, start_y, start_x + size, start_y + size)
    save_image(img.crop(area), output_name)

def save_image(img, name):
    try:
        img.save(name)
        print(f"Saved {name}")
    except Exception as e:
        print(f"* ERROR: Could not save image {name}: {e}")

# Main processing based on command-line arguments
for arg in sys.argv[1:]:
    if arg.lower().endswith((".png", ".jpg")):
        process_image(arg)
        processed = True

if not processed:
    print("* ERROR: No Image provided")
    print("Usage: 'python script.py image-name.png'")
