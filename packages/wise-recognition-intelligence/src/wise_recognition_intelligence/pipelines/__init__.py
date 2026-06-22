"""Recognition pipeline entry points."""

from wise_recognition_intelligence.pipelines.recognition_pipeline import (
    eligible_assets,
    evaluate_asset,
    evaluate_assets,
    rank_assets_for_inclusion,
)

__all__ = ["eligible_assets", "evaluate_asset", "evaluate_assets", "rank_assets_for_inclusion"]
