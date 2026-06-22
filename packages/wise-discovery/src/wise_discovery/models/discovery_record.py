"""Discovery Record model (09-source-discovery-agent §6.2, v1 agent schema)."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, UniqueConstraint, func, text
from sqlalchemy.dialects.postgresql import ENUM, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from wise_discovery.base import AuditMixin, Base, UUIDPrimaryKeyMixin
from wise_discovery.enums import ApprovalStatus

APPROVAL_STATUS_ENUM = ENUM(
    ApprovalStatus,
    name="approval_status_enum",
    schema="discovery",
    create_type=False,
    values_callable=lambda enum: [member.value for member in enum],
)


class DiscoveryRecord(Base, UUIDPrimaryKeyMixin, AuditMixin):
    """Candidate discovery record pending steward approval."""

    __tablename__ = "records"
    __table_args__ = (
        UniqueConstraint("stable_id", name="uq_discovery_records_stable_id"),
        {"schema": "discovery"},
    )

    stable_id: Mapped[str] = mapped_column(String(128), nullable=False)
    source_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("registry.sources.id"),
        nullable=True,
    )
    source_record_uri: Mapped[str | None] = mapped_column(String(512), nullable=True)
    raw_payload_ref: Mapped[str | None] = mapped_column(String(512), nullable=True)
    discovery_timestamp: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        server_default=func.now(),
    )
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    approval_status: Mapped[ApprovalStatus] = mapped_column(
        APPROVAL_STATUS_ENUM,
        nullable=False,
        server_default=ApprovalStatus.PROPOSED.value,
    )
    provenance_event_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    evidence_uris: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False,
        server_default=text("'[]'::jsonb"),
    )

    # RC1 compatibility columns (Reference Capability seeds and contracts)
    title: Mapped[str | None] = mapped_column(String(512), nullable=True)
    source_registry_ref: Mapped[str | None] = mapped_column(String(128), nullable=True)
    rights_uri: Mapped[str | None] = mapped_column(String(512), nullable=True)
    ingestion_candidacy_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    external_identifiers: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    record_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    discovery_event_id: Mapped[str | None] = mapped_column(String(128), nullable=True)

    @property
    def status(self) -> ApprovalStatus:
        """Backward-compatible alias used by RC1 assemblers."""
        return self.approval_status

    @status.setter
    def status(self, value: ApprovalStatus | str) -> None:
        self.approval_status = ApprovalStatus(value)
