"""Reference Capability 1 agent propose logic — shared by platform services and orchestration."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from wise_contracts.common import ApprovalStatus
from wise_contracts.discovery import DiscoveryRecord
from wise_contracts.graph import GraphEntity
from wise_contracts.metadata import EntityAssertion, MetadataRecord
from wise_contracts.preservation import PreservedObjectDescriptor
from wise_contracts.quality import QualityReviewRecord
from wise_registry.models.source import Source
from wise_reference.seed.stonehenge import build_stonehenge_seed

RC1_STABLE_IDS = frozenset({"stonehenge"})


def _require_stable_id(stable_id: str) -> dict[str, Any]:
    if stable_id not in RC1_STABLE_IDS:
        raise ValueError(f"Unsupported stable_id={stable_id!r}")
    return build_stonehenge_seed()


def resolve_source_registry_refs(session: Session | None, canonical_names: list[str]) -> list[str]:
    """Resolve Source Registry canonical names; system of record is registry.sources."""
    if session is None:
        return canonical_names
    resolved: list[str] = []
    for name in canonical_names:
        row = session.scalar(select(Source).where(Source.canonical_name == name))
        if row is None:
            raise KeyError(f"Source Registry missing canonical_name={name!r}")
        if not row.active:
            raise ValueError(f"Source Registry source inactive: {name!r}")
        resolved.append(row.canonical_name)
    return resolved


def propose_discovery_record(stable_id: str, session: Session | None = None) -> dict[str, Any]:
    seed = _require_stable_id(stable_id)
    record_data = dict(seed["discovery"]["record_data"])
    record_data["status"] = ApprovalStatus.PROPOSED.value
    refs = resolve_source_registry_refs(
        session,
        list(record_data.get("evidence", {}).get("source_registry_refs", [record_data["source_registry_ref"]])),
    )
    record_data["source_registry_ref"] = refs[0]
    evidence = dict(record_data["evidence"])
    evidence["source_registry_refs"] = refs
    record_data["evidence"] = evidence
    DiscoveryRecord.model_validate(record_data)
    return {
        "record": record_data,
        "discovery_event_id": seed["discovery"]["discovery_event_id"],
        "source_registry_refs": refs,
        "provenance_event_id": evidence["provenance_event_id"],
    }


def propose_preservation(
    stable_id: str,
    *,
    discovery_record_id: str,
    session: Session | None = None,
) -> dict[str, Any]:
    seed = _require_stable_id(stable_id)
    _ = session
    object_descriptor = dict(seed["preservation"]["object_descriptor"])
    object_descriptor["status"] = ApprovalStatus.PROPOSED.value
    object_descriptor["discovery_record_id"] = discovery_record_id
    PreservedObjectDescriptor.model_validate(object_descriptor)
    premis_events = [event for _, event in seed["preservation"]["premis_events"]]
    ingest_event_id = seed["preservation"]["ingest_event_id"]
    return {
        "object_descriptor": object_descriptor,
        "premis_events": premis_events,
        "ingest_event_id": ingest_event_id,
        "provenance_event_id": ingest_event_id,
    }


def propose_metadata(
    stable_id: str,
    *,
    preserved_object_ark: str,
    session: Session | None = None,
) -> dict[str, Any]:
    seed = _require_stable_id(stable_id)
    _ = session
    metadata_data = dict(seed["metadata"]["record_data"])
    metadata_data["status"] = ApprovalStatus.PROPOSED.value
    MetadataRecord.model_validate(metadata_data)

    assertion_data = dict(seed["assertion"]["assertion_data"])
    assertion_data["status"] = ApprovalStatus.PROPOSED.value
    assertion_data["metadata_record_id"] = metadata_data["id"]
    assertion_data["preservation_ark"] = preserved_object_ark
    EntityAssertion.model_validate(assertion_data)

    modeling_event_id = seed["metadata"]["modeling_event_id"]
    return {
        "metadata_record": metadata_data,
        "entity_assertion": assertion_data,
        "modeling_event_id": modeling_event_id,
        "provenance_event_id": assertion_data["evidence"]["provenance_event_id"],
        "evidence": assertion_data["evidence"],
    }


def propose_graph_entity(
    stable_id: str,
    *,
    entity_assertion_id: str,
    session: Session | None = None,
) -> dict[str, Any]:
    seed = _require_stable_id(stable_id)
    _ = session
    graph_data = dict(seed["graph"]["entity_data"])
    graph_data["status"] = ApprovalStatus.PROPOSED.value
    graph_data["entity_assertion_id"] = entity_assertion_id
    for link in graph_data.get("external_links", []):
        link["status"] = ApprovalStatus.PROPOSED.value
    GraphEntity.model_validate(graph_data)
    graph_event_id = seed["provenance_chain"][4]
    return {
        "graph_entity": graph_data,
        "graph_event_id": graph_event_id,
        "provenance_event_id": graph_event_id,
        "evidence": (graph_data.get("external_links") or [{}])[0].get("evidence"),
    }


def propose_quality_review(
    stable_id: str,
    *,
    graph_entity_uri: str,
    session: Session | None = None,
) -> dict[str, Any]:
    seed = _require_stable_id(stable_id)
    _ = session
    review_data = dict(seed["quality"]["review_data"])
    review_data["status"] = ApprovalStatus.PROPOSED.value
    review_data["disposition"] = None
    review_data["entity_uri"] = graph_entity_uri
    QualityReviewRecord.model_validate(review_data)
    quality_event_id = seed["provenance_chain"][-1]
    return {
        "quality_review": review_data,
        "quality_event_id": quality_event_id,
        "provenance_event_id": quality_event_id,
    }
