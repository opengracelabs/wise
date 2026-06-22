"""Seed schema mapping crosswalk rules for RC1 source types.

Revision ID: 002_seed_schema_mappings
Revises: 001_initial_modeling_schema
Create Date: 2026-06-22
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "002_seed_schema_mappings"
down_revision: Union[str, None] = "001_initial_modeling_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SEED_ACTOR = "metadata-agent@1.0.0"

MAPPINGS = [
    # UNESCO World Heritage
    ("unesco", "site", "dublin_core", "dcterms:title", "E27", 10),
    ("unesco", "id_no", "dublin_core", "dcterms:identifier", "E27", 20),
    ("unesco", "short_description", "dublin_core", "dcterms:description", "E27", 30),
    ("unesco", "latitude", "cidoc_crm", "geo:lat", "E53", 40),
    ("unesco", "longitude", "cidoc_crm", "geo:long", "E53", 50),
    # Wikidata
    ("wikidata", "id", "dublin_core", "dcterms:identifier", None, 10),
    ("wikidata", "labels.en.value", "dublin_core", "dcterms:title", None, 20),
    ("wikidata", "descriptions.en.value", "dublin_core", "dcterms:description", None, 30),
    ("wikidata", "id", "skos", "wikidata:entity", None, 40),
    # Wikimedia Commons
    ("wikimedia-commons", "title", "dublin_core", "dcterms:title", "E73", 10),
    ("wikimedia-commons", "title", "dublin_core", "dcterms:identifier", "E73", 20),
    ("wikimedia-commons", "artist", "dublin_core", "dcterms:creator", "E39", 30),
    ("wikimedia-commons", "license", "dublin_core", "dcterms:rights", "E73", 40),
    # OpenStreetMap
    ("openstreetmap", "tags.name", "dublin_core", "dcterms:title", "E53", 10),
    ("openstreetmap", "id", "dublin_core", "dcterms:identifier", "E53", 20),
    ("openstreetmap", "lat", "cidoc_crm", "geo:lat", "E53", 30),
    ("openstreetmap", "lon", "cidoc_crm", "geo:long", "E53", 40),
    ("openstreetmap", "tags.wikidata", "skos", "osm:wikidata", "E53", 50),
]


def upgrade() -> None:
    conn = op.get_bind()
    for source, field_path, target, term, crm_class, priority in MAPPINGS:
        conn.execute(
            sa.text(
                """
                INSERT INTO modeling.schema_mappings (
                    source_canonical_name, source_field_path, mapping_target, target_term,
                    crm_class, transform_rule, priority, active, created_by, updated_by
                )
                VALUES (
                    :source, :field_path,
                    CAST(:target AS modeling.mapping_target_enum),
                    :term, :crm_class, 'direct', :priority, true, :actor, :actor
                )
                ON CONFLICT ON CONSTRAINT uq_schema_mappings_crosswalk DO NOTHING
                """
            ),
            {
                "source": source,
                "field_path": field_path,
                "target": target,
                "term": term,
                "crm_class": crm_class,
                "priority": priority,
                "actor": SEED_ACTOR,
            },
        )


def downgrade() -> None:
    conn = op.get_bind()
    for source, field_path, target, term, _crm, _priority in MAPPINGS:
        conn.execute(
            sa.text(
                """
                DELETE FROM modeling.schema_mappings
                WHERE source_canonical_name = :source
                  AND source_field_path = :field_path
                  AND mapping_target = CAST(:target AS modeling.mapping_target_enum)
                  AND target_term = :term
                """
            ),
            {"source": source, "field_path": field_path, "target": target, "term": term},
        )
