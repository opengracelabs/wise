"""Reference Capability 3 protected area schema with PostGIS.

Revision ID: 005_rc3_protected_areas
Revises: 004_seed_panthera_leo
Create Date: 2026-06-22
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from geoalchemy2 import Geometry
from sqlalchemy.dialects import postgresql

revision: str = "005_rc3_protected_areas"
down_revision: Union[str, None] = "004_seed_panthera_leo"
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


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    op.execute("CREATE SCHEMA IF NOT EXISTS conservation")

    conservation_status = postgresql.ENUM(
        *APPROVAL_VALUES,
        name="approval_status_enum",
        schema="conservation",
        create_type=False,
    )
    conservation_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "protected_areas",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("stable_id", sa.String(length=128), nullable=False),
        sa.Column("status", conservation_status, server_default="proposed", nullable=False),
        sa.Column("pref_label", sa.String(length=512), nullable=False),
        sa.Column("designation_type", sa.String(length=64), nullable=False),
        sa.Column("graph_entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("discovery_record_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("boundary", Geometry(geometry_type="MULTIPOLYGON", srid=4326), nullable=False),
        sa.Column("centroid", Geometry(geometry_type="POINT", srid=4326), nullable=False),
        sa.Column("conservation_metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("external_identifiers", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("area_data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("provenance_event_id", postgresql.UUID(as_uuid=True), nullable=False),
        *AUDIT_COLUMNS,
        sa.ForeignKeyConstraint(["graph_entity_id"], ["graph.entities.id"]),
        sa.ForeignKeyConstraint(["discovery_record_id"], ["discovery.records.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("stable_id", name="uq_protected_areas_stable_id"),
        schema="conservation",
    )

    op.create_index(
        "ix_protected_areas_boundary_gist",
        "protected_areas",
        ["boundary"],
        schema="conservation",
        postgresql_using="gist",
    )
    op.create_index(
        "ix_protected_areas_centroid_gist",
        "protected_areas",
        ["centroid"],
        schema="conservation",
        postgresql_using="gist",
    )


def downgrade() -> None:
    op.drop_index("ix_protected_areas_centroid_gist", table_name="protected_areas", schema="conservation")
    op.drop_index("ix_protected_areas_boundary_gist", table_name="protected_areas", schema="conservation")
    op.drop_table("protected_areas", schema="conservation")
    op.execute("DROP TYPE IF EXISTS conservation.approval_status_enum")
    op.execute("DROP SCHEMA IF EXISTS conservation CASCADE")
