"""Tests for backend/qrcode/assembler.py"""

import pytest
from backend.qrcode.assembler import AssemblyError, assemble, needs_assembly
from backend.qrcode.parser import parse_raw_text


def test_single_qr_does_not_need_assembly(sample_raw_single_qr):
    assert not needs_assembly([sample_raw_single_qr])


def test_multi_qr_needs_assembly(sample_raw_multi_qr):
    part1, part2 = sample_raw_multi_qr
    assert needs_assembly([part1, part2])


def test_assemble_two_parts(sample_raw_multi_qr):
    part1, part2 = sample_raw_multi_qr
    assembled = assemble([part1, part2])

    # Should be parseable
    bulletin = parse_raw_text(assembled)
    assert bulletin.process == "2024BR"
    assert bulletin.section == "0002"
    assert bulletin.eligible_voters == 300


def test_assemble_out_of_order(sample_raw_multi_qr):
    part1, part2 = sample_raw_multi_qr
    # Supply in reverse order — should still work
    assembled = assemble([part2, part1])
    bulletin = parse_raw_text(assembled)
    assert bulletin.process == "2024BR"


def test_assemble_duplicate_part_raises(sample_raw_multi_qr):
    part1, _ = sample_raw_multi_qr
    with pytest.raises(AssemblyError, match="Duplicate"):
        assemble([part1, part1])


def test_assemble_missing_part_raises(sample_raw_multi_qr):
    part1, _ = sample_raw_multi_qr
    with pytest.raises(AssemblyError, match="Missing"):
        assemble([part1])  # only part 1 of 2


def test_assemble_empty_raises():
    with pytest.raises(AssemblyError):
        assemble([])
