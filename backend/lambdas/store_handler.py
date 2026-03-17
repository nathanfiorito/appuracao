"""
Step 5 — Store Lambda

Persists the verified BU to DynamoDB. Skipped if bulletin is a duplicate.

Input:  { ..., "bulletin": {...}, "duplicate": False }
Output: { ..., "stored": True }
"""

import logging

from ..qrcode.models import BulletinData
from ..storage.dynamodb import save_bulletin
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def handler(event: dict, context) -> dict:
    if event.get("duplicate"):
        logger.info("Skipping store — bulletin is a duplicate")
        return {**event, "stored": False, "store_skipped_reason": "duplicate"}

    bulletin_dict: dict = event["bulletin"]
    bulletin = BulletinData(**bulletin_dict)

    try:
        save_bulletin(bulletin)
        logger.info("Stored BU %s / %s", bulletin.pk, bulletin.sk)
        return {**event, "stored": True}
    except ClientError as exc:
        if exc.response["Error"]["Code"] == "ConditionalCheckFailedException":
            # Race condition — another worker stored the same BU first
            logger.warning("Concurrent duplicate for %s / %s", bulletin.pk, bulletin.sk)
            return {**event, "stored": False, "store_skipped_reason": "concurrent_duplicate"}
        raise
