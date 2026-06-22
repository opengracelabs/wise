"""Typed models for WISE portfolio intelligence."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CommercialTier(StrEnum):
    """Commercial tier assigned by global ranking."""

    TIER_1 = "Tier 1"
    TIER_2 = "Tier 2"
    TIER_3 = "Tier 3"
    TIER_4 = "Tier 4"


class PortfolioKind(StrEnum):
    """Portfolio outputs produced by the optimizer."""

    HOMEPAGE = "homepage"
    COLLECTION = "collection"
    SERIES = "series"
    PRODUCT = "product"


NARRATIVE_CATEGORIES: tuple[str, ...] = (
    "Heritage",
    "Biodiversity",
    "Geography",
    "Culture",
    "Climate",
)


class PortfolioAssetInput(BaseModel):
    """Input asset available for portfolio curation."""

    model_config = ConfigDict(frozen=True)

    stable_id: str = Field(min_length=1, max_length=160)
    title: str = Field(min_length=1, max_length=512)
    global_rank_score: float = Field(ge=0.0, le=100.0)
    recognition_score: float = Field(ge=0.0, le=100.0)
    demand_score: float = Field(ge=0.0, le=100.0)
    commercial_tier: CommercialTier
    asset_type: str = Field(min_length=1, max_length=128)
    category: str = Field(min_length=1, max_length=128)
    geography: str = Field(min_length=1, max_length=128)
    domain: str | None = Field(default=None, max_length=128)

    @field_validator("global_rank_score", "recognition_score", "demand_score", mode="before")
    @classmethod
    def normalize_score(cls, value: float) -> float:
        """Accept either 0-1 normalized scores or already scaled 0-100 scores."""

        score = float(value)
        if 0.0 <= score <= 1.0:
            score *= 100.0
        return round(score, 2)

    @property
    def diversity_domain(self) -> str:
        return self.domain or self.category


class PortfolioSpec(BaseModel):
    """Configuration for one portfolio output."""

    model_config = ConfigDict(frozen=True)

    kind: PortfolioKind
    output_file: str
    title: str
    target_size: int = Field(default=5, ge=1)
    required_categories: tuple[str, ...] = NARRATIVE_CATEGORIES
    allowed_commercial_tiers: tuple[CommercialTier, ...] = (
        CommercialTier.TIER_1,
        CommercialTier.TIER_2,
        CommercialTier.TIER_3,
        CommercialTier.TIER_4,
    )


class PortfolioSelection(BaseModel):
    """One selected asset in a portfolio."""

    portfolio_rank: int = Field(ge=1)
    stable_id: str
    title: str
    global_rank_score: float = Field(ge=0.0, le=100.0)
    recognition_score: float = Field(ge=0.0, le=100.0)
    demand_score: float = Field(ge=0.0, le=100.0)
    stabilized_selection_score: float = Field(ge=0.0, le=100.0)
    commercial_tier: CommercialTier
    asset_type: str
    category: str
    domain: str
    geography: str
    why_this_asset_was_selected: str


class PortfolioOutput(BaseModel):
    """Structured optimizer output for one portfolio."""

    portfolio_type: PortfolioKind
    title: str
    output_file: str
    target_size: int
    diversity_constraints: dict[str, float]
    narrative_balance: dict[str, int]
    ranking_stabilization: str
    assets: list[PortfolioSelection]
