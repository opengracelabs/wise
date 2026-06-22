"""Deterministic scoring and tier classification for global assets."""

from __future__ import annotations

from collections.abc import Iterable, Mapping

from wise_global_ranking.models import (
    EntryEligibility,
    GlobalRankedAsset,
    GlobalRankingInput,
    RankingTier,
    TIER_CLASSIFICATIONS,
)

COMPONENT_KEYS = (
    "demand",
    "recognition",
    "emotional",
    "visual_impact",
    "historical_importance",
)

DEFAULT_WEIGHTS: dict[str, float] = {
    "demand": 0.35,
    "recognition": 0.20,
    "emotional": 0.15,
    "visual_impact": 0.15,
    "historical_importance": 0.15,
}

HIGH_DEMAND_THRESHOLD = 80.0
WIDELY_RECOGNIZED_THRESHOLD = 75.0
HISTORICALLY_IMPORTANT_THRESHOLD = 75.0
LOW_COMMERCIAL_DEMAND_THRESHOLD = 50.0


def component_scores(asset: GlobalRankingInput) -> dict[str, float]:
    """Return normalized 0-100 component scores for one asset."""

    return {
        "demand": asset.demand_score,
        "recognition": asset.recognition_score,
        "emotional": asset.emotional_score,
        "visual_impact": asset.visual_impact_score,
        "historical_importance": asset.historical_importance_score,
    }


def global_rank_score(
    asset: GlobalRankingInput,
    weights: Mapping[str, float] = DEFAULT_WEIGHTS,
) -> float:
    """Calculate the weighted global rank score on a 0-100 scale."""

    _validate_weights(weights)
    scores = component_scores(asset)
    weighted_score = sum(scores[key] * weights[key] for key in COMPONENT_KEYS)
    return round(weighted_score, 2)


def classify_asset(asset: GlobalRankingInput) -> RankingTier:
    """Classify one asset into the frozen Tier 1-4 ranking taxonomy."""

    if not asset.commercial_use and not asset.product_use:
        return RankingTier.TIER_4

    if (
        asset.is_unesco
        and asset.has_award_or_prize
        and asset.demand_score >= HIGH_DEMAND_THRESHOLD
    ):
        return RankingTier.TIER_1

    if (
        asset.historical_importance_score >= HISTORICALLY_IMPORTANT_THRESHOLD
        or asset.recognition_score >= WIDELY_RECOGNIZED_THRESHOLD
    ):
        return RankingTier.TIER_2

    if asset.educational_use or asset.demand_score < LOW_COMMERCIAL_DEMAND_THRESHOLD:
        return RankingTier.TIER_3

    return RankingTier.TIER_4


def eligibility_for_tier(tier: RankingTier) -> EntryEligibility:
    """Apply the Series, Products, and Marketplace tier gate."""

    allowed = tier in {RankingTier.TIER_1, RankingTier.TIER_2}
    return EntryEligibility(series=allowed, products=allowed, marketplace=allowed)


def rank_asset(asset: GlobalRankingInput, rank: int) -> GlobalRankedAsset:
    """Rank and classify one asset."""

    tier = classify_asset(asset)
    return GlobalRankedAsset(
        rank=rank,
        stable_id=asset.stable_id,
        title=asset.title,
        asset_type=asset.asset_type,
        global_rank_score=global_rank_score(asset),
        tier=tier,
        classification=TIER_CLASSIFICATIONS[tier],
        eligibility=eligibility_for_tier(tier),
        component_scores=component_scores(asset),
        recognition={
            "unesco_whc_id": asset.unesco_whc_id,
            "awards_prizes": list(asset.awards_prizes),
            "evidence_uris": list(asset.recognition_evidence_uris),
        },
        metadata=asset.metadata,
    )


def rank_assets(assets: Iterable[GlobalRankingInput]) -> list[GlobalRankedAsset]:
    """Rank assets globally, highest score first."""

    sorted_assets = sorted(
        assets,
        key=lambda asset: (-global_rank_score(asset), asset.stable_id),
    )
    return [rank_asset(asset, rank=index + 1) for index, asset in enumerate(sorted_assets)]


def build_global_ranking_output(
    assets: Iterable[GlobalRankingInput],
    *,
    ranking_version: str = "wise-global-ranking/0.1.0",
) -> dict:
    """Build the JSON-serializable global ranking artifact."""

    ranked_assets = rank_assets(assets)
    return {
        "ranking_version": ranking_version,
        "score_scale": "0-100",
        "weights": DEFAULT_WEIGHTS,
        "classification_rule": {
            "tier_1": "UNESCO + award/prize winners + high demand",
            "tier_2": "Historically important OR widely recognized",
            "tier_3": "Useful but low commercial demand",
            "tier_4": "No commercial or product use",
        },
        "eligibility_rule": "Only Tier 1-2 assets can enter Series, Products, and Marketplace.",
        "assets": [
            asset.model_dump(mode="json")
            for asset in ranked_assets
        ],
    }


def _validate_weights(weights: Mapping[str, float]) -> None:
    missing = set(COMPONENT_KEYS) - set(weights)
    if missing:
        raise ValueError(f"Missing global ranking weights: {sorted(missing)}")

    total = sum(weights[key] for key in COMPONENT_KEYS)
    if round(total, 6) != 1.0:
        raise ValueError(f"Global ranking weights must sum to 1.0, got {total}")
