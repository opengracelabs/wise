"""Unit tests for registry manifests."""

from wise_orchestration.manifest_loader import (
    CANONICAL_AGENT_COUNT,
    CANONICAL_CAPABILITY_COUNT,
    load_agents_manifest,
    load_capabilities_manifest,
)
from wise_orchestration.registry import GRAPH_REGISTRY


def test_agent_manifest_count():
    agents = load_agents_manifest()
    assert len(agents) == CANONICAL_AGENT_COUNT


def test_capability_manifest_count():
    capabilities, links, services = load_capabilities_manifest()
    assert len(capabilities) == CANONICAL_CAPABILITY_COUNT
    assert len(links) >= 10
    assert len(services) >= 8


def test_manifest_graph_ids_match_registry():
    agents = load_agents_manifest()
    manifest_graph_ids = {agent.langgraph_graph_id for agent in agents}
    assert manifest_graph_ids == set(GRAPH_REGISTRY)


def test_governance_agents_are_read_only():
    agents = load_agents_manifest()
    read_only = {a.langgraph_graph_id for a in agents if a.read_only}
    assert read_only == {"standards", "benchmark"}
