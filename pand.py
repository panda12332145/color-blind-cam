import sys
import tkinter as tk
from PIL import Image, ImageTk
import os

def hex_to_rgba(hex_str):
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4, 6))

def read_panda_file(panda_path):
    try:
        with open(panda_path, 'r') as file:
            lines = file.read().strip().split('\n')
            hex_colors = [line[i:i+8] for line in lines for i in range(0, len(line), 8)]
            width = len(lines[0]) // 8
            height = len(lines)
            return hex_colors, width, height
    except Exception as e:
        print(f"Error reading .panda file: {e}")
        return None, 0, 0

def create_image_from_hex(hex_colors, width, height):
    img = Image.new('RGBA', (width, height))
    pixels = img.load()
    
    for y in range(height):
        for x in range(width):
            hex_color = hex_colors[y * width + x]
            rgba = hex_to_rgba(hex_color)
            pixels[x, y] = rgba
            
    return img

def display_image(image, title):
    root = tk.Tk()
    root.title(title)
    
    img_tk = ImageTk.PhotoImage(image)
    label = tk.Label(root, image=img_tk)
    label.pack()
    
    root.mainloop()

def main():
    if len(sys.argv) < 2:
        print("Usage: drag and drop a .panda file onto this script.")
        sys.exit(1)
    
    panda_path = sys.argv[1]
    
    if not os.path.isfile(panda_path):
        print(f"File does not exist: {panda_path}")
        sys.exit(1)

    print(f"Opening file: {panda_path}")  # Debug message

    hex_colors, width, height = read_panda_file(panda_path)
    
    if hex_colors:
        img = create_image_from_hex(hex_colors, width, height)
        display_image(img, os.path.basename(panda_path))
    else:
        print("Failed to read or interpret .panda file.")

if __name__ == "__main__":
    main()
