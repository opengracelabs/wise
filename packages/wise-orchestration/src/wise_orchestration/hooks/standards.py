"""Standards Agent validation hook (22-standards-agent — read-only, pre-approval)."""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from wise_orchestration.state import PipelineStage, RC1GraphState, StandardsReportRef

REQUIRED_EVIDENCE_FIELDS = (
    "evidence_uris",
    "confidence",
    "evidence_summary",
    "method",
    "source_registry_refs",
    "provenance_event_id",
)


def _validate_evidence_profile(evidence: dict[str, Any] | None) -> list[str]:
    if not evidence:
        return ["Evidence Output Profile missing (03 §6.6)"]
    violations = []
    for field in REQUIRED_EVIDENCE_FIELDS:
        if field not in evidence or evidence[field] in (None, "", []):
            violations.append(f"Evidence Output Profile missing field: {field}")
    return violations


def _validate_discovery(state: RC1GraphState) -> StandardsReportRef:
    record = state.get("discovery_record") or {}
    violations: list[str] = []
    if not record.get("source_registry_ref"):
        violations.append("Discovery record missing source_registry_ref")
    if not record.get("rights_uri"):
        violations.append("Discovery record missing rights_uri")
    violations.extend(_validate_evidence_profile(record.get("evidence")))
    score = 100.0 if not violations else max(0.0, 100.0 - len(violations) * 20)
    return StandardsReportRef(
        standard="CIDOC-CRM",
        stage=PipelineStage.SOURCE_DISCOVERY,
        scope="discovery-record",
        adoption_level="Required",
        conformance_score=score,
        passed=not violations,
        violations=violations,
        provenance_event_id=record.get("evidence", {}).get("provenance_event_id"),
    )


def _validate_metadata(state: RC1GraphState) -> StandardsReportRef:
    assertion = state.get("entity_assertion") or {}
    violations = _validate_evidence_profile(assertion.get("evidence"))
    if not assertion.get("authority_links"):
        violations.append("Entity assertion missing authority_links (CIDOC-CRM binding)")
    score = 100.0 if not violations else max(0.0, 100.0 - len(violations) * 15)
    return StandardsReportRef(
        standard="CIDOC-CRM",
        stage=PipelineStage.METADATA,
        scope="entity-assertion",
        adoption_level="Required",
        conformance_score=score,
        passed=not violations,
        violations=violations,
        provenance_event_id=assertion.get("evidence", {}).get("provenance_event_id"),
    )


def _validate_graph(state: RC1GraphState) -> StandardsReportRef:
    entity = state.get("graph_entity") or {}
    violations: list[str] = []
    if not entity.get("entity_uri"):
        violations.append("Graph entity missing canonical entity_uri")
    links = entity.get("external_links") or []
    for link in links:
        violations.extend(_validate_evidence_profile(link.get("evidence")))
    score = 100.0 if not violations else max(0.0, 100.0 - len(violations) * 10)
    return StandardsReportRef(
        standard="Schema.org",
        stage=PipelineStage.KNOWLEDGE_GRAPH,
        scope="graph-entity",
        adoption_level="Recommended",
        conformance_score=score,
        passed=not violations,
        violations=violations,
        provenance_event_id=state.get("current_provenance_event_id"),
    )


def _validate_preservation(state: RC1GraphState) -> StandardsReportRef:
    obj = state.get("preserved_object") or {}
    violations: list[str] = []
    if not obj.get("ark"):
        violations.append("Preserved object missing ARK identifier")
    fixity = obj.get("fixity") or {}
    if fixity.get("result") != "pass":
        violations.append("PREMIS fixity check did not pass")
    score = 100.0 if not violations else max(0.0, 100.0 - len(violations) * 25)
    return StandardsReportRef(
        standard="PREMIS",
        stage=PipelineStage.PRESERVATION,
        scope="preserved-object",
        adoption_level="Required",
        conformance_score=score,
        passed=not violations,
        violations=violations,
        provenance_event_id=obj.get("provenance", {}).get("event_id"),
    )


def _validate_quality(state: RC1GraphState) -> StandardsReportRef:
    review = state.get("quality_review") or {}
    violations: list[str] = []
    if review.get("disposition") is not None:
        violations.append("Quality disposition must be null before steward approval")
    if review.get("composite_score", 0) < 0.85:
        violations.append("Composite quality score below institutional threshold")
    score = float(review.get("composite_score", 0) * 100)
    return StandardsReportRef(
        standard="CIDOC-CRM",
        stage=PipelineStage.QUALITY_REVIEW,
        scope="quality-review",
        adoption_level="Required",
        conformance_score=score,
        passed=not violations,
        violations=violations,
        provenance_event_id=review.get("provenance", {}).get("event_id"),
    )


_STAGE_VALIDATORS = {
    PipelineStage.SOURCE_DISCOVERY.value: _validate_discovery,
    PipelineStage.PRESERVATION.value: _validate_preservation,
    PipelineStage.METADATA.value: _validate_metadata,
    PipelineStage.KNOWLEDGE_GRAPH.value: _validate_graph,
    PipelineStage.QUALITY_REVIEW.value: _validate_quality,
}


def standards_validation_hook(state: RC1GraphState) -> dict[str, Any]:
    """Standards Agent hook — validates outputs before steward approval gate."""
    stage = state.get("current_stage", "")
    validator = _STAGE_VALIDATORS.get(stage)
    if validator is None:
        return {}
    report = validator(state)
    patch: dict[str, Any] = {
        "standards_reports": [report.model_dump(mode="json")],
    }
    if report.adoption_level == "Required" and not report.passed:
        patch["errors"] = [
            {
                "stage": stage,
                "code": "standards_violation",
                "message": "; ".join(report.violations) or "Required standard check failed",
                "retryable": False,
            }
        ]
    return patch


def standards_hook_node(state: RC1GraphState) -> dict[str, Any]:
    return standards_validation_hook(state)
