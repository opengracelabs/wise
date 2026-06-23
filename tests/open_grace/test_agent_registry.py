from open_grace_governance.lifecycle import LifecycleStage
from open_grace_governance.schemas import AgentRegistryRecord
from open_grace_agent_registry import AgentRegistry


def test_import_canonical_agent_manifest(tmp_path):
    registry = AgentRegistry(tmp_path / "agents.json")
    count = registry.import_canonical_manifest()
    agents = registry.list()

    assert count == 15
    assert all(agent.agent_id.startswith("wise.agent.") for agent in agents)
    assert any(agent.agent_id == "wise.agent.standards" for agent in agents)
    assert registry.get("wise.agent.benchmark").read_only is True


def test_propose_and_advance_agent_lifecycle(tmp_path):
    registry = AgentRegistry(tmp_path / "agents.json")
    candidate = AgentRegistryRecord(
        agent_id="wise.agent.test-candidate",
        spec_prefix="99",
        spec_path="docs/architecture/canonical/99-test-agent.md",
        display_name="Test Candidate",
        plane="platform",
        langgraph_graph_id="test-candidate",
        output_schema_uri="wise_contracts.orchestration.BenchmarkReport",
    )
    registry.propose(candidate)
    advanced = registry.advance(
        "wise.agent.test-candidate",
        LifecycleStage.REVIEW,
        steward_actor="architecture-office",
    )
    assert advanced.lifecycle_stage == LifecycleStage.REVIEW
