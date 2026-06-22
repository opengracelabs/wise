"""Metadata Agent v1 orchestration pipeline."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from wise_metadata.enums import (
    AssertionStatus,
    MappingRunStatus,
    ModelingEventType,
    SourceSchema,
)
from wise_metadata.evidence import evidence_profile_to_json
from wise_metadata.models import (
    AuthorityRecordProposal,
    EntityAssertionProposal,
    MappingRun,
    ModelingProvenanceEvent,
    NormalizedRecord,
    SchemaMapping,
    ValidationResult,
)
from wise_metadata.schemas.normalized_record import NormalizedRecordCreate
from wise_metadata.services.authority_proposer import propose_from_normalized
from wise_metadata.services.mapper import apply_schema_mappings
from wise_metadata.services.normalizer import AGENT_VERSION, normalize_metadata
from wise_metadata.services.rights_validator import validate_rights, validation_domain as rights_domain
from wise_metadata.services.source_validator import validate_source, validation_domain as source_domain
from wise_registry.models.license import License
from wise_registry.models.rights_status import RightsStatus
from wise_registry.models.source import Source


def _source_registry_ref(source: Source) -> str:
    return f"https://wise.example/registry/source/{source.id}"


def _record_modeling_event(
    session: Session,
    *,
    event_type: ModelingEventType,
    linked_entity_type: str,
    linked_entity_id: UUID,
    source_id: UUID,
    actor: str = AGENT_VERSION,
    evidence_uris: list[str] | None = None,
    notes: str | None = None,
    registry_provenance_event_id: UUID | None = None,
) -> ModelingProvenanceEvent:
    event = ModelingProvenanceEvent(
        event_type=event_type,
        linked_entity_type=linked_entity_type,
        linked_entity_id=linked_entity_id,
        source_id=source_id,
        registry_provenance_event_id=registry_provenance_event_id,
        actor=actor,
        agent_version=AGENT_VERSION,
        evidence_uris=evidence_uris or [],
        notes=notes,
        occurred_at=datetime.now(timezone.utc),
        created_by=AGENT_VERSION,
        updated_by=AGENT_VERSION,
    )
    session.add(event)
    session.flush()
    return event


def process_record(
    session: Session,
    *,
    source: Source,
    record: NormalizedRecordCreate,
    rights_uri: str | None = None,
    license: License | None = None,
    rights_status: RightsStatus | None = None,
) -> dict:
    """
    Execute Metadata Agent v1 pipeline for one source record.

    Returns summary dict with created entity IDs. Does not write to Knowledge Graph.
    """
    registry_ref = _source_registry_ref(source)

    source_outcome = validate_source(
        source,
        source_registry_ref=registry_ref,
    )
    normalized_payload, original_literals, language = normalize_metadata(
        record.source_schema,
        record.raw_payload,
    )

    normalized = NormalizedRecord(
        source_id=record.source_id,
        external_record_id=record.external_record_id,
        source_schema=record.source_schema,
        source_schema_version=record.source_schema_version,
        raw_payload=record.raw_payload,
        normalized_payload=normalized_payload,
        original_literals=original_literals,
        language=language or record.language,
        registry_provenance_event_id=record.registry_provenance_event_id,
        created_by=record.audit.created_by,
        updated_by=record.audit.updated_by,
    )
    session.add(normalized)
    session.flush()

    norm_event = _record_modeling_event(
        session,
        event_type=ModelingEventType.NORMALIZE,
        linked_entity_type="normalized_record",
        linked_entity_id=normalized.id,
        source_id=source.id,
        evidence_uris=[registry_ref],
        notes=f"Normalized {record.source_schema.value} record {record.external_record_id}",
        registry_provenance_event_id=record.registry_provenance_event_id,
    )
    normalized.normalization_event_id = norm_event.id

    session.add(
        ValidationResult(
            normalized_record_id=normalized.id,
            source_id=source.id,
            validation_domain=source_domain(),
            status=source_outcome.status,
            severity=source_outcome.severity,
            findings=source_outcome.findings,
            evidence=source_outcome.evidence,
            created_by=AGENT_VERSION,
            updated_by=AGENT_VERSION,
        )
    )

    rights_outcome = validate_rights(
        rights_uri=rights_uri,
        license=license or source.license,
        rights_status=rights_status,
        source_registry_ref=registry_ref,
        provenance_event_id=norm_event.id,
    )
    session.add(
        ValidationResult(
            normalized_record_id=normalized.id,
            source_id=source.id,
            validation_domain=rights_domain(),
            status=rights_outcome.status,
            severity=rights_outcome.severity,
            findings=rights_outcome.findings,
            license_id=rights_outcome.license_id,
            rights_status_id=rights_outcome.rights_status_id,
            evidence=rights_outcome.evidence,
            created_by=AGENT_VERSION,
            updated_by=AGENT_VERSION,
        )
    )

    mapping_run = MappingRun(
        normalized_record_id=normalized.id,
        source_id=source.id,
        agent_version=AGENT_VERSION,
        status=MappingRunStatus.RUNNING,
        created_by=AGENT_VERSION,
        updated_by=AGENT_VERSION,
    )
    session.add(mapping_run)
    session.flush()

    mappings = session.scalars(
        select(SchemaMapping)
        .where(SchemaMapping.source_canonical_name == source.canonical_name)
        .where(SchemaMapping.active.is_(True))
    ).all()

    assertion_drafts, unmapped = apply_schema_mappings(
        normalized_payload,
        list(mappings),
        source_registry_ref=registry_ref,
        provenance_event_id=norm_event.id,
        rights_uri=rights_uri,
    )

    for draft in assertion_drafts:
        session.add(
            EntityAssertionProposal(
                mapping_run_id=mapping_run.id,
                normalized_record_id=normalized.id,
                subject_uri=draft.subject_uri,
                predicate=draft.predicate,
                object_value=draft.object_value,
                object_type=draft.object_type,
                language=draft.language,
                entity_type=draft.entity_type,
                mapping_target=draft.mapping_target,
                status=AssertionStatus.PROPOSED,
                rights_uri=draft.rights_uri,
                evidence=draft.evidence,
                created_by=AGENT_VERSION,
                updated_by=AGENT_VERSION,
            )
        )

    mapping_run.mappings_applied = len(assertion_drafts)
    mapping_run.unmapped_fields = unmapped
    mapping_run.status = MappingRunStatus.COMPLETED
    mapping_run.completed_at = datetime.now(timezone.utc)

    map_event = _record_modeling_event(
        session,
        event_type=ModelingEventType.MAP,
        linked_entity_type="mapping_run",
        linked_entity_id=mapping_run.id,
        source_id=source.id,
        evidence_uris=[registry_ref],
        notes=f"Applied {len(assertion_drafts)} mappings",
        registry_provenance_event_id=record.registry_provenance_event_id,
    )

    for auth_draft in propose_from_normalized(
        normalized_payload,
        source_canonical_name=source.canonical_name,
        source_registry_ref=registry_ref,
        provenance_event_id=map_event.id,
    ):
        session.add(
            AuthorityRecordProposal(
                normalized_record_id=normalized.id,
                entity_type=auth_draft.entity_type,
                provisional_uri=auth_draft.provisional_uri,
                pref_label=auth_draft.pref_label,
                alt_labels=auth_draft.alt_labels,
                external_scheme=auth_draft.external_scheme,
                external_id=auth_draft.external_id,
                link_type=auth_draft.link_type,
                match_confidence=auth_draft.match_confidence,
                match_method=auth_draft.match_method,
                status=AssertionStatus.PROPOSED,
                skos_payload=auth_draft.skos_payload,
                evidence=auth_draft.evidence,
                created_by=AGENT_VERSION,
                updated_by=AGENT_VERSION,
            )
        )

    _record_modeling_event(
        session,
        event_type=ModelingEventType.AUTHORITY_PROPOSE,
        linked_entity_type="normalized_record",
        linked_entity_id=normalized.id,
        source_id=source.id,
        evidence_uris=[registry_ref],
        registry_provenance_event_id=record.registry_provenance_event_id,
    )

    session.flush()

    return {
        "normalized_record_id": str(normalized.id),
        "mapping_run_id": str(mapping_run.id),
        "assertion_proposals": len(assertion_drafts),
        "unmapped_fields": unmapped,
    }


def source_schema_for_canonical_name(canonical_name: str) -> SourceSchema:
    """Map registry source canonical_name to metadata source schema."""
    mapping = {
        "unesco": SourceSchema.UNESCO_WHC,
        "wikidata": SourceSchema.WIKIDATA,
        "wikimedia-commons": SourceSchema.WIKIMEDIA_COMMONS,
        "openstreetmap": SourceSchema.OPENSTREETMAP,
    }
    if canonical_name not in mapping:
        raise ValueError(f"No source schema mapping for {canonical_name}")
    return mapping[canonical_name]
