import cv2
import tensorflow as tf
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import os

# --- INISIALISASI MODEL ---
print("Memuat model TensorFlow (Harap tunggu beberapa saat)...")
try:
    # Ganti dengan path ke model Anda jika berbeda
    model = tf.saved_model.load("model/ssd_mobilenet_v2_coco/saved_model") 
    print("Model berhasil dimuat!")
except Exception as e:
    print(f"Error memuat model: {e}")
    model = None

# --- LOGIKA DETEKSI & GUI ---
def process_detection():
    if model is None:
        messagebox.showerror("Error", "Model TensorFlow gagal dimuat. Periksa path folder model Anda.")
        return

    # 1. Dialog Pilih Gambar
    file_path = filedialog.askopenfilename(
        title="Pilih Gambar untuk Deteksi Objek",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )
    
    if not file_path:
        return

    lbl_status.config(text="Memproses deteksi objek...", fg="blue")
    root.update()

    try:
        # 2. Load dan Pre-processing Gambar
        image_bgr = cv2.imread(file_path)
        if image_bgr is None:
            messagebox.showerror("Error", "Gambar tidak dapat dibaca!")
            return
            
        # TensorFlow membutuhkan format RGB
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        input_tensor = np.expand_dims(image_rgb, axis=0)

        # 3. Lakukan Deteksi
        detections = model(input_tensor)

        boxes = detections['detection_boxes'][0].numpy()
        classes = detections['detection_classes'][0].numpy()
        scores = detections['detection_scores'][0].numpy()

        output_image = image_bgr.copy()
        detected_count = 0

        # 4. Gambar Bounding Box
        for i in range(len(boxes)):
            if scores[i] > 0.5:  # Hanya tampilkan yang akurasinya > 50%
                detected_count += 1
                box = boxes[i]
                ymin, xmin, ymax, xmax = box
                (startX, startY, endX, endY) = (
                    int(xmin * output_image.shape[1]), 
                    int(ymin * output_image.shape[0]), 
                    int(xmax * output_image.shape[1]), 
                    int(ymax * output_image.shape[0])
                )
                
                # Gambar kotak hijau
                cv2.rectangle(output_image, (startX, startY), (endX, endY), (0, 255, 0), 2)
                
                # Tulis label skor di atas kotak
                label = f"Obj: {scores[i]*100:.1f}%"
                cv2.putText(output_image, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        lbl_status.config(text=f"Deteksi Selesai! ({detected_count} objek).\nPilih folder penyimpanan...", fg="blue")
        root.update()

        # 5. Dialog Pilih Folder Penyimpanan
        save_dir = filedialog.askdirectory(title="Pilih Folder untuk Menyimpan Hasil")
        
        if save_dir:
            # Menggunakan nama file asli dengan tambahan prefix 'detected_'
            original_name = os.path.basename(file_path)
            save_path = os.path.join(save_dir, f"detected_{original_name}")
            cv2.imwrite(save_path, output_image)
            lbl_status.config(text=f"Tersimpan di:\n{save_path}", fg="green")
        else:
            lbl_status.config(text="Batal menyimpan. Menampilkan pratinjau...", fg="orange")
            
        root.update()

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        if not save_dir:
            lbl_status.config(text="Siap memproses gambar lain.", fg="black")

    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
        lbl_status.config(text="Terjadi Error.", fg="red")

# --- UI SETUP ---
root = tk.Tk()
root.title("TF Object Detection Tool")
root.geometry("450x250")
root.configure(padx=20, pady=20)

tk.Label(root, text="AI Object Detection", font=("Arial", 14, "bold")).pack(pady=5)
tk.Label(root, text="(TensorFlow MobileNet V2)", font=("Arial", 10, "italic"), fg="gray").pack()

btn_select = tk.Button(
    root, 
    text="PILIH GAMBAR", 
    command=process_detection, 
    bg="#dc3545", # Warna merah agar beda dengan UI Morfologi
    fg="white", 
    font=("Arial", 10, "bold"), 
    padx=20, 
    pady=10, 
    cursor="hand2"
)
btn_select.pack(pady=20)

lbl_status = tk.Label(root, text="Menunggu input gambar...", font=("Arial", 10), wraplength=400)
lbl_status.pack(side="bottom", pady=10)

root.mainloop()