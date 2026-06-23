"""Cross-registry validation for knowledge records."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from open_grace_governance.lifecycle import LifecycleStage
from open_grace_governance.validation.rules import ValidationResult
from open_grace_knowledge.reference_models import KNOWLEDGE_REFERENCE_MODEL_BY_SLUG
from open_grace_knowledge.schemas import (
    CollectionRegistryRecord,
    EntityRegistryRecord,
    HeritageRegistryRecord,
    KnowledgeGraphRegistryRecord,
    MediaRegistryRecord,
    PlaceRegistryRecord,
    SpeciesRegistryRecord,
)

if TYPE_CHECKING:
    from open_grace_agent_registry import AgentRegistry, CapabilityRegistry
    from open_grace_audit import AuditRegistry
    from open_grace_benchmarking import BenchmarkRegistry
    from open_grace_knowledge.registries.system import KnowledgeSystem


def _require_publication_fields(record, errors: list[str]) -> None:
    stage = getattr(record, "lifecycle_stage", None)
    if stage != LifecycleStage.PUBLICATION:
        return
    steward = getattr(record, "steward_actor", None)
    if not steward:
        errors.append("steward_actor required at publication stage")


def validate_knowledge_reference_models(record, errors: list[str]) -> None:
    slugs = getattr(record, "reference_models", []) or []
    for slug in slugs:
        if slug not in KNOWLEDGE_REFERENCE_MODEL_BY_SLUG:
            errors.append(f"unknown knowledge reference model slug: {slug}")


def validate_entity_record(record: EntityRegistryRecord) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    validate_knowledge_reference_models(record, errors)
    _require_publication_fields(record, errors)

    if "wikidata" in record.reference_models and "wikidata" not in record.external_ids:
        warnings.append("wikidata reference model declared but no wikidata external_id")

    return ValidationResult(valid=not errors, errors=errors, warnings=warnings)


def validate_place_record(record: PlaceRegistryRecord) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    validate_knowledge_reference_models(record, errors)
    _require_publication_fields(record, errors)

    has_postgis = any(store.store.value == "postgis" for store in record.backing_stores)
    if record.geometry_ref and not has_postgis:
        warnings.append("geometry_ref set but no postgis backing store declared")

    return ValidationResult(valid=not errors, errors=errors, warnings=warnings)


def validate_species_record(record: SpeciesRegistryRecord) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    validate_knowledge_reference_models(record, errors)
    _require_publication_fields(record, errors)

    if "gbif" in record.reference_models and record.gbif_taxon_key is None:
        warnings.append("gbif reference model declared but gbif_taxon_key missing")

    return ValidationResult(valid=not errors, errors=errors, warnings=warnings)


def validate_heritage_record(record: HeritageRegistryRecord) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    validate_knowledge_reference_models(record, errors)
    _require_publication_fields(record, errors)

    if record.unesco_id and "wikidata" not in record.reference_models:
        warnings.append("unesco_id present; consider wikidata reference model")

    return ValidationResult(valid=not errors, errors=errors, warnings=warnings)


def validate_collection_record(record: CollectionRegistryRecord) -> ValidationResult:
    errors: list[str] = []
    validate_knowledge_reference_models(record, errors)
    _require_publication_fields(record, errors)
    return ValidationResult(valid=not errors, errors=errors)


def validate_media_record(record: MediaRegistryRecord) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    validate_knowledge_reference_models(record, errors)
    _require_publication_fields(record, errors)

    if record.internet_archive_identifier and "internet-archive" not in record.reference_models:
        warnings.append("internet_archive_identifier set without internet-archive reference model")

    return ValidationResult(valid=not errors, errors=errors, warnings=warnings)


def validate_knowledge_graph_record(record: KnowledgeGraphRegistryRecord) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    validate_knowledge_reference_models(record, errors)
    _require_publication_fields(record, errors)

    if not record.node_registry_refs:
        errors.append("node_registry_refs must not be empty")

    has_opensearch = any(store.store.value == "opensearch" for store in record.backing_stores)
    if record.opensearch_index and not has_opensearch:
        warnings.append("opensearch_index set but no opensearch backing store declared")

    return ValidationResult(valid=not errors, errors=errors, warnings=warnings)


_VALIDATORS = {
    EntityRegistryRecord: validate_entity_record,
    PlaceRegistryRecord: validate_place_record,
    SpeciesRegistryRecord: validate_species_record,
    HeritageRegistryRecord: validate_heritage_record,
    CollectionRegistryRecord: validate_collection_record,
    MediaRegistryRecord: validate_media_record,
    KnowledgeGraphRegistryRecord: validate_knowledge_graph_record,
}


def validate_knowledge_entry(record) -> ValidationResult:
    validator = _VALIDATORS.get(type(record))
    if validator is None:
        return ValidationResult(
            valid=False,
            errors=[f"no knowledge validator for {type(record).__name__}"],
        )
    return validator(record)


_REGISTRY_KEY_TO_GETTER = {
    "entity": "entities",
    "place": "places",
    "species": "species",
    "heritage": "heritage",
    "collection": "collections",
    "media": "media",
}


@dataclass
class KnowledgeValidationContext:
    knowledge: KnowledgeSystem
    agents: AgentRegistry | None = None
    capabilities: CapabilityRegistry | None = None
    audits: AuditRegistry | None = None
    benchmarks: BenchmarkRegistry | None = None


def _resolve_registry_ref(
    registry_key: str,
    entry_id: str,
    context: KnowledgeValidationContext,
    errors: list[str],
) -> None:
    getter_name = _REGISTRY_KEY_TO_GETTER.get(registry_key)
    if getter_name is None:
        errors.append(f"unknown registry key in node_registry_refs: {registry_key}")
        return
    registry = getattr(context.knowledge, getter_name)
    id_field = registry_key + "_id" if registry_key != "species" else "species_id"
    if registry_key == "entity":
        id_field = "entity_id"
    elif registry_key == "place":
        id_field = "place_id"
    elif registry_key == "heritage":
        id_field = "heritage_id"
    elif registry_key == "collection":
        id_field = "collection_id"
    elif registry_key == "media":
        id_field = "media_id"

    record = registry.get(entry_id)
    if record is None:
        errors.append(f"unknown {registry_key} ref: {entry_id}")


def validate_knowledge_cross_registry(
    record,
    context: KnowledgeValidationContext | None = None,
) -> ValidationResult:
    base = validate_knowledge_entry(record)
    if context is None:
        return base

    errors = list(base.errors)
    warnings = list(base.warnings)

    if isinstance(record, PlaceRegistryRecord) and record.parent_place_id:
        if context.knowledge.places.get(record.parent_place_id) is None:
            errors.append(f"unknown parent_place_id: {record.parent_place_id}")

    if isinstance(record, SpeciesRegistryRecord):
        if record.parent_species_id and context.knowledge.species.get(record.parent_species_id) is None:
            errors.append(f"unknown parent_species_id: {record.parent_species_id}")
        for place_id in record.place_ids:
            if context.knowledge.places.get(place_id) is None:
                errors.append(f"unknown place_id: {place_id}")

    if isinstance(record, HeritageRegistryRecord):
        if record.place_id and context.knowledge.places.get(record.place_id) is None:
            errors.append(f"unknown place_id: {record.place_id}")
        for collection_id in record.collection_ids:
            if context.knowledge.collections.get(collection_id) is None:
                errors.append(f"unknown collection_id: {collection_id}")
        for entity_id in record.entity_ids:
            if context.knowledge.entities.get(entity_id) is None:
                errors.append(f"unknown entity_id: {entity_id}")

    if isinstance(record, CollectionRegistryRecord):
        for entity_id in record.item_entity_ids:
            if context.knowledge.entities.get(entity_id) is None:
                errors.append(f"unknown item_entity_id: {entity_id}")
        for place_id in record.place_ids:
            if context.knowledge.places.get(place_id) is None:
                errors.append(f"unknown place_id: {place_id}")

    if isinstance(record, MediaRegistryRecord):
        if record.collection_id and context.knowledge.collections.get(record.collection_id) is None:
            errors.append(f"unknown collection_id: {record.collection_id}")
        for entity_id in record.entity_ids:
            if context.knowledge.entities.get(entity_id) is None:
                errors.append(f"unknown entity_id: {entity_id}")
        for place_id in record.place_ids:
            if context.knowledge.places.get(place_id) is None:
                errors.append(f"unknown place_id: {place_id}")

    if isinstance(record, KnowledgeGraphRegistryRecord):
        for registry_key, entry_ids in record.node_registry_refs.items():
            for entry_id in entry_ids:
                _resolve_registry_ref(registry_key, entry_id, context, errors)

    steward = getattr(record, "steward_agent_id", None)
    if steward and context.agents and context.agents.get(steward) is None:
        errors.append(f"unknown steward_agent_id: {steward}")

    capability = getattr(record, "capability_id", None)
    if capability and context.capabilities and context.capabilities.get(capability) is None:
        errors.append(f"unknown capability_id: {capability}")

    if isinstance(record, KnowledgeGraphRegistryRecord):
        if context.audits:
            for audit_id in record.audit_requirement_ids:
                if context.audits.get(audit_id) is None:
                    errors.append(f"unknown audit_requirement_id: {audit_id}")
        if context.benchmarks:
            for benchmark_id in record.benchmark_ids:
                if context.benchmarks.get(benchmark_id) is None:
                    errors.append(f"unknown benchmark_id: {benchmark_id}")

    return ValidationResult(valid=not errors, errors=errors, warnings=warnings)
