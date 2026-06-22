"""Tests for WISE portfolio intelligence."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from wise_portfolio_intelligence import (
    PORTFOLIO_OUTPUT_FILES,
    NARRATIVE_CATEGORIES,
    REFERENCE_ASSETS,
    PortfolioAssetInput,
    build_metrics_from_package,
    build_portfolio_metrics,
    build_reference_portfolios,
    load_portfolio_outputs,
    portfolio_optimizer,
    serialize_portfolios,
)


def test_diversity_validation_and_narrative_balance() -> None:
    portfolios = build_reference_portfolios()

    for portfolio in portfolios.values():
        assert len(portfolio.assets) == portfolio.target_size
        max_allowed = int(portfolio.target_size * 0.2)

        assert set(portfolio.narrative_balance) == set(NARRATIVE_CATEGORIES)
        assert all(count == 1 for count in portfolio.narrative_balance.values())
        assert max(Counter(asset.domain for asset in portfolio.assets).values()) <= max_allowed
        assert max(Counter(asset.geography for asset in portfolio.assets).values()) <= max_allowed
        assert max(Counter(asset.asset_type for asset in portfolio.assets).values()) <= max_allowed
        assert all(asset.why_this_asset_was_selected for asset in portfolio.assets)


def test_ranking_consistency_and_commercial_tier_filtering() -> None:
    portfolios = build_reference_portfolios()
    homepage = portfolios["homepage_portfolio.json"]
    product = portfolios["product_portfolio.json"]

    stabilized_scores = [asset.stabilized_selection_score for asset in homepage.assets]
    assert stabilized_scores == sorted(stabilized_scores, reverse=True)

    selected_ids = {asset.stable_id for asset in homepage.assets}
    assert "stonehenge" in selected_ids
    assert "machu-picchu" not in selected_ids
    assert "great-barrier-reef" in selected_ids
    assert "arctic-sea-ice" not in selected_ids
    assert {asset.commercial_tier for asset in product.assets} <= {"Tier 1", "Tier 2"}


def test_portfolio_stability_over_minor_score_changes() -> None:
    baseline = build_reference_portfolios()["homepage_portfolio.json"]
    baseline_ids = [asset.stable_id for asset in baseline.assets]
    selected = set(baseline_ids)

    adjusted_assets: list[PortfolioAssetInput] = []
    for asset in REFERENCE_ASSETS:
        if asset.stable_id in selected:
            adjusted_assets.append(asset)
            continue
        adjusted_assets.append(
            asset.model_copy(
                update={"global_rank_score": min(asset.global_rank_score + 1.0, 100.0)}
            )
        )

    adjusted = portfolio_optimizer(adjusted_assets)["homepage_portfolio.json"]
    assert [asset.stable_id for asset in adjusted.assets] == baseline_ids
    assert all(count == 1 for count in adjusted.narrative_balance.values())


def test_committed_portfolio_artifacts_match_reference_builder() -> None:
    package_root = Path(__file__).parents[2] / "packages" / "wise-portfolio-intelligence"
    generated = serialize_portfolios(build_reference_portfolios())

    for output_file, expected in generated.items():
        committed = json.loads((package_root / output_file).read_text(encoding="utf-8"))
        assert committed == expected


def test_portfolio_metrics_generated_from_existing_outputs() -> None:
    package_root = Path(__file__).parents[2] / "packages" / "wise-portfolio-intelligence"
    committed_metrics = json.loads((package_root / "portfolio_metrics.json").read_text(encoding="utf-8"))
    generated_metrics = build_metrics_from_package(package_root)

    assert set(generated_metrics["source_portfolios"]) == set(PORTFOLIO_OUTPUT_FILES)
    assert committed_metrics == generated_metrics
    assert generated_metrics["aggregate_metrics"]["diversity_score"] == 91.67
    assert generated_metrics["aggregate_metrics"]["geographic_balance_score"] == 66.67
    assert generated_metrics["aggregate_metrics"]["domain_balance_score"] == 100.0
    assert generated_metrics["aggregate_metrics"]["asset_type_balance_score"] == 100.0
    assert generated_metrics["aggregate_metrics"]["narrative_balance_score"] == 100.0
    assert generated_metrics["aggregate_metrics"]["concentration_risk_score"] == 20.0
    assert {region["name"] for region in generated_metrics["representation"]["underrepresented_regions"]} == {
        "Africa",
        "Arctic",
    }


def test_governance_metrics_detect_concentration_and_imbalance() -> None:
    package_root = Path(__file__).parents[2] / "packages" / "wise-portfolio-intelligence"
    portfolios = load_portfolio_outputs(package_root)
    homepage = portfolios["homepage_portfolio.json"]
    repeated_asset = homepage["assets"][0]
    imbalanced_portfolio = {
        **homepage,
        "assets": [
            {
                **repeated_asset,
                "geography": "Europe",
                "domain": "Heritage",
                "category": "Heritage",
                "asset_type": "megalithic_site",
            }
            for index in range(5)
        ],
    }

    metrics = build_portfolio_metrics({"homepage_portfolio.json": imbalanced_portfolio})

    assert metrics["aggregate_metrics"]["diversity_score"] < 100.0
    assert metrics["aggregate_metrics"]["geographic_balance_score"] < 100.0
    assert metrics["aggregate_metrics"]["domain_balance_score"] < 100.0
    assert metrics["aggregate_metrics"]["narrative_balance_score"] < 100.0
    assert metrics["aggregate_metrics"]["concentration_risk_score"] == 100.0
    assert {region["name"] for region in metrics["representation"]["underrepresented_regions"]} >= {
        "Africa",
        "Arctic",
    }
