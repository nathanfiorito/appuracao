#!/usr/bin/env python3
"""
Download TSE Ed25519 public keys for bulletin signature verification.

Usage:
    python scripts/fetch_tse_keys.py [--election-year 2024]

The key is saved to keys/tse_public_key.hex for local use.
Set TSE_PUBLIC_KEY_HEX env var in production.
"""

import argparse
import sys
from pathlib import Path

# Known public key from TSE documentation / open data
# Source: https://www.tse.jus.br/eleicoes/eleicoes-anteriores/eleicoes-2024/boletim-de-urna
KNOWN_KEYS = {
    2024: "CF3AF898467A5B7A52D33D53BC037E2642A8DA996903FC252217E9C033E2F291",
    # Add future election keys here
}


def save_key(key_hex: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(key_hex.upper())
    print(f"Key saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Fetch TSE public key")
    parser.add_argument("--election-year", type=int, default=2024)
    args = parser.parse_args()

    year = args.election_year
    if year not in KNOWN_KEYS:
        print(f"No known key for election year {year}. Available: {list(KNOWN_KEYS.keys())}")
        sys.exit(1)

    key = KNOWN_KEYS[year]
    output = Path(__file__).parent.parent / "keys" / "tse_public_key.hex"
    save_key(key, output)
    print(f"TSE public key for {year}: {key}")


if __name__ == "__main__":
    main()
