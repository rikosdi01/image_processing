import cv2
import numpy as np

# Membaca gambar
image = cv2.imread('As Engkol Y. Mio.JPG', cv2.IMREAD_GRAYSCALE)  # Membaca gambar dalam mode grayscale

if image is None:
    print("Gambar tidak ditemukan!")
    exit()  # Jika gambar tidak ditemukan, keluar dari program

# Membuat kernel untuk operasi morfologi
kernel = np.ones((5,5), np.uint8)  # Kernel berbentuk matriks 5x5

# Melakukan operasi morfologi pada gambar asli
dilated_image = cv2.dilate(image, kernel, iterations=1)
eroded_image = cv2.erode(image, kernel, iterations=1)

# Resize setelah operasi morfologi
resized_dilated_image = cv2.resize(dilated_image, (1200, 800))
resized_eroded_image = cv2.resize(eroded_image, (1200, 800))

# Menampilkan hasil
cv2.imshow('Original Image', cv2.resize(image, (1200, 800)))  # Menampilkan gambar asli yang di-resize
cv2.imshow('Dilated Image', resized_dilated_image)
cv2.imshow('Eroded Image', resized_eroded_image)

# Menyimpan gambar hasil morfologi
cv2.imwrite('Morfologi/dilated_image.jpg', resized_dilated_image)
cv2.imwrite('Morfologi/eroded_image.jpg', resized_eroded_image)

cv2.waitKey(0)  # Tunggu sampai pengguna menekan tombol
cv2.destroyAllWindows()  # Tutup semua jendela
