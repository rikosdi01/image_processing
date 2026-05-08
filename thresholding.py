import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def process_thresholding():
    # 1. Dialog untuk memilih file gambar
    file_path = filedialog.askopenfilename(
        title="Pilih Gambar untuk Thresholding",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )
    
    if not file_path:
        return  # Batal memilih file

    lbl_status.config(text="Memproses gambar...", fg="blue")
    root.update()

    try:
        # 2. Membaca gambar dan konversi ke Grayscale
        img = cv2.imread(file_path)
        
        if img is None:
            messagebox.showerror("Error", "Gambar tidak dapat dibaca atau format tidak didukung!")
            lbl_status.config(text="Gagal memproses gambar.", fg="red")
            return

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 3. Thresholding untuk mendapatkan mask
        ret, mask = cv2.threshold(img_gray, 190, 255, cv2.THRESH_BINARY_INV)  # Mask area hitam
        ret, mask2 = cv2.threshold(img_gray, 190, 255, cv2.THRESH_BINARY)     # Mask area selain hitam

        # 4. Membuat gambar dengan 4 channel (BGRA - Ada Alpha untuk transparansi)
        img_with_alpha = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        img_with_alpha2 = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

        # 5. Menetapkan area transparan (mask == 0)
        img_with_alpha[mask == 0] = [0, 0, 0, 0]   # Transparan untuk inverse
        img_with_alpha2[mask2 == 0] = [0, 0, 0, 0] # Transparan untuk normal

        # 6. Resize gambar
        resized_img = cv2.resize(img_with_alpha, (1200, 800))
        resized_img2 = cv2.resize(img_with_alpha2, (1200, 800))

        # 7. Dialog untuk memilih FOLDER PENYIMPANAN
        save_dir = filedialog.askdirectory(
            title="Pilih Folder untuk Menyimpan Hasil"
        )

        if save_dir:
            # Ambil nama asli tanpa ekstensi (misal: 'laptop_1' dari 'laptop_1.jpg')
            original_name = os.path.basename(file_path)
            name_only, _ = os.path.splitext(original_name)
            
            # 8. Simpan gambar (WAJIB .png agar transparansi tidak hilang)
            save_path_1 = os.path.join(save_dir, f"{name_only}_trans_inv.png")
            save_path_2 = os.path.join(save_dir, f"{name_only}_trans_norm.png")
            
            cv2.imwrite(save_path_1, resized_img)
            cv2.imwrite(save_path_2, resized_img2)
            
            lbl_status.config(text="Disimpan format PNG! Tekan tombol di pratinjau untuk menutup.", fg="green")
        else:
            lbl_status.config(text="Batal menyimpan. Menampilkan pratinjau...\nTekan tombol apa saja untuk menutup.", fg="orange")
            
        root.update()

        cv2.waitKey(0)  # Tunggu sampai pengguna menekan tombol pada keyboard
        cv2.destroyAllWindows()  # Tutup semua jendela gambar OpenCV

        lbl_status.config(text="Siap memproses gambar lain.", fg="black")

    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan teknis: {e}")
        lbl_status.config(text="Terjadi Error.", fg="red")

# --- UI SETUP ---
root = tk.Tk()
root.title("Image Thresholding Tool")
root.geometry("400x250")
root.configure(padx=20, pady=20)

# Header
tk.Label(root, text="Alat Background Remover Basic", font=("Arial", 14, "bold")).pack(pady=5)
tk.Label(root, text="(Thresholding OpenCV)", font=("Arial", 10, "italic"), fg="gray").pack()

# Tombol Eksekusi
btn_select = tk.Button(
    root, 
    text="PILIH GAMBAR", 
    command=process_thresholding, 
    bg="#007bff", # Warna biru
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