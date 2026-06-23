"""Knowledge compliance reports."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from open_grace_knowledge.validation import (
    KnowledgeValidationContext,
    validate_knowledge_cross_registry,
)

if TYPE_CHECKING:
    from open_grace_knowledge.registries.system import KnowledgeSystem
    from open_grace_knowledge.schemas import (
        CollectionRegistryRecord,
        EntityRegistryRecord,
        HeritageRegistryRecord,
        KnowledgeGraphRegistryRecord,
        MediaRegistryRecord,
        PlaceRegistryRecord,
        SpeciesRegistryRecord,
    )

KNOWLEDGE_REPORT_FILENAME = "knowledge_compliance_report.json"


@dataclass
class KnowledgeComplianceReport:
    entry_id: str
    registry: str
    display_name: str
    generated_at: str
    validation_passed: bool
    validation_errors: list[str] = field(default_factory=list)
    validation_warnings: list[str] = field(default_factory=list)
    backing_stores: list[str] = field(default_factory=list)
    reference_models: list[str] = field(default_factory=list)

    @property
    def compliant(self) -> bool:
        return self.validation_passed


def _registry_name(record) -> str:
    type_name = type(record).__name__
    return type_name.removesuffix("RegistryRecord").lower()


def _display_name(record) -> str:
    for attr in ("display_name", "scientific_name"):
        value = getattr(record, attr, None)
        if value:
            return value
    return getattr(record, "graph_id", "unknown")


def _entry_id(record) -> str:
    for attr in (
        "entity_id",
        "place_id",
        "species_id",
        "heritage_id",
        "collection_id",
        "media_id",
        "graph_id",
    ):
        value = getattr(record, attr, None)
        if value:
            return value
    return "unknown"


def generate_knowledge_report(
    record: (
        EntityRegistryRecord
        | PlaceRegistryRecord
        | SpeciesRegistryRecord
        | HeritageRegistryRecord
        | CollectionRegistryRecord
        | MediaRegistryRecord
        | KnowledgeGraphRegistryRecord
    ),
    *,
    context: KnowledgeValidationContext | None = None,
) -> KnowledgeComplianceReport:
    validation = validate_knowledge_cross_registry(record, context)
    backing = [store.store.value for store in getattr(record, "backing_stores", [])]
    return KnowledgeComplianceReport(
        entry_id=_entry_id(record),
        registry=_registry_name(record),
        display_name=_display_name(record),
        generated_at=datetime.now(UTC).isoformat(),
        validation_passed=validation.valid,
        validation_errors=validation.errors,
        validation_warnings=validation.warnings,
        backing_stores=backing,
        reference_models=list(getattr(record, "reference_models", [])),
    )


def generate_fleet_knowledge_reports(
    knowledge: KnowledgeSystem,
    *,
    context: KnowledgeValidationContext | None = None,
) -> list[KnowledgeComplianceReport]:
    reports: list[KnowledgeComplianceReport] = []
    for registry in (
        knowledge.entities,
        knowledge.places,
        knowledge.species,
        knowledge.heritage,
        knowledge.collections,
        knowledge.media,
        knowledge.knowledge_graphs,
    ):
        for record in registry.list():
            reports.append(generate_knowledge_report(record, context=context))
    return reports


def report_to_dict(report: KnowledgeComplianceReport) -> dict[str, Any]:
    payload = asdict(report)
    payload["compliant"] = report.compliant
    return payload


def write_knowledge_report(
    report: KnowledgeComplianceReport,
    output_dir: Path,
    *,
    filename: str = KNOWLEDGE_REPORT_FILENAME,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / filename
    path.write_text(json.dumps(report_to_dict(report), indent=2), encoding="utf-8")
    return path
