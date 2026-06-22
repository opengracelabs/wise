"""Discovery record Pydantic schemas."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from wise_discovery.enums import ApprovalStatus
from wise_discovery.schemas.audit import AuditFields, AuditFieldsCreate
from wise_discovery.schemas.evidence import EvidenceProfile


class DiscoveryRecordCreate(BaseModel):
    """Input for creating a discovery record via the agent."""

    stable_id: str = Field(min_length=1, max_length=128)
    source_id: UUID
    source_record_uri: str = Field(min_length=1, max_length=512)
    raw_payload_ref: str | None = Field(default=None, max_length=512)
    confidence: float = Field(ge=0.0, le=1.0)
    evidence_uris: list[str] = Field(min_length=1)
    evidence_summary: str = Field(min_length=1)
    method: str = Field(min_length=1)
    rights_uri: str | None = Field(default=None, max_length=512)
    title: str | None = Field(default=None, max_length=512)
    external_identifiers: dict | None = None
    record_data: dict | None = None
    approval_status: ApprovalStatus = ApprovalStatus.PROPOSED
    audit: AuditFieldsCreate = Field(default_factory=AuditFieldsCreate)


class DiscoveryRecordRead(BaseModel):
    """Discovery record as persisted in discovery.records."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    stable_id: str
    source_id: UUID | None
    source_record_uri: str | None
    raw_payload_ref: str | None
    discovery_timestamp: datetime | None
    confidence: float | None
    approval_status: ApprovalStatus
    provenance_event_id: UUID
    evidence_uris: list[str]
    rights_uri: str | None = None
    title: str | None = None
    source_registry_ref: str | None = None
    ingestion_candidacy_score: float | None = None
    external_identifiers: dict | None = None
    record_data: dict | None = None
    discovery_event_id: str | None = None
    audit: AuditFields | None = None


class SourceValidationResult(BaseModel):
    """Outcome of source validation checks."""

    status: str
    severity: str
    findings: list[dict]
    evidence: EvidenceProfile


class ReachabilityResult(BaseModel):
    """Outcome of HTTP reachability probe."""

    status: str
    url_checked: str | None
    http_status: int | None = None
    error: str | None = None


class RightsPosture(BaseModel):
    """Rights posture propagated from source registry metadata."""

    rights_uri: str | None
    license_uri: str | None
    license_code: str | None
    source_registry_ref: str
    summary: str
