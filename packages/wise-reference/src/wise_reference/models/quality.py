"""Quality review models."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from wise_reference.base import AuditMixin, Base, UUIDPrimaryKeyMixin
from wise_reference.enums import ApprovalStatus

APPROVAL_STATUS_ENUM = ENUM(
    ApprovalStatus,
    name="approval_status_enum",
    schema="quality",
    create_type=False,
    values_callable=lambda enum: [member.value for member in enum],
)


class QualityReview(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "reviews"
    __table_args__ = (
        UniqueConstraint("entity_uri", name="uq_quality_reviews_entity_uri"),
        {"schema": "quality"},
    )

    entity_uri: Mapped[str] = mapped_column(String(512), nullable=False)
    preservation_ark: Mapped[str] = mapped_column(String(255), nullable=False)
    graph_entity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("graph.entities.id"),
        nullable=False,
    )
    status: Mapped[ApprovalStatus] = mapped_column(
        APPROVAL_STATUS_ENUM,
        nullable=False,
        server_default=ApprovalStatus.PROPOSED.value,
    )
    review_domain: Mapped[str] = mapped_column(String(64), nullable=False)
    severity: Mapped[str] = mapped_column(String(32), nullable=False)
    finding: Mapped[str] = mapped_column(Text, nullable=False)
    recommended_action: Mapped[str] = mapped_column(Text, nullable=False)
    composite_score: Mapped[float] = mapped_column(Float, nullable=False)
    disposition: Mapped[str | None] = mapped_column(String(32), nullable=True)
    reviewed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    review_data: Mapped[dict] = mapped_column(JSONB, nullable=False)
