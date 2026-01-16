import cv2
from paddleocr import PaddleOCR
import pprint

IMAGE_PATH = r"C:\Users\bhowm_lesfaqy\Downloads\WhatsApp Image 2026-01-13 at 13.18.18 (1).jpeg"  # <-- put one RC image here

ocr = PaddleOCR(
    lang="en",
    use_angle_cls=False,
    show_log=False
)

img = cv2.imread(IMAGE_PATH)

if img is None:
    raise ValueError("Image not found or unreadable")

results = ocr.ocr(img, cls=False)

print("\n========== RAW OCR OUTPUT ==========\n")
pprint.pprint(results)

print("\n========== FLATTENED TEXT ==========\n")
for line in results[0]:
    text = line[1][0]
    score = line[1][1]
    print(f"{text}  | confidence={round(score, 3)}")
