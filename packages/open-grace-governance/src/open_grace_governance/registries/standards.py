"""Standards and Risk registries (constitutional plane)."""

from __future__ import annotations

from pathlib import Path

import yaml

from open_grace_governance.lifecycle import LifecycleStage, advance_lifecycle
from open_grace_governance.schemas import RiskRegistryRecord, StandardsRegistryRecord
from open_grace_governance.store.base import JsonRegistryStore
from open_grace_governance.validation import validate_entry

_PACKAGE_DATA = Path(__file__).resolve().parents[1] / "data"


class StandardsRegistry:
    def __init__(self, store_path: Path | None = None) -> None:
        self._store = JsonRegistryStore(
            store_path or _PACKAGE_DATA / "standards_registry.json",
            StandardsRegistryRecord,
            "standard_id",
        )

    def seed_from_yaml(self, path: Path | None = None) -> int:
        seed_path = path or _PACKAGE_DATA / "seed" / "standards_registry.yaml"
        if not seed_path.is_file():
            return 0
        data = yaml.safe_load(seed_path.read_text(encoding="utf-8"))
        count = 0
        for row in data.get("standards", []):
            record = StandardsRegistryRecord.model_validate(row)
            result = validate_entry(record)
            if not result.valid:
                raise ValueError(f"invalid standard seed {row}: {result.errors}")
            self._store.upsert(record)
            count += 1
        self._store.save()
        return count

    def list(self) -> list[StandardsRegistryRecord]:
        return self._store.all()

    def get(self, standard_id: str) -> StandardsRegistryRecord | None:
        return self._store.get(standard_id)

    def register(self, record: StandardsRegistryRecord) -> StandardsRegistryRecord:
        result = validate_entry(record)
        if not result.valid:
            raise ValueError("; ".join(result.errors))
        return self._store.upsert(record)

    def advance(
        self,
        standard_id: str,
        target: LifecycleStage,
        *,
        steward_actor: str | None = None,
    ) -> StandardsRegistryRecord:
        record = self._store.get(standard_id)
        if record is None:
            raise KeyError(standard_id)
        record.lifecycle_stage = advance_lifecycle(record.lifecycle_stage, target)
        record.touch(steward_actor=steward_actor)
        if target == LifecycleStage.PUBLICATION:
            result = validate_entry(record)
            if not result.valid:
                raise ValueError("; ".join(result.errors))
        self._store.upsert(record)
        self._store.save()
        return record


class RiskRegistry:
    def __init__(self, store_path: Path | None = None) -> None:
        self._store = JsonRegistryStore(
            store_path or _PACKAGE_DATA / "risk_registry.json",
            RiskRegistryRecord,
            "risk_id",
        )

    def seed_from_yaml(self, path: Path | None = None) -> int:
        seed_path = path or _PACKAGE_DATA / "seed" / "risk_registry.yaml"
        if not seed_path.is_file():
            return 0
        data = yaml.safe_load(seed_path.read_text(encoding="utf-8"))
        count = 0
        for row in data.get("risks", []):
            record = RiskRegistryRecord.model_validate(row)
            result = validate_entry(record)
            if not result.valid:
                raise ValueError(f"invalid risk seed {row}: {result.errors}")
            self._store.upsert(record)
            count += 1
        self._store.save()
        return count

    def list(self) -> list[RiskRegistryRecord]:
        return self._store.all()

    def get(self, risk_id: str) -> RiskRegistryRecord | None:
        return self._store.get(risk_id)

    def register(self, record: RiskRegistryRecord) -> RiskRegistryRecord:
        result = validate_entry(record)
        if not result.valid:
            raise ValueError("; ".join(result.errors))
        return self._store.upsert(record)

    def advance(
        self,
        risk_id: str,
        target: LifecycleStage,
        *,
        steward_actor: str | None = None,
    ) -> RiskRegistryRecord:
        record = self._store.get(risk_id)
        if record is None:
            raise KeyError(risk_id)
        record.lifecycle_stage = advance_lifecycle(record.lifecycle_stage, target)
        record.touch(steward_actor=steward_actor)
        self._store.upsert(record)
        self._store.save()
        return record
