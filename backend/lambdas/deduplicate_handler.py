"""
Step 4 — Deduplicate Lambda

Checks DynamoDB to see if this BU (identified by PK/SK) was already processed.
If it's a duplicate with the same signature → skip (idempotent).
If it's a duplicate with a different signature → flag for manual review and skip.

Input:  { ..., "bulletin": {...} }
Output: { ..., "bulletin": {...}, "duplicate": True/False }
"""

import logging

from ..storage.dynamodb import bulletin_exists

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def handler(event: dict, context) -> dict:
    bulletin: dict = event["bulletin"]
    pk = f"{bulletin['process']}#{bulletin['plea']}#{bulletin['turn']}"
    sk = (
        f"{bulletin['state']}#{bulletin['municipality_code']}"
        f"#{bulletin['zone']}#{bulletin['section']}"
    )

    is_duplicate = bulletin_exists(pk, sk)

    if is_duplicate:
        logger.info("Duplicate BU detected: %s / %s — skipping", pk, sk)

    return {**event, "duplicate": is_duplicate}
