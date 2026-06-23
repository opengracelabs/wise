"""Capability Framework registry and agent bindings."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from open_grace_governance.lifecycle import LifecycleStage
from open_grace_governance.schemas.capability_framework import CapabilityFrameworkRecord
from open_grace_governance.store.base import JsonRegistryStore
from open_grace_governance.validation import validate_entry

_PACKAGE_DATA = Path(__file__).resolve().parents[1] / "data"


@dataclass(frozen=True)
class AgentCapabilityBinding:
    agent_id: str
    capability_class_id: str


class CapabilityFrameworkRegistry:
    def __init__(self, store_path: Path | None = None) -> None:
        self._store = JsonRegistryStore(
            store_path or _PACKAGE_DATA / "capability_framework.json",
            CapabilityFrameworkRecord,
            "id",
        )
        self._bindings: list[AgentCapabilityBinding] = []

    def seed_from_yaml(self, path: Path | None = None) -> int:
        seed_path = path or _PACKAGE_DATA / "seed" / "capability_framework.yaml"
        if not seed_path.is_file():
            return 0
        data = yaml.safe_load(seed_path.read_text(encoding="utf-8"))
        count = 0
        for row in data.get("capability_classes", []):
            record = CapabilityFrameworkRecord.model_validate(row)
            result = validate_entry(record)
            if not result.valid:
                raise ValueError(f"invalid capability class seed {row}: {result.errors}")
            self._store.upsert(record)
            count += 1
        self._bindings = [
            AgentCapabilityBinding(
                agent_id=row["agent_id"],
                capability_class_id=row["capability_class_id"],
            )
            for row in data.get("agent_bindings", [])
        ]
        self._store.save()
        return count

    def list(self) -> list[CapabilityFrameworkRecord]:
        return self._store.all()

    def get(self, capability_class_id: str) -> CapabilityFrameworkRecord | None:
        return self._store.get(capability_class_id)

    def bindings(self) -> list[AgentCapabilityBinding]:
        return list(self._bindings)

    def bindings_for_agent(self, agent_id: str) -> list[str]:
        return [
            binding.capability_class_id
            for binding in self._bindings
            if binding.agent_id == agent_id
        ]

    def agents_for_capability(self, capability_class_id: str) -> list[str]:
        return [
            binding.agent_id
            for binding in self._bindings
            if binding.capability_class_id == capability_class_id
        ]

    def register(self, record: CapabilityFrameworkRecord) -> CapabilityFrameworkRecord:
        result = validate_entry(record)
        if not result.valid:
            raise ValueError("; ".join(result.errors))
        self._store.upsert(record)
        self._store.save()
        return record

    def is_published(self, capability_class_id: str) -> bool:
        record = self.get(capability_class_id)
        return record is not None and record.lifecycle_stage == LifecycleStage.PUBLICATION
