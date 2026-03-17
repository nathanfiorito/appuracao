"""
Multi-QR Code assembler.

Some BUs are split across 2–4 QR codes. The assembler collects all parts
(identified by QRBU:{index}:{total}) and concatenates them in order once all
parts are present.
"""

from .models import QRCodePart
from .parser import extract_qr_part_header


class AssemblyError(Exception):
    pass


def needs_assembly(raw_codes: list[str]) -> bool:
    """Return True if the input requires multi-QR assembly."""
    if len(raw_codes) > 1:
        return True
    header = extract_qr_part_header(raw_codes[0])
    return header.total > 1


def assemble(raw_codes: list[str]) -> str:
    """
    Assemble multiple QR code parts into a single raw BU text.

    Args:
        raw_codes: List of raw QR code texts in any order.

    Returns:
        Concatenated raw text (parts joined with newline, headers stripped).

    Raises:
        AssemblyError: If parts are missing or duplicated.
    """
    parts: dict[int, QRCodePart] = {}

    for raw in raw_codes:
        part = extract_qr_part_header(raw)
        if part.index in parts:
            raise AssemblyError(f"Duplicate QR part index {part.index}")
        parts[part.index] = part

    if not parts:
        raise AssemblyError("No QR parts provided")

    # Validate completeness
    total = next(iter(parts.values())).total
    for part in parts.values():
        if part.total != total:
            raise AssemblyError(
                f"Inconsistent total across parts: {part.total} vs {total}"
            )

    missing = set(range(1, total + 1)) - set(parts.keys())
    if missing:
        raise AssemblyError(f"Missing QR parts: {sorted(missing)}")

    # Concatenate in order
    assembled_parts = []
    for i in range(1, total + 1):
        text = parts[i].raw_text
        # Strip the QRBU header line from all parts except the first
        # so the combined text parses as a single document
        if i > 1:
            text = _strip_qrbu_header(text)
        assembled_parts.append(text.strip())

    return "\n".join(assembled_parts)


def _strip_qrbu_header(raw: str) -> str:
    """Remove the leading QRBU:n:m token from a QR part."""
    import re
    return re.sub(r"^QRBU:\d+:\d+\s*", "", raw.strip())


def assemble_from_parts(parts: list[QRCodePart]) -> str:
    """Assemble from already-parsed QRCodePart objects."""
    return assemble([p.raw_text for p in parts])
