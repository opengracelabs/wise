from open_grace_governance.capabilities import CapabilityFrameworkRegistry
from open_grace_governance.capabilities.validation import (
    CapabilityValidationContext,
    validate_capability_framework,
)
from open_grace_governance.schemas.capability_framework import CapabilityFrameworkRecord
from open_grace_agent_registry import ModelRegistry
from open_grace_benchmarking import BenchmarkRegistry
from open_grace_governance.registries import RiskRegistry, StandardsRegistry


def _seed_context(tmp_path) -> CapabilityValidationContext:
    benchmarks = BenchmarkRegistry(tmp_path / "benchmarks.json")
    models = ModelRegistry(tmp_path / "models.json")
    standards = StandardsRegistry(tmp_path / "standards.json")
    risks = RiskRegistry(tmp_path / "risks.json")
    benchmarks.seed_from_yaml()
    models.seed_from_yaml()
    standards.seed_from_yaml()
    risks.seed_from_yaml()
    return CapabilityValidationContext(
        benchmarks=benchmarks,
        models=models,
        standards=standards,
        risks=risks,
    )


def test_capability_framework_passes_with_seeded_registries(tmp_path):
    framework = CapabilityFrameworkRegistry(tmp_path / "framework.json")
    framework.seed_from_yaml()
    context = _seed_context(tmp_path)

    for record in framework.list():
        result = validate_capability_framework(record, context)
        assert result.valid, result.errors


def test_capability_framework_rejects_unknown_benchmark(tmp_path):
    record = CapabilityFrameworkRecord(
        id="wise.capability.class.research",
        name="Research",
        description="Test",
        owner="test",
        benchmark_set=["wise.benchmark.missing"],
        risk_profile=["wise.risk.model-hallucination"],
        approved_models=["wise.model.gpt-4o"],
        required_standards=["wise.standard.cidoc-crm"],
        audit_requirements=["test"],
        reference_models=["unesco"],
    )
    context = _seed_context(tmp_path)
    result = validate_capability_framework(record, context)
    assert not result.valid
    assert any("unknown benchmark" in error for error in result.errors)
