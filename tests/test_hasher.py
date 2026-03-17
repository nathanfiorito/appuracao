"""Tests for backend/crypto/hasher.py"""

import hashlib
import pytest
from backend.crypto.hasher import compute_sha512, compute_cumulative_hash, verify_hash


def test_compute_sha512_known_value():
    # SHA-512 of "abc" is well-known
    expected = (
        "ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a"
        "2192992a274fc1a836ba3c23a3feebbd454d4423643ce80e2a9ac94fa54ca49f"
    )
    assert compute_sha512("abc") == expected


def test_compute_sha512_bytes():
    result = compute_sha512(b"abc")
    assert len(result) == 128  # 512 bits = 128 hex chars


def test_compute_sha512_empty():
    # SHA-512("") is defined
    expected = hashlib.sha512(b"").hexdigest()
    assert compute_sha512("") == expected


def test_cumulative_hash_single():
    single = compute_cumulative_hash(["hello"])
    assert single == compute_sha512("" + "hello")


def test_cumulative_hash_two_parts():
    first = compute_sha512("part1")
    second = compute_sha512(first + "part2")
    result = compute_cumulative_hash(["part1", "part2"])
    assert result == second


def test_cumulative_hash_empty_raises():
    with pytest.raises(ValueError):
        compute_cumulative_hash([])


def test_verify_hash_correct(sample_raw_single_qr):
    # Build a raw text with a valid hash
    import re
    # Strip any existing HASH tag
    clean = re.sub(r"\bHASH:\S*", "", sample_raw_single_qr).strip()
    correct_hash = compute_sha512(clean)

    raw_with_hash = clean + f" HASH:{correct_hash}"
    assert verify_hash(raw_with_hash, correct_hash)


def test_verify_hash_wrong(sample_raw_single_qr):
    wrong_hash = "a" * 128
    assert not verify_hash(sample_raw_single_qr, wrong_hash)
