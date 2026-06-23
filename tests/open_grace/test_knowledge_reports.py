import json

from open_grace_knowledge import KnowledgeSystem, generate_fleet_knowledge_reports
from open_grace_knowledge.reports import write_knowledge_report
from open_grace_knowledge.validation import KnowledgeValidationContext


def test_fleet_reports_all_compliant_after_seed(tmp_path):
    system = KnowledgeSystem.create(tmp_path)
    system.seed_all()
    context = KnowledgeValidationContext(knowledge=system)

    reports = generate_fleet_knowledge_reports(system, context=context)

    assert len(reports) == 21
    assert all(report.compliant for report in reports)
    assert any(report.registry == "entity" for report in reports)
    assert any(report.registry == "knowledgegraph" for report in reports)


def test_write_knowledge_report_json(tmp_path):
    system = KnowledgeSystem.create(tmp_path)
    system.seed_all()
    context = KnowledgeValidationContext(knowledge=system)
    report = generate_fleet_knowledge_reports(system, context=context)[0]

    path = write_knowledge_report(report, tmp_path / "reports")
    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload["compliant"] is True
    assert "backing_stores" in payload
    assert "reference_models" in payload
