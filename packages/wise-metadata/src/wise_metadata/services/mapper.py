"""Schema mapping engine — applies crosswalk rules to normalized metadata."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4

from wise_metadata.enums import MappingTarget
from wise_metadata.evidence import build_evidence_profile, evidence_profile_to_json
from wise_metadata.models.schema_mapping import SchemaMapping
from wise_metadata.services.normalizer import _get_path


@dataclass
class AssertionDraft:
    """Draft entity assertion before persistence."""

    subject_uri: str
    predicate: str
    object_value: str
    object_type: str
    language: str | None
    entity_type: str
    mapping_target: MappingTarget
    rights_uri: str | None
    evidence: dict


def apply_schema_mappings(
    normalized_payload: dict,
    mappings: list[SchemaMapping],
    *,
    source_registry_ref: str,
    provenance_event_id: UUID | None,
    subject_uri: str | None = None,
    rights_uri: str | None = None,
) -> tuple[list[AssertionDraft], list[str]]:
    """Apply active crosswalk rules; return assertion drafts and unmapped field paths."""
    subject = subject_uri or f"https://wise.example/id/provisional/{uuid4()}"
    applied_paths: set[str] = set()
    drafts: list[AssertionDraft] = []

    sorted_mappings = sorted(
        [m for m in mappings if m.active],
        key=lambda m: m.priority,
    )

    for mapping in sorted_mappings:
        value = normalized_payload.get(mapping.target_term)
        if value is None:
            value = _get_path(normalized_payload, mapping.target_term)
        if value is None:
            continue

        applied_paths.add(mapping.source_field_path)
        evidence = build_evidence_profile(
            evidence_uris=[f"field://{mapping.source_field_path}"],
            confidence=1.0 if mapping.transform_rule == "direct" else 0.9,
            evidence_summary=(
                f"Mapped {mapping.source_field_path} → {mapping.target_term} "
                f"via {mapping.mapping_target.value}"
            ),
            method="rule-based",
            source_registry_refs=[source_registry_ref],
            provenance_event_id=provenance_event_id,
        )
        drafts.append(
            AssertionDraft(
                subject_uri=subject,
                predicate=mapping.target_term,
                object_value=str(value),
                object_type="literal",
                language=None,
                entity_type=mapping.crm_class or mapping.mapping_target.value,
                mapping_target=mapping.mapping_target,
                rights_uri=rights_uri,
                evidence=evidence_profile_to_json(evidence),
            )
        )

    all_source_paths = {m.source_field_path for m in sorted_mappings}
    unmapped = sorted(all_source_paths - applied_paths)
    return drafts, unmapped
