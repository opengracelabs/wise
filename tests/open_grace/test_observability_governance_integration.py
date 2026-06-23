from open_grace_governance.system import GovernanceSystem


def test_governance_observability_seed_and_validate(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    seeded = system.seed_all()

    assert seeded["agent_metrics"] == 3
    assert seeded["benchmark_metrics"] == 3

    result = system.validate_metric_context("wise.metric.agent.metadata-latency-p50")
    assert result.valid, result.errors

    result = system.validate_metric_context("wise.metric.benchmark.standards-conformance-observed")
    assert result.valid, result.errors


def test_record_agent_metric_via_governance(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    system.seed_all()

    metric = system.record_agent_metric(
        agent_id="wise.agent.metadata",
        metric_kind="latency",
        value=150.0,
        unit="ms",
    )
    assert metric.metric_id.startswith("wise.metric.agent.metadata-latency-")
    assert system.summary()["agent_metrics"] == 4


def test_observability_reports_with_registry_hooks(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    system.seed_all()

    reports = system.observability_reports()
    assert len(reports) == 15
    assert all(report.validation_passed for report in reports)

    summary = system.summary()
    assert summary["agent_metrics"] == 3
    assert summary["cost_metrics"] == 3
