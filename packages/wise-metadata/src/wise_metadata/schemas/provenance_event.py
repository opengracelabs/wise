"""Modeling provenance event schemas."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from wise_metadata.enums import ModelingEventType
from wise_metadata.schemas.audit import AuditFields, AuditFieldsCreate


class ModelingProvenanceEventCreate(BaseModel):
    """Create modeling-layer provenance event."""

    event_type: ModelingEventType
    linked_entity_type: str = Field(max_length=64)
    linked_entity_id: UUID
    source_id: UUID
    registry_provenance_event_id: UUID | None = None
    actor: str = Field(default="metadata-agent@1.0.0", max_length=255)
    agent_version: str = Field(default="metadata-agent@1.0.0", max_length=64)
    evidence_uris: list[str] = Field(default_factory=list)
    notes: str | None = None
    occurred_at: datetime | None = None
    audit: AuditFieldsCreate = Field(default_factory=AuditFieldsCreate)


class ModelingProvenanceEventRead(BaseModel):
    """Read modeling provenance event."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    event_type: ModelingEventType
    linked_entity_type: str
    linked_entity_id: UUID
    source_id: UUID
    registry_provenance_event_id: UUID | None
    actor: str
    agent_version: str
    evidence_uris: list[str]
    notes: str | None
    occurred_at: datetime
    audit: AuditFields
