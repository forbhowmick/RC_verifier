import re
import cv2
from paddleocr import PaddleOCR

# ---------------- OCR INIT ----------------
ocr = PaddleOCR(
    lang="en",
    use_angle_cls=False,
    show_log=False
)

# ---------------- REGEX ----------------
VRN_REGEX = r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}"
ENGINE_REGEX = r"[A-Z0-9]{10,}"
CHASSIS_REGEX = r"[A-HJ-NPR-Z0-9]{17}"

# ---------------- MAIN FUNCTION ----------------
def extract_rc_details(image_path: str) -> dict:
    image = cv2.imread(image_path)
    if image is None:
        return {"status": "FAIL", "reason": "IMAGE_READ_FAILED"}

    # ✅ CORRECT OCR CALL
    results = ocr.ocr(image, cls=False)

    if not results or not results[0]:
        return {"status": "FAIL", "reason": "NO_TEXT_DETECTED"}

    texts = []
    for line in results[0]:
        text = line[1][0]
        conf = line[1][1]
        texts.append((text.strip(), conf))

    # ---------------- DEBUG LOG ----------------
    print("\n===== FASTAPI OCR TEXT =====")
    for t, c in texts:
        print(f"{t} | conf={round(c,3)}")
    print("============================\n")

    # ---------------- FIELD EXTRACTION ----------------
    vrn = None
    engine = None
    chassis = None
    fuel = None

    prev_text = ""

    for text, conf in texts:
        clean = text.replace(" ", "").upper()

        # VRN
        if not vrn:
            match = re.search(VRN_REGEX, clean)
            if match:
                vrn = match.group()

        # ENGINE
        if "ENGINE" in prev_text.upper():
            if re.fullmatch(ENGINE_REGEX, clean):
                engine = clean

        # CHASSIS
        if "CHASSIS" in prev_text.upper():
            match = re.search(CHASSIS_REGEX, clean)
            if match:
                chassis = match.group()

        # FUEL
        if text.upper() in ["PETROL", "DIESEL", "CNG", "EV", "ELECTRIC"]:
            fuel = text.upper()

        prev_text = text

    if not vrn or not engine:
        return {
            "status": "FAIL",
            "reason": "MANDATORY_FIELDS_MISSING",
            "debug": {
                "vrn": vrn,
                "engine": engine
            }
        }

    return {
        "status": "SUCCESS",
        "data": {
            "vrn": vrn,
            "engine_last5": engine[-5:],
            "engine_full": engine,
            "chassis": chassis,
            "fuel": fuel
        }
    }
