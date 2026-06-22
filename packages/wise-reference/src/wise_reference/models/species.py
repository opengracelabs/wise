"""Species Registry models."""

from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wise_reference.base import AuditMixin, Base, UUIDPrimaryKeyMixin
from wise_reference.enums import ApprovalStatus

APPROVAL_STATUS_ENUM = ENUM(
    ApprovalStatus,
    name="approval_status_enum",
    schema="species",
    create_type=False,
    values_callable=lambda enum: [member.value for member in enum],
)


class SpeciesRegistryEntry(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "registry_entries"
    __table_args__ = (
        UniqueConstraint("stable_id", name="uq_species_registry_stable_id"),
        UniqueConstraint("gbif_taxon_key", name="uq_species_registry_gbif_taxon_key"),
        UniqueConstraint("species_uri", name="uq_species_registry_species_uri"),
        {"schema": "species"},
    )

    stable_id: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[ApprovalStatus] = mapped_column(
        APPROVAL_STATUS_ENUM,
        nullable=False,
        server_default=ApprovalStatus.PROPOSED.value,
    )
    species_uri: Mapped[str] = mapped_column(String(512), nullable=False)
    scientific_name: Mapped[str] = mapped_column(String(255), nullable=False)
    scientific_name_authorship: Mapped[str | None] = mapped_column(String(255), nullable=True)
    taxonomic_rank: Mapped[str] = mapped_column(String(64), nullable=False)
    gbif_taxon_key: Mapped[str] = mapped_column(String(32), nullable=False)
    gbif_usage_key: Mapped[str] = mapped_column(String(32), nullable=False)
    discovery_record_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("discovery.records.id"),
        nullable=True,
    )
    registry_data: Mapped[dict] = mapped_column(JSONB, nullable=False)
    provenance_event_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)

    backbone_links: Mapped[list["SpeciesBackboneLink"]] = relationship(
        back_populates="species_entry"
    )
