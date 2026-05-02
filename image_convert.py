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

# Create main window
root = tk.Tk()
root.title("Image Converter with Background Removal")
root.geometry("400x950")

remove_bg_var = tk.BooleanVar(value=False)
remove_bg_toggle = tk.Checkbutton(root, text="Remove Background", variable=remove_bg_var)
remove_bg_toggle.pack(pady=5)

apply_bg_var = tk.BooleanVar(value=False)
apply_bg_toggle = tk.Checkbutton(root, text="Apply Background Color", variable=apply_bg_var)
apply_bg_toggle.pack(pady=5)

bg_color_var = tk.StringVar(value="(255, 255, 255)")
bg_color_label = tk.Label(root, text="Background Color: White (Default)")
bg_color_label.pack(pady=5)

bg_color_button = tk.Button(root, text="Select Background Color", command=select_bg_color)
bg_color_button.pack(pady=5)

# Create a title label
title_label = tk.Label(root, text="JPG to WebP Converter", font=("Arial", 16, "bold"), bg="#f7f7f7")
title_label.pack(pady=10)

# Input folder selection
input_label = tk.Label(root, text="Input Folder (JPG):", bg="#f7f7f7")
input_label.pack(pady=5)

input_entry = tk.Entry(root, width=50)
input_entry.pack(pady=5)

input_button = tk.Button(root, text="Browse", command=select_input_folder, bg="#4CAF50", fg="white")
input_button.pack(pady=5)

# Output folder selection
output_label = tk.Label(root, text="Output Folder (WebP):", bg="#f7f7f7")
output_label.pack(pady=5)

output_entry = tk.Entry(root, width=50)
output_entry.pack(pady=5)

output_button = tk.Button(root, text="Browse", command=select_output_folder, bg="#4CAF50", fg="white")
output_button.pack(pady=5)

output_format_var = tk.StringVar(value="original")
output_format_label = tk.Label(root, text="Output Format:")
output_format_label.pack(pady=5)

output_format_dropdown = tk.OptionMenu(root, output_format_var, "original", "JPEG", "WebP", "PNG")
output_format_dropdown.pack(pady=5)

# Watermark toggle switch
watermark_var = tk.BooleanVar(value=False)
watermark_toggle = tk.Checkbutton(root, text="Use Watermark", variable=watermark_var, bg="#f7f7f7", command=lambda: toggle_watermark_fields())
watermark_toggle.pack(pady=5)

# Watermark selection
watermark_label = tk.Label(root, text="Watermark Image:", bg="#f7f7f7")
watermark_entry = tk.Entry(root, width=50)
watermark_button = tk.Button(root, text="Browse", command=select_watermark, bg="#4CAF50", fg="white")

# Position selection
position_var = tk.StringVar(value="bottom right")  # Default position
position_label = tk.Label(root, text="Watermark Position:", bg="#f7f7f7")

positions = ["top left", "top right", "center", "bottom left", "bottom right"]

# Function to show/hide watermark fields
def toggle_watermark_fields():
    if watermark_var.get():
        watermark_label.pack(pady=5)
        watermark_entry.pack(pady=5)
        watermark_button.pack(pady=5)
        position_label.pack(pady=5)
        for pos in positions:
            position_radio = tk.Radiobutton(root, text=pos.capitalize(), variable=position_var, value=pos, bg="#f7f7f7")
            position_radio.pack(anchor=tk.W)  # Pack with anchor to align left
        # Add fields for custom width, height, and transparency
        width_label.pack(pady=5)
        width_entry.pack(pady=5)
        height_label.pack(pady=5)
        height_entry.pack(pady=5)
        transparency_label.pack(pady=5)
        transparency_entry.pack(pady=5)
        show_button.pack(pady=5)
    else:
        watermark_label.pack_forget()
        watermark_entry.pack_forget()
        watermark_button.pack_forget()
        position_label.pack_forget()
        for pos in positions:
            for widget in root.pack_slaves():  # Remove all radio buttons
                if isinstance(widget, tk.Radiobutton):
                    widget.pack_forget()
        width_label.pack_forget()
        width_entry.pack_forget()
        height_label.pack_forget()
        height_entry.pack_forget()
        transparency_label.pack_forget()
        transparency_entry.pack_forget()
        show_button.pack_forget()

# Width and height inputs
width_label = tk.Label(root, text="Custom Width:", bg="#f7f7f7")
width_entry = tk.Entry(root, width=10)
height_label = tk.Label(root, text="Custom Height:", bg="#f7f7f7")
height_entry = tk.Entry(root, width=10)

# Transparency input
transparency_label = tk.Label(root, text="Watermark Transparency (0.0 - 1.0):", bg="#f7f7f7")
transparency_entry = tk.Entry(root, width=10)
transparency_entry.insert(0, "1.0")  # Default value

def show_watermark_preview():
    # Get user inputs for width, height, and transparency
    try:
        custom_width = int(width_entry.get()) if width_entry.get() else None
        custom_height = int(height_entry.get()) if height_entry.get() else None
        transparency = float(transparency_entry.get()) if transparency_entry.get() else 1.0
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for width, height, and transparency.")
        return

    # Load the watermark image
    if not watermark_entry.get():
        messagebox.showerror("Error", "Please select a watermark image.")
        return

    watermark_path = watermark_entry.get()
    watermark = Image.open(watermark_path).convert("RGBA")

    # Resize watermark
    if custom_width and custom_height:
        watermark = watermark.resize((custom_width, custom_height), Image.LANCZOS)

    # Apply transparency
    alpha = watermark.split()[3]
    alpha = alpha.point(lambda p: p * transparency)  # Adjust transparency
    watermark.putalpha(alpha)

    # Create a new window for preview
    preview_window = tk.Toplevel(root)
    preview_window.title("Watermark Preview")

    # Create a blank canvas for the preview
    canvas = tk.Canvas(preview_window, width=watermark.width, height=watermark.height)
    canvas.pack()

    # Create an ImageTk object and display it on the canvas
    watermark_preview = ImageTk.PhotoImage(watermark)
    canvas.create_image(0, 0, anchor=tk.NW, image=watermark_preview)

    # Keep a reference to avoid garbage collection
    canvas.watermark_preview = watermark_preview

show_button = tk.Button(root, text="Show Watermark", command=show_watermark_preview, bg="#4CAF50", fg="white")

# Conversion button
convert_button = tk.Button(root, text="Convert", command=start_conversion)
convert_button.pack(side=tk.BOTTOM, pady=20)

# Run the application
root.mainloop()