"""Authority record proposal schemas."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from wise_metadata.enums import AssertionStatus, AuthorityEntityType, AuthorityMatchMethod
from wise_metadata.schemas.audit import AuditFields, AuditFieldsCreate
from wise_metadata.schemas.evidence import EvidenceProfile


class AuthorityRecordProposalCreate(BaseModel):
    """Propose authority reconciliation candidate."""

    normalized_record_id: UUID
    entity_type: AuthorityEntityType
    provisional_uri: str = Field(max_length=512)
    pref_label: str = Field(max_length=512)
    alt_labels: list[str] = Field(default_factory=list)
    external_scheme: str = Field(max_length=64)
    external_id: str = Field(max_length=128)
    link_type: str = Field(default="exactMatch", max_length=32)
    match_confidence: float = Field(ge=0.0, le=1.0)
    match_method: AuthorityMatchMethod
    skos_payload: dict = Field(default_factory=dict)
    evidence: EvidenceProfile
    audit: AuditFieldsCreate = Field(default_factory=AuditFieldsCreate)


class AuthorityRecordProposalRead(BaseModel):
    """Read authority record proposal."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    normalized_record_id: UUID
    entity_type: AuthorityEntityType
    provisional_uri: str
    pref_label: str
    alt_labels: list[str]
    external_scheme: str
    external_id: str
    link_type: str
    match_confidence: float
    match_method: AuthorityMatchMethod
    status: AssertionStatus
    skos_payload: dict
    evidence: EvidenceProfile
    audit: AuditFields
