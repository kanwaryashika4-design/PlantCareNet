import numpy as np
from PIL import Image
import cv2
from config import IMG_SIZE

CONFIDENCE_THRESHOLD = 60.0
GREEN_PIXEL_RATIO_MIN = 0.06

def preprocess_image(file_stream):
    img = Image.open(file_stream).convert('RGB')
    img_resized = img.resize(IMG_SIZE)
    arr = np.array(img_resized).astype('float32') / 255.0
    arr = np.expand_dims(arr, axis=0)
    return arr, img

def validate_is_tomato_leaf(pil_image, confidence):
    """
    Multi-layer validation to reject non-leaf images including
    green charts, graphs, screenshots, and other objects.
    """
    img_np = np.array(pil_image.convert('RGB'))
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    total_pixels = img_np.shape[0] * img_np.shape[1]
    reasons = []

    # ── CHECK 1: Model confidence ─────────────────────────────
    if confidence < CONFIDENCE_THRESHOLD:
        reasons.append(
            f"Model confidence too low ({confidence:.1f}%) — "
            f"minimum required is {CONFIDENCE_THRESHOLD}%"
        )

    # ── CHECK 2: Green pixel ratio ────────────────────────────
    lower_green = np.array([25, 30, 30])
    upper_green = np.array([95, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    green_pixels = cv2.countNonZero(green_mask)
    green_ratio = green_pixels / total_pixels

    if green_ratio < GREEN_PIXEL_RATIO_MIN:
        reasons.append(
            f"Insufficient green leaf area detected ({green_ratio*100:.1f}%) "
            f"— image does not appear to be a plant leaf"
        )

    # ── CHECK 3: Color texture variance (catches charts/graphs) ──
    # Natural leaves have organic color variation.
    # Charts and graphs have large uniform-color regions with very low variance.
    if green_pixels > 200:
        green_sat_values = hsv[:, :, 1][green_mask > 0]
        green_val_values = hsv[:, :, 2][green_mask > 0]
        sat_std = float(np.std(green_sat_values))
        val_std = float(np.std(green_val_values))

        # Very low standard deviation = uniform color = chart/diagram
        if sat_std < 18.0 and val_std < 18.0 and green_ratio > 0.15:
            reasons.append(
                "Image appears to be a chart, diagram, or solid-colored "
                "object — natural leaf texture not detected"
            )

    # ── CHECK 4: Edge density (organic vs geometric) ─────────────
    # Natural leaf images contain organic curved edges from veins and
    # leaf margins. Charts have very sparse or purely straight edges.
    edges = cv2.Canny(gray, 40, 120)
    edge_density = cv2.countNonZero(edges) / total_pixels

    if edge_density < 0.015 and green_ratio > 0.25:
        reasons.append(
            "Image lacks organic edge texture expected in natural leaf "
            "photography — may be a graphic or diagram"
        )

    # ── CHECK 5: Dominant color uniformity test ───────────────────
    # Quantise the image into 8 dominant colours. If one colour
    # accounts for more than 60% of the image, it is almost certainly
    # a flat graphic, not a natural photograph.
    small = cv2.resize(img_bgr, (64, 64))
    pixels = small.reshape(-1, 3).astype(np.float32)
    _, labels, centers = cv2.kmeans(
        pixels, 8,
        None,
        (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0),
        3,
        cv2.KMEANS_RANDOM_CENTERS
    )
    counts = np.bincount(labels.flatten())
    dominant_ratio = counts.max() / counts.sum()

    if dominant_ratio > 0.60 and green_ratio > 0.15:
        reasons.append(
            f"Image is dominated by a single flat colour "
            f"({dominant_ratio*100:.0f}% of pixels) — "
            f"natural leaf images have varied colour distributions"
        )

    if reasons:
        return False, reasons

    return True, []