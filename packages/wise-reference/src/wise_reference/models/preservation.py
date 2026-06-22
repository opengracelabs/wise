"""Preservation models."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wise_reference.base import AuditMixin, Base, UUIDPrimaryKeyMixin
from wise_reference.enums import ApprovalStatus

APPROVAL_STATUS_ENUM = ENUM(
    ApprovalStatus,
    name="approval_status_enum",
    schema="preservation",
    create_type=False,
    values_callable=lambda enum: [member.value for member in enum],
)


class PreservationObject(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "objects"
    __table_args__ = (
        UniqueConstraint("stable_id", name="uq_preservation_objects_stable_id"),
        UniqueConstraint("ark", name="uq_preservation_objects_ark"),
        {"schema": "preservation"},
    )

    stable_id: Mapped[str] = mapped_column(String(128), nullable=False)
    ark: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[ApprovalStatus] = mapped_column(
        APPROVAL_STATUS_ENUM,
        nullable=False,
        server_default=ApprovalStatus.PROPOSED.value,
    )
    discovery_record_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("discovery.records.id"),
        nullable=False,
    )
    object_descriptor: Mapped[dict] = mapped_column(JSONB, nullable=False)
    fixity_digest: Mapped[str] = mapped_column(String(128), nullable=False)
    fixity_verified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    storage_tier: Mapped[str] = mapped_column(String(8), nullable=False, server_default="T0")
    minio_key: Mapped[str | None] = mapped_column(String(512), nullable=True)
    rights_uri: Mapped[str] = mapped_column(String(512), nullable=False)
    ingest_event_id: Mapped[str] = mapped_column(String(128), nullable=False)

    premis_events: Mapped[list["PremisEvent"]] = relationship(back_populates="preservation_object")


class PremisEvent(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "premis_events"
    __table_args__ = {"schema": "preservation"}

    preservation_object_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("preservation.objects.id"),
        nullable=False,
    )
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    event_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    agent_version: Mapped[str] = mapped_column(String(64), nullable=False)
    actor_id: Mapped[str] = mapped_column(String(255), nullable=False, server_default="system")
    event_detail: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_uris: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    outcome: Mapped[str] = mapped_column(String(32), nullable=False, server_default="success")
    event_data: Mapped[dict] = mapped_column(JSONB, nullable=False)

    preservation_object: Mapped["PreservationObject"] = relationship(back_populates="premis_events")
