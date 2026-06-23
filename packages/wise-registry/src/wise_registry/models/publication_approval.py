"""RC17 publication approval workflow model."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, String, Text, func, text
from sqlalchemy.dialects.postgresql import ENUM, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wise_registry.base import AuditMixin, Base, UUIDPrimaryKeyMixin
from wise_registry.enums import ApprovalWorkflowStatus

APPROVAL_WORKFLOW_STATUS_ENUM = ENUM(
    ApprovalWorkflowStatus,
    name="approval_workflow_status_enum",
    schema="registry",
    create_type=False,
    values_callable=lambda enum: [member.value for member in enum],
)


class PublicationApproval(Base, UUIDPrimaryKeyMixin, AuditMixin):
    """Human publication approval tied to an RC17 asset gate snapshot."""

    __tablename__ = "publication_approvals"
    __table_args__ = (
        CheckConstraint(
            "(approval_status != 'approved') OR "
            "(source_verified_snapshot "
            "AND license_verified_snapshot "
            "AND provenance_verified_snapshot "
            "AND rights_approved_snapshot "
            "AND approved_at IS NOT NULL)",
            name="ck_publication_approvals_requires_rc17_sequence",
        ),
        {"schema": "registry"},
    )

    asset_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("registry.assets.id"),
        nullable=False,
    )
    approval_status: Mapped[ApprovalWorkflowStatus] = mapped_column(
        APPROVAL_WORKFLOW_STATUS_ENUM,
        nullable=False,
        server_default=ApprovalWorkflowStatus.PENDING.value,
    )
    requested_by: Mapped[str] = mapped_column(String(255), nullable=False, server_default="system")
    requested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    approved_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    publication_channel: Mapped[str | None] = mapped_column(String(128), nullable=True)
    publication_uri: Mapped[str | None] = mapped_column(String(512), nullable=True)
    source_verified_snapshot: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    license_verified_snapshot: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    provenance_verified_snapshot: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    rights_approved_snapshot: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    attribution_snapshot: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        server_default=text("'{}'::jsonb"),
    )
    decision_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    asset: Mapped["Asset"] = relationship(back_populates="publication_approvals")

    def __repr__(self) -> str:
        return f"<PublicationApproval asset_id={self.asset_id!r} status={self.approval_status!r}>"


from wise_registry.models.asset import Asset  # noqa: E402, F401
