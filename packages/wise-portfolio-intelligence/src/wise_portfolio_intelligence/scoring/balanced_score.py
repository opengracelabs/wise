"""Mission-first balanced scoring for portfolio selection."""

from __future__ import annotations

from wise_portfolio_intelligence.adapters.commercial_input import PortfolioCandidate

HISTORICAL_LEVEL_WEIGHTS = {
    "global": 100,
    "high": 80,
    "moderate": 55,
    "limited": 20,
    "unknown": 0,
}


def historical_weight(candidate: PortfolioCandidate) -> int:
    """Convert historical significance labels into a bounded scoring signal."""

    return HISTORICAL_LEVEL_WEIGHTS.get(candidate.historical_significance_level.lower(), 0)


def balanced_portfolio_score(candidate: PortfolioCandidate) -> int:
    """Score candidates while keeping commercial appeal subordinate to mission signals."""

    score = (
        candidate.recognition_score * 0.45
        + historical_weight(candidate) * 0.20
        + candidate.final_selection_score * 0.20
        + candidate.commercial_appeal_score * 0.15
    )
    return max(0, min(100, round(score)))
