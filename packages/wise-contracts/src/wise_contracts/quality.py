"""Quality Review contracts (13-quality-review-agent §6)."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from wise_contracts.common import ApprovalStatus, ProvenanceRef


class QualityDimensionScore(BaseModel):
    """Per-dimension quality score."""

    dimension: str
    score: float = Field(ge=0.0, le=1.0)
    threshold: float = Field(ge=0.0, le=1.0)
    passed: bool


class QualityReviewRecord(BaseModel):
    """Quality Review Record (13-quality-review-agent §6.2)."""

    id: str
    status: ApprovalStatus = ApprovalStatus.PROPOSED
    entity_uri: str
    preservation_ark: str
    review_domain: str
    severity: str
    finding: str
    recommended_action: str
    composite_score: float = Field(ge=0.0, le=1.0)
    dimension_scores: list[QualityDimensionScore] = Field(default_factory=list)
    disposition: str | None = None
    provenance: ProvenanceRef
    reviewed_at: datetime
