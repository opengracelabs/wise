"""Tests for the WISE global ranking package."""

from __future__ import annotations

import json
from pathlib import Path

from wise_global_ranking import (
    GlobalRankingInput,
    RankingTier,
    build_reference_global_ranking_output,
    classify_asset,
    global_rank_score,
    rank_assets,
)


def test_global_rank_score_combines_all_components() -> None:
    asset = GlobalRankingInput(
        stable_id="sample",
        title="Sample",
        asset_type="heritage_site",
        demand_score=80,
        recognition_score=70,
        emotional_score=60,
        visual_impact_score=50,
        historical_importance_score=40,
    )

    assert global_rank_score(asset) == 64.5


def test_tier_1_requires_unesco_award_and_high_demand() -> None:
    asset = GlobalRankingInput(
        stable_id="iconic-site",
        title="Iconic Site",
        asset_type="heritage_site",
        demand_score=0.92,
        recognition_score=95,
        emotional_score=90,
        visual_impact_score=90,
        historical_importance_score=95,
        unesco_whc_id="999",
        awards_prizes=("Global heritage prize",),
    )

    assert classify_asset(asset) == RankingTier.TIER_1
    ranked = rank_assets([asset])[0]
    assert ranked.eligibility.series is True
    assert ranked.eligibility.products is True
    assert ranked.eligibility.marketplace is True


def test_tier_3_and_tier_4_assets_are_blocked_from_commercial_entry() -> None:
    educational = GlobalRankingInput(
        stable_id="teaching-record",
        title="Teaching Record",
        asset_type="archive_record",
        demand_score=25,
        recognition_score=20,
        emotional_score=35,
        visual_impact_score=30,
        historical_importance_score=40,
        educational_use=True,
    )
    archival = GlobalRankingInput(
        stable_id="restricted-record",
        title="Restricted Record",
        asset_type="archive_record",
        demand_score=95,
        recognition_score=95,
        emotional_score=95,
        visual_impact_score=95,
        historical_importance_score=95,
        commercial_use=False,
        product_use=False,
    )

    ranked = {asset.stable_id: asset for asset in rank_assets([educational, archival])}
    assert ranked["teaching-record"].tier == RankingTier.TIER_3
    assert ranked["restricted-record"].tier == RankingTier.TIER_4
    assert ranked["teaching-record"].eligibility.products is False
    assert ranked["restricted-record"].eligibility.marketplace is False


def test_committed_global_ranked_assets_matches_reference_builder() -> None:
    artifact_path = Path(__file__).parents[2] / "packages" / "wise-global-ranking" / "global_ranked_assets.json"
    committed_output = json.loads(artifact_path.read_text(encoding="utf-8"))
    generated_output = build_reference_global_ranking_output()

    assert committed_output == generated_output
    scores = [asset["global_rank_score"] for asset in committed_output["assets"]]
    assert scores == sorted(scores, reverse=True)
    for asset in committed_output["assets"]:
        eligible = asset["tier"] in {"Tier 1", "Tier 2"}
        assert asset["eligibility"] == {
            "series": eligible,
            "products": eligible,
            "marketplace": eligible,
        }
