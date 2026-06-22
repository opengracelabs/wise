"""Source Registry v1.1 — provenance chain hardening.

Revision ID: 005_registry_v1_1_provenance_hardening
Revises: 004_seed_eol_source, 004_seed_agents_capabilities, 003_rc3_conservation_sources
Create Date: 2026-06-22

Changes:
- evidence_uri -> evidence_uris (JSONB array)
- previous_event_id self-referential FK for linked provenance chains
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "005_registry_v1_1_provenance_hardening"
down_revision: Union[str, tuple[str, ...], None] = (
    "004_seed_eol_source",
    "004_seed_agents_capabilities",
    "003_rc3_conservation_sources",
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "provenance_events",
        sa.Column("evidence_uris", postgresql.JSONB(), nullable=True),
        schema="registry",
    )
    op.execute(
        """
        UPDATE registry.provenance_events
        SET evidence_uris = CASE
            WHEN evidence_uri IS NOT NULL THEN jsonb_build_array(evidence_uri)
            ELSE '[]'::jsonb
        END
        """
    )
    op.alter_column(
        "provenance_events",
        "evidence_uris",
        existing_type=postgresql.JSONB(),
        nullable=False,
        server_default=sa.text("'[]'::jsonb"),
        schema="registry",
    )
    op.drop_column("provenance_events", "evidence_uri", schema="registry")

    op.add_column(
        "provenance_events",
        sa.Column("previous_event_id", postgresql.UUID(as_uuid=True), nullable=True),
        schema="registry",
    )
    op.create_foreign_key(
        "fk_provenance_events_previous_event_id",
        "provenance_events",
        "provenance_events",
        ["previous_event_id"],
        ["id"],
        source_schema="registry",
        referent_schema="registry",
    )
    op.create_index(
        "ix_provenance_events_previous_event_id",
        "provenance_events",
        ["previous_event_id"],
        schema="registry",
    )


def downgrade() -> None:
    op.drop_index(
        "ix_provenance_events_previous_event_id",
        table_name="provenance_events",
        schema="registry",
    )
    op.drop_constraint(
        "fk_provenance_events_previous_event_id",
        "provenance_events",
        schema="registry",
        type_="foreignkey",
    )
    op.drop_column("provenance_events", "previous_event_id", schema="registry")

    op.add_column(
        "provenance_events",
        sa.Column("evidence_uri", sa.String(length=512), nullable=True),
        schema="registry",
    )
    op.execute(
        """
        UPDATE registry.provenance_events
        SET evidence_uri = evidence_uris->>0
        WHERE evidence_uris IS NOT NULL
          AND jsonb_typeof(evidence_uris) = 'array'
          AND jsonb_array_length(evidence_uris) > 0
        """
    )
    op.drop_column("provenance_events", "evidence_uris", schema="registry")
