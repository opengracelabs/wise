"""RC1 LangGraph state schema — Phase 1 orchestration wiring."""

from __future__ import annotations

from enum import StrEnum
from typing import Annotated, Any, TypedDict

from pydantic import BaseModel, Field

from wise_contracts.common import ApprovalStatus


class PipelineStage(StrEnum):
    """RC1 pipeline stages aligned with agent specs 09–13."""

    SOURCE_DISCOVERY = "source_discovery"
    PRESERVATION = "preservation"
    METADATA = "metadata"
    KNOWLEDGE_GRAPH = "knowledge_graph"
    QUALITY_REVIEW = "quality_review"
    COMPLETE = "complete"
    FAILED = "failed"
    DEAD_LETTER = "dead_letter"


class ErrorRecord(BaseModel):
    """Structured error captured during agent execution."""

    stage: PipelineStage
    code: str
    message: str
    retryable: bool = True


class BenchmarkReportRef(BaseModel):
    """Lightweight reference to a Benchmark Agent evaluation hook result."""

    agent_id: str
    stage: PipelineStage
    result: str  # pass | warn | fail | regression
    run_id: str
    scores: dict[str, float] = Field(default_factory=dict)


class StandardsReportRef(BaseModel):
    """Standards Agent compliance hook result (22-standards-agent §6.1)."""

    standard: str
    stage: PipelineStage
    scope: str
    adoption_level: str
    conformance_score: float
    passed: bool
    violations: list[str] = Field(default_factory=list)
    provenance_event_id: str | None = None


class ApprovalGateState(BaseModel):
    """Steward approval gate context (04-system-diagram §2.2)."""

    gate_id: str
    stage: PipelineStage
    status: ApprovalStatus = ApprovalStatus.PROPOSED
    steward_id: str | None = None
    rejection_reason: str | None = None
    artifact_key: str | None = None


def merge_provenance_chain(left: list[str], right: list[str]) -> list[str]:
    """Append provenance event IDs without duplication."""
    seen = set(left)
    merged = list(left)
    for event_id in right:
        if event_id not in seen:
            merged.append(event_id)
            seen.add(event_id)
    return merged


def merge_benchmark_reports(
    left: list[dict[str, Any]], right: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    return left + right


def merge_standards_reports(
    left: list[dict[str, Any]], right: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    return left + right


def merge_source_registry_refs(left: list[str], right: list[str]) -> list[str]:
    seen = set(left)
    merged = list(left)
    for ref in right:
        if ref not in seen:
            merged.append(ref)
            seen.add(ref)
    return merged


class RC1GraphState(TypedDict, total=False):
    """LangGraph state for Reference Capability 1 orchestration."""

    # Run identity (persisted to registry.agent_runs)
    orchestrator_run_id: str
    thread_id: str
    stable_id: str
    target_title: str

    # Pipeline position
    current_stage: str
    next_stage: str | None

    # Stage artifacts (wise-contracts payloads)
    discovery_record: dict[str, Any] | None
    preserved_object: dict[str, Any] | None
    premis_events: list[dict[str, Any]]
    metadata_record: dict[str, Any] | None
    entity_assertion: dict[str, Any] | None
    graph_entity: dict[str, Any] | None
    quality_review: dict[str, Any] | None

    # Provenance + evidence (03 §6.6)
    provenance_chain: Annotated[list[str], merge_provenance_chain]
    current_provenance_event_id: str | None
    source_registry_refs: Annotated[list[str], merge_source_registry_refs]
    evidence_profiles: dict[str, dict[str, Any]]

    # Governance hooks
    approval_gate: dict[str, Any] | None
    pending_interrupt: bool
    benchmark_reports: Annotated[list[dict[str, Any]], merge_benchmark_reports]
    standards_reports: Annotated[list[dict[str, Any]], merge_standards_reports]
    pipeline_benchmark_report: dict[str, Any] | None

    # Recovery
    errors: list[dict[str, Any]]
    retry_count: int
    max_retries: int
    dead_letter: bool
    steward_escalation: bool

    agent_versions: dict[str, str]


def initial_state_for_stonehenge(
    *,
    orchestrator_run_id: str | None = None,
    thread_id: str | None = None,
) -> RC1GraphState:
    """Return initial graph state for the Stonehenge RC1 target object."""
    return RC1GraphState(
        orchestrator_run_id=orchestrator_run_id or "",
        thread_id=thread_id or "",
        stable_id="stonehenge",
        target_title="Stonehenge",
        current_stage=PipelineStage.SOURCE_DISCOVERY.value,
        next_stage=PipelineStage.PRESERVATION.value,
        discovery_record=None,
        preserved_object=None,
        premis_events=[],
        metadata_record=None,
        entity_assertion=None,
        graph_entity=None,
        quality_review=None,
        approval_gate=None,
        pending_interrupt=False,
        provenance_chain=[],
        current_provenance_event_id=None,
        source_registry_refs=[],
        evidence_profiles={},
        errors=[],
        retry_count=0,
        max_retries=3,
        dead_letter=False,
        steward_escalation=False,
        benchmark_reports=[],
        standards_reports=[],
        pipeline_benchmark_report=None,
        agent_versions={
            "wise.agent.source-discovery": "0.1.0",
            "wise.agent.preservation": "0.1.0",
            "wise.agent.metadata": "0.1.0",
            "wise.agent.knowledge-graph": "0.1.0",
            "wise.agent.quality-review": "0.1.0",
        },
    )
