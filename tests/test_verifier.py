"""Tests for backend/crypto/verifier.py"""

import pytest
from nacl.signing import SigningKey
from backend.crypto.verifier import SignatureVerificationError, verify_signature


def _make_keypair():
    """Generate a fresh Ed25519 keypair for testing."""
    sk = SigningKey.generate()
    vk = sk.verify_key
    return sk, vk.encode().hex()


def test_valid_signature():
    sk, pub_hex = _make_keypair()
    content = "PROC:2024BR PLEI:0000407 TURN:1"
    sig_bytes = sk.sign(content.encode()).signature
    sig_hex = sig_bytes.hex()

    # verify_signature strips ASSI: tag before verifying
    raw_with_sig = content + f" ASSI:{sig_hex}"
    assert verify_signature(raw_with_sig, sig_hex, pub_hex)


def test_invalid_signature():
    _, pub_hex = _make_keypair()
    wrong_sig = "00" * 64  # 64 zero bytes
    raw = "PROC:2024BR ASSI:" + wrong_sig
    assert not verify_signature(raw, wrong_sig, pub_hex)


def test_tampered_content():
    sk, pub_hex = _make_keypair()
    original = "PROC:2024BR PLEI:0000407"
    sig_bytes = sk.sign(original.encode()).signature
    sig_hex = sig_bytes.hex()

    # Tamper: change vote count after signing
    tampered = original + " VNOM:9999 ASSI:" + sig_hex
    assert not verify_signature(tampered, sig_hex, pub_hex)


def test_bad_public_key_raises():
    with pytest.raises(SignatureVerificationError):
        verify_signature("PROC:2024BR ASSI:aabb", "aabb", "notahexkey")


def test_bad_signature_format_raises():
    _, pub_hex = _make_keypair()
    with pytest.raises(SignatureVerificationError):
        verify_signature("PROC:2024BR ASSI:xyz", "xyz", pub_hex)
