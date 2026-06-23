"""Resolve canonical WISE manifest paths without modifying architecture."""

from __future__ import annotations

import os
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def manifest_root() -> Path:
    env_root = os.environ.get("WISE_MANIFEST_ROOT")
    if env_root:
        return Path(env_root)
    root = repo_root()
    canonical = root / "data" / "registry"
    if (canonical / "agents" / "manifest.yaml").is_file():
        return canonical
    return root / "packages" / "wise-orchestration" / "src" / "wise_orchestration" / "data" / "registry"


def agents_manifest_path() -> Path:
    return manifest_root() / "agents" / "manifest.yaml"


def capabilities_manifest_path() -> Path:
    return manifest_root() / "capabilities" / "manifest.yaml"
