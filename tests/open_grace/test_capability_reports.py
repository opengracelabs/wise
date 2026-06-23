import json

from open_grace_governance.capabilities import CapabilityFrameworkRegistry
from open_grace_governance.capabilities.reports import (
    CAPABILITY_REPORT_FILENAME,
    generate_capability_report,
    write_capability_report,
)
from open_grace_governance.capabilities.validation import CapabilityValidationContext
from open_grace_governance.system import GovernanceSystem


def test_generate_and_write_capability_report(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    system.seed_all()

    record = system.capability_framework.get("wise.capability.class.analysis")
    report = generate_capability_report(
        record,
        context=system.capability_validation_context(),
        benchmark_registry=system.benchmarks,
        observed_values={
            "wise.benchmark.kg-reliability": 0.95,
            "wise.benchmark.analysis-latency": 20.0,
        },
        linked_agents=system.capability_framework.agents_for_capability(record.id),
    )

    assert report.validation_passed is True
    assert report.benchmark_passed is True
    assert report.compliant is True
    assert "wise.agent.knowledge-graph" in report.linked_agents

    path = write_capability_report(report, tmp_path / "reports")
    payload = json.loads((tmp_path / "reports" / CAPABILITY_REPORT_FILENAME).read_text())
    assert payload["capability_id"] == "wise.capability.class.analysis"
    assert payload["compliant"] is True
    assert path.is_file()


def test_fleet_capability_reports(tmp_path):
    system = GovernanceSystem.create(tmp_path)
    system.seed_all()
    reports = system.capability_reports()

    assert len(reports) == 8
    assert all(report.validation_passed for report in reports)
