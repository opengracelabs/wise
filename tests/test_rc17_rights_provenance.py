"""RC17 rights and provenance infrastructure validation tests."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
RIGHTS = ROOT / "rights"
COLLECTIONS = ROOT / "content" / "collections"
RIGHTS_DOCS = ROOT / "docs" / "rights"
REPORT = ROOT / "docs" / "implementation" / "rc17-rights-provenance-report.md"

ALLOWED_RIGHTS = {"Approved", "Review Required", "Restricted", "Unknown"}
ALLOWED_PUBLICATION = {"Draft", "Editorial Review", "Rights Review", "Approved", "Published"}


def _load(name: str):
    with (RIGHTS / name).open(encoding="utf-8") as handle:
        return json.load(handle)


def _collection_assets() -> set[str]:
    assets: set[str] = set()
    for path in COLLECTIONS.glob("*.md"):
        in_assets = False
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip() == "## Key assets":
                in_assets = True
                continue
            if in_assets and line.startswith("## "):
                break
            if in_assets and line.startswith("- "):
                assets.add(line[2:].strip())
    return assets


def _validate_assets(asset_registry: dict, source_registry: dict, license_registry: dict) -> None:
    sources = {source["source_id"] for source in source_registry["sources"]}
    licenses = {license_["license_id"] for license_ in license_registry["licenses"]}

    for asset in asset_registry["assets"]:
        assert asset["asset_id"]
        assert asset["source"], f"source missing for {asset['asset_id']}"
        assert asset["source_id"] in sources, f"source missing for {asset['asset_id']}"
        assert asset["license"], f"license missing for {asset['asset_id']}"
        assert asset["license_id"] in licenses, f"license unknown for {asset['asset_id']}"
        assert asset["license_id"] != "UNKNOWN", f"license unknown for {asset['asset_id']}"
        assert asset["rights_status"] in ALLOWED_RIGHTS
        assert asset["rights_status"] != "Unknown", f"rights status unknown for {asset['asset_id']}"
        assert asset["publication_status"] in ALLOWED_PUBLICATION


def test_rc17_required_registry_files_exist() -> None:
    expected = {
        "asset-registry.json",
        "source-registry.json",
        "license-registry.json",
        "attribution-registry.json",
        "provenance-registry.json",
        "publication-approvals.json",
        "jurisdiction-rules.json",
    }

    assert {path.name for path in RIGHTS.glob("*.json")} == expected


def test_rc17_every_collection_asset_is_registered() -> None:
    registry = _load("asset-registry.json")
    registered = {asset["title"] for asset in registry["assets"]}

    assert _collection_assets() == registered
    for asset in registry["assets"]:
        assert {
            "asset_id",
            "source",
            "license",
            "rights_status",
            "publication_status",
        }.issubset(asset)


def test_rc17_rights_validation_accepts_current_registries() -> None:
    _validate_assets(
        _load("asset-registry.json"),
        _load("source-registry.json"),
        _load("license-registry.json"),
    )


def test_rc17_validation_fails_for_missing_source() -> None:
    assets = _load("asset-registry.json")
    broken = copy.deepcopy(assets)
    broken["assets"][0]["source"] = ""

    with pytest.raises(AssertionError, match="source missing"):
        _validate_assets(broken, _load("source-registry.json"), _load("license-registry.json"))


def test_rc17_validation_fails_for_unknown_license() -> None:
    assets = _load("asset-registry.json")
    broken = copy.deepcopy(assets)
    broken["assets"][0]["license_id"] = "UNKNOWN"

    with pytest.raises(AssertionError, match="license unknown"):
        _validate_assets(broken, _load("source-registry.json"), _load("license-registry.json"))


def test_rc17_validation_fails_for_unknown_rights_status() -> None:
    assets = _load("asset-registry.json")
    broken = copy.deepcopy(assets)
    broken["assets"][0]["rights_status"] = "Unknown"

    with pytest.raises(AssertionError, match="rights status unknown"):
        _validate_assets(broken, _load("source-registry.json"), _load("license-registry.json"))


def test_rc17_cross_registry_counts_and_metrics_match() -> None:
    assets = _load("asset-registry.json")
    attributions = _load("attribution-registry.json")
    provenance = _load("provenance-registry.json")
    approvals = _load("publication-approvals.json")

    asset_ids = {asset["asset_id"] for asset in assets["assets"]}
    assert len(asset_ids) == len(assets["assets"]) == 42
    assert {item["asset_id"] for item in attributions["attributions"]} == asset_ids
    assert {item["asset_id"] for item in provenance["events"]} == asset_ids
    assert {item["asset_id"] for item in approvals["approvals"]} == asset_ids

    metrics = assets["summary_metrics"]
    assert metrics["assets_approved"] == 6
    assert metrics["assets_blocked"] == 4
    assert metrics["assets_requiring_review"] == 32
    assert approvals["summary_metrics"] == metrics


def test_rc17_policy_docs_and_report_exist() -> None:
    expected_docs = {
        "rights-policy.md",
        "provenance-policy.md",
        "attribution-policy.md",
        "publication-approval-process.md",
        "jurisdiction-guidelines.md",
    }

    assert {path.name for path in RIGHTS_DOCS.glob("*.md")} == expected_docs
    report = REPORT.read_text(encoding="utf-8")
    assert "Assets approved | 6" in report
    assert "Assets blocked | 4" in report
    assert "Assets requiring review | 32" in report
    assert "does not alter architecture, governance, ADRs" in report
