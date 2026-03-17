"""
Integration tests for Step Function Lambda handlers.
Uses moto to mock DynamoDB and S3.
"""

import json
import os
import pytest

# moto must be imported before boto3 in the test module
import boto3
from moto import mock_aws

from backend.lambdas.parse_handler import handler as parse_handler
from backend.lambdas.assemble_handler import handler as assemble_handler
from backend.lambdas.verify_handler import handler as verify_handler
from backend.lambdas.deduplicate_handler import handler as deduplicate_handler
from backend.lambdas.store_handler import handler as store_handler
from backend.lambdas.tally_handler import handler as tally_handler
from backend.lambdas.publish_handler import handler as publish_handler


# ─── DynamoDB + S3 fixtures ───────────────────────────────────────────────────

@pytest.fixture
def aws_resources():
    """Create mocked DynamoDB tables and S3 bucket."""
    with mock_aws():
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

        # Bulletins table
        dynamodb.create_table(
            TableName="test-bulletins",
            KeySchema=[
                {"AttributeName": "pk", "KeyType": "HASH"},
                {"AttributeName": "sk", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "pk", "AttributeType": "S"},
                {"AttributeName": "sk", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )

        # Partial QR table
        dynamodb.create_table(
            TableName="test-partial-qrcodes",
            KeySchema=[
                {"AttributeName": "pk", "KeyType": "HASH"},
                {"AttributeName": "sk", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "pk", "AttributeType": "S"},
                {"AttributeName": "sk", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )

        # Results S3 bucket
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket="test-results-bucket")

        yield {"dynamodb": dynamodb, "s3": s3}


# ─── parse_handler ────────────────────────────────────────────────────────────

def test_parse_handler_single_qr(sample_raw_single_qr):
    event = {
        "qr_codes": [sample_raw_single_qr],
        "metadata": {"request_id": "req-001"},
    }
    result = parse_handler(event, None)
    assert not result["needs_assembly"]
    assert result["bulletin"]["process"] == "2024BR"


def test_parse_handler_multi_qr(sample_raw_multi_qr):
    part1, part2 = sample_raw_multi_qr
    event = {
        "qr_codes": [part1, part2],
        "metadata": {"request_id": "req-002"},
    }
    result = parse_handler(event, None)
    assert result["needs_assembly"]
    assert len(result["parts"]) == 2


def test_parse_handler_empty_raises():
    with pytest.raises(ValueError):
        parse_handler({"qr_codes": [], "metadata": {}}, None)


# ─── assemble_handler ─────────────────────────────────────────────────────────

def test_assemble_handler_passthrough_single_qr(sample_raw_single_qr, aws_resources):
    # needs_assembly=False → passthrough
    event = {
        "qr_codes": [sample_raw_single_qr],
        "needs_assembly": False,
        "bulletin": {"process": "2024BR"},
        "metadata": {},
    }
    result = assemble_handler(event, None)
    assert not result["needs_assembly"]
    assert result["bulletin"]["process"] == "2024BR"


def test_assemble_handler_multi_qr(sample_raw_multi_qr, aws_resources):
    part1, part2 = sample_raw_multi_qr
    event = {
        "qr_codes": [part1, part2],
        "needs_assembly": True,
        "parts": [
            {"index": 1, "total": 2, "raw_text": part1},
            {"index": 2, "total": 2, "raw_text": part2},
        ],
        "metadata": {"request_id": "req-003"},
    }
    result = assemble_handler(event, None)
    assert not result["needs_assembly"]
    assert result["bulletin"]["section"] == "0002"


# ─── verify_handler ───────────────────────────────────────────────────────────

def test_verify_handler_no_signature(sample_raw_single_qr):
    """BU without signature → sig_verified=False but no error."""
    event = {
        "bulletin": {
            "raw_text": sample_raw_single_qr,
            "hash_value": None,
            "signature": None,
        }
    }
    result = verify_handler(event, None)
    assert result["bulletin"]["sig_verified"] is False


def test_verify_handler_valid_signature():
    from nacl.signing import SigningKey
    sk = SigningKey.generate()
    pub_hex = sk.verify_key.encode().hex()
    os.environ["TSE_PUBLIC_KEY_HEX"] = pub_hex

    content = "PROC:2024BR PLEI:0000407 TURN:1 UNFE:SP MUNI:71072 ZONA:0001 SECA:0001"
    sig_hex = sk.sign(content.encode()).signature.hex()
    raw_with_sig = content + f" ASSI:{sig_hex}"

    event = {
        "bulletin": {
            "raw_text": raw_with_sig,
            "hash_value": None,
            "signature": sig_hex,
        }
    }
    result = verify_handler(event, None)
    assert result["bulletin"]["sig_verified"] is True

    # Cleanup
    del os.environ["TSE_PUBLIC_KEY_HEX"]


# ─── deduplicate_handler ──────────────────────────────────────────────────────

def test_deduplicate_not_found(aws_resources):
    event = {
        "bulletin": {
            "process": "2024BR", "plea": "0000407", "turn": "1",
            "state": "SP", "municipality_code": "71072",
            "zone": "0001", "section": "0001",
        }
    }
    result = deduplicate_handler(event, None)
    assert not result["duplicate"]


def test_deduplicate_found(aws_resources, sample_raw_single_qr):
    from backend.storage.dynamodb import save_bulletin
    from backend.qrcode.parser import parse_raw_text

    bulletin = parse_raw_text(sample_raw_single_qr)
    save_bulletin(bulletin)

    event = {
        "bulletin": {
            "process": "2024BR", "plea": "0000407", "turn": "1",
            "state": "SP", "municipality_code": "71072",
            "zone": "0001", "section": "0001",
        }
    }
    result = deduplicate_handler(event, None)
    assert result["duplicate"]


# ─── store_handler ────────────────────────────────────────────────────────────

def test_store_handler_stores_bulletin(aws_resources, sample_raw_single_qr):
    from backend.qrcode.parser import parse_raw_text
    bulletin = parse_raw_text(sample_raw_single_qr)
    event = {"duplicate": False, "bulletin": bulletin.model_dump(mode="json")}
    result = store_handler(event, None)
    assert result["stored"]


def test_store_handler_skips_duplicate(aws_resources):
    event = {"duplicate": True, "bulletin": {}}
    result = store_handler(event, None)
    assert not result["stored"]
    assert result["store_skipped_reason"] == "duplicate"


# ─── tally + publish ──────────────────────────────────────────────────────────

def test_tally_skips_when_not_stored():
    event = {"stored": False}
    result = tally_handler(event, None)
    assert result["tally_skipped"]
    assert result["summary"] is None


def test_tally_and_publish_full_pipeline(aws_resources, sample_raw_single_qr):
    from backend.qrcode.parser import parse_raw_text
    from backend.storage.dynamodb import save_bulletin

    bulletin = parse_raw_text(sample_raw_single_qr)
    save_bulletin(bulletin)

    tally_event = {"stored": True}
    tally_result = tally_handler(tally_event, None)
    assert tally_result["summary"] is not None
    assert len(tally_result["summary"]["elections"]) > 0

    pub_result = publish_handler(tally_result, None)
    assert pub_result["published_url"] is not None
    assert pub_result["published_url"].startswith("s3://")


def test_publish_skips_when_no_summary():
    event = {"summary": None, "tally_skipped": True}
    result = publish_handler(event, None)
    assert result["published_url"] is None
