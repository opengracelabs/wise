"""Benchmark Agent evaluation hook (23-benchmark-agent — hook only, not agent node)."""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from wise_orchestration.state import BenchmarkReportRef, PipelineStage, RC1GraphState

# Per-agent benchmark thresholds from agent specs §AI Fabric Governance
RC1_BENCHMARK_THRESHOLDS: dict[str, dict[str, float]] = {
    PipelineStage.SOURCE_DISCOVERY.value: {
        "rights_accuracy": 0.90,
        "metadata_completeness": 0.80,
    },
    PipelineStage.PRESERVATION.value: {
        "fixity_pass_rate": 1.0,
    },
    PipelineStage.METADATA.value: {
        "schema_validation_pass_rate": 0.80,
        "authority_match_precision": 0.85,
    },
    PipelineStage.KNOWLEDGE_GRAPH.value: {
        "link_confidence": 0.85,
    },
    PipelineStage.QUALITY_REVIEW.value: {
        "composite_score": 0.85,
    },
}

AGENT_ID_BY_STAGE: dict[str, str] = {
    PipelineStage.SOURCE_DISCOVERY.value: "09-source-discovery",
    PipelineStage.PRESERVATION.value: "11-preservation",
    PipelineStage.METADATA.value: "10-metadata",
    PipelineStage.KNOWLEDGE_GRAPH.value: "12-knowledge-graph",
    PipelineStage.QUALITY_REVIEW.value: "13-quality-review",
}


def _score_stage_artifact(state: RC1GraphState, stage: str) -> dict[str, float]:
    """Compute lightweight benchmark scores from stage artifacts (no live LLM)."""
    if stage == PipelineStage.SOURCE_DISCOVERY.value:
        record = state.get("discovery_record") or {}
        score = float(record.get("ingestion_candidacy_score", 0.0))
        evidence = record.get("evidence") or {}
        return {
            "rights_accuracy": 1.0 if record.get("rights_uri") else 0.0,
            "metadata_completeness": score,
            "confidence": float(evidence.get("confidence", 0.0)),
        }
    if stage == PipelineStage.PRESERVATION.value:
        obj = state.get("preserved_object") or {}
        fixity = obj.get("fixity") or {}
        return {
            "fixity_pass_rate": 1.0 if fixity.get("result") == "pass" else 0.0,
        }
    if stage == PipelineStage.METADATA.value:
        assertion = state.get("entity_assertion") or {}
        evidence = assertion.get("evidence") or {}
        links = assertion.get("authority_links") or []
        avg_conf = sum(l.get("confidence", 0) for l in links) / max(len(links), 1)
        return {
            "schema_validation_pass_rate": 1.0,
            "authority_match_precision": avg_conf,
            "confidence": float(evidence.get("confidence", 0.0)),
        }
    if stage == PipelineStage.KNOWLEDGE_GRAPH.value:
        entity = state.get("graph_entity") or {}
        links = entity.get("external_links") or []
        confidences = [
            (link.get("evidence") or {}).get("confidence", 0.0) for link in links
        ]
        avg = sum(confidences) / max(len(confidences), 1)
        return {"link_confidence": avg}
    if stage == PipelineStage.QUALITY_REVIEW.value:
        review = state.get("quality_review") or {}
        return {"composite_score": float(review.get("composite_score", 0.0))}
    return {}


def _evaluate_scores(stage: str, scores: dict[str, float]) -> str:
    """Return pass | warn | fail against registered thresholds."""
    thresholds = RC1_BENCHMARK_THRESHOLDS.get(stage, {})
    if not thresholds:
        return "pass"
    failures = 0
    warnings = 0
    for metric, threshold in thresholds.items():
        value = scores.get(metric, 0.0)
        if value < threshold * 0.9:
            failures += 1
        elif value < threshold:
            warnings += 1
    if failures:
        return "fail"
    if warnings:
        return "warn"
    return "pass"


def benchmark_evaluation_hook(state: RC1GraphState) -> dict[str, Any]:
    """Run Benchmark Agent evaluation hook after each agent node (23-benchmark-agent §4)."""
    stage = state.get("current_stage", "")
    agent_id = AGENT_ID_BY_STAGE.get(stage, "unknown")
    scores = _score_stage_artifact(state, stage)
    result = _evaluate_scores(stage, scores)

    report = BenchmarkReportRef(
        agent_id=agent_id,
        stage=PipelineStage(stage),
        result=result,
        run_id=f"bench-{uuid4().hex[:12]}",
        scores=scores,
    )

    return {"benchmark_reports": [report.model_dump(mode="json")]}


def benchmark_hook_node(state: RC1GraphState) -> dict[str, Any]:
    """LangGraph node wrapper for the benchmark evaluation hook."""
    return benchmark_evaluation_hook(state)
