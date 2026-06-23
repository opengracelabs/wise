"""RC9 portfolio data validation tests."""

from __future__ import annotations

from pathlib import Path

from tests.portfolio_helpers import PORTFOLIO_DIR, assert_ranked, assert_score, load_portfolio_records


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "implementation" / "rc9-global-asset-report.md"
AUDIT = ROOT / "docs" / "implementation" / "rc9-portfolio-audit.md"

REQUIRED_FIELDS = {
    "title",
    "category",
    "country",
    "recognition_score",
    "demand_score",
    "commercial_score",
    "portfolio_score",
    "product_recommendations",
}

ALLOWED_PRODUCTS = {
    "Fine Art Print",
    "Framed Print",
    "Canvas Print",
    "Poster",
    "Jigsaw Puzzle",
    "Coffee Table Book",
    "Calendar",
    "Postcards",
    "Educational Card Set",
    "Posters",
    "Framed Prints",
    "Canvas Prints",
    "Puzzles",
    "Calendars",
    "Coffee Table Books",
    "Historic Maps",
    "Educational Card Sets",
}


def test_rc9_portfolio_files_have_100_required_records() -> None:
    for filename in [
        "top_100_global_assets.json",
        "top_100_collections.json",
        "top_100_series.json",
    ]:
        records = load_portfolio_records(filename)
        assert_ranked(records, 100)

        for record in records:
            assert record["title"]
            assert record["category"]
            assert "recognition_score" in record
            assert "demand_score" in record
            assert "commercial_score" in record
            assert "portfolio_score" in record
            assert record["product_recommendations"]
            if filename == "top_100_global_assets.json":
                assert record["country"]
            for key in ("recognition_score", "demand_score", "commercial_score", "portfolio_score"):
                assert_score(record, key)


def test_rc9_report_declares_frozen_architecture_scope() -> None:
    report = REPORT.read_text(encoding="utf-8")

    assert "Architecture v1.0 remains frozen" in report
    assert "No agents were added or changed" in report
    assert "No ADRs were added or changed" in report
    assert "Top 20 likely best-selling products" in report


def test_rc9_audit_declares_score_and_priority_lists() -> None:
    audit = AUDIT.read_text(encoding="utf-8")

    assert "Architecture v1.0 remains frozen" in audit
    assert "Portfolio score: 84 / 100" in audit
    assert "Top 25 highest-priority assets" in audit
    assert "Top 25 highest-priority collections" in audit
    assert "Top 25 highest-priority series" in audit
