import cv2
import numpy as np


def check_image_quality(image_path: str) -> dict:
    image = cv2.imread(image_path)

    if image is None:
        return {
            "status": "FAIL",
            "reason": "IMAGE_NOT_READABLE"
        }

    height, width, _ = image.shape

    # 1️⃣ Resolution check
    if width < 600 or height < 400:
        return {
            "status": "FAIL",
            "reason": "LOW_RESOLUTION"
        }

    # 2️⃣ Blur detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

    if blur_score < 80:
        return {
            "status": "FAIL",
            "reason": "IMAGE_TOO_BLURRY"
        }

    # 3️⃣ Brightness check
    brightness = np.mean(gray)

    if brightness < 60:
        return {
            "status": "FAIL",
            "reason": "IMAGE_TOO_DARK"
        }

    if brightness > 200:
        return {
            "status": "FAIL",
            "reason": "IMAGE_TOO_BRIGHT"
        }

    return {
        "status": "PASS",
        "reason": "IMAGE_QUALITY_OK"
    }
