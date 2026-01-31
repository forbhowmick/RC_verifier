import re
from paddleocr import PaddleOCR

ocr = PaddleOCR(
    lang="en",
    use_angle_cls=False,
    show_log=False
)

VRN_REGEX = r"\b[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}\b"


def extract_rc_details(image_path: str) -> dict:
    """
    OCR RC image and extract VRN
    ALWAYS returns vrn key (None if not found)
    """

    try:
        ocr_result = ocr.ocr(image_path, cls=False)
    except Exception as e:
        return {
            "status": "FAIL",
            "vrn": None,
            "raw_text": [],
            "error": str(e)
        }

    extracted_texts = []

    for page in ocr_result:
        for _, (text, confidence) in page:
            extracted_texts.append(text.strip())

    combined_text = " ".join(extracted_texts)

    match = re.search(VRN_REGEX, combined_text)

    return {
        "status": "SUCCESS",
        "vrn": match.group(0) if match else None,
        "raw_text": extracted_texts
    }
