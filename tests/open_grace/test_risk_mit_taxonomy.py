"""MIT AI Risk Repository taxonomy fields on RiskRegistryRecord."""

from open_grace_governance.lifecycle import LifecycleStage
from open_grace_governance.registries import RiskRegistry
from open_grace_governance.schemas import RiskRegistryRecord
from open_grace_governance.validation import validate_entry
import pytest


def _mit_risk_kwargs(**overrides):
    base = {
        "risk_id": "wise.risk.test-mit",
        "display_name": "Test MIT risk",
        "severity": "high",
        "framework": "mit-ai-risk",
        "control_id": "MIT-7.1.1",
        "mitigation": "Benchmark and steward review",
        "agent_id": "wise.agent.metadata",
        "risk_domain": "ai-system-safety",
        "harm_type": "reputational",
        "affected_party": "society",
        "causal_source": "ai-system",
        "intent": "unintentional",
        "timing": "post-deployment",
        "residual_risk": "medium",
        "evidence": "tests/open_grace/test_risk_mit_taxonomy.py",
        "reference_models": ["mit-ai-risk", "nist-ai-rmf"],
        "lifecycle_stage": LifecycleStage.PUBLICATION,
        "steward_actor": "test-steward",
    }
    base.update(overrides)
    return base


def test_mit_fields_required_on_schema():
    with pytest.raises(ValueError):
        RiskRegistryRecord(
            risk_id="wise.risk.incomplete",
            display_name="Incomplete",
            severity="low",
            framework="nist-ai-rmf",
            control_id="MAP-1",
            mitigation="Review",
            agent_id="wise.agent.metadata",
        )


def test_residual_risk_cannot_exceed_severity():
    with pytest.raises(ValueError):
        RiskRegistryRecord(**_mit_risk_kwargs(severity="medium", residual_risk="high"))


def test_invalid_risk_domain_rejected():
    with pytest.raises(ValueError):
        RiskRegistryRecord(**_mit_risk_kwargs(risk_domain="not-a-domain"))


def test_seed_risks_load_with_mit_fields(tmp_path):
    registry = RiskRegistry(tmp_path / "risks.json")
    count = registry.seed_from_yaml()
    risks = registry.list()

    assert count == 5
    for risk in risks:
        assert risk.risk_domain
        assert risk.harm_type
        assert risk.affected_party
        assert risk.causal_source
        assert risk.intent
        assert risk.timing
        assert risk.residual_risk
        assert risk.evidence


def test_mit_aligned_seed_risks_present(tmp_path):
    registry = RiskRegistry(tmp_path / "risks.json")
    registry.seed_from_yaml()

    injection = registry.get("wise.risk.prompt-injection-attack")
    assert injection is not None
    assert injection.framework == "mit-ai-risk"
    assert injection.risk_domain == "malicious-actors"
    assert injection.intent == "intentional"

    misclass = registry.get("wise.risk.biodiversity-misclassification")
    assert misclass is not None
    assert misclass.affected_party == "ecosystem"
    assert misclass.harm_type == "environmental"


def test_validate_entry_passes_for_seed_risks(tmp_path):
    registry = RiskRegistry(tmp_path / "risks.json")
    registry.seed_from_yaml()

    for risk in registry.list():
        result = validate_entry(risk)
        assert result.valid, f"{risk.risk_id}: {result.errors}"


def test_validate_entry_warns_without_mit_reference_model():
    record = RiskRegistryRecord(**_mit_risk_kwargs(reference_models=["nist-ai-rmf"]))
    result = validate_entry(record)
    assert result.valid
    assert any("mit-ai-risk" in warning for warning in result.warnings)


def test_validate_entry_rejects_orphan_risk():
    record = RiskRegistryRecord(
        **_mit_risk_kwargs(agent_id=None, capability_id=None),
    )
    result = validate_entry(record)
    assert not result.valid
    assert any("agent_id or capability_id" in error for error in result.errors)
