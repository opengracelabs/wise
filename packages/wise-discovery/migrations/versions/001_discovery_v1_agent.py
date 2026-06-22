"""Discovery Agent v1 columns on discovery.records.

Revision ID: 001_discovery_v1_agent
Revises: 006_seed_everglades
Create Date: 2026-06-22

Requires registry and reference migrations (discovery.records from RC1).
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001_discovery_v1_agent"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS discovery")

    op.alter_column(
        "records",
        "status",
        new_column_name="approval_status",
        schema="discovery",
    )

    op.alter_column("records", "title", nullable=True, schema="discovery")
    op.alter_column("records", "source_registry_ref", nullable=True, schema="discovery")
    op.alter_column("records", "rights_uri", nullable=True, schema="discovery")
    op.alter_column("records", "ingestion_candidacy_score", nullable=True, schema="discovery")
    op.alter_column("records", "external_identifiers", nullable=True, schema="discovery")
    op.alter_column("records", "record_data", nullable=True, schema="discovery")
    op.alter_column("records", "discovery_event_id", nullable=True, schema="discovery")

    op.add_column(
        "records",
        sa.Column("source_id", postgresql.UUID(as_uuid=True), nullable=True),
        schema="discovery",
    )
    op.add_column(
        "records",
        sa.Column("source_record_uri", sa.String(length=512), nullable=True),
        schema="discovery",
    )
    op.add_column(
        "records",
        sa.Column("raw_payload_ref", sa.String(length=512), nullable=True),
        schema="discovery",
    )
    op.add_column(
        "records",
        sa.Column(
            "discovery_timestamp",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        schema="discovery",
    )
    op.add_column(
        "records",
        sa.Column("confidence", sa.Float(), nullable=True),
        schema="discovery",
    )
    op.add_column(
        "records",
        sa.Column(
            "evidence_uris",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
        schema="discovery",
    )

    op.create_foreign_key(
        "fk_discovery_records_source_id",
        "records",
        "sources",
        ["source_id"],
        ["id"],
        source_schema="discovery",
        referent_schema="registry",
    )

    op.execute(
        """
        ALTER TABLE discovery.records
        ADD CONSTRAINT fk_discovery_records_provenance_event_id
        FOREIGN KEY (provenance_event_id)
        REFERENCES registry.provenance_events(id)
        NOT VALID
        """
    )


def downgrade() -> None:
    op.execute(
        "ALTER TABLE discovery.records DROP CONSTRAINT IF EXISTS fk_discovery_records_provenance_event_id"
    )
    op.drop_constraint(
        "fk_discovery_records_source_id",
        "records",
        schema="discovery",
        type_="foreignkey",
    )

    op.drop_column("records", "evidence_uris", schema="discovery")
    op.drop_column("records", "confidence", schema="discovery")
    op.drop_column("records", "discovery_timestamp", schema="discovery")
    op.drop_column("records", "raw_payload_ref", schema="discovery")
    op.drop_column("records", "source_record_uri", schema="discovery")
    op.drop_column("records", "source_id", schema="discovery")

    op.alter_column("records", "discovery_event_id", nullable=False, schema="discovery")
    op.alter_column("records", "record_data", nullable=False, schema="discovery")
    op.alter_column("records", "external_identifiers", nullable=False, schema="discovery")
    op.alter_column("records", "ingestion_candidacy_score", nullable=False, schema="discovery")
    op.alter_column("records", "rights_uri", nullable=False, schema="discovery")
    op.alter_column("records", "source_registry_ref", nullable=False, schema="discovery")
    op.alter_column("records", "title", nullable=False, schema="discovery")

    op.alter_column(
        "records",
        "approval_status",
        new_column_name="status",
        schema="discovery",
    )
