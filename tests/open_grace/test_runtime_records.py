"""Runtime record persistence tests."""

from open_grace_governance.system import GovernanceSystem
from open_grace_runtime import RuntimeSystem
from open_grace_runtime.schemas import ExecutionStatus


def _translation_observed() -> dict[str, float]:
    return {
        "wise.benchmark.translation-cost": 0.03,
        "wise.benchmark.translation-quality": 0.85,
    }


def test_execution_audit_and_benchmark_records_persisted(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    system.seed_all()
    runtime = RuntimeSystem.create(system)

    result = runtime.run_agent(
        "wise.agent.translation",
        observed_values=_translation_observed(),
        steward_actor="test-runtime",
    )

    assert result.execution is not None
    assert result.execution.status == ExecutionStatus.COMPLETED
    assert result.execution.gate_results
    assert result.execution.audit_id is not None

    stored = runtime.executions.get(result.run_id)
    assert stored is not None
    assert stored.agent_id == "wise.agent.translation"
    assert stored.capability_class_ids == ["wise.capability.class.translation"]

    audit = system.audits.get(result.audit_id)
    assert audit is not None
    assert audit.subject_id == "wise.agent.translation"
    assert audit.trace_id == result.run_id

    benchmark_runs = runtime.benchmark_runs.for_run(result.run_id)
    assert len(benchmark_runs) == 2
    assert all(run.passed for run in benchmark_runs)


def test_blocked_run_persists_execution_record(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    system.seed_all()
    runtime = RuntimeSystem.create(system)

    result = runtime.run_agent("wise.agent.translation", observed_values={})

    assert result.halted is True
    stored = runtime.executions.get(result.run_id)
    assert stored is not None
    assert stored.status == ExecutionStatus.BLOCKED
    assert stored.output_ref is None
    assert any(not gate.passed for gate in stored.gate_results)
