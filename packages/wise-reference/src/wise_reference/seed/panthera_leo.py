"""Panthera leo Reference Capability 2 seed data builder.

Target species: Panthera leo (Lion)
- GBIF taxonKey: 5219404
- Wikidata: Q140
- Encyclopedia of Life: 328450
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

STABLE_ID = "panthera-leo"
ARK = "ark:/99999/gbif/5219404/"
ENTITY_URI = "https://wise.example.org/species/panthera-leo"
SPECIES_URI = ENTITY_URI
RIGHTS_URI = "https://creativecommons.org/publicdomain/zero/1.0/"
SOURCE_REGISTRY_REF = "gbif"
SEED_ACTOR = "wise-reference-seed"
AGENT_VERSION = "wise-reference/0.2.0"

DATA_ROOT = Path(__file__).resolve().parents[5] / "data" / "reference"

BACKBONE_CHAIN = [
    {"gbif_usage_key": "1", "scientific_name": "Animalia", "taxonomic_rank": "kingdom", "parent_usage_key": None},
    {"gbif_usage_key": "44", "scientific_name": "Chordata", "taxonomic_rank": "phylum", "parent_usage_key": "1"},
    {"gbif_usage_key": "359", "scientific_name": "Mammalia", "taxonomic_rank": "class", "parent_usage_key": "44"},
    {"gbif_usage_key": "732", "scientific_name": "Carnivora", "taxonomic_rank": "order", "parent_usage_key": "359"},
    {"gbif_usage_key": "9703", "scientific_name": "Felidae", "taxonomic_rank": "family", "parent_usage_key": "732"},
    {"gbif_usage_key": "5215027", "scientific_name": "Panthera", "taxonomic_rank": "genus", "parent_usage_key": "9703"},
    {
        "gbif_usage_key": "5219404",
        "scientific_name": "Panthera leo",
        "taxonomic_rank": "species",
        "parent_usage_key": "5215027",
        "kingdom": "Animalia",
        "phylum": "Chordata",
        "class": "Mammalia",
        "order": "Carnivora",
        "family": "Felidae",
        "genus": "Panthera",
    },
]


def _load_json(relative: str) -> dict:
    return json.loads((DATA_ROOT / relative).read_text(encoding="utf-8"))


def _fixity_digest(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def build_panthera_leo_seed() -> dict:
    gbif = _load_json("gbif/panthera-leo-5219404.json")
    wikidata = _load_json("wikidata/Q140-panthera-leo.json")
    eol = _load_json("eol/328450-panthera-leo.json")
    now = datetime(2026, 6, 22, 14, 0, 0, tzinfo=UTC)

    discovery_id = uuid4()
    provenance_discovery = uuid4()
    discovery_event_id = "discovery-panthera-leo-20260622"
    ingest_event_id = "ingest-panthera-leo-20260622"
    modeling_event_id = "modeling-panthera-leo-20260622"
    graph_event_id = "graph-panthera-leo-20260622"
    quality_event_id = "quality-panthera-leo-20260622"
    species_registry_id = uuid4()
    species_provenance = uuid4()

    metadata_content = json.dumps(gbif, sort_keys=True)
    fixity = _fixity_digest(metadata_content)

    darwin_core = {
        "scientific_name": gbif["scientific_name"],
        "scientific_name_authorship": gbif["scientific_name_authorship"],
        "taxon_rank": gbif["taxon_rank"],
        "kingdom": gbif["kingdom"],
        "phylum": gbif["phylum"],
        "class": gbif["class"],
        "order": gbif["order"],
        "family": gbif["family"],
        "genus": gbif["genus"],
        "specific_epithet": gbif["specific_epithet"],
        "taxonomic_status": gbif["taxonomic_status"],
        "nomenclatural_code": "ICZN",
    }

    discovery_record_data = {
        "@context": "https://wise.example.org/context/discovery/v1",
        "@type": "wise:DiscoveryRecord",
        "id": str(discovery_id),
        "stable_id": STABLE_ID,
        "status": "approved",
        "title": gbif["common_name"],
        "description": f"GBIF backbone species {gbif['scientific_name']} ({gbif['scientific_name_authorship']})",
        "source_registry_ref": SOURCE_REGISTRY_REF,
        "rights_uri": RIGHTS_URI,
        "ingestion_candidacy_score": 0.96,
        "external_identifiers": {
            "gbif_taxon_key": gbif["gbif_taxon_key"],
            "gbif_usage_key": gbif["gbif_usage_key"],
            "wikidata": wikidata["wikidata_id"],
            "eol": eol["eol_page_id"],
        },
        "evidence": {
            "evidence_uris": [gbif["source_uri"], wikidata["source_uri"], eol["source_uri"]],
            "confidence": 0.99,
            "evidence_summary": "GBIF taxon 5219404 cross-validated with Wikidata Q140 and EOL 328450",
            "method": "gbif-backbone-harvest-v1",
            "source_registry_refs": [SOURCE_REGISTRY_REF, "wikidata", "eol"],
            "provenance_event_id": str(provenance_discovery),
        },
        "provenance": {
            "event_id": discovery_event_id,
            "event_type": "harvest",
            "agent_version": AGENT_VERSION,
            "event_timestamp": now.isoformat(),
            "actor_id": SEED_ACTOR,
        },
        "discovered_at": now.isoformat(),
    }

    species_registry_data = {
        "id": str(species_registry_id),
        "stable_id": STABLE_ID,
        "status": "approved",
        "species_uri": SPECIES_URI,
        "scientific_name": gbif["scientific_name"],
        "scientific_name_authorship": gbif["scientific_name_authorship"],
        "taxonomic_rank": gbif["taxon_rank"],
        "gbif_taxon_key": gbif["gbif_taxon_key"],
        "gbif_usage_key": gbif["gbif_usage_key"],
        "darwin_core": darwin_core,
        "external_identifiers": discovery_record_data["external_identifiers"],
        "evidence": discovery_record_data["evidence"],
        "provenance": {
            "event_id": f"species-registry-{STABLE_ID}",
            "event_type": "register",
            "agent_version": AGENT_VERSION,
            "event_timestamp": now.isoformat(),
            "actor_id": SEED_ACTOR,
        },
        "source_registry_ref": SOURCE_REGISTRY_REF,
    }

    backbone_nodes = []
    for node in BACKBONE_CHAIN:
        node_id = uuid4()
        backbone_nodes.append(
            {
                "id": node_id,
                "gbif_usage_key": node["gbif_usage_key"],
                "scientific_name": node["scientific_name"],
                "taxonomic_rank": node["taxonomic_rank"],
                "parent_usage_key": node.get("parent_usage_key"),
                "kingdom": node.get("kingdom"),
                "phylum": node.get("phylum"),
                "class": node.get("class"),
                "order": node.get("order"),
                "family": node.get("family"),
                "genus": node.get("genus"),
                "node_data": {
                    "gbif_usage_key": node["gbif_usage_key"],
                    "scientific_name": node["scientific_name"],
                    "taxonomic_rank": node["taxonomic_rank"],
                    "parent_usage_key": node.get("parent_usage_key"),
                    "source": "GBIF Taxonomic Backbone",
                },
            }
        )

    preservation_id = uuid4()
    object_descriptor = {
        "ark": ARK,
        "stable_id": STABLE_ID,
        "status": "approved",
        "format_uri": "http://www.nationalarchives.gov.uk/pronom/fmt/141",
        "format_label": "Plain Text File",
        "fixity": {
            "algorithm": "sha256",
            "digest": fixity,
            "verified_at": now.isoformat(),
            "result": "pass",
        },
        "storage_tier": "T0",
        "replica_count": 1,
        "minio_key": "ark:/99999/gbif/5219404/dwc-taxonomy.json",
        "rights_uri": RIGHTS_URI,
        "provenance": {
            "event_id": ingest_event_id,
            "event_type": "ingest",
            "agent_version": AGENT_VERSION,
            "event_timestamp": now.isoformat(),
            "actor_id": SEED_ACTOR,
        },
        "discovery_record_id": str(discovery_id),
        "ingest_event_id": ingest_event_id,
    }

    premis_deposit_id = uuid4()
    premis_fixity_id = uuid4()
    premis_events = [
        (
            premis_deposit_id,
            {
                "id": str(premis_deposit_id),
                "event_type": "ingestion",
                "event_timestamp": now.isoformat(),
                "agent_version": AGENT_VERSION,
                "actor_id": SEED_ACTOR,
                "preservation_object_ark": ARK,
                "event_detail": "Darwin Core taxonomy package deposited to T0 storage",
                "evidence_uris": [gbif["source_uri"]],
                "outcome": "success",
            },
        ),
        (
            premis_fixity_id,
            {
                "id": str(premis_fixity_id),
                "event_type": "fixity",
                "event_timestamp": now.isoformat(),
                "agent_version": AGENT_VERSION,
                "actor_id": SEED_ACTOR,
                "preservation_object_ark": ARK,
                "event_detail": "Initial SHA-256 fixity verification passed",
                "evidence_uris": [f"minio://wise-preservation/{object_descriptor['minio_key']}"],
                "outcome": "success",
            },
        ),
    ]

    metadata_id = uuid4()
    metadata_record_data = {
        "id": str(metadata_id),
        "stable_id": STABLE_ID,
        "status": "approved",
        "source_schema": "darwin-core",
        "source_schema_version": "2023-09",
        "preserved_object_ark": ARK,
        "title": gbif["scientific_name"],
        "description": f"Darwin Core normalized taxon record for {gbif['scientific_name']}",
        "language": "en",
        "rights_uri": RIGHTS_URI,
        "field_mappings": {
            "dwc:scientificName": "dwc:scientificName",
            "dwc:scientificNameAuthorship": "dwc:scientificNameAuthorship",
            "dwc:taxonRank": "dwc:taxonRank",
            "dwc:kingdom": "dwc:kingdom",
            "dwc:family": "dwc:family",
            "dwc:genus": "dwc:genus",
        },
        "original_literals": {
            "scientificName": gbif["scientific_name"],
            "vernacularName": gbif["common_name"],
        },
        "darwin_core": darwin_core,
        "provenance": {
            "event_id": modeling_event_id,
            "event_type": "normalization",
            "agent_version": AGENT_VERSION,
            "event_timestamp": now.isoformat(),
            "actor_id": SEED_ACTOR,
        },
    }

    assertion_id = uuid4()
    assertion_data = {
        "id": str(assertion_id),
        "status": "approved",
        "entity_uri": ENTITY_URI,
        "entity_type": "dwc:Taxon",
        "pref_label": gbif["scientific_name"],
        "alt_labels": [gbif["common_name"]],
        "descriptive_overlay": {
            "dwc:scientificName": gbif["scientific_name"],
            "dwc:scientificNameAuthorship": gbif["scientific_name_authorship"],
            "dwc:taxonRank": gbif["taxon_rank"],
            "dwc:kingdom": gbif["kingdom"],
            "dwc:family": gbif["family"],
            "dwc:genus": gbif["genus"],
            "dwc:vernacularName": gbif["common_name"],
        },
        "authority_links": [
            {
                "registry": "gbif",
                "identifier": gbif["gbif_taxon_key"],
                "link_type": "exactMatch",
                "confidence": 1.0,
                "method": "primary-source",
            },
            {
                "registry": "wikidata",
                "identifier": wikidata["wikidata_id"],
                "link_type": "exactMatch",
                "confidence": 0.99,
                "method": "identifier-crosswalk",
            },
            {
                "registry": "eol",
                "identifier": eol["eol_page_id"],
                "link_type": "exactMatch",
                "confidence": 0.98,
                "method": "identifier-crosswalk",
            },
        ],
        "rights_uri": RIGHTS_URI,
        "evidence": {
            "evidence_uris": [gbif["source_uri"], wikidata["source_uri"], eol["source_uri"]],
            "confidence": 0.99,
            "evidence_summary": "Darwin Core Taxon mapped from GBIF backbone with Wikidata and EOL authority links",
            "method": "darwin-core-biodiversity-v1",
            "source_registry_refs": [SOURCE_REGISTRY_REF, "wikidata", "eol"],
            "provenance_event_id": modeling_event_id,
        },
        "provenance": {
            "event_id": modeling_event_id,
            "event_type": "modeling",
            "agent_version": AGENT_VERSION,
            "event_timestamp": now.isoformat(),
            "actor_id": SEED_ACTOR,
        },
        "metadata_record_id": str(metadata_id),
        "rdf_triples": [
            {"subject": ENTITY_URI, "predicate": "rdf:type", "object": "dwc:Taxon"},
            {"subject": ENTITY_URI, "predicate": "dwc:scientificName", "object": gbif["scientific_name"]},
            {"subject": ENTITY_URI, "predicate": "dwc:taxonID", "object": gbif["gbif_taxon_key"]},
        ],
    }

    graph_entity_id = uuid4()
    wikidata_link_id = uuid4()
    eol_link_id = uuid4()
    external_links = [
        (
            wikidata_link_id,
            {
                "id": str(wikidata_link_id),
                "status": "approved",
                "external_authority": "wikidata",
                "external_identifier": wikidata["wikidata_id"],
                "link_type": "sameAs",
                "evidence": {
                    "evidence_uris": [wikidata["source_uri"]],
                    "confidence": 0.99,
                    "evidence_summary": "Wikidata Q140 exact match for Panthera leo",
                    "method": "authority-reconciliation-v1",
                    "source_registry_refs": ["wikidata"],
                    "provenance_event_id": graph_event_id,
                },
            },
        ),
        (
            eol_link_id,
            {
                "id": str(eol_link_id),
                "status": "approved",
                "external_authority": "eol",
                "external_identifier": eol["eol_page_id"],
                "link_type": "sameAs",
                "evidence": {
                    "evidence_uris": [eol["source_uri"]],
                    "confidence": 0.98,
                    "evidence_summary": "EOL page 328450 exact match for Panthera leo",
                    "method": "authority-reconciliation-v1",
                    "source_registry_refs": ["eol"],
                    "provenance_event_id": graph_event_id,
                },
            },
        ),
    ]

    graph_entity_data = {
        "id": str(graph_entity_id),
        "entity_uri": ENTITY_URI,
        "stable_id": STABLE_ID,
        "status": "approved",
        "label": gbif["scientific_name"],
        "entity_type": "dwc:Taxon",
        "entity_assertion_id": str(assertion_id),
        "external_links": [link[1] for link in external_links],
        "relationships": [
            {
                "subject": ENTITY_URI,
                "predicate": "dwc:family",
                "object": "Felidae",
            },
            {
                "subject": ENTITY_URI,
                "predicate": "dwc:genus",
                "object": "Panthera",
            },
        ],
    }

    quality_id = uuid4()
    quality_review_data = {
        "id": str(quality_id),
        "status": "approved",
        "entity_uri": ENTITY_URI,
        "preservation_ark": ARK,
        "review_domain": "composite",
        "severity": "info",
        "finding": "Darwin Core metadata, GBIF identifiers, rights, and accessibility meet RC2 thresholds.",
        "recommended_action": "Approve for public species demonstration page.",
        "composite_score": 0.97,
        "dimension_scores": [
            {"dimension": "metadata", "score": 0.96, "threshold": 0.80, "passed": True},
            {"dimension": "rights", "score": 1.0, "threshold": 0.90, "passed": True},
            {"dimension": "accessibility", "score": 0.95, "threshold": 0.90, "passed": True},
            {"dimension": "completeness", "score": 0.94, "threshold": 0.85, "passed": True},
        ],
        "disposition": "accepted",
        "provenance": {
            "event_id": quality_event_id,
            "event_type": "quality_review",
            "agent_version": AGENT_VERSION,
            "event_timestamp": now.isoformat(),
            "actor_id": SEED_ACTOR,
        },
        "reviewed_at": now.isoformat(),
    }

    return {
        "stable_id": STABLE_ID,
        "scientific_name": gbif["scientific_name"],
        "common_name": gbif["common_name"],
        "ark": ARK,
        "entity_uri": ENTITY_URI,
        "now": now,
        "discovery": {
            "id": discovery_id,
            "provenance_event_id": provenance_discovery,
            "discovery_event_id": discovery_event_id,
            "record_data": discovery_record_data,
            "external_identifiers": discovery_record_data["external_identifiers"],
            "ingestion_candidacy_score": discovery_record_data["ingestion_candidacy_score"],
        },
        "species_registry": {
            "id": species_registry_id,
            "provenance_event_id": species_provenance,
            "registry_data": species_registry_data,
        },
        "backbone_nodes": backbone_nodes,
        "preservation": {
            "id": preservation_id,
            "fixity_digest": fixity,
            "object_descriptor": object_descriptor,
            "ingest_event_id": ingest_event_id,
            "premis_events": premis_events,
        },
        "metadata": {
            "id": metadata_id,
            "modeling_event_id": modeling_event_id,
            "record_data": metadata_record_data,
        },
        "assertion": {
            "id": assertion_id,
            "assertion_data": assertion_data,
        },
        "graph": {
            "entity_id": graph_entity_id,
            "entity_data": graph_entity_data,
            "external_links": external_links,
        },
        "quality": {
            "id": quality_id,
            "review_data": quality_review_data,
        },
        "provenance_chain": [
            discovery_event_id,
            f"species-registry-{STABLE_ID}",
            ingest_event_id,
            str(premis_fixity_id),
            modeling_event_id,
            graph_event_id,
            quality_event_id,
        ],
    }
