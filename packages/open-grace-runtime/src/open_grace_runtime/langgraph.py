"""LangGraph execution flow for Open Grace Agent Runtime v2.

Infrastructure wiring only — no LLM calls. The execute node records a stub result.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict
from uuid import uuid4

from langgraph.graph import END, START, StateGraph

from open_grace_governance.schemas.common import utc_now
from open_grace_runtime.gates import (
    select_approved_model,
    validate_agent_registry_gate,
    validate_benchmark_gate,
    validate_capability_gate,
    validate_knowledge_context,
    validate_risk_gate,
)
from open_grace_runtime.instrumentation import get_runtime_instrumentation
from open_grace_runtime.schemas import ExecutionStatus, GateResult

if TYPE_CHECKING:
    from open_grace_runtime.system import RuntimeSystem


class RuntimeState(TypedDict):
    run_id: str
    agent_id: str
    model_id: str | None
    capability_class_ids: list[str]
    observed_values: dict[str, float]
    gate_results: list[dict]
    halted: bool
    status: str
    output_ref: str | None
    audit_id: str | None
    benchmark_evaluations: list[dict]
    steward_actor: str | None
    preferred_model_id: str | None
    started_at: str
    completed_at: str | None


def _append_gate(state: RuntimeState, gate: GateResult) -> list[dict]:
    results = list(state.get("gate_results", []))
    results.append(gate.model_dump(mode="json"))
    return results


def _make_run_id(agent_id: str) -> str:
    slug = agent_id.rsplit(".", maxsplit=1)[-1]
    return f"wise.execution.{slug}-{uuid4().hex[:8]}"


def build_runtime_graph(runtime: RuntimeSystem):
    """Compile the gated agent execution graph."""
    instrumentation = get_runtime_instrumentation()

    def _instrumented(node_name: str, handler):
        def wrapped(state: RuntimeState) -> RuntimeState:
            with instrumentation.trace_node(
                node_name,
                agent_id=state["agent_id"],
                run_id=state["run_id"],
            ):
                return handler(state)

        wrapped.__name__ = node_name
        return wrapped

    def select_agent(state: RuntimeState) -> RuntimeState:
        if state.get("halted"):
            return state
        gate = validate_agent_registry_gate(runtime.governance.agents, state["agent_id"])
        knowledge_gate = validate_knowledge_context(runtime.governance, state["agent_id"])
        gate_results = _append_gate(state, gate)
        gate_results.append(knowledge_gate.model_dump(mode="json"))
        halted = not gate.passed or not knowledge_gate.passed
        errors = gate.errors + knowledge_gate.errors
        return {
            **state,
            "gate_results": gate_results,
            "halted": halted,
            "status": ExecutionStatus.BLOCKED.value if halted else ExecutionStatus.RUNNING.value,
        }

    def validate_capability(state: RuntimeState) -> RuntimeState:
        if state.get("halted"):
            return state
        gate = validate_capability_gate(runtime.governance, state["agent_id"])
        gate_results = _append_gate(state, gate)
        halted = not gate.passed
        return {
            **state,
            "gate_results": gate_results,
            "halted": halted,
            "status": ExecutionStatus.BLOCKED.value if halted else state["status"],
        }

    def validate_risk(state: RuntimeState) -> RuntimeState:
        if state.get("halted"):
            return state
        gate = validate_risk_gate(
            runtime.governance.capability_framework,
            runtime.governance.risks,
            state["agent_id"],
        )
        gate_results = _append_gate(state, gate)
        halted = not gate.passed
        return {
            **state,
            "gate_results": gate_results,
            "halted": halted,
            "status": ExecutionStatus.BLOCKED.value if halted else state["status"],
        }

    def select_model(state: RuntimeState) -> RuntimeState:
        if state.get("halted"):
            return state
        gate = validate_benchmark_gate(
            runtime.governance.capability_framework,
            runtime.governance.benchmarks,
            state["agent_id"],
            state.get("observed_values", {}),
            runtime.benchmark_runs,
        )
        gate_results = _append_gate(state, gate)
        if not gate.passed:
            return {
                **state,
                "gate_results": gate_results,
                "halted": True,
                "status": ExecutionStatus.BLOCKED.value,
            }

        model_id, class_ids = select_approved_model(
            runtime.governance.capability_framework,
            state["agent_id"],
            preferred_model_id=state.get("preferred_model_id"),
        )
        if model_id is None:
            model_gate = GateResult(
                gate_name="model_selection",
                passed=False,
                errors=["no approved model available for agent"],
            )
            return {
                **state,
                "gate_results": gate_results + [model_gate.model_dump(mode="json")],
                "halted": True,
                "status": ExecutionStatus.BLOCKED.value,
            }
        return {
            **state,
            "gate_results": gate_results,
            "model_id": model_id,
            "capability_class_ids": class_ids,
        }

    def execute(state: RuntimeState) -> RuntimeState:
        if state.get("halted"):
            return state
        run_id = state["run_id"]
        output_ref = f"stub://execution/{run_id}"
        runtime.governance.record_agent_metric(
            agent_id=state["agent_id"],
            metric_kind="latency",
            value=1.0,
            unit="ms",
            execution_id=run_id,
            steward_actor=state.get("steward_actor"),
        )
        return {
            **state,
            "output_ref": output_ref,
            "status": ExecutionStatus.RUNNING.value,
        }

    def evaluate(state: RuntimeState) -> RuntimeState:
        if state.get("halted"):
            return state
        from open_grace_governance.capabilities.benchmarking import evaluate_capability_benchmarks

        evaluations: list[dict] = []
        observed = state.get("observed_values", {})
        for class_id in state.get("capability_class_ids", []):
            record = runtime.governance.capability_framework.get(class_id)
            if record is None:
                continue
            result = evaluate_capability_benchmarks(
                record,
                runtime.governance.benchmarks,
                observed,
            )
            for evaluation in result.evaluations:
                evaluations.append(evaluation.__dict__)
                slug = evaluation.benchmark_id.rsplit(".", maxsplit=1)[-1]
                metric_id = f"wise.metric.benchmark.{slug}-observed-{uuid4().hex[:8]}"
                from open_grace_governance.lifecycle import LifecycleStage
                from open_grace_observability.schemas import BenchmarkMetric

                runtime.governance.observability.benchmark_metrics.record(
                    BenchmarkMetric(
                        metric_id=metric_id,
                        display_name=f"{evaluation.benchmark_id} observed",
                        benchmark_id=evaluation.benchmark_id,
                        agent_id=state["agent_id"],
                        metric_kind="observed",
                        observed_value=evaluation.observed_value,
                        unit="ratio",
                        passed=evaluation.passed,
                        trace_id=state["run_id"],
                        lifecycle_stage=LifecycleStage.AUDIT,
                        steward_actor=state.get("steward_actor"),
                        reference_models=["opentelemetry", "prometheus"],
                    )
                )
        return {**state, "benchmark_evaluations": evaluations}

    def audit(state: RuntimeState) -> RuntimeState:
        if state.get("halted"):
            return state
        from open_grace_audit import record_lifecycle_audit
        from open_grace_governance.lifecycle import LifecycleStage

        agent = runtime.governance.agents.get(state["agent_id"])
        from_stage = agent.lifecycle_stage if agent else LifecycleStage.PUBLICATION
        entry = record_lifecycle_audit(
            runtime.governance.audits,
            subject_type="agent",
            subject_id=state["agent_id"],
            from_stage=from_stage,
            to_stage=LifecycleStage.AUDIT,
            reviewer_id=state.get("steward_actor") or "open-grace-runtime",
            evidence_ref=f"runtime/{state['run_id']}",
            trace_id=state["run_id"],
            outcome="pass",
        )
        return {**state, "audit_id": entry.audit_id}

    def persist(state: RuntimeState) -> RuntimeState:
        from open_grace_runtime.schemas import BenchmarkRunRecord, ExecutionRecord

        completed_at = utc_now()
        gate_results = [GateResult.model_validate(row) for row in state.get("gate_results", [])]
        status = ExecutionStatus(state["status"])
        if not state.get("halted") and status == ExecutionStatus.RUNNING.value:
            status = ExecutionStatus.COMPLETED

        execution = ExecutionRecord(
            run_id=state["run_id"],
            agent_id=state["agent_id"],
            model_id=state.get("model_id"),
            capability_class_ids=state.get("capability_class_ids", []),
            status=status,
            started_at=state["started_at"],
            completed_at=completed_at,
            gate_results=gate_results,
            output_ref=state.get("output_ref"),
            audit_id=state.get("audit_id"),
        )
        runtime.executions.save(execution)

        benchmark_records: list[BenchmarkRunRecord] = []
        for class_id in state.get("capability_class_ids", []):
            for row in state.get("benchmark_evaluations", []):
                slug = row["benchmark_id"].rsplit(".", maxsplit=1)[-1]
                benchmark_records.append(
                    BenchmarkRunRecord(
                        benchmark_run_id=f"wise.benchmark-run.{slug}-{uuid4().hex[:8]}",
                        run_id=state["run_id"],
                        agent_id=state["agent_id"],
                        capability_class_id=class_id,
                        benchmark_id=row["benchmark_id"],
                        passed=row["passed"],
                        observed_value=row["observed_value"],
                        reason=row["reason"],
                    )
                )
        if benchmark_records:
            runtime.benchmark_runs.save_all(benchmark_records)

        return {
            **state,
            "status": status.value,
            "completed_at": completed_at.isoformat(),
        }

    graph = StateGraph(RuntimeState)
    graph.add_node("select_agent", _instrumented("select_agent", select_agent))
    graph.add_node("validate_capability", _instrumented("validate_capability", validate_capability))
    graph.add_node("validate_risk", _instrumented("validate_risk", validate_risk))
    graph.add_node("select_model", _instrumented("select_model", select_model))
    graph.add_node("execute", _instrumented("execute", execute))
    graph.add_node("evaluate", _instrumented("evaluate", evaluate))
    graph.add_node("audit", _instrumented("audit", audit))
    graph.add_node("persist", _instrumented("persist", persist))

    graph.add_edge(START, "select_agent")
    graph.add_edge("select_agent", "validate_capability")
    graph.add_edge("validate_capability", "validate_risk")
    graph.add_edge("validate_risk", "select_model")
    graph.add_edge("select_model", "execute")
    graph.add_edge("execute", "evaluate")
    graph.add_edge("evaluate", "audit")
    graph.add_edge("audit", "persist")
    graph.add_edge("persist", END)

    return graph.compile()


def initial_runtime_state(
    *,
    agent_id: str,
    observed_values: dict[str, float] | None = None,
    preferred_model_id: str | None = None,
    steward_actor: str | None = None,
    run_id: str | None = None,
) -> RuntimeState:
    rid = run_id or _make_run_id(agent_id)
    now = utc_now()
    return {
        "run_id": rid,
        "agent_id": agent_id,
        "model_id": None,
        "capability_class_ids": [],
        "observed_values": observed_values or {},
        "gate_results": [],
        "halted": False,
        "status": ExecutionStatus.PENDING.value,
        "output_ref": None,
        "audit_id": None,
        "benchmark_evaluations": [],
        "steward_actor": steward_actor,
        "preferred_model_id": preferred_model_id,
        "started_at": now.isoformat(),
        "completed_at": None,
    }
