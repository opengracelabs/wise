from open_grace_governance.lifecycle import LifecycleStage
from open_grace_governance.registries import RiskRegistry, StandardsRegistry


def test_seed_standards_registry(tmp_path):
    registry = StandardsRegistry(tmp_path / "standards.json")
    count = registry.seed_from_yaml()
    standards = registry.list()

    assert count == 4
    assert registry.get("wise.standard.cidoc-crm").reference_model_slug == "unesco"


def test_advance_standard_lifecycle(tmp_path):
    registry = StandardsRegistry(tmp_path / "standards.json")
    registry.seed_from_yaml()
    record = registry.advance(
        "wise.standard.opentelemetry",
        LifecycleStage.AUDIT,
        steward_actor="architecture-office",
    )
    assert record.lifecycle_stage == LifecycleStage.AUDIT


def test_seed_risk_registry(tmp_path):
    registry = RiskRegistry(tmp_path / "risks.json")
    count = registry.seed_from_yaml()
    risks = registry.list()

    assert count == 3
    assert any(risk.framework == "nist-ai-rmf" for risk in risks)
