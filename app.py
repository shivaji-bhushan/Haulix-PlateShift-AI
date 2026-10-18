"""
APEX // PlateScan - Main Flask Application Server
Serves the car-themed single-page frontend and provides REST endpoints
for YOLO-based vehicle license plate detection and EasyOCR character recognition.
"""

import logging
import os
import time
import cv2
import numpy as np
from flask import Flask, jsonify, render_template, request, send_from_directory

from detector import scan_vehicle_image

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("platescan.app")

# Initialize Flask app
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
SAMPLES_DIR = os.path.join(STATIC_DIR, "images", "samples")

app = Flask(
    __name__,
    static_folder=STATIC_DIR,
    template_folder=TEMPLATES_DIR
)

# Limit uploads to 16MB and auto-reload templates
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['TEMPLATES_AUTO_RELOAD'] = True

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Renders the main PlateShift interface."""
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health():
    """Service health & telemetry check."""
    return jsonify({
        "status": "online",
        "service": "PlateShift",
        "detector": "YOLOv8 Nano License Plate",
        "ocr": "EasyOCR CRNN",
        "device": "CPU"
    })

@app.route('/api/scan', methods=['POST'])
def scan_plate():
    """
    Primary scanning endpoint.
    Accepts:
      - 'image': File upload via multipart/form-data
      - 'sample_name': Name of a bundled sample image from static/images/samples/
    Returns:
      JSON telemetry including plate detection status, bounding box coordinates,
      image dimensions, OCR extracted text and confidence, and annotated base64 image.
    """
    start_time = time.time()
    img_bgr = None

    # Check for direct file upload
    if 'image' in request.files:
        file = request.files['image']
        if file.filename == '':
            return jsonify({"success": False, "error": "No selected file."}), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                "success": False,
                "error": f"Invalid file format. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            }), 400

        try:
            file_bytes = np.frombuffer(file.read(), np.uint8)
            img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        except Exception as e:
            logger.error(f"Failed to decode uploaded image: {e}")
            return jsonify({"success": False, "error": "Unable to decode image file."}), 400

    # Or check for preset sample selection
    elif 'sample_name' in request.form:
        sample_name = os.path.basename(request.form.get('sample_name', ''))
        sample_path = os.path.join(SAMPLES_DIR, sample_name)
        
        if not os.path.exists(sample_path):
            return jsonify({"success": False, "error": f"Sample preset '{sample_name}' not found."}), 404

        img_bgr = cv2.imread(sample_path)

    else:
        return jsonify({
            "success": False,
            "error": "No vehicle image file or sample preset provided in request."
        }), 400

    if img_bgr is None:
        return jsonify({"success": False, "error": "Image buffer is empty or corrupted."}), 400

    try:
        # Run detection & OCR pipeline
        result = scan_vehicle_image(img_bgr)
        elapsed = round(time.time() - start_time, 2)
        result["execution_time_seconds"] = elapsed
        return jsonify(result)

    except Exception as e:
        logger.exception(f"Unhandled error during plate scan: {e}")
        return jsonify({"success": False, "error": f"Scanning engine error: {str(e)}"}), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"success": False, "error": "File size exceeds the 16MB limit."}), 413

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"success": False, "error": "Internal server processing error."}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print("\n=======================================================")
    print("  [ONLINE] APEX // PlateScan Running Locally")
    print(f"  Dashboard: http://127.0.0.1:{port}")
    print("=======================================================\n")
    app.run(host='127.0.0.1', port=port, debug=False)
