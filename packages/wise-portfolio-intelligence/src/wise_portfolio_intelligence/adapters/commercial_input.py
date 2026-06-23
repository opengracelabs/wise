"""Portfolio input adapter for commercial-intelligence fields."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from wise_commercial_intelligence import calculate_commercial_score


@dataclass(frozen=True)
class PortfolioCandidate:
    """Normalized asset candidate used by portfolio selection."""

    id: str
    title: str
    recognition_score: int
    commercial_appeal_score: int
    commercial_tier: str
    final_selection_score: int
    historical_significance_level: str
    award_tags: tuple[str, ...]
    country: str
    domain: str
    collection_family: str
    portfolio_category: str
    rights_status: str
    source_asset: Mapping[str, Any]


def _int_score(value: Any) -> int:
    if value in (None, ""):
        return 0
    return max(0, min(100, round(float(value))))


def _string(value: Any, default: str) -> str:
    text = str(value).strip() if value not in (None, "") else ""
    return text or default


def _tags(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        values = [value]
    else:
        try:
            values = list(value)
        except TypeError:
            values = [value]
    return tuple(sorted({str(tag).strip() for tag in values if str(tag).strip()}))


def adapt_commercial_portfolio_input(asset: Mapping[str, Any]) -> PortfolioCandidate:
    """Normalize recognition and commercial intelligence fields for portfolio selection."""

    if {
        "commercial_appeal_score",
        "commercial_tier",
        "final_selection_score",
    }.issubset(asset):
        commercial_fields = {
            "recognition_score": _int_score(asset.get("recognition_score")),
            "commercial_appeal_score": _int_score(asset.get("commercial_appeal_score")),
            "commercial_tier": _string(asset.get("commercial_tier"), "Archive Only"),
            "final_selection_score": _int_score(asset.get("final_selection_score")),
        }
    else:
        evaluation = calculate_commercial_score(asset)
        commercial_fields = evaluation.to_asset_fields()

    return PortfolioCandidate(
        id=_string(asset.get("id"), _string(asset.get("stable_id"), "unknown")),
        title=_string(asset.get("title"), "Untitled asset"),
        recognition_score=_int_score(commercial_fields.get("recognition_score")),
        commercial_appeal_score=_int_score(commercial_fields.get("commercial_appeal_score")),
        commercial_tier=_string(commercial_fields.get("commercial_tier"), "Archive Only"),
        final_selection_score=_int_score(commercial_fields.get("final_selection_score")),
        historical_significance_level=_string(asset.get("historical_significance_level"), "unknown"),
        award_tags=_tags(asset.get("award_tags")),
        country=_string(asset.get("country"), "Unknown"),
        domain=_string(asset.get("domain"), "unknown"),
        collection_family=_string(asset.get("collection_family"), "uncategorized"),
        portfolio_category=_string(asset.get("portfolio_category"), "homepage"),
        rights_status=_string(asset.get("rights_status"), "Unknown"),
        source_asset=asset,
    )
