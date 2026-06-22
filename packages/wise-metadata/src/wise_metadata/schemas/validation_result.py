"""Validation result schemas."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from wise_metadata.enums import ValidationDomain, ValidationStatus
from wise_metadata.schemas.audit import AuditFields, AuditFieldsCreate
from wise_metadata.schemas.evidence import EvidenceProfile


class ValidationResultCreate(BaseModel):
    """Record source, rights, or schema validation outcome."""

    normalized_record_id: UUID
    source_id: UUID
    validation_domain: ValidationDomain
    status: ValidationStatus
    severity: str = Field(default="info", max_length=16)
    findings: list[dict] = Field(default_factory=list)
    mapping_run_id: UUID | None = None
    rights_status_id: UUID | None = None
    license_id: UUID | None = None
    evidence: EvidenceProfile
    audit: AuditFieldsCreate = Field(default_factory=AuditFieldsCreate)


class ValidationResultRead(BaseModel):
    """Read validation result."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    normalized_record_id: UUID
    source_id: UUID
    mapping_run_id: UUID | None
    validation_domain: ValidationDomain
    status: ValidationStatus
    severity: str
    findings: list[dict]
    rights_status_id: UUID | None
    license_id: UUID | None
    evidence: EvidenceProfile
    audit: AuditFields
