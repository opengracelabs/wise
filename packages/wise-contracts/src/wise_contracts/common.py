"""Shared contract primitives for WISE interface contracts (architecture-v1.0 §7)."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, HttpUrl


class ApprovalStatus(StrEnum):
    """Steward approval workflow states (04-system-diagram §2.2)."""

    PROPOSED = "proposed"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"


class EvidenceOutputProfile(BaseModel):
    """Evidence Output Profile (03-canonical-architecture §6.6)."""

    evidence_uris: list[HttpUrl | str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
    evidence_summary: str
    method: str
    source_registry_refs: list[str] = Field(default_factory=list)
    provenance_event_id: str | None = None


class ProvenanceRef(BaseModel):
    """Lightweight provenance chain link."""

    event_id: str
    event_type: str
    agent_version: str
    event_timestamp: datetime
    actor_id: str = "system"
