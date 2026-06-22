"""Tests for RC17 rights and provenance lifecycle validation."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from rights import (
    LIFECYCLE_STAGES,
    generate_summary_metrics,
    load_registries,
    validate_asset_lifecycle,
    validate_registries,
)


RIGHTS_ROOT = Path(__file__).parents[2] / "rights"


def test_all_registry_assets_validate_through_lifecycle() -> None:
    registries = load_registries(RIGHTS_ROOT)
    results = validate_registries(registries)
    results_by_id = {result.asset_id: result for result in results}

    assert set(results_by_id) == {
        "stonehenge",
        "everglades-national-park",
        "panthera-leo",
        "wikidata-q140-lion",
        "sensitive-oral-history-example",
    }
    assert all(set(result.stages) == set(LIFECYCLE_STAGES) for result in results)
    assert results_by_id["stonehenge"].publishable is True
    assert results_by_id["everglades-national-park"].publishable is True
    assert results_by_id["panthera-leo"].publishable is True
    assert results_by_id["wikidata-q140-lion"].publishable is True
    assert results_by_id["sensitive-oral-history-example"].publishable is False


def test_unknown_rights_fail_validation() -> None:
    registries = load_registries(RIGHTS_ROOT)
    mutated = copy.deepcopy(registries)
    mutated["assets"]["assets"][0]["rights_status"] = "unknown"

    result = validate_asset_lifecycle("stonehenge", mutated)

    assert result.publishable is False
    assert result.stages["Rights Approved"] is False
    assert "unknown_rights" in result.blockers


def test_missing_source_fails_validation() -> None:
    registries = load_registries(RIGHTS_ROOT)
    mutated = copy.deepcopy(registries)
    mutated["assets"]["assets"][0]["source_id"] = "missing-source"

    result = validate_asset_lifecycle("stonehenge", mutated)

    assert result.publishable is False
    assert result.stages["Source Verified"] is False
    assert "missing_source" in result.blockers
    assert "provenance_source_mismatch" in result.blockers


def test_missing_license_fails_validation() -> None:
    registries = load_registries(RIGHTS_ROOT)
    mutated = copy.deepcopy(registries)
    mutated["assets"]["assets"][0]["license_id"] = "missing-license"

    result = validate_asset_lifecycle("stonehenge", mutated)

    assert result.publishable is False
    assert result.stages["License Verified"] is False
    assert "missing_license" in result.blockers


def test_restricted_assets_cannot_be_publishable() -> None:
    registries = load_registries(RIGHTS_ROOT)
    result = validate_asset_lifecycle("sensitive-oral-history-example", registries)

    assert result.publishable is False
    assert result.stages["Source Verified"] is True
    assert result.stages["License Verified"] is True
    assert result.stages["Provenance Verified"] is True
    assert result.stages["Rights Approved"] is False
    assert result.stages["Publication Approved"] is False
    assert "restricted_asset" in result.blockers
    assert "license_publication_blocked" in result.blockers


def test_summary_metrics_generated_from_registries() -> None:
    registries = load_registries(RIGHTS_ROOT)
    results = validate_registries(registries)
    generated = generate_summary_metrics(results, registries)
    committed = json.loads((RIGHTS_ROOT / "summary-metrics.json").read_text(encoding="utf-8"))

    assert committed == generated
    assert generated["asset_count"] == 5
    assert generated["publishable_count"] == 4
    assert generated["blocked_count"] == 1
    assert generated["source_coverage"]["coverage"] == 1.0
    assert generated["license_coverage"]["coverage"] == 1.0
    assert generated["publication_readiness"]["restricted_asset_count"] == 1
