"""Commercial intelligence scoring tests."""

import json
from importlib import resources

from wise_commercial_intelligence import calculate_commercial_score, evaluate_asset, rank_assets


def test_icon_product_output_contains_required_fields() -> None:
    asset = {
        "id": "stonehenge",
        "title": "Stonehenge",
        "recognition_score": 94,
        "award_tags": ["unesco_world_heritage", "smithsonian_featured_collection"],
        "historical_significance_level": "global",
        "hero_image": True,
        "visually_distinctive": True,
        "cultural_identity": True,
        "curriculum_relevance": True,
        "visitor_destination": True,
        "decorative_fit": True,
        "collectible_fit": True,
    }

    evaluated = evaluate_asset(asset)

    assert evaluated["recognition_score"] == 94
    assert evaluated["commercial_appeal_score"] >= 80
    assert evaluated["final_selection_score"] >= 85
    assert evaluated["commercial_tier"] == "Icon Product"
    assert set(evaluated["commercial_breakdown"]) == {
        "visual_impact",
        "emotional_connection",
        "educational_demand",
        "tourism_interest",
        "giftability",
    }


def test_commercial_appeal_is_separate_from_recognition_score() -> None:
    low_commercial_asset = {
        "recognition_score": 96,
        "award_tags": [],
        "historical_significance_level": "limited",
    }

    evaluation = calculate_commercial_score(low_commercial_asset)

    assert evaluation.recognition_score == 96
    assert evaluation.commercial_appeal_score < evaluation.recognition_score
    assert evaluation.commercial_tier in {"Educational Product", "Archive Only"}


def test_educational_product_can_be_driven_by_learning_demand() -> None:
    asset = {
        "recognition_score": 62,
        "award_tags": ["nobel_related"],
        "historical_significance_level": "high",
        "curriculum_relevance": True,
        "museum_learning_value": True,
    }

    evaluated = evaluate_asset(asset)

    assert evaluated["commercial_breakdown"]["educational_demand"] >= 14
    assert evaluated["commercial_tier"] == "Educational Product"


def test_archive_only_for_low_recognition_low_appeal_asset() -> None:
    evaluated = evaluate_asset(
        {
            "recognition_score": 18,
            "award_tags": [],
            "historical_significance_level": "limited",
        }
    )

    assert evaluated["commercial_appeal_score"] == 0
    assert evaluated["final_selection_score"] == 7
    assert evaluated["commercial_tier"] == "Archive Only"


def test_explicit_dimension_scores_are_capped() -> None:
    evaluated = evaluate_asset(
        {
            "recognition_score": 101,
            "visual_impact_score": 250,
            "emotional_connection_score": 250,
            "educational_demand_score": 200,
            "tourism_interest_score": 150,
            "giftability_score": 150,
        }
    )

    assert evaluated["recognition_score"] == 100
    assert evaluated["commercial_appeal_score"] == 100
    assert evaluated["final_selection_score"] == 100
    assert evaluated["commercial_tier"] == "Icon Product"


def test_sample_rankings_are_valid_and_ordered() -> None:
    sample_path = resources.files("wise_commercial_intelligence.samples").joinpath("sample_rankings.json")
    samples = json.loads(sample_path.read_text(encoding="utf-8"))

    ranked = rank_assets(samples)

    assert [asset["commercial_tier"] for asset in ranked] == [
        "Icon Product",
        "Strong Product",
        "Educational Product",
        "Archive Only",
    ]
    assert ranked[0]["final_selection_score"] > ranked[-1]["final_selection_score"]
