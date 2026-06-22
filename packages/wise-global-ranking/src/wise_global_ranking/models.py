"""Typed models for WISE global asset ranking."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class RankingTier(StrEnum):
    """Commercial ranking tiers for global assets."""

    TIER_1 = "Tier 1"
    TIER_2 = "Tier 2"
    TIER_3 = "Tier 3"
    TIER_4 = "Tier 4"


TIER_CLASSIFICATIONS: dict[RankingTier, str] = {
    RankingTier.TIER_1: "ICONIC GLOBAL HERITAGE",
    RankingTier.TIER_2: "HIGH CULTURAL VALUE",
    RankingTier.TIER_3: "EDUCATIONAL VALUE",
    RankingTier.TIER_4: "ARCHIVAL ONLY",
}


class EntryEligibility(BaseModel):
    """Destinations gated by ranking tier."""

    series: bool
    products: bool
    marketplace: bool


class GlobalRankingInput(BaseModel):
    """Input metrics required to rank one global asset."""

    model_config = ConfigDict(frozen=True)

    stable_id: str = Field(min_length=1, max_length=160)
    title: str = Field(min_length=1, max_length=512)
    asset_type: str = Field(min_length=1, max_length=128)
    demand_score: float = Field(ge=0.0, le=100.0)
    recognition_score: float = Field(ge=0.0, le=100.0)
    emotional_score: float = Field(ge=0.0, le=100.0)
    visual_impact_score: float = Field(ge=0.0, le=100.0)
    historical_importance_score: float = Field(ge=0.0, le=100.0)
    unesco_whc_id: str | None = None
    awards_prizes: tuple[str, ...] = ()
    recognition_evidence_uris: tuple[str, ...] = ()
    educational_use: bool = True
    commercial_use: bool = True
    product_use: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator(
        "demand_score",
        "recognition_score",
        "emotional_score",
        "visual_impact_score",
        "historical_importance_score",
        mode="before",
    )
    @classmethod
    def normalize_score(cls, value: float) -> float:
        """Accept either 0-1 normalized scores or already scaled 0-100 scores."""

        score = float(value)
        if 0.0 <= score <= 1.0:
            score *= 100.0
        return round(score, 2)

    @property
    def is_unesco(self) -> bool:
        return self.unesco_whc_id is not None

    @property
    def has_award_or_prize(self) -> bool:
        return len(self.awards_prizes) > 0


class GlobalRankedAsset(BaseModel):
    """Ranked asset output written to global_ranked_assets.json."""

    rank: int = Field(ge=1)
    stable_id: str
    title: str
    asset_type: str
    global_rank_score: float = Field(ge=0.0, le=100.0)
    tier: RankingTier
    classification: str
    eligibility: EntryEligibility
    component_scores: dict[str, float]
    recognition: dict[str, Any]
    metadata: dict[str, Any] = Field(default_factory=dict)
