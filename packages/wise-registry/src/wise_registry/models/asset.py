"""RC17 asset registry model."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wise_registry.base import AuditMixin, Base, UUIDPrimaryKeyMixin
from wise_registry.enums import ApprovalWorkflowStatus, VerificationStatus

VERIFICATION_STATUS_ENUM = ENUM(
    VerificationStatus,
    name="verification_status_enum",
    schema="registry",
    create_type=False,
    values_callable=lambda enum: [member.value for member in enum],
)

APPROVAL_WORKFLOW_STATUS_ENUM = ENUM(
    ApprovalWorkflowStatus,
    name="approval_workflow_status_enum",
    schema="registry",
    create_type=False,
    values_callable=lambda enum: [member.value for member in enum],
)


class Asset(Base, UUIDPrimaryKeyMixin, AuditMixin):
    """Registered asset with RC17 rights, provenance, and publication gates."""

    __tablename__ = "assets"
    __table_args__ = (
        UniqueConstraint("stable_id", name="uq_assets_stable_id"),
        CheckConstraint(
            "(license_verification_status != 'verified') OR license_id IS NOT NULL",
            name="ck_assets_verified_license_has_license",
        ),
        CheckConstraint(
            "(provenance_verification_status != 'verified') OR provenance_event_id IS NOT NULL",
            name="ck_assets_verified_provenance_has_event",
        ),
        CheckConstraint(
            "(rights_approval_status != 'approved') OR rights_status_id IS NOT NULL",
            name="ck_assets_approved_rights_has_status",
        ),
        CheckConstraint(
            "(publication_approval_status != 'approved') OR "
            "(source_verification_status = 'verified' "
            "AND license_verification_status = 'verified' "
            "AND provenance_verification_status = 'verified' "
            "AND rights_approval_status = 'approved' "
            "AND publication_approved_at IS NOT NULL)",
            name="ck_assets_publication_requires_rc17_sequence",
        ),
        {"schema": "registry"},
    )

    stable_id: Mapped[str] = mapped_column(String(128), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    asset_type: Mapped[str] = mapped_column(String(64), nullable=False)
    source_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("registry.sources.id"),
        nullable=False,
    )
    source_record_uri: Mapped[str | None] = mapped_column(String(512), nullable=True)
    canonical_uri: Mapped[str | None] = mapped_column(String(512), nullable=True)
    license_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("registry.licenses.id"),
        nullable=True,
    )
    rights_status_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("registry.rights_statuses.id"),
        nullable=True,
    )
    provenance_event_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("registry.provenance_events.id"),
        nullable=True,
    )
    source_verification_status: Mapped[VerificationStatus] = mapped_column(
        VERIFICATION_STATUS_ENUM,
        nullable=False,
        server_default=VerificationStatus.PENDING.value,
    )
    source_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    source_verified_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    license_verification_status: Mapped[VerificationStatus] = mapped_column(
        VERIFICATION_STATUS_ENUM,
        nullable=False,
        server_default=VerificationStatus.PENDING.value,
    )
    license_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    license_verified_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    provenance_verification_status: Mapped[VerificationStatus] = mapped_column(
        VERIFICATION_STATUS_ENUM,
        nullable=False,
        server_default=VerificationStatus.PENDING.value,
    )
    provenance_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    provenance_verified_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    rights_approval_status: Mapped[ApprovalWorkflowStatus] = mapped_column(
        APPROVAL_WORKFLOW_STATUS_ENUM,
        nullable=False,
        server_default=ApprovalWorkflowStatus.PENDING.value,
    )
    rights_approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    rights_approved_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    publication_approval_status: Mapped[ApprovalWorkflowStatus] = mapped_column(
        APPROVAL_WORKFLOW_STATUS_ENUM,
        nullable=False,
        server_default=ApprovalWorkflowStatus.PENDING.value,
    )
    publication_approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    publication_approved_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    source: Mapped["Source"] = relationship(back_populates="assets")
    license: Mapped["License | None"] = relationship(back_populates="assets")
    rights_status: Mapped["RightsStatus | None"] = relationship(back_populates="assets")
    provenance_event: Mapped["ProvenanceEvent | None"] = relationship(back_populates="assets")
    attributions: Mapped[list["Attribution"]] = relationship(back_populates="asset")
    publication_approvals: Mapped[list["PublicationApproval"]] = relationship(back_populates="asset")

    @property
    def rc17_sequence_complete(self) -> bool:
        """Return True when every pre-publication RC17 gate has passed."""
        return (
            self.source_verification_status == VerificationStatus.VERIFIED
            and self.license_verification_status == VerificationStatus.VERIFIED
            and self.provenance_verification_status == VerificationStatus.VERIFIED
            and self.rights_approval_status == ApprovalWorkflowStatus.APPROVED
        )

    @property
    def publishable(self) -> bool:
        """Return True only after the full RC17 gate sequence is complete."""
        return (
            self.rc17_sequence_complete
            and self.publication_approval_status == ApprovalWorkflowStatus.APPROVED
        )

    def __repr__(self) -> str:
        return f"<Asset stable_id={self.stable_id!r}>"


from wise_registry.models.attribution import Attribution  # noqa: E402, F401
from wise_registry.models.license import License  # noqa: E402, F401
from wise_registry.models.provenance_event import ProvenanceEvent  # noqa: E402, F401
from wise_registry.models.publication_approval import PublicationApproval  # noqa: E402, F401
from wise_registry.models.rights_status import RightsStatus  # noqa: E402, F401
from wise_registry.models.source import Source  # noqa: E402, F401
