"""Panthera leo Reference Capability 2 seed migration.

Revision ID: 004_seed_panthera_leo
Revises: 003_rc2_species_schemas
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

from wise_reference.seed.panthera_leo import (  # noqa: E402
    ENTITY_URI,
    RIGHTS_URI,
    SEED_ACTOR,
    SOURCE_REGISTRY_REF,
    build_panthera_leo_seed,
)

revision: str = "004_seed_panthera_leo"
down_revision: Union[str, None] = "003_rc2_species_schemas"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    seed = build_panthera_leo_seed()
    conn = op.get_bind()
    now = seed["now"]

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
            "title": seed["common_name"],
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
            INSERT INTO species.registry_entries (
                id, stable_id, status, species_uri, scientific_name,
                scientific_name_authorship, taxonomic_rank, gbif_taxon_key,
                gbif_usage_key, discovery_record_id, registry_data,
                provenance_event_id, created_by, updated_by
            ) VALUES (
                :id, :stable_id, 'approved', :species_uri, :scientific_name,
                :authorship, :rank, :taxon_key, :usage_key, :discovery_record_id,
                CAST(:registry_data AS jsonb), :provenance_event_id, :actor, :actor
            )
            ON CONFLICT (stable_id) DO NOTHING
            """
        ),
        {
            "id": str(seed["species_registry"]["id"]),
            "stable_id": seed["stable_id"],
            "species_uri": seed["entity_uri"],
            "scientific_name": seed["scientific_name"],
            "authorship": seed["species_registry"]["registry_data"]["scientific_name_authorship"],
            "rank": seed["species_registry"]["registry_data"]["taxonomic_rank"],
            "taxon_key": seed["species_registry"]["registry_data"]["gbif_taxon_key"],
            "usage_key": seed["species_registry"]["registry_data"]["gbif_usage_key"],
            "discovery_record_id": str(seed["discovery"]["id"]),
            "registry_data": json.dumps(seed["species_registry"]["registry_data"]),
            "provenance_event_id": str(seed["species_registry"]["provenance_event_id"]),
            "actor": SEED_ACTOR,
        },
    )

    backbone_id_by_key: dict[str, str] = {}
    for node in seed["backbone_nodes"]:
        conn.execute(
            sa.text(
                """
                INSERT INTO taxonomy.backbone_nodes (
                    id, gbif_usage_key, scientific_name, taxonomic_rank,
                    parent_usage_key, status, kingdom, phylum, taxonomic_class,
                    taxonomic_order, family, genus, node_data, created_by, updated_by
                ) VALUES (
                    :id, :usage_key, :scientific_name, :rank, :parent_key,
                    'approved', :kingdom, :phylum, :taxonomic_class, :taxonomic_order,
                    :family, :genus, CAST(:node_data AS jsonb), :actor, :actor
                )
                ON CONFLICT (gbif_usage_key) DO NOTHING
                """
            ),
            {
                "id": str(node["id"]),
                "usage_key": node["gbif_usage_key"],
                "scientific_name": node["scientific_name"],
                "rank": node["taxonomic_rank"],
                "parent_key": node.get("parent_usage_key"),
                "kingdom": node.get("kingdom"),
                "phylum": node.get("phylum"),
                "taxonomic_class": node.get("class"),
                "taxonomic_order": node.get("order"),
                "family": node.get("family"),
                "genus": node.get("genus"),
                "node_data": json.dumps(node["node_data"]),
                "actor": SEED_ACTOR,
            },
        )
        backbone_id_by_key[node["gbif_usage_key"]] = str(node["id"])

    for node in seed["backbone_nodes"]:
        conn.execute(
            sa.text(
                """
                INSERT INTO taxonomy.species_backbone_links (
                    species_registry_id, backbone_node_id, link_type, link_data,
                    created_by, updated_by
                ) VALUES (
                    :species_id, :backbone_id, 'exactMatch',
                    CAST(:link_data AS jsonb), :actor, :actor
                )
                ON CONFLICT (species_registry_id, backbone_node_id) DO NOTHING
                """
            ),
            {
                "species_id": str(seed["species_registry"]["id"]),
                "backbone_id": backbone_id_by_key[node["gbif_usage_key"]],
                "link_data": json.dumps(
                    {
                        "gbif_usage_key": node["gbif_usage_key"],
                        "scientific_name": node["scientific_name"],
                        "taxonomic_rank": node["taxonomic_rank"],
                    }
                ),
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
                "agent_version": event_data["agent_version"],
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
            "title": seed["scientific_name"],
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
            "pref_label": seed["scientific_name"],
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
            "label": seed["scientific_name"],
            "entity_type": seed["graph"]["entity_data"]["entity_type"],
            "entity_assertion_id": str(seed["assertion"]["id"]),
            "entity_data": json.dumps(seed["graph"]["entity_data"]),
            "actor": SEED_ACTOR,
        },
    )

    for link_id, link_data in seed["graph"]["external_links"]:
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
                "id": str(link_id),
                "entity_id": str(seed["graph"]["entity_id"]),
                "external_authority": link_data["external_authority"],
                "external_identifier": link_data["external_identifier"],
                "link_type": link_data["link_type"],
                "confidence": link_data["evidence"]["confidence"],
                "link_data": json.dumps(link_data),
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


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM quality.reviews WHERE entity_uri = :uri"), {"uri": ENTITY_URI})
    conn.execute(
        sa.text(
            "DELETE FROM graph.external_links WHERE entity_id IN "
            "(SELECT id FROM graph.entities WHERE stable_id = 'panthera-leo')"
        )
    )
    conn.execute(sa.text("DELETE FROM graph.entities WHERE stable_id = 'panthera-leo'"))
    conn.execute(sa.text("DELETE FROM modeling.entity_assertions WHERE entity_uri = :uri"), {"uri": ENTITY_URI})
    conn.execute(sa.text("DELETE FROM modeling.metadata_records WHERE stable_id = 'panthera-leo'"))
    conn.execute(
        sa.text(
            "DELETE FROM preservation.premis_events WHERE preservation_object_id IN "
            "(SELECT id FROM preservation.objects WHERE stable_id = 'panthera-leo')"
        )
    )
    conn.execute(sa.text("DELETE FROM preservation.objects WHERE stable_id = 'panthera-leo'"))
    conn.execute(
        sa.text(
            "DELETE FROM taxonomy.species_backbone_links WHERE species_registry_id IN "
            "(SELECT id FROM species.registry_entries WHERE stable_id = 'panthera-leo')"
        )
    )
    conn.execute(
        sa.text(
            "DELETE FROM taxonomy.backbone_nodes WHERE gbif_usage_key IN "
            "('1','44','359','732','9703','5215027','5219404')"
        )
    )
    conn.execute(sa.text("DELETE FROM species.registry_entries WHERE stable_id = 'panthera-leo'"))
    conn.execute(sa.text("DELETE FROM discovery.records WHERE stable_id = 'panthera-leo'"))
