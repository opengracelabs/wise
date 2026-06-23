"""Commercial appeal scoring for WISE assets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

COMMERCIAL_TIERS = (
    "Icon Product",
    "Strong Product",
    "Educational Product",
    "Archive Only",
)

VISUAL_TAGS = {
    "unesco_world_heritage",
    "national_geographic_award",
    "smithsonian_featured_collection",
    "wildlife_photographer_of_the_year",
    "major_photography_award",
    "pulitzer_prize",
}
EDUCATIONAL_TAGS = {
    "unesco_world_heritage",
    "nobel_related",
    "smithsonian_featured_collection",
    "pulitzer_prize",
}
TOURISM_TAGS = {
    "unesco_world_heritage",
    "national_geographic_award",
    "smithsonian_featured_collection",
}
GIFT_TAGS = {
    "unesco_world_heritage",
    "national_geographic_award",
    "wildlife_photographer_of_the_year",
    "major_photography_award",
}


@dataclass(frozen=True)
class CommercialBreakdown:
    """Component scores for commercial appeal."""

    visual_impact: int
    emotional_connection: int
    educational_demand: int
    tourism_interest: int
    giftability: int

    @property
    def total(self) -> int:
        """Return the 0-100 commercial appeal score."""

        return clamp_score(
            self.visual_impact
            + self.emotional_connection
            + self.educational_demand
            + self.tourism_interest
            + self.giftability,
            0,
            100,
        )


@dataclass(frozen=True)
class CommercialEvaluation:
    """Commercial scoring output for an asset."""

    recognition_score: int
    commercial_appeal_score: int
    final_selection_score: int
    commercial_tier: str
    breakdown: CommercialBreakdown

    def to_asset_fields(self) -> dict[str, Any]:
        """Return serializable fields to attach to an asset."""

        return {
            "recognition_score": self.recognition_score,
            "commercial_appeal_score": self.commercial_appeal_score,
            "final_selection_score": self.final_selection_score,
            "commercial_tier": self.commercial_tier,
            "commercial_breakdown": {
                "visual_impact": self.breakdown.visual_impact,
                "emotional_connection": self.breakdown.emotional_connection,
                "educational_demand": self.breakdown.educational_demand,
                "tourism_interest": self.breakdown.tourism_interest,
                "giftability": self.breakdown.giftability,
            },
        }


def clamp_score(value: float | int, lower: int, upper: int) -> int:
    """Clamp and round a score into an integer range."""

    return max(lower, min(upper, round(float(value))))


def normalize_award_tags(value: Any) -> set[str]:
    """Normalize award tags into a lowercase set."""

    if value is None:
        return set()
    if isinstance(value, str):
        values = [value]
    else:
        try:
            values = list(value)
        except TypeError:
            values = [value]
    return {str(tag).strip().lower() for tag in values if str(tag).strip()}


def _bool(asset: Mapping[str, Any], key: str) -> bool:
    return bool(asset.get(key))


def _optional_score(asset: Mapping[str, Any], key: str, upper: int) -> int | None:
    value = asset.get(key)
    if value is None:
        return None
    return clamp_score(value, 0, upper)


def _level(asset: Mapping[str, Any]) -> str:
    return str(asset.get("historical_significance_level", "unknown")).strip().lower()


def score_visual_impact(asset: Mapping[str, Any], award_tags: Iterable[str]) -> int:
    """Score visual product impact on a 0-25 scale."""

    explicit = _optional_score(asset, "visual_impact_score", 25)
    if explicit is not None:
        return explicit

    tags = set(award_tags)
    score = 0
    if tags & VISUAL_TAGS:
        score += 9
    if _bool(asset, "hero_image") or _bool(asset, "high_resolution_visual"):
        score += 7
    if _bool(asset, "visually_distinctive") or _bool(asset, "iconic_visual"):
        score += 6
    if _level(asset) in {"global", "high"}:
        score += 3
    return clamp_score(score, 0, 25)


def score_emotional_connection(asset: Mapping[str, Any], award_tags: Iterable[str]) -> int:
    """Score emotional connection on a 0-25 scale."""

    explicit = _optional_score(asset, "emotional_connection_score", 25)
    if explicit is not None:
        return explicit

    tags = set(award_tags)
    score = 0
    if _bool(asset, "human_story") or _bool(asset, "cultural_identity"):
        score += 8
    if _bool(asset, "endangered_species") or _bool(asset, "conservation_story"):
        score += 7
    if tags & {"pulitzer_prize", "wildlife_photographer_of_the_year", "nobel_related"}:
        score += 5
    if _level(asset) in {"global", "high", "moderate"}:
        score += 3
    if int(asset.get("recognition_score", 0) or 0) >= 85:
        score += 2
    return clamp_score(score, 0, 25)


def score_educational_demand(asset: Mapping[str, Any], award_tags: Iterable[str]) -> int:
    """Score educational demand on a 0-20 scale."""

    explicit = _optional_score(asset, "educational_demand_score", 20)
    if explicit is not None:
        return explicit

    tags = set(award_tags)
    score = 0
    if tags & EDUCATIONAL_TAGS:
        score += 7
    if _level(asset) in {"global", "high"}:
        score += 5
    if _bool(asset, "curriculum_relevance") or _bool(asset, "museum_learning_value"):
        score += 5
    if int(asset.get("recognition_score", 0) or 0) >= 80:
        score += 3
    return clamp_score(score, 0, 20)


def score_tourism_interest(asset: Mapping[str, Any], award_tags: Iterable[str]) -> int:
    """Score tourism interest on a 0-15 scale."""

    explicit = _optional_score(asset, "tourism_interest_score", 15)
    if explicit is not None:
        return explicit

    tags = set(award_tags)
    score = 0
    if tags & TOURISM_TAGS:
        score += 6
    if _bool(asset, "visitor_destination") or _bool(asset, "travel_interest"):
        score += 5
    if _level(asset) == "global":
        score += 3
    if int(asset.get("recognition_score", 0) or 0) >= 90:
        score += 1
    return clamp_score(score, 0, 15)


def score_giftability(asset: Mapping[str, Any], award_tags: Iterable[str]) -> int:
    """Score product giftability on a 0-15 scale."""

    explicit = _optional_score(asset, "giftability_score", 15)
    if explicit is not None:
        return explicit

    tags = set(award_tags)
    score = 0
    if tags & GIFT_TAGS:
        score += 5
    if _bool(asset, "decorative_fit") or _bool(asset, "broad_audience"):
        score += 5
    if _bool(asset, "seasonal_gift_fit") or _bool(asset, "collectible_fit"):
        score += 3
    if int(asset.get("recognition_score", 0) or 0) >= 80:
        score += 2
    return clamp_score(score, 0, 15)


def calculate_final_selection_score(recognition_score: int, commercial_appeal_score: int) -> int:
    """Blend recognition and commercial appeal without collapsing the two inputs."""

    return clamp_score((recognition_score * 0.40) + (commercial_appeal_score * 0.60), 0, 100)


def commercial_tier(final_selection_score: int, commercial_appeal_score: int, educational_demand: int) -> str:
    """Assign a commercial tier from selection and dimension scores."""

    if final_selection_score >= 85 and commercial_appeal_score >= 80:
        return "Icon Product"
    if final_selection_score >= 70 and commercial_appeal_score >= 65:
        return "Strong Product"
    if educational_demand >= 14 or final_selection_score >= 55:
        return "Educational Product"
    return "Archive Only"


def calculate_commercial_score(asset: Mapping[str, Any]) -> CommercialEvaluation:
    """Calculate commercial appeal, final selection score, and product tier."""

    recognition_score = clamp_score(asset.get("recognition_score", 0) or 0, 0, 100)
    award_tags = normalize_award_tags(asset.get("award_tags", ()))

    breakdown = CommercialBreakdown(
        visual_impact=score_visual_impact(asset, award_tags),
        emotional_connection=score_emotional_connection(asset, award_tags),
        educational_demand=score_educational_demand(asset, award_tags),
        tourism_interest=score_tourism_interest(asset, award_tags),
        giftability=score_giftability(asset, award_tags),
    )
    appeal_score = breakdown.total
    final_score = calculate_final_selection_score(recognition_score, appeal_score)

    return CommercialEvaluation(
        recognition_score=recognition_score,
        commercial_appeal_score=appeal_score,
        final_selection_score=final_score,
        commercial_tier=commercial_tier(final_score, appeal_score, breakdown.educational_demand),
        breakdown=breakdown,
    )
