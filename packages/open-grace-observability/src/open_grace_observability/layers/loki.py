"""Loki log stream and label schema definitions."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

_PACKAGE_DATA = Path(__file__).resolve().parents[1] / "data" / "loki"


@dataclass(frozen=True)
class LokiLabelSchema:
    name: str
    description: str
    required: bool = True


@dataclass(frozen=True)
class LokiLogStream:
    stream: str
    labels: dict[str, str]
    description: str


def load_label_schemas(path: Path | None = None) -> list[LokiLabelSchema]:
    schema_path = path or _PACKAGE_DATA / "log_streams.yaml"
    if not schema_path.is_file():
        return []
    data = yaml.safe_load(schema_path.read_text(encoding="utf-8"))
    return [
        LokiLabelSchema(
            name=row["name"],
            description=row["description"],
            required=row.get("required", True),
        )
        for row in data.get("label_schemas", [])
    ]


def load_log_streams(path: Path | None = None) -> list[LokiLogStream]:
    schema_path = path or _PACKAGE_DATA / "log_streams.yaml"
    if not schema_path.is_file():
        return []
    data = yaml.safe_load(schema_path.read_text(encoding="utf-8"))
    return [
        LokiLogStream(
            stream=row["stream"],
            labels=dict(row.get("labels", {})),
            description=row.get("description", ""),
        )
        for row in data.get("log_streams", [])
    ]
