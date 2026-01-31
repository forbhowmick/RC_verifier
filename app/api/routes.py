from fastapi import APIRouter, UploadFile, File
import shutil
import os

from app.services.ocr_service import extract_rc_details
from app.services.db_verification_service import verify_vrn_in_database

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/verify-rc")
async def verify_rc(file: UploadFile = File(...)):
    image_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ocr_result = extract_rc_details(image_path)

    # SAFELY read vrn
    vrn = ocr_result.get("vrn")

    if ocr_result["status"] != "SUCCESS":
        return {
            "status": "FAIL",
            "stage": "OCR",
            "details": ocr_result
        }

    if not vrn:
        return {
            "status": "FAIL",
            "stage": "VRN_EXTRACTION",
            "reason": "VRN_NOT_FOUND",
            "ocr_text": ocr_result["raw_text"]
        }

    db_result = verify_vrn_in_database(vrn)

    return {
        "status": "SUCCESS",
        "vrn": vrn,
        "db_verification": db_result,
        "ocr_text": ocr_result["raw_text"]
    }
