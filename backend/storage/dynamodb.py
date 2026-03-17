"""
DynamoDB storage for bulletins and partial QR code assembly buffers.
"""

import json
from datetime import datetime, timezone
from typing import Optional

import boto3
from boto3.dynamodb.conditions import Key

from ..config import config
from ..qrcode.models import BulletinData


def _get_table(name: str):
    dynamodb = boto3.resource("dynamodb", region_name=config.AWS_REGION)
    return dynamodb.Table(name)


# ─── Bulletins ────────────────────────────────────────────────────────────────


def bulletin_exists(pk: str, sk: str) -> bool:
    """Check if a BU with this PK/SK already exists (deduplication)."""
    table = _get_table(config.BULLETINS_TABLE)
    response = table.get_item(Key={"pk": pk, "sk": sk}, ProjectionExpression="pk")
    return "Item" in response


def save_bulletin(bulletin: BulletinData) -> None:
    """Persist a verified BU to DynamoDB. BUs are immutable — no update."""
    table = _get_table(config.BULLETINS_TABLE)

    # Serialize elections as a plain dict list for DynamoDB
    elections_data = [e.model_dump() for e in bulletin.elections]

    item = {
        "pk": bulletin.pk,
        "sk": bulletin.sk,
        "process": bulletin.process,
        "plea": bulletin.plea,
        "turn": bulletin.turn,
        "state": bulletin.state,
        "municipality_code": bulletin.municipality_code,
        "zone": bulletin.zone,
        "section": bulletin.section,
        "eligible_voters": bulletin.eligible_voters,
        "compared_voters": bulletin.compared_voters,
        "absent_voters": bulletin.absent_voters,
        "elections": json.dumps(elections_data),
        "hash_value": bulletin.hash_value or "",
        "signature": bulletin.signature or "",
        "sig_verified": bulletin.sig_verified,
        "raw_text": bulletin.raw_text or "",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    # Condition: only insert if not already present (idempotent guard)
    table.put_item(
        Item=item,
        ConditionExpression="attribute_not_exists(pk)",
    )


def get_all_bulletins(pk: str) -> list[dict]:
    """Retrieve all BUs for a given process/plea/turn partition."""
    table = _get_table(config.BULLETINS_TABLE)
    response = table.query(KeyConditionExpression=Key("pk").eq(pk))
    return response.get("Items", [])


def scan_all_bulletins() -> list[dict]:
    """Full table scan — used only by tally Lambda (small tables only)."""
    table = _get_table(config.BULLETINS_TABLE)
    items = []
    response = table.scan()
    items.extend(response.get("Items", []))
    while "LastEvaluatedKey" in response:
        response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        items.extend(response.get("Items", []))
    return items


# ─── Partial QR Code Assembly Buffer ─────────────────────────────────────────


def save_partial_qr(session_id: str, qr_index: int, total: int, raw_text: str) -> None:
    """Buffer a single QR part for multi-QR assembly (TTL: 1 hour)."""
    import time
    table = _get_table(config.PARTIAL_QR_TABLE)
    table.put_item(Item={
        "pk": session_id,
        "sk": str(qr_index),
        "total": total,
        "raw_text": raw_text,
        "ttl": int(time.time()) + 3600,
    })


def get_partial_qrs(session_id: str) -> list[dict]:
    """Retrieve all buffered QR parts for a session."""
    table = _get_table(config.PARTIAL_QR_TABLE)
    response = table.query(KeyConditionExpression=Key("pk").eq(session_id))
    return sorted(response.get("Items", []), key=lambda x: int(x["sk"]))


def delete_partial_qrs(session_id: str) -> None:
    """Clean up assembly buffer after successful assembly."""
    table = _get_table(config.PARTIAL_QR_TABLE)
    items = get_partial_qrs(session_id)
    with table.batch_writer() as batch:
        for item in items:
            batch.delete_item(Key={"pk": item["pk"], "sk": item["sk"]})
