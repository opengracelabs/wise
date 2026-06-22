import json

import pytest

from wise_portfolio_intelligence import (
    COLLECTION_CANDIDATES_FILENAME,
    HOMEPAGE_CANDIDATES_FILENAME,
    PRODUCT_CANDIDATES_FILENAME,
    SERIES_CANDIDATES_FILENAME,
    calculate_portfolio_priority_score,
    load_assets,
    select_portfolio,
    write_portfolio_outputs,
)


def test_calculates_portfolio_priority_score_from_required_inputs():
    score = calculate_portfolio_priority_score(
        recognition_score=80,
        demand_score=90,
        commercial_tier="premium",
        domain="Heritage",
    )

    assert score == 88


def test_rejects_scores_outside_accepted_range():
    with pytest.raises(ValueError, match="between 0 and 100"):
        calculate_portfolio_priority_score(
            recognition_score=101,
            demand_score=90,
            commercial_tier="premium",
            domain="Heritage",
        )


def test_select_portfolio_routes_assets_to_candidate_categories():
    result = select_portfolio(
        [
            _asset("homepage", 90, 92, "premium", "asset", "Heritage", "Italy", family="a"),
            _asset("collection", 75, 80, "collection", "collection", "Biodiversity", "Kenya", family="b"),
            _asset("series", 74, 82, "series", "series", "Protected Areas", "Brazil", family="c"),
            _asset("product", 65, 78, "product", "object", "Art", "Japan", family="d"),
            _asset("archive", 80, 80, "archive", "asset", "Historical Maps", "France", family="e"),
        ]
    )

    assert [asset["id"] for asset in result.homepage_candidates] == ["homepage"]
    assert [asset["id"] for asset in result.collection_candidates] == ["collection"]
    assert [asset["id"] for asset in result.series_candidates] == ["series"]
    assert [asset["id"] for asset in result.product_candidates] == ["product"]
    assert [asset["id"] for asset in result.archive_only] == ["archive"]


def test_select_portfolio_avoids_over_concentration():
    concentrated = [
        _asset(f"italy-{index}", 95 - index, 95 - index, "premium", "asset", "Heritage", "Italy", family=f"a{index}")
        for index in range(5)
    ]
    diverse = [
        _asset("kenya", 84, 84, "premium", "asset", "Biodiversity", "Kenya", family="b"),
        _asset("brazil", 83, 83, "premium", "asset", "Protected Areas", "Brazil", family="c"),
        _asset("japan", 82, 82, "premium", "asset", "Art", "Japan", family="d"),
        _asset("france", 81, 81, "premium", "asset", "Historical Maps", "France", family="e"),
        _asset("peru", 80, 80, "premium", "asset", "Cultural Traditions", "Peru", family="f"),
    ]

    result = select_portfolio(concentrated + diverse, portfolio_limit=10)
    selected = result.homepage_candidates
    italy_count = sum(1 for asset in selected if asset["portfolio_inputs"]["country"] == "Italy")

    assert italy_count == 2
    assert len(selected) == 7
    assert {asset["id"] for asset in result.archive_only if asset["id"].startswith("italy-")} == {
        "italy-2",
        "italy-3",
        "italy-4",
    }


def test_select_portfolio_enforces_domain_and_collection_family_caps():
    assets = [
        _asset("heritage-1", 95, 95, "premium", "asset", "Heritage", "Italy", family="shared"),
        _asset("heritage-2", 94, 94, "premium", "asset", "Heritage", "Kenya", family="shared"),
        _asset("heritage-3", 93, 93, "premium", "asset", "Heritage", "Brazil", family="unique-1"),
        _asset("bio", 89, 89, "premium", "asset", "Biodiversity", "Japan", family="unique-2"),
        _asset("art", 88, 88, "premium", "asset", "Art", "France", family="unique-3"),
        _asset("maps", 87, 87, "premium", "asset", "Historical Maps", "Peru", family="unique-4"),
        _asset("traditions", 86, 86, "premium", "asset", "Cultural Traditions", "India", family="unique-5"),
        _asset("protected", 85, 85, "premium", "asset", "Protected Areas", "Canada", family="unique-6"),
        _asset("other-1", 84, 84, "premium", "asset", "Education", "Egypt", family="unique-7"),
        _asset("other-2", 83, 83, "premium", "asset", "Language", "Mexico", family="unique-8"),
    ]

    result = select_portfolio(assets, portfolio_limit=10)
    selected_ids = {asset["id"] for asset in result.homepage_candidates}

    assert "heritage-1" in selected_ids
    assert "heritage-2" in selected_ids
    assert "heritage-3" not in selected_ids
    assert "heritage-3" in {asset["id"] for asset in result.archive_only}


def test_write_portfolio_outputs_creates_required_json_files(tmp_path):
    result = write_portfolio_outputs(
        [
            _asset("homepage", 90, 92, "premium", "asset", "Heritage", "Italy", family="a"),
            _asset("collection", 75, 80, "collection", "collection", "Biodiversity", "Kenya", family="b"),
            _asset("series", 74, 82, "series", "series", "Protected Areas", "Brazil", family="c"),
            _asset("product", 65, 78, "product", "object", "Art", "Japan", family="d"),
        ],
        tmp_path,
    )

    homepage = json.loads((tmp_path / HOMEPAGE_CANDIDATES_FILENAME).read_text())
    collections = json.loads((tmp_path / COLLECTION_CANDIDATES_FILENAME).read_text())
    series = json.loads((tmp_path / SERIES_CANDIDATES_FILENAME).read_text())
    products = json.loads((tmp_path / PRODUCT_CANDIDATES_FILENAME).read_text())

    assert [asset["id"] for asset in homepage] == ["homepage"]
    assert [asset["id"] for asset in collections] == ["collection"]
    assert [asset["id"] for asset in series] == ["series"]
    assert [asset["id"] for asset in products] == ["product"]
    assert result.homepage_candidates == homepage


def test_load_assets_accepts_assets_wrapper(tmp_path):
    input_file = tmp_path / "assets.json"
    input_file.write_text(json.dumps({"assets": [_asset("wrapped", 70, 70, "product", "asset", "Art", "Japan")]}))

    assert load_assets(input_file)[0]["id"] == "wrapped"


def _asset(
    asset_id,
    recognition_score,
    demand_score,
    commercial_tier,
    asset_type,
    domain,
    region,
    *,
    family=None,
):
    asset = {
        "id": asset_id,
        "recognition_score": recognition_score,
        "demand_score": demand_score,
        "commercial_tier": commercial_tier,
        "asset_type": asset_type,
        "domain": domain,
        "region": region,
    }
    if family is not None:
        asset["collection_family"] = family
    return asset
