"""RC17 rights and provenance infrastructure.

Revision ID: 007_rc17_rights_provenance
Revises: 006_merge_rc3_and_v1_1
Create Date: 2026-06-22

Changes:
- Add source verification and rights status linkage
- Add asset, attribution, and publication approval registries
- Enforce RC17 publication sequence constraints
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "007_rc17_rights_provenance"
down_revision: Union[str, tuple[str, ...], None] = "006_merge_rc3_and_v1_1"
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
    op.execute(
        """
        DO $$ BEGIN
            CREATE TYPE registry.verification_status_enum AS ENUM (
                'pending', 'verified', 'failed'
            );
        EXCEPTION WHEN duplicate_object THEN NULL; END $$;
        """
    )
    op.execute(
        """
        DO $$ BEGIN
            CREATE TYPE registry.approval_workflow_status_enum AS ENUM (
                'pending', 'approved', 'rejected', 'revoked'
            );
        EXCEPTION WHEN duplicate_object THEN NULL; END $$;
        """
    )

    verification_status = postgresql.ENUM(
        "pending",
        "verified",
        "failed",
        name="verification_status_enum",
        schema="registry",
        create_type=False,
    )
    approval_status = postgresql.ENUM(
        "pending",
        "approved",
        "rejected",
        "revoked",
        name="approval_workflow_status_enum",
        schema="registry",
        create_type=False,
    )

    op.add_column(
        "sources",
        sa.Column("rights_status_id", postgresql.UUID(as_uuid=True), nullable=True),
        schema="registry",
    )
    op.add_column(
        "sources",
        sa.Column(
            "source_verification_status",
            verification_status,
            server_default="pending",
            nullable=False,
        ),
        schema="registry",
    )
    op.add_column(
        "sources",
        sa.Column("source_verified_at", sa.DateTime(timezone=True), nullable=True),
        schema="registry",
    )
    op.add_column(
        "sources",
        sa.Column("source_verified_by", sa.String(length=255), nullable=True),
        schema="registry",
    )
    op.create_foreign_key(
        "fk_sources_rights_status_id",
        "sources",
        "rights_statuses",
        ["rights_status_id"],
        ["id"],
        source_schema="registry",
        referent_schema="registry",
    )
    op.create_index(
        "ix_sources_rights_status_id",
        "sources",
        ["rights_status_id"],
        schema="registry",
    )
    op.create_index(
        "ix_sources_source_verification_status",
        "sources",
        ["source_verification_status"],
        schema="registry",
    )

    op.create_table(
        "assets",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("stable_id", sa.String(length=128), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("asset_type", sa.String(length=64), nullable=False),
        sa.Column("source_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_record_uri", sa.String(length=512), nullable=True),
        sa.Column("canonical_uri", sa.String(length=512), nullable=True),
        sa.Column("license_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("rights_status_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("provenance_event_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "source_verification_status",
            verification_status,
            server_default="pending",
            nullable=False,
        ),
        sa.Column("source_verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("source_verified_by", sa.String(length=255), nullable=True),
        sa.Column(
            "license_verification_status",
            verification_status,
            server_default="pending",
            nullable=False,
        ),
        sa.Column("license_verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("license_verified_by", sa.String(length=255), nullable=True),
        sa.Column(
            "provenance_verification_status",
            verification_status,
            server_default="pending",
            nullable=False,
        ),
        sa.Column("provenance_verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("provenance_verified_by", sa.String(length=255), nullable=True),
        sa.Column(
            "rights_approval_status",
            approval_status,
            server_default="pending",
            nullable=False,
        ),
        sa.Column("rights_approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("rights_approved_by", sa.String(length=255), nullable=True),
        sa.Column(
            "publication_approval_status",
            approval_status,
            server_default="pending",
            nullable=False,
        ),
        sa.Column("publication_approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("publication_approved_by", sa.String(length=255), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        *AUDIT_COLUMNS,
        sa.CheckConstraint(
            "(license_verification_status != 'verified') OR license_id IS NOT NULL",
            name="ck_assets_verified_license_has_license",
        ),
        sa.CheckConstraint(
            "(provenance_verification_status != 'verified') OR provenance_event_id IS NOT NULL",
            name="ck_assets_verified_provenance_has_event",
        ),
        sa.CheckConstraint(
            "(rights_approval_status != 'approved') OR rights_status_id IS NOT NULL",
            name="ck_assets_approved_rights_has_status",
        ),
        sa.CheckConstraint(
            "(publication_approval_status != 'approved') OR "
            "(source_verification_status = 'verified' "
            "AND license_verification_status = 'verified' "
            "AND provenance_verification_status = 'verified' "
            "AND rights_approval_status = 'approved' "
            "AND publication_approved_at IS NOT NULL)",
            name="ck_assets_publication_requires_rc17_sequence",
        ),
        sa.ForeignKeyConstraint(["source_id"], ["registry.sources.id"]),
        sa.ForeignKeyConstraint(["license_id"], ["registry.licenses.id"]),
        sa.ForeignKeyConstraint(["rights_status_id"], ["registry.rights_statuses.id"]),
        sa.ForeignKeyConstraint(["provenance_event_id"], ["registry.provenance_events.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("stable_id", name="uq_assets_stable_id"),
        schema="registry",
    )
    op.create_index("ix_assets_source_id", "assets", ["source_id"], schema="registry")
    op.create_index("ix_assets_license_id", "assets", ["license_id"], schema="registry")
    op.create_index(
        "ix_assets_rights_status_id",
        "assets",
        ["rights_status_id"],
        schema="registry",
    )
    op.create_index(
        "ix_assets_publication_approval_status",
        "assets",
        ["publication_approval_status"],
        schema="registry",
    )

    op.create_table(
        "attributions",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("asset_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("license_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("rights_status_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("display_text", sa.String(length=512), nullable=False),
        sa.Column("credit_line", sa.String(length=512), nullable=True),
        sa.Column("attribution_uri", sa.String(length=512), nullable=True),
        sa.Column("required", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("sort_order", sa.Integer(), server_default="0", nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        *AUDIT_COLUMNS,
        sa.ForeignKeyConstraint(["asset_id"], ["registry.assets.id"]),
        sa.ForeignKeyConstraint(["source_id"], ["registry.sources.id"]),
        sa.ForeignKeyConstraint(["license_id"], ["registry.licenses.id"]),
        sa.ForeignKeyConstraint(["rights_status_id"], ["registry.rights_statuses.id"]),
        sa.PrimaryKeyConstraint("id"),
        schema="registry",
    )
    op.create_index("ix_attributions_asset_id", "attributions", ["asset_id"], schema="registry")
    op.create_index("ix_attributions_source_id", "attributions", ["source_id"], schema="registry")

    op.create_table(
        "publication_approvals",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("asset_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "approval_status",
            approval_status,
            server_default="pending",
            nullable=False,
        ),
        sa.Column("requested_by", sa.String(length=255), server_default="system", nullable=False),
        sa.Column(
            "requested_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("approved_by", sa.String(length=255), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("publication_channel", sa.String(length=128), nullable=True),
        sa.Column("publication_uri", sa.String(length=512), nullable=True),
        sa.Column("source_verified_snapshot", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("license_verified_snapshot", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("provenance_verified_snapshot", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("rights_approved_snapshot", sa.Boolean(), server_default="false", nullable=False),
        sa.Column(
            "attribution_snapshot",
            postgresql.JSONB(),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column("decision_notes", sa.Text(), nullable=True),
        *AUDIT_COLUMNS,
        sa.CheckConstraint(
            "(approval_status != 'approved') OR "
            "(source_verified_snapshot "
            "AND license_verified_snapshot "
            "AND provenance_verified_snapshot "
            "AND rights_approved_snapshot "
            "AND approved_at IS NOT NULL)",
            name="ck_publication_approvals_requires_rc17_sequence",
        ),
        sa.ForeignKeyConstraint(["asset_id"], ["registry.assets.id"]),
        sa.PrimaryKeyConstraint("id"),
        schema="registry",
    )
    op.create_index(
        "ix_publication_approvals_asset_id",
        "publication_approvals",
        ["asset_id"],
        schema="registry",
    )
    op.create_index(
        "ix_publication_approvals_status",
        "publication_approvals",
        ["approval_status"],
        schema="registry",
    )


def downgrade() -> None:
    op.drop_index(
        "ix_publication_approvals_status",
        table_name="publication_approvals",
        schema="registry",
    )
    op.drop_index(
        "ix_publication_approvals_asset_id",
        table_name="publication_approvals",
        schema="registry",
    )
    op.drop_table("publication_approvals", schema="registry")

    op.drop_index("ix_attributions_source_id", table_name="attributions", schema="registry")
    op.drop_index("ix_attributions_asset_id", table_name="attributions", schema="registry")
    op.drop_table("attributions", schema="registry")

    op.drop_index(
        "ix_assets_publication_approval_status",
        table_name="assets",
        schema="registry",
    )
    op.drop_index("ix_assets_rights_status_id", table_name="assets", schema="registry")
    op.drop_index("ix_assets_license_id", table_name="assets", schema="registry")
    op.drop_index("ix_assets_source_id", table_name="assets", schema="registry")
    op.drop_table("assets", schema="registry")

    op.drop_index(
        "ix_sources_source_verification_status",
        table_name="sources",
        schema="registry",
    )
    op.drop_index("ix_sources_rights_status_id", table_name="sources", schema="registry")
    op.drop_constraint(
        "fk_sources_rights_status_id",
        "sources",
        schema="registry",
        type_="foreignkey",
    )
    op.drop_column("sources", "source_verified_by", schema="registry")
    op.drop_column("sources", "source_verified_at", schema="registry")
    op.drop_column("sources", "source_verification_status", schema="registry")
    op.drop_column("sources", "rights_status_id", schema="registry")

    op.execute("DROP TYPE IF EXISTS registry.approval_workflow_status_enum")
    op.execute("DROP TYPE IF EXISTS registry.verification_status_enum")
