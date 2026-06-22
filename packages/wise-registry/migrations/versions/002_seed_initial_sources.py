"""Seed initial Source Registry reference data and authoritative sources.

Revision ID: 002_seed_initial_sources
Revises: 001_initial_source_registry
Create Date: 2026-06-22

Initial sources: UNESCO, Wikidata, Wikimedia Commons, OpenStreetMap, GBIF.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "002_seed_initial_sources"
down_revision: Union[str, None] = "001_initial_source_registry"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SEED_ACTOR = "wise-registry-seed"


def upgrade() -> None:
    conn = op.get_bind()

    source_types = [
        {
            "code": "authority",
            "label": "Authority File",
            "description": "Authoritative reference data provider (UNESCO, Wikidata, GBIF)",
        },
        {
            "code": "media_repository",
            "label": "Media Repository",
            "description": "Open media and cultural asset repository",
        },
        {
            "code": "geospatial",
            "label": "Geospatial Foundation",
            "description": "Open geospatial data and map infrastructure",
        },
        {
            "code": "biodiversity",
            "label": "Biodiversity Data",
            "description": "Species occurrence and taxonomy data infrastructure",
        },
    ]
    for row in source_types:
        conn.execute(
            sa.text(
                """
                INSERT INTO registry.source_types (code, label, description, created_by, updated_by)
                VALUES (:code, :label, :description, :actor, :actor)
                ON CONFLICT (code) DO NOTHING
                """
            ),
            {**row, "actor": SEED_ACTOR},
        )

    licenses = [
        {
            "code": "CC0-1.0",
            "uri": "https://creativecommons.org/publicdomain/zero/1.0/",
            "label": "Creative Commons Zero 1.0",
            "spdx_id": "CC0-1.0",
            "description": "Public domain dedication",
        },
        {
            "code": "CC-BY-4.0",
            "uri": "https://creativecommons.org/licenses/by/4.0/",
            "label": "Creative Commons Attribution 4.0",
            "spdx_id": "CC-BY-4.0",
            "description": "Attribution required",
        },
        {
            "code": "ODbL-1.0",
            "uri": "https://opendatacommons.org/licenses/odbl/1-0/",
            "label": "Open Database License 1.0",
            "spdx_id": None,
            "description": "Share-alike for database contents",
        },
    ]
    for row in licenses:
        conn.execute(
            sa.text(
                """
                INSERT INTO registry.licenses (code, uri, label, spdx_id, description, created_by, updated_by)
                VALUES (:code, :uri, :label, :spdx_id, :description, :actor, :actor)
                ON CONFLICT (code) DO NOTHING
                """
            ),
            {**row, "actor": SEED_ACTOR},
        )

    rights_statuses = [
        {
            "code": "NoC-OKLR",
            "uri": "http://rightsstatements.org/vocab/NoC-OKLR/1.0/",
            "label": "No Copyright - Other Known Legal Restrictions",
            "description": "Public domain or open license with other legal restrictions",
        },
        {
            "code": "NoC-NCR",
            "uri": "http://rightsstatements.org/vocab/NoC-NCR/1.0/",
            "label": "No Copyright - Non-Commercial Use Only",
            "description": "No copyright but non-commercial use restrictions may apply",
        },
        {
            "code": "CNE",
            "uri": "http://rightsstatements.org/vocab/CNE/1.0/",
            "label": "Copyright Not Evaluated",
            "description": "Rights status has not been evaluated",
        },
    ]
    for row in rights_statuses:
        conn.execute(
            sa.text(
                """
                INSERT INTO registry.rights_statuses (code, uri, label, description, created_by, updated_by)
                VALUES (:code, :uri, :label, :description, :actor, :actor)
                ON CONFLICT (code) DO NOTHING
                """
            ),
            {**row, "actor": SEED_ACTOR},
        )

    sources = [
        {
            "canonical_name": "unesco",
            "display_name": "UNESCO World Heritage Centre",
            "source_type_code": "authority",
            "license_code": None,
            "homepage_url": "https://whc.unesco.org/",
            "api_url": "https://whc.unesco.org/en/syndication/",
            "trust_level": "authoritative",
        },
        {
            "canonical_name": "wikidata",
            "display_name": "Wikidata",
            "source_type_code": "authority",
            "license_code": "CC0-1.0",
            "homepage_url": "https://www.wikidata.org/",
            "api_url": "https://query.wikidata.org/sparql",
            "trust_level": "authoritative",
        },
        {
            "canonical_name": "wikimedia-commons",
            "display_name": "Wikimedia Commons",
            "source_type_code": "media_repository",
            "license_code": "CC-BY-4.0",
            "homepage_url": "https://commons.wikimedia.org/",
            "api_url": "https://commons.wikimedia.org/w/api.php",
            "trust_level": "high",
        },
        {
            "canonical_name": "openstreetmap",
            "display_name": "OpenStreetMap",
            "source_type_code": "geospatial",
            "license_code": "ODbL-1.0",
            "homepage_url": "https://www.openstreetmap.org/",
            "api_url": "https://api.openstreetmap.org/api/0.6/",
            "trust_level": "authoritative",
        },
        {
            "canonical_name": "gbif",
            "display_name": "GBIF",
            "source_type_code": "biodiversity",
            "license_code": "CC0-1.0",
            "homepage_url": "https://www.gbif.org/",
            "api_url": "https://api.gbif.org/v1/",
            "trust_level": "authoritative",
        },
    ]

    insert_source_sql = sa.text(
        """
        INSERT INTO registry.sources (
            canonical_name, display_name,
            source_type_id, license_id,
            homepage_url, api_url, trust_level, active,
            created_by, updated_by
        )
        SELECT
            :canonical_name, :display_name,
            st.id,
            lic.id,
            :homepage_url, :api_url,
            CAST(:trust_level AS registry.trust_level_enum),
            true,
            :actor, :actor
        FROM registry.source_types st
        LEFT JOIN registry.licenses lic ON lic.code = :license_code
        WHERE st.code = :source_type_code
        ON CONFLICT (canonical_name) DO NOTHING
        RETURNING id, canonical_name, display_name
        """
    )

    for source in sources:
        row = conn.execute(
            insert_source_sql,
            {
                "canonical_name": source["canonical_name"],
                "display_name": source["display_name"],
                "source_type_code": source["source_type_code"],
                "license_code": source["license_code"],
                "homepage_url": source["homepage_url"],
                "api_url": source["api_url"],
                "trust_level": source["trust_level"],
                "actor": SEED_ACTOR,
            },
        ).fetchone()

        if row is None:
            existing = conn.execute(
                sa.text(
                    """
                    SELECT id, canonical_name, display_name
                    FROM registry.sources
                    WHERE canonical_name = :canonical_name
                    """
                ),
                {"canonical_name": source["canonical_name"]},
            ).fetchone()
            if existing is None:
                continue
            source_id, canonical_name, display_name = existing
        else:
            source_id, canonical_name, display_name = row

        conn.execute(
            sa.text(
                """
                INSERT INTO registry.provenance_events (
                    source_id, event_type, actor, evidence_uri, notes,
                    created_by, updated_by
                )
                VALUES (
                    :source_id,
                    'register'::registry.provenance_event_type_enum,
                    :actor,
                    :evidence_uri,
                    :notes,
                    :actor, :actor
                )
                """
            ),
            {
                "source_id": source_id,
                "actor": SEED_ACTOR,
                "evidence_uri": source["homepage_url"],
                "notes": f"Initial registration of authoritative source {canonical_name} ({display_name})",
            },
        )


def downgrade() -> None:
    conn = op.get_bind()
    canonical_names = ("unesco", "wikidata", "wikimedia-commons", "openstreetmap", "gbif")
    conn.execute(
        sa.text(
            """
            DELETE FROM registry.provenance_events
            WHERE source_id IN (
                SELECT id FROM registry.sources WHERE canonical_name = ANY(:canonical_names)
            )
            """
        ),
        {"canonical_names": list(canonical_names)},
    )
    conn.execute(
        sa.text("DELETE FROM registry.sources WHERE canonical_name = ANY(:canonical_names)"),
        {"canonical_names": list(canonical_names)},
    )
    conn.execute(
        sa.text(
            """
            DELETE FROM registry.rights_statuses
            WHERE code IN ('NoC-OKLR', 'NoC-NCR', 'CNE')
            """
        )
    )
    conn.execute(
        sa.text(
            """
            DELETE FROM registry.licenses
            WHERE code IN ('CC0-1.0', 'CC-BY-4.0', 'ODbL-1.0')
            """
        )
    )
    conn.execute(
        sa.text(
            """
            DELETE FROM registry.source_types
            WHERE code IN ('authority', 'media_repository', 'geospatial', 'biodiversity')
            """
        )
    )
