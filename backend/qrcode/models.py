"""Pydantic models for Boletim de Urna data."""
from typing import Optional
from pydantic import BaseModel, Field, model_validator


class CandidateVotes(BaseModel):
    """Votes for a single candidate or option."""

    number: str = Field(description="Candidate number or special code (BRANC, NULO, etc.)")
    votes: int = Field(ge=0)
    name: Optional[str] = None  # populated later from TSE data


class ElectionResult(BaseModel):
    """Results for a single cargo (office) within a BU."""

    cargo_code: str = Field(description="TSE cargo code, e.g. '1' = President, '3' = Governor")
    cargo_name: Optional[str] = None
    valid_votes: int = Field(ge=0)
    blank_votes: int = Field(ge=0)
    null_votes: int = Field(ge=0)
    total_votes: int = Field(ge=0)
    candidates: list[CandidateVotes] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_totals(self) -> "ElectionResult":
        computed = self.valid_votes + self.blank_votes + self.null_votes
        if computed != self.total_votes:
            raise ValueError(
                f"Cargo {self.cargo_code}: valid({self.valid_votes}) + "
                f"blank({self.blank_votes}) + null({self.null_votes}) = {computed} "
                f"!= total({self.total_votes})"
            )
        return self


class BulletinData(BaseModel):
    """Parsed and validated Boletim de Urna (BU)."""

    # Identification — used as DynamoDB key
    process: str = Field(description="PROC — processo eleitoral")
    plea: str = Field(description="PLEI — pleito")
    turn: str = Field(description="TURN — turno")
    state: str = Field(description="UNFE — UF")
    municipality_code: str = Field(description="MUNI — código IBGE do município")
    zone: str = Field(description="ZONA — zona eleitoral")
    section: str = Field(description="SECA — seção eleitoral")

    # Electoral roll
    eligible_voters: int = Field(ge=0, description="APTO — eleitores aptos")
    compared_voters: int = Field(ge=0, description="COMP — comparecimento")
    absent_voters: int = Field(ge=0, description="FALT — ausentes")

    # Results per cargo
    elections: list[ElectionResult] = Field(default_factory=list)

    # Crypto
    hash_value: Optional[str] = None  # SHA-512 hex
    signature: Optional[str] = None  # Ed25519 hex
    sig_verified: bool = False

    # Raw storage for audit
    raw_text: Optional[str] = None

    @property
    def pk(self) -> str:
        return f"{self.process}#{self.plea}#{self.turn}"

    @property
    def sk(self) -> str:
        return f"{self.state}#{self.municipality_code}#{self.zone}#{self.section}"

    @model_validator(mode="after")
    def validate_roll(self) -> "BulletinData":
        if self.compared_voters + self.absent_voters != self.eligible_voters:
            raise ValueError(
                f"COMP({self.compared_voters}) + FALT({self.absent_voters}) "
                f"!= APTO({self.eligible_voters})"
            )
        return self


class QRCodePart(BaseModel):
    """One QR code fragment from a multi-QR bulletin."""

    index: int = Field(ge=1, description="1-based QR index")
    total: int = Field(ge=1, description="Total QR codes in this BU")
    raw_text: str
    hash_value: Optional[str] = None  # hash of this part (if present)


class IngestRequest(BaseModel):
    """Payload received from the frontend."""

    qr_codes: list[str] = Field(min_length=1, description="Raw decoded QR code text(s)")
