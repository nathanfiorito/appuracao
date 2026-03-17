#!/usr/bin/env python3
"""
Fetch complementary BU data from TSE open data.

Downloads candidate name → number mapping for a given election,
municipality, and cargo. Used to enrich results with candidate names.

Usage:
    python scripts/fetch_complementary.py --year 2024 --state SP --muni 71072
"""

import argparse
import json
import sys
import urllib.request
from pathlib import Path


def fetch_candidates(year: int, state: str, muni: str) -> list[dict]:
    """
    Stub: fetch candidate data from TSE open data API.

    In production, call:
    https://resultados.tse.jus.br/oficial/ele2024/candidatos/{state}/{muni}.json
    """
    # TODO: implement real TSE API call
    print(f"Fetching candidates for {state}/{muni} ({year})...")
    print("NOTE: This is a stub. Implement TSE API call for production use.")
    return []


def main():
    parser = argparse.ArgumentParser(description="Fetch TSE candidate data")
    parser.add_argument("--year", type=int, default=2024)
    parser.add_argument("--state", required=True)
    parser.add_argument("--muni", required=True)
    args = parser.parse_args()

    candidates = fetch_candidates(args.year, args.state, args.muni)

    output = Path(__file__).parent.parent / "data" / f"candidates_{args.state}_{args.muni}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(candidates, ensure_ascii=False, indent=2))
    print(f"Saved {len(candidates)} candidates to {output}")


if __name__ == "__main__":
    main()
