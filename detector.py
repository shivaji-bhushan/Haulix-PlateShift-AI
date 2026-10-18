"""
APEX // PlateScan - Vehicle Plate Detector Engine
Coordinates YOLOv8 model loading, bounding-box detection, plate cropping,
OCR invocation, and racing-themed visual annotation.
"""

import base64
import logging
import os
import cv2
import numpy as np

from ocr_engine import recognize_plate_text
from car_classifier import identify_vehicle_make_model

logger = logging.getLogger("platescan.detector")

# Model configurations
HF_REPO_ID = "Koushim/yolov8-license-plate-detection"
HF_FILENAME = "best.pt"
LOCAL_MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
LOCAL_WEIGHTS_PATH = os.path.join(LOCAL_MODEL_DIR, "yolov8n_plate.pt")

_yolo_model = None

def get_yolo_model():
    """
    Loads or downloads the fine-tuned YOLOv8 license plate detector model.
    Falls back gracefully to alternative weights if needed.
    """
    global _yolo_model
    if _yolo_model is not None:
        return _yolo_model

    os.makedirs(LOCAL_MODEL_DIR, exist_ok=True)

    # 1. Check local cached file
    if os.path.exists(LOCAL_WEIGHTS_PATH) and os.path.getsize(LOCAL_WEIGHTS_PATH) > 1000000:
        logger.info(f"Loading local YOLOv8 plate weights from {LOCAL_WEIGHTS_PATH}")
        try:
            from ultralytics import YOLO
            _yolo_model = YOLO(LOCAL_WEIGHTS_PATH)
            return _yolo_model
        except Exception as e:
            logger.warning(f"Failed to load cached model {LOCAL_WEIGHTS_PATH}: {e}")

    # 2. Download from HuggingFace
    try:
        from huggingface_hub import hf_hub_download
        from ultralytics import YOLO
        logger.info(f"Downloading license plate detector weights from HuggingFace ({HF_REPO_ID})...")
        downloaded_path = hf_hub_download(repo_id=HF_REPO_ID, filename=HF_FILENAME, local_dir=LOCAL_MODEL_DIR)
        
        # Rename/copy to standardized local path if different
        if downloaded_path != LOCAL_WEIGHTS_PATH:
            import shutil
            shutil.copy2(downloaded_path, LOCAL_WEIGHTS_PATH)

        _yolo_model = YOLO(LOCAL_WEIGHTS_PATH)
        logger.info("YOLOv8 license plate model loaded successfully.")
        return _yolo_model
    except Exception as e:
        logger.error(f"Hugging Face download failed: {e}. Attempting fallback.")

    # 3. Fallback: Base YOLOv8 nano or contour detector
    try:
        from ultralytics import YOLO
        logger.info("Loading default yolov8n model as detector fallback...")
        _yolo_model = YOLO("yolov8n.pt")
        return _yolo_model
    except Exception as e:
        logger.error(f"Could not initialize YOLO model: {e}")
        _yolo_model = False
        return None

def fallback_contour_detect(image_bgr: np.ndarray):
    """
    Classical computer vision plate localization fallback (OpenCV Morphological Filtering)
    used if neural model weights are temporarily unavailable.
    """
    h, w = image_bgr.shape[:2]
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    
    # Sobel gradient along X axis to emphasize vertical plate edges
    grad_x = cv2.Sobel(gray, cv2.CV_16S, 1, 0, ksize=3)
    grad_x = cv2.convertScaleAbs(grad_x)

    # Morphological closing with rectangular kernel typical of license plates (ratio ~3:1 to 5:1)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (17, 5))
    closed = cv2.morphologyEx(grad_x, cv2.MORPH_CLOSE, kernel)

    # Binarize
    _, thresh = cv2.threshold(closed, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidates = []

    for c in contours:
        x, y, cw, ch = cv2.boundingRect(c)
        aspect_ratio = cw / float(max(ch, 1))
        area = cw * ch
        # Typical license plate characteristics: aspect ratio between 2.0 and 6.0, reasonable size
        if 2.0 <= aspect_ratio <= 6.0 and (w * h * 0.002) <= area <= (w * h * 0.25):
            candidates.append((x, y, cw, ch, 0.65))

    # Sort by proximity to lower-middle region where plates usually reside
    candidates.sort(key=lambda b: abs((b[0] + b[2]/2) - w/2) + abs((b[1] + b[3]/2) - h*0.65))
    return candidates[:2]

def draw_hud_bounding_box(image_bgr: np.ndarray, x: int, y: int, w: int, h: int, label: str, conf: float) -> np.ndarray:
    """
    Draws a sleek, automotive HUD-style bounding box around the detected plate with corner brackets.
    """
    annotated = image_bgr.copy()
    x2, y2 = x + w, y + h

    # Primary box (Neon Racing Red / Amber)
    color_border = (0, 30, 235)  # BGR for racing red/amber
    color_accent = (255, 210, 0)  # BGR for cyan highlight
    thickness = 2
    
    cv2.rectangle(annotated, (x, y), (x2, y2), color_border, thickness)

    # Corner brackets for futuristic HUD aesthetic
    corner_len = max(10, min(w // 4, h // 4))
    bracket_thickness = 3
    
    # Top-Left
    cv2.line(annotated, (x, y), (x + corner_len, y), color_accent, bracket_thickness)
    cv2.line(annotated, (x, y), (x, y + corner_len), color_accent, bracket_thickness)
    # Top-Right
    cv2.line(annotated, (x2, y), (x2 - corner_len, y), color_accent, bracket_thickness)
    cv2.line(annotated, (x2, y), (x2, y + corner_len), color_accent, bracket_thickness)
    # Bottom-Left
    cv2.line(annotated, (x, y2), (x + corner_len, y2), color_accent, bracket_thickness)
    cv2.line(annotated, (x, y2), (x, y2 - corner_len), color_accent, bracket_thickness)
    # Bottom-Right
    cv2.line(annotated, (x2, y2), (x2 - corner_len, y2), color_accent, bracket_thickness)
    cv2.line(annotated, (x2, y2), (x2, y2 - corner_len), color_accent, bracket_thickness)

    # Badge label above plate
    badge_text = f"{label} ({int(conf * 100)}%)"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.55
    text_thickness = 1
    (text_w, text_h), baseline = cv2.getTextSize(badge_text, font, font_scale, text_thickness)

    badge_y1 = max(0, y - text_h - 10)
    badge_y2 = y
    badge_x1 = x
    badge_x2 = x + text_w + 12

    # Draw badge background
    cv2.rectangle(annotated, (badge_x1, badge_y1), (badge_x2, badge_y2), (20, 23, 30), cv2.FILLED)
    cv2.rectangle(annotated, (badge_x1, badge_y1), (badge_x2, badge_y2), color_border, 1)

    # Draw text inside badge
    cv2.putText(annotated, badge_text, (badge_x1 + 6, badge_y2 - 5), font, font_scale, (255, 255, 255), text_thickness, cv2.LINE_AA)

    return annotated

def scan_vehicle_image(image_bgr: np.ndarray, conf_threshold: float = 0.25) -> dict:
    """
    Main detection pipeline:
    1. Runs YOLO model to detect license plate coordinates.
    2. Crops plate region(s).
    3. Runs OCR engine on the crop.
    4. Annotates image with coordinates and OCR tag.
    5. Returns structured telemetry dictionary.
    """
    if image_bgr is None or image_bgr.size == 0:
        return {"success": False, "error": "Invalid or empty image provided"}

    img_h, img_w = image_bgr.shape[:2]
    model = get_yolo_model()

    detected_boxes = []

    if model:
        try:
            # Run YOLO prediction (CPU inference, 640x640 resize)
            results = model.predict(source=image_bgr, conf=conf_threshold, verbose=False, device='cpu')
            
            for res in results:
                boxes = res.boxes
                for box in boxes:
                    xyxy = box.xyxy[0].cpu().numpy()
                    x1, y1, x2, y2 = [int(v) for v in xyxy]
                    conf = float(box.conf[0].cpu().numpy())
                    cls_id = int(box.cls[0].cpu().numpy())

                    # Clamp coordinates within image bounds
                    x1 = max(0, min(x1, img_w - 1))
                    y1 = max(0, min(y1, img_h - 1))
                    x2 = max(x1 + 1, min(x2, img_w))
                    y2 = max(y1 + 1, min(y2, img_h))
                    
                    bw = x2 - x1
                    bh = y2 - y1

                    detected_boxes.append((x1, y1, bw, bh, conf))
        except Exception as e:
            logger.error(f"YOLO inference error: {e}. Trying classical CV fallback.")

    # If YOLO didn't yield or failed, try classical CV
    if not detected_boxes:
        logger.info("Checking classical CV fallback for candidate plate regions...")
        detected_boxes = fallback_contour_detect(image_bgr)

    # If still no plates detected:
    if not detected_boxes:
        vehicle_info = identify_vehicle_make_model(image_bgr)
        return {
            "success": True,
            "plate_detected": False,
            "plates_count": 0,
            "image_dimensions": {
                "width": img_w,
                "height": img_h,
                "channels": 3
            },
            "plates": [],
            "primary_plate": None,
            "vehicle_intelligence": vehicle_info,
            "message": "No vehicle number plate detected in the image."
        }

    # Sort plates by confidence descending
    detected_boxes.sort(key=lambda b: b[4], reverse=True)

    annotated_image = image_bgr.copy()
    plates_data = []

    for idx, (bx, by, bw, bh, conf) in enumerate(detected_boxes):
        # Extract crop with slight padding for OCR
        pad_x = int(bw * 0.05)
        pad_y = int(bh * 0.08)
        crop_x1 = max(0, bx - pad_x)
        crop_y1 = max(0, by - pad_y)
        crop_x2 = min(img_w, bx + bw + pad_x)
        crop_y2 = min(img_h, by + bh + pad_y)

        plate_crop = image_bgr[crop_y1:crop_y2, crop_x1:crop_x2]

        # Base64 crop for high-res plate inspection preview
        crop_b64 = ""
        if plate_crop is not None and plate_crop.size > 0:
            try:
                _, crop_buf = cv2.imencode('.jpg', plate_crop, [cv2.IMWRITE_JPEG_QUALITY, 92])
                crop_b64 = base64.b64encode(crop_buf).decode('utf-8')
            except Exception:
                pass

        # Run OCR
        ocr_result = recognize_plate_text(plate_crop)

        # Label for annotation HUD
        display_label = ocr_result["text"] if ocr_result["text"] else "LICENSE PLATE"

        # Draw box on annotated image
        annotated_image = draw_hud_bounding_box(
            annotated_image, bx, by, bw, bh, display_label, conf
        )

        plate_entry = {
            "index": idx + 1,
            "detection_confidence": round(float(conf), 4),
            "crop_base64": crop_b64,
            "bounding_box": {
                "x": int(bx),
                "y": int(by),
                "width": int(bw),
                "height": int(bh),
                "x2": int(bx + bw),
                "y2": int(by + bh),
                "normalized": {
                    "x": round(bx / img_w, 4),
                    "y": round(by / img_h, 4),
                    "width": round(bw / img_w, 4),
                    "height": round(bh / img_h, 4)
                }
            },
            "ocr": {
                "text": ocr_result["text"],
                "raw_text": ocr_result["raw_text"],
                "confidence": ocr_result["confidence"],
                "engine": ocr_result["engine"],
                "tokens": ocr_result["tokens"],
                "is_best_effort": True
            }
        }
        plates_data.append(plate_entry)

    # Encode annotated image to Base64 JPEG
    _, buffer = cv2.imencode('.jpg', annotated_image, [cv2.IMWRITE_JPEG_QUALITY, 88])
    annotated_b64 = base64.b64encode(buffer).decode('utf-8')

    # Detect Vehicle Make, Model, Color, and Orientation
    primary_box = plates_data[0]["bounding_box"] if plates_data else None
    vehicle_info = identify_vehicle_make_model(image_bgr, primary_box)

    return {
        "success": True,
        "plate_detected": True,
        "plates_count": len(plates_data),
        "image_dimensions": {
            "width": img_w,
            "height": img_h,
            "channels": 3
        },
        "plates": plates_data,
        "primary_plate": plates_data[0],
        "vehicle_intelligence": vehicle_info,
        "annotated_image_base64": annotated_b64,
        "model_info": {
            "detector": f"YOLOv8 Nano License Plate ({HF_REPO_ID})",
            "ocr": "EasyOCR CRNN",
            "classifier": "Stanford Cars Neural Classifier",
            "device": "CPU"
        }
    }
