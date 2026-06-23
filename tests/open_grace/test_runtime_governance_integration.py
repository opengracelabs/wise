"""GovernanceSystem runtime integration tests."""

from open_grace_governance.system import GovernanceSystem
from open_grace_runtime import RuntimeSystem
from open_grace_runtime.schemas import ExecutionStatus


def _translation_observed() -> dict[str, float]:
    return {
        "wise.benchmark.translation-cost": 0.03,
        "wise.benchmark.translation-quality": 0.85,
    }


def test_governance_run_agent_integration(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    system.seed_all()

    result = system.run_agent(
        "wise.agent.translation",
        observed_values=_translation_observed(),
        steward_actor="governance-runtime-test",
    )

    assert result.status == ExecutionStatus.COMPLETED
    assert system.runtime.summary()["executions"] == 1
    assert system.runtime.summary()["benchmark_runs"] == 2


def test_runtime_system_create_from_governance(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    system.seed_all()

    runtime = RuntimeSystem.create(system)
    assert runtime.governance is system

    result = runtime.run_agent(
        "wise.agent.translation",
        observed_values=_translation_observed(),
    )
    assert result.halted is False


def test_run_agent_records_observability_metrics(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    system.seed_all()
    before_agent_metrics = system.summary()["agent_metrics"]
    before_benchmark_metrics = system.summary()["benchmark_metrics"]

    system.run_agent(
        "wise.agent.translation",
        observed_values=_translation_observed(),
        steward_actor="observability-test",
    )

    after = system.summary()
    assert after["agent_metrics"] == before_agent_metrics + 1
    assert after["benchmark_metrics"] == before_benchmark_metrics + 2
