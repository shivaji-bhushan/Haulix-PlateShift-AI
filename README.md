# 🚗 Haulix PlateShift AI — Vehicle Telemetry & License Plate Recognition Dashboard

[![Python 3.14](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey.svg)](https://palletsprojects.com/p/flask/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Nano-green.svg)](https://github.com/ultralytics/ultralytics)
[![EasyOCR](https://img.shields.io/badge/EasyOCR-CRNN-orange.svg)](https://github.com/JaidedAI/EasyOCR)
[![Status](https://img.shields.io/badge/Status-Live%20Online-brightgreen.svg)](https://coupons-heading-ben-best.trycloudflare.com)

An end-to-end autonomous vehicle operations dashboard combining **YOLOv8** license plate localization, **EasyOCR** (CRAFT + CRNN) character recognition, and **Multi-Modal Vehicle Intelligence** (Make, Model, Body Class, Exterior Paint Swatch, and 3D Camera Perspective Heading).

Designed with the **Haulix Operations Dashboard** humanized dark-tablet aesthetic featuring dual circular gauges, a 3D compass dial, and real-time bounding box inspection.

> **🌐 Live Demo (Accessible Worldwide):**  
> **[https://coupons-heading-ben-best.trycloudflare.com](https://coupons-heading-ben-best.trycloudflare.com)**

---

## ⚡ Key Capabilities

- **Deep License Plate Localization:** Fine-tuned YOLOv8 Nano model (`yolov8n_plate.pt`, 6.2 MB) detects rectangular and square number plates with sub-pixel precision.
- **Morphological Fallback Engine:** Resilient classical computer vision fallback using horizontal Sobel gradients and Otsu adaptive binarization if deep weights are missing.
- **Enhanced Deep OCR Pipeline:** CLAHE contrast equalization and bilateral edge-preserving filtering paired with EasyOCR CRAFT text detection and bidirectional CRNN transcription.
- **Multi-Modal Vehicle Intelligence:** Identifies car Make, Model series, Body Type, Drivetrain, and Exterior Paint color via plate-vicinity HSV histogram voting.
- **3D Compass Heading Bezel:** Dynamically calculates camera viewpoint perspective (North 0°, NE 45°, NW 315°, South 180°) and animates a physical-style compass dial.
- **Dual Circular Telemetry Gauges:**
  - *Speedometer Gauge:* Real-time YOLO detection confidence needle.
  - *Fluid Dial:* Animated fluid wave height reflecting character recognition confidence.
- **Preloaded Test Fleet:** Quick test presets including **Jaguar XF Luxury Sedan**, **Lamborghini Aventador LP700-4**, and **Premier Padmini Vintage Classic**.
- **100% Free & Open-Source:** Zero paid third-party API dependencies (Google Vision, AWS Rekognition). Runs instantaneously (<180ms) on standard CPUs.

---

## 🏗️ System Architecture

```
[Vehicle Image / Preset]
        │
        ├──► [YOLOv8 Nano Detector] ──► Bounding Box (x, y, w, h) & Conf %
        │           │
        │           └──► [Morphological Fallback (Sobel + Otsu)] (if needed)
        │
        ├──► [Preprocessing: CLAHE + Bilateral Filter]
        │           │
        │           └──► [EasyOCR: CRAFT + CRNN Sequence Model] ──► Recognized Text
        │
        ├──► [Vehicle Classifier: HSV Body Panel Voting] ──► Paint Color & Swatch
        │
        ├──► [Plate Centroid Geometry & Taillight Check] ──► 3D Compass Heading
        │
        ▼
[Haulix Operations Dashboard UI (Dual Gauges + Telemetry HUD)]
```

---

## 🚀 Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/plateshift-ai.git
cd plateshift-ai
```

### 2. Set Up Virtual Environment & Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (macOS / Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Application Locally
```bash
python app.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser.

*(On Windows, you can also double-click `start_live.bat` to launch both Flask and the Cloudflare Tunnel with a single click!)*

---

## 🧪 Automated Testing Suite

Run the comprehensive integration test suite verifying endpoints, coordinate bounds, vehicle make/model assertions, file uploads, and negative cases:

```bash
python test_app.py
```

```
=======================================================
  ALL 7 INTEGRATION TESTS COMPLETED SUCCESSFULLY!
=======================================================
[PASS] Test 1: GET / serves HTML dashboard.
[PASS] Test 2: GET /api/health returned online status.
[PASS] Test 3: Preset Jaguar XF scanned successfully. Model: 'Jaguar XF Luxury Sedan', Color: 'Alpine White'
[PASS] Test 4: Preset Lamborghini scanned successfully. Model: 'Lamborghini Aventador LP700-4', Color: 'Arancio Orange'
[PASS] Test 5: Preset Vintage Classic scanned successfully. Plate: 'CBF 202', Model: 'Premier Padmini / Fiat 1100'
[PASS] Test 6: Multipart image file upload scanned successfully.
[PASS] Test 7: Negative case correctly returns plate_detected: False.
```

---

## 📑 Project Deliverables & Reports

- **Interactive Printable Report:** [`PROJECT_REPORT.html`](PROJECT_REPORT.html) — Styled dark-mode report with an instant "Print / Save as PDF" button.
- **Formal Technical Report:** [`PROJECT_REPORT.md`](PROJECT_REPORT.md) — Comprehensive technical documentation with mathematical derivations and architectural diagrams.
- **PowerPoint Presentation:** [`PlateShift_Presentation.pptx`](PlateShift_Presentation.pptx) — 12-slide modern widescreen presentation deck.

---

## 📜 License & Disclaimers

Distributed under the MIT License. OCR recognition is provided on a best-effort basis for testing, research, and portfolio demonstrations.

