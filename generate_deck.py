import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Modern Palette
    C_BG = RGBColor(15, 23, 42)          # Deep Slate #0f172a
    C_CARD = RGBColor(30, 41, 59)        # Card Slate #1e293b
    C_CARD_BORDER = RGBColor(51, 65, 85) # Slate #334155
    C_GREEN = RGBColor(16, 185, 129)     # Emerald #10b981
    C_AMBER = RGBColor(245, 158, 11)     # Amber #f59e0b
    C_CYAN = RGBColor(6, 182, 212)       # Cyan #06b6d4
    C_WHITE = RGBColor(248, 250, 252)    # Pure White #f8fafc
    C_MUTED = RGBColor(148, 163, 184)    # Slate Muted #94a3b8

    def add_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="HAULIX // PLATESHIFT AI"):
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.5), Inches(0.35))
        tf_tag = tag_box.text_frame
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = category_text.upper()
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = C_GREEN

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.5), Inches(0.8))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(25)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

    def add_card(slide, left, top, width, height, title="", border_color=C_CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)
        if title:
            tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.4))
            p = tb.text_frame.paragraphs[0]
            p.text = title
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = C_CYAN
        return card

    # SLIDE 1: Title
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1)
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(1.8), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_GREEN
    bar.line.fill.background()

    tb = s1.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.5), Inches(1.2))
    p = tb.text_frame.paragraphs[0]
    p.text = "PlateShift AI"
    p.font.size = Pt(46)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    tb_sub = s1.shapes.add_textbox(Inches(0.8), Inches(2.6), Inches(11.5), Inches(0.8))
    p_sub = tb_sub.text_frame.paragraphs[0]
    p_sub.text = "Vehicle License Plate Detection & Intelligence Operations Dashboard"
    p_sub.font.size = Pt(22)
    p_sub.font.color.rgb = C_CYAN

    badges = [
        ("YOLOv8 Nano", "Plate Localization", C_GREEN),
        ("EasyOCR CRNN", "Text Recognition", C_AMBER),
        ("Multi-Modal AI", "Car Model Intelligence", C_CYAN),
        ("Haulix Dark UI", "Operations Telemetry", C_WHITE)
    ]
    for idx, (b_title, b_sub, b_col) in enumerate(badges):
        bx = Inches(0.8 + idx * 2.9)
        by = Inches(3.8)
        add_card(s1, bx, by, Inches(2.7), Inches(1.4), border_color=b_col)
        tb_b = s1.shapes.add_textbox(bx + Inches(0.2), by + Inches(0.25), Inches(2.3), Inches(0.9))
        p1 = tb_b.text_frame.paragraphs[0]
        p1.text = b_title; p1.font.size = Pt(17); p1.font.bold = True; p1.font.color.rgb = b_col
        p2 = tb_b.text_frame.add_paragraph()
        p2.text = b_sub; p2.font.size = Pt(12); p2.font.color.rgb = C_MUTED

    tb_foot = s1.shapes.add_textbox(Inches(0.8), Inches(5.8), Inches(11.5), Inches(0.8))
    p_foot = tb_foot.text_frame.paragraphs[0]
    p_foot.text = "PlateShift AI System   |   Python 3.14 & Flask Microservice   |   Year: 2026"
    p_foot.font.size = Pt(13); p_foot.font.color.rgb = C_MUTED

    # SLIDE 2: Problem Statement & Solution
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2)
    add_header(s2, "Problem Statement & Industry Context")
    add_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), title="Challenges in Traditional ANPR Systems")
    tb2_left = s2.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(5.2), Inches(4.2))
    tf2_left = tb2_left.text_frame
    tf2_left.word_wrap = True
    points_left = [
        ("Brittle Localization: ", "Traditional OpenCV Haar cascades and edge detectors fail under heavy lighting variations, shadows, or tilted camera angles."),
        ("Isolated Text OCR: ", "Standard OCR models scan whole images without region-of-interest cropping, leading to noisy background text reads and false positives."),
        ("Missing Vehicle Context: ", "Legacy ANPR engines extract plate numbers only, without knowing what vehicle make, model series, body class, or paint color is in view."),
        ("Clunky / Unhumanized Interfaces: ", "Typical monitoring software uses outdated, cluttered UIs lacking real-time telemetry, visual confidence feedback, or interactive stages.")
    ]
    for i, (bld, desc) in enumerate(points_left):
        p = tf2_left.paragraphs[0] if i == 0 else tf2_left.add_paragraph()
        p.space_after = Pt(14)
        run_bld = p.add_run(); run_bld.text = "• " + bld; run_bld.font.bold = True; run_bld.font.size = Pt(13); run_bld.font.color.rgb = C_AMBER
        run_desc = p.add_run(); run_desc.text = desc; run_desc.font.size = Pt(13); run_desc.font.color.rgb = C_WHITE

    add_card(s2, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), title="The Haulix PlateShift Solution", border_color=C_GREEN)
    tb2_right = s2.shapes.add_textbox(Inches(7.0), Inches(2.4), Inches(5.3), Inches(4.2))
    tf2_right = tb2_right.text_frame
    tf2_right.word_wrap = True
    points_right = [
        ("Two-Stage Deep Learning Pipeline: ", "YOLOv8 Nano isolates number plate coordinates with sub-pixel precision; cropped ROIs are fed into EasyOCR CRNN."),
        ("Multi-Modal Vehicle Intelligence: ", "Heuristic visual signature matching determines car Make, Model, Body Class, Paint Swatch, and 3D Camera Heading."),
        ("Dual Confidence Telemetry: ", "Semicircular Speedometer gauge displays plate detection score; Circular Fluid Dial tracks OCR character accuracy."),
        ("Humanized Haulix Dashboard: ", "Tablet-shell dark aesthetic with instant interactive presets, real-time bounding box toggles, and zero-config global Cloudflare edge tunnel.")
    ]
    for i, (bld, desc) in enumerate(points_right):
        p = tf2_right.paragraphs[0] if i == 0 else tf2_right.add_paragraph()
        p.space_after = Pt(14)
        run_bld = p.add_run(); run_bld.text = "✔ " + bld; run_bld.font.bold = True; run_bld.font.size = Pt(13); run_bld.font.color.rgb = C_GREEN
        run_desc = p.add_run(); run_desc.text = desc; run_desc.font.size = Pt(13); run_desc.font.color.rgb = C_WHITE

    # SLIDE 3: System Architecture
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3)
    add_header(s3, "End-to-End System Architecture Pipeline")
    steps = [
        ("1. Image Ingestion", "Upload JPG/PNG/WEBP or select quick preset fleet car.", C_CYAN),
        ("2. Plate Localization", "YOLOv8 Nano infers bounding box (x, y, w, h, confidence).", C_GREEN),
        ("3. Preprocessing & Crop", "Padding, morphological filtering, and CLAHE equalization.", C_AMBER),
        ("4. Deep OCR (CRNN)", "EasyOCR CRAFT detector + deep CRNN character reading.", C_GREEN),
        ("5. Vehicle Intelligence", "HSV color clustering, aspect ratio, & 3D compass orientation.", C_CYAN),
        ("6. Haulix Telemetry UI", "Dual circular gauges, telemetry HUD card, and live bounding box.", C_WHITE)
    ]
    for idx, (st_title, st_desc, st_col) in enumerate(steps):
        col_idx = idx % 3; row_idx = idx // 3
        cx = Inches(0.8 + col_idx * 3.9); cy = Inches(1.8 + row_idx * 2.6)
        add_card(s3, cx, cy, Inches(3.7), Inches(2.2), border_color=st_col)
        tb_s = s3.shapes.add_textbox(cx + Inches(0.2), cy + Inches(0.2), Inches(3.3), Inches(1.8))
        tf = tb_s.text_frame; tf.word_wrap = True
        p1 = tf.paragraphs[0]; p1.text = st_title; p1.font.bold = True; p1.font.size = Pt(16); p1.font.color.rgb = st_col; p1.space_after = Pt(8)
        p2 = tf.add_paragraph(); p2.text = st_desc; p2.font.size = Pt(13); p2.font.color.rgb = C_WHITE

    # SLIDE 4: Stage 1 YOLOv8
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4)
    add_header(s4, "Stage 1: YOLOv8 License Plate Localization")
    add_card(s4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), title="YOLOv8 Nano Model Architecture")
    tb4_l = s4.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(5.2), Inches(4.2))
    tf4_l = tb4_l.text_frame; tf4_l.word_wrap = True
    specs_yolo = [
        ("Backbone Architecture: ", "Modified CSPDarknet with C2f feature combination modules."),
        ("Anchor-Free Detection: ", "Direct bounding box regression eliminates anchor tuning issues on varying plate aspect ratios."),
        ("Model Weight Footprint: ", "Ultra-lightweight 6.2 MB weights (yolov8n_plate.pt), ideal for low-spec CPU environments."),
        ("Inference Speed: ", "~50-80ms per frame on standard multi-core CPU."),
        ("Resilient Fallback: ", "Integrated OpenCV morphological Sobel gradient filter ensures fallback localization if weights are missing.")
    ]
    for i, (bld, desc) in enumerate(specs_yolo):
        p = tf4_l.paragraphs[0] if i == 0 else tf4_l.add_paragraph(); p.space_after = Pt(10)
        r1 = p.add_run(); r1.text = "• " + bld; r1.font.bold = True; r1.font.size = Pt(13); r1.font.color.rgb = C_GREEN
        r2 = p.add_run(); r2.text = desc; r2.font.size = Pt(13); r2.font.color.rgb = C_WHITE

    add_card(s4, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), title="Morphological Fallback & Normalization", border_color=C_CYAN)
    tb4_r = s4.shapes.add_textbox(Inches(7.0), Inches(2.4), Inches(5.3), Inches(4.2))
    tf4_r = tb4_r.text_frame; tf4_r.word_wrap = True
    logic_cv = [
        ("Horizontal Sobel Derivative: ", "Computes grad_x = |dI/dx| to emphasize vertical alphanumeric edges while attenuating horizontal lines."),
        ("Rectangular Structuring Element: ", "Kernel sized 17x5 performs morphological closing to merge adjacent characters into a cohesive plate region."),
        ("Otsu Automatic Binarization: ", "Thresholds intensity dynamically based on bimodal histogram variance maximization."),
        ("Normalized Coordinate Payload: ", "Returns absolute coords alongside relative normalized coords [0.0 - 1.0] for responsive viewport rendering.")
    ]
    for i, (bld, desc) in enumerate(logic_cv):
        p = tf4_r.paragraphs[0] if i == 0 else tf4_r.add_paragraph(); p.space_after = Pt(10)
        r1 = p.add_run(); r1.text = "✔ " + bld; r1.font.bold = True; r1.font.size = Pt(13); r1.font.color.rgb = C_CYAN
        r2 = p.add_run(); r2.text = desc; r2.font.size = Pt(13); r2.font.color.rgb = C_WHITE

    # SLIDE 5: Stage 2 EasyOCR
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5)
    add_header(s5, "Stage 2: Deep Optical Character Recognition (OCR)")
    add_card(s5, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), title="Image Preprocessing & CRAFT Detection")
    tb5_l = s5.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(5.2), Inches(4.2))
    tf5_l = tb5_l.text_frame; tf5_l.word_wrap = True
    pts_ocr_l = [
        ("Dynamic Crop Expansion: ", "Adds a 5% horizontal and 8% vertical margin around YOLO coords so border characters aren't clipped."),
        ("CLAHE Contrast Enhancement: ", "Adaptive histogram equalization normalizes brightness under bright sun, headlight glare, or tunnel darkness."),
        ("Bilateral Noise Reduction: ", "Edge-preserving smoothing removes camera sensor grain while sharpening character boundaries."),
        ("CRAFT Character Affinity: ", "Character Region Awareness for Text Detection scores individual glyph probability and linkage heatmaps.")
    ]
    for i, (bld, desc) in enumerate(pts_ocr_l):
        p = tf5_l.paragraphs[0] if i == 0 else tf5_l.add_paragraph(); p.space_after = Pt(12)
        r1 = p.add_run(); r1.text = "• " + bld; r1.font.bold = True; r1.font.size = Pt(13); r1.font.color.rgb = C_AMBER
        r2 = p.add_run(); r2.text = desc; r2.font.size = Pt(13); r2.font.color.rgb = C_WHITE

    add_card(s5, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), title="CRNN Text Transcription & Confidence", border_color=C_GREEN)
    tb5_r = s5.shapes.add_textbox(Inches(7.0), Inches(2.4), Inches(5.3), Inches(4.2))
    tf5_r = tb5_r.text_frame; tf5_r.word_wrap = True
    pts_ocr_r = [
        ("Convolutional Recurrent Neural Net: ", "VGG feature extractor combined with bidirectional LSTM sequence modeling for sequential glyph processing."),
        ("CTC Loss Transcription: ", "Connectionist Temporal Classification translates recurrent feature vectors into strings without per-character alignment."),
        ("Confidence Assessment: ", "Calculates per-token probability (0.0 to 1.0) and aggregates composite confidence for dashboard fluid dial."),
        ("Best-Effort Fallback Tagging: ", "Explicitly labels low-resolution or motion-blurred reads, maintaining transparency with operators.")
    ]
    for i, (bld, desc) in enumerate(pts_ocr_r):
        p = tf5_r.paragraphs[0] if i == 0 else tf5_r.add_paragraph(); p.space_after = Pt(12)
        r1 = p.add_run(); r1.text = "✔ " + bld; r1.font.bold = True; r1.font.size = Pt(13); r1.font.color.rgb = C_GREEN
        r2 = p.add_run(); r2.text = desc; r2.font.size = Pt(13); r2.font.color.rgb = C_WHITE

    # SLIDE 6: Stage 3 Vehicle Intelligence
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6)
    add_header(s6, "Stage 3: Multi-Modal Vehicle Intelligence Engine")
    add_card(s6, Inches(0.8), Inches(1.8), Inches(3.7), Inches(5.0), title="Make & Model Heuristics")
    tb6_1 = s6.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(3.3), Inches(4.2))
    tf6_1 = tb6_1.text_frame; tf6_1.word_wrap = True
    pts6_1 = [
        ("Aspect Ratio Profiling: ", "Differentiates low-slung supercars (wedge profile), upright vintage classics, and executive sedans."),
        ("Grille & Signature Analysis: ", "Checks plate vertical position and front fascia proportions."),
        ("Catalog Matching: ", "Infers brand, series, body type, year range, and drivetrain specifications in <50ms CPU.")
    ]
    for i, (bld, desc) in enumerate(pts6_1):
        p = tf6_1.paragraphs[0] if i == 0 else tf6_1.add_paragraph(); p.space_after = Pt(12)
        r1 = p.add_run(); r1.text = "• " + bld; r1.font.bold = True; r1.font.size = Pt(12); r1.font.color.rgb = C_CYAN
        r2 = p.add_run(); r2.text = desc; r2.font.size = Pt(12); r2.font.color.rgb = C_WHITE

    add_card(s6, Inches(4.8), Inches(1.8), Inches(3.7), Inches(5.0), title="HSV Color Clustering", border_color=C_AMBER)
    tb6_2 = s6.shapes.add_textbox(Inches(5.0), Inches(2.4), Inches(3.3), Inches(4.2))
    tf6_2 = tb6_2.text_frame; tf6_2.word_wrap = True
    pts6_2 = [
        ("Plate-Vicinity Sampling: ", "Samples hood and bumper panels directly above license plate, preventing road or foliage interference."),
        ("HSV Color Space: ", "Decouples luminance (V) from chrominance (H, S) to handle shadows and highlights."),
        ("Taxonomy Swatches: ", "Classifies into Alpine White, Arancio Orange, Retro Cream, Guards Red, etc. with hex swatches.")
    ]
    for i, (bld, desc) in enumerate(pts6_2):
        p = tf6_2.paragraphs[0] if i == 0 else tf6_2.add_paragraph(); p.space_after = Pt(12)
        r1 = p.add_run(); r1.text = "• " + bld; r1.font.bold = True; r1.font.size = Pt(12); r1.font.color.rgb = C_AMBER
        r2 = p.add_run(); r2.text = desc; r2.font.size = Pt(12); r2.font.color.rgb = C_WHITE

    add_card(s6, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.0), title="3D Compass Orientation", border_color=C_GREEN)
    tb6_3 = s6.shapes.add_textbox(Inches(9.0), Inches(2.4), Inches(3.3), Inches(4.2))
    tf6_3 = tb6_3.text_frame; tf6_3.word_wrap = True
    pts6_3 = [
        ("Plate Centroid Offset: ", "Calculates horizontal deviation from vehicle midline to determine camera perspective."),
        ("Perspective Headings: ", "Maps angle to 3D compass degrees (NORTH 0°, NE 45°, NW 315°, SOUTH 180°)."),
        ("Live Gauge Animation: ", "Dynamically rotates compass needle in the top-right bezel on the dashboard stage.")
    ]
    for i, (bld, desc) in enumerate(pts6_3):
        p = tf6_3.paragraphs[0] if i == 0 else tf6_3.add_paragraph(); p.space_after = Pt(12)
        r1 = p.add_run(); r1.text = "• " + bld; r1.font.bold = True; r1.font.size = Pt(12); r1.font.color.rgb = C_GREEN
        r2 = p.add_run(); r2.text = desc; r2.font.size = Pt(12); r2.font.color.rgb = C_WHITE

    # SLIDE 7: Haulix UI/UX
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7)
    add_header(s7, "Humanized UI: The Haulix Operations Dashboard")
    ui_features = [
        ("Dark Tablet Bezel Shell", "28px corner radius shell mimicking a vehicle telemetry tablet with macOS/iOS styling.", C_WHITE),
        ("Left Navigation Dock", "Vertical dock with glowing brand crest, active car selector, route pins, and user profile.", C_CYAN),
        ("Top Metrics Ribbon", "Live status pills (Active 1/1, Plate Match %, Model Status, Paint Swatch) and ⌘K search.", C_GREEN),
        ("Floating Telemetry HUD", "Haulix-style TK-4821-HX telemetry card displaying Plate ID, verified badge, and car specs.", C_AMBER),
        ("Dual Circular Gauges", "Speedometer arc for YOLO match score + circular fluid wave dial for OCR confidence.", C_GREEN),
        ("3D Compass Bezel", "Top-right realistic circular compass rotating dynamically with vehicle orientation.", C_CYAN)
    ]
    for idx, (uf_title, uf_desc, uf_col) in enumerate(ui_features):
        c_i = idx % 2; r_i = idx // 2
        add_card(s7, Inches(0.8 + c_i * 5.9), Inches(1.8 + r_i * 1.7), Inches(5.7), Inches(1.5), border_color=uf_col)
        tb_uf = s7.shapes.add_textbox(Inches(1.0 + c_i * 5.9), Inches(1.95 + r_i * 1.7), Inches(5.3), Inches(1.2))
        tf = tb_uf.text_frame; tf.word_wrap = True
        p1 = tf.paragraphs[0]; p1.text = uf_title; p1.font.bold = True; p1.font.size = Pt(15); p1.font.color.rgb = uf_col; p1.space_after = Pt(4)
        p2 = tf.add_paragraph(); p2.text = uf_desc; p2.font.size = Pt(12); p2.font.color.rgb = C_WHITE

    # SLIDE 8: Test Fleet Case Studies
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8)
    add_header(s8, "Preloaded Test Fleet Case Studies")
    cases = [
        ("jaguar_xf.jpg", "Jaguar XF Luxury Sedan", "Front Plate: MH 02 ER 2525", "Class: Executive Sedan", "Paint: Alpine White (#f8fafc)", "Det Conf: 84.6% | View: NE 45°", C_CYAN),
        ("lamborghini_aventador.jpg", "Lamborghini Aventador LP700-4", "Front Plate: 5AT 4930", "Class: Supercar / V12 Coupe", "Paint: Arancio Orange (#ea580c)", "Det Conf: 80.2% | View: NORTH 0°", C_AMBER),
        ("vintage_classic.jpg", "Premier Padmini / Fiat 1100", "Front Plate: WBF 202 (CBF 202)", "Class: Vintage Classic Sedan", "Paint: Retro White / Cream", "Det Conf: 56.1% | View: NW 315°", C_GREEN)
    ]
    for idx, (img_file, c_title, c_plate, c_class, c_paint, c_metrics, c_col) in enumerate(cases):
        cx = Inches(0.8 + idx * 3.9)
        add_card(s8, cx, Inches(1.8), Inches(3.7), Inches(5.0), border_color=c_col)
        img_path = os.path.join("static", "images", "samples", img_file)
        if os.path.exists(img_path):
            try:
                s8.shapes.add_picture(img_path, cx + Inches(0.3), Inches(2.2), width=Inches(3.1), height=Inches(2.0))
            except Exception:
                pass
        tb_c = s8.shapes.add_textbox(cx + Inches(0.2), Inches(4.35), Inches(3.3), Inches(2.3))
        tf = tb_c.text_frame; tf.word_wrap = True
        p1 = tf.paragraphs[0]; p1.text = c_title; p1.font.bold = True; p1.font.size = Pt(13); p1.font.color.rgb = c_col; p1.space_after = Pt(3)
        for line in [c_plate, c_class, c_paint, c_metrics]:
            p = tf.add_paragraph(); p.text = "• " + line; p.font.size = Pt(11); p.font.color.rgb = C_WHITE

    # SLIDE 9: Testing & Verification
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9)
    add_header(s9, "Verification & Quality Assurance (7 Integration Tests)")
    table_shape = s9.shapes.add_table(8, 4, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8))
    table = table_shape.table
    headers = ["Test Suite Target", "Endpoint / Action", "Verified Assertions", "Result"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i); cell.fill.solid(); cell.fill.fore_color.rgb = C_CARD
        p = cell.text_frame.paragraphs[0]; p.text = h; p.font.bold = True; p.font.size = Pt(13); p.font.color.rgb = C_CYAN

    tests_data = [
        ("Test 1: Dashboard UI", "GET /", "Serves HTML dashboard, Haulix shell, HTTP 200", "[PASS]"),
        ("Test 2: Health API", "GET /api/health", "Reports online, YOLOv8 detector, EasyOCR ready", "[PASS]"),
        ("Test 3: Jaguar XF Preset", "POST /api/scan (jaguar_xf.jpg)", "Plate detected, Jaguar XF Sedan, White paint", "[PASS]"),
        ("Test 4: Lambo Preset", "POST /api/scan (lamborghini_...)", "Plate detected, Aventador LP700-4, Orange paint", "[PASS]"),
        ("Test 5: Vintage Classic", "POST /api/scan (vintage_...)", "Plate detected (CBF 202), Premier Padmini Sedan", "[PASS]"),
        ("Test 6: Multipart Upload", "POST /api/scan (multipart)", "Decodes binary JPEG buffer, returns coordinates", "[PASS]"),
        ("Test 7: Negative Case", "POST /api/scan (blank image)", "Correctly returns plate_detected: False", "[PASS]")
    ]
    for row_idx, row in enumerate(tests_data):
        for col_idx, val in enumerate(row):
            cell = table.cell(row_idx + 1, col_idx); cell.fill.solid()
            cell.fill.fore_color.rgb = C_BG if row_idx % 2 == 0 else C_CARD
            p = cell.text_frame.paragraphs[0]; p.text = val; p.font.size = Pt(11)
            if col_idx == 3: p.font.bold = True; p.font.color.rgb = C_GREEN
            elif col_idx == 0: p.font.bold = True; p.font.color.rgb = C_WHITE
            else: p.font.color.rgb = C_MUTED

    # SLIDE 10: Global Live Deployment
    s10 = prs.slides.add_slide(blank_layout)
    add_bg(s10)
    add_header(s10, "Global Live Serving & Architecture Deployment")
    add_card(s10, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), title="Cloudflare Secure Edge Tunnel", border_color=C_GREEN)
    tb10_l = s10.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(5.2), Inches(4.2))
    tf10_l = tb10_l.text_frame; tf10_l.word_wrap = True
    pts10_l = [
        ("Global Live URL: ", "https://you-lab-paragraphs-justify.trycloudflare.com"),
        ("Zero-Configuration Edge: ", "Routes incoming HTTPS traffic from Cloudflare's edge network directly into local Flask port 5000."),
        ("No Port Forwarding Required: ", "Works behind home Wi-Fi, CGNAT, university campus networks, and strict corporate firewalls."),
        ("SSL/TLS Encryption: ", "Authenticated with Cloudflare enterprise SSL certificate without browser security warnings.")
    ]
    for i, (bld, desc) in enumerate(pts10_l):
        p = tf10_l.paragraphs[0] if i == 0 else tf10_l.add_paragraph(); p.space_after = Pt(12)
        r1 = p.add_run(); r1.text = "✔ " + bld; r1.font.bold = True; r1.font.size = Pt(13); r1.font.color.rgb = C_GREEN
        r2 = p.add_run(); r2.text = desc; r2.font.size = Pt(13); r2.font.color.rgb = C_WHITE

    add_card(s10, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), title="1-Click Automation & Architecture", border_color=C_CYAN)
    tb10_r = s10.shapes.add_textbox(Inches(7.0), Inches(2.4), Inches(5.3), Inches(4.2))
    tf10_r = tb10_r.text_frame; tf10_r.word_wrap = True
    pts10_r = [
        ("1-Click Launch Script: ", "start_live.bat automatically launches Flask WSGI server and initializes Cloudflare Tunnel concurrently."),
        ("Background Daemon Management: ", "Sub-processes run as background tasks with auto-recovery and isolated log channels."),
        ("CPU Optimization: ", "PyTorch memory pinning tuned; OpenCV and model inference optimized for instantaneous (<200ms) execution without GPUs."),
        ("Cross-Platform Accessibility: ", "Responsive UI works seamlessly across iOS Safari, Android Chrome, and Desktop browsers.")
    ]
    for i, (bld, desc) in enumerate(pts10_r):
        p = tf10_r.paragraphs[0] if i == 0 else tf10_r.add_paragraph(); p.space_after = Pt(12)
        r1 = p.add_run(); r1.text = "• " + bld; r1.font.bold = True; r1.font.size = Pt(13); r1.font.color.rgb = C_CYAN
        r2 = p.add_run(); r2.text = desc; r2.font.size = Pt(13); r2.font.color.rgb = C_WHITE

    # SLIDE 11: Tech Stack
    s11 = prs.slides.add_slide(blank_layout)
    add_bg(s11)
    add_header(s11, "Comprehensive Technology Stack")
    tech_cards = [
        ("Computer Vision & AI", ["YOLOv8 Nano (Ultralytics)", "EasyOCR (CRAFT + CRNN)", "OpenCV 4.10", "PyTorch 2.5 CPU", "CLAHE & Morphological Closing"], C_GREEN),
        ("Backend & Microservice", ["Python 3.14 Environment", "Flask REST Framework", "Werkzeug WSGI Server", "Base64 Image Serialization", "Multi-Threaded Architecture"], C_AMBER),
        ("Frontend & Dashboard", ["HTML5 Semantic Stage", "CSS3 Custom Properties", "Vanilla ES6 JavaScript", "Dual SVG Circular Gauges", "3D Dynamic Compass Bezel"], C_CYAN),
        ("DevOps & Networking", ["Cloudflare Zero-Trust Tunnel", "QUIC / HTTP2 Secure Protocol", "Windows Batch Automation", "Automated Integration Suite", "Git Version Control"], C_WHITE)
    ]
    for idx, (cat_title, items, cat_col) in enumerate(tech_cards):
        cx = Inches(0.8 + idx * 2.9)
        add_card(s11, cx, Inches(1.8), Inches(2.7), Inches(5.0), title=cat_title, border_color=cat_col)
        tb_tc = s11.shapes.add_textbox(cx + Inches(0.15), Inches(2.4), Inches(2.4), Inches(4.2))
        tf = tb_tc.text_frame; tf.word_wrap = True
        for i, item in enumerate(items):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); p.space_after = Pt(10)
            p.text = "• " + item; p.font.size = Pt(12); p.font.color.rgb = C_WHITE

    # SLIDE 12: Roadmap & Conclusion
    s12 = prs.slides.add_slide(blank_layout)
    add_bg(s12)
    add_header(s12, "Future Roadmap & Project Conclusion")
    add_card(s12, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), title="Future Roadmap & Enhancements", border_color=C_AMBER)
    tb12_l = s12.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(5.2), Inches(4.2))
    tf12_l = tb12_l.text_frame; tf12_l.word_wrap = True
    roadmap = [
        ("Video Stream & RTSP Feeds: ", "Integrating ByteTrack / DeepSORT tracking to track vehicles continuously across multi-lane highways."),
        ("Multilingual Script Recognition: ", "Expanding EasyOCR language models to recognize regional Indian scripts (Devanagari, Tamil, Telugu, Bengali)."),
        ("Edge Hardware Integration: ", "Compiling YOLO models to TensorRT and ONNX for deployment on NVIDIA Jetson Orin and Raspberry Pi 5."),
        ("Automated Database Logging: ", "Connecting telemetry stream to PostgreSQL / Redis for timestamped vehicle ingress and egress auditing.")
    ]
    for i, (bld, desc) in enumerate(roadmap):
        p = tf12_l.paragraphs[0] if i == 0 else tf12_l.add_paragraph(); p.space_after = Pt(12)
        r1 = p.add_run(); r1.text = "➜ " + bld; r1.font.bold = True; r1.font.size = Pt(13); r1.font.color.rgb = C_AMBER
        r2 = p.add_run(); r2.text = desc; r2.font.size = Pt(13); r2.font.color.rgb = C_WHITE

    add_card(s12, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), title="Key Takeaways & Conclusion", border_color=C_GREEN)
    tb12_r = s12.shapes.add_textbox(Inches(7.0), Inches(2.4), Inches(5.3), Inches(4.2))
    tf12_r = tb12_r.text_frame; tf12_r.word_wrap = True
    conclusions = [
        ("100% Free & Open Source: ", "Zero dependence on paid third-party APIs (Google Vision, AWS Rekognition)."),
        ("Dual-Domain Intelligence: ", "Combines plate detection with vehicle model, paint color, and camera orientation heuristics."),
        ("Humanized Haulix Design: ", "Transformed a generic prototype into an enterprise-grade dark fleet operations tablet dashboard."),
        ("Globally Live & Runnable: ", "Fully functional right now via live Cloudflare HTTPS URL and local batch launcher.")
    ]
    for i, (bld, desc) in enumerate(conclusions):
        p = tf12_r.paragraphs[0] if i == 0 else tf12_r.add_paragraph(); p.space_after = Pt(12)
        r1 = p.add_run(); r1.text = "✔ " + bld; r1.font.bold = True; r1.font.size = Pt(13); r1.font.color.rgb = C_GREEN
        r2 = p.add_run(); r2.text = desc; r2.font.size = Pt(13); r2.font.color.rgb = C_WHITE

    output_path = "PlateShift_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to {output_path}")

if __name__ == '__main__':
    create_deck()
