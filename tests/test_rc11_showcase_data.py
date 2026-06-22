"""RC11 showcase portfolio validation tests."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PORTFOLIO_DIR = ROOT / "data" / "portfolio"
REPORT = ROOT / "docs" / "implementation" / "rc11-showcase-report.md"

ALLOWED_PRODUCT_CATEGORIES = {
    "Posters",
    "Framed Prints",
    "Canvas Prints",
    "Puzzles",
    "Calendars",
    "Coffee Table Books",
}


def _load(name: str) -> list[dict]:
    with (PORTFOLIO_DIR / name).open(encoding="utf-8") as handle:
        return json.load(handle)


def _assert_ranked(records: list[dict], expected_count: int) -> None:
    assert len(records) == expected_count
    assert [record["rank"] for record in records] == list(range(1, expected_count + 1))


def _assert_score(record: dict, key: str = "showcase_score") -> None:
    assert 0 <= record[key] <= 100


def test_rc11_showcase_assets_have_required_scores() -> None:
    records = _load("top_25_showcase_assets.json")
    _assert_ranked(records, 25)

    for record in records:
        for key in [
            "recognition_score",
            "visual_appeal_score",
            "educational_value_score",
            "commercial_value_score",
            "global_significance_score",
            "showcase_score",
        ]:
            _assert_score(record, key)
        assert record["recommended_products"]


def test_rc11_showcase_collections_balance_required_themes() -> None:
    records = _load("top_25_showcase_collections.json")
    _assert_ranked(records, 25)

    tags = {tag for record in records for tag in record["balance_tags"]}
    assert {"heritage", "biodiversity", "geography", "culture", "climate"}.issubset(tags)

    for record in records:
        _assert_score(record)
        assert record["balance_tags"]


def test_rc11_showcase_series_include_strength_scores() -> None:
    records = _load("top_25_showcase_series.json")
    _assert_ranked(records, 25)

    for record in records:
        for key in [
            "narrative_strength_score",
            "educational_strength_score",
            "product_potential_score",
            "showcase_score",
        ]:
            _assert_score(record, key)


def test_rc11_product_files_use_allowed_categories() -> None:
    top_50 = _load("top_50_products.json")
    top_25 = _load("top_25_showcase_products.json")

    _assert_ranked(top_50, 50)
    _assert_ranked(top_25, 25)

    for record in [*top_50, *top_25]:
        assert record["category"] in ALLOWED_PRODUCT_CATEGORIES
        _assert_score(record)


def test_rc11_report_declares_frozen_architecture_scope() -> None:
    report = REPORT.read_text(encoding="utf-8")

    assert "Architecture v1.0 remains frozen" in report
    assert "No governance changes" in report
    assert "No agents are proposed or added" in report
    assert "Top 10 products to launch first" in report
