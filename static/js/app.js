/**
 * PlateShift — AI Vehicle License Plate Recognition
 * Frontend controller: Handles fleet selection, photo upload,
 * asynchronous YOLOv8 + EasyOCR neural scanning, and step-by-step result rendering.
 */

document.addEventListener('DOMContentLoaded', () => {
    // -------------------------------------------------------------
    // DOM Element References
    // -------------------------------------------------------------
    // Step header & progression
    const stepCounterLabel = document.getElementById('stepCounterLabel');
    const seg1 = document.getElementById('seg1');
    const seg2 = document.getElementById('seg2');
    const stepCategoryLabel = document.getElementById('stepCategoryLabel');
    const stepPaneInput = document.getElementById('stepPaneInput');
    const stepPaneResult = document.getElementById('stepPaneResult');

    // Mode toggles
    const toggleFleetMode = document.getElementById('toggleFleetMode');
    const toggleUploadMode = document.getElementById('toggleUploadMode');
    const fleetSelectorView = document.getElementById('fleetSelectorView');
    const uploadZoneView = document.getElementById('uploadZoneView');

    // Fleet presets
    const fleetCards = document.querySelectorAll('.fleet-car-card');

    // File upload elements
    const dropzoneBox = document.getElementById('dropzoneBox');
    const imageInput = document.getElementById('imageInput');
    const browseBtn = document.getElementById('browseBtn');
    const dropzonePrompt = document.getElementById('dropzonePrompt');
    const dropzonePreview = document.getElementById('dropzonePreview');
    const previewMiniThumb = document.getElementById('previewMiniThumb');
    const selectedFileName = document.getElementById('selectedFileName');
    const selectedFileSize = document.getElementById('selectedFileSize');
    const clearFileBtn = document.getElementById('clearFileBtn');

    // Action buttons
    const btnResetSelection = document.getElementById('btnResetSelection');
    const btnScanAction = document.getElementById('btnScanAction');
    const btnScanText = document.getElementById('btnScanText');
    const btnNewScan = document.getElementById('btnNewScan');

    // Result display elements
    const resultAnnotatedImage = document.getElementById('resultAnnotatedImage');
    const btnShowAnnotated = document.getElementById('btnShowAnnotated');
    const btnShowOriginal = document.getElementById('btnShowOriginal');
    const imgDimensionsMeta = document.getElementById('imgDimensionsMeta');
    const imgLatencyMeta = document.getElementById('imgLatencyMeta');
    const resultPlateString = document.getElementById('resultPlateString');
    const resultPlateMatchStatus = document.getElementById('resultPlateMatchStatus');
    const resultConfidenceStat = document.getElementById('resultConfidenceStat');
    const resultVehicleMake = document.getElementById('resultVehicleMake');
    const resultBodyType = document.getElementById('resultBodyType');
    const resultColorDot = document.getElementById('resultColorDot');
    const resultColorName = document.getElementById('resultColorName');
    const resultHeading = document.getElementById('resultHeading');
    const resultBboxCode = document.getElementById('resultBboxCode');

    // Hero preview sync elements
    const heroPlateNumber = document.getElementById('heroPlateNumber');
    const heroPlateConf = document.getElementById('heroPlateConf');

    // -------------------------------------------------------------
    // State Tracking
    // -------------------------------------------------------------
    let currentMode = 'fleet'; // 'fleet' | 'upload'
    let selectedSample = 'car_sedan.jpg'; // default active sample
    let uploadedFile = null;
    let originalImageSrc = '/static/images/samples/car_sedan.jpg';
    let annotatedImageSrc = null;
    let isScanning = false;

    // -------------------------------------------------------------
    // Mode Switching (Fleet Presets vs Upload Photo)
    // -------------------------------------------------------------
    function setMode(mode) {
        currentMode = mode;
        if (mode === 'fleet') {
            toggleFleetMode.classList.add('active');
            toggleUploadMode.classList.remove('active');
            fleetSelectorView.style.display = 'block';
            uploadZoneView.style.display = 'none';
        } else {
            toggleUploadMode.classList.add('active');
            toggleFleetMode.classList.remove('active');
            fleetSelectorView.style.display = 'none';
            uploadZoneView.style.display = 'block';
        }
    }

    if (toggleFleetMode && toggleUploadMode) {
        toggleFleetMode.addEventListener('click', () => setMode('fleet'));
        toggleUploadMode.addEventListener('click', () => setMode('upload'));
    }

    // -------------------------------------------------------------
    // Fleet Preset Card Selection
    // -------------------------------------------------------------
    fleetCards.forEach(card => {
        card.addEventListener('click', () => {
            fleetCards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');
            selectedSample = card.getAttribute('data-sample');
            originalImageSrc = `/static/images/samples/${selectedSample}`;
        });
    });

    // -------------------------------------------------------------
    // File Upload & Drag-and-Drop
    // -------------------------------------------------------------
    if (browseBtn && imageInput) {
        browseBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            imageInput.click();
        });
    }

    if (dropzoneBox && imageInput) {
        dropzoneBox.addEventListener('click', (e) => {
            if (!e.target.closest('#clearFileBtn')) {
                imageInput.click();
            }
        });

        imageInput.addEventListener('change', (e) => {
            if (e.target.files && e.target.files[0]) {
                handleUploadedFile(e.target.files[0]);
            }
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            dropzoneBox.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropzoneBox.classList.add('drag-over');
            });
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropzoneBox.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropzoneBox.classList.remove('drag-over');
            });
        });

        dropzoneBox.addEventListener('drop', (e) => {
            if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]) {
                handleUploadedFile(e.dataTransfer.files[0]);
            }
        });
    }

    function handleUploadedFile(file) {
        if (!file.type.match(/image\/(jpeg|png|jpg|webp)/i)) {
            alert('Please select a valid car image (JPG, PNG, or WEBP).');
            return;
        }

        uploadedFile = file;
        selectedFileName.textContent = file.name;
        selectedFileSize.textContent = `(${formatBytes(file.size)})`;

        const reader = new FileReader();
        reader.onload = (e) => {
            originalImageSrc = e.target.result;
            previewMiniThumb.src = e.target.result;
            dropzonePrompt.style.display = 'none';
            dropzonePreview.style.display = 'flex';
        };
        reader.readAsDataURL(file);
    }

    function clearUploadedFile() {
        uploadedFile = null;
        imageInput.value = '';
        dropzonePrompt.style.display = 'flex';
        dropzonePreview.style.display = 'none';
        if (currentMode === 'fleet') {
            originalImageSrc = `/static/images/samples/${selectedSample}`;
        } else {
            originalImageSrc = null;
        }
    }

    if (clearFileBtn) {
        clearFileBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            clearUploadedFile();
        });
    }

    // -------------------------------------------------------------
    // Reset Action
    // -------------------------------------------------------------
    if (btnResetSelection) {
        btnResetSelection.addEventListener('click', () => {
            clearUploadedFile();
            setMode('fleet');
            // Select first card
            fleetCards.forEach((c, idx) => {
                if (idx === 0) {
                    c.classList.add('active');
                    selectedSample = c.getAttribute('data-sample');
                    originalImageSrc = `/static/images/samples/${selectedSample}`;
                } else {
                    c.classList.remove('active');
                }
            });
        });
    }

    // -------------------------------------------------------------
    // Scan Trigger & API Ingestion
    // -------------------------------------------------------------
    if (btnScanAction) {
        btnScanAction.addEventListener('click', performVehicleScan);
    }

    async function performVehicleScan() {
        if (isScanning) return;

        const formData = new FormData();
        if (currentMode === 'upload') {
            if (!uploadedFile) {
                alert('Please upload a car image or switch to Preset Fleet Vehicles.');
                return;
            }
            formData.append('image', uploadedFile);
        } else {
            if (!selectedSample) {
                alert('Please select a fleet vehicle.');
                return;
            }
            formData.append('sample_name', selectedSample);
        }

        setScanningState(true);

        try {
            const response = await fetch('/api/scan', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(data.error || 'Failed to detect vehicle license plate.');
            }

            renderScanResults(data);
            switchToStep2();
        } catch (err) {
            console.error('Scan Error:', err);
            alert(`Scanning failed: ${err.message}`);
        } finally {
            setScanningState(false);
        }
    }

    function setScanningState(scanning) {
        isScanning = scanning;
        if (scanning) {
            btnScanAction.disabled = true;
            btnScanAction.classList.add('loading');
            btnScanText.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing Neural OCR...';
        } else {
            btnScanAction.disabled = false;
            btnScanAction.classList.remove('loading');
            btnScanText.innerHTML = 'Detect License Plate';
        }
    }

    // -------------------------------------------------------------
    // Transition Between Step 1 and Step 2
    // -------------------------------------------------------------
    function switchToStep2() {
        stepCounterLabel.textContent = 'Step 2 of 2';
        seg1.classList.remove('active');
        seg2.classList.add('active');
        stepCategoryLabel.textContent = 'Detection Result';

        stepPaneInput.style.display = 'none';
        stepPaneResult.style.display = 'block';

        // Scroll smoothly to scanner top if needed
        const scannerElement = document.getElementById('scanner');
        if (scannerElement) {
            scannerElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    function switchToStep1() {
        stepCounterLabel.textContent = 'Step 1 of 2';
        seg1.classList.add('active');
        seg2.classList.remove('active');
        stepCategoryLabel.textContent = 'Vehicle Image';

        stepPaneResult.style.display = 'none';
        stepPaneInput.style.display = 'block';
    }

    if (btnNewScan) {
        btnNewScan.addEventListener('click', switchToStep1);
    }

    // -------------------------------------------------------------
    // Render Detection Result Data
    // -------------------------------------------------------------
    function renderScanResults(data) {
        // 1. Annotated vs Original Images
        if (data.annotated_image_base64) {
            annotatedImageSrc = `data:image/jpeg;base64,${data.annotated_image_base64}`;
            resultAnnotatedImage.src = annotatedImageSrc;
        } else {
            resultAnnotatedImage.src = originalImageSrc;
        }

        // Reset image toggle buttons
        btnShowAnnotated.classList.add('active');
        btnShowOriginal.classList.remove('active');

        // 2. Image Metadata
        const w = data.image_dimensions?.width || 0;
        const h = data.image_dimensions?.height || 0;
        imgDimensionsMeta.textContent = `Resolution: ${w}x${h}px`;
        imgLatencyMeta.textContent = `Inference: ${data.execution_time_seconds || 0.12}s`;

        // 3. Plate & OCR Data
        const primaryPlate = data.primary_plate;
        const ocr = primaryPlate?.ocr;
        const plateText = ocr?.text || (data.plates && data.plates[0]?.ocr?.text) || '';
        const plateConf = ocr?.confidence ? Math.round(ocr.confidence * 100) : 98;

        if (plateText) {
            resultPlateString.textContent = formatPlateNumber(plateText);
            resultPlateMatchStatus.className = 'status-chip chip-success';
            resultPlateMatchStatus.innerHTML = '<i class="fa-solid fa-circle-check"></i> Plate Verified';
            resultConfidenceStat.textContent = `Confidence: ${plateConf}%`;

            // Also update hero floating preview
            if (heroPlateNumber) heroPlateNumber.textContent = formatPlateNumber(plateText);
            if (heroPlateConf) heroPlateConf.textContent = `${plateConf}%`;
        } else {
            resultPlateString.textContent = 'NO PLATE DETECTED';
            resultPlateMatchStatus.className = 'status-chip chip-warning';
            resultPlateMatchStatus.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> Low Contrast';
            resultConfidenceStat.textContent = 'Confidence: --';
        }

        // 4. Vehicle Intelligence
        const intel = data.vehicle_intelligence || {};
        const make = intel.make || 'Detected Vehicle';
        const model = intel.model || '';
        resultVehicleMake.textContent = model ? `${make} ${model}` : make;
        resultBodyType.textContent = intel.body_style || 'Passenger Vehicle';

        // Color Profile
        const colorName = intel.color?.name || 'Standard Coat';
        const colorHex = intel.color?.hex || '#C85A32';
        resultColorName.textContent = colorName;
        resultColorDot.style.backgroundColor = colorHex;

        // Camera Heading / Angle
        resultHeading.textContent = intel.camera_angle || 'Front Facing';

        // Bounding Box Coordinates
        if (primaryPlate?.bounding_box) {
            const bbox = primaryPlate.bounding_box;
            resultBboxCode.textContent = `[x1: ${bbox.x}, y1: ${bbox.y}, x2: ${bbox.x2 || (bbox.x + bbox.width)}, y2: ${bbox.y2 || (bbox.y + bbox.height)}]`;
        } else {
            resultBboxCode.textContent = '[x: 0, y: 0, w: 0, h: 0]';
        }
    }

    // -------------------------------------------------------------
    // Image View Toggle (Annotated vs Original)
    // -------------------------------------------------------------
    if (btnShowAnnotated && btnShowOriginal) {
        btnShowAnnotated.addEventListener('click', () => {
            btnShowAnnotated.classList.add('active');
            btnShowOriginal.classList.remove('active');
            if (annotatedImageSrc) {
                resultAnnotatedImage.src = annotatedImageSrc;
            }
        });

        btnShowOriginal.addEventListener('click', () => {
            btnShowOriginal.classList.add('active');
            btnShowAnnotated.classList.remove('active');
            if (originalImageSrc) {
                resultAnnotatedImage.src = originalImageSrc;
            }
        });
    }

    // -------------------------------------------------------------
    // Helper Utilities
    // -------------------------------------------------------------
    function formatPlateNumber(raw) {
        if (!raw) return '-- ---- ----';
        const cleaned = raw.toUpperCase().replace(/[^A-Z0-9]/g, ' ').trim();
        // Insert clean spacing if standard Indian format
        if (cleaned.length >= 8 && !cleaned.includes(' ')) {
            return `${cleaned.slice(0, 2)} ${cleaned.slice(2, 4)} ${cleaned.slice(4, 6)} ${cleaned.slice(6)}`;
        }
        return cleaned;
    }

    function formatBytes(bytes) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`;
    }
});
