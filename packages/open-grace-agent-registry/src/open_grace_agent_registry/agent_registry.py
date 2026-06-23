"""Agent registry with lifecycle governance."""

from __future__ import annotations

from pathlib import Path

import yaml

from open_grace_governance.lifecycle import LifecycleStage, advance_lifecycle
from open_grace_governance.schemas import AgentRegistryRecord
from open_grace_governance.store.base import JsonRegistryStore
from open_grace_governance.validation import validate_entry

from open_grace_agent_registry.manifest_paths import agents_manifest_path


class AgentRegistry:
    def __init__(self, store_path: Path | None = None) -> None:
        default = Path(__file__).resolve().parent / "data" / "agent_registry.json"
        self._store = JsonRegistryStore(store_path or default, AgentRegistryRecord, "agent_id")

    def import_canonical_manifest(self, manifest_path: Path | None = None) -> int:
        """Load operational agents from existing WISE manifest (read-only import)."""
        path = manifest_path or agents_manifest_path()
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        count = 0
        for row in data["agents"]:
            record = AgentRegistryRecord(
                lifecycle_stage=LifecycleStage.PUBLICATION,
                steward_actor="wise-manifest-import",
                reference_models=["iso-42001", "nist-ai-rmf"],
                **row,
            )
            result = validate_entry(record)
            if not result.valid:
                raise ValueError(f"invalid agent manifest row {row['agent_id']}: {result.errors}")
            self._store.upsert(record)
            count += 1
        self._store.save()
        return count

    def list(self) -> list[AgentRegistryRecord]:
        return self._store.all()

    def get(self, agent_id: str) -> AgentRegistryRecord | None:
        return self._store.get(agent_id)

    def propose(self, record: AgentRegistryRecord) -> AgentRegistryRecord:
        record.lifecycle_stage = LifecycleStage.PROPOSAL
        result = validate_entry(record)
        if not result.valid:
            raise ValueError("; ".join(result.errors))
        self._store.upsert(record)
        self._store.save()
        return record

    def advance(
        self,
        agent_id: str,
        target: LifecycleStage,
        *,
        steward_actor: str | None = None,
    ) -> AgentRegistryRecord:
        record = self._store.get(agent_id)
        if record is None:
            raise KeyError(agent_id)
        record.lifecycle_stage = advance_lifecycle(record.lifecycle_stage, target)
        record.touch(steward_actor=steward_actor)
        if target == LifecycleStage.PUBLICATION:
            result = validate_entry(record)
            if not result.valid:
                raise ValueError("; ".join(result.errors))
        self._store.upsert(record)
        self._store.save()
        return record
