from open_grace_governance.capabilities import CapabilityFrameworkRegistry, evaluate_capability_benchmarks
from open_grace_benchmarking import BenchmarkRegistry


def test_evaluate_capability_benchmark_set(tmp_path):
    framework = CapabilityFrameworkRegistry(tmp_path / "framework.json")
    benchmarks = BenchmarkRegistry(tmp_path / "benchmarks.json")
    framework.seed_from_yaml()
    benchmarks.seed_from_yaml()

    record = framework.get("wise.capability.class.translation")
    observed = {
        "wise.benchmark.translation-cost": 0.03,
        "wise.benchmark.translation-quality": 0.85,
    }
    result = evaluate_capability_benchmarks(record, benchmarks, observed)

    assert result.passed is True
    assert len(result.evaluations) == 2


def test_capability_benchmark_fails_on_missing_observation(tmp_path):
    framework = CapabilityFrameworkRegistry(tmp_path / "framework.json")
    benchmarks = BenchmarkRegistry(tmp_path / "benchmarks.json")
    framework.seed_from_yaml()
    benchmarks.seed_from_yaml()

    record = framework.get("wise.capability.class.publishing")
    result = evaluate_capability_benchmarks(record, benchmarks, {})

    assert result.passed is False
    assert result.failures
