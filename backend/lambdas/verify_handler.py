"""
Step 3 — Verify Lambda

Verifies SHA-512 hash and Ed25519 signature of the BU.
Sets sig_verified=True on success. On failure, marks the bulletin but does NOT
raise — a BU with sig_verified=False is stored separately for manual review.

Input:  { ..., "bulletin": {...} }
Output: { ..., "bulletin": {..., "sig_verified": True/False} }
"""

import logging

from ..crypto.hasher import verify_hash
from ..crypto.keys import get_tse_public_key_hex
from ..crypto.verifier import SignatureVerificationError, verify_signature

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def handler(event: dict, context) -> dict:
    bulletin: dict = event["bulletin"]
    raw_text: str = bulletin.get("raw_text", "")
    hash_value: str = bulletin.get("hash_value", "")
    signature: str = bulletin.get("signature", "")

    if not raw_text:
        raise ValueError("bulletin.raw_text is required for verification")

    sig_verified = False
    verification_notes = []

    # Hash check
    if hash_value:
        hash_ok = verify_hash(raw_text, hash_value)
        if not hash_ok:
            verification_notes.append("SHA-512 hash mismatch")
            logger.warning("Hash mismatch for bulletin %s/%s", bulletin.get("pk"), bulletin.get("sk"))
        else:
            verification_notes.append("SHA-512 OK")
    else:
        verification_notes.append("No hash field present")

    # Signature check
    if signature:
        try:
            pub_key = get_tse_public_key_hex()
            sig_ok = verify_signature(raw_text, signature, pub_key)
            if sig_ok:
                sig_verified = True
                verification_notes.append("Ed25519 signature OK")
            else:
                verification_notes.append("Ed25519 signature INVALID")
                logger.warning(
                    "Invalid signature for bulletin %s/%s", bulletin.get("pk"), bulletin.get("sk")
                )
        except SignatureVerificationError as exc:
            verification_notes.append(f"Signature verification error: {exc}")
            logger.error("Signature verification error: %s", exc)
    else:
        verification_notes.append("No signature field present")

    bulletin["sig_verified"] = sig_verified
    bulletin["verification_notes"] = verification_notes

    return {**event, "bulletin": bulletin}
