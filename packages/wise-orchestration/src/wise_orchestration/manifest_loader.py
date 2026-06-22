"""Load agent and capability manifests from data/registry/."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[4]
PACKAGE_DATA_ROOT = Path(__file__).resolve().parents[1] / "data" / "registry"
CANONICAL_AGENT_COUNT = 15
CANONICAL_CAPABILITY_COUNT = 12


def manifest_root() -> Path:
    """Resolve manifest directory (dev repo root or WISE_MANIFEST_ROOT in containers)."""
    env_root = os.environ.get("WISE_MANIFEST_ROOT")
    if env_root:
        return Path(env_root)
    repo_manifest = REPO_ROOT / "data" / "registry"
    if (repo_manifest / "agents" / "manifest.yaml").is_file():
        return repo_manifest
    return PACKAGE_DATA_ROOT


def agents_manifest_path() -> Path:
    return manifest_root() / "agents" / "manifest.yaml"


def capabilities_manifest_path() -> Path:
    return manifest_root() / "capabilities" / "manifest.yaml"


@dataclass(frozen=True)
class AgentManifestEntry:
    agent_id: str
    spec_prefix: str
    spec_path: str
    display_name: str
    plane: str
    build_phase: int | None
    service_binding: str | None
    langgraph_graph_id: str
    output_schema_uri: str
    evidence_profile: bool
    read_only: bool


@dataclass(frozen=True)
class CapabilityManifestEntry:
    capability_id: str
    canonical_section: str
    display_name: str
    build_phase: int | None
    plane: str
    contract_producer: str | None
    contract_consumer: str | None


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_agents_manifest(manifest_path: Path | None = None) -> list[AgentManifestEntry]:
    data = _load_yaml(manifest_path or agents_manifest_path())
    entries = []
    for row in data["agents"]:
        entries.append(
            AgentManifestEntry(
                agent_id=row["agent_id"],
                spec_prefix=row["spec_prefix"],
                spec_path=row["spec_path"],
                display_name=row["display_name"],
                plane=row["plane"],
                build_phase=row.get("build_phase"),
                service_binding=row.get("service_binding"),
                langgraph_graph_id=row["langgraph_graph_id"],
                output_schema_uri=row["output_schema_uri"],
                evidence_profile=bool(row.get("evidence_profile", False)),
                read_only=bool(row.get("read_only", False)),
            )
        )
    return entries


def load_capabilities_manifest(
    manifest_path: Path | None = None,
) -> tuple[list[CapabilityManifestEntry], list[tuple[str, str, str]], list[tuple[str, str, str, str]]]:
    data = _load_yaml(manifest_path or capabilities_manifest_path())
    capabilities = [
        CapabilityManifestEntry(
            capability_id=row["capability_id"],
            canonical_section=row["canonical_section"],
            display_name=row["display_name"],
            build_phase=row.get("build_phase"),
            plane=row["plane"],
            contract_producer=row.get("contract_producer"),
            contract_consumer=row.get("contract_consumer"),
        )
        for row in data["capabilities"]
    ]
    links = [
        (row["capability_id"], row["agent_id"], row["role"])
        for row in data.get("capability_agents", [])
    ]
    services = [
        (
            row["capability_id"],
            row["service_name"],
            row["base_url_env"],
            row.get("health_path", "/health"),
        )
        for row in data.get("capability_services", [])
    ]
    return capabilities, links, services
