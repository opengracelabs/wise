"""Capability registry with agent linkage."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from open_grace_governance.lifecycle import LifecycleStage, advance_lifecycle
from open_grace_governance.schemas import CapabilityRegistryRecord
from open_grace_governance.store.base import JsonRegistryStore
from open_grace_governance.validation import validate_entry

from open_grace_agent_registry.manifest_paths import capabilities_manifest_path


@dataclass(frozen=True)
class CapabilityAgentBinding:
    capability_id: str
    agent_id: str
    role: str


class CapabilityRegistry:
    def __init__(self, store_path: Path | None = None) -> None:
        default = Path(__file__).resolve().parent / "data" / "capability_registry.json"
        self._store = JsonRegistryStore(
            store_path or default,
            CapabilityRegistryRecord,
            "capability_id",
        )
        self._bindings: list[CapabilityAgentBinding] = []

    def import_canonical_manifest(self, manifest_path: Path | None = None) -> int:
        path = manifest_path or capabilities_manifest_path()
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        count = 0
        for row in data["capabilities"]:
            record = CapabilityRegistryRecord(
                lifecycle_stage=LifecycleStage.PUBLICATION,
                steward_actor="wise-manifest-import",
                reference_models=["iso-42001"],
                **row,
            )
            result = validate_entry(record)
            if not result.valid:
                raise ValueError(
                    f"invalid capability manifest row {row['capability_id']}: {result.errors}"
                )
            self._store.upsert(record)
            count += 1
        for row in data.get("capability_agents", []):
            self._bindings.append(
                CapabilityAgentBinding(
                    capability_id=row["capability_id"],
                    agent_id=row["agent_id"],
                    role=row["role"],
                )
            )
        self._store.save()
        return count

    def list(self) -> list[CapabilityRegistryRecord]:
        return self._store.all()

    def bindings(self) -> list[CapabilityAgentBinding]:
        return list(self._bindings)

    def get(self, capability_id: str) -> CapabilityRegistryRecord | None:
        return self._store.get(capability_id)

    def register(self, record: CapabilityRegistryRecord) -> CapabilityRegistryRecord:
        result = validate_entry(record)
        if not result.valid:
            raise ValueError("; ".join(result.errors))
        self._store.upsert(record)
        self._store.save()
        return record

    def advance(
        self,
        capability_id: str,
        target: LifecycleStage,
        *,
        steward_actor: str | None = None,
    ) -> CapabilityRegistryRecord:
        record = self._store.get(capability_id)
        if record is None:
            raise KeyError(capability_id)
        record.lifecycle_stage = advance_lifecycle(record.lifecycle_stage, target)
        record.touch(steward_actor=steward_actor)
        self._store.upsert(record)
        self._store.save()
        return record
