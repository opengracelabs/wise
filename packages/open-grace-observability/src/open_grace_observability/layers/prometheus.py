"""Prometheus metric definitions and exposition helpers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

_PACKAGE_DATA = Path(__file__).resolve().parents[1] / "data" / "prometheus"


@dataclass(frozen=True)
class PrometheusMetricDefinition:
    name: str
    metric_type: str
    help: str
    labels: tuple[str, ...]


def load_metric_definitions(path: Path | None = None) -> list[PrometheusMetricDefinition]:
    defs_path = path or _PACKAGE_DATA / "metric_definitions.yaml"
    if not defs_path.is_file():
        return []
    data = yaml.safe_load(defs_path.read_text(encoding="utf-8"))
    return [
        PrometheusMetricDefinition(
            name=row["name"],
            metric_type=row["type"],
            help=row["help"],
            labels=tuple(row.get("labels", [])),
        )
        for row in data.get("metrics", [])
    ]


def exposition_line(
    name: str,
    value: float,
    *,
    labels: dict[str, str] | None = None,
    timestamp_ms: int | None = None,
) -> str:
    if labels:
        label_str = ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()))
        metric = f"{name}{{{label_str}}}"
    else:
        metric = name
    line = f"{metric} {value}"
    if timestamp_ms is not None:
        line += f" {timestamp_ms}"
    return line


def render_exposition(
  samples: list[dict[str, Any]],
  *,
  definitions: list[PrometheusMetricDefinition] | None = None,
) -> str:
    """Render Prometheus text exposition format from sample dicts."""
    defs = definitions or load_metric_definitions()
    def_by_name = {d.name: d for d in defs}
    lines: list[str] = []
    seen_help: set[str] = set()

    for sample in samples:
        name = sample["name"]
        if name in def_by_name and name not in seen_help:
            definition = def_by_name[name]
            lines.append(f"# HELP {name} {definition.help}")
            lines.append(f"# TYPE {name} {definition.metric_type}")
            seen_help.add(name)
        lines.append(
            exposition_line(
                name,
                float(sample["value"]),
                labels=sample.get("labels"),
                timestamp_ms=sample.get("timestamp_ms"),
            )
        )
    return "\n".join(lines) + ("\n" if lines else "")


def definitions_to_json(path: Path | None = None) -> str:
    return json.dumps(
        [
            {
                "name": d.name,
                "type": d.metric_type,
                "help": d.help,
                "labels": list(d.labels),
            }
            for d in load_metric_definitions(path)
        ],
        indent=2,
    )
