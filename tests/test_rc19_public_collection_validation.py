"""RC19 rights-aware public collection validation tests."""

from __future__ import annotations

import importlib.util
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_public_collection.py"
SPEC = importlib.util.spec_from_file_location("validate_public_collection", SCRIPT_PATH)
assert SPEC and SPEC.loader
validate_public_collection = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_public_collection)


def _report():
    return validate_public_collection.build_report()


def _asset(report, asset_id):
    return next(asset for asset in report["assets"] if asset["asset_id"] == asset_id)


def test_rc19_summary_counts_and_pipeline():
    report = _report()
    assert report["collection"]["title"] == "Big Cats of the World"
    assert report["validation_pipeline"] == [
        "Asset",
        "Source Check",
        "License Check",
        "Attribution Check",
        "Provenance Check",
        "Publication Approval Check",
        "Collection Eligibility",
    ]
    assert report["summary"] == {
        "assets_reviewed": 9,
        "approved_assets": 3,
        "blocked_assets": 6,
        "missing_provenance": 1,
        "missing_attribution": 1,
        "publication_readiness_score": 33.33,
    }


def test_rc19_approved_assets_are_fully_eligible():
    report = _report()
    assert set(report["approved_assets"]) == {
        "bigcats-lion-gbif-profile",
        "bigcats-tiger-commons-photo",
        "bigcats-snow-leopard-eol-summary",
    }
    for asset_id in report["approved_assets"]:
        asset = _asset(report, asset_id)
        assert asset["eligible"] is True
        assert not asset["blocked_reasons"]
        assert all(result == "pass" for result in asset["checks"].values())


def test_rc19_unknown_rights_fail():
    asset = _asset(_report(), "bigcats-leopard-field-audio")
    assert asset["eligible"] is False
    assert "unknown_rights" in asset["blocked_reasons"]
    assert asset["checks"]["License Check"] == "fail"


def test_rc19_missing_source_fails():
    asset = _asset(_report(), "bigcats-cheetah-range-map")
    assert asset["eligible"] is False
    assert "missing_source" in asset["blocked_reasons"]
    assert asset["checks"]["Source Check"] == "fail"


def test_rc19_missing_attribution_fails():
    asset = _asset(_report(), "bigcats-cougar-education-card")
    assert asset["eligible"] is False
    assert "missing_attribution" in asset["blocked_reasons"]
    assert asset["checks"]["Attribution Check"] == "fail"


def test_rc19_restricted_assets_fail():
    asset = _asset(_report(), "bigcats-jaguar-museum-scan")
    assert asset["eligible"] is False
    assert "restricted_asset" in asset["blocked_reasons"]
    assert asset["checks"]["License Check"] == "fail"


def test_rc19_unapproved_assets_fail():
    asset = _asset(_report(), "bigcats-lynx-draft-profile")
    assert asset["eligible"] is False
    assert "unapproved_asset" in asset["blocked_reasons"]
    assert asset["checks"]["Asset"] == "fail"


def test_rc19_missing_provenance_is_reported():
    asset = _asset(_report(), "bigcats-clouded-leopard-archive-photo")
    assert asset["eligible"] is False
    assert "missing_provenance" in asset["blocked_reasons"]
    assert asset["checks"]["Provenance Check"] == "fail"
