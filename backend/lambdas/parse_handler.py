"""
Step 1 — Parse Lambda

Input:  { "qr_codes": ["QRBU:1:1 ..."], "metadata": {...} }
Output: { "qr_codes": [...], "metadata": {...}, "parsed": {...} }
"""

import json
import logging

from ..qrcode.assembler import needs_assembly
from ..qrcode.parser import extract_qr_part_header, parse_raw_text

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def handler(event: dict, context) -> dict:
    logger.info("parse_handler received event keys: %s", list(event.keys()))

    qr_codes: list[str] = event["qr_codes"]

    if not qr_codes:
        raise ValueError("qr_codes is empty")

    # Determine if we have a multi-QR BU or a single QR
    if needs_assembly(qr_codes):
        # Pass through to assemble step — return parts metadata
        parts = [extract_qr_part_header(raw) for raw in qr_codes]
        return {
            **event,
            "needs_assembly": True,
            "parts": [p.model_dump() for p in parts],
        }

    # Single QR — parse immediately
    raw = qr_codes[0]
    bulletin = parse_raw_text(raw)

    return {
        **event,
        "needs_assembly": False,
        "bulletin": bulletin.model_dump(mode="json"),
    }
