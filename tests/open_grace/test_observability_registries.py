from open_grace_observability import ObservabilitySystem


def test_seed_all_five_metric_registries(tmp_path):
    system = ObservabilitySystem.create(tmp_path)
    seeded = system.seed_all()

    assert seeded["agent_metrics"] == 3
    assert seeded["capability_metrics"] == 3
    assert seeded["benchmark_metrics"] == 3
    assert seeded["audit_metrics"] == 3
    assert seeded["cost_metrics"] == 3

    summary = system.summary()
    assert summary["agent_metrics"] == 3
    assert summary["cost_metrics"] == 3


def test_get_by_id_resolves_agent_metric(tmp_path):
    system = ObservabilitySystem.create(tmp_path)
    system.seed_all()

    record = system.get_by_id("wise.metric.agent.metadata-latency-p50")
    assert record is not None
    assert record.agent_id == "wise.agent.metadata"
    assert record.value == 245.5


def test_record_agent_execution(tmp_path):
    system = ObservabilitySystem.create(tmp_path)

    metric = system.record_agent_execution(
        agent_id="wise.agent.metadata",
        metric_kind="latency",
        value=100.0,
        unit="ms",
        trace_id="trace-abc",
    )
    assert metric.metric_id.startswith("wise.metric.agent.metadata-latency-")
    assert len(system.agent_metrics.list()) == 1
