"""Shared registry implementation for knowledge stores."""

from __future__ import annotations

from pathlib import Path
from typing import Generic, TypeVar

import yaml
from pydantic import BaseModel

from open_grace_governance.lifecycle import LifecycleStage, advance_lifecycle
from open_grace_governance.store.base import JsonRegistryStore
from open_grace_knowledge.validation import validate_knowledge_entry

T = TypeVar("T", bound=BaseModel)

_PACKAGE_DATA = Path(__file__).resolve().parents[1] / "data"


class KnowledgeRegistry(Generic[T]):
    """YAML-seeded JSON file registry for a single knowledge domain."""

    def __init__(
        self,
        *,
        store_path: Path,
        model: type[T],
        id_field: str,
        seed_filename: str,
        seed_key: str,
    ) -> None:
        self._id_field = id_field
        self._seed_key = seed_key
        self._seed_path = _PACKAGE_DATA / "seed" / seed_filename
        self._store = JsonRegistryStore(store_path, model, id_field)

    def seed_from_yaml(self, path: Path | None = None) -> int:
        seed_path = path or self._seed_path
        if not seed_path.is_file():
            return 0
        data = yaml.safe_load(seed_path.read_text(encoding="utf-8"))
        count = 0
        for row in data.get(self._seed_key, []):
            record = self._store.model.model_validate(row)
            result = validate_knowledge_entry(record)
            if not result.valid:
                raise ValueError(f"invalid seed row {row}: {result.errors}")
            self._store.upsert(record)
            count += 1
        self._store.save()
        return count

    def list(self) -> list[T]:
        return self._store.all()

    def get(self, entry_id: str) -> T | None:
        return self._store.get(entry_id)

    def register(self, record: T) -> T:
        result = validate_knowledge_entry(record)
        if not result.valid:
            raise ValueError("; ".join(result.errors))
        self._store.upsert(record)
        self._store.save()
        return record

    def advance(
        self,
        entry_id: str,
        target: LifecycleStage,
        *,
        steward_actor: str | None = None,
    ):
        record = self._store.get(entry_id)
        if record is None:
            raise KeyError(entry_id)
        record.lifecycle_stage = advance_lifecycle(record.lifecycle_stage, target)
        record.touch(steward_actor=steward_actor)
        if target == LifecycleStage.PUBLICATION:
            result = validate_knowledge_entry(record)
            if not result.valid:
                raise ValueError("; ".join(result.errors))
        self._store.upsert(record)
        self._store.save()
        return record
