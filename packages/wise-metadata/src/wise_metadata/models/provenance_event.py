"""Modeling-layer provenance events."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, ENUM, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wise_metadata.base import AuditMixin, Base, UUIDPrimaryKeyMixin
from wise_metadata.enums import ModelingEventType

MODELING_EVENT_TYPE_ENUM = ENUM(
    ModelingEventType,
    name="modeling_event_type_enum",
    schema="modeling",
    create_type=False,
    values_callable=lambda enum: [member.value for member in enum],
)


class ModelingProvenanceEvent(Base, UUIDPrimaryKeyMixin, AuditMixin):
    """PREMIS-aligned modeling events linked to registry provenance chain."""

    __tablename__ = "provenance_events"
    __table_args__ = {"schema": "modeling"}

    event_type: Mapped[ModelingEventType] = mapped_column(MODELING_EVENT_TYPE_ENUM, nullable=False)
    linked_entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    linked_entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    source_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("registry.sources.id"),
        nullable=False,
    )
    registry_provenance_event_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("registry.provenance_events.id"),
        nullable=True,
    )
    actor: Mapped[str] = mapped_column(String(255), nullable=False)
    agent_version: Mapped[str] = mapped_column(String(64), nullable=False)
    evidence_uris: Mapped[list[str]] = mapped_column(
        ARRAY(Text),
        nullable=False,
        server_default="{}",
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    normalized_records: Mapped[list["NormalizedRecord"]] = relationship(
        back_populates="normalization_event",
        foreign_keys="NormalizedRecord.normalization_event_id",
    )
