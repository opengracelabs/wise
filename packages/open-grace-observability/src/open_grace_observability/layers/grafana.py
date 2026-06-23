"""Grafana dashboard definition loader."""

from __future__ import annotations

import json
from pathlib import Path

_PACKAGE_DATA = Path(__file__).resolve().parents[1] / "data" / "grafana" / "dashboards"


def list_dashboards(directory: Path | None = None) -> list[Path]:
    root = directory or _PACKAGE_DATA
    if not root.is_dir():
        return []
    return sorted(root.glob("*.json"))


def load_dashboard(name: str, directory: Path | None = None) -> dict:
    root = directory or _PACKAGE_DATA
    path = root / name
    if not path.is_file():
        raise FileNotFoundError(f"dashboard not found: {name}")
    return json.loads(path.read_text(encoding="utf-8"))


def dashboard_uid(name: str, directory: Path | None = None) -> str:
    dashboard = load_dashboard(name, directory)
    return dashboard.get("uid", dashboard.get("title", name))
