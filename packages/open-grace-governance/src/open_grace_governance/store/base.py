"""File-backed JSON registry store."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class JsonRegistryStore(Generic[T]):
    """Persist governed registry records as JSON arrays."""

    def __init__(self, path: Path, model: type[T], id_field: str) -> None:
        self.path = path
        self.model = model
        self.id_field = id_field
        self._records: dict[str, T] = {}
        if path.is_file():
            self._load()

    def _load(self) -> None:
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        for row in payload.get("entries", []):
            record = self.model.model_validate(row)
            self._records[getattr(record, self.id_field)] = record

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        entries = [record.model_dump(mode="json") for record in self._records.values()]
        self.path.write_text(
            json.dumps({"version": "1.0", "entries": entries}, indent=2),
            encoding="utf-8",
        )

    def all(self) -> list[T]:
        return list(self._records.values())

    def get(self, entry_id: str) -> T | None:
        return self._records.get(entry_id)

    def upsert(self, record: T) -> T:
        entry_id = getattr(record, self.id_field)
        self._records[entry_id] = record
        return record

    def delete(self, entry_id: str) -> bool:
        return self._records.pop(entry_id, None) is not None

    def clear(self) -> None:
        self._records.clear()
