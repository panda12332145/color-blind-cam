import cv2
import numpy as np
from PIL import Image, ImageTk
import datetime
import uuid
import json
import platform
import tempfile
import os
import tkinter as tk
from tkinter import messagebox

def apply_deuteranopia_filter(image):
    """Aplica um filtro de cores para deuteranomalia."""
    img_array = np.array(image)
    correction_matrix = np.array([
        [0.4002, 0.7075, -0.0808],
        [0.1423, 0.9293, -0.0716],
        [-0.0088, 0.0000, 1.0088]
    ])
    img_array = np.dot(img_array[..., :3], correction_matrix.T).clip(0, 255).astype(np.uint8)
    return Image.fromarray(np.dstack((img_array, np.array(image)[..., 3])))

def rgba_to_hex(rgba):
    return '{:02x}{:02x}{:02x}{:02x}'.format(rgba[0], rgba[1], rgba[2], rgba[3])

def process_image(cv_image):
    """Processa a imagem capturada pela câmera."""
    img = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGBA))
    img = apply_deuteranopia_filter(img)
    
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
    
    return img, hex_string

def save_image_and_metadata(image, hex_string):
    now = datetime.datetime.now()
    os_prefix = {
        'nt': 'WIN',  # Windows
        'posix': 'LINU'  # Linux/Mac
    }.get(os.name, 'OTHR')  # Outros sistemas operacionais
    timestamp = now.strftime(f'{os_prefix}_%Y-%m-%d_%H-%M-%S')
    unique_id = str(uuid.uuid4())
    png_file_name = f"{timestamp}_{unique_id}.png"
    panda_file_name = f"{timestamp}_{unique_id}.panda"
    metadata_file_name = f"{timestamp}_{unique_id}_metadata.json"
    
    # Criar arquivos temporários
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png", mode='w+b') as temp_png_file:
        png_file_name = temp_png_file.name
        image.save(png_file_name)
        print(f"Image saved to {png_file_name}")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w') as temp_metadata_file:
        metadata_file_name = temp_metadata_file.name
        metadata = {
            'timestamp': now.isoformat(),
            'unique_id': unique_id,
            'device': platform.node(),
            'os': platform.system() + " " + platform.release(),
            'location': 'Not available',
        }
        json.dump(metadata, temp_metadata_file, indent=4)
        print(f"Metadata saved to {metadata_file_name}")
    
    # Salva a string hexadecimal em um arquivo .panda
    with open(panda_file_name, 'w') as panda_file:
        panda_file.write(hex_string)
    print(f"Hex string saved to {panda_file_name}")
    
    # Remover arquivos temporários
    os.remove(png_file_name)
    os.remove(metadata_file_name)
    print("Temporary files removed.")

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera App")
        self.root.geometry("800x480")  # Ajuste o tamanho da janela para acomodar o botão
        
        self.camera = cv2.VideoCapture(0)
        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack(side=tk.LEFT)
        
        # Criação do botão circular vermelho
        self.button_frame = tk.Frame(root, width=160, height=480)
        self.button_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.button_canvas = tk.Canvas(self.button_frame, width=160, height=480, bg="white", bd=0, highlightthickness=0)
        self.button_canvas.pack()
        self.button_canvas.create_oval(20, 200, 140, 320, fill="red", outline="red")
        self.button_canvas.bind("<Button-1>", self.capture_photo)
        
        self.update_frame()
    
    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.root.after(10, self.update_frame)
    
    def capture_photo(self, event=None):
        ret, frame = self.camera.read()
        if ret:
            img, hex_string = process_image(frame)
            save_image_and_metadata(img, hex_string)
            messagebox.showinfo("Info", "Foto tirada e salva com sucesso!")
        else:
            messagebox.showerror("Error", "Não foi possível capturar a foto.")

    def __del__(self):
        self.camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()
