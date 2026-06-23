"""Nature & Culture agent role registration across Open Grace registries."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import yaml
from pydantic import BaseModel, Field

from open_grace_governance.lifecycle import LifecycleStage
from open_grace_governance.schemas import AuditRegistryRecord
from open_grace_governance.store.base import JsonRegistryStore
from open_grace_governance.validation import ValidationResult

if TYPE_CHECKING:
    from open_grace_governance.system import GovernanceSystem

_PACKAGE_DATA = Path(__file__).resolve().parent / "data"

_KNOWLEDGE_LINK_GETTERS = {
    "entity": "entities",
    "place": "places",
    "species": "species",
    "heritage": "heritage",
    "collection": "collections",
    "media": "media",
    "knowledge_graph": "knowledge_graphs",
}


class NatureCultureAuditHook(BaseModel):
    hook_id: str
    display_name: str
    requirement: str


class NatureCultureAgentRecord(BaseModel):
    role_id: str
    display_name: str
    agent_id: str
    capability_class_id: str
    knowledge_links: dict[str, list[str]] = Field(default_factory=dict)
    benchmark_ids: list[str] = Field(default_factory=list)
    audit_requirements: list[str] = Field(default_factory=list)
    audit_hook_ids: list[str] = Field(default_factory=list)


def nature_culture_seed_path() -> Path:
    return _PACKAGE_DATA / "seed" / "nature_culture_agents.yaml"


def load_nature_culture_seed(path: Path | None = None) -> list[dict[str, Any]]:
    seed_path = path or nature_culture_seed_path()
    data = yaml.safe_load(seed_path.read_text(encoding="utf-8"))
    return data.get("agents", [])


def _parse_seed_row(row: dict[str, Any]) -> NatureCultureAgentRecord:
    audit_hooks = row.get("audit_hooks", [])
    return NatureCultureAgentRecord(
        role_id=row["role_id"],
        display_name=row["display_name"],
        agent_id=row["agent_id"],
        capability_class_id=row["capability_class_id"],
        knowledge_links=row.get("knowledge_links", {}),
        benchmark_ids=row.get("benchmark_ids", []),
        audit_requirements=row.get("audit_requirements", []),
        audit_hook_ids=[hook["hook_id"] for hook in audit_hooks],
    )


class NatureCultureAgentRegistry:
    """Registry of Nature & Culture role bindings to canonical WISE agents."""

    def __init__(self, store_path: Path | None = None) -> None:
        default = _PACKAGE_DATA / "nature_culture_agents.json"
        self._store = JsonRegistryStore(
            store_path or default,
            NatureCultureAgentRecord,
            "role_id",
        )

    def list(self) -> list[NatureCultureAgentRecord]:
        return self._store.all()

    def get(self, role_id: str) -> NatureCultureAgentRecord | None:
        return self._store.get(role_id)

    def get_by_agent(self, agent_id: str) -> NatureCultureAgentRecord | None:
        for record in self._store.all():
            if record.agent_id == agent_id:
                return record
        return None

    def register_from_seed(
        self,
        system: GovernanceSystem,
        *,
        seed_path: Path | None = None,
        steward_actor: str = "open-grace-nature-culture-seed",
    ) -> int:
        """Register all Nature & Culture agents and their audit hooks."""
        seed_file = seed_path or nature_culture_seed_path()
        data = yaml.safe_load(seed_file.read_text(encoding="utf-8"))
        steward = data.get("steward_actor", steward_actor)
        count = 0

        for row in data.get("agents", []):
            record = _parse_seed_row(row)
            if system.agents.get(record.agent_id) is None:
                raise ValueError(
                    f"canonical agent not registered: {record.agent_id} "
                    f"(run seed_all before register_nature_culture_agents)"
                )

            for hook in row.get("audit_hooks", []):
                audit_entry = AuditRegistryRecord(
                    audit_id=hook["hook_id"],
                    display_name=hook["display_name"],
                    subject_type="agent",
                    subject_id=record.agent_id,
                    evidence_ref=f"nature-culture/{record.role_id}/{hook['requirement']}",
                    outcome="pass",
                    reviewer_id=steward,
                    lifecycle_stage=LifecycleStage.AUDIT,
                    steward_actor=steward,
                    reference_models=["iso-27001", "opentelemetry"],
                )
                system.audits.record(audit_entry)

            self._store.upsert(record)
            count += 1

        self._store.save()
        return count

    def validate_cross_registry(self, system: GovernanceSystem) -> ValidationResult:
        """Ensure all Nature & Culture bindings resolve across registries."""
        errors: list[str] = []
        warnings: list[str] = []

        records = self._store.all()
        if not records:
            errors.append("no Nature & Culture agents registered")
            return ValidationResult(valid=False, errors=errors)

        for record in records:
            prefix = f"{record.role_id} ({record.display_name})"

            if system.agents.get(record.agent_id) is None:
                errors.append(f"{prefix}: unknown agent_id {record.agent_id}")

            capability_class = system.capability_framework.get(record.capability_class_id)
            if capability_class is None:
                errors.append(
                    f"{prefix}: unknown capability_class_id {record.capability_class_id}"
                )
            else:
                bound_classes = system.capability_framework.bindings_for_agent(record.agent_id)
                if record.capability_class_id not in bound_classes:
                    errors.append(
                        f"{prefix}: capability class {record.capability_class_id} "
                        f"not bound to {record.agent_id}"
                    )
                missing_audit_reqs = set(record.audit_requirements) - set(
                    capability_class.audit_requirements
                )
                if missing_audit_reqs:
                    errors.append(
                        f"{prefix}: audit requirements not in capability class: "
                        f"{sorted(missing_audit_reqs)}"
                    )

            for registry_key, entry_ids in record.knowledge_links.items():
                getter_name = _KNOWLEDGE_LINK_GETTERS.get(registry_key)
                if getter_name is None:
                    errors.append(f"{prefix}: unknown knowledge link key {registry_key}")
                    continue
                registry = getattr(system.knowledge, getter_name)
                for entry_id in entry_ids:
                    if registry.get(entry_id) is None:
                        errors.append(f"{prefix}: unknown {registry_key} ref {entry_id}")

            for benchmark_id in record.benchmark_ids:
                benchmark = system.benchmarks.get(benchmark_id)
                if benchmark is None:
                    errors.append(f"{prefix}: unknown benchmark_id {benchmark_id}")
                elif capability_class is not None and benchmark_id not in capability_class.benchmark_set:
                    errors.append(
                        f"{prefix}: benchmark {benchmark_id} not in capability class "
                        f"{record.capability_class_id} benchmark_set"
                    )

            for hook_id in record.audit_hook_ids:
                if system.audits.get(hook_id) is None:
                    errors.append(f"{prefix}: audit hook not registered: {hook_id}")

        return ValidationResult(valid=not errors, errors=errors, warnings=warnings)


def register_nature_culture_agents(
    system: GovernanceSystem,
    *,
    seed_path: Path | None = None,
) -> int:
    """Convenience entry point for Nature & Culture agent registration."""
    return system.nature_culture.register_from_seed(system, seed_path=seed_path)
