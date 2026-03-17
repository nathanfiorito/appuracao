"""
Parser for Boletim de Urna QR Code text.

The BU QR code format is a sequence of tag:value pairs separated by spaces or newlines.
Tags follow the TSE specification (e.g., QRBU, VRQR, PROC, PLEI, TURN, UNFE, MUNI,
ZONA, SECA, APTO, COMP, FALT, etc.).

Multi-QR BUs are prefixed with: QRBU:{index}:{total}
"""

import re
from .models import BulletinData, CandidateVotes, ElectionResult, QRCodePart


# Tags that introduce a new cargo block
_CARGO_START_TAG = "IDCA"
# Tags that introduce candidate votes within a cargo
_CANDIDATE_TAG = "IDDV"
_VOTE_TAG = "QTDV"
_BLANK_TAG = "VBRA"
_NULL_TAG = "VNUL"
_VALID_TAG = "VNOM"  # votos nominais válidos (candidates)
_LEGENDA_TAG = "VLEG"  # votos de legenda (partido)
_TOTAL_CARGO_TAG = "TOTA"  # total geral do cargo


def _tokenize(raw: str) -> dict[str, list[str]]:
    """
    Convert raw QR text to a dict of tag → [values].

    Multiple occurrences of the same tag (e.g., multiple IDDV) are collected as a list.
    """
    tokens: dict[str, list[str]] = {}
    # Tags are uppercase letters/digits, values follow after ':'
    # Lines can be "TAG:VALUE" or just "TAG:" (empty value)
    pattern = re.compile(r"\b([A-Z0-9]{2,6}):([^\s]*)")
    for match in pattern.finditer(raw):
        tag, value = match.group(1), match.group(2)
        tokens.setdefault(tag, []).append(value)
    return tokens


def _parse_int(tokens: dict, tag: str, default: int = 0) -> int:
    vals = tokens.get(tag, [])
    if not vals or vals[0] == "":
        return default
    return int(vals[0])


def _parse_str(tokens: dict, tag: str, default: str = "") -> str:
    vals = tokens.get(tag, [])
    return vals[0] if vals else default


def parse_raw_text(raw: str) -> BulletinData:
    """
    Parse raw QR Code text into a BulletinData object.

    Raises ValueError on missing mandatory fields or invalid totals.
    """
    tokens = _tokenize(raw)

    # Identification
    process = _parse_str(tokens, "PROC")
    plea = _parse_str(tokens, "PLEI")
    turn = _parse_str(tokens, "TURN")
    state = _parse_str(tokens, "UNFE")
    municipality = _parse_str(tokens, "MUNI")
    zone = _parse_str(tokens, "ZONA")
    section = _parse_str(tokens, "SECA")

    for tag, val in [
        ("PROC", process), ("PLEI", plea), ("TURN", turn),
        ("UNFE", state), ("MUNI", municipality), ("ZONA", zone), ("SECA", section),
    ]:
        if not val:
            raise ValueError(f"Mandatory tag '{tag}' missing or empty in QR text")

    # Electoral roll
    eligible = _parse_int(tokens, "APTO")
    compared = _parse_int(tokens, "COMP")
    absent = _parse_int(tokens, "FALT")

    # Crypto fields
    hash_value = _parse_str(tokens, "HASH") or None
    signature = _parse_str(tokens, "ASSI") or None

    # Parse cargo blocks
    elections = _parse_elections(raw)

    return BulletinData(
        process=process,
        plea=plea,
        turn=turn,
        state=state,
        municipality_code=municipality,
        zone=zone,
        section=section,
        eligible_voters=eligible,
        compared_voters=compared,
        absent_voters=absent,
        elections=elections,
        hash_value=hash_value,
        signature=signature,
        raw_text=raw,
    )


def _parse_elections(raw: str) -> list[ElectionResult]:
    """
    Extract election results per cargo from raw QR text.

    The TSE format interleaves cargo/candidate blocks. We split on IDCA occurrences
    and process each block independently.
    """
    elections: list[ElectionResult] = []

    # Split raw text into cargo blocks by finding IDCA tags
    # Each block starts at IDCA and ends before the next IDCA (or end of string)
    blocks = re.split(r"(?=\bIDCA:)", raw)

    for block in blocks:
        if not block.strip() or "IDCA:" not in block:
            continue

        btokens = _tokenize(block)
        cargo_code = _parse_str(btokens, "IDCA")
        if not cargo_code:
            continue

        blank = _parse_int(btokens, "VBRA")
        null = _parse_int(btokens, "VNUL")
        nominal = _parse_int(btokens, "VNOM")
        legenda = _parse_int(btokens, "VLEG")
        total = _parse_int(btokens, "TOTA")

        valid = nominal + legenda

        # Candidate votes: IDDV:number QTDV:qty pairs
        candidates = _parse_candidates(block)

        # If total is missing, compute it
        if total == 0:
            total = valid + blank + null

        elections.append(ElectionResult(
            cargo_code=cargo_code,
            valid_votes=valid,
            blank_votes=blank,
            null_votes=null,
            total_votes=total,
            candidates=candidates,
        ))

    return elections


def _parse_candidates(block: str) -> list[CandidateVotes]:
    """Extract IDDV/QTDV pairs from a cargo block."""
    candidates: list[CandidateVotes] = []
    # Find all IDDV:number ... QTDV:qty sequences
    pairs = re.findall(r"IDDV:(\S+).*?QTDV:(\d+)", block, re.DOTALL)
    for number, qty in pairs:
        candidates.append(CandidateVotes(number=number, votes=int(qty)))
    return candidates


def extract_qr_part_header(raw: str) -> QRCodePart:
    """
    Extract the multi-QR header from raw text.

    The first token is expected to be: QRBU:{index}:{total}
    Falls back to index=1, total=1 for single-QR BUs that omit the header.
    """
    match = re.match(r"QRBU:(\d+):(\d+)", raw.strip())
    if match:
        return QRCodePart(index=int(match.group(1)), total=int(match.group(2)), raw_text=raw)
    return QRCodePart(index=1, total=1, raw_text=raw)
