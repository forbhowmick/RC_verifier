# app/services/rc_verification_service.py

def verify_rc_with_authority(vrn: str, engine_last5: str) -> dict:
    """
    MOCK RC verification service.
    Replace with real govt/vendor API later.
    """

    # ---- Mock RC database ----
    mock_rc_db = {
        "CG10BF2700": {
            "engine_last5": "9747",
            "status": "ACTIVE"
        },
        "OD02AB1234": {
            "engine_last5": "F45K9",
            "status": "ACTIVE"
        }
    }

    record = mock_rc_db.get(vrn)

    if not record:
        return {
            "status": "FAIL",
            "reason": "VRN_NOT_FOUND"
        }

    if record["engine_last5"] != engine_last5:
        return {
            "status": "FAIL",
            "reason": "ENGINE_MISMATCH"
        }

    return {
        "status": "SUCCESS",
        "vehicle_status": record["status"]
    }
