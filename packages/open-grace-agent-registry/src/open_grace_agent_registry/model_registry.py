"""Model registry for AI Platform model councils."""

from __future__ import annotations

from pathlib import Path

import yaml

from open_grace_governance.lifecycle import LifecycleStage, advance_lifecycle
from open_grace_governance.schemas import ModelRegistryRecord
from open_grace_governance.store.base import JsonRegistryStore
from open_grace_governance.validation import validate_entry

_PACKAGE_DATA = Path(__file__).resolve().parent / "data"


class ModelRegistry:
    def __init__(self, store_path: Path | None = None) -> None:
        self._store = JsonRegistryStore(
            store_path or _PACKAGE_DATA / "model_registry.json",
            ModelRegistryRecord,
            "model_id",
        )

    def seed_from_yaml(self, path: Path | None = None) -> int:
        seed_path = path or _PACKAGE_DATA / "seed" / "model_registry.yaml"
        if not seed_path.is_file():
            return 0
        data = yaml.safe_load(seed_path.read_text(encoding="utf-8"))
        count = 0
        for row in data.get("models", []):
            record = ModelRegistryRecord.model_validate(row)
            result = validate_entry(record)
            if not result.valid:
                raise ValueError(f"invalid model seed {row}: {result.errors}")
            self._store.upsert(record)
            count += 1
        self._store.save()
        return count

    def list(self) -> list[ModelRegistryRecord]:
        return self._store.all()

    def get(self, model_id: str) -> ModelRegistryRecord | None:
        return self._store.get(model_id)

    def register(self, record: ModelRegistryRecord) -> ModelRegistryRecord:
        result = validate_entry(record)
        if not result.valid:
            raise ValueError("; ".join(result.errors))
        self._store.upsert(record)
        self._store.save()
        return record

    def advance(
        self,
        model_id: str,
        target: LifecycleStage,
        *,
        steward_actor: str | None = None,
    ) -> ModelRegistryRecord:
        record = self._store.get(model_id)
        if record is None:
            raise KeyError(model_id)
        record.lifecycle_stage = advance_lifecycle(record.lifecycle_stage, target)
        record.touch(steward_actor=steward_actor)
        if target == LifecycleStage.PUBLICATION:
            result = validate_entry(record)
            if not result.valid:
                raise ValueError("; ".join(result.errors))
        self._store.upsert(record)
        self._store.save()
        return record
