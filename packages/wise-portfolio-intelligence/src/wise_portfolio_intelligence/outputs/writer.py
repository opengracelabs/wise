"""Helpers for serializing portfolio candidate outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping


def write_candidate_outputs(
    outputs: Mapping[str, list[Mapping[str, Any]]],
    output_dir: str | Path,
) -> list[Path]:
    """Write candidate output groups to JSON files."""

    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for filename, rows in outputs.items():
        output_path = path / filename
        output_path.write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        written.append(output_path)
    return written
