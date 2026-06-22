"""Mapping run schemas."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from wise_metadata.enums import MappingRunStatus
from wise_metadata.schemas.audit import AuditFields, AuditFieldsCreate


class MappingRunCreate(BaseModel):
    """Start a schema mapping run for a normalized record."""

    normalized_record_id: UUID
    source_id: UUID
    agent_version: str = Field(default="metadata-agent@1.0.0", max_length=64)
    audit: AuditFieldsCreate = Field(default_factory=AuditFieldsCreate)


class MappingRunRead(BaseModel):
    """Mapping run execution record."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    normalized_record_id: UUID
    source_id: UUID
    agent_version: str
    status: MappingRunStatus
    mappings_applied: int
    unmapped_fields: list[str]
    started_at: datetime
    completed_at: datetime | None
    audit: AuditFields
