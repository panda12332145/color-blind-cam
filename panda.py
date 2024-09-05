import tkinter as tk
from PIL import Image, ImageTk

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
        print(f"Error: {e}")
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

def display_image(image):
    root = tk.Tk()
    root.title("imagem.panda")
    
    img_tk = ImageTk.PhotoImage(image)
    label = tk.Label(root, image=img_tk)
    label.pack()
    
    root.mainloop()

def main():
    panda_path = 'imagem.panda'
    
    hex_colors, width, height = read_panda_file(panda_path)
    
    if hex_colors:
        img = create_image_from_hex(hex_colors, width, height)
        display_image(img)
    else:
        print("Failed to read or interpret .panda file.")

if __name__ == "__main__":
    main()
