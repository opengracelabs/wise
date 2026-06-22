"""Evidence Output Profile Pydantic schema."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class EvidenceProfile(BaseModel):
    """Canonical evidence attachment per 03-canonical-architecture.md §6.6."""

    model_config = ConfigDict(extra="forbid")

    evidence_uris: list[str] = Field(min_length=1)
    confidence: float = Field(ge=0.0, le=1.0)
    evidence_summary: str = Field(min_length=1)
    method: str = Field(
        min_length=1,
        description="Derivation method: rule-based, feed-direct, steward-reviewed, etc.",
    )
    source_registry_refs: list[str] = Field(min_length=1)
    provenance_event_id: UUID | None = None
