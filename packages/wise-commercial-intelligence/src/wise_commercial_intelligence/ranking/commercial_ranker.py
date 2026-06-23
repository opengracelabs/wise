"""Commercial ranking helpers."""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from wise_commercial_intelligence.scoring.commercial_score import calculate_commercial_score


def evaluate_asset(asset: Mapping[str, Any]) -> dict[str, Any]:
    """Attach commercial intelligence output fields to an asset."""

    evaluation = calculate_commercial_score(asset)
    return {**dict(asset), **evaluation.to_asset_fields()}


def evaluate_assets(assets: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Evaluate a batch of assets for commercial intelligence."""

    return [evaluate_asset(asset) for asset in assets]


def rank_assets(assets: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Evaluate and rank assets by final selection score."""

    evaluated = evaluate_assets(assets)
    return sorted(
        evaluated,
        key=lambda asset: (
            int(asset.get("final_selection_score", 0)),
            int(asset.get("commercial_appeal_score", 0)),
            int(asset.get("recognition_score", 0)),
            str(asset.get("id", "")),
        ),
        reverse=True,
    )


def sample_ranking_summary(assets: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Return compact ranking rows for product-selection reviews."""

    return [
        {
            "id": asset.get("id"),
            "title": asset.get("title"),
            "recognition_score": asset["recognition_score"],
            "commercial_appeal_score": asset["commercial_appeal_score"],
            "final_selection_score": asset["final_selection_score"],
            "commercial_tier": asset["commercial_tier"],
        }
        for asset in rank_assets(assets)
    ]
