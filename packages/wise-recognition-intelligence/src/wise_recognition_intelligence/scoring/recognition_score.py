"""Composite recognition scoring for WISE assets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from wise_recognition_intelligence.awards import (
    AwardSignal,
    detect_nobel_related,
    detect_photography_awards,
    detect_pulitzer,
    detect_unesco_world_heritage,
    detect_wildlife_conservation_awards,
)
from wise_recognition_intelligence.scoring.citation_index_score import build_citation_index
from wise_recognition_intelligence.scoring.historical_importance_score import (
    clamp_score,
    infer_historical_significance_level,
    score_historical_importance,
)

ELIGIBILITY_THRESHOLD = 70


@dataclass(frozen=True)
class RecognitionBreakdown:
    """Component scores for the 40/30/20/10 recognition model."""

    awards_weight: int
    historical_importance: int
    citation_volume: int
    cultural_impact: int

    @property
    def total(self) -> int:
        """Return the capped recognition score."""

        return clamp_score(
            self.awards_weight + self.historical_importance + self.citation_volume + self.cultural_impact,
            0,
            100,
        )


@dataclass(frozen=True)
class RecognitionEvaluation:
    """Recognition scoring output required before collection or product inclusion."""

    recognition_score: int
    award_tags: tuple[str, ...]
    historical_significance_level: str
    citation_index: dict[str, int | str]
    global_rank_bucket: str
    eligible: bool
    breakdown: RecognitionBreakdown

    def to_asset_fields(self) -> dict[str, Any]:
        """Return serializable fields to attach to an asset."""

        return {
            "recognition_score": self.recognition_score,
            "award_tags": list(self.award_tags),
            "historical_significance_level": self.historical_significance_level,
            "citation_index": self.citation_index,
            "global_rank_bucket": self.global_rank_bucket,
            "eligible_for_collections": self.eligible,
            "eligible_for_series": self.eligible,
            "eligible_for_commercial_products": self.eligible,
            "recognition_breakdown": {
                "awards_weight": self.breakdown.awards_weight,
                "historical_importance": self.breakdown.historical_importance,
                "citation_volume": self.breakdown.citation_volume,
                "cultural_impact": self.breakdown.cultural_impact,
            },
        }


def detect_award_signals(asset: Mapping[str, Any]) -> list[AwardSignal]:
    """Run all configured award detectors for an asset."""

    signals: list[AwardSignal] = []
    for detector in (
        detect_unesco_world_heritage,
        detect_nobel_related,
        detect_pulitzer,
        detect_wildlife_conservation_awards,
        detect_photography_awards,
    ):
        signals.extend(detector(asset))

    deduplicated: dict[str, AwardSignal] = {}
    for signal in signals:
        existing = deduplicated.get(signal.tag)
        if existing is None or signal.weight > existing.weight:
            deduplicated[signal.tag] = signal
    return list(deduplicated.values())


def score_awards_weight(signals: Iterable[AwardSignal]) -> int:
    """Score awards on a capped 0-40 scale."""

    weighted_total = sum(round(signal.weight * signal.confidence) for signal in signals)
    return clamp_score(weighted_total, 0, 40)


def score_cultural_impact(asset: Mapping[str, Any], award_tags: Iterable[str]) -> int:
    """Score cultural impact on a 0-10 scale."""

    explicit_score = asset.get("cultural_impact_score")
    if explicit_score is not None:
        return clamp_score(explicit_score, 0, 10)

    tags = set(award_tags)
    score = 0
    if "smithsonian_featured_collection" in tags:
        score += 5
    if "national_geographic_award" in tags:
        score += 4
    if "pulitzer_prize" in tags:
        score += 4
    if "unesco_world_heritage" in tags:
        score += 3
    if asset.get("editorial_selection") or asset.get("featured_collection"):
        score += 3
    if int(asset.get("wikipedia_pageviews", 0) or 0) >= 500_000:
        score += 2

    return clamp_score(score, 0, 10)


def calculate_recognition_score(asset: Mapping[str, Any]) -> RecognitionEvaluation:
    """Calculate recognition score and inclusion eligibility for an asset."""

    from wise_recognition_intelligence.ranking.global_importance_ranker import global_rank_bucket

    award_signals = detect_award_signals(asset)
    award_tags = tuple(sorted(signal.tag for signal in award_signals))
    awards_weight = score_awards_weight(award_signals)
    historical_importance = score_historical_importance(asset, award_tags)
    citation_index = build_citation_index(asset)
    cultural_impact = score_cultural_impact(asset, award_tags)

    breakdown = RecognitionBreakdown(
        awards_weight=awards_weight,
        historical_importance=historical_importance,
        citation_volume=int(citation_index["score"]),
        cultural_impact=cultural_impact,
    )
    recognition_score = breakdown.total

    return RecognitionEvaluation(
        recognition_score=recognition_score,
        award_tags=award_tags,
        historical_significance_level=infer_historical_significance_level(historical_importance),
        citation_index=citation_index,
        global_rank_bucket=global_rank_bucket(recognition_score),
        eligible=recognition_score >= ELIGIBILITY_THRESHOLD,
        breakdown=breakdown,
    )
