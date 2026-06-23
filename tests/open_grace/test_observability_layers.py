from open_grace_observability import ObservabilitySystem
from open_grace_observability.layers import (
    load_dashboard,
    load_log_streams,
    load_metric_definitions,
    render_exposition,
    trace_agent_execution,
)
from open_grace_observability.reports import generate_fleet_observability_reports, write_observability_report


def test_prometheus_metric_definitions():
    defs = load_metric_definitions()
    assert len(defs) >= 6
    names = {d.name for d in defs}
    assert "open_grace_agent_execution_latency_seconds" in names


def test_prometheus_exposition_format():
    text = render_exposition(
        [
            {
                "name": "open_grace_agent_execution_total",
                "value": 42,
                "labels": {"agent_id": "wise.agent.metadata", "outcome": "success"},
            }
        ]
    )
    assert "# HELP open_grace_agent_execution_total" in text
    assert 'agent_id="wise.agent.metadata"' in text
    assert "42" in text


def test_grafana_dashboard_loads():
    dashboard = load_dashboard("open-grace-overview.json")
    assert dashboard["uid"] == "open-grace-overview"
    assert len(dashboard["panels"]) >= 4


def test_loki_log_streams():
    streams = load_log_streams()
    assert len(streams) >= 4
    assert any(s.stream == "audit_evidence" for s in streams)


def test_opentelemetry_stub_span(tmp_path):
    with trace_agent_execution("wise.agent.metadata", execution_id="exec-1") as span:
        assert span is not None
        if hasattr(span, "trace_id"):
            assert len(span.trace_id) > 0


def test_observability_reports(tmp_path):
    system = ObservabilitySystem.create(tmp_path)
    system.seed_all()

    reports = generate_fleet_observability_reports(system)
    assert len(reports) == 15
    assert all(report.validation_passed for report in reports)

    path = write_observability_report(reports[0], tmp_path / "reports")
    assert path.is_file()
