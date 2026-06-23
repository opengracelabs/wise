import pytest

from open_grace_governance.capabilities.registry import AgentCapabilityBinding
from open_grace_governance.lifecycle import LifecycleStage
from open_grace_governance.schemas import AgentRegistryRecord
from open_grace_governance.system import GovernanceSystem


def test_validate_agent_approval_passes_for_bound_agent(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    system.seed_all()

    result = system.validate_agent_approval("wise.agent.translation")
    assert result.valid is True


def test_advance_agent_to_approval_requires_capability_validation(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    system.seed_all()

    candidate = AgentRegistryRecord(
        agent_id="wise.agent.test-candidate",
        spec_prefix="99",
        spec_path="docs/architecture/canonical/99-test-agent.md",
        display_name="Test Candidate",
        plane="platform",
        langgraph_graph_id="test-candidate",
        output_schema_uri="wise_contracts.orchestration.BenchmarkReport",
    )
    system.agents.propose(candidate)
    system.capability_framework._bindings.append(
        AgentCapabilityBinding(
            agent_id=candidate.agent_id,
            capability_class_id="wise.capability.class.translation",
        )
    )
    system.agents.advance(candidate.agent_id, LifecycleStage.REVIEW, steward_actor="test")
    system.agents.advance(candidate.agent_id, LifecycleStage.BENCHMARK, steward_actor="test")

    approved = system.advance_agent(
        candidate.agent_id,
        LifecycleStage.APPROVAL,
        steward_actor="architecture-office",
    )
    assert approved.lifecycle_stage == LifecycleStage.APPROVAL


def test_advance_agent_approval_blocked_on_invalid_capability_binding(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    system.seed_all()

    system.benchmarks._store.delete("wise.benchmark.translation-quality")
    system.benchmarks._store.save()

    result = system.validate_agent_approval("wise.agent.translation")
    assert result.valid is False

    candidate = AgentRegistryRecord(
        agent_id="wise.agent.blocked-candidate",
        spec_prefix="99",
        spec_path="docs/architecture/canonical/99-test-agent.md",
        display_name="Blocked Candidate",
        plane="platform",
        langgraph_graph_id="blocked-candidate",
        output_schema_uri="wise_contracts.orchestration.BenchmarkReport",
    )
    system.agents.propose(candidate)
    system.capability_framework._bindings.append(
        AgentCapabilityBinding(
            agent_id=candidate.agent_id,
            capability_class_id="wise.capability.class.translation",
        )
    )
    system.agents.advance(candidate.agent_id, LifecycleStage.REVIEW, steward_actor="test")
    system.agents.advance(candidate.agent_id, LifecycleStage.BENCHMARK, steward_actor="test")

    with pytest.raises(ValueError, match="capability validation failed"):
        system.advance_agent(
            candidate.agent_id,
            LifecycleStage.APPROVAL,
            steward_actor="architecture-office",
        )
