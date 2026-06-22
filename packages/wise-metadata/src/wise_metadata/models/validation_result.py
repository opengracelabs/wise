"""Validation results for source, rights, and schema checks."""

from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import ENUM, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wise_metadata.base import AuditMixin, Base, UUIDPrimaryKeyMixin
from wise_metadata.enums import ValidationDomain, ValidationStatus

VALIDATION_STATUS_ENUM = ENUM(
    ValidationStatus,
    name="validation_status_enum",
    schema="modeling",
    create_type=False,
    values_callable=lambda enum: [member.value for member in enum],
)
VALIDATION_DOMAIN_ENUM = ENUM(
    ValidationDomain,
    name="validation_domain_enum",
    schema="modeling",
    create_type=False,
    values_callable=lambda enum: [member.value for member in enum],
)


class ValidationResult(Base, UUIDPrimaryKeyMixin, AuditMixin):
    """Source, rights, or schema validation outcome."""

    __tablename__ = "validation_results"
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
    mapping_run_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("modeling.mapping_runs.id"),
        nullable=True,
    )
    validation_domain: Mapped[ValidationDomain] = mapped_column(VALIDATION_DOMAIN_ENUM, nullable=False)
    status: Mapped[ValidationStatus] = mapped_column(VALIDATION_STATUS_ENUM, nullable=False)
    severity: Mapped[str] = mapped_column(String(16), nullable=False, server_default="info")
    findings: Mapped[list] = mapped_column(JSONB, nullable=False, server_default="[]")
    rights_status_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("registry.rights_statuses.id"),
        nullable=True,
    )
    license_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("registry.licenses.id"),
        nullable=True,
    )
    evidence: Mapped[dict] = mapped_column(JSONB, nullable=False)

    normalized_record: Mapped["NormalizedRecord"] = relationship(back_populates="validation_results")


from wise_metadata.models.normalized_record import NormalizedRecord  # noqa: E402, F401
