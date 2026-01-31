import pandas as pd
import os
import math


def clean_json(value):
    """Convert NaN / inf to None (JSON-safe)"""
    if value is None:
        return None
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
    return value


def verify_vrn_in_database(vrn: str) -> dict:
    try:
        base_dir = os.path.dirname(os.path.dirname(__file__))  # app/
        db_path = os.path.join(base_dir, "data", "api_verifies.xlsx")

        if not os.path.exists(db_path):
            return {
                "status": "FAIL",
                "reason": "DATABASE_FILE_NOT_FOUND",
                "path": db_path
            }

        df = pd.read_excel(db_path)

        df.columns = [c.strip().upper() for c in df.columns]

        if "VRN" not in df.columns:
            return {
                "status": "FAIL",
                "reason": "VRN_COLUMN_MISSING",
                "columns": list(df.columns)
            }

        df["VRN"] = df["VRN"].astype(str).str.upper().str.strip()
        vrn = vrn.upper().strip()

        match = df[df["VRN"] == vrn]

        if match.empty:
            return {
                "status": "FAIL",
                "reason": "VRN_NOT_FOUND_IN_DATABASE"
            }

        record_raw = match.iloc[0].to_dict()

        # 🔥 JSON-safe cleaning
        record = {k: clean_json(v) for k, v in record_raw.items()}

        return {
            "status": "SUCCESS",
            "record": record
        }

    except Exception as e:
        return {
            "status": "FAIL",
            "reason": "DATABASE_ERROR",
            "error": str(e)
        }
