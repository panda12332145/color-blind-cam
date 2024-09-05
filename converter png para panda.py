from PIL import Image

def rgba_to_hex(rgba):
    return '{:02x}{:02x}{:02x}{:02x}'.format(rgba[0], rgba[1], rgba[2], rgba[3])

def analyze_image(image_path):
    try:
        with Image.open(image_path) as img:
            img = img.convert('RGBA')
            width, height = img.size
            hex_lines = []
            
            for y in range(height):
                hex_colors = []
                for x in range(width):
                    rgba = img.getpixel((x, y))
                    hex_color = rgba_to_hex(rgba)
                    hex_colors.append(hex_color)
                hex_line = ''.join(hex_colors)
                hex_lines.append(hex_line)
            
            hex_string = '\n'.join(hex_lines)
            return hex_string
    except Exception as e:
        print(f"Error: {e}")
        return None

def save_hex_string(hex_string, output_path):
    try:
        with open(output_path, 'w') as file:
            file.write(hex_string)
    except Exception as e:
        print(f"Error: {e}")

def main():
    image_path = 'imagem.png'
    output_path = 'imagem.panda'
    
    hex_string = analyze_image(image_path)
    
    if hex_string:
        save_hex_string(hex_string, output_path)
        print(f"Hex string saved to {output_path}")
    else:
        print("Failed to analyze image.")

if __name__ == "__main__":
    main()
