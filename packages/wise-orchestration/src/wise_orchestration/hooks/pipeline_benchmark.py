"""Pipeline-level Benchmark Agent evaluation after RC1 completion."""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from wise_contracts.orchestration import BenchmarkReport
from wise_orchestration.state import PipelineStage, RC1GraphState


def evaluate_completed_pipeline(state: RC1GraphState) -> dict[str, Any]:
    """Benchmark Agent composite evaluation for a completed RC1 run (23-benchmark-agent §5)."""
    stage_reports = state.get("benchmark_reports") or []
    failures = sum(1 for r in stage_reports if r.get("result") == "fail")
    warnings = sum(1 for r in stage_reports if r.get("result") == "warn")
    provenance_len = len(state.get("provenance_chain") or [])
    standards_reports = state.get("standards_reports") or []
    standards_failures = sum(
        1 for r in standards_reports if r.get("adoption_level") == "Required" and not r.get("passed")
    )

    scores = {
        "stage_benchmark_pass_rate": (len(stage_reports) - failures - warnings) / max(len(stage_reports), 1),
        "provenance_chain_length": float(provenance_len),
        "standards_required_pass_rate": (len(standards_reports) - standards_failures) / max(
            len(standards_reports), 1
        ),
    }

    if failures or standards_failures:
        result = "fail"
    elif warnings:
        result = "warn"
    else:
        result = "pass"

    report = BenchmarkReport(
        agent_reference="wise.agent.benchmark",
        evaluation_domain="composite",
        result=result,
        scores=scores,
        findings=[] if result == "pass" else ["RC1 pipeline composite benchmark did not pass"],
        provenance={
            "benchmark_run_id": f"bench-pipeline-{uuid4().hex[:12]}",
            "orchestrator_run_id": state.get("orchestrator_run_id", ""),
            "stable_id": state.get("stable_id", ""),
        },
    )
    return {"pipeline_benchmark_report": report.model_dump(mode="json")}


def pipeline_benchmark_node(state: RC1GraphState) -> dict[str, Any]:
    if state.get("current_stage") != PipelineStage.COMPLETE.value:
        return {}
    return evaluate_completed_pipeline(state)
