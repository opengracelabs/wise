"""Authority record proposal generation."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4

from wise_metadata.enums import AuthorityEntityType, AuthorityMatchMethod
from wise_metadata.evidence import build_evidence_profile, evidence_profile_to_json


@dataclass
class AuthorityDraft:
    entity_type: AuthorityEntityType
    provisional_uri: str
    pref_label: str
    alt_labels: list[str]
    external_scheme: str
    external_id: str
    link_type: str
    match_confidence: float
    match_method: AuthorityMatchMethod
    skos_payload: dict
    evidence: dict


def propose_place_authority(
    *,
    pref_label: str,
    external_scheme: str,
    external_id: str,
    source_registry_ref: str,
    provenance_event_id: UUID | None = None,
    match_method: AuthorityMatchMethod = AuthorityMatchMethod.EXACT,
    match_confidence: float = 1.0,
    alt_labels: list[str] | None = None,
) -> AuthorityDraft:
    """Propose place authority record with SKOS representation."""
    provisional_uri = f"https://wise.example/id/authority/{uuid4()}"
    skos = {
        "skos:prefLabel": pref_label,
        "skos:altLabel": alt_labels or [],
        "skos:exactMatch": f"{external_scheme}:{external_id}",
    }
    evidence = evidence_profile_to_json(
        build_evidence_profile(
            evidence_uris=[f"{external_scheme}:{external_id}"],
            confidence=match_confidence,
            evidence_summary=f"Authority proposal for place {pref_label}",
            method=match_method.value,
            source_registry_refs=[source_registry_ref],
            provenance_event_id=provenance_event_id,
        )
    )
    return AuthorityDraft(
        entity_type=AuthorityEntityType.PLACE,
        provisional_uri=provisional_uri,
        pref_label=pref_label,
        alt_labels=alt_labels or [],
        external_scheme=external_scheme,
        external_id=external_id,
        link_type="exactMatch",
        match_confidence=match_confidence,
        match_method=match_method,
        skos_payload=skos,
        evidence=evidence,
    )


def propose_from_normalized(
    normalized_payload: dict,
    *,
    source_canonical_name: str,
    source_registry_ref: str,
    provenance_event_id: UUID | None = None,
) -> list[AuthorityDraft]:
    """Generate authority proposals from normalized metadata fields."""
    proposals: list[AuthorityDraft] = []

    title = normalized_payload.get("dcterms:title")
    if not title:
        return proposals

    if source_canonical_name == "wikidata" and normalized_payload.get("wikidata:entity"):
        proposals.append(
            propose_place_authority(
                pref_label=str(title),
                external_scheme="wikidata",
                external_id=str(normalized_payload["wikidata:entity"]),
                source_registry_ref=source_registry_ref,
                provenance_event_id=provenance_event_id,
            )
        )
    elif source_canonical_name == "openstreetmap" and normalized_payload.get("osm:wikidata"):
        proposals.append(
            propose_place_authority(
                pref_label=str(title),
                external_scheme="wikidata",
                external_id=str(normalized_payload["osm:wikidata"]),
                source_registry_ref=source_registry_ref,
                provenance_event_id=provenance_event_id,
                match_method=AuthorityMatchMethod.FUZZY,
                match_confidence=0.9,
            )
        )
    elif source_canonical_name == "unesco" and normalized_payload.get("dcterms:identifier"):
        proposals.append(
            propose_place_authority(
                pref_label=str(title),
                external_scheme="unesco.whc",
                external_id=str(normalized_payload["dcterms:identifier"]),
                source_registry_ref=source_registry_ref,
                provenance_event_id=provenance_event_id,
            )
        )

    return proposals
