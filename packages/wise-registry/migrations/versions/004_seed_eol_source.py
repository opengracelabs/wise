"""Encyclopedia of Life source registry seed.

Revision ID: 004_seed_eol_source
Revises: 003_agent_capability_registry
Create Date: 2026-06-22
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "004_seed_eol_source"
down_revision: Union[str, None] = "003_agent_capability_registry"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SEED_ACTOR = "wise-registry-seed"


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        sa.text(
            """
            INSERT INTO registry.sources (
                canonical_name, display_name,
                source_type_id, license_id,
                homepage_url, api_url, trust_level, active,
                created_by, updated_by
            )
            SELECT
                'eol', 'Encyclopedia of Life',
                st.id,
                lic.id,
                'https://eol.org/',
                'https://eol.org/api/',
                'authoritative'::registry.trust_level_enum,
                true,
                :actor, :actor
            FROM registry.source_types st
            JOIN registry.licenses lic ON lic.code = 'CC-BY-4.0'
            WHERE st.code = 'biodiversity'
            ON CONFLICT (canonical_name) DO NOTHING
            """
        ),
        {"actor": SEED_ACTOR},
    )


def downgrade() -> None:
    op.execute("DELETE FROM registry.sources WHERE canonical_name = 'eol'")
