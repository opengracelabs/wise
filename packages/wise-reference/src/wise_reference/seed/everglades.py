"""Everglades National Park Reference Capability 3 seed data builder."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

STABLE_ID = "everglades-national-park"
ARK = "ark:/99999/374/everglades-national-park/"
ENTITY_URI = "https://wise.example.org/entity/everglades-national-park"
RIGHTS_URI = "http://rightsstatements.org/vocab/NoC-OKLR/1.0/"
SOURCE_REGISTRY_REF = "ramsar"
SEED_ACTOR = "wise-reference-seed"
AGENT_VERSION = "wise-reference/0.1.0"

# Deterministic UUIDs for reproducible migrations and tests
DISCOVERY_ID = UUID("a1000001-0003-4000-8000-000000000001")
PROVENANCE_DISCOVERY = UUID("a1000001-0003-4000-8000-000000000002")
PRESERVATION_ID = UUID("a1000001-0003-4000-8000-000000000003")
PREMIS_DEPOSIT_ID = UUID("a1000001-0003-4000-8000-000000000004")
PREMIS_FIXITY_ID = UUID("a1000001-0003-4000-8000-000000000005")
METADATA_ID = UUID("a1000001-0003-4000-8000-000000000006")
ASSERTION_ID = UUID("a1000001-0003-4000-8000-000000000007")
GRAPH_ENTITY_ID = UUID("a1000001-0003-4000-8000-000000000008")
EXTERNAL_LINK_ID = UUID("a1000001-0003-4000-8000-000000000009")
QUALITY_ID = UUID("a1000001-0003-4000-8000-00000000000a")
PROTECTED_AREA_ID = UUID("a1000001-0003-4000-8000-00000000000b")

DATA_ROOT = Path(__file__).resolve().parents[5] / "data" / "reference"


def _load_json(relative: str) -> dict:
    return json.loads((DATA_ROOT / relative).read_text(encoding="utf-8"))


def _fixity_digest(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def build_everglades_seed() -> dict:
    """Build deterministic seed payloads for the Everglades RC3 pipeline."""
    ramsar = _load_json("ramsar/everglades-374.json")
    wikidata = _load_json("wikidata/Q212174-everglades.json")
    unesco = _load_json("unesco/everglades-76.json")
    boundary = _load_json("geospatial/everglades-boundary.json")
    now = datetime(2026, 6, 22, 14, 0, 0, tzinfo=UTC)

    discovery_event_id = "discovery-everglades-20260622"
    ingest_event_id = "ingest-everglades-20260622"
    modeling_event_id = "modeling-everglades-20260622"
    graph_event_id = "graph-everglades-20260622"
    quality_event_id = "quality-everglades-20260622"

    metadata_content = json.dumps(ramsar, sort_keys=True)
    fixity = _fixity_digest(metadata_content)

    discovery_record_data = {
        "@context": "https://wise.example.org/context/discovery/v1",
        "@type": "wise:DiscoveryRecord",
        "id": str(DISCOVERY_ID),
        "stable_id": STABLE_ID,
        "status": "approved",
        "title": ramsar["short_title"],
        "description": ramsar["description"],
        "source_registry_ref": SOURCE_REGISTRY_REF,
        "rights_uri": RIGHTS_URI,
        "ingestion_candidacy_score": 0.96,
        "external_identifiers": {
            "ramsar": ramsar["ramsar_site_id"],
            "wikidata": wikidata["wikidata_id"],
            "unesco_whc": unesco["unesco_whc_id"],
            "geonames": wikidata["geonames_id"],
        },
        "evidence": {
            "evidence_uris": [ramsar["source_uri"], wikidata["source_uri"], unesco["source_uri"]],
            "confidence": 0.98,
            "evidence_summary": (
                "Ramsar Site 374 cross-validated with Wikidata Q212174, "
                "UNESCO WHC 76, and GeoNames 4157029"
            ),
            "method": "ramsar-harvest-v1",
            "source_registry_refs": [SOURCE_REGISTRY_REF, "wikidata", "unesco-whc", "geonames"],
            "provenance_event_id": str(PROVENANCE_DISCOVERY),
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
        "minio_key": "ark:/99999/374/everglades-national-park/metadata.json",
        "rights_uri": RIGHTS_URI,
        "provenance": {
            "event_id": ingest_event_id,
            "event_type": "ingest",
            "agent_version": AGENT_VERSION,
            "event_timestamp": now.isoformat(),
            "actor_id": SEED_ACTOR,
        },
        "discovery_record_id": str(DISCOVERY_ID),
        "ingest_event_id": ingest_event_id,
    }

    premis_deposit = {
        "id": str(PREMIS_DEPOSIT_ID),
        "event_type": "ingestion",
        "event_timestamp": now.isoformat(),
        "agent_version": AGENT_VERSION,
        "actor_id": SEED_ACTOR,
        "preservation_object_ark": ARK,
        "event_detail": "BagIt ingest package deposited to T0 storage",
        "evidence_uris": [ramsar["source_uri"]],
        "outcome": "success",
    }

    premis_fixity = {
        "id": str(PREMIS_FIXITY_ID),
        "event_type": "fixity",
        "event_timestamp": now.isoformat(),
        "agent_version": AGENT_VERSION,
        "actor_id": SEED_ACTOR,
        "preservation_object_ark": ARK,
        "event_detail": "Initial SHA-256 fixity verification passed",
        "evidence_uris": [f"minio://wise-preservation/{object_descriptor['minio_key']}"],
        "outcome": "success",
    }

    metadata_record_data = {
        "id": str(METADATA_ID),
        "stable_id": STABLE_ID,
        "status": "approved",
        "source_schema": "ramsar-site",
        "source_schema_version": "2026.1",
        "preserved_object_ark": ARK,
        "title": ramsar["short_title"],
        "description": ramsar["description"],
        "language": "en",
        "rights_uri": RIGHTS_URI,
        "field_mappings": {
            "site.official_name": "dcterms:title",
            "site.description": "dcterms:description",
            "site.designation_date": "dcterms:created",
            "site.boundary": "geo:hasGeometry",
            "site.iucn_category": "wise:iucnCategory",
            "site.ramsar_criteria": "wise:ramsarCriteria",
        },
        "original_literals": {
            "title": ramsar["official_name"],
            "description": ramsar["description"],
        },
        "provenance": {
            "event_id": modeling_event_id,
            "event_type": "normalization",
            "agent_version": AGENT_VERSION,
            "event_timestamp": now.isoformat(),
            "actor_id": SEED_ACTOR,
        },
    }

    conservation_metadata = {
        "iucn_category": ramsar["iucn_category"],
        "designation_type": ramsar["designation_type"],
        "ramsar_criteria": ramsar["ramsar_criteria"],
        "designation_date": ramsar["designation_date"],
        "area_hectares": ramsar["area_hectares"],
        "country": ramsar["country"],
        "unesco_whc_id": unesco["unesco_whc_id"],
        "management_authority": "National Park Service",
    }

    assertion_data = {
        "id": str(ASSERTION_ID),
        "status": "approved",
        "entity_uri": ENTITY_URI,
        "entity_type": "crm:E27_Site",
        "pref_label": ramsar["short_title"],
        "alt_labels": [ramsar["official_name"], unesco["title"]],
        "descriptive_overlay": {
            "dcterms:title": ramsar["short_title"],
            "dcterms:description": ramsar["description"],
            "dcterms:spatial": "Florida, United States",
            "wise:protectedAreaType": "national_park",
            "wise:iucnCategory": ramsar["iucn_category"],
        },
        "conservation_metadata": conservation_metadata,
        "authority_links": [
            {
                "registry": "ramsar",
                "identifier": ramsar["ramsar_site_id"],
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
                "registry": "unesco-whc",
                "identifier": unesco["unesco_whc_id"],
                "link_type": "exactMatch",
                "confidence": 1.0,
                "method": "authority-crosswalk",
            },
            {
                "registry": "geonames",
                "identifier": wikidata["geonames_id"],
                "link_type": "exactMatch",
                "confidence": 0.97,
                "method": "geonames-reconciliation-v1",
            },
        ],
        "geographic_anchor": boundary,
        "temporal_bounds": {
            "dcterms:created": ramsar["designation_date"],
            "wise:unescoInscribed": unesco["date_inscribed"],
        },
        "rights_uri": RIGHTS_URI,
        "evidence": {
            "evidence_uris": [ramsar["source_uri"], wikidata["source_uri"]],
            "confidence": 0.98,
            "evidence_summary": "CIDOC-CRM E27 Site with conservation metadata from Ramsar registry",
            "method": "cidoc-crm-conservation-v1",
            "source_registry_refs": [SOURCE_REGISTRY_REF, "wikidata", "geonames"],
            "provenance_event_id": modeling_event_id,
        },
        "provenance": {
            "event_id": modeling_event_id,
            "event_type": "modeling",
            "agent_version": AGENT_VERSION,
            "event_timestamp": now.isoformat(),
            "actor_id": SEED_ACTOR,
        },
        "metadata_record_id": str(METADATA_ID),
        "rdf_triples": [
            {"subject": ENTITY_URI, "predicate": "rdf:type", "object": "crm:E27_Site"},
            {"subject": ENTITY_URI, "predicate": "skos:prefLabel", "object": ramsar["short_title"]},
            {"subject": ENTITY_URI, "predicate": "geo:hasGeometry", "object": "geo:everglades-boundary"},
            {"subject": ENTITY_URI, "predicate": "wise:iucnCategory", "object": ramsar["iucn_category"]},
        ],
    }

    external_link_data = {
        "id": str(EXTERNAL_LINK_ID),
        "status": "approved",
        "external_authority": "wikidata",
        "external_identifier": wikidata["wikidata_id"],
        "link_type": "sameAs",
        "evidence": {
            "evidence_uris": [wikidata["source_uri"]],
            "confidence": 0.99,
            "evidence_summary": "Wikidata Q212174 exact match for Everglades National Park",
            "method": "authority-reconciliation-v1",
            "source_registry_refs": ["wikidata"],
            "provenance_event_id": graph_event_id,
        },
    }

    graph_entity_data = {
        "id": str(GRAPH_ENTITY_ID),
        "entity_uri": ENTITY_URI,
        "stable_id": STABLE_ID,
        "status": "approved",
        "label": ramsar["short_title"],
        "entity_type": "crm:E27_Site",
        "entity_assertion_id": str(ASSERTION_ID),
        "external_links": [external_link_data],
        "relationships": [
            {
                "subject": ENTITY_URI,
                "predicate": "crm:P89_falls_within",
                "object": "https://wise.example.org/entity/united-states",
            },
            {
                "subject": ENTITY_URI,
                "predicate": "crm:P89_falls_within",
                "object": "https://wise.example.org/entity/florida",
            },
        ],
    }

    quality_review_data = {
        "id": str(QUALITY_ID),
        "status": "approved",
        "entity_uri": ENTITY_URI,
        "preservation_ark": ARK,
        "review_domain": "composite",
        "severity": "info",
        "finding": (
            "Protected area metadata, geospatial boundary, conservation designations, "
            "and accessibility dimensions meet Reference Capability 3 thresholds."
        ),
        "recommended_action": "Approve for map service and public demonstration surface publication.",
        "composite_score": 0.95,
        "dimension_scores": [
            {"dimension": "metadata", "score": 0.94, "threshold": 0.80, "passed": True},
            {"dimension": "rights", "score": 1.0, "threshold": 0.90, "passed": True},
            {"dimension": "accessibility", "score": 0.93, "threshold": 0.90, "passed": True},
            {"dimension": "completeness", "score": 0.94, "threshold": 0.85, "passed": True},
            {"dimension": "geospatial", "score": 0.96, "threshold": 0.85, "passed": True},
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

    protected_area_data = {
        "id": str(PROTECTED_AREA_ID),
        "stable_id": STABLE_ID,
        "status": "approved",
        "pref_label": ramsar["short_title"],
        "designation_type": "national_park",
        "conservation_metadata": conservation_metadata,
        "external_identifiers": discovery_record_data["external_identifiers"],
        "boundary_geojson": boundary,
        "centroid": {
            "type": "Point",
            "coordinates": [
                ramsar["coordinates"]["longitude"],
                ramsar["coordinates"]["latitude"],
            ],
        },
        "evidence": assertion_data["evidence"],
        "provenance": {
            "event_id": modeling_event_id,
            "event_type": "geospatial_modeling",
            "agent_version": AGENT_VERSION,
            "event_timestamp": now.isoformat(),
            "actor_id": SEED_ACTOR,
        },
    }

    return {
        "stable_id": STABLE_ID,
        "title": ramsar["short_title"],
        "ark": ARK,
        "entity_uri": ENTITY_URI,
        "now": now,
        "boundary_geojson": boundary,
        "discovery": {
            "id": DISCOVERY_ID,
            "provenance_event_id": PROVENANCE_DISCOVERY,
            "discovery_event_id": discovery_event_id,
            "record_data": discovery_record_data,
            "external_identifiers": discovery_record_data["external_identifiers"],
            "ingestion_candidacy_score": discovery_record_data["ingestion_candidacy_score"],
        },
        "preservation": {
            "id": PRESERVATION_ID,
            "fixity_digest": fixity,
            "object_descriptor": object_descriptor,
            "ingest_event_id": ingest_event_id,
            "premis_events": [
                (PREMIS_DEPOSIT_ID, premis_deposit),
                (PREMIS_FIXITY_ID, premis_fixity),
            ],
        },
        "metadata": {
            "id": METADATA_ID,
            "modeling_event_id": modeling_event_id,
            "record_data": metadata_record_data,
        },
        "assertion": {
            "id": ASSERTION_ID,
            "assertion_data": assertion_data,
        },
        "graph": {
            "entity_id": GRAPH_ENTITY_ID,
            "entity_data": graph_entity_data,
            "external_link_id": EXTERNAL_LINK_ID,
            "external_link_data": external_link_data,
        },
        "quality": {
            "id": QUALITY_ID,
            "review_data": quality_review_data,
        },
        "protected_area": {
            "id": PROTECTED_AREA_ID,
            "area_data": protected_area_data,
        },
        "provenance_chain": [
            discovery_event_id,
            ingest_event_id,
            str(PREMIS_FIXITY_ID),
            modeling_event_id,
            graph_event_id,
            quality_event_id,
        ],
    }
