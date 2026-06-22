"""Portfolio optimizer for globally ranked WISE assets."""

from __future__ import annotations

import math
from collections import Counter
from collections.abc import Iterable, Mapping

from wise_portfolio_intelligence.models import (
    CommercialTier,
    NARRATIVE_CATEGORIES,
    PortfolioAssetInput,
    PortfolioKind,
    PortfolioOutput,
    PortfolioSelection,
    PortfolioSpec,
)

DIVERSITY_LIMIT = 0.20
SCORE_STABILITY_BAND = 5.0

DEFAULT_DIVERSITY_CONSTRAINTS: dict[str, float] = {
    "domain": DIVERSITY_LIMIT,
    "geography": DIVERSITY_LIMIT,
    "asset_type": DIVERSITY_LIMIT,
}

DEFAULT_PORTFOLIO_SPECS: tuple[PortfolioSpec, ...] = (
    PortfolioSpec(
        kind=PortfolioKind.HOMEPAGE,
        output_file="homepage_portfolio.json",
        title="Homepage Global Portfolio",
        target_size=5,
    ),
    PortfolioSpec(
        kind=PortfolioKind.COLLECTION,
        output_file="collection_portfolio.json",
        title="Balanced Collection Portfolio",
        target_size=5,
    ),
    PortfolioSpec(
        kind=PortfolioKind.SERIES,
        output_file="series_portfolio.json",
        title="Narrative Series Portfolio",
        target_size=5,
    ),
    PortfolioSpec(
        kind=PortfolioKind.PRODUCT,
        output_file="product_portfolio.json",
        title="Product-Ready Portfolio",
        target_size=5,
        allowed_commercial_tiers=(CommercialTier.TIER_1, CommercialTier.TIER_2),
    ),
)

TIER_PRIORITY: dict[CommercialTier, int] = {
    CommercialTier.TIER_1: 1,
    CommercialTier.TIER_2: 2,
    CommercialTier.TIER_3: 3,
    CommercialTier.TIER_4: 4,
}


def portfolio_optimizer(
    assets: Iterable[PortfolioAssetInput],
    *,
    portfolio_specs: Iterable[PortfolioSpec] = DEFAULT_PORTFOLIO_SPECS,
    diversity_constraints: Mapping[str, float] = DEFAULT_DIVERSITY_CONSTRAINTS,
) -> dict[str, PortfolioOutput]:
    """Create balanced homepage, collection, series, and product portfolios."""

    asset_list = list(assets)
    if not asset_list:
        raise ValueError("portfolio_optimizer requires at least one asset")

    outputs: dict[str, PortfolioOutput] = {}
    for spec in portfolio_specs:
        outputs[spec.output_file] = _build_portfolio(
            asset_list,
            spec=spec,
            diversity_constraints=diversity_constraints,
        )
    return outputs


def serialize_portfolios(portfolios: Mapping[str, PortfolioOutput]) -> dict[str, dict]:
    """Convert portfolio outputs to JSON-serializable dictionaries."""

    return {
        output_file: portfolio.model_dump(mode="json")
        for output_file, portfolio in portfolios.items()
    }


def _build_portfolio(
    assets: list[PortfolioAssetInput],
    *,
    spec: PortfolioSpec,
    diversity_constraints: Mapping[str, float],
) -> PortfolioOutput:
    max_counts = _max_counts(spec.target_size, diversity_constraints)
    selected: list[PortfolioAssetInput] = []

    for category in spec.required_categories:
        candidate = _best_candidate_for_category(
            category,
            assets,
            spec=spec,
            selected=selected,
            max_counts=max_counts,
        )
        if candidate is None:
            raise ValueError(
                f"Unable to fill {spec.output_file}: no eligible asset for category {category!r}"
            )
        selected.append(candidate)

    if len(selected) < spec.target_size:
        for candidate in _sorted_candidates(assets):
            if candidate in selected:
                continue
            if candidate.commercial_tier not in spec.allowed_commercial_tiers:
                continue
            if _can_select(candidate, selected, max_counts):
                selected.append(candidate)
            if len(selected) == spec.target_size:
                break

    if len(selected) != spec.target_size:
        raise ValueError(
            f"Unable to fill {spec.output_file}: selected {len(selected)} of {spec.target_size}"
        )

    ranked = sorted(
        selected,
        key=lambda asset: (
            -stabilized_selection_score(asset),
            -asset.global_rank_score,
            TIER_PRIORITY[asset.commercial_tier],
            asset.stable_id,
        ),
    )

    return PortfolioOutput(
        portfolio_type=spec.kind,
        title=spec.title,
        output_file=spec.output_file,
        target_size=spec.target_size,
        diversity_constraints=dict(diversity_constraints),
        narrative_balance=dict(Counter(asset.category for asset in ranked)),
        ranking_stabilization=(
            "Selection uses 5-point score bands and hard 20% domain, geography, "
            "and asset-type caps to prevent single-category domination."
        ),
        assets=[
            _selection_for_asset(asset, rank=index + 1, spec=spec)
            for index, asset in enumerate(ranked)
        ],
    )


def _best_candidate_for_category(
    category: str,
    assets: list[PortfolioAssetInput],
    *,
    spec: PortfolioSpec,
    selected: list[PortfolioAssetInput],
    max_counts: Mapping[str, int],
) -> PortfolioAssetInput | None:
    for candidate in _sorted_candidates(assets):
        if candidate.category != category:
            continue
        if candidate.commercial_tier not in spec.allowed_commercial_tiers:
            continue
        if candidate in selected:
            continue
        if _can_select(candidate, selected, max_counts):
            return candidate
    return None


def _sorted_candidates(assets: Iterable[PortfolioAssetInput]) -> list[PortfolioAssetInput]:
    return sorted(
        assets,
        key=lambda asset: (
            -selection_band(asset),
            -asset.global_rank_score,
            TIER_PRIORITY[asset.commercial_tier],
            asset.category,
            asset.stable_id,
        ),
    )


def _can_select(
    candidate: PortfolioAssetInput,
    selected: list[PortfolioAssetInput],
    max_counts: Mapping[str, int],
) -> bool:
    domain_counts = Counter(asset.diversity_domain for asset in selected)
    geography_counts = Counter(asset.geography for asset in selected)
    asset_type_counts = Counter(asset.asset_type for asset in selected)

    return (
        domain_counts[candidate.diversity_domain] < max_counts["domain"]
        and geography_counts[candidate.geography] < max_counts["geography"]
        and asset_type_counts[candidate.asset_type] < max_counts["asset_type"]
    )


def stabilized_selection_score(asset: PortfolioAssetInput) -> float:
    """Blend ranking, recognition, and demand before applying stability bands."""

    score = (
        asset.global_rank_score * 0.70
        + asset.recognition_score * 0.15
        + asset.demand_score * 0.15
    )
    return round(score, 2)


def selection_band(asset: PortfolioAssetInput) -> float:
    """Return a 5-point score band to dampen minor score churn."""

    return math.floor(stabilized_selection_score(asset) / SCORE_STABILITY_BAND) * SCORE_STABILITY_BAND


def _selection_for_asset(
    asset: PortfolioAssetInput,
    *,
    rank: int,
    spec: PortfolioSpec,
) -> PortfolioSelection:
    return PortfolioSelection(
        portfolio_rank=rank,
        stable_id=asset.stable_id,
        title=asset.title,
        global_rank_score=asset.global_rank_score,
        recognition_score=asset.recognition_score,
        demand_score=asset.demand_score,
        stabilized_selection_score=stabilized_selection_score(asset),
        commercial_tier=asset.commercial_tier,
        asset_type=asset.asset_type,
        category=asset.category,
        domain=asset.diversity_domain,
        geography=asset.geography,
        why_this_asset_was_selected=_explain_selection(asset, spec),
    )


def _explain_selection(asset: PortfolioAssetInput, spec: PortfolioSpec) -> str:
    return (
        f"Selected for the {spec.title} because it anchors the {asset.category} narrative, "
        f"has global rank {asset.global_rank_score:.2f}, recognition {asset.recognition_score:.2f}, "
        f"demand {asset.demand_score:.2f}, and preserves diversity across domain "
        f"{asset.diversity_domain}, geography {asset.geography}, and asset type {asset.asset_type}."
    )


def _max_counts(target_size: int, diversity_constraints: Mapping[str, float]) -> dict[str, int]:
    max_counts = {
        key: max(1, math.floor(target_size * limit))
        for key, limit in diversity_constraints.items()
    }
    for required_key in DEFAULT_DIVERSITY_CONSTRAINTS:
        if required_key not in max_counts:
            raise ValueError(f"Missing diversity constraint: {required_key}")
    return max_counts
