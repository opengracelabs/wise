"""Cap-aware portfolio candidate selection."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from wise_portfolio_intelligence.adapters.commercial_input import (
    PortfolioCandidate,
    adapt_commercial_portfolio_input,
)
from wise_portfolio_intelligence.scoring.balanced_score import balanced_portfolio_score
from wise_portfolio_intelligence.selection.rights_gate import RightsDecision, rights_gate


@dataclass(frozen=True)
class PortfolioSelectionConfig:
    """Selection caps that preserve portfolio balance."""

    max_items: int = 12
    max_per_country: int = 2
    max_per_domain: int = 3
    max_per_collection_family: int = 2
    portfolio_category: str | None = None


def _why_selected(candidate: PortfolioCandidate, score: int, rights_decision: RightsDecision) -> str:
    parts = [
        f"balanced portfolio score {score}",
        f"recognition score {candidate.recognition_score}",
        f"commercial appeal {candidate.commercial_appeal_score}",
        f"commercial tier {candidate.commercial_tier}",
        f"rights status {rights_decision.rights_status}",
    ]
    return "; ".join(parts)


def _to_output(candidate: PortfolioCandidate, score: int, rights_decision: RightsDecision) -> dict[str, Any]:
    return {
        "id": candidate.id,
        "title": candidate.title,
        "recognition_score": candidate.recognition_score,
        "commercial_appeal_score": candidate.commercial_appeal_score,
        "final_selection_score": candidate.final_selection_score,
        "commercial_tier": candidate.commercial_tier,
        "portfolio_category": candidate.portfolio_category,
        "rights_status": rights_decision.rights_status,
        "rights_eligibility": rights_decision.eligibility,
        "publishable": rights_decision.publishable,
        "country": candidate.country,
        "domain": candidate.domain,
        "collection_family": candidate.collection_family,
        "balanced_portfolio_score": score,
        "why_this_asset_was_selected": _why_selected(candidate, score, rights_decision),
    }


def _cap_allows(counter: Counter[str], key: str, cap: int) -> bool:
    return counter[key] < cap


def select_portfolio_candidates(
    assets: Iterable[Mapping[str, Any]],
    config: PortfolioSelectionConfig | None = None,
) -> list[dict[str, Any]]:
    """Select candidates with rights gating and diversity caps."""

    config = config or PortfolioSelectionConfig()
    scored: list[tuple[int, PortfolioCandidate, RightsDecision]] = []
    for asset in assets:
        candidate = adapt_commercial_portfolio_input(asset)
        if config.portfolio_category and candidate.portfolio_category != config.portfolio_category:
            continue

        rights_decision = rights_gate(candidate.rights_status)
        if rights_decision.excluded:
            continue

        scored.append((balanced_portfolio_score(candidate), candidate, rights_decision))

    ranked = sorted(
        scored,
        key=lambda row: (
            row[0],
            row[1].recognition_score,
            row[1].final_selection_score,
            row[1].commercial_appeal_score,
            row[1].id,
        ),
        reverse=True,
    )

    country_counts: Counter[str] = Counter()
    domain_counts: Counter[str] = Counter()
    family_counts: Counter[str] = Counter()
    selected: list[dict[str, Any]] = []

    for score, candidate, rights_decision in ranked:
        if len(selected) >= config.max_items:
            break
        if not _cap_allows(country_counts, candidate.country, config.max_per_country):
            continue
        if not _cap_allows(domain_counts, candidate.domain, config.max_per_domain):
            continue
        if not _cap_allows(family_counts, candidate.collection_family, config.max_per_collection_family):
            continue

        selected.append(_to_output(candidate, score, rights_decision))
        country_counts[candidate.country] += 1
        domain_counts[candidate.domain] += 1
        family_counts[candidate.collection_family] += 1

    return selected


def select_candidate_outputs(
    assets: Iterable[Mapping[str, Any]],
    *,
    homepage_config: PortfolioSelectionConfig | None = None,
    collection_config: PortfolioSelectionConfig | None = None,
    series_config: PortfolioSelectionConfig | None = None,
    product_config: PortfolioSelectionConfig | None = None,
) -> dict[str, list[dict[str, Any]]]:
    """Build all portfolio candidate output groups."""

    asset_list = list(assets)
    return {
        "homepage_candidates.json": select_portfolio_candidates(
            asset_list,
            homepage_config or PortfolioSelectionConfig(max_items=6, portfolio_category="homepage"),
        ),
        "collection_candidates.json": select_portfolio_candidates(
            asset_list,
            collection_config or PortfolioSelectionConfig(max_items=8, portfolio_category="collection"),
        ),
        "series_candidates.json": select_portfolio_candidates(
            asset_list,
            series_config or PortfolioSelectionConfig(max_items=8, portfolio_category="series"),
        ),
        "product_candidates.json": select_portfolio_candidates(
            asset_list,
            product_config or PortfolioSelectionConfig(max_items=8, portfolio_category="product"),
        ),
    }
