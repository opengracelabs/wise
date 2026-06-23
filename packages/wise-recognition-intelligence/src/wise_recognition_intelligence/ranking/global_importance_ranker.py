"""Global importance rank bucketing for recognition-scored assets."""

from __future__ import annotations

from typing import Any, Iterable, Mapping


def global_rank_bucket(recognition_score: int) -> str:
    """Return the global rank bucket for a recognition score."""

    if recognition_score >= 90:
        return "global_top_tier"
    if recognition_score >= 80:
        return "global_high_importance"
    if recognition_score >= 70:
        return "global_collection_eligible"
    if recognition_score >= 50:
        return "recognized_but_ineligible"
    return "below_recognition_threshold"


def rank_assets(evaluated_assets: Iterable[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    """Rank evaluated assets by recognition score descending."""

    return sorted(
        evaluated_assets,
        key=lambda asset: (int(asset.get("recognition_score", 0)), str(asset.get("id", ""))),
        reverse=True,
    )
