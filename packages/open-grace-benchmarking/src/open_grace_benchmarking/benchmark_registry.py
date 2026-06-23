"""Benchmark registry and evaluation gate."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from open_grace_governance.lifecycle import LifecycleStage, advance_lifecycle
from open_grace_governance.schemas import BenchmarkRegistryRecord
from open_grace_governance.store.base import JsonRegistryStore
from open_grace_governance.validation import validate_entry

_PACKAGE_DATA = Path(__file__).resolve().parent / "data"


@dataclass(frozen=True)
class BenchmarkEvaluation:
    benchmark_id: str
    agent_id: str
    metric: str
    observed_value: float
    passed: bool
    reason: str


class BenchmarkRegistry:
    def __init__(self, store_path: Path | None = None) -> None:
        self._store = JsonRegistryStore(
            store_path or _PACKAGE_DATA / "benchmark_registry.json",
            BenchmarkRegistryRecord,
            "benchmark_id",
        )

    def seed_from_yaml(self, path: Path | None = None) -> int:
        seed_path = path or _PACKAGE_DATA / "seed" / "benchmark_registry.yaml"
        if not seed_path.is_file():
            return 0
        data = yaml.safe_load(seed_path.read_text(encoding="utf-8"))
        count = 0
        for row in data.get("benchmarks", []):
            record = BenchmarkRegistryRecord.model_validate(row)
            result = validate_entry(record)
            if not result.valid:
                raise ValueError(f"invalid benchmark seed {row}: {result.errors}")
            self._store.upsert(record)
            count += 1
        self._store.save()
        return count

    def list(self) -> list[BenchmarkRegistryRecord]:
        return self._store.all()

    def for_agent(self, agent_id: str) -> list[BenchmarkRegistryRecord]:
        return [record for record in self._store.all() if record.agent_id == agent_id]

    def get(self, benchmark_id: str) -> BenchmarkRegistryRecord | None:
        return self._store.get(benchmark_id)

    def register(self, record: BenchmarkRegistryRecord) -> BenchmarkRegistryRecord:
        result = validate_entry(record)
        if not result.valid:
            raise ValueError("; ".join(result.errors))
        self._store.upsert(record)
        self._store.save()
        return record

    def advance(
        self,
        benchmark_id: str,
        target: LifecycleStage,
        *,
        steward_actor: str | None = None,
    ) -> BenchmarkRegistryRecord:
        record = self._store.get(benchmark_id)
        if record is None:
            raise KeyError(benchmark_id)
        record.lifecycle_stage = advance_lifecycle(record.lifecycle_stage, target)
        record.touch(steward_actor=steward_actor)
        self._store.upsert(record)
        self._store.save()
        return record


def evaluate_benchmark(
    record: BenchmarkRegistryRecord,
    observed_value: float,
) -> BenchmarkEvaluation:
    """Evaluate an observed metric against registry thresholds."""
    passed = True
    reasons: list[str] = []

    if record.threshold_min is not None and observed_value < record.threshold_min:
        passed = False
        reasons.append(f"below min {record.threshold_min}")
    if record.threshold_max is not None and observed_value > record.threshold_max:
        passed = False
        reasons.append(f"above max {record.threshold_max}")

    return BenchmarkEvaluation(
        benchmark_id=record.benchmark_id,
        agent_id=record.agent_id,
        metric=record.metric,
        observed_value=observed_value,
        passed=passed,
        reason="; ".join(reasons) if reasons else "within thresholds",
    )
