from PIL import Image, ImageTk
import os
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from rembg import remove

def convert_images(input_folder, output_folder, output_format="original", watermark_path=None, position=None, transparency=None, custom_width=None, custom_height=None, remove_bg=False, bg_color=(255, 255, 255), apply_bg=False):
    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(input_folder, filename)
            img = Image.open(img_path).convert("RGBA")

            # Remove background if selected
            if remove_bg:
                img = remove(img)
                if apply_bg:
                    bg_layer = Image.new("RGBA", img.size, bg_color + (255,))
                    img = Image.alpha_composite(bg_layer, img)

            # Add watermark if specified
            if watermark_path and position:
                img = add_watermark(img, watermark_path, position, transparency, custom_width, custom_height)

            # Define output file name and format
            if output_format == "WebP":
                output_filename = os.path.splitext(filename)[0] + ".webp"
                output_path = os.path.join(output_folder, output_filename)
                img = img.convert("RGB")  # Convert to RGB to handle transparency correctly
                img.save(output_path, "WEBP", quality=70)
            elif output_format == "JPEG":
                output_filename = os.path.splitext(filename)[0] + ".jpeg"  # Use .jpeg extension
                output_path = os.path.join(output_folder, output_filename)
                img.convert("RGB").save(output_path, "JPEG", quality=85)  # Set quality to 85 for balanced file size
            elif output_format == "PNG":
                output_filename = os.path.splitext(filename)[0] + ".png"  # Use .png extension
                output_path = os.path.join(output_folder, output_filename)
                img.save(output_path, "PNG", optimize=True)  # Optimize PNG images
            else:
                # Use original extension
                output_filename = filename
                output_path = os.path.join(output_folder, output_filename)
                if img.mode == "RGBA" and output_filename.lower().endswith((".jpg", ".jpeg")):
                    img = img.convert("RGB")
                if output_filename.lower().endswith(".png"):
                    img.save(output_path, "PNG", optimize=True)  # Optimize PNG images
                else:
                    img.save(output_path, quality=85)  # Set quality to 85 for JPEG and WebP

            print(f"{filename} converted to {output_filename} with watermark and background removed.")
            
def add_watermark(image, watermark_path, position, transparency=1.0, custom_width=None, custom_height=None):
    # Load the watermark image
    watermark = Image.open(watermark_path).convert("RGBA")

    # Resize watermark if custom dimensions are provided
    if custom_width and custom_height:
        watermark = watermark.resize((custom_width, custom_height), Image.LANCZOS)
    else:
        base_width, base_height = image.size
        watermark_width, watermark_height = watermark.size
        scale = 0.1
        new_width = int(base_width * scale)
        new_height = int((new_width / watermark_width) * watermark_height)
        watermark = watermark.resize((new_width, new_height), Image.LANCZOS)

    # Create a transparent layer to hold the watermark
    transparent_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    
    # Calculate position to place the watermark
    if position == "top left":
        x, y = 10, 10
    elif position == "top right":
        x, y = image.width - watermark.width - 10, 10
    elif position == "center":
        x, y = (image.width - watermark.width) // 2, (image.height - watermark.height) // 2
    elif position == "bottom left":
        x, y = 10, image.height - watermark.height - 10
    elif position == "bottom right":
        x, y = image.width - watermark.width - 10, image.height - watermark.height - 10

    # Apply transparency to the watermark
    watermark = watermark.convert("RGBA")
    alpha = watermark.split()[3]
    alpha = alpha.point(lambda p: p * transparency)
    watermark.putalpha(alpha)

    # Paste the watermark onto the transparent layer
    transparent_layer.paste(watermark, (x, y), watermark)
    
    # Composite the original image with the watermark layer
    watermarked_image = Image.alpha_composite(image.convert("RGBA"), transparent_layer)
    
    return watermarked_image.convert("RGB")

def select_bg_color():
    color_code = colorchooser.askcolor(title="Choose Background Color")[0]
    if color_code:
        bg_color_var.set(color_code)
        bg_color_label.config(text=f"Selected Color: {color_code}")

def select_input_folder():
    input_folder = filedialog.askdirectory()
    input_entry.delete(0, tk.END)
    input_entry.insert(0, input_folder)

def select_output_folder():
    output_folder = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_folder)

def select_watermark():
    watermark_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    watermark_entry.delete(0, tk.END)
    watermark_entry.insert(0, watermark_path)
    
    if watermark_path:
        with Image.open(watermark_path) as img:
            width, height = img.size
            width_entry.delete(0, tk.END)
            width_entry.insert(0, str(width))
            height_entry.delete(0, tk.END)
            height_entry.insert(0, str(height))


def start_conversion():
    input_folder = input_entry.get()
    output_folder = output_entry.get()
    output_format = output_format_var.get()

    if watermark_var.get():
        watermark_path = watermark_entry.get()
        selected_position = position_var.get()
        try:
            transparency = float(transparency_entry.get()) if transparency_entry.get() else 1.0
            custom_width = int(width_entry.get()) if width_entry.get() else None
            custom_height = int(height_entry.get()) if height_entry.get() else None
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for transparency, width, and height.")
            return
    else:
        watermark_path = None
        selected_position = None
        transparency = None
        custom_width = None
        custom_height = None

    if not input_folder or not output_folder:
        messagebox.showerror("Error", "Please select input folder and output folder.")
        return

    if watermark_var.get() and (not watermark_path):
        messagebox.showerror("Error", "Please select a watermark image.")
        return

    remove_bg = remove_bg_var.get()
    apply_bg = apply_bg_var.get()
    bg_color = tuple(map(int, bg_color_var.get().strip("()").split(", ")))
    
    convert_images(input_folder, output_folder, output_format, watermark_path, selected_position, transparency, custom_width, custom_height, remove_bg, bg_color, apply_bg)
    messagebox.showinfo("Success", "Conversion completed successfully!")

def show_watermark_preview():
    try:
        custom_width = int(width_entry.get()) if width_entry.get() else None
        custom_height = int(height_entry.get()) if height_entry.get() else None
        transparency = float(transparency_entry.get()) if transparency_entry.get() else 1.0
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for width, height, and transparency.")
        return

    if not watermark_entry.get():
        messagebox.showerror("Error", "Please select a watermark image.")
        return

    watermark_path = watermark_entry.get()
    watermark = Image.open(watermark_path).convert("RGBA")

    if custom_width and custom_height:
        watermark = watermark.resize((custom_width, custom_height), Image.LANCZOS)

    alpha = watermark.split()[3]
    alpha = alpha.point(lambda p: p * transparency)
    watermark.putalpha(alpha)

    preview_window = tk.Toplevel(root)
    preview_window.title("Watermark Preview")

    canvas = tk.Canvas(preview_window, width=watermark.width, height=watermark.height)
    canvas.pack()

    watermark_preview = ImageTk.PhotoImage(watermark)
    canvas.create_image(0, 0, anchor=tk.NW, image=watermark_preview)
    canvas.watermark_preview = watermark_preview

# ==========================================
# UI SETUP & LAYOUT
# ==========================================

root = tk.Tk()
root.title("Batch Image Converter & Watermark")
# Ubah ukuran menjadi lebih lebar dan pendek
root.geometry("850x600") 

# Judul Utama
title_label = tk.Label(root, text="Image Converter Pro", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Container Utama yang dibagi 2 (Kiri dan Kanan)
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# --- FRAME KIRI (File & Background) ---
left_frame = tk.Frame(main_frame)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

# Input
tk.Label(left_frame, text="Input Folder:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
input_entry = tk.Entry(left_frame, width=45)
input_entry.pack(anchor=tk.W, pady=2)
tk.Button(left_frame, text="Browse Input", command=select_input_folder, bg="#007bff", fg="white").pack(anchor=tk.W, pady=(0, 15))

# Output
tk.Label(left_frame, text="Output Folder:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
output_entry = tk.Entry(left_frame, width=45)
output_entry.pack(anchor=tk.W, pady=2)
tk.Button(left_frame, text="Browse Output", command=select_output_folder, bg="#007bff", fg="white").pack(anchor=tk.W, pady=(0, 15))

# Format
tk.Label(left_frame, text="Output Format:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
output_format_var = tk.StringVar(value="original")
output_format_dropdown = tk.OptionMenu(left_frame, output_format_var, "original", "JPEG", "WebP", "PNG")
output_format_dropdown.pack(anchor=tk.W, pady=(0, 15))

# Background Removal Section
tk.Label(left_frame, text="Background Options:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
remove_bg_var = tk.BooleanVar(value=False)
tk.Checkbutton(left_frame, text="Remove Background (AI)", variable=remove_bg_var).pack(anchor=tk.W)

apply_bg_var = tk.BooleanVar(value=False)
tk.Checkbutton(left_frame, text="Apply New Background Color", variable=apply_bg_var).pack(anchor=tk.W)

bg_color_var = tk.StringVar(value="(255, 255, 255)")
bg_color_label = tk.Label(left_frame, text="Current Color: White (Default)", fg="gray")
bg_color_label.pack(anchor=tk.W)
tk.Button(left_frame, text="Select BG Color", command=select_bg_color).pack(anchor=tk.W, pady=(5, 0))


# --- FRAME KANAN (Watermark) ---
right_frame = tk.Frame(main_frame)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

# Fungsi Toggle Sederhana (Hanya sembunyikan container)
def toggle_watermark_fields():
    if watermark_var.get():
        wm_container.pack(fill=tk.BOTH, expand=True)
    else:
        wm_container.pack_forget()

watermark_var = tk.BooleanVar(value=False)
tk.Checkbutton(right_frame, text="Enable Watermark", variable=watermark_var, font=("Arial", 10, "bold"), command=toggle_watermark_fields).pack(anchor=tk.W, pady=(0, 10))

# Container khusus watermark agar mudah disembunyikan/dimunculkan
wm_container = tk.Frame(right_frame)

tk.Label(wm_container, text="Watermark Image:").pack(anchor=tk.W)
watermark_entry = tk.Entry(wm_container, width=45)
watermark_entry.pack(anchor=tk.W, pady=2)
tk.Button(wm_container, text="Browse Watermark", command=select_watermark, bg="#17a2b8", fg="white").pack(anchor=tk.W, pady=(0, 10))

# Posisi
tk.Label(wm_container, text="Position:").pack(anchor=tk.W)
position_var = tk.StringVar(value="bottom right")
positions = ["top left", "top right", "center", "bottom left", "bottom right"]
for pos in positions:
    tk.Radiobutton(wm_container, text=pos.capitalize(), variable=position_var, value=pos).pack(anchor=tk.W)

# Size & Transparency
ukuran_frame = tk.Frame(wm_container)
ukuran_frame.pack(anchor=tk.W, pady=10)

tk.Label(ukuran_frame, text="Width:").grid(row=0, column=0, sticky="w")
width_entry = tk.Entry(ukuran_frame, width=8)
width_entry.grid(row=0, column=1, padx=(0, 15))

tk.Label(ukuran_frame, text="Height:").grid(row=0, column=2, sticky="w")
height_entry = tk.Entry(ukuran_frame, width=8)
height_entry.grid(row=0, column=3)

tk.Label(wm_container, text="Transparency (0.0 - 1.0):").pack(anchor=tk.W)
transparency_entry = tk.Entry(wm_container, width=10)
transparency_entry.insert(0, "1.0")
transparency_entry.pack(anchor=tk.W, pady=2)

tk.Button(wm_container, text="Show Watermark Preview", command=show_watermark_preview).pack(anchor=tk.W, pady=10)

# Sembunyikan kontainer watermark saat awal berjalan
wm_container.pack_forget()

# --- TOMBOL CONVERT DI BAWAH ---
bottom_frame = tk.Frame(root)
bottom_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=20)
convert_button = tk.Button(bottom_frame, text="START CONVERSION", command=start_conversion, bg="#28a745", fg="white", font=("Arial", 12, "bold"), padx=30, pady=10)
convert_button.pack()

root.mainloop()