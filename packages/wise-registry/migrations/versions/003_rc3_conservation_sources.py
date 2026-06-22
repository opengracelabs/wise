"""RC3 conservation authority sources.

Revision ID: 003_rc3_conservation_sources
Revises: 002_seed_initial_sources
Create Date: 2026-06-22
"""

from __future__ import annotations

import json
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "003_rc3_conservation_sources"
down_revision: Union[str, None] = "002_seed_initial_sources"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SEED_ACTOR = "wise-registry-seed"


def upgrade() -> None:
    conn = op.get_bind()

    sources = [
        {
            "canonical_name": "ramsar",
            "stable_id": "ramsar",
            "display_name": "Ramsar Convention on Wetlands",
            "source_type_code": "authority",
            "license_code": None,
            "homepage_url": "https://www.ramsar.org/",
            "api_url": "https://rsis.ramsar.org/",
            "trust_level": "authoritative",
        },
        {
            "canonical_name": "unesco-mab",
            "stable_id": "unesco-mab",
            "display_name": "UNESCO Man and the Biosphere Programme",
            "source_type_code": "authority",
            "license_code": None,
            "homepage_url": "https://www.unesco.org/en/mab",
            "api_url": None,
            "trust_level": "authoritative",
        },
        {
            "canonical_name": "geonames",
            "stable_id": "geonames",
            "display_name": "GeoNames",
            "source_type_code": "geospatial",
            "license_code": "CC-BY-4.0",
            "homepage_url": "https://www.geonames.org/",
            "api_url": "https://www.geonames.org/export/",
            "trust_level": "authoritative",
        },
    ]

    insert_source_sql = sa.text(
        """
        INSERT INTO registry.sources (
            canonical_name, stable_id, display_name,
            source_type_id, license_id,
            homepage_url, api_url, trust_level, active,
            created_by, updated_by
        )
        SELECT
            :canonical_name, :stable_id, :display_name,
            st.id,
            lic.id,
            :homepage_url, :api_url,
            CAST(:trust_level AS registry.trust_level_enum),
            true,
            :actor, :actor
        FROM registry.source_types st
        LEFT JOIN registry.licenses lic ON lic.code = :license_code
        WHERE st.code = :source_type_code
        ON CONFLICT (canonical_name) DO UPDATE
        SET stable_id = EXCLUDED.stable_id,
            display_name = EXCLUDED.display_name,
            updated_by = EXCLUDED.updated_by
        RETURNING id, canonical_name
        """
    )

    for source in sources:
        row = conn.execute(insert_source_sql, {**source, "actor": SEED_ACTOR}).fetchone()
        if row is None:
            continue
        source_id, canonical_name = row
        conn.execute(
            sa.text(
                """
                INSERT INTO registry.provenance_events (
                    source_id, event_type, actor, evidence_uris, notes,
                    created_by, updated_by
                )
                VALUES (
                    :source_id,
                    'register'::registry.provenance_event_type_enum,
                    :actor,
                    CAST(:evidence_uris AS jsonb),
                    :notes,
                    :actor, :actor
                )
                """
            ),
            {
                "source_id": source_id,
                "actor": SEED_ACTOR,
                "evidence_uris": json.dumps([source["homepage_url"]]),
                "notes": f"RC3 conservation authority registration: {canonical_name}",
            },
        )


def downgrade() -> None:
    conn = op.get_bind()
    canonical_names = ("ramsar", "unesco-mab", "geonames")
    conn.execute(
        sa.text(
            """
            DELETE FROM registry.provenance_events
            WHERE source_id IN (
                SELECT id FROM registry.sources WHERE canonical_name = ANY(:names)
            )
            """
        ),
        {"names": list(canonical_names)},
    )
    conn.execute(
        sa.text("DELETE FROM registry.sources WHERE canonical_name = ANY(:names)"),
        {"names": list(canonical_names)},
    )
