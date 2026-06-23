"""Shared schema primitives for governed registry entries."""

from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import Annotated

from pydantic import BaseModel, Field, field_validator

from open_grace_governance.lifecycle import LifecycleStage

WISE_AGENT_ID = re.compile(r"^wise\.agent\.[a-z0-9]+(?:-[a-z0-9]+)*$")
WISE_CAPABILITY_ID = re.compile(r"^wise\.capability\.[a-z0-9]+(?:-[a-z0-9]+)*$")
WISE_STANDARD_ID = re.compile(r"^wise\.standard\.[a-z0-9]+(?:-[a-z0-9]+)*$")
WISE_RISK_ID = re.compile(r"^wise\.risk\.[a-z0-9]+(?:-[a-z0-9]+)*$")
WISE_BENCHMARK_ID = re.compile(r"^wise\.benchmark\.[a-z0-9]+(?:-[a-z0-9]+)*$")
WISE_AUDIT_ID = re.compile(r"^wise\.audit\.[a-z0-9]+(?:-[a-z0-9]+)*$")
WISE_MODEL_ID = re.compile(r"^wise\.model\.[a-z0-9]+(?:-[a-z0-9]+)*$")


def utc_now() -> datetime:
    return datetime.now(UTC)


class GovernedRecord(BaseModel):
    """Base record with lifecycle and provenance metadata."""

    lifecycle_stage: LifecycleStage = LifecycleStage.PROPOSAL
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    steward_actor: str | None = None
    reference_models: list[str] = Field(default_factory=list)

    def touch(self, *, steward_actor: str | None = None) -> None:
        self.updated_at = utc_now()
        if steward_actor is not None:
            self.steward_actor = steward_actor


AgentPlane = Annotated[str, Field(pattern=r"^(platform|experience|constitutional)$")]
CapabilityRole = Annotated[str, Field(pattern=r"^(primary|supporting|governance)$")]
RiskSeverity = Annotated[str, Field(pattern=r"^(low|medium|high|critical)$")]
MitRiskDomain = Annotated[
    str,
    Field(
        pattern=r"^(discrimination-toxicity|privacy-security|misinformation|"
        r"malicious-actors|human-computer-interaction|socioeconomic-environmental|"
        r"ai-system-safety)$"
    ),
]
MitHarmType = Annotated[
    str,
    Field(
        pattern=r"^(psychological|physical|financial|reputational|environmental|"
        r"rights-violation|societal)$"
    ),
]
MitAffectedParty = Annotated[
    str,
    Field(
        pattern=r"^(individual|group|society|organization|ecosystem|"
        r"marginalized-population)$"
    ),
]
MitCausalSource = Annotated[
    str,
    Field(pattern=r"^(human|ai-system|third-party|organizational|environmental)$")
]
MitRiskIntent = Annotated[str, Field(pattern=r"^(intentional|unintentional|unknown)$")]
MitRiskTiming = Annotated[
    str,
    Field(pattern=r"^(pre-deployment|post-deployment|runtime|both)$")
]
BenchmarkMetric = Annotated[str, Field(pattern=r"^(accuracy|cost|latency|safety|reliability)$")]

_SEVERITY_ORDINAL = {"low": 0, "medium": 1, "high": 2, "critical": 3}
