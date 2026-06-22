"""Reference Capability 2 species and taxonomy schemas.

Revision ID: 003_rc2_species_schemas
Revises: 002_seed_stonehenge
Create Date: 2026-06-22
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "003_rc2_species_schemas"
down_revision: Union[str, None] = "002_seed_stonehenge"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

AUDIT_COLUMNS = [
    sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    sa.Column("created_by", sa.String(length=255), server_default="system", nullable=False),
    sa.Column("updated_by", sa.String(length=255), server_default="system", nullable=False),
    sa.Column("row_version", sa.Integer(), server_default="1", nullable=False),
]

APPROVAL_VALUES = ("proposed", "approved", "rejected", "superseded")


def _approval_enum(schema: str) -> postgresql.ENUM:
    return postgresql.ENUM(
        *APPROVAL_VALUES,
        name="approval_status_enum",
        schema=schema,
        create_type=False,
    )


def upgrade() -> None:
    for schema in ("species", "taxonomy"):
        op.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")

    species_status = _approval_enum("species")
    taxonomy_status = _approval_enum("taxonomy")
    species_status.create(op.get_bind(), checkfirst=True)
    taxonomy_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "registry_entries",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("stable_id", sa.String(length=128), nullable=False),
        sa.Column("status", species_status, server_default="proposed", nullable=False),
        sa.Column("species_uri", sa.String(length=512), nullable=False),
        sa.Column("scientific_name", sa.String(length=255), nullable=False),
        sa.Column("scientific_name_authorship", sa.String(length=255), nullable=True),
        sa.Column("taxonomic_rank", sa.String(length=64), nullable=False),
        sa.Column("gbif_taxon_key", sa.String(length=32), nullable=False),
        sa.Column("gbif_usage_key", sa.String(length=32), nullable=False),
        sa.Column("discovery_record_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("registry_data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("provenance_event_id", postgresql.UUID(as_uuid=True), nullable=False),
        *AUDIT_COLUMNS,
        sa.ForeignKeyConstraint(["discovery_record_id"], ["discovery.records.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("stable_id", name="uq_species_registry_stable_id"),
        sa.UniqueConstraint("gbif_taxon_key", name="uq_species_registry_gbif_taxon_key"),
        sa.UniqueConstraint("species_uri", name="uq_species_registry_species_uri"),
        schema="species",
    )

    op.create_table(
        "backbone_nodes",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("gbif_usage_key", sa.String(length=32), nullable=False),
        sa.Column("scientific_name", sa.String(length=255), nullable=False),
        sa.Column("taxonomic_rank", sa.String(length=64), nullable=False),
        sa.Column("parent_usage_key", sa.String(length=32), nullable=True),
        sa.Column("status", taxonomy_status, server_default="approved", nullable=False),
        sa.Column("kingdom", sa.String(length=128), nullable=True),
        sa.Column("phylum", sa.String(length=128), nullable=True),
        sa.Column("taxonomic_class", sa.String(length=128), nullable=True),
        sa.Column("taxonomic_order", sa.String(length=128), nullable=True),
        sa.Column("family", sa.String(length=128), nullable=True),
        sa.Column("genus", sa.String(length=128), nullable=True),
        sa.Column("node_data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        *AUDIT_COLUMNS,
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("gbif_usage_key", name="uq_taxonomy_backbone_gbif_usage_key"),
        schema="taxonomy",
    )

    op.create_table(
        "species_backbone_links",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("species_registry_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("backbone_node_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("link_type", sa.String(length=32), server_default="exactMatch", nullable=False),
        sa.Column("link_data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        *AUDIT_COLUMNS,
        sa.ForeignKeyConstraint(["species_registry_id"], ["species.registry_entries.id"]),
        sa.ForeignKeyConstraint(["backbone_node_id"], ["taxonomy.backbone_nodes.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "species_registry_id",
            "backbone_node_id",
            name="uq_species_backbone_link",
        ),
        schema="taxonomy",
    )


def downgrade() -> None:
    op.drop_table("species_backbone_links", schema="taxonomy")
    op.drop_table("backbone_nodes", schema="taxonomy")
    op.drop_table("registry_entries", schema="species")
    op.execute("DROP TYPE IF EXISTS taxonomy.approval_status_enum")
    op.execute("DROP TYPE IF EXISTS species.approval_status_enum")
    op.execute("DROP SCHEMA IF EXISTS taxonomy CASCADE")
    op.execute("DROP SCHEMA IF EXISTS species CASCADE")
