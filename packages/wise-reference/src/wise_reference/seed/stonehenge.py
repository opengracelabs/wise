"""Stonehenge Reference Capability 1 seed data builder."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID, uuid4

STABLE_ID = "stonehenge"
ARK = "ark:/99999/373/stonehenge/"
ENTITY_URI = "https://wise.example.org/entity/stonehenge"
RIGHTS_URI = "http://rightsstatements.org/vocab/NoC-OKLR/1.0/"
SOURCE_REGISTRY_REF = "unesco"
SEED_ACTOR = "wise-reference-seed"
AGENT_VERSION = "wise-reference/0.1.0"

DATA_ROOT = Path(__file__).resolve().parents[5] / "data" / "reference"


def _load_json(relative: str) -> dict:
    return json.loads((DATA_ROOT / relative).read_text(encoding="utf-8"))


def _fixity_digest(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def build_stonehenge_seed() -> dict:
    """Build deterministic seed payloads for the Stonehenge RC1 pipeline."""
    unesco = _load_json("unesco/stonehenge-373.json")
    wikidata = _load_json("wikidata/Q39671-stonehenge.json")
    now = datetime(2026, 6, 22, 12, 0, 0, tzinfo=UTC)

    discovery_id = uuid4()
    provenance_discovery = uuid4()
    discovery_event_id = "discovery-stonehenge-20260622"

    ingest_event_id = "ingest-stonehenge-20260622"
    modeling_event_id = "modeling-stonehenge-20260622"
    graph_event_id = "graph-stonehenge-20260622"
    quality_event_id = "quality-stonehenge-20260622"

    metadata_content = json.dumps(unesco, sort_keys=True)
    fixity = _fixity_digest(metadata_content)

    discovery_record_data = {
        "@context": "https://wise.example.org/context/discovery/v1",
        "@type": "wise:DiscoveryRecord",
        "id": str(discovery_id),
        "stable_id": STABLE_ID,
        "status": "approved",
        "title": unesco["short_title"],
        "description": unesco["description"],
        "source_registry_ref": SOURCE_REGISTRY_REF,
        "rights_uri": RIGHTS_URI,
        "ingestion_candidacy_score": 0.94,
        "external_identifiers": {
            "unesco_whc": unesco["unesco_whc_id"],
            "wikidata": wikidata["wikidata_id"],
        },
        "evidence": {
            "evidence_uris": [unesco["source_uri"], wikidata["source_uri"]],
            "confidence": 0.97,
            "evidence_summary": "UNESCO World Heritage List entry 373 cross-validated with Wikidata Q39671",
            "method": "unesco-whc-harvest-v1",
            "source_registry_refs": [SOURCE_REGISTRY_REF, "wikidata"],
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

    preservation_id = uuid4()
    premis_deposit_id = uuid4()
    premis_fixity_id = uuid4()

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
        "minio_key": f"ark:/99999/373/stonehenge/metadata.json",
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

    premis_deposit = {
        "id": str(premis_deposit_id),
        "event_type": "ingestion",
        "event_timestamp": now.isoformat(),
        "agent_version": AGENT_VERSION,
        "actor_id": SEED_ACTOR,
        "preservation_object_ark": ARK,
        "event_detail": "BagIt ingest package deposited to T0 storage",
        "evidence_uris": [unesco["source_uri"]],
        "outcome": "success",
    }

    premis_fixity = {
        "id": str(premis_fixity_id),
        "event_type": "fixity",
        "event_timestamp": now.isoformat(),
        "agent_version": AGENT_VERSION,
        "actor_id": SEED_ACTOR,
        "preservation_object_ark": ARK,
        "event_detail": "Initial SHA-256 fixity verification passed",
        "evidence_uris": [f"minio://wise-preservation/{object_descriptor['minio_key']}"],
        "outcome": "success",
    }

    metadata_id = uuid4()
    metadata_record_data = {
        "id": str(metadata_id),
        "stable_id": STABLE_ID,
        "status": "approved",
        "source_schema": "unesco-whc-site",
        "source_schema_version": "2026.1",
        "preserved_object_ark": ARK,
        "title": unesco["short_title"],
        "description": unesco["description"],
        "language": "en",
        "rights_uri": RIGHTS_URI,
        "field_mappings": {
            "site.name": "dcterms:title",
            "site.description": "dcterms:description",
            "site.date_inscribed": "dcterms:created",
            "site.coordinates": "crm:P53_has_former_or_current_location",
        },
        "original_literals": {
            "title": unesco["title"],
            "description": unesco["description"],
        },
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
        "entity_type": "crm:E27_Site",
        "pref_label": unesco["short_title"],
        "alt_labels": [unesco["title"]],
        "descriptive_overlay": {
            "dcterms:title": unesco["short_title"],
            "dcterms:description": unesco["description"],
            "dcterms:spatial": "Wiltshire, England",
        },
        "authority_links": [
            {
                "registry": "wikidata",
                "identifier": wikidata["wikidata_id"],
                "link_type": "exactMatch",
                "confidence": 0.99,
                "method": "identifier-crosswalk",
            },
            {
                "registry": "unesco-whc",
                "identifier": unesco["unesco_whc_id"],
                "link_type": "exactMatch",
                "confidence": 1.0,
                "method": "primary-source",
            },
        ],
        "geographic_anchor": {
            "type": "Point",
            "coordinates": [unesco["coordinates"]["longitude"], unesco["coordinates"]["latitude"]],
        },
        "temporal_bounds": {"dcterms:created": unesco["date_inscribed"]},
        "rights_uri": RIGHTS_URI,
        "evidence": {
            "evidence_uris": [unesco["source_uri"], wikidata["source_uri"]],
            "confidence": 0.98,
            "evidence_summary": "CIDOC-CRM E27 Site mapped from UNESCO WHC site record",
            "method": "cidoc-crm-heritage-v1",
            "source_registry_refs": [SOURCE_REGISTRY_REF, "wikidata"],
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
            {"subject": ENTITY_URI, "predicate": "rdf:type", "object": "crm:E27_Site"},
            {"subject": ENTITY_URI, "predicate": "skos:prefLabel", "object": unesco["short_title"]},
            {"subject": ENTITY_URI, "predicate": "dcterms:identifier", "object": unesco["unesco_whc_id"]},
        ],
    }

    graph_entity_id = uuid4()
    external_link_id = uuid4()
    external_link_data = {
        "id": str(external_link_id),
        "status": "approved",
        "external_authority": "wikidata",
        "external_identifier": wikidata["wikidata_id"],
        "link_type": "sameAs",
        "evidence": {
            "evidence_uris": [wikidata["source_uri"]],
            "confidence": 0.99,
            "evidence_summary": "Wikidata Q39671 exact match for Stonehenge site entity",
            "method": "authority-reconciliation-v1",
            "source_registry_refs": ["wikidata"],
            "provenance_event_id": graph_event_id,
        },
    }

    graph_entity_data = {
        "id": str(graph_entity_id),
        "entity_uri": ENTITY_URI,
        "stable_id": STABLE_ID,
        "status": "approved",
        "label": unesco["short_title"],
        "entity_type": "crm:E27_Site",
        "entity_assertion_id": str(assertion_id),
        "external_links": [external_link_data],
        "relationships": [
            {
                "subject": ENTITY_URI,
                "predicate": "crm:P89_falls_within",
                "object": "https://wise.example.org/entity/united-kingdom",
            }
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
        "finding": "All required metadata, rights, and accessibility dimensions meet Reference Capability 1 thresholds.",
        "recommended_action": "Approve for public demonstration surface publication.",
        "composite_score": 0.96,
        "dimension_scores": [
            {"dimension": "metadata", "score": 0.95, "threshold": 0.80, "passed": True},
            {"dimension": "rights", "score": 1.0, "threshold": 0.90, "passed": True},
            {"dimension": "accessibility", "score": 0.94, "threshold": 0.90, "passed": True},
            {"dimension": "completeness", "score": 0.93, "threshold": 0.85, "passed": True},
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
        "title": unesco["short_title"],
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
        "preservation": {
            "id": preservation_id,
            "fixity_digest": fixity,
            "object_descriptor": object_descriptor,
            "ingest_event_id": ingest_event_id,
            "premis_events": [
                (premis_deposit_id, premis_deposit),
                (premis_fixity_id, premis_fixity),
            ],
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
            "external_link_id": external_link_id,
            "external_link_data": external_link_data,
        },
        "quality": {
            "id": quality_id,
            "review_data": quality_review_data,
        },
        "provenance_chain": [
            discovery_event_id,
            ingest_event_id,
            str(premis_fixity_id),
            modeling_event_id,
            graph_event_id,
            quality_event_id,
        ],
    }
