import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def process_morphology():
    # 1. Membuka dialog untuk memilih file gambar
    file_path = filedialog.askopenfilename(
        title="Pilih Gambar untuk Operasi Morfologi",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )
    
    if not file_path:
        return  # Batal memilih file

    lbl_status.config(text="Memproses gambar...", fg="blue")
    root.update()

    try:
        # 2. Membaca gambar dalam mode grayscale
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

        if image is None:
            messagebox.showerror("Error", "Gambar tidak dapat dibaca atau format tidak didukung!")
            lbl_status.config(text="Gagal memproses gambar.", fg="red")
            return

        # 3. Membuat kernel untuk operasi morfologi (Matriks 5x5)
        kernel = np.ones((5, 5), np.uint8)

        # 4. Melakukan operasi morfologi pada gambar asli
        dilated_image = cv2.dilate(image, kernel, iterations=1)
        eroded_image = cv2.erode(image, kernel, iterations=1)

        # 5. Resize setelah operasi morfologi
        resized_original = cv2.resize(image, (1200, 800))
        resized_dilated_image = cv2.resize(dilated_image, (1200, 800))
        resized_eroded_image = cv2.resize(eroded_image, (1200, 800))

        # 6. Membuka dialog untuk memilih FOLDER PENYIMPANAN
        save_dir = filedialog.askdirectory(
            title="Pilih Folder untuk Menyimpan Hasil"
        )

        if save_dir:
            # 7. Menyimpan gambar di folder yang dipilih pengguna
            original_name = os.path.basename(file_path)
            
            # Memisahkan nama file dan ekstensinya (misal: 'laptop_1' dan '.jpg')
            name_only, ext = os.path.splitext(original_name)
            
            # Format nama baru yang lebih rapi
            save_path_dil = os.path.join(save_dir, f"{name_only}_dilated.jpg")
            save_path_ero = os.path.join(save_dir, f"{name_only}_eroded.jpg")
            
            cv2.imwrite(save_path_dil, resized_dilated_image)
            cv2.imwrite(save_path_ero, resized_eroded_image)
            lbl_status.config(text="Disimpan! Tekan tombol di jendela gambar untuk menutup.", fg="green")
        else:
            # Jika pengguna menekan 'Cancel' pada dialog penyimpanan
            lbl_status.config(text="Batal menyimpan. Menampilkan pratinjau...\nTekan tombol apa saja untuk menutup.", fg="orange")
            
        root.update()

        # 8. Menampilkan hasil di jendela OpenCV
        # cv2.imshow('Original Image', resized_original)
        # cv2.imshow('Dilated Image', resized_dilated_image)
        # cv2.imshow('Eroded Image', resized_eroded_image)

        cv2.waitKey(0)  # Tunggu sampai pengguna menekan tombol pada keyboard
        cv2.destroyAllWindows()  # Tutup semua jendela gambar OpenCV

        lbl_status.config(text="Siap memproses gambar lain.", fg="black")

    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan teknis: {e}")
        lbl_status.config(text="Terjadi Error.", fg="red")

# --- UI SETUP ---
root = tk.Tk()
root.title("Image Morphology Tool")
root.geometry("400x250")
root.configure(padx=20, pady=20)

# Header
tk.Label(root, text="Alat Operasi Morfologi Citra", font=("Arial", 14, "bold")).pack(pady=5)
tk.Label(root, text="(Erosi & Dilasi OpenCV)", font=("Arial", 10, "italic"), fg="gray").pack()

# Tombol Eksekusi
btn_select = tk.Button(
    root, 
    text="PILIH GAMBAR", 
    command=process_morphology, 
    bg="#28a745", 
    fg="white", 
    font=("Arial", 10, "bold"), 
    padx=20, 
    pady=10, 
    cursor="hand2"
)
btn_select.pack(pady=25)

# Status bar
lbl_status = tk.Label(root, text="Menunggu input gambar...", font=("Arial", 10), wraplength=350)
lbl_status.pack(side="bottom", pady=10)

root.mainloop()