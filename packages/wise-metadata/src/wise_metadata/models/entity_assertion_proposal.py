"""Entity assertion proposals (no canonical graph placement)."""

from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ENUM, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wise_metadata.base import AuditMixin, Base, UUIDPrimaryKeyMixin
from wise_metadata.enums import AssertionStatus, MappingTarget

ASSERTION_STATUS_ENUM = ENUM(
    AssertionStatus,
    name="assertion_status_enum",
    schema="modeling",
    create_type=False,
    values_callable=lambda enum: [member.value for member in enum],
)
MAPPING_TARGET_ENUM = ENUM(
    MappingTarget,
    name="mapping_target_enum",
    schema="modeling",
    create_type=False,
    values_callable=lambda enum: [member.value for member in enum],
)


class EntityAssertionProposal(Base, UUIDPrimaryKeyMixin, AuditMixin):
    """RDF-ready entity assertion candidate pending steward approval."""

    __tablename__ = "entity_assertion_proposals"
    __table_args__ = {"schema": "modeling"}

    mapping_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("modeling.mapping_runs.id"),
        nullable=False,
    )
    normalized_record_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("modeling.normalized_records.id"),
        nullable=False,
    )
    subject_uri: Mapped[str] = mapped_column(String(512), nullable=False)
    predicate: Mapped[str] = mapped_column(String(256), nullable=False)
    object_value: Mapped[str] = mapped_column(Text, nullable=False)
    object_type: Mapped[str] = mapped_column(String(32), nullable=False, server_default="literal")
    language: Mapped[str | None] = mapped_column(String(16), nullable=True)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    mapping_target: Mapped[MappingTarget] = mapped_column(MAPPING_TARGET_ENUM, nullable=False)
    status: Mapped[AssertionStatus] = mapped_column(
        ASSERTION_STATUS_ENUM,
        nullable=False,
        server_default=AssertionStatus.PROPOSED.value,
    )
    rights_uri: Mapped[str | None] = mapped_column(String(512), nullable=True)
    evidence: Mapped[dict] = mapped_column(JSONB, nullable=False)

    mapping_run: Mapped["MappingRun"] = relationship(back_populates="assertion_proposals")
    normalized_record: Mapped["NormalizedRecord"] = relationship(back_populates="assertion_proposals")


from wise_metadata.models.mapping_run import MappingRun  # noqa: E402, F401
from wise_metadata.models.normalized_record import NormalizedRecord  # noqa: E402, F401
