import pytest

from open_grace_governance.lifecycle import LifecycleStage
from open_grace_governance.schemas import (
    AgentRegistryRecord,
    BenchmarkRegistryRecord,
    ModelRegistryRecord,
    RiskRegistryRecord,
    StandardsRegistryRecord,
)
from open_grace_governance.validation import validate_entry


def test_agent_record_rejects_invalid_id():
    with pytest.raises(ValueError):
        AgentRegistryRecord(
            agent_id="invalid",
            spec_prefix="99",
            spec_path="docs/example.md",
            display_name="Example",
            plane="platform",
            langgraph_graph_id="example",
            output_schema_uri="wise_contracts.example.Example",
        )


def test_standards_record_requires_known_reference_model():
    record = StandardsRegistryRecord(
        standard_id="wise.standard.test",
        display_name="Test",
        binding_uri="https://example.com",
        schema_family="test",
        reference_model_slug="not-a-model",
    )
    result = validate_entry(record)
    assert not result.valid


def test_benchmark_requires_threshold():
    record = BenchmarkRegistryRecord(
        benchmark_id="wise.benchmark.test",
        display_name="Test",
        agent_id="wise.agent.metadata",
        metric="accuracy",
        unit="ratio",
    )
    result = validate_entry(record)
    assert not result.valid


def test_model_restricted_cannot_serve_constitutional_plane():
    record = ModelRegistryRecord(
        model_id="wise.model.restricted",
        provider="other",
        model_name="restricted",
        safety_tier="restricted",
        allowed_planes=["constitutional"],
    )
    result = validate_entry(record)
    assert not result.valid


def test_risk_requires_subject_reference():
    record = RiskRegistryRecord(
        risk_id="wise.risk.orphan",
        display_name="Orphan",
        severity="low",
        framework="nist-ai-rmf",
        control_id="MAP-1",
        mitigation="Review",
        risk_domain="ai-system-safety",
        harm_type="reputational",
        affected_party="society",
        causal_source="ai-system",
        intent="unintentional",
        timing="post-deployment",
        residual_risk="low",
        evidence="tests/open_grace/test_validation.py",
    )
    result = validate_entry(record)
    assert not result.valid


def test_publication_requires_steward_actor():
    record = AgentRegistryRecord(
        agent_id="wise.agent.test-agent",
        spec_prefix="99",
        spec_path="docs/example.md",
        display_name="Test Agent",
        plane="platform",
        langgraph_graph_id="test-agent",
        output_schema_uri="wise_contracts.example.Example",
        lifecycle_stage=LifecycleStage.PUBLICATION,
    )
    result = validate_entry(record)
    assert not result.valid
