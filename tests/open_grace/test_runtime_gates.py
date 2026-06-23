"""Gate blocking tests for Open Grace Agent Runtime v2."""

import pytest

from open_grace_governance.capabilities.registry import AgentCapabilityBinding
from open_grace_governance.lifecycle import LifecycleStage
from open_grace_governance.schemas import AgentRegistryRecord
from open_grace_governance.system import GovernanceSystem
from open_grace_runtime import RuntimeSystem
from open_grace_runtime.schemas import BenchmarkRunRecord, ExecutionStatus


def _translation_observed() -> dict[str, float]:
    return {
        "wise.benchmark.translation-cost": 0.03,
        "wise.benchmark.translation-quality": 0.85,
    }


def test_agent_registry_gate_blocks_unapproved_agent(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    system.seed_all()

    candidate = AgentRegistryRecord(
        agent_id="wise.agent.runtime-candidate",
        spec_prefix="99",
        spec_path="docs/architecture/canonical/99-test-agent.md",
        display_name="Runtime Candidate",
        plane="platform",
        langgraph_graph_id="runtime-candidate",
        output_schema_uri="wise_contracts.orchestration.BenchmarkReport",
    )
    system.agents.propose(candidate)
    system.capability_framework._bindings.append(
        AgentCapabilityBinding(
            agent_id=candidate.agent_id,
            capability_class_id="wise.capability.class.translation",
        )
    )

    runtime = RuntimeSystem.create(system)
    result = runtime.run_agent(candidate.agent_id, observed_values=_translation_observed())

    assert result.halted is True
    assert result.status == ExecutionStatus.BLOCKED
    gate = next(g for g in result.gate_results if g.gate_name == "agent_registry")
    assert gate.passed is False
    assert result.output_ref is None


def test_capability_gate_blocks_invalid_binding(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    system.seed_all()
    system.benchmarks._store.delete("wise.benchmark.translation-quality")
    system.benchmarks._store.save()

    runtime = RuntimeSystem.create(system)
    result = runtime.run_agent("wise.agent.translation", observed_values=_translation_observed())

    assert result.halted is True
    gate = next(g for g in result.gate_results if g.gate_name == "capability_validation")
    assert gate.passed is False


def test_risk_gate_blocks_unpublished_risk(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    system.seed_all()

    risk = system.risks.get("wise.risk.rights-clearance-gap")
    risk.lifecycle_stage = LifecycleStage.PROPOSAL
    system.risks._store.upsert(risk)
    system.risks._store.save()

    runtime = RuntimeSystem.create(system)
    result = runtime.run_agent("wise.agent.translation", observed_values=_translation_observed())

    assert result.halted is True
    gate_names = {gate.gate_name for gate in result.gate_results}
    assert "capability_validation" in gate_names or "risk_validation" in gate_names
    blocking = [
        gate
        for gate in result.gate_results
        if gate.gate_name in {"capability_validation", "risk_validation"} and not gate.passed
    ]
    assert blocking
    assert any("not published" in error for gate in blocking for error in gate.errors)


def test_risk_gate_blocks_unmitigated_risk(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    system.seed_all()

    risk = system.risks.get("wise.risk.rights-clearance-gap")
    risk.mitigation = "   "
    system.risks._store.upsert(risk)
    system.risks._store.save()

    runtime = RuntimeSystem.create(system)
    result = runtime.run_agent("wise.agent.translation", observed_values=_translation_observed())

    assert result.halted is True
    gate = next(g for g in result.gate_results if g.gate_name == "risk_validation")
    assert gate.passed is False
    assert any("not mitigated" in error for error in gate.errors)


def test_benchmark_gate_blocks_missing_observations(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    system.seed_all()

    runtime = RuntimeSystem.create(system)
    result = runtime.run_agent("wise.agent.translation", observed_values={})

    assert result.halted is True
    gate = next(g for g in result.gate_results if g.gate_name == "benchmark_validation")
    assert gate.passed is False


def test_benchmark_gate_allows_recorded_passing_evaluation(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    system.seed_all()

    runtime = RuntimeSystem.create(system)
    runtime.benchmark_runs.save_all(
        [
            BenchmarkRunRecord(
                benchmark_run_id="wise.benchmark-run.translation-cost-seed",
                run_id="wise.execution.translation-prior",
                agent_id="wise.agent.translation",
                capability_class_id="wise.capability.class.translation",
                benchmark_id="wise.benchmark.translation-cost",
                passed=True,
                observed_value=0.02,
                reason="within thresholds",
            ),
            BenchmarkRunRecord(
                benchmark_run_id="wise.benchmark-run.translation-quality-seed",
                run_id="wise.execution.translation-prior",
                agent_id="wise.agent.translation",
                capability_class_id="wise.capability.class.translation",
                benchmark_id="wise.benchmark.translation-quality",
                passed=True,
                observed_value=0.9,
                reason="within thresholds",
            ),
        ]
    )

    result = runtime.run_agent("wise.agent.translation", observed_values={})

    assert result.halted is False
    gate = next(g for g in result.gate_results if g.gate_name == "benchmark_validation")
    assert gate.passed is True
