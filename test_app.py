"""
Unit and Integration Test Suite for APEX // PlateScan Flask Application
"""

import io
import json
import cv2
import numpy as np
from app import app

def test_routes():
    print("\n--- Starting APEX PlateScan Automated Test Suite ---")
    client = app.test_client()

    # Test 1: Frontend Route
    resp = client.get('/')
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    assert b"PlateShift" in resp.data
    print("[PASS] Test 1: GET / serves HTML dashboard.")

    # Test 2: Health API
    resp = client.get('/api/health')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "online"
    assert "YOLOv8" in data["detector"]
    print("[PASS] Test 2: GET /api/health returned online status.")

    # Test 3: Preset Scan 1 - Jaguar XF Luxury Sedan
    resp = client.post('/api/scan', data={'sample_name': 'jaguar_xf.jpg'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True
    assert data["plate_detected"] is True
    box = data["primary_plate"]["bounding_box"]
    assert "x" in box and "y" in box and "width" in box and "height" in box
    v_info = data.get("vehicle_intelligence", {})
    assert "Jaguar" in v_info.get("full_name", "")
    assert v_info.get("color", {}).get("family") == "White"
    print(f"[PASS] Test 3: Preset Jaguar XF scanned successfully. Model: '{v_info['full_name']}', Color: '{v_info['color']['name']}'")

    # Test 4: Preset Scan 2 - Lamborghini Aventador Supercar
    resp = client.post('/api/scan', data={'sample_name': 'lamborghini_aventador.jpg'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True
    assert data["plate_detected"] is True
    v_info = data.get("vehicle_intelligence", {})
    assert "Lamborghini" in v_info.get("full_name", "")
    assert v_info.get("color", {}).get("family") == "Orange"
    print(f"[PASS] Test 4: Preset Lamborghini scanned successfully. Model: '{v_info['full_name']}', Color: '{v_info['color']['name']}'")

    # Test 5: Preset Scan 3 - Vintage Classic Premier Padmini
    resp = client.post('/api/scan', data={'sample_name': 'vintage_classic.jpg'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True
    assert data["plate_detected"] is True
    v_info = data.get("vehicle_intelligence", {})
    assert "Premier" in v_info.get("full_name", "") or "Padmini" in v_info.get("full_name", "")
    ocr_text = data["primary_plate"]["ocr"]["text"]
    print(f"[PASS] Test 5: Preset Vintage Classic scanned successfully. Plate: '{ocr_text}', Model: '{v_info['full_name']}'")

    # Test 6: File Upload via multipart/form-data
    with open('static/images/samples/lamborghini_aventador.jpg', 'rb') as f:
        img_bytes = f.read()
    
    upload_data = {
        'image': (io.BytesIO(img_bytes), 'uploaded_lambo.jpg')
    }
    resp = client.post('/api/scan', data=upload_data, content_type='multipart/form-data')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["plate_detected"] is True
    print("[PASS] Test 6: Multipart image file upload scanned successfully.")

    # Test 7: Negative Case (No Plate in blank image)
    blank_img = np.zeros((300, 300, 3), dtype=np.uint8) + 100
    _, buffer = cv2.imencode('.jpg', blank_img)
    upload_blank = {
        'image': (io.BytesIO(buffer.tobytes()), 'blank.jpg')
    }
    resp = client.post('/api/scan', data=upload_blank, content_type='multipart/form-data')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True
    assert data["plate_detected"] is False
    assert "No vehicle number plate detected" in data["message"]
    print("[PASS] Test 7: Negative case correctly returns plate_detected: False.")

    print("\n=======================================================")
    print("  ALL 7 INTEGRATION TESTS COMPLETED SUCCESSFULLY!")
    print("=======================================================\n")

if __name__ == '__main__':
    test_routes()
