# 🏎️ APEX // PlateScan — AI Vehicle License Plate Detection & OCR

An end-to-end, car-themed web application that scans vehicle images for license plates using a fine-tuned **YOLOv8** model and extracts alphanumeric plate characters using **EasyOCR**.

Runs **100% locally on standard laptop CPUs** with zero paid cloud API dependencies.

---

## 🛠️ Tech Stack & Model Provenance

- **Backend Framework**: Python 3.10+ / 3.14 with [Flask](https://flask.palletsprojects.com/)
- **License Plate Detector**:
  - **Architecture**: Ultralytics YOLOv8 Nano (`yolov8n`), fine-tuned specifically for vehicle license plate detection.
  - **Source**: Hugging Face Hub ([`Koushim/yolov8-license-plate-detection`](https://huggingface.co/Koushim/yolov8-license-plate-detection)).
  - **Local Model Cache**: Stored locally in `./models/yolov8n_plate.pt` (~6.2 MB) for offline execution.
  - **Device / Runtime**: CPU-optimized (640x640 resolution, FP32).
- **OCR Engine**:
  - **Architecture**: [EasyOCR](https://github.com/JaidedAI/EasyOCR) (PyTorch CRAFT character region detector + CRNN sequence recognizer).
  - **Device**: Pure CPU execution (`gpu=False`).
- **Computer Vision & Drawing**: [OpenCV](https://opencv.org/) (`opencv-python`) for image decoding, cropping, HUD bounding box rendering, and base64 transmission.
- **Frontend**: Responsive single-page interface styled with a dark asphalt theme, carbon-fiber textures, brushed chrome accents, racing-red highlights, and skeuomorphic license plate display.

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.10, 3.11, 3.12, 3.13, or 3.14 (64-bit)
- Windows, macOS, or Linux

### 2. Activate the Virtual Environment
If you are running in the project directory, activate the pre-configured virtual environment:

**On Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt `cmd`):**
```cmd
venv\Scripts\activate.bat
```

**On Linux / macOS:**
```bash
source venv/bin/activate
```

*(If creating a new virtual environment from scratch)*:
```bash
python -m venv venv
.\venv\Scripts\pip install -r requirements.txt
```

### 3. Launch the Application
Start the Flask web server:
```powershell
python app.py
```

Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🧪 Quick Test Fleet (1-Click Presets)

The application includes 3 bundled test vehicles ready to inspect immediately:
1. **White Sedan**: Frontal view with standard European license plate (`KA05 MB`).
2. **Red Sports Car**: Rear bumper view with California-style plate (`APEX 911`).
3. **Angled Car**: Oblique perspective view testing angled detection (`SPEED 77`).

You can also drop or browse any custom **JPG**, **JPEG**, **PNG**, or **WEBP** vehicle photograph from your local drive.

---

## 📊 Telemetry & Output Data

When a vehicle image is scanned, the API computes and displays:
1. **Plate Detected Status**: Green telemetry light if found, or plain notice if absent.
2. **Bounding Box Coordinates**:
   - `x`: Top-left horizontal coordinate in pixels.
   - `y`: Top-left vertical coordinate in pixels.
   - `width`: Width of the bounding box in pixels.
   - `height`: Height of the bounding box in pixels.
   - `image_dimensions`: Native image width and height (`W × H px`) ensuring coordinates are interpretable.
   - `coverage`: Percentage of total canvas occupied by the plate.
3. **OCR License Plate Readout**:
   - Skeuomorphic physical plate representation of recognized characters.
   - Confidence percentage meter.
   - Best-effort recognition disclaimer.
4. **Annotated Image Display**:
   - High-visibility racing HUD overlay with neon-red bounding box and cyan corner brackets.
   - Toggle button between **Annotated** and **Original** views.

---

## ⚠️ Limitations & Best-Effort Disclaimer

Optical Character Recognition (OCR) is inherently a **best-effort** estimation. While the YOLOv8 model localizes license plates with high accuracy (~98%+), character recognition accuracy degrades under the following conditions:
- Oblique / extreme camera angles (>45 degrees off-axis)
- Low sensor resolution, motion blur, or digital compression artifacts
- Heavy shadows, headlight glare, or nighttime noise
- Road grime, mud, or weathered physical plates
- Stylized, italicized, or decorative novelty fonts

The app is intended for inspection, testing, and portfolio demonstrations—not for automated law enforcement or legal citations.

---

## 🔬 Automated Testing

To run the automated integration test suite:
```powershell
python test_app.py
```
This tests all routes (`/`, `/api/health`, `/api/scan`), sample presets, file uploads, bounding box assertions, and negative non-plate scenarios.
