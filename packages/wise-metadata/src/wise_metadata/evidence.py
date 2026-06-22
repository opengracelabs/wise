"""Evidence Output Profile builder (03-canonical-architecture.md §6.6)."""

from __future__ import annotations

from uuid import UUID

from wise_metadata.schemas.evidence import EvidenceProfile


def build_evidence_profile(
    *,
    evidence_uris: list[str],
    confidence: float,
    evidence_summary: str,
    method: str,
    source_registry_refs: list[str],
    provenance_event_id: UUID | None = None,
) -> EvidenceProfile:
    """Construct a validated Evidence Output Profile for assertion-making outputs."""
    return EvidenceProfile(
        evidence_uris=evidence_uris,
        confidence=confidence,
        evidence_summary=evidence_summary,
        method=method,
        source_registry_refs=source_registry_refs,
        provenance_event_id=provenance_event_id,
    )


def evidence_profile_to_json(profile: EvidenceProfile) -> dict:
    """Serialize evidence profile for JSONB storage."""
    return profile.model_dump(mode="json")
