"""RC13 representation expansion validation tests."""

from __future__ import annotations

from pathlib import Path

from tests.portfolio_helpers import assert_ranked, assert_score, load_portfolio_records


ROOT = Path(__file__).resolve().parents[1]
RESCORE = ROOT / "docs" / "implementation" / "rc13-portfolio-rescore.md"
COVERAGE = ROOT / "docs" / "implementation" / "rc13-global-coverage-report.md"

FOCUS_REGIONS = {
    "Sub-Saharan Africa",
    "West Asia",
    "Central Asia",
    "South Asia",
    "South/Southeast Asia",
    "Oceania",
    "Indigenous Cultures",
}


def test_rc13_expansion_candidates_cover_focus_regions() -> None:
    candidates = load_portfolio_records("expansion_candidates.json")

    assert len(candidates) == 100
    regions = {candidate["target_region"] for candidate in candidates}
    assert {
        "Sub-Saharan Africa",
        "West Asia",
        "Central Asia",
        "South Asia",
        "Oceania",
        "Indigenous Cultures",
    }.issubset(regions)

    for candidate in candidates:
        assert candidate["target_region"] in FOCUS_REGIONS | {"Biodiversity", "Cartography", "Other"}
        assert candidate["product_recommendations"]
        for key in (
            "recognition_score",
            "demand_score",
            "commercial_score",
            "portfolio_score",
        ):
            assert_score(candidate, key)


def test_rc13_top_200_files_have_required_balance_fields() -> None:
    for filename in [
        "top_200_global_assets.json",
        "top_200_collections.json",
        "top_200_series.json",
    ]:
        records = load_portfolio_records(filename)
        assert_ranked(records, 200)

        if filename == "top_200_global_assets.json":
            countries = {record["country"] for record in records}
            assert len(countries) > 1

        for record in records:
            assert record["product_recommendations"]
            for key in (
                "recognition_score",
                "demand_score",
                "commercial_score",
                "portfolio_score",
            ):
                assert_score(record, key)


def test_rc13_reports_declare_target_score_and_frozen_scope() -> None:
    rescore = RESCORE.read_text(encoding="utf-8")
    coverage = COVERAGE.read_text(encoding="utf-8")

    assert ("84 -> 91" in rescore or "84 → 90+" in rescore or "**93.0**" in rescore)
    assert ("**91**" in rescore or "93.0" in rescore)
    assert ("Architecture v1.0 remains frozen" in rescore or "Does not modify Architecture v1.0" in rescore)
    assert ("No agents are proposed or added" in rescore or "agents (ADR-011)" in rescore)
    assert "Sub-Saharan Africa" in coverage
    assert "Indigenous representation" in coverage
    assert "remaining gaps" in coverage.lower()
