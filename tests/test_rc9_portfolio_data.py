"""RC9 portfolio data validation tests."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PORTFOLIO_DIR = ROOT / "data" / "portfolio"
REPORT = ROOT / "docs" / "implementation" / "rc9-global-asset-report.md"

REQUIRED_FIELDS = {
    "title",
    "category",
    "country",
    "recognition_score",
    "demand_score",
    "commercial_score",
    "portfolio_score",
    "recommended_products",
}

ALLOWED_PRODUCTS = {
    "Posters",
    "Framed Prints",
    "Canvas Prints",
    "Puzzles",
    "Calendars",
    "Coffee Table Books",
    "Historic Maps",
    "Educational Card Sets",
}


def _load(name: str) -> list[dict]:
    with (PORTFOLIO_DIR / name).open(encoding="utf-8") as handle:
        return json.load(handle)


def test_rc9_portfolio_files_have_100_required_records() -> None:
    for filename in [
        "top_100_global_assets.json",
        "top_100_collections.json",
        "top_100_series.json",
    ]:
        records = _load(filename)
        assert len(records) == 100
        assert [record["rank"] for record in records] == list(range(1, 101))

        for record in records:
            assert REQUIRED_FIELDS.issubset(record)
            assert record["title"]
            assert record["category"]
            assert record["country"]
            assert 0 <= record["recognition_score"] <= 1
            assert 0 <= record["demand_score"] <= 1
            assert 0 <= record["commercial_score"] <= 1
            assert 0 <= record["portfolio_score"] <= 1
            assert set(record["recommended_products"]).issubset(ALLOWED_PRODUCTS)
            assert record["recommended_products"]


def test_rc9_report_declares_frozen_architecture_scope() -> None:
    report = REPORT.read_text(encoding="utf-8")

    assert "Architecture v1.0 remains frozen" in report
    assert "No agents were added or changed" in report
    assert "No ADRs were added or changed" in report
    assert "Top 20 likely best-selling products" in report
