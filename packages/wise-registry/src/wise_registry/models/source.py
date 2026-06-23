"""Source registry entry model."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wise_registry.base import AuditMixin, Base, UUIDPrimaryKeyMixin
from wise_registry.enums import TrustLevel, VerificationStatus

TRUST_LEVEL_ENUM = ENUM(
    TrustLevel,
    name="trust_level_enum",
    schema="registry",
    create_type=False,
    values_callable=lambda enum: [member.value for member in enum],
)

VERIFICATION_STATUS_ENUM = ENUM(
    VerificationStatus,
    name="verification_status_enum",
    schema="registry",
    create_type=False,
    values_callable=lambda enum: [member.value for member in enum],
)


class Source(Base, UUIDPrimaryKeyMixin, AuditMixin):
    """Registered authoritative or public source."""

    __tablename__ = "sources"
    __table_args__ = (
        UniqueConstraint("canonical_name", name="uq_sources_canonical_name"),
        UniqueConstraint("stable_id", name="uq_sources_stable_id"),
        {"schema": "registry"},
    )

    canonical_name: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        comment="Stable institutional identifier (e.g. unesco, wikidata)",
    )
    stable_id: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        comment="Pipeline source_registry_ref alias (e.g. unesco-whc, ramsar)",
    )
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    source_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("registry.source_types.id"),
        nullable=False,
    )
    homepage_url: Mapped[str] = mapped_column(String(512), nullable=False)
    api_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
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
    trust_level: Mapped[TrustLevel] = mapped_column(
        TRUST_LEVEL_ENUM,
        nullable=False,
        server_default=TrustLevel.UNVERIFIED.value,
    )
    source_verification_status: Mapped[VerificationStatus] = mapped_column(
        VERIFICATION_STATUS_ENUM,
        nullable=False,
        server_default=VerificationStatus.PENDING.value,
    )
    source_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    source_verified_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")

    source_type: Mapped["SourceType"] = relationship(back_populates="sources")
    license: Mapped["License | None"] = relationship(back_populates="sources")
    rights_status: Mapped["RightsStatus | None"] = relationship(back_populates="sources")
    assets: Mapped[list["Asset"]] = relationship(back_populates="source")
    attributions: Mapped[list["Attribution"]] = relationship(back_populates="source")
    provenance_events: Mapped[list["ProvenanceEvent"]] = relationship(
        back_populates="source",
        foreign_keys="ProvenanceEvent.source_id",
    )

    def __repr__(self) -> str:
        return f"<Source canonical_name={self.canonical_name!r}>"


from wise_registry.models.license import License  # noqa: E402, F401
from wise_registry.models.provenance_event import ProvenanceEvent  # noqa: E402, F401
from wise_registry.models.rights_status import RightsStatus  # noqa: E402, F401
from wise_registry.models.source_type import SourceType  # noqa: E402, F401
from wise_registry.models.asset import Asset  # noqa: E402, F401
from wise_registry.models.attribution import Attribution  # noqa: E402, F401
