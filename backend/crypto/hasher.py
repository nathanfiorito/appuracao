"""
SHA-512 cumulative hash computation for BU verification.

The TSE computes a cumulative SHA-512 over the BU content.
The HASH field in the QR code contains this value in hex.
"""

import hashlib


def compute_sha512(data: str | bytes) -> str:
    """Compute SHA-512 of the given data and return hex digest."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha512(data).hexdigest()


def compute_cumulative_hash(parts: list[str]) -> str:
    """
    Compute cumulative SHA-512 over multiple parts.

    For multi-QR BUs, the TSE chains hashes: each part's hash is computed
    over (previous_hash + current_part_content).
    """
    if not parts:
        raise ValueError("No parts provided for cumulative hash")

    current_hash = ""
    for part in parts:
        content = current_hash + part
        current_hash = compute_sha512(content)

    return current_hash


def verify_hash(raw_text: str, expected_hex: str) -> bool:
    """
    Verify that the SHA-512 of raw_text matches expected_hex.

    Strips the HASH tag itself from the content before computing,
    since the hash is computed over the BU content excluding the HASH field.
    """
    import re
    # Remove the HASH:... token from the text before hashing
    content = re.sub(r"\bHASH:\S*", "", raw_text).strip()
    computed = compute_sha512(content)
    return computed.lower() == expected_hex.lower()
