"""ProvenanceEvent Pydantic schemas."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from wise_registry.enums import ProvenanceEventType
from wise_registry.schemas.audit import AuditFields, AuditFieldsCreate


class ProvenanceEventBase(BaseModel):
    source_id: UUID
    event_type: ProvenanceEventType
    event_timestamp: datetime | None = None
    actor: str = Field(default="system", max_length=255)
    evidence_uri: str | None = Field(default=None, max_length=512)
    notes: str | None = None


class ProvenanceEventCreate(ProvenanceEventBase, AuditFieldsCreate):
    pass


class ProvenanceEventRead(ProvenanceEventBase, AuditFields):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    event_timestamp: datetime
