"""Recognition scoring pipeline for asset inclusion decisions."""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from wise_recognition_intelligence.ranking.global_importance_ranker import rank_assets
from wise_recognition_intelligence.scoring.recognition_score import (
    ELIGIBILITY_THRESHOLD,
    calculate_recognition_score,
)


def evaluate_asset(asset: Mapping[str, Any]) -> dict[str, Any]:
    """Attach recognition-intelligence output fields to an asset."""

    evaluation = calculate_recognition_score(asset)
    return {**dict(asset), **evaluation.to_asset_fields()}


def evaluate_assets(assets: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Evaluate a batch of assets."""

    return [evaluate_asset(asset) for asset in assets]


def eligible_assets(assets: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Return only assets meeting the recognition threshold."""

    evaluated = evaluate_assets(assets)
    return [asset for asset in evaluated if int(asset["recognition_score"]) >= ELIGIBILITY_THRESHOLD]


def rank_assets_for_inclusion(assets: Iterable[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    """Evaluate and rank assets that are eligible for inclusion."""

    return rank_assets(eligible_assets(assets))
