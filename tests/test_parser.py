"""Tests for backend/qrcode/parser.py"""

import pytest
from backend.qrcode.parser import extract_qr_part_header, parse_raw_text
from backend.qrcode.models import BulletinData


def test_parse_single_qr(sample_raw_single_qr):
    bulletin = parse_raw_text(sample_raw_single_qr)

    assert isinstance(bulletin, BulletinData)
    assert bulletin.process == "2024BR"
    assert bulletin.plea == "0000407"
    assert bulletin.turn == "1"
    assert bulletin.state == "SP"
    assert bulletin.municipality_code == "71072"
    assert bulletin.zone == "0001"
    assert bulletin.section == "0001"
    assert bulletin.eligible_voters == 500
    assert bulletin.compared_voters == 400
    assert bulletin.absent_voters == 100


def test_parse_pk_sk(sample_raw_single_qr):
    bulletin = parse_raw_text(sample_raw_single_qr)
    assert bulletin.pk == "2024BR#0000407#1"
    assert bulletin.sk == "SP#71072#0001#0001"


def test_parse_elections(sample_raw_single_qr):
    bulletin = parse_raw_text(sample_raw_single_qr)
    assert len(bulletin.elections) == 1
    election = bulletin.elections[0]
    assert election.cargo_code == "11"
    assert election.blank_votes == 10
    assert election.null_votes == 5
    assert election.valid_votes == 385
    assert election.total_votes == 400


def test_parse_candidates(sample_raw_single_qr):
    bulletin = parse_raw_text(sample_raw_single_qr)
    candidates = bulletin.elections[0].candidates
    assert len(candidates) == 2
    numbers = {c.number for c in candidates}
    assert "11111" in numbers
    assert "22222" in numbers


def test_parse_missing_mandatory_tag():
    raw = "VRQR:1.5 PLEI:0000407 TURN:1 UNFE:SP MUNI:71072 ZONA:0001 SECA:0001 APTO:100 COMP:80 FALT:20"
    with pytest.raises(ValueError, match="PROC"):
        parse_raw_text(raw)


def test_extract_qr_part_header_single(sample_raw_single_qr):
    part = extract_qr_part_header(sample_raw_single_qr)
    assert part.index == 1
    assert part.total == 1


def test_extract_qr_part_header_multi():
    raw = "QRBU:2:3 SOME:DATA"
    part = extract_qr_part_header(raw)
    assert part.index == 2
    assert part.total == 3


def test_extract_qr_part_header_missing_header():
    # Falls back to single QR
    raw = "PROC:2024BR PLEI:0000407"
    part = extract_qr_part_header(raw)
    assert part.index == 1
    assert part.total == 1


def test_roll_validation_error():
    """COMP + FALT != APTO should raise."""
    raw = (
        "QRBU:1:1 VRQR:1.5 PROC:2024BR PLEI:0000407 TURN:1 FASE:O "
        "UNFE:SP MUNI:71072 ZONA:0001 SECA:0001 "
        "APTO:500 COMP:400 FALT:200 "  # 400 + 200 != 500
        "IDCA:11 VBRA:10 VNUL:5 VNOM:385 VLEG:0 TOTA:400 "
    )
    with pytest.raises(ValueError, match="COMP"):
        parse_raw_text(raw)
