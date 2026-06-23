"""Runtime system coordinator."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from open_grace_runtime.langgraph import build_runtime_graph, initial_runtime_state
from open_grace_runtime.schemas import ExecutionRecord, ExecutionStatus, GateResult
from open_grace_runtime.stores import BenchmarkRunRecordStore, ExecutionRecordStore

if TYPE_CHECKING:
    from open_grace_governance.system import GovernanceSystem


@dataclass
class AgentRunResult:
    run_id: str
    agent_id: str
    status: ExecutionStatus
    halted: bool
    gate_results: list[GateResult]
    model_id: str | None
    output_ref: str | None
    audit_id: str | None
    execution: ExecutionRecord | None


@dataclass
class RuntimeSystem:
    """Open Grace Agent Runtime v2 — gated LangGraph execution."""

    governance: GovernanceSystem
    executions: ExecutionRecordStore
    benchmark_runs: BenchmarkRunRecordStore
    _graph: object | None = None

    @classmethod
    def create(
        cls,
        governance: GovernanceSystem,
        root: Path | None = None,
    ) -> RuntimeSystem:
        base = root or governance.agents._store.path.parent / "runtime"
        base.mkdir(parents=True, exist_ok=True)
        return cls(
            governance=governance,
            executions=ExecutionRecordStore(base / "execution_records.json"),
            benchmark_runs=BenchmarkRunRecordStore(base / "benchmark_run_records.json"),
        )

    @property
    def graph(self):
        if self._graph is None:
            self._graph = build_runtime_graph(self)
        return self._graph

    def run_agent(
        self,
        agent_id: str,
        *,
        observed_values: dict[str, float] | None = None,
        preferred_model_id: str | None = None,
        steward_actor: str | None = None,
        run_id: str | None = None,
    ) -> AgentRunResult:
        state = initial_runtime_state(
            agent_id=agent_id,
            observed_values=observed_values,
            preferred_model_id=preferred_model_id,
            steward_actor=steward_actor,
            run_id=run_id,
        )
        final_state = self.graph.invoke(state)
        gate_results = [
            GateResult.model_validate(row) for row in final_state.get("gate_results", [])
        ]
        execution = self.executions.get(final_state["run_id"])
        return AgentRunResult(
            run_id=final_state["run_id"],
            agent_id=agent_id,
            status=ExecutionStatus(final_state["status"]),
            halted=final_state.get("halted", False),
            gate_results=gate_results,
            model_id=final_state.get("model_id"),
            output_ref=final_state.get("output_ref"),
            audit_id=final_state.get("audit_id"),
            execution=execution,
        )

    def summary(self) -> dict[str, int]:
        return {
            "executions": len(self.executions.list()),
            "benchmark_runs": len(self.benchmark_runs.list()),
        }
