/**
 * Haulix PlateShift — Dashboard Controller
 * Connects vehicle scanning, plate OCR, make & model intelligence,
 * dual circular gauges, and 3D compass heading.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Core Upload & Input Elements
    const dropzoneBox = document.getElementById('dropzoneBox');
    const imageInput = document.getElementById('imageInput');
    const browseBtn = document.getElementById('browseBtn');
    const selectedFileBar = document.getElementById('selectedFileBar');
    const selectedFileName = document.getElementById('selectedFileName');
    const selectedFileSize = document.getElementById('selectedFileSize');
    const clearFileBtn = document.getElementById('clearFileBtn');
    const scanBtn = document.getElementById('scanBtn');
    const presetCards = document.querySelectorAll('.fleet-preset-card');
    const filterPills = document.querySelectorAll('.filter-pill');
    const globalSearchInput = document.getElementById('globalSearchInput');

    // Viewport & Overlays
    const viewportIdle = document.getElementById('viewportIdle');
    const scanLoadingOverlay = document.getElementById('scanLoadingOverlay');
    const imageViewerFrame = document.getElementById('imageViewerFrame');
    const displayImage = document.getElementById('displayImage');
    const noPlateCard = document.getElementById('noPlateCard');
    const rawJsonPre = document.getElementById('rawJsonPre');
    const latencyVal = document.getElementById('latencyVal');

    // Floating Telemetry HUD Elements
    const floatingHudCard = document.getElementById('floatingHudCard');
    const floatingPlateId = document.getElementById('floatingPlateId');
    const floatingStatusPill = document.getElementById('floatingStatusPill');
    const floatingModelName = document.getElementById('floatingModelName');
    const floatingBodyType = document.getElementById('floatingBodyType');
    const floatingColorDot = document.getElementById('floatingColorDot');
    const floatingColorName = document.getElementById('floatingColorName');
    const floatingCoords = document.getElementById('floatingCoords');
    const floatingDims = document.getElementById('floatingDims');

    // Dual Circular Gauges Elements
    const speedoNeedle = document.getElementById('speedoNeedle');
    const valPlateConfNum = document.getElementById('valPlateConfNum');
    const fluidWaveBg = document.getElementById('fluidWaveBg');
    const valOcrConfNum = document.getElementById('valOcrConfNum');

    // 3D Compass Elements
    const compassNeedle = document.getElementById('compassNeedle');
    const compassHeadingText = document.getElementById('compassHeadingText');
    const compassViewText = document.getElementById('compassViewText');

    // Top Metric Indicators
    const metricPlateScore = document.getElementById('metricPlateScore');
    const metricModelStatus = document.getElementById('metricModelStatus');
    const metricColorStatus = document.getElementById('metricColorStatus');

    // Toggle Controls
    const toggleOverlayBBox = document.getElementById('toggleOverlayBBox');
    const toggleHudCard = document.getElementById('toggleHudCard');
    const toggleAnnotatedBtn = document.getElementById('toggleAnnotatedBtn');
    const toggleOriginalBtn = document.getElementById('toggleOriginalBtn');

    // State Variables
    let currentFile = null;
    let currentSampleName = null;
    let originalImageSrc = null;
    let annotatedImageSrc = null;

    // ---------------------------------------------------------
    // File Ingestion & Drag/Drop
    // ---------------------------------------------------------
    browseBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        imageInput.click();
    });

    dropzoneBox.addEventListener('click', (e) => {
        if (!e.target.closest('#clearFileBtn') && !e.target.closest('#scanBtn')) {
            imageInput.click();
        }
    });

    imageInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
            handleFileSelect(e.target.files[0]);
        }
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropzoneBox.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzoneBox.style.borderColor = 'var(--accent-green)';
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropzoneBox.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzoneBox.style.borderColor = '';
        });
    });

    dropzoneBox.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        if (dt && dt.files && dt.files[0]) {
            handleFileSelect(dt.files[0]);
        }
    });

    clearFileBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        resetFileInput();
    });

    function handleFileSelect(file) {
        if (!file.type.match(/image\/(jpeg|png|jpg|webp)/i)) {
            alert('Please select a valid car image (JPG, PNG, or WEBP).');
            return;
        }

        currentFile = file;
        currentSampleName = null;

        selectedFileName.textContent = file.name;
        selectedFileSize.textContent = `(${formatBytes(file.size)})`;
        selectedFileBar.classList.remove('hidden');

        presetCards.forEach(c => c.style.borderColor = 'var(--border-subtle)');
        scanBtn.disabled = false;

        const reader = new FileReader();
        reader.onload = (e) => {
            originalImageSrc = e.target.result;
            annotatedImageSrc = null;
            showImagePreview(originalImageSrc);
        };
        reader.readAsDataURL(file);
    }

    function resetFileInput() {
        currentFile = null;
        currentSampleName = null;
        originalImageSrc = null;
        annotatedImageSrc = null;
        imageInput.value = '';
        selectedFileBar.classList.add('hidden');
        scanBtn.disabled = true;

        presetCards.forEach(c => c.style.borderColor = 'var(--border-subtle)');

        imageViewerFrame.classList.add('hidden');
        viewportIdle.classList.remove('hidden');
        floatingHudCard.style.opacity = '0';
        noPlateCard.classList.add('hidden');
    }

    // ---------------------------------------------------------
    // Preset Fleet Selection
    // ---------------------------------------------------------
    presetCards.forEach(card => {
        card.addEventListener('click', () => {
            const sampleName = card.getAttribute('data-sample');
            selectPreset(sampleName, card);
        });
    });

    function selectPreset(sampleName, activeCard) {
        currentFile = null;
        currentSampleName = sampleName;
        imageInput.value = '';

        presetCards.forEach(c => c.style.borderColor = 'var(--border-subtle)');
        activeCard.style.borderColor = 'var(--accent-green)';

        selectedFileName.textContent = sampleName;
        selectedFileSize.textContent = '(Preset)';
        selectedFileBar.classList.remove('hidden');

        scanBtn.disabled = false;

        const sampleUrl = `/static/images/samples/${sampleName}`;
        originalImageSrc = sampleUrl;
        annotatedImageSrc = null;
        showImagePreview(sampleUrl);
    }

    function showImagePreview(src) {
        displayImage.src = src;
        viewportIdle.classList.add('hidden');
        imageViewerFrame.classList.remove('hidden');
        floatingHudCard.style.opacity = '0';
        noPlateCard.classList.add('hidden');
        setActiveToggle('original');
    }

    // ---------------------------------------------------------
    // Viewport Toggle Controls (Annotated vs Original)
    // ---------------------------------------------------------
    toggleAnnotatedBtn.addEventListener('click', () => {
        if (annotatedImageSrc) {
            displayImage.src = annotatedImageSrc;
            setActiveToggle('annotated');
            if (toggleOverlayBBox) toggleOverlayBBox.checked = true;
        }
    });

    toggleOriginalBtn.addEventListener('click', () => {
        if (originalImageSrc) {
            displayImage.src = originalImageSrc;
            setActiveToggle('original');
            if (toggleOverlayBBox) toggleOverlayBBox.checked = false;
        }
    });

    if (toggleOverlayBBox) {
        toggleOverlayBBox.addEventListener('change', () => {
            if (toggleOverlayBBox.checked && annotatedImageSrc) {
                displayImage.src = annotatedImageSrc;
                setActiveToggle('annotated');
            } else if (originalImageSrc) {
                displayImage.src = originalImageSrc;
                setActiveToggle('original');
            }
        });
    }

    if (toggleHudCard) {
        toggleHudCard.addEventListener('change', () => {
            floatingHudCard.style.display = toggleHudCard.checked ? 'flex' : 'none';
        });
    }

    function setActiveToggle(type) {
        if (type === 'annotated') {
            toggleAnnotatedBtn.classList.add('active');
            toggleOriginalBtn.classList.remove('active');
        } else {
            toggleOriginalBtn.classList.add('active');
            toggleAnnotatedBtn.classList.remove('active');
        }
    }

    // ---------------------------------------------------------
    // Run Scanner API
    // ---------------------------------------------------------
    scanBtn.addEventListener('click', async () => {
        if (!currentFile && !currentSampleName) return;

        scanBtn.disabled = true;
        scanLoadingOverlay.classList.remove('hidden');
        noPlateCard.classList.add('hidden');

        const formData = new FormData();
        if (currentFile) {
            formData.append('image', currentFile);
        } else if (currentSampleName) {
            formData.append('sample_name', currentSampleName);
        }

        const startTime = performance.now();

        try {
            const response = await fetch('/api/scan', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            const elapsed = ((performance.now() - startTime) / 1000).toFixed(2);

            scanLoadingOverlay.classList.add('hidden');
            scanBtn.disabled = false;

            if (!response.ok || !data.success) {
                alert(`Analysis Error: ${data.error || 'Server error.'}`);
                return;
            }

            renderDashboardTelemetry(data, elapsed);

        } catch (err) {
            console.error('Scan request failed:', err);
            scanLoadingOverlay.classList.add('hidden');
            scanBtn.disabled = false;
            alert(`Connection error: ${err.message}`);
        }
    });

    // ---------------------------------------------------------
    // Render Complete Telemetry, Gauges, Compass & Car Model
    // ---------------------------------------------------------
    function renderDashboardTelemetry(data, elapsed) {
        rawJsonPre.textContent = JSON.stringify(data, null, 2);
        latencyVal.textContent = `Scan time: ${data.execution_time_seconds || elapsed}s`;

        // 1. Vehicle Intelligence (Make & Model, Color, Orientation)
        const vInfo = data.vehicle_intelligence || {};

        if (vInfo.full_name) {
            floatingModelName.textContent = `${vInfo.full_name} • ${vInfo.year_range || '2022'} • ${vInfo.body_type || 'Vehicle'}`;
            metricModelStatus.textContent = vInfo.make;
        }

        if (vInfo.body_type) {
            floatingBodyType.textContent = vInfo.body_type;
        }

        // Color Swatch
        if (vInfo.color) {
            floatingColorName.textContent = vInfo.color.name;
            floatingColorDot.style.backgroundColor = vInfo.color.hex || '#e11d48';
            metricColorStatus.textContent = vInfo.color.name;
        }

        // 3D Compass Heading
        if (vInfo.orientation) {
            const deg = vInfo.orientation.degrees !== undefined ? vInfo.orientation.degrees : 0;
            compassNeedle.style.transform = `rotate(${deg}deg)`;
            compassHeadingText.textContent = `${vInfo.orientation.heading} (${deg}°)`;
            compassViewText.textContent = vInfo.orientation.view;
        }

        // 2. Handle Plate Detection State
        if (!data.plate_detected) {
            noPlateCard.classList.remove('hidden');
            floatingPlateId.textContent = "PLATE NOT FOUND";
            floatingStatusPill.textContent = "Unregistered";
            floatingStatusPill.style.color = "var(--accent-red)";
            floatingStatusPill.style.borderColor = "rgba(239, 68, 68, 0.3)";
            floatingStatusPill.style.background = "rgba(239, 68, 68, 0.15)";
            
            valPlateConfNum.textContent = "0%";
            speedoNeedle.style.transform = "rotate(-90deg)";
            valOcrConfNum.textContent = "N/A";
            fluidWaveBg.style.height = "0%";

            metricPlateScore.textContent = "None";
            metricPlateScore.className = "text-amber";

            floatingHudCard.style.opacity = '1';
            return;
        }

        // Plate Found!
        noPlateCard.classList.add('hidden');
        floatingHudCard.style.opacity = '1';

        // Update image to annotated view
        if (data.annotated_image_base64) {
            annotatedImageSrc = `data:image/jpeg;base64,${data.annotated_image_base64}`;
            displayImage.src = annotatedImageSrc;
            setActiveToggle('annotated');
            if (toggleOverlayBBox) toggleOverlayBBox.checked = true;
        }

        const plate = data.primary_plate;
        const box = plate.bounding_box;
        const dims = data.image_dimensions;

        // Plate ID text
        const ocrText = (plate.ocr && plate.ocr.text && plate.ocr.text.trim()) 
            ? plate.ocr.text.trim().toUpperCase() 
            : 'UNREADABLE PLATE';
        floatingPlateId.textContent = ocrText;
        floatingStatusPill.textContent = "Verified";
        floatingStatusPill.style.color = "var(--accent-green)";
        floatingStatusPill.style.borderColor = "rgba(16, 185, 129, 0.3)";
        floatingStatusPill.style.background = "rgba(16, 185, 129, 0.15)";

        // Coordinates & Dims
        floatingCoords.textContent = `${box.x}, ${box.y} px`;
        floatingDims.textContent = `${box.width} × ${box.height} px`;

        // 3. Update Circular Gauges
        // Gauge 1: Semicircular Speedometer
        const detConf = Math.round(plate.detection_confidence * 100);
        valPlateConfNum.textContent = `${detConf}%`;
        metricPlateScore.textContent = `${detConf}%`;
        metricPlateScore.className = "text-green";

        // Map 0-100% to needle angle (-90deg to +90deg)
        const needleAngle = -90 + (detConf * 1.8);
        speedoNeedle.style.transform = `rotate(${needleAngle}deg)`;

        // Gauge 2: Circular Fluid Level (OCR Confidence)
        const ocrConf = plate.ocr.confidence !== null ? Math.round(plate.ocr.confidence * 100) : 0;
        valOcrConfNum.textContent = plate.ocr.confidence !== null ? `${ocrConf}%` : 'N/A';
        fluidWaveBg.style.height = `${Math.min(100, Math.max(0, ocrConf))}%`;
    }

    // Filter pills interaction
    filterPills.forEach(pill => {
        pill.addEventListener('click', () => {
            filterPills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');
            const cat = (pill.getAttribute('data-filter') || '').toLowerCase();

            presetCards.forEach(card => {
                const sampleName = (card.getAttribute('data-sample') || '').toLowerCase();
                const cardText = card.textContent.toLowerCase();
                if (cat === 'all') {
                    card.style.display = 'flex';
                } else if (cat === 'sedan' && (sampleName.includes('jaguar') || sampleName.includes('sedan') || cardText.includes('sedan') || cardText.includes('jaguar'))) {
                    card.style.display = 'flex';
                } else if (cat === 'sports' && (sampleName.includes('lamborghini') || sampleName.includes('suv') || cardText.includes('aventador') || cardText.includes('sports'))) {
                    card.style.display = 'flex';
                } else if ((cat === 'vintage' || cat === 'classic') && (sampleName.includes('vintage') || sampleName.includes('classic') || cardText.includes('vintage') || cardText.includes('padmini'))) {
                    card.style.display = 'flex';
                } else if (cat === 'suv' && (sampleName.includes('suv') || sampleName.includes('traffic'))) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // Real-time search filter for quick fleet presets
    if (globalSearchInput) {
        globalSearchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            presetCards.forEach(card => {
                const text = card.textContent.toLowerCase();
                const sample = (card.getAttribute('data-sample') || '').toLowerCase();
                if (!query || text.includes(query) || sample.includes(query)) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }

    // Helper: format bytes
    function formatBytes(bytes, decimals = 1) {
        if (!+bytes) return '0 B';
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
    }

    // Keyboard shortcut ⌘K or Ctrl+K for search
    window.addEventListener('keydown', (e) => {
        if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
            e.preventDefault();
            globalSearchInput.focus();
        }
    });

    // Dock quick actions
    const dockScanBtn = document.getElementById('dockScanBtn');
    if (dockScanBtn) {
        dockScanBtn.addEventListener('click', () => imageInput.click());
    }
    const dockFleetBtn = document.getElementById('dockFleetBtn');
    if (dockFleetBtn) {
        dockFleetBtn.addEventListener('click', () => {
            const firstPreset = document.querySelector('.fleet-preset-card');
            if (firstPreset) firstPreset.click();
        });
    }
});
