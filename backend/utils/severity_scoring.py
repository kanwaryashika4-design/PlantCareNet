import cv2
import numpy as np

def calculate_severity(pil_image, disease_label):
    """
    Only calculates severity for diseased leaves.
    Returns 0.0 and 'N/A' for healthy leaves.
    Severity buckets: 0-20% Mild, 21-50% Moderate, 51-100% Severe
    """

    # If healthy, no severity scoring needed
    if disease_label.lower() == 'healthy':
        return 0.0, 'N/A'

    img = np.array(pil_image.convert('RGB'))
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    # Disease/discolored pixels: brown, yellow, dark spots
    lower_disease = np.array([10, 40, 40])
    upper_disease = np.array([30, 255, 255])
    disease_mask = cv2.inRange(hsv, lower_disease, upper_disease)

    # Healthy green leaf pixels
    lower_leaf = np.array([35, 40, 40])
    upper_leaf = np.array([85, 255, 255])
    leaf_mask = cv2.inRange(hsv, lower_leaf, upper_leaf)

    disease_pixels = cv2.countNonZero(disease_mask)
    leaf_pixels = cv2.countNonZero(leaf_mask)
    total_leaf_pixels = leaf_pixels + disease_pixels

    if total_leaf_pixels == 0:
        return 0.0, 'Mild'

    severity_pct = round((disease_pixels / total_leaf_pixels) * 100, 2)
    severity_pct = min(severity_pct, 100.0)

    # Your defined severity buckets
    if severity_pct <= 20:
        bucket = 'Mild'
    elif severity_pct <= 50:
        bucket = 'Moderate'
    else:
        bucket = 'Severe'

    return severity_pct, bucket