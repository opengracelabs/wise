"""Normalized metadata record schemas."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from wise_metadata.enums import SourceSchema
from wise_metadata.schemas.audit import AuditFields, AuditFieldsCreate


class NormalizedRecordCreate(BaseModel):
    """Ingest raw source metadata for normalization."""

    source_id: UUID
    external_record_id: str = Field(min_length=1, max_length=512)
    source_schema: SourceSchema
    source_schema_version: str = Field(default="1.0", max_length=32)
    raw_payload: dict
    language: str | None = Field(default=None, max_length=16)
    registry_provenance_event_id: UUID | None = None
    audit: AuditFieldsCreate = Field(default_factory=AuditFieldsCreate)


class NormalizedRecordRead(BaseModel):
    """Normalized metadata record with preserved originals."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    source_id: UUID
    external_record_id: str
    source_schema: SourceSchema
    source_schema_version: str
    raw_payload: dict
    normalized_payload: dict
    original_literals: dict
    language: str | None
    registry_provenance_event_id: UUID | None
    normalization_event_id: UUID | None
    audit: AuditFields
