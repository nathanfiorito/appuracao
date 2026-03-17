"""Shared fixtures for all tests."""

import os
import pytest

# Set env vars before any imports that read them
os.environ.setdefault("BULLETINS_TABLE", "test-bulletins")
os.environ.setdefault("PARTIAL_QR_TABLE", "test-partial-qrcodes")
os.environ.setdefault("RESULTS_BUCKET", "test-results-bucket")
os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
os.environ.setdefault("AWS_ACCESS_KEY_ID", "testing")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "testing")

# The known TSE test key from the manual / security checklist
TSE_TEST_PUBLIC_KEY_HEX = "CF3AF898467A5B7A52D33D53BC037E2642A8DA996903FC252217E9C033E2F291"


@pytest.fixture
def sample_raw_single_qr() -> str:
    """Minimal valid BU raw text (single QR, no signature)."""
    return (
        "QRBU:1:1 "
        "VRQR:1.5 "
        "PROC:2024BR "
        "PLEI:0000407 "
        "TURN:1 "
        "FASE:O "
        "UNFE:SP "
        "MUNI:71072 "
        "ZONA:0001 "
        "SECA:0001 "
        "APTO:500 "
        "COMP:400 "
        "FALT:100 "
        "IDCA:11 "
        "VBRA:10 "
        "VNUL:5 "
        "VNOM:385 "
        "VLEG:0 "
        "TOTA:400 "
        "IDDV:11111 QTDV:200 "
        "IDDV:22222 QTDV:185 "
    )


@pytest.fixture
def sample_raw_multi_qr() -> tuple[str, str]:
    """Two-part multi-QR BU."""
    part1 = (
        "QRBU:1:2 "
        "VRQR:1.5 "
        "PROC:2024BR "
        "PLEI:0000407 "
        "TURN:1 "
        "FASE:O "
        "UNFE:SP "
        "MUNI:71072 "
        "ZONA:0001 "
        "SECA:0002 "
        "APTO:300 "
        "COMP:250 "
        "FALT:50 "
    )
    part2 = (
        "QRBU:2:2 "
        "IDCA:11 "
        "VBRA:5 "
        "VNUL:3 "
        "VNOM:242 "
        "VLEG:0 "
        "TOTA:250 "
        "IDDV:11111 QTDV:150 "
        "IDDV:22222 QTDV:92 "
    )
    return part1, part2
