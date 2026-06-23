"""JSON-backed runtime record stores."""

from __future__ import annotations

from pathlib import Path

from open_grace_governance.store.base import JsonRegistryStore
from open_grace_runtime.schemas import BenchmarkRunRecord, ExecutionRecord


class ExecutionRecordStore:
    def __init__(self, path: Path) -> None:
        self._store = JsonRegistryStore(path, ExecutionRecord, "run_id")

    def list(self) -> list[ExecutionRecord]:
        return self._store.all()

    def get(self, run_id: str) -> ExecutionRecord | None:
        return self._store.get(run_id)

    def for_agent(self, agent_id: str) -> list[ExecutionRecord]:
        return [record for record in self._store.all() if record.agent_id == agent_id]

    def save(self, record: ExecutionRecord) -> ExecutionRecord:
        self._store.upsert(record)
        self._store.save()
        return record


class BenchmarkRunRecordStore:
    def __init__(self, path: Path) -> None:
        self._store = JsonRegistryStore(path, BenchmarkRunRecord, "benchmark_run_id")
        self._path = path

    def list(self) -> list[BenchmarkRunRecord]:
        return self._store.all()

    def for_run(self, run_id: str) -> list[BenchmarkRunRecord]:
        return [record for record in self._store.all() if record.run_id == run_id]

    def for_agent_benchmark(self, agent_id: str, benchmark_id: str) -> list[BenchmarkRunRecord]:
        return [
            record
            for record in self._store.all()
            if record.agent_id == agent_id and record.benchmark_id == benchmark_id
        ]

    def has_passing_evaluation(self, agent_id: str, benchmark_id: str) -> bool:
        return any(
            record.passed
            for record in self.for_agent_benchmark(agent_id, benchmark_id)
        )

    def save_all(self, records: list[BenchmarkRunRecord]) -> list[BenchmarkRunRecord]:
        for record in records:
            self._store.upsert(record)
        self._store.save()
        return records
