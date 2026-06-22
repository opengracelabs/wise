"""Startup validation — manifest, database, and graph registry must align."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from wise_orchestration.graphs.registry import GRAPH_REGISTRY, assert_graph_has_no_canonical_write_path
from wise_orchestration.manifest_loader import (
    CANONICAL_AGENT_COUNT,
    CANONICAL_CAPABILITY_COUNT,
    load_agents_manifest,
    load_capabilities_manifest,
)
from wise_registry.models import Agent, Capability


class RegistryValidationError(RuntimeError):
    """Raised when manifest, database, and graph registrations diverge."""


def _agent_key(entry) -> str:
    return entry.agent_id


def validate_registry_alignment(session: Session) -> None:
    """Fail fast if manifest, registry tables, or graph factory diverge."""
    manifest_agents = load_agents_manifest()
    manifest_caps, manifest_links, manifest_services = load_capabilities_manifest()

    if len(manifest_agents) != CANONICAL_AGENT_COUNT:
        raise RegistryValidationError(
            f"Agent manifest count {len(manifest_agents)} != {CANONICAL_AGENT_COUNT}"
        )
    if len(manifest_caps) != CANONICAL_CAPABILITY_COUNT:
        raise RegistryValidationError(
            f"Capability manifest count {len(manifest_caps)} != {CANONICAL_CAPABILITY_COUNT}"
        )

    db_agents = session.scalars(select(Agent)).all()
    db_caps = session.scalars(select(Capability)).all()

    if len(db_agents) != CANONICAL_AGENT_COUNT:
        raise RegistryValidationError(
            f"Database agent count {len(db_agents)} != {CANONICAL_AGENT_COUNT}"
        )
    if len(db_caps) != CANONICAL_CAPABILITY_COUNT:
        raise RegistryValidationError(
            f"Database capability count {len(db_caps)} != {CANONICAL_CAPABILITY_COUNT}"
        )

    manifest_by_id = {_agent_key(a): a for a in manifest_agents}
    db_by_id = {a.agent_id: a for a in db_agents}

    if set(manifest_by_id) != set(db_by_id):
        raise RegistryValidationError(
            f"Agent ID mismatch manifest={sorted(manifest_by_id)} db={sorted(db_by_id)}"
        )

    graph_ids_manifest = {a.langgraph_graph_id for a in manifest_agents}
    graph_ids_registry = set(GRAPH_REGISTRY)

    if graph_ids_manifest != graph_ids_registry:
        missing_in_graphs = graph_ids_manifest - graph_ids_registry
        extra_in_graphs = graph_ids_registry - graph_ids_manifest
        raise RegistryValidationError(
            f"Graph registry mismatch missing={sorted(missing_in_graphs)} extra={sorted(extra_in_graphs)}"
        )

    for agent in manifest_agents:
        db_agent = db_by_id[agent.agent_id]
        fields = (
            ("spec_prefix", agent.spec_prefix, db_agent.spec_prefix),
            ("spec_path", agent.spec_path, db_agent.spec_path),
            ("langgraph_graph_id", agent.langgraph_graph_id, db_agent.langgraph_graph_id),
            ("read_only", agent.read_only, db_agent.read_only),
            ("plane", agent.plane, db_agent.plane.value),
        )
        for name, manifest_val, db_val in fields:
            if manifest_val != db_val:
                raise RegistryValidationError(
                    f"Agent {agent.agent_id} field {name}: manifest={manifest_val!r} db={db_val!r}"
                )
        assert_graph_has_no_canonical_write_path(agent.langgraph_graph_id)

    manifest_cap_ids = {c.capability_id for c in manifest_caps}
    db_cap_ids = {c.capability_id for c in db_caps}
    if manifest_cap_ids != db_cap_ids:
        raise RegistryValidationError(
            f"Capability ID mismatch manifest={sorted(manifest_cap_ids)} db={sorted(db_cap_ids)}"
        )

    _ = manifest_links, manifest_services  # reserved for Phase 1 link validation
