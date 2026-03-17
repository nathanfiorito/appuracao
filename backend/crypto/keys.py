"""
TSE public key management.

Keys are loaded from environment variables or a local file downloaded
via scripts/fetch_tse_keys.py. Never hardcode keys here.
"""

import os
from pathlib import Path


_TSE_KEY_FILE = Path(__file__).parent.parent.parent / "keys" / "tse_public_key.hex"


def get_tse_public_key_hex() -> str:
    """
    Return the TSE Ed25519 public key as a hex string.

    Resolution order:
    1. TSE_PUBLIC_KEY_HEX environment variable
    2. keys/tse_public_key.hex file in project root

    Raises:
        RuntimeError if no key is available.
    """
    env_key = os.environ.get("TSE_PUBLIC_KEY_HEX", "").strip()
    if env_key:
        return env_key

    if _TSE_KEY_FILE.exists():
        return _TSE_KEY_FILE.read_text().strip()

    raise RuntimeError(
        "TSE public key not found. Set TSE_PUBLIC_KEY_HEX env var or run "
        "scripts/fetch_tse_keys.py to download it."
    )
