from open_grace_observability import ObservabilitySystem
from open_grace_observability.schemas import AgentExecutionMetric
from open_grace_observability.validation import validate_metric_entry


def test_validate_agent_metric_reference_models():
    metric = AgentExecutionMetric(
        metric_id="wise.metric.agent.test-latency",
        display_name="Test",
        agent_id="wise.agent.metadata",
        metric_kind="latency",
        value=1.0,
        unit="ms",
        reference_models=["opentelemetry"],
    )
    result = validate_metric_entry(metric)
    assert result.valid


def test_reject_unknown_reference_model():
    metric = AgentExecutionMetric(
        metric_id="wise.metric.agent.test-latency",
        display_name="Test",
        agent_id="wise.agent.metadata",
        metric_kind="latency",
        value=1.0,
        unit="ms",
        reference_models=["not-a-real-model"],
    )
    result = validate_metric_entry(metric)
    assert not result.valid
    assert "unknown observability reference model" in result.errors[0]


def test_cross_registry_unknown_agent(tmp_path):
    from open_grace_observability.validation import MetricValidationContext, validate_metric_cross_registry

    system = ObservabilitySystem.create(tmp_path)
    system.seed_all()

    metric = system.agent_metrics.get("wise.metric.agent.metadata-latency-p50")
    context = MetricValidationContext(observability=system, agents=None)
    result = validate_metric_cross_registry(metric, context)
    assert result.valid

    class FakeAgents:
        def get(self, agent_id):
            return None

    context = MetricValidationContext(observability=system, agents=FakeAgents())
    result = validate_metric_cross_registry(metric, context)
    assert not result.valid
    assert "unknown agent_id" in result.errors[0]
