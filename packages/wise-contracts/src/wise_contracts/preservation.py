"""Preservation contracts (11-preservation-agent §6)."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from wise_contracts.common import ApprovalStatus, ProvenanceRef


class FixityRecord(BaseModel):
    """SHA-256 fixity verification record."""

    algorithm: str = "sha256"
    digest: str
    verified_at: datetime
    result: str = "pass"


class PreservedObjectDescriptor(BaseModel):
    """OAIS Archival Information Package descriptor (11-preservation-agent §6.3)."""

    ark: str
    stable_id: str
    status: ApprovalStatus = ApprovalStatus.PROPOSED
    format_uri: str = "http://www.nationalarchives.gov.uk/pronom/x-fmt/111"
    format_label: str = "Plain Text"
    fixity: FixityRecord
    storage_tier: str = "T0"
    replica_count: int = 1
    minio_key: str | None = None
    rights_uri: str
    provenance: ProvenanceRef
    discovery_record_id: str
    ingest_event_id: str


class PremisEvent(BaseModel):
    """PREMIS preservation event (11-preservation-agent §6.2)."""

    id: str
    event_type: str
    event_timestamp: datetime
    agent_version: str
    actor_id: str = "system"
    preservation_object_ark: str
    event_detail: str
    evidence_uris: list[str] = Field(default_factory=list)
    outcome: str = "success"
