"""Initial Source Registry schema.

Revision ID: 001_initial_source_registry
Revises:
Create Date: 2026-06-22

"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001_initial_source_registry"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

AUDIT_COLUMNS = [
    sa.Column(
        "created_at",
        sa.DateTime(timezone=True),
        server_default=sa.text("now()"),
        nullable=False,
    ),
    sa.Column(
        "updated_at",
        sa.DateTime(timezone=True),
        server_default=sa.text("now()"),
        nullable=False,
    ),
    sa.Column(
        "created_by",
        sa.String(length=255),
        server_default="system",
        nullable=False,
    ),
    sa.Column(
        "updated_by",
        sa.String(length=255),
        server_default="system",
        nullable=False,
    ),
    sa.Column(
        "row_version",
        sa.Integer(),
        server_default="1",
        nullable=False,
    ),
]


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS registry")

    op.execute(
        """
        DO $$ BEGIN
            CREATE TYPE registry.trust_level_enum AS ENUM (
                'authoritative', 'high', 'medium', 'low', 'unverified'
            );
        EXCEPTION WHEN duplicate_object THEN NULL; END $$;
        """
    )
    op.execute(
        """
        DO $$ BEGIN
            CREATE TYPE registry.provenance_event_type_enum AS ENUM (
                'register', 'update', 'harvest', 'approve', 'deprecate', 'link'
            );
        EXCEPTION WHEN duplicate_object THEN NULL; END $$;
        """
    )

    trust_level = postgresql.ENUM(
        "authoritative",
        "high",
        "medium",
        "low",
        "unverified",
        name="trust_level_enum",
        schema="registry",
        create_type=False,
    )
    provenance_event_type = postgresql.ENUM(
        "register",
        "update",
        "harvest",
        "approve",
        "deprecate",
        "link",
        name="provenance_event_type_enum",
        schema="registry",
        create_type=False,
    )

    op.create_table(
        "source_types",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("label", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        *AUDIT_COLUMNS,
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code", name="uq_source_types_code"),
        schema="registry",
    )

    op.create_table(
        "licenses",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("uri", sa.String(length=512), nullable=False),
        sa.Column("label", sa.String(length=255), nullable=False),
        sa.Column("spdx_id", sa.String(length=64), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        *AUDIT_COLUMNS,
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code", name="uq_licenses_code"),
        sa.UniqueConstraint("uri", name="uq_licenses_uri"),
        schema="registry",
    )

    op.create_table(
        "rights_statuses",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("uri", sa.String(length=512), nullable=False),
        sa.Column("label", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        *AUDIT_COLUMNS,
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code", name="uq_rights_statuses_code"),
        sa.UniqueConstraint("uri", name="uq_rights_statuses_uri"),
        schema="registry",
    )

    op.create_table(
        "sources",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("canonical_name", sa.String(length=128), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("source_type_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("homepage_url", sa.String(length=512), nullable=False),
        sa.Column("api_url", sa.String(length=512), nullable=True),
        sa.Column("license_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "trust_level",
            trust_level,
            server_default="unverified",
            nullable=False,
        ),
        sa.Column("active", sa.Boolean(), server_default="true", nullable=False),
        *AUDIT_COLUMNS,
        sa.ForeignKeyConstraint(["source_type_id"], ["registry.source_types.id"]),
        sa.ForeignKeyConstraint(["license_id"], ["registry.licenses.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("canonical_name", name="uq_sources_canonical_name"),
        schema="registry",
    )
    op.create_index("ix_sources_source_type_id", "sources", ["source_type_id"], schema="registry")
    op.create_index("ix_sources_active", "sources", ["active"], schema="registry")

    op.create_table(
        "provenance_events",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("source_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("event_type", provenance_event_type, nullable=False),
        sa.Column(
            "event_timestamp",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("actor", sa.String(length=255), server_default="system", nullable=False),
        sa.Column("evidence_uri", sa.String(length=512), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        *AUDIT_COLUMNS,
        sa.ForeignKeyConstraint(["source_id"], ["registry.sources.id"]),
        sa.PrimaryKeyConstraint("id"),
        schema="registry",
    )
    op.create_index(
        "ix_provenance_events_source_id",
        "provenance_events",
        ["source_id"],
        schema="registry",
    )


def downgrade() -> None:
    op.drop_index("ix_provenance_events_source_id", table_name="provenance_events", schema="registry")
    op.drop_table("provenance_events", schema="registry")
    op.drop_index("ix_sources_active", table_name="sources", schema="registry")
    op.drop_index("ix_sources_source_type_id", table_name="sources", schema="registry")
    op.drop_table("sources", schema="registry")
    op.drop_table("rights_statuses", schema="registry")
    op.drop_table("licenses", schema="registry")
    op.drop_table("source_types", schema="registry")

    op.execute("DROP TYPE IF EXISTS registry.provenance_event_type_enum")
    op.execute("DROP TYPE IF EXISTS registry.trust_level_enum")
    op.execute("DROP SCHEMA IF EXISTS registry CASCADE")
