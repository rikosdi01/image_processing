import cv2
import torch
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
from torchvision import transforms
from matplotlib import pyplot as plt

# --- LOGIKA DEEPLAB (TETAP SAMA) ---
def load_model():
    # Menggunakan weights terbaru sesuai anjuran warning di terminal Anda
    model = torch.hub.load('pytorch/vision', 'deeplabv3_resnet101', weights='DeepLabV3_ResNet101_Weights.DEFAULT')
    model.eval()
    return model

def make_transparent_foreground(pic, mask):
    b, g, r = cv2.split(np.array(pic).astype('uint8'))
    a = np.ones(mask.shape, dtype='uint8') * 255
    alpha_im = cv2.merge([b, g, r, a], 4)
    bg = np.zeros(alpha_im.shape)
    new_mask = np.stack([mask, mask, mask, mask], axis=2)
    foreground = np.where(new_mask, alpha_im, bg).astype(np.uint8)
    return foreground

def remove_background(model, input_image):
    preprocess = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = preprocess(input_image).unsqueeze(0)
    if torch.cuda.is_available():
        input_tensor = input_tensor.cuda()
        model = model.cuda()

    with torch.no_grad():
        output = model(input_tensor)['out'][0]

    # Gunakan probabilitas foreground total agar lebih robust
    probs = torch.softmax(output, dim=0)
    fg_prob = 1 - probs[0]   # semua kelas kecuali background
    mask = (fg_prob > 0.5).cpu().numpy().astype(np.uint8) * 255

    foreground = make_transparent_foreground(input_image, mask)
    return foreground

# --- LOGIKA GUI ---
def open_and_process():
    file_path = filedialog.askopenfilename(
        title="Select Image for Background Removal",
        filetypes=[("Image files", "*.jpg *.jpeg *.png")]
    )
    
    if file_path:
        try:
            lbl_status.config(text="Processing image with DeepLabV3+...", fg="blue")
            root.update()
            
            # Load & Process
            input_image = Image.open(file_path).convert("RGB")
            result_np = remove_background(deeplab_model, input_image)
            
            # Konversi hasil ke format yang bisa ditampilkan Tkinter
            result_img = Image.fromarray(result_np)
            result_img.thumbnail((400, 400)) # Resize untuk preview
            img_tk = ImageTk.PhotoImage(result_img)
            
            panel.configure(image=img_tk)
            panel.image = img_tk
            
            lbl_status.config(text="Success! Background removed.", fg="green")
            
            # Opsi simpan hasil
            if messagebox.askyesno("Save Result", "Do you want to save the result as PNG?"):
                save_path = filedialog.asksaveasfilename(defaultextension=".png")
                if save_path:
                    Image.fromarray(result_np).save(save_path)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image: {e}")
            lbl_status.config(text="Ready", fg="black")

# --- INITIALIZATION ---
print("Loading DeepLab Model...")
deeplab_model = load_model()

# UI Setup
root = tk.Tk()
root.title("AI Background Remover (DeepLabV3+)")
root.geometry("500x600")

tk.Label(root, text="Semantic Segmentation R&D", font=("Arial", 14, "bold")).pack(pady=10)

btn_select = tk.Button(root, text="Select Image", command=open_and_process, 
                       bg="#0078d4", fg="white", padx=20, pady=10)
btn_select.pack(pady=20)

panel = tk.Label(root, text="Preview will appear here")
panel.pack(pady=10)

lbl_status = tk.Label(root, text="Ready", font=("Arial", 10))
lbl_status.pack(side="bottom", pady=20)

root.mainloop()