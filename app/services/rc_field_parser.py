import re

VRN_PATTERN = r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}"
VIN_PATTERN = r"[A-HJ-NPR-Z0-9]{17}"
ENGINE_PATTERN = r"[A-Z0-9]{8,}"

FUEL_TYPES = ["PETROL", "DIESEL", "CNG", "EV", "ELECTRIC", "HYBRID"]


def parse_rc_fields(ocr_items: list) -> dict:
    extracted = {
        "vrn": None,
        "engine_full": None,
        "engine_last5": None,
        "chassis": None,
        "fuel": None
    }

    previous_text = ""

    for item in ocr_items:
        text = item.get("text", "").upper().replace(" ", "")
        raw_text = item.get("text", "").upper()

        # ---------------- VRN ----------------
        if not extracted["vrn"]:
            match = re.search(VRN_PATTERN, text)
            if match:
                extracted["vrn"] = match.group()

        # ---------------- ENGINE ----------------
        if "ENGINE" in previous_text or "MOTOR" in previous_text:
            if re.fullmatch(ENGINE_PATTERN, text):
                extracted["engine_full"] = text
                extracted["engine_last5"] = text[-5:]

        # ---------------- CHASSIS ----------------
        if "CHASSIS" in previous_text:
            match = re.search(VIN_PATTERN, text)
            if match:
                extracted["chassis"] = match.group()

        # ---------------- FUEL ----------------
        if "FUEL" in previous_text:
            if raw_text in FUEL_TYPES:
                extracted["fuel"] = raw_text

        previous_text = raw_text

    return extracted
