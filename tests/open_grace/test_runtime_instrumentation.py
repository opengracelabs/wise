"""Runtime v2 OpenTelemetry instrumentation tests."""

from open_grace_governance.system import GovernanceSystem
from open_grace_observability.layers.prometheus import render_exposition
from open_grace_runtime.instrumentation import RuntimeInstrumentation, get_runtime_instrumentation
from open_grace_runtime.system import RuntimeSystem


def test_runtime_instrumentation_metrics_snapshot():
    inst = RuntimeInstrumentation()
    inst.record_execution_outcome(
        agent_id="wise.agent.translation",
        run_id="wise.execution.translation-test01",
        success=True,
        halted=False,
        gate_results=[{"gate_name": "agent_registry", "passed": True}],
        benchmark_evaluations=[
            {"benchmark_id": "wise.benchmark.translation-quality", "observed_value": 0.9}
        ],
    )
    snap = inst.snapshot
    assert snap.execution_count == 1
    assert snap.execution_success_count == 1
    assert snap.execution_success_rate == 1.0
    assert snap.benchmark_score == 0.9


def test_runtime_instrumentation_gate_failures():
    inst = RuntimeInstrumentation()
    inst.record_execution_outcome(
        agent_id="wise.agent.translation",
        run_id="wise.execution.translation-test02",
        success=False,
        halted=True,
        gate_results=[
            {"gate_name": "risk_validation", "passed": False},
            {"gate_name": "capability_validation", "passed": False},
        ],
    )
    assert inst.snapshot.risk_gate_failures == 1
    assert inst.snapshot.capability_gate_failures == 1


def test_runtime_graph_records_instrumentation(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    system.seed_all()
    runtime = RuntimeSystem.create(system)

    before = get_runtime_instrumentation().snapshot.execution_count
    runtime.run_agent(
        "wise.agent.translation",
        observed_values={
            "wise.benchmark.translation-cost": 0.03,
            "wise.benchmark.translation-quality": 0.85,
        },
        steward_actor="otel-test",
    )
    after = get_runtime_instrumentation().snapshot.execution_count
    assert after == before + 1
    assert len(get_runtime_instrumentation().snapshot.node_latencies_ms) >= 4


def test_prometheus_exposition_for_runtime_metrics():
    inst = RuntimeInstrumentation()
    inst.record_execution_outcome(
        agent_id="wise.agent.metadata",
        run_id="wise.execution.metadata-test01",
        success=True,
        halted=False,
        gate_results=[],
        benchmark_evaluations=[{"benchmark_id": "wise.benchmark.metadata-quality", "observed_value": 0.95}],
    )
    text = render_exposition(inst.prometheus_samples())
    assert "open_grace_runtime_execution_count" in text
    assert "open_grace_runtime_benchmark_score" in text
