"""Provenance propagation helpers for RC1 orchestration."""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from wise_contracts.common import EvidenceOutputProfile, ProvenanceRef


def new_event_id(prefix: str, stable_id: str) -> str:
    """Generate a deterministic-style provenance event identifier."""
    return f"{prefix}-{stable_id}-{uuid4().hex[:8]}"


def build_provenance_ref(
    *,
    event_id: str,
    event_type: str,
    agent_version: str,
    actor_id: str = "wise-orchestration",
) -> dict[str, Any]:
    """Build a ProvenanceRef-compatible dict for graph state."""
    from datetime import UTC, datetime

    ref = ProvenanceRef(
        event_id=event_id,
        event_type=event_type,
        agent_version=agent_version,
        event_timestamp=datetime.now(UTC),
        actor_id=actor_id,
    )
    return ref.model_dump(mode="json")


def build_evidence_profile(
    *,
    evidence_uris: list[str],
    confidence: float,
    evidence_summary: str,
    method: str,
    source_registry_refs: list[str],
    provenance_event_id: str,
) -> dict[str, Any]:
    """Build an Evidence Output Profile dict (03-canonical-architecture §6.6)."""
    profile = EvidenceOutputProfile(
        evidence_uris=evidence_uris,
        confidence=confidence,
        evidence_summary=evidence_summary,
        method=method,
        source_registry_refs=source_registry_refs,
        provenance_event_id=provenance_event_id,
    )
    return profile.model_dump(mode="json")


def append_provenance_event(chain: list[str], event_id: str) -> list[str]:
    """Return a new chain with event_id appended if not already present."""
    if event_id in chain:
        return chain
    return [*chain, event_id]


def link_parent_provenance(
    child_event_id: str,
    parent_event_ids: list[str],
) -> dict[str, Any]:
    """Attach parent provenance links for chain continuity."""
    return {
        "event_id": child_event_id,
        "parent_event_ids": parent_event_ids,
    }


def propagate_from_seed(seed: dict[str, Any]) -> list[str]:
    """Extract the provenance chain from Stonehenge seed data."""
    return list(seed.get("provenance_chain", []))
