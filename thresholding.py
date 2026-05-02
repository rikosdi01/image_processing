import cv2
import numpy as np

# Membaca gambar
img = cv2.imread('As Engkol Y. Mio.JPG')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Thresholding untuk mendapatkan mask
ret, mask = cv2.threshold(img_gray, 190, 255, cv2.THRESH_BINARY_INV)  # Mask untuk area hitam
ret, mask2 = cv2.threshold(img_gray, 190, 255, cv2.THRESH_BINARY)  # Mask untuk area selain hitam

# Membuat gambar dengan 4 channel (BGRA)
img_with_alpha = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
img_with_alpha2 = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

# Menetapkan area hitam pada mask sebagai transparan (mask == 0 untuk transparan)
img_with_alpha[mask == 0] = [0, 0, 0, 0]  # Set RGB = 0,0,0 dan alpha = 0 untuk transparansi

# Menetapkan area selain hitam pada mask2 sebagai transparan (mask2 == 0 untuk transparan)
img_with_alpha2[mask2 == 0] = [0, 0, 0, 0]  # Set RGB = 0,0,0 dan alpha = 0 untuk transparansi

# Resize gambar
resized_img = cv2.resize(img_with_alpha, (1200, 800))
resized_img2 = cv2.resize(img_with_alpha2, (1200, 800))

# Menampilkan gambar
cv2.imshow('Image with Transparency', resized_img)
cv2.imshow('Image with Transparency 2', resized_img2)  # Show the second image with transparency

# Menyimpan gambar dengan transparansi
cv2.imwrite('transparan.png', resized_img)  # Save the first image with transparency

cv2.waitKey(0)
cv2.destroyAllWindows()
