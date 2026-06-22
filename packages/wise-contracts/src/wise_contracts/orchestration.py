"""Orchestration and governance report contracts (architecture-v1.0 AI Fabric)."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class AgentPlane(StrEnum):
    PLATFORM = "platform"
    EXPERIENCE = "experience"
    CONSTITUTIONAL = "constitutional"


class AgentStatus(StrEnum):
    REGISTERED = "registered"
    CANDIDATE = "candidate"
    PRODUCTION = "production"
    SUSPENDED = "suspended"
    WITHDRAWN = "withdrawn"


class CapabilityRole(StrEnum):
    PRIMARY = "primary"
    SUPPORTING = "supporting"
    GOVERNANCE = "governance"


class RunStatus(StrEnum):
    RUNNING = "running"
    INTERRUPTED = "interrupted"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentRegistryEntry(BaseModel):
    """Canonical agent row exposed via orchestrator registry API."""

    agent_id: str
    spec_prefix: str
    spec_path: str
    display_name: str
    plane: AgentPlane
    build_phase: int | None
    service_binding: str | None
    langgraph_graph_id: str
    output_schema_uri: str
    evidence_profile: bool
    read_only: bool
    status: AgentStatus = AgentStatus.REGISTERED


class CapabilityRegistryEntry(BaseModel):
    """Platform or constitutional capability."""

    capability_id: str
    canonical_section: str
    display_name: str
    build_phase: int | None
    plane: AgentPlane
    contract_producer: str | None = None
    contract_consumer: str | None = None
    status: Literal["active", "deprecated"] = "active"


class CapabilityAgentLink(BaseModel):
    capability_id: str
    agent_id: str
    role: CapabilityRole


class StewardApprovalRequest(BaseModel):
    """Human approval gate input (04-system-diagram §2.2)."""

    thread_id: str
    decision: Literal["approved", "rejected"]
    reviewer_id: str
    notes: str | None = None


class RunStartRequest(BaseModel):
    graph_id: str
    agent_id: str
    input_ref: str | None = None
    trigger_source: Literal["n8n", "api", "manual", "pipeline"] = "api"


class RC1RunStartRequest(BaseModel):
    stable_id: str = "stonehenge"
    trigger_source: Literal["n8n", "api", "manual", "pipeline"] = "api"


class RC1RunResumeRequest(BaseModel):
    decision: Literal["approved", "rejected"]
    steward_id: str
    rejection_reason: str | None = None


class RunResumeRequest(BaseModel):
    decision: Literal["approved", "rejected"]
    reviewer_id: str
    notes: str | None = None


class AgentRunRecord(BaseModel):
    run_id: UUID
    agent_id: str
    agent_version: str
    graph_thread_id: str
    trigger_source: str
    input_ref: str | None = None
    output_ref: str | None = None
    status: RunStatus
    provenance_event_id: str | None = None
    started_at: datetime
    completed_at: datetime | None = None


class BenchmarkReport(BaseModel):
    """Benchmark Agent output (23-benchmark-agent.md §6.1) — read-only evidence."""

    agent_reference: str
    evaluation_domain: Literal["performance", "quality", "compliance", "composite"]
    result: Literal["pass", "warn", "fail", "regression"]
    scores: dict[str, float] = Field(default_factory=dict)
    findings: list[str] = Field(default_factory=list)
    provenance: dict[str, str] = Field(default_factory=dict)


class StandardsComplianceReport(BaseModel):
    """Standards Agent output (22-standards-agent.md §6.1) — read-only evidence."""

    standard: Literal["CIDOC-CRM", "Darwin-Core", "Schema.org"]
    scope: str
    adoption_level: Literal["Required", "Recommended"]
    conformance_score: float = Field(ge=0.0, le=100.0)
    passed: bool
    violations: list[str] = Field(default_factory=list)
    provenance: dict[str, str] = Field(default_factory=dict)
