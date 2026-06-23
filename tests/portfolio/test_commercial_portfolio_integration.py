"""Commercial and portfolio intelligence integration tests."""

import json
from importlib import resources

from wise_portfolio_intelligence import (
    PortfolioSelectionConfig,
    adapt_commercial_portfolio_input,
    select_candidate_outputs,
    select_portfolio_candidates,
)

REQUIRED_OUTPUT_FIELDS = {
    "recognition_score",
    "commercial_appeal_score",
    "final_selection_score",
    "commercial_tier",
    "portfolio_category",
    "rights_status",
    "why_this_asset_was_selected",
}


def test_portfolio_adapter_accepts_commercial_scores() -> None:
    candidate = adapt_commercial_portfolio_input(
        {
            "id": "stonehenge-product",
            "title": "Stonehenge Product",
            "recognition_score": 92,
            "commercial_appeal_score": 88,
            "commercial_tier": "Icon Product",
            "final_selection_score": 90,
            "historical_significance_level": "global",
            "award_tags": ["unesco_world_heritage"],
            "country": "United Kingdom",
            "domain": "heritage",
            "collection_family": "megalithic-sites",
            "portfolio_category": "product",
            "rights_status": "Open",
        }
    )

    assert candidate.recognition_score == 92
    assert candidate.commercial_appeal_score == 88
    assert candidate.commercial_tier == "Icon Product"
    assert candidate.final_selection_score == 90
    assert candidate.portfolio_category == "product"


def test_adapter_can_calculate_missing_commercial_fields() -> None:
    candidate = adapt_commercial_portfolio_input(
        {
            "id": "calculated-commercial",
            "recognition_score": 94,
            "award_tags": ["unesco_world_heritage"],
            "historical_significance_level": "global",
            "hero_image": True,
            "visually_distinctive": True,
            "cultural_identity": True,
            "curriculum_relevance": True,
            "visitor_destination": True,
            "decorative_fit": True,
            "collectible_fit": True,
        }
    )

    assert candidate.commercial_appeal_score >= 80
    assert candidate.commercial_tier == "Icon Product"


def test_commercial_score_cannot_override_diversity_caps() -> None:
    assets = [
        {
            "id": "high-commerce-us-a",
            "title": "High Commerce US A",
            "recognition_score": 96,
            "commercial_appeal_score": 100,
            "commercial_tier": "Icon Product",
            "final_selection_score": 98,
            "historical_significance_level": "global",
            "country": "United States",
            "domain": "heritage",
            "collection_family": "family-a",
            "portfolio_category": "homepage",
            "rights_status": "Open",
        },
        {
            "id": "high-commerce-us-b",
            "title": "High Commerce US B",
            "recognition_score": 95,
            "commercial_appeal_score": 99,
            "commercial_tier": "Icon Product",
            "final_selection_score": 97,
            "historical_significance_level": "global",
            "country": "United States",
            "domain": "nature",
            "collection_family": "family-b",
            "portfolio_category": "homepage",
            "rights_status": "Open",
        },
        {
            "id": "balanced-uk",
            "title": "Balanced UK",
            "recognition_score": 78,
            "commercial_appeal_score": 62,
            "commercial_tier": "Educational Product",
            "final_selection_score": 68,
            "historical_significance_level": "high",
            "country": "United Kingdom",
            "domain": "culture",
            "collection_family": "family-c",
            "portfolio_category": "homepage",
            "rights_status": "Open",
        },
    ]

    selected = select_portfolio_candidates(
        assets,
        PortfolioSelectionConfig(max_items=2, max_per_country=1, portfolio_category="homepage"),
    )

    assert [asset["id"] for asset in selected] == ["high-commerce-us-a", "balanced-uk"]
    assert sum(1 for asset in selected if asset["country"] == "United States") == 1


def test_unknown_and_restricted_rights_assets_are_excluded() -> None:
    assets = [
        {
            "id": "unknown-rights",
            "recognition_score": 100,
            "commercial_appeal_score": 100,
            "commercial_tier": "Icon Product",
            "final_selection_score": 100,
            "historical_significance_level": "global",
            "portfolio_category": "product",
            "rights_status": "Unknown",
        },
        {
            "id": "restricted-rights",
            "recognition_score": 99,
            "commercial_appeal_score": 99,
            "commercial_tier": "Icon Product",
            "final_selection_score": 99,
            "historical_significance_level": "global",
            "portfolio_category": "product",
            "rights_status": "Restricted",
        },
        {
            "id": "open-rights",
            "recognition_score": 72,
            "commercial_appeal_score": 55,
            "commercial_tier": "Educational Product",
            "final_selection_score": 62,
            "historical_significance_level": "moderate",
            "portfolio_category": "product",
            "rights_status": "Open",
        },
    ]

    selected = select_portfolio_candidates(assets, PortfolioSelectionConfig(max_items=3, portfolio_category="product"))

    assert [asset["id"] for asset in selected] == ["open-rights"]


def test_review_required_assets_are_not_publishable() -> None:
    selected = select_portfolio_candidates(
        [
            {
                "id": "review-required",
                "recognition_score": 82,
                "commercial_appeal_score": 67,
                "commercial_tier": "Strong Product",
                "final_selection_score": 73,
                "historical_significance_level": "high",
                "portfolio_category": "collection",
                "rights_status": "Review Required",
            }
        ],
        PortfolioSelectionConfig(max_items=1, portfolio_category="collection"),
    )

    assert selected[0]["id"] == "review-required"
    assert selected[0]["publishable"] is False
    assert selected[0]["rights_status"] == "Review Required"


def test_candidate_output_groups_use_consistent_schema() -> None:
    outputs = select_candidate_outputs(
        [
            {
                "id": "homepage-open",
                "recognition_score": 92,
                "commercial_appeal_score": 88,
                "commercial_tier": "Icon Product",
                "final_selection_score": 90,
                "historical_significance_level": "global",
                "portfolio_category": "homepage",
                "rights_status": "Open",
            },
            {
                "id": "collection-open",
                "recognition_score": 82,
                "commercial_appeal_score": 67,
                "commercial_tier": "Strong Product",
                "final_selection_score": 73,
                "historical_significance_level": "high",
                "portfolio_category": "collection",
                "rights_status": "Open",
            },
            {
                "id": "series-open",
                "recognition_score": 80,
                "commercial_appeal_score": 76,
                "commercial_tier": "Strong Product",
                "final_selection_score": 78,
                "historical_significance_level": "moderate",
                "portfolio_category": "series",
                "rights_status": "Open",
            },
            {
                "id": "product-open",
                "recognition_score": 84,
                "commercial_appeal_score": 73,
                "commercial_tier": "Strong Product",
                "final_selection_score": 77,
                "historical_significance_level": "high",
                "portfolio_category": "product",
                "rights_status": "Open",
            },
        ]
    )

    assert set(outputs) == {
        "homepage_candidates.json",
        "collection_candidates.json",
        "series_candidates.json",
        "product_candidates.json",
    }
    for rows in outputs.values():
        assert rows
        for row in rows:
            assert REQUIRED_OUTPUT_FIELDS.issubset(row)


def test_packaged_candidate_json_outputs_use_consistent_schema() -> None:
    for filename in (
        "homepage_candidates.json",
        "collection_candidates.json",
        "series_candidates.json",
        "product_candidates.json",
    ):
        output_path = resources.files("wise_portfolio_intelligence.outputs").joinpath(filename)
        rows = json.loads(output_path.read_text(encoding="utf-8"))

        assert rows
        for row in rows:
            assert REQUIRED_OUTPUT_FIELDS.issubset(row)
