"""Mapping run execution audit."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import ARRAY, ENUM, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wise_metadata.base import AuditMixin, Base, UUIDPrimaryKeyMixin
from wise_metadata.enums import MappingRunStatus

MAPPING_RUN_STATUS_ENUM = ENUM(
    MappingRunStatus,
    name="mapping_run_status_enum",
    schema="modeling",
    create_type=False,
    values_callable=lambda enum: [member.value for member in enum],
)


class MappingRun(Base, UUIDPrimaryKeyMixin, AuditMixin):
    """Schema mapping execution for a normalized record."""

    __tablename__ = "mapping_runs"
    __table_args__ = {"schema": "modeling"}

    normalized_record_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("modeling.normalized_records.id"),
        nullable=False,
    )
    source_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("registry.sources.id"),
        nullable=False,
    )
    agent_version: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[MappingRunStatus] = mapped_column(
        MAPPING_RUN_STATUS_ENUM,
        nullable=False,
        server_default=MappingRunStatus.PENDING.value,
    )
    mappings_applied: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    unmapped_fields: Mapped[list] = mapped_column(JSONB, nullable=False, server_default="[]")
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    normalized_record: Mapped["NormalizedRecord"] = relationship(back_populates="mapping_runs")
    assertion_proposals: Mapped[list["EntityAssertionProposal"]] = relationship(
        back_populates="mapping_run"
    )


from wise_metadata.models.entity_assertion_proposal import EntityAssertionProposal  # noqa: E402, F401
from wise_metadata.models.normalized_record import NormalizedRecord  # noqa: E402, F401
