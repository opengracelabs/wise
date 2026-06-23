"""Citation-index normalization for recognition intelligence."""

from __future__ import annotations

from typing import Any, Mapping

from wise_recognition_intelligence.scoring.historical_importance_score import clamp_score


def _int_value(asset: Mapping[str, Any], key: str) -> int:
    value = asset.get(key, 0)
    if value in (None, ""):
        return 0
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return 0


def build_citation_index(asset: Mapping[str, Any]) -> dict[str, int | str]:
    """Build a citation-index profile from Wikipedia and academic proxy signals."""

    academic_citations = _int_value(asset, "academic_citation_count") + _int_value(asset, "citation_count")
    wikipedia_citations = _int_value(asset, "wikipedia_citation_count")
    wikipedia_pageviews = _int_value(asset, "wikipedia_pageviews") + _int_value(asset, "wikipedia_pageviews_90d")
    source_citations = _int_value(asset, "source_citation_count")

    citation_volume = academic_citations + wikipedia_citations + source_citations
    pageview_units = wikipedia_pageviews // 10_000
    composite_volume = citation_volume + pageview_units

    if academic_citations >= 1_000 or wikipedia_citations >= 2_000 or wikipedia_pageviews >= 2_000_000:
        score = 20
    elif academic_citations >= 500 or wikipedia_citations >= 1_000 or wikipedia_pageviews >= 1_000_000:
        score = 18
    elif academic_citations >= 250 or wikipedia_citations >= 500 or wikipedia_pageviews >= 500_000:
        score = 16
    elif academic_citations >= 100 or wikipedia_citations >= 200 or wikipedia_pageviews >= 200_000:
        score = 13
    elif academic_citations >= 25 or wikipedia_citations >= 75 or wikipedia_pageviews >= 50_000:
        score = 9
    elif composite_volume > 0:
        score = 5
    else:
        score = 0

    return {
        "score": clamp_score(score, 0, 20),
        "citation_volume": citation_volume,
        "academic_citations": academic_citations,
        "wikipedia_citations": wikipedia_citations,
        "wikipedia_pageviews": wikipedia_pageviews,
        "source_citations": source_citations,
        "composite_volume": composite_volume,
    }


def score_citation_volume(asset: Mapping[str, Any]) -> int:
    """Score citation volume on a 0-20 scale."""

    return int(build_citation_index(asset)["score"])
