import cv2
import numpy as np
from PIL import Image, ImageChops
import tempfile
import os


def perform_ela(image_path: str, quality: int = 90) -> float:
    """
    Perform Error Level Analysis (ELA)

    Higher score => more likely image has been edited
    """

    # Load original image
    original = Image.open(image_path).convert("RGB")

    # Save compressed copy
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp:
        temp_path = temp.name

    original.save(temp_path, "JPEG", quality=quality)

    # Reload compressed image
    compressed = Image.open(temp_path)

    # Compute pixel difference
    ela_image = ImageChops.difference(original, compressed)
    ela_array = np.asarray(ela_image)

    # Mean difference = ELA score
    ela_score = float(np.mean(ela_array))

    # Cleanup
    os.remove(temp_path)

    return ela_score


def noise_variance(image_path: str) -> float:
    """
    Detect image noise level using Laplacian variance

    Low variance => suspicious smoothing or tampering
    """

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        return 0.0

    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    return float(laplacian.var())


def detect_tampering(image_path: str) -> dict:
    """
    Main tamper detection function
    """

    ela_score = perform_ela(image_path)
    noise_score = noise_variance(image_path)

    tampered = False
    reasons = []

    # Thresholds (empirical, safe defaults)
    if ela_score > 15:
        tampered = True
        reasons.append("HIGH_ELA_SCORE")

    if noise_score < 100:
        tampered = True
        reasons.append("LOW_NOISE_VARIANCE")

    confidence = min(1.0, ela_score / 30)

    return {
        "tampered": tampered,
        "confidence": round(confidence, 2),
        "ela_score": round(ela_score, 2),
        "noise_score": round(noise_score, 2),
        "reasons": reasons
    }
