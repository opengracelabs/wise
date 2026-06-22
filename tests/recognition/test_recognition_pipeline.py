"""Recognition intelligence scoring tests."""

from wise_recognition_intelligence import calculate_recognition_score, evaluate_asset
from wise_recognition_intelligence.pipelines import eligible_assets, rank_assets_for_inclusion


def test_unesco_asset_is_collection_series_and_commercial_eligible() -> None:
    asset = {
        "id": "stonehenge",
        "title": "Stonehenge",
        "unesco_world_heritage_id": "373",
        "historical_significance_level": "global",
        "wikipedia_pageviews": 1_250_000,
        "wikipedia_citation_count": 650,
        "academic_citation_count": 125,
    }

    evaluated = evaluate_asset(asset)

    assert evaluated["recognition_score"] >= 70
    assert "unesco_world_heritage" in evaluated["award_tags"]
    assert evaluated["historical_significance_level"] == "global"
    assert evaluated["citation_index"]["score"] >= 16
    assert evaluated["global_rank_bucket"] in {"global_high_importance", "global_top_tier"}
    assert evaluated["eligible_for_collections"] is True
    assert evaluated["eligible_for_series"] is True
    assert evaluated["eligible_for_commercial_products"] is True


def test_low_signal_asset_is_not_eligible() -> None:
    asset = {
        "id": "unrecognized-snapshot",
        "title": "Unrecognized Snapshot",
        "historical_significance_level": "limited",
    }

    evaluated = evaluate_asset(asset)

    assert evaluated["recognition_score"] < 70
    assert evaluated["award_tags"] == []
    assert evaluated["global_rank_bucket"] == "below_recognition_threshold"
    assert evaluated["eligible_for_collections"] is False
    assert evaluated["eligible_for_series"] is False
    assert evaluated["eligible_for_commercial_products"] is False


def test_pulitzer_and_national_geographic_signals_rank_above_threshold() -> None:
    asset = {
        "id": "prize-photo",
        "title": "Prize Photograph",
        "awards": ["Pulitzer Prize for Feature Photography", "National Geographic Award"],
        "historical_significance_level": "major",
        "wikipedia_pageviews_90d": 240_000,
        "wikipedia_citation_count": 220,
        "editorial_selection": True,
    }

    evaluation = calculate_recognition_score(asset)

    assert evaluation.recognition_score >= 70
    assert {"pulitzer_prize", "national_geographic_award"}.issubset(set(evaluation.award_tags))
    assert evaluation.global_rank_bucket in {"global_collection_eligible", "global_high_importance", "global_top_tier"}


def test_pipeline_filters_and_ranks_only_eligible_assets() -> None:
    assets = [
        {
            "id": "low",
            "historical_significance_level": "limited",
        },
        {
            "id": "smithsonian",
            "smithsonian_featured_collection": True,
            "historical_significance_level": "major",
            "academic_citation_count": 260,
            "featured_collection": True,
        },
        {
            "id": "unesco",
            "unesco_whc_id": "001",
            "historical_significance_level": "global",
            "wikipedia_pageviews": 2_100_000,
        },
    ]

    eligible = eligible_assets(assets)
    ranked = rank_assets_for_inclusion(assets)

    assert {asset["id"] for asset in eligible} == {"smithsonian", "unesco"}
    assert [asset["id"] for asset in ranked] == ["unesco", "smithsonian"]
