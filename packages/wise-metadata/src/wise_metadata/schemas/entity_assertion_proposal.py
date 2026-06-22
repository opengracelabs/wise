"""Entity assertion proposal schemas (no graph placement)."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from wise_metadata.enums import AssertionStatus, MappingTarget
from wise_metadata.schemas.audit import AuditFields, AuditFieldsCreate
from wise_metadata.schemas.evidence import EvidenceProfile


class EntityAssertionProposalCreate(BaseModel):
    """Propose RDF-ready entity assertion for steward review."""

    mapping_run_id: UUID
    normalized_record_id: UUID
    subject_uri: str = Field(max_length=512)
    predicate: str = Field(max_length=256)
    object_value: str
    object_type: str = Field(default="literal", max_length=32)
    language: str | None = Field(default=None, max_length=16)
    entity_type: str = Field(max_length=64)
    mapping_target: MappingTarget
    rights_uri: str | None = Field(default=None, max_length=512)
    evidence: EvidenceProfile
    audit: AuditFieldsCreate = Field(default_factory=AuditFieldsCreate)


class EntityAssertionProposalRead(BaseModel):
    """Read entity assertion proposal."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    mapping_run_id: UUID
    normalized_record_id: UUID
    subject_uri: str
    predicate: str
    object_value: str
    object_type: str
    language: str | None
    entity_type: str
    mapping_target: MappingTarget
    status: AssertionStatus
    rights_uri: str | None
    evidence: EvidenceProfile
    audit: AuditFields
