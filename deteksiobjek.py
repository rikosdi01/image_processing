import cv2
import tensorflow as tf
import numpy as np

# Muat model pre-trained dari TensorFlow Model Zoo (misalnya, model deteksi objek)
model = tf.saved_model.load("ssd_mobilenet_v2_coco/saved_model")  # Ganti dengan path ke model yang benar

# Fungsi untuk memuat gambar
def load_image(image_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return np.expand_dims(image_rgb, axis=0)

# Fungsi untuk mendeteksi objek
def detect_objects(image_path):
    image = load_image(image_path)

    # Lakukan deteksi objek
    detections = model(image)

    # Ambil informasi deteksi
    boxes = detections['detection_boxes'][0].numpy()
    classes = detections['detection_classes'][0].numpy()
    scores = detections['detection_scores'][0].numpy()

    # Tampilkan hasil deteksi
    image = cv2.imread(image_path)
    for i in range(len(boxes)):
        if scores[i] > 0.5:  # Deteksi hanya jika score lebih besar dari 0.5
            box = boxes[i]
            ymin, xmin, ymax, xmax = box
            (startX, startY, endX, endY) = (int(xmin * image.shape[1]), int(ymin * image.shape[0]), int(xmax * image.shape[1]), int(ymax * image.shape[0]))
            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
    
    # Tampilkan gambar hasil deteksi
    cv2.imshow("Object Detection", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Deteksi objek pada gambar
image_path = 'As Engkol Y. Mio.JPG'
detect_objects(image_path)
