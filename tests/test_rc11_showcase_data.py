"""RC11 showcase portfolio validation tests."""

from __future__ import annotations

from pathlib import Path

from tests.portfolio_helpers import assert_ranked, assert_score, load_portfolio_records


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "implementation" / "rc11-showcase-report.md"

ALLOWED_PRODUCT_CATEGORIES = {
    "Posters",
    "Framed Prints",
    "Canvas Prints",
    "Puzzles",
    "Calendars",
    "Coffee Table Books",
    "Coffee Table Book",
    "Jigsaw Puzzles",
    "Framed Print",
    "Canvas Print",
    "Poster",
}


def test_rc11_showcase_assets_have_required_scores() -> None:
    records = load_portfolio_records("top_25_showcase_assets.json")
    assert_ranked(records, 25)

    for record in records:
        for key in (
            "global_significance",
            "visual_appeal",
            "educational_value",
            "commercial_potential",
            "showcase_score",
        ):
            assert_score(record, key)
        assert record["product_recommendations"]


def test_rc11_showcase_collections_balance_required_themes() -> None:
    records = load_portfolio_records("top_25_showcase_collections.json")
    assert_ranked(records, 25)

    themes = {record["showcase_theme"].lower() for record in records}
    assert {"heritage", "biodiversity", "geography", "culture", "climate"}.issubset(themes)

    for record in records:
        assert_score(record, "showcase_score")
        assert record["showcase_theme"]


def test_rc11_showcase_series_include_strength_scores() -> None:
    records = load_portfolio_records("top_25_showcase_series.json")
    assert_ranked(records, 25)

    for record in records:
        for key in (
            "narrative_strength",
            "educational_value",
            "product_potential",
            "showcase_score",
        ):
            assert_score(record, key)


def test_rc11_product_files_use_allowed_categories() -> None:
    top_50 = load_portfolio_records("top_50_products.json")
    top_25 = load_portfolio_records("top_25_showcase_products.json")

    assert_ranked(top_50, 50)
    assert_ranked(top_25, 25)

    for record in top_50:
        assert record["category"] in ALLOWED_PRODUCT_CATEGORIES
        assert_score(record, "showcase_score")

    for record in top_25:
        assert record["category"] in ALLOWED_PRODUCT_CATEGORIES
        assert_score(record, "showcase_score")


def test_rc11_report_declares_frozen_architecture_scope() -> None:
    report = REPORT.read_text(encoding="utf-8")

    assert "Does not modify Architecture v1.0" in report
    assert "governance" in report
    assert ("No agents are proposed or added" in report or "agents (ADR-011)" in report)
    assert ("Top 10 products to launch first" in report or "Top 10 launch" in report)
