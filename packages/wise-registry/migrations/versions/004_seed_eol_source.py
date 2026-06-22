"""Encyclopedia of Life source registry seed.

Revision ID: 004_seed_eol_source
Revises: 003_agent_capability_registry
Create Date: 2026-06-22
"""

from __future__ import annotations

import json
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "004_seed_eol_source"
down_revision: Union[str, None] = "003_agent_capability_registry"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SEED_ACTOR = "wise-registry-seed"
EOL_HOMEPAGE = "https://eol.org/"


def upgrade() -> None:
    conn = op.get_bind()

    row = conn.execute(
        sa.text(
            """
            INSERT INTO registry.sources (
                canonical_name, stable_id, display_name,
                source_type_id, license_id,
                homepage_url, api_url, trust_level, active,
                created_by, updated_by
            )
            SELECT
                'eol', 'eol', 'Encyclopedia of Life',
                st.id,
                lic.id,
                :homepage_url,
                'https://eol.org/api/',
                'authoritative'::registry.trust_level_enum,
                true,
                :actor, :actor
            FROM registry.source_types st
            JOIN registry.licenses lic ON lic.code = 'CC-BY-4.0'
            WHERE st.code = 'biodiversity'
            ON CONFLICT (canonical_name) DO NOTHING
            RETURNING id
            """
        ),
        {"actor": SEED_ACTOR, "homepage_url": EOL_HOMEPAGE},
    ).fetchone()

    if row is None:
        existing = conn.execute(
            sa.text("SELECT id FROM registry.sources WHERE canonical_name = 'eol'")
        ).fetchone()
        if existing is None:
            return
        source_id = existing[0]
    else:
        source_id = row[0]

    conn.execute(
        sa.text(
            """
            INSERT INTO registry.provenance_events (
                source_id, event_type, actor, evidence_uris, notes,
                created_by, updated_by
            )
            SELECT
                :source_id,
                'register'::registry.provenance_event_type_enum,
                :actor,
                CAST(:evidence_uris AS jsonb),
                'Initial registration of authoritative source eol (Encyclopedia of Life)',
                :actor, :actor
            WHERE NOT EXISTS (
                SELECT 1 FROM registry.provenance_events pe
                WHERE pe.source_id = :source_id
                  AND pe.event_type = 'register'::registry.provenance_event_type_enum
            )
            """
        ),
        {
            "source_id": source_id,
            "actor": SEED_ACTOR,
            "evidence_uris": json.dumps([EOL_HOMEPAGE]),
        },
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        sa.text(
            """
            DELETE FROM registry.provenance_events
            WHERE source_id IN (SELECT id FROM registry.sources WHERE canonical_name = 'eol')
              AND notes LIKE 'Initial registration of authoritative source eol%'
            """
        )
    )
    conn.execute(sa.text("DELETE FROM registry.sources WHERE canonical_name = 'eol'"))
