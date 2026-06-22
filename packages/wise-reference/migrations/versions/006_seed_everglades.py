"""Everglades National Park Reference Capability 3 seed migration.

Revision ID: 006_seed_everglades
Revises: 005_rc3_protected_areas
Create Date: 2026-06-22
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from wise_reference.seed.everglades import (  # noqa: E402
    AGENT_VERSION,
    ENTITY_URI,
    RIGHTS_URI,
    SEED_ACTOR,
    SOURCE_REGISTRY_REF,
    build_everglades_seed,
)

revision: str = "006_seed_everglades"
down_revision: Union[str, None] = "005_rc3_protected_areas"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    seed = build_everglades_seed()
    conn = op.get_bind()
    now = seed["now"]
    boundary_json = json.dumps(seed["boundary_geojson"])
    centroid = seed["protected_area"]["area_data"]["centroid"]

    conn.execute(
        sa.text(
            """
            INSERT INTO discovery.records (
                id, stable_id, status, title, source_registry_ref, rights_uri,
                ingestion_candidacy_score, external_identifiers, record_data,
                provenance_event_id, discovery_event_id, created_by, updated_by
            ) VALUES (
                :id, :stable_id, 'approved', :title, :source_registry_ref, :rights_uri,
                :score, CAST(:external_ids AS jsonb), CAST(:record_data AS jsonb),
                :provenance_event_id, :discovery_event_id, :actor, :actor
            )
            ON CONFLICT (stable_id) DO NOTHING
            """
        ),
        {
            "id": str(seed["discovery"]["id"]),
            "stable_id": seed["stable_id"],
            "title": seed["title"],
            "source_registry_ref": SOURCE_REGISTRY_REF,
            "rights_uri": RIGHTS_URI,
            "score": seed["discovery"]["ingestion_candidacy_score"],
            "external_ids": json.dumps(seed["discovery"]["external_identifiers"]),
            "record_data": json.dumps(seed["discovery"]["record_data"]),
            "provenance_event_id": str(seed["discovery"]["provenance_event_id"]),
            "discovery_event_id": seed["discovery"]["discovery_event_id"],
            "actor": SEED_ACTOR,
        },
    )

    conn.execute(
        sa.text(
            """
            INSERT INTO preservation.objects (
                id, stable_id, ark, status, discovery_record_id, object_descriptor,
                fixity_digest, fixity_verified_at, storage_tier, minio_key, rights_uri,
                ingest_event_id, created_by, updated_by
            ) VALUES (
                :id, :stable_id, :ark, 'approved', :discovery_record_id,
                CAST(:object_descriptor AS jsonb), :fixity_digest, :verified_at,
                'T0', :minio_key, :rights_uri, :ingest_event_id, :actor, :actor
            )
            ON CONFLICT (stable_id) DO NOTHING
            """
        ),
        {
            "id": str(seed["preservation"]["id"]),
            "stable_id": seed["stable_id"],
            "ark": seed["ark"],
            "discovery_record_id": str(seed["discovery"]["id"]),
            "object_descriptor": json.dumps(seed["preservation"]["object_descriptor"]),
            "fixity_digest": seed["preservation"]["fixity_digest"],
            "verified_at": now,
            "minio_key": seed["preservation"]["object_descriptor"]["minio_key"],
            "rights_uri": RIGHTS_URI,
            "ingest_event_id": seed["preservation"]["ingest_event_id"],
            "actor": SEED_ACTOR,
        },
    )

    for event_id, event_data in seed["preservation"]["premis_events"]:
        conn.execute(
            sa.text(
                """
                INSERT INTO preservation.premis_events (
                    id, preservation_object_id, event_type, event_timestamp,
                    agent_version, actor_id, event_detail, evidence_uris, outcome,
                    event_data, created_by, updated_by
                ) VALUES (
                    :id, :object_id, :event_type, :event_timestamp,
                    :agent_version, :actor_id, :event_detail,
                    CAST(:evidence_uris AS jsonb), :outcome,
                    CAST(:event_data AS jsonb), :actor, :actor
                )
                ON CONFLICT (id) DO NOTHING
                """
            ),
            {
                "id": str(event_id),
                "object_id": str(seed["preservation"]["id"]),
                "event_type": event_data["event_type"],
                "event_timestamp": now,
                "agent_version": AGENT_VERSION,
                "actor_id": SEED_ACTOR,
                "event_detail": event_data["event_detail"],
                "evidence_uris": json.dumps(event_data.get("evidence_uris", [])),
                "outcome": event_data["outcome"],
                "event_data": json.dumps(event_data),
                "actor": SEED_ACTOR,
            },
        )

    conn.execute(
        sa.text(
            """
            INSERT INTO modeling.metadata_records (
                id, stable_id, status, preservation_object_id, source_schema,
                source_schema_version, title, rights_uri, record_data,
                modeling_event_id, created_by, updated_by
            ) VALUES (
                :id, :stable_id, 'approved', :preservation_object_id, :source_schema,
                :source_schema_version, :title, :rights_uri,
                CAST(:record_data AS jsonb), :modeling_event_id, :actor, :actor
            )
            ON CONFLICT (stable_id) DO NOTHING
            """
        ),
        {
            "id": str(seed["metadata"]["id"]),
            "stable_id": seed["stable_id"],
            "preservation_object_id": str(seed["preservation"]["id"]),
            "source_schema": seed["metadata"]["record_data"]["source_schema"],
            "source_schema_version": seed["metadata"]["record_data"]["source_schema_version"],
            "title": seed["title"],
            "rights_uri": RIGHTS_URI,
            "record_data": json.dumps(seed["metadata"]["record_data"]),
            "modeling_event_id": seed["metadata"]["modeling_event_id"],
            "actor": SEED_ACTOR,
        },
    )

    conn.execute(
        sa.text(
            """
            INSERT INTO modeling.entity_assertions (
                id, metadata_record_id, status, entity_uri, entity_type,
                pref_label, rights_uri, assertion_data, created_by, updated_by
            ) VALUES (
                :id, :metadata_record_id, 'approved', :entity_uri, :entity_type,
                :pref_label, :rights_uri, CAST(:assertion_data AS jsonb), :actor, :actor
            )
            ON CONFLICT (entity_uri) DO NOTHING
            """
        ),
        {
            "id": str(seed["assertion"]["id"]),
            "metadata_record_id": str(seed["metadata"]["id"]),
            "entity_uri": ENTITY_URI,
            "entity_type": seed["assertion"]["assertion_data"]["entity_type"],
            "pref_label": seed["title"],
            "rights_uri": RIGHTS_URI,
            "assertion_data": json.dumps(seed["assertion"]["assertion_data"]),
            "actor": SEED_ACTOR,
        },
    )

    conn.execute(
        sa.text(
            """
            INSERT INTO graph.entities (
                id, stable_id, entity_uri, status, label, entity_type,
                entity_assertion_id, entity_data, created_by, updated_by
            ) VALUES (
                :id, :stable_id, :entity_uri, 'approved', :label, :entity_type,
                :entity_assertion_id, CAST(:entity_data AS jsonb), :actor, :actor
            )
            ON CONFLICT (stable_id) DO NOTHING
            """
        ),
        {
            "id": str(seed["graph"]["entity_id"]),
            "stable_id": seed["stable_id"],
            "entity_uri": ENTITY_URI,
            "label": seed["title"],
            "entity_type": seed["graph"]["entity_data"]["entity_type"],
            "entity_assertion_id": str(seed["assertion"]["id"]),
            "entity_data": json.dumps(seed["graph"]["entity_data"]),
            "actor": SEED_ACTOR,
        },
    )

    conn.execute(
        sa.text(
            """
            INSERT INTO graph.external_links (
                id, entity_id, status, external_authority, external_identifier,
                link_type, confidence, link_data, created_by, updated_by
            ) VALUES (
                :id, :entity_id, 'approved', :external_authority, :external_identifier,
                :link_type, :confidence, CAST(:link_data AS jsonb), :actor, :actor
            )
            ON CONFLICT (id) DO NOTHING
            """
        ),
        {
            "id": str(seed["graph"]["external_link_id"]),
            "entity_id": str(seed["graph"]["entity_id"]),
            "external_authority": seed["graph"]["external_link_data"]["external_authority"],
            "external_identifier": seed["graph"]["external_link_data"]["external_identifier"],
            "link_type": seed["graph"]["external_link_data"]["link_type"],
            "confidence": seed["graph"]["external_link_data"]["evidence"]["confidence"],
            "link_data": json.dumps(seed["graph"]["external_link_data"]),
            "actor": SEED_ACTOR,
        },
    )

    conn.execute(
        sa.text(
            """
            INSERT INTO quality.reviews (
                id, entity_uri, preservation_ark, graph_entity_id, status,
                review_domain, severity, finding, recommended_action,
                composite_score, disposition, reviewed_at, review_data,
                created_by, updated_by
            ) VALUES (
                :id, :entity_uri, :preservation_ark, :graph_entity_id, 'approved',
                :review_domain, :severity, :finding, :recommended_action,
                :composite_score, :disposition, :reviewed_at,
                CAST(:review_data AS jsonb), :actor, :actor
            )
            ON CONFLICT (entity_uri) DO NOTHING
            """
        ),
        {
            "id": str(seed["quality"]["id"]),
            "entity_uri": ENTITY_URI,
            "preservation_ark": seed["ark"],
            "graph_entity_id": str(seed["graph"]["entity_id"]),
            "review_domain": seed["quality"]["review_data"]["review_domain"],
            "severity": seed["quality"]["review_data"]["severity"],
            "finding": seed["quality"]["review_data"]["finding"],
            "recommended_action": seed["quality"]["review_data"]["recommended_action"],
            "composite_score": seed["quality"]["review_data"]["composite_score"],
            "disposition": seed["quality"]["review_data"]["disposition"],
            "reviewed_at": now,
            "review_data": json.dumps(seed["quality"]["review_data"]),
            "actor": SEED_ACTOR,
        },
    )

    area = seed["protected_area"]
    conn.execute(
        sa.text(
            """
            INSERT INTO conservation.protected_areas (
                id, stable_id, status, pref_label, designation_type,
                graph_entity_id, discovery_record_id,
                boundary, centroid,
                conservation_metadata, external_identifiers, area_data,
                provenance_event_id, created_by, updated_by
            ) VALUES (
                :id, :stable_id, 'approved', :pref_label, :designation_type,
                :graph_entity_id, :discovery_record_id,
                ST_Multi(ST_SetSRID(ST_GeomFromGeoJSON(:boundary), 4326)),
                ST_SetSRID(ST_MakePoint(:centroid_lon, :centroid_lat), 4326),
                CAST(:conservation_metadata AS jsonb),
                CAST(:external_identifiers AS jsonb),
                CAST(:area_data AS jsonb),
                :provenance_event_id, :actor, :actor
            )
            ON CONFLICT (stable_id) DO NOTHING
            """
        ),
        {
            "id": str(area["id"]),
            "stable_id": seed["stable_id"],
            "pref_label": seed["title"],
            "designation_type": area["area_data"]["designation_type"],
            "graph_entity_id": str(seed["graph"]["entity_id"]),
            "discovery_record_id": str(seed["discovery"]["id"]),
            "boundary": boundary_json,
            "centroid_lon": centroid["coordinates"][0],
            "centroid_lat": centroid["coordinates"][1],
            "conservation_metadata": json.dumps(area["area_data"]["conservation_metadata"]),
            "external_identifiers": json.dumps(area["area_data"]["external_identifiers"]),
            "area_data": json.dumps(area["area_data"]),
            "provenance_event_id": str(seed["discovery"]["provenance_event_id"]),
            "actor": SEED_ACTOR,
        },
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        sa.text("DELETE FROM conservation.protected_areas WHERE stable_id = 'everglades-national-park'")
    )
    conn.execute(sa.text("DELETE FROM quality.reviews WHERE entity_uri = :uri"), {"uri": ENTITY_URI})
    conn.execute(
        sa.text(
            """
            DELETE FROM graph.external_links
            WHERE entity_id IN (
                SELECT id FROM graph.entities WHERE stable_id = 'everglades-national-park'
            )
            """
        )
    )
    conn.execute(sa.text("DELETE FROM graph.entities WHERE stable_id = 'everglades-national-park'"))
    conn.execute(
        sa.text("DELETE FROM modeling.entity_assertions WHERE entity_uri = :uri"),
        {"uri": ENTITY_URI},
    )
    conn.execute(
        sa.text("DELETE FROM modeling.metadata_records WHERE stable_id = 'everglades-national-park'")
    )
    conn.execute(
        sa.text(
            """
            DELETE FROM preservation.premis_events
            WHERE preservation_object_id IN (
                SELECT id FROM preservation.objects WHERE stable_id = 'everglades-national-park'
            )
            """
        )
    )
    conn.execute(
        sa.text("DELETE FROM preservation.objects WHERE stable_id = 'everglades-national-park'")
    )
    conn.execute(
        sa.text("DELETE FROM discovery.records WHERE stable_id = 'everglades-national-park'")
    )
