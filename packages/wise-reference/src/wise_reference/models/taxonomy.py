"""GBIF Taxonomic Backbone models."""

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
    schema="taxonomy",
    create_type=False,
    values_callable=lambda enum: [member.value for member in enum],
)


class TaxonomicBackboneNode(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "backbone_nodes"
    __table_args__ = (
        UniqueConstraint("gbif_usage_key", name="uq_taxonomy_backbone_gbif_usage_key"),
        {"schema": "taxonomy"},
    )

    gbif_usage_key: Mapped[str] = mapped_column(String(32), nullable=False)
    scientific_name: Mapped[str] = mapped_column(String(255), nullable=False)
    taxonomic_rank: Mapped[str] = mapped_column(String(64), nullable=False)
    parent_usage_key: Mapped[str | None] = mapped_column(String(32), nullable=True)
    status: Mapped[ApprovalStatus] = mapped_column(
        APPROVAL_STATUS_ENUM,
        nullable=False,
        server_default=ApprovalStatus.APPROVED.value,
    )
    kingdom: Mapped[str | None] = mapped_column(String(128), nullable=True)
    phylum: Mapped[str | None] = mapped_column(String(128), nullable=True)
    taxonomic_class: Mapped[str | None] = mapped_column(String(128), nullable=True)
    taxonomic_order: Mapped[str | None] = mapped_column(String(128), nullable=True)
    family: Mapped[str | None] = mapped_column(String(128), nullable=True)
    genus: Mapped[str | None] = mapped_column(String(128), nullable=True)
    node_data: Mapped[dict] = mapped_column(JSONB, nullable=False)

    species_links: Mapped[list["SpeciesBackboneLink"]] = relationship(
        back_populates="backbone_node"
    )


class SpeciesBackboneLink(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "species_backbone_links"
    __table_args__ = (
        UniqueConstraint(
            "species_registry_id",
            "backbone_node_id",
            name="uq_species_backbone_link",
        ),
        {"schema": "taxonomy"},
    )

    species_registry_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("species.registry_entries.id"),
        nullable=False,
    )
    backbone_node_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("taxonomy.backbone_nodes.id"),
        nullable=False,
    )
    link_type: Mapped[str] = mapped_column(String(32), nullable=False, server_default="exactMatch")
    link_data: Mapped[dict] = mapped_column(JSONB, nullable=False)

    species_entry: Mapped["SpeciesRegistryEntry"] = relationship(back_populates="backbone_links")
    backbone_node: Mapped["TaxonomicBackboneNode"] = relationship(back_populates="species_links")
