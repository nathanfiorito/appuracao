"""
Step 2 — Assemble Lambda

Handles multi-QR BU assembly. If all parts are present, assembles and parses.
If parts are missing, buffers in DynamoDB (partial_qrcodes table) and raises
a retriable error so Step Functions can retry later.

Input:  { "qr_codes": [...], "metadata": {...}, "needs_assembly": True, "parts": [...] }
Output: { ..., "bulletin": {...} }
"""

import logging
import uuid

from ..qrcode.assembler import assemble
from ..qrcode.parser import parse_raw_text
from ..storage.dynamodb import delete_partial_qrs, get_partial_qrs, save_partial_qr

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def handler(event: dict, context) -> dict:
    if not event.get("needs_assembly"):
        # Already assembled or single-QR — pass through
        return event

    qr_codes: list[str] = event["qr_codes"]
    metadata: dict = event.get("metadata", {})

    # Use request_id as session key so all parts from same request are grouped
    session_id = metadata.get("request_id", str(uuid.uuid4()))

    # Store all received parts
    parts = event.get("parts", [])
    total = parts[0]["total"] if parts else len(qr_codes)

    for part, raw in zip(parts, qr_codes):
        save_partial_qr(
            session_id=session_id,
            qr_index=part["index"],
            total=part["total"],
            raw_text=raw,
        )

    # Check if all parts are now buffered
    stored = get_partial_qrs(session_id)
    if len(stored) < total:
        raise IncompleteAssemblyError(
            f"Have {len(stored)}/{total} parts for session {session_id}"
        )

    # All parts present — assemble and parse
    raw_codes = [s["raw_text"] for s in sorted(stored, key=lambda x: int(x["sk"]))]
    assembled = assemble(raw_codes)
    bulletin = parse_raw_text(assembled)

    delete_partial_qrs(session_id)

    return {
        **event,
        "needs_assembly": False,
        "bulletin": bulletin.model_dump(mode="json"),
    }


class IncompleteAssemblyError(Exception):
    """Raised when not all QR parts have been received yet."""
