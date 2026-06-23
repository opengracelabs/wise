"""LangGraph runtime flow tests."""

from open_grace_governance.system import GovernanceSystem
from open_grace_runtime.langgraph import build_runtime_graph, initial_runtime_state
from open_grace_runtime.schemas import ExecutionStatus
from open_grace_runtime.system import RuntimeSystem


def _translation_observed() -> dict[str, float]:
    return {
        "wise.benchmark.translation-cost": 0.03,
        "wise.benchmark.translation-quality": 0.85,
    }


def test_runtime_graph_compiles(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    system.seed_all()
    runtime = RuntimeSystem.create(system)

    app = build_runtime_graph(runtime)
    state = initial_runtime_state(
        agent_id="wise.agent.translation",
        observed_values=_translation_observed(),
        steward_actor="test-runtime",
    )
    final = app.invoke(state)

    assert final["halted"] is False
    assert final["status"] == ExecutionStatus.COMPLETED.value
    assert final["model_id"] is not None
    assert final["output_ref"].startswith("stub://execution/")
    assert final["audit_id"] is not None
    assert len(final["gate_results"]) >= 4


def test_runtime_full_flow_via_system(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    system.seed_all()

    result = system.run_agent(
        "wise.agent.translation",
        observed_values=_translation_observed(),
        steward_actor="test-runtime",
    )

    assert result.halted is False
    assert result.status == ExecutionStatus.COMPLETED
    assert result.model_id in {"wise.model.claude-sonnet", "wise.model.gpt-4o"}
    assert result.execution is not None
    assert result.execution.output_ref.startswith("stub://execution/")

    gate_names = {gate.gate_name for gate in result.gate_results}
    assert "agent_registry" in gate_names
    assert "capability_validation" in gate_names
    assert "risk_validation" in gate_names
    assert "benchmark_validation" in gate_names
