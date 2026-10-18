"""
APEX // PlateScan - Optical Character Recognition (OCR) Engine
Uses EasyOCR (PyTorch CRAFT + CRNN) for local, CPU-friendly license plate text extraction.
"""

import logging
import re
import cv2
import numpy as np

logger = logging.getLogger("platescan.ocr")

# Lazy-loaded EasyOCR reader instance
_easyocr_reader = None

def get_ocr_reader():
    """Lazy initialize the EasyOCR reader to save memory until first scan."""
    global _easyocr_reader
    if _easyocr_reader is None:
        try:
            import easyocr
            logger.info("Initializing EasyOCR reader (CPU mode, English language)...")
            # gpu=False ensures reliable, light CPU execution on standard laptops
            _easyocr_reader = easyocr.Reader(['en'], gpu=False, verbose=False)
            logger.info("EasyOCR reader initialized successfully.")
        except Exception as e:
            logger.warning(f"Could not load EasyOCR: {e}. Falling back to basic extraction.")
            _easyocr_reader = False
    return _easyocr_reader

def clean_plate_text(text: str) -> str:
    """
    Cleans raw OCR output to retain standard license plate characters (alphanumeric, dashes, spaces).
    Removes common punctuation noise (dots, quotes, underscores, special symbols).
    """
    if not text:
        return ""
    # Strip whitespace and common noise characters
    cleaned = re.sub(r'[^A-Za-z0-9\s\-]', '', text).strip()
    # Normalize multiple spaces
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.upper()

def preprocess_plate_crop(crop_bgr: np.ndarray) -> np.ndarray:
    """
    Applies image enhancement to improve OCR recognition on low-contrast or small plate crops.
    """
    if crop_bgr is None or crop_bgr.size == 0:
        return crop_bgr

    h, w = crop_bgr.shape[:2]
    
    # Upscale small plate crops (EasyOCR performs best with plate height >= 60px)
    if h < 70 or w < 160:
        scale = max(70 / max(h, 1), 160 / max(w, 1))
        new_w = int(w * scale)
        new_h = int(h * scale)
        crop_bgr = cv2.resize(crop_bgr, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

    # Convert to grayscale
    gray = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2GRAY)

    # Contrast Limited Adaptive Histogram Equalization (CLAHE) for uneven lighting
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Mild bilateral filtering to preserve edges while smoothing background noise
    denoised = cv2.bilateralFilter(enhanced, 7, 50, 50)

    return denoised

def recognize_plate_text(plate_crop_bgr: np.ndarray) -> dict:
    """
    Extracts license plate text and confidence score from a cropped BGR image of a license plate.

    Returns:
        dict: {
            "text": str,
            "raw_text": str,
            "confidence": float (0.0 to 1.0) or None,
            "tokens": list of dicts with text and confidence,
            "engine": str
        }
    """
    if plate_crop_bgr is None or plate_crop_bgr.size == 0:
        return {
            "text": "",
            "raw_text": "",
            "confidence": None,
            "tokens": [],
            "engine": "none"
        }

    h, w = plate_crop_bgr.shape[:2]
    if h < 3 or w < 6:
        return {
            "text": "",
            "raw_text": "",
            "confidence": None,
            "tokens": [],
            "engine": "none"
        }

    reader = get_ocr_reader()

    # Preprocess image
    try:
        processed_crop = preprocess_plate_crop(plate_crop_bgr)
    except Exception as e:
        logger.warning(f"Preprocessing error: {e}, using raw crop.")
        processed_crop = plate_crop_bgr

    if reader:
        try:
            # EasyOCR readtext on processed image
            results = reader.readtext(processed_crop)
            
            # If processed crop yielded nothing, try on original crop as fallback
            if not results:
                results = reader.readtext(plate_crop_bgr)

            if results:
                tokens = []
                total_conf = 0.0
                all_text_parts = []

                for item in results:
                    # Item format: (bounding_box_corners, text, confidence)
                    _, text, conf = item
                    cleaned = clean_plate_text(text)
                    if cleaned:
                        tokens.append({
                            "text": cleaned,
                            "raw": text,
                            "confidence": round(float(conf), 4)
                        })
                        total_conf += float(conf)
                        all_text_parts.append(cleaned)

                if tokens:
                    final_text = " ".join(all_text_parts)
                    avg_conf = round(total_conf / len(tokens), 4)
                    return {
                        "text": final_text,
                        "raw_text": " ".join([t["raw"] for t in tokens]),
                        "confidence": avg_conf,
                        "tokens": tokens,
                        "engine": "EasyOCR-CRNN"
                    }

        except Exception as e:
            logger.error(f"EasyOCR inference exception: {e}")

    # Fallback if EasyOCR returned no text or is unavailable
    return {
        "text": "",
        "raw_text": "",
        "confidence": None,
        "tokens": [],
        "engine": "EasyOCR (No text resolved)"
    }
