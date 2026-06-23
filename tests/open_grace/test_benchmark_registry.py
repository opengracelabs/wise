from open_grace_benchmarking import BenchmarkRegistry, evaluate_benchmark


def test_seed_and_evaluate_benchmarks(tmp_path):
    registry = BenchmarkRegistry(tmp_path / "benchmarks.json")
    count = registry.seed_from_yaml()
    benchmarks = registry.for_agent("wise.agent.standards")

    assert count == 13
    assert benchmarks
    evaluation = evaluate_benchmark(benchmarks[0], 0.97)
    assert evaluation.passed is True

    failed = evaluate_benchmark(benchmarks[0], 0.50)
    assert failed.passed is False
