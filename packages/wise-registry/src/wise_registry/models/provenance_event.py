"""Provenance event audit model (PREMIS-aligned)."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func, text
from sqlalchemy.dialects.postgresql import ENUM, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wise_registry.base import AuditMixin, Base, UUIDPrimaryKeyMixin
from wise_registry.enums import ProvenanceEventType

PROVENANCE_EVENT_TYPE_ENUM = ENUM(
    ProvenanceEventType,
    name="provenance_event_type_enum",
    schema="registry",
    create_type=False,
    values_callable=lambda enum: [member.value for member in enum],
)


class ProvenanceEvent(Base, UUIDPrimaryKeyMixin, AuditMixin):
    """Audit log entry in a source provenance chain."""

    __tablename__ = "provenance_events"
    __table_args__ = {"schema": "registry"}

    source_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("registry.sources.id"),
        nullable=False,
    )
    event_type: Mapped[ProvenanceEventType] = mapped_column(
        PROVENANCE_EVENT_TYPE_ENUM,
        nullable=False,
    )
    event_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    actor: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        server_default="system",
        comment="Steward, service, or agent principal",
    )
    evidence_uris: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False,
        server_default=text("'[]'::jsonb"),
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    previous_event_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("registry.provenance_events.id"),
        nullable=True,
    )

    source: Mapped["Source"] = relationship(
        back_populates="provenance_events",
        foreign_keys=[source_id],
    )
    previous_event: Mapped["ProvenanceEvent | None"] = relationship(
        "ProvenanceEvent",
        remote_side="ProvenanceEvent.id",
        foreign_keys=[previous_event_id],
        back_populates="next_events",
    )
    next_events: Mapped[list["ProvenanceEvent"]] = relationship(
        "ProvenanceEvent",
        foreign_keys="ProvenanceEvent.previous_event_id",
        back_populates="previous_event",
    )

    def __repr__(self) -> str:
        return f"<ProvenanceEvent type={self.event_type!r} source={self.source_id!r}>"


from wise_registry.models.source import Source  # noqa: E402, F401
