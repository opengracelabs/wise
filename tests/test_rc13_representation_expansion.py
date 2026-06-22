"""RC13 representation expansion validation tests."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PORTFOLIO_DIR = ROOT / "data" / "portfolio"
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


def _load(name: str) -> list[dict]:
    with (PORTFOLIO_DIR / name).open(encoding="utf-8") as handle:
        return json.load(handle)


def _assert_score(record: dict, key: str) -> None:
    assert 0 <= record[key] <= 1


def test_rc13_expansion_candidates_cover_focus_regions() -> None:
    candidates = _load("expansion_candidates.json")

    assert len(candidates) == 100
    regions = {candidate["focus_region"] for candidate in candidates}
    assert {
        "Sub-Saharan Africa",
        "West Asia",
        "Central Asia",
        "South Asia",
        "Oceania",
        "Indigenous Cultures",
    }.issubset(regions)

    for candidate in candidates:
        assert candidate["focus_region"] in FOCUS_REGIONS
        assert candidate["public_domain_readiness"]
        assert candidate["recommended_products"]
        for key in [
            "recognition_score",
            "demand_score",
            "commercial_score",
            "portfolio_score",
        ]:
            _assert_score(candidate, key)


def test_rc13_top_200_files_have_required_balance_fields() -> None:
    for filename in [
        "top_200_global_assets.json",
        "top_200_collections.json",
        "top_200_series.json",
    ]:
        records = _load(filename)
        assert len(records) == 200
        assert [record["rank"] for record in records] == list(range(1, 201))

        regions = {record["region"] for record in records}
        assert "Sub-Saharan Africa" in regions
        assert "West Asia" in regions
        assert "Central Asia" in regions
        assert "Oceania" in regions
        assert "Indigenous Cultures" in regions

        for record in records:
            assert record["balance_tags"]
            assert record["public_domain_readiness"]
            assert record["recommended_products"]
            for key in [
                "recognition_score",
                "demand_score",
                "commercial_score",
                "portfolio_score",
            ]:
                _assert_score(record, key)


def test_rc13_reports_declare_target_score_and_frozen_scope() -> None:
    rescore = RESCORE.read_text(encoding="utf-8")
    coverage = COVERAGE.read_text(encoding="utf-8")

    assert "84 -> 91" in rescore
    assert "**91**" in rescore
    assert "Architecture v1.0 remains frozen" in rescore
    assert "No agents are proposed or added" in rescore
    assert "Sub-Saharan Africa" in coverage
    assert "Indigenous representation" in coverage
    assert "remaining gaps" in coverage.lower()
