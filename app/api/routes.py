from fastapi import APIRouter, UploadFile, File, HTTPException
import tempfile
import os

from app.services.ocr_service import extract_rc_details

router = APIRouter()


@router.get("/")
def health():
    return {"status": "RC Fraud Detection API is running"}


@router.post("/verify-rc")
async def verify_rc(file: UploadFile = File(...)):
    """
    Upload RC image and extract VRN + Engine details
    """

    # 1. Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Only image files are allowed"
        )

    # 2. Save image temporarily
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(await file.read())
            temp_path = tmp.name
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to save uploaded image"
        )

    # 3. Run OCR
    try:
        result = extract_rc_details(temp_path)
    finally:
        # 4. Cleanup temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return result
