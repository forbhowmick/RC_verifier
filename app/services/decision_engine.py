# app/services/decision_engine.py

def make_penalty_decision(
    ocr_result: dict,
    rc_verification: dict
) -> dict:
    """
    Final business decision engine
    """

    # OCR already validated before calling this
    if rc_verification["status"] != "SUCCESS":

        if rc_verification.get("reason") == "ENGINE_MISMATCH":
            return {
                "decision": "PENALTY_VALID",
                "reason": "ENGINE_NUMBER_MISMATCH"
            }

        return {
            "decision": "MANUAL_REVIEW_REQUIRED",
            "reason": rc_verification.get("reason", "RC_VERIFICATION_FAILED")
        }

    return {
        "decision": "PENALTY_INVALID",
        "reason": "RC_DETAILS_MATCHED"
    }
