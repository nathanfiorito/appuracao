"""
Ed25519 signature verification for BU authenticity.

The TSE signs the BU content with a per-election Ed25519 key.
The ASSI field contains the signature in hex.
"""

import re
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError


class SignatureVerificationError(Exception):
    pass


def verify_signature(raw_text: str, signature_hex: str, public_key_hex: str) -> bool:
    """
    Verify Ed25519 signature over BU content.

    The signature covers the BU content with the ASSI field stripped,
    using the same convention as the hash (sign then append).

    Args:
        raw_text: Full raw QR text including ASSI tag.
        signature_hex: Hex-encoded signature from ASSI field.
        public_key_hex: Hex-encoded TSE public key.

    Returns:
        True if signature is valid.

    Raises:
        SignatureVerificationError on key/signature format errors.
    """
    try:
        # Strip the ASSI token from the signed content
        content = re.sub(r"\bASSI:\S*", "", raw_text).strip()
        signed_bytes = content.encode("utf-8")

        sig_bytes = bytes.fromhex(signature_hex)
        pub_bytes = bytes.fromhex(public_key_hex)

        verify_key = VerifyKey(pub_bytes)
        verify_key.verify(signed_bytes, sig_bytes)
        return True

    except BadSignatureError:
        return False
    except (ValueError, Exception) as exc:
        raise SignatureVerificationError(f"Verification error: {exc}") from exc
