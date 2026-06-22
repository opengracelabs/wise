"""Knowledge modeling models."""

from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wise_reference.base import AuditMixin, Base, UUIDPrimaryKeyMixin
from wise_reference.enums import ApprovalStatus

APPROVAL_STATUS_ENUM = ENUM(
    ApprovalStatus,
    name="approval_status_enum",
    schema="modeling",
    create_type=False,
    values_callable=lambda enum: [member.value for member in enum],
)


class MetadataRecord(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "metadata_records"
    __table_args__ = (
        UniqueConstraint("stable_id", name="uq_metadata_records_stable_id"),
        {"schema": "modeling"},
    )

    stable_id: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[ApprovalStatus] = mapped_column(
        APPROVAL_STATUS_ENUM,
        nullable=False,
        server_default=ApprovalStatus.PROPOSED.value,
    )
    preservation_object_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("preservation.objects.id"),
        nullable=False,
    )
    source_schema: Mapped[str] = mapped_column(String(128), nullable=False)
    source_schema_version: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    rights_uri: Mapped[str] = mapped_column(String(512), nullable=False)
    record_data: Mapped[dict] = mapped_column(JSONB, nullable=False)
    modeling_event_id: Mapped[str] = mapped_column(String(128), nullable=False)

    entity_assertions: Mapped[list["EntityAssertion"]] = relationship(
        back_populates="metadata_record"
    )


class EntityAssertion(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "entity_assertions"
    __table_args__ = {"schema": "modeling"}

    metadata_record_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("modeling.metadata_records.id"),
        nullable=False,
    )
    status: Mapped[ApprovalStatus] = mapped_column(
        APPROVAL_STATUS_ENUM,
        nullable=False,
        server_default=ApprovalStatus.PROPOSED.value,
    )
    entity_uri: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)
    entity_type: Mapped[str] = mapped_column(String(128), nullable=False)
    pref_label: Mapped[str] = mapped_column(String(512), nullable=False)
    rights_uri: Mapped[str] = mapped_column(String(512), nullable=False)
    assertion_data: Mapped[dict] = mapped_column(JSONB, nullable=False)

    metadata_record: Mapped["MetadataRecord"] = relationship(back_populates="entity_assertions")
