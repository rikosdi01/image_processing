# 🧠 Vision Intelligence & Image Processing Suite

<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white" />
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" />
  <img src="https://img.shields.io/badge/Tkinter-gray?style=for-the-badge" />
</p>

## 📝 Project Overview
This repository is an **R&D Showcase** of various Computer Vision and Image Processing algorithms. It demonstrates the practical implementation of deep learning models and matrix manipulations to solve real-world visual data problems. 

The suite consists of four standalone desktop applications with intuitive Graphical User Interfaces (GUI), built to handle everything from AI-powered background removal to structural morphology and object detection.

---

## 🚀 The Toolkits & Features

### 1. Batch Image Converter Pro (AI Background Remover)
A powerful batch processing tool utilizing `rembg` for AI-driven background segmentation. It allows users to manipulate images in bulk with custom outputs.
* **Features:** Format conversion (WebP, PNG, JPEG), AI Background Removal, custom background color application, and dynamic watermarking with transparency controls.

<table border="0">
  <tr>
    <td width="50%" align="center"><b>User Interface</b></td>
    <td width="50%" align="center"><b>AI Processing Result</b></td>
  </tr>
  <tr>
    <td align="center"><img src="assets/preview/convert.png" width="350" alt="Converter UI"/></td>
    <td align="center"><img src="assets/converter/no_backgrounds/laptop_1.png" width="300" alt="No Background Result"/></td>
  </tr>
</table>

### 2. AI Object Detection
An intelligent scanner that leverages the **TensorFlow MobileNet V2 (COCO)** pre-trained model to identify multiple objects within a single frame.
* **Features:** Bounding box generation, accuracy score labeling, and automatic result saving.

<table border="0">
  <tr>
    <td width="50%" align="center"><b>Detection Setup</b></td>
    <td width="50%" align="center"><b>TensorFlow Detection Output</b></td>
  </tr>
  <tr>
    <td align="center"><img src="assets/preview/object_detection.png" width="300" alt="Detection UI"/></td>
    <td align="center"><img src="assets/object_detection/detected_laptop_1.jpg" width="300" alt="Detection Result"/></td>
  </tr>
</table>

### 3. Image Morphology Tool
A matrix-manipulation tool to process image structures using **OpenCV Erosion and Dilation**.
* **Features:** 5x5 kernel processing to expand or shrink foreground pixels, useful for noise removal or structural enhancement.

<table border="0">
  <tr>
    <td width="33%" align="center"><b>User Interface</b></td>
    <td width="33%" align="center"><b>Dilated Image</b></td>
    <td width="33%" align="center"><b>Eroded Image</b></td>
  </tr>
  <tr>
    <td align="center"><img src="assets/preview/morphology.png" width="250" alt="Morphology UI"/></td>
    <td align="center"><img src="assets/morphology/laptop_1_dilated.jpg" width="250" alt="Dilated Result"/></td>
    <td align="center"><img src="assets/morphology/laptop_1_eroded.jpg" width="250" alt="Eroded Result"/></td>
  </tr>
</table>

### 4. Background Remover Basic (Thresholding)
A fundamental computer vision tool that uses binary thresholding algorithms to separate objects from high-contrast backgrounds.
* **Features:** Generates both normal and inverse transparency masks, saving outputs strictly in `.png` to preserve the alpha channel.

<table border="0">
  <tr>
    <td width="50%" align="center"><b>User Interface</b></td>
    <td width="50%" align="center"><b>Thresholding Output (Inverse Mask)</b></td>
  </tr>
  <tr>
    <td align="center"><img src="assets/preview/thresholding.png" width="300" alt="Threshold UI"/></td>
    <td align="center"><img src="assets/thresholding/laptop_1_trans_inv.png" width="300" alt="Threshold Result"/></td>
  </tr>
</table>

---

## ⚙️ Installation & Setup

### Prerequisites
* Python 3.10+
* Ensure you are in a virtual environment (`.venv`) to prevent library conflicts.

### 1. Install Dependencies
All required libraries, including `tensorflow`, `opencv-python`, `rembg`, and `Pillow`, are listed in the requirements file.
```bash
pip install -r requirements.txt

### 2. Download Pre-Trained AI Models (Required)

> [!IMPORTANT]  
> To keep this repository lightweight, the heavy model weights (`*.pb`, `*.h5`) and model directories are excluded via `.gitignore`. You must download them manually to run the AI-powered tools.

**A. Object Detection Model (SSD MobileNet V2)**
1. Download the [SSD MobileNet v2 320x320 COCO](http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_320x320_coco17_tpu-8.tar.gz) model.
2. Extract the `.tar.gz` archive.
3. Rename the extracted folder to `ssd_mobilenet_v2_coco`.
4. Place this folder inside a `model/` directory in the root of your project.

**B. Segmentation Model (Mask R-CNN)**
1. Download the pre-trained `mask_rcnn_coco.h5` weights. *(Note: You can download this from the official Matterport Mask R-CNN releases).*
2. Place the `mask_rcnn_coco.h5` file directly inside the `model/` directory.

**Expected Folder Structure:**
Before running the scripts, ensure your root directory looks like this:

```text
Vision-Intelligence-Suite/
├── assets/
├── model/
│   ├── ssd_mobilenet_v2_coco/      # MobileNet V2 Model
│   └── mask_rcnn_coco.h5           # Mask R-CNN Weights
├── image_convert.py
├── object_detection.py
├── morphology.py
├── thresholding.py
└── requirements.txt

### 3. Run the Tools
Navigate to the root directory and run the desired python script:

python image_convert.py
python object_detection.py
python morphology.py
python thresholding.py
