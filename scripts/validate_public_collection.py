"""RC19 rights-aware public collection validation.

Generates a deterministic validation report for the "Big Cats of the World"
public collection. The pipeline is intentionally data-local so it can run in CI
without service dependencies.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPORT_VERSION = "rc19-public-collection-validation-v1"
GENERATED_AT = "2026-06-22T00:00:00Z"
APPROVED = "approved"
ALLOWED_RIGHTS_CATEGORIES = {"public_domain", "open_license"}

PIPELINE = [
    "Asset",
    "Source Check",
    "License Check",
    "Attribution Check",
    "Provenance Check",
    "Publication Approval Check",
    "Collection Eligibility",
]

BIG_CATS_ASSETS: list[dict[str, Any]] = [
    {
        "asset_id": "bigcats-lion-gbif-profile",
        "title": "Lion species profile",
        "species": "Panthera leo",
        "asset_status": APPROVED,
        "source_record": {
            "source_record_id": "source-gbif-panthera-leo-5219404",
            "status": APPROVED,
            "authority": "GBIF",
            "uri": "https://www.gbif.org/species/5219404",
        },
        "rights_record": {
            "rights_record_id": "rights-gbif-cc0",
            "status": APPROVED,
            "rights_category": "public_domain",
            "license_uri": "https://creativecommons.org/publicdomain/zero/1.0/",
            "restricted": False,
        },
        "attribution_record": {
            "attribution_record_id": "attr-gbif-panthera-leo",
            "status": APPROVED,
            "credit_line": "GBIF Backbone Taxonomy",
        },
        "provenance_record": {
            "provenance_record_id": "prov-gbif-panthera-leo",
            "status": APPROVED,
            "event_type": "register",
        },
        "publication_approval": {
            "publication_approval_id": "pub-lion-profile",
            "status": APPROVED,
            "approved_by": "steward-review",
        },
    },
    {
        "asset_id": "bigcats-tiger-commons-photo",
        "title": "Tiger open-license photograph",
        "species": "Panthera tigris",
        "asset_status": APPROVED,
        "source_record": {
            "source_record_id": "source-commons-panthera-tigris",
            "status": APPROVED,
            "authority": "Wikimedia Commons",
            "uri": "https://commons.wikimedia.org/wiki/Panthera_tigris",
        },
        "rights_record": {
            "rights_record_id": "rights-tiger-cc-by-sa",
            "status": APPROVED,
            "rights_category": "open_license",
            "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
            "restricted": False,
        },
        "attribution_record": {
            "attribution_record_id": "attr-tiger-commons",
            "status": APPROVED,
            "credit_line": "Wikimedia Commons contributors, CC BY-SA 4.0",
        },
        "provenance_record": {
            "provenance_record_id": "prov-tiger-commons",
            "status": APPROVED,
            "event_type": "rights-review",
        },
        "publication_approval": {
            "publication_approval_id": "pub-tiger-photo",
            "status": APPROVED,
            "approved_by": "steward-review",
        },
    },
    {
        "asset_id": "bigcats-snow-leopard-eol-summary",
        "title": "Snow leopard education summary",
        "species": "Panthera uncia",
        "asset_status": APPROVED,
        "source_record": {
            "source_record_id": "source-eol-panthera-uncia",
            "status": APPROVED,
            "authority": "Encyclopedia of Life",
            "uri": "https://eol.org/",
        },
        "rights_record": {
            "rights_record_id": "rights-eol-cc-by",
            "status": APPROVED,
            "rights_category": "open_license",
            "license_uri": "https://creativecommons.org/licenses/by/4.0/",
            "restricted": False,
        },
        "attribution_record": {
            "attribution_record_id": "attr-snow-leopard-eol",
            "status": APPROVED,
            "credit_line": "Encyclopedia of Life contributors, CC BY 4.0",
        },
        "provenance_record": {
            "provenance_record_id": "prov-snow-leopard-eol",
            "status": APPROVED,
            "event_type": "source-harvest",
        },
        "publication_approval": {
            "publication_approval_id": "pub-snow-leopard-summary",
            "status": APPROVED,
            "approved_by": "steward-review",
        },
    },
    {
        "asset_id": "bigcats-jaguar-museum-scan",
        "title": "Jaguar historical museum scan",
        "species": "Panthera onca",
        "asset_status": APPROVED,
        "source_record": {
            "source_record_id": "source-museum-jaguar-scan",
            "status": APPROVED,
            "authority": "Partner Museum",
            "uri": "https://example.org/partner-museum/jaguar",
        },
        "rights_record": {
            "rights_record_id": "rights-jaguar-restricted",
            "status": APPROVED,
            "rights_category": "restricted",
            "license_uri": "partner-internal-only",
            "restricted": True,
        },
        "attribution_record": {
            "attribution_record_id": "attr-jaguar-museum",
            "status": APPROVED,
            "credit_line": "Partner Museum",
        },
        "provenance_record": {
            "provenance_record_id": "prov-jaguar-museum",
            "status": APPROVED,
            "event_type": "partner-deposit",
        },
        "publication_approval": {
            "publication_approval_id": "pub-jaguar-scan",
            "status": APPROVED,
            "approved_by": "steward-review",
        },
    },
    {
        "asset_id": "bigcats-leopard-field-audio",
        "title": "Leopard field audio",
        "species": "Panthera pardus",
        "asset_status": APPROVED,
        "source_record": {
            "source_record_id": "source-leopard-field-audio",
            "status": APPROVED,
            "authority": "Field Recording Archive",
            "uri": "https://example.org/field-recordings/leopard",
        },
        "rights_record": {
            "rights_record_id": "rights-leopard-unknown",
            "status": "unknown",
            "rights_category": "unknown",
            "license_uri": None,
            "restricted": False,
        },
        "attribution_record": {
            "attribution_record_id": "attr-leopard-field-audio",
            "status": APPROVED,
            "credit_line": "Field Recording Archive",
        },
        "provenance_record": {
            "provenance_record_id": "prov-leopard-field-audio",
            "status": APPROVED,
            "event_type": "source-harvest",
        },
        "publication_approval": {
            "publication_approval_id": "pub-leopard-audio",
            "status": APPROVED,
            "approved_by": "steward-review",
        },
    },
    {
        "asset_id": "bigcats-cheetah-range-map",
        "title": "Cheetah range map",
        "species": "Acinonyx jubatus",
        "asset_status": APPROVED,
        "source_record": None,
        "rights_record": {
            "rights_record_id": "rights-cheetah-map-cc-by",
            "status": APPROVED,
            "rights_category": "open_license",
            "license_uri": "https://creativecommons.org/licenses/by/4.0/",
            "restricted": False,
        },
        "attribution_record": {
            "attribution_record_id": "attr-cheetah-map",
            "status": APPROVED,
            "credit_line": "Range map contributor",
        },
        "provenance_record": {
            "provenance_record_id": "prov-cheetah-map",
            "status": APPROVED,
            "event_type": "geospatial-import",
        },
        "publication_approval": {
            "publication_approval_id": "pub-cheetah-map",
            "status": APPROVED,
            "approved_by": "steward-review",
        },
    },
    {
        "asset_id": "bigcats-cougar-education-card",
        "title": "Cougar education card",
        "species": "Puma concolor",
        "asset_status": APPROVED,
        "source_record": {
            "source_record_id": "source-cougar-education-card",
            "status": APPROVED,
            "authority": "Education Partner",
            "uri": "https://example.org/education/cougar",
        },
        "rights_record": {
            "rights_record_id": "rights-cougar-card-cc-by",
            "status": APPROVED,
            "rights_category": "open_license",
            "license_uri": "https://creativecommons.org/licenses/by/4.0/",
            "restricted": False,
        },
        "attribution_record": None,
        "provenance_record": {
            "provenance_record_id": "prov-cougar-card",
            "status": APPROVED,
            "event_type": "education-import",
        },
        "publication_approval": {
            "publication_approval_id": "pub-cougar-card",
            "status": APPROVED,
            "approved_by": "steward-review",
        },
    },
    {
        "asset_id": "bigcats-clouded-leopard-archive-photo",
        "title": "Clouded leopard archive photograph",
        "species": "Neofelis nebulosa",
        "asset_status": APPROVED,
        "source_record": {
            "source_record_id": "source-clouded-leopard-archive",
            "status": APPROVED,
            "authority": "Archive Partner",
            "uri": "https://example.org/archive/clouded-leopard",
        },
        "rights_record": {
            "rights_record_id": "rights-clouded-leopard-cc-by",
            "status": APPROVED,
            "rights_category": "open_license",
            "license_uri": "https://creativecommons.org/licenses/by/4.0/",
            "restricted": False,
        },
        "attribution_record": {
            "attribution_record_id": "attr-clouded-leopard-archive",
            "status": APPROVED,
            "credit_line": "Archive Partner",
        },
        "provenance_record": None,
        "publication_approval": {
            "publication_approval_id": "pub-clouded-leopard-photo",
            "status": APPROVED,
            "approved_by": "steward-review",
        },
    },
    {
        "asset_id": "bigcats-lynx-draft-profile",
        "title": "Lynx draft profile",
        "species": "Lynx lynx",
        "asset_status": "proposed",
        "source_record": {
            "source_record_id": "source-lynx-draft-profile",
            "status": APPROVED,
            "authority": "Draft Partner",
            "uri": "https://example.org/drafts/lynx",
        },
        "rights_record": {
            "rights_record_id": "rights-lynx-cc-by",
            "status": APPROVED,
            "rights_category": "open_license",
            "license_uri": "https://creativecommons.org/licenses/by/4.0/",
            "restricted": False,
        },
        "attribution_record": {
            "attribution_record_id": "attr-lynx-draft-profile",
            "status": APPROVED,
            "credit_line": "Draft Partner",
        },
        "provenance_record": {
            "provenance_record_id": "prov-lynx-draft-profile",
            "status": APPROVED,
            "event_type": "draft-import",
        },
        "publication_approval": {
            "publication_approval_id": "pub-lynx-draft-profile",
            "status": APPROVED,
            "approved_by": "steward-review",
        },
    },
]


def _status(record: dict[str, Any] | None) -> str | None:
    if record is None:
        return None
    return record.get("status")


def _check_asset(asset: dict[str, Any]) -> tuple[dict[str, str], list[str]]:
    checks: dict[str, str] = {}
    blocked_reasons: list[str] = []

    if asset.get("asset_status") == APPROVED:
        checks["Asset"] = "pass"
    else:
        checks["Asset"] = "fail"
        blocked_reasons.append("unapproved_asset")

    source_record = asset.get("source_record")
    if source_record is None:
        checks["Source Check"] = "fail"
        blocked_reasons.append("missing_source")
    elif _status(source_record) != APPROVED:
        checks["Source Check"] = "fail"
        blocked_reasons.append("unapproved_source")
    else:
        checks["Source Check"] = "pass"

    rights_record = asset.get("rights_record")
    rights_category = None if rights_record is None else rights_record.get("rights_category")
    if rights_record is None or _status(rights_record) == "unknown" or rights_category == "unknown":
        checks["License Check"] = "fail"
        blocked_reasons.append("unknown_rights")
    elif _status(rights_record) != APPROVED:
        checks["License Check"] = "fail"
        blocked_reasons.append("unapproved_rights")
    elif rights_record.get("restricted") or rights_category not in ALLOWED_RIGHTS_CATEGORIES:
        checks["License Check"] = "fail"
        blocked_reasons.append("restricted_asset")
    else:
        checks["License Check"] = "pass"

    attribution_record = asset.get("attribution_record")
    if attribution_record is None:
        checks["Attribution Check"] = "fail"
        blocked_reasons.append("missing_attribution")
    elif _status(attribution_record) != APPROVED:
        checks["Attribution Check"] = "fail"
        blocked_reasons.append("unapproved_attribution")
    else:
        checks["Attribution Check"] = "pass"

    provenance_record = asset.get("provenance_record")
    if provenance_record is None:
        checks["Provenance Check"] = "fail"
        blocked_reasons.append("missing_provenance")
    elif _status(provenance_record) != APPROVED:
        checks["Provenance Check"] = "fail"
        blocked_reasons.append("unapproved_provenance")
    else:
        checks["Provenance Check"] = "pass"

    publication_approval = asset.get("publication_approval")
    if publication_approval is None or _status(publication_approval) != APPROVED:
        checks["Publication Approval Check"] = "fail"
        blocked_reasons.append("publication_not_approved")
    else:
        checks["Publication Approval Check"] = "pass"

    checks["Collection Eligibility"] = "pass" if not blocked_reasons else "fail"
    return checks, blocked_reasons


def validate_asset(asset: dict[str, Any]) -> dict[str, Any]:
    checks, blocked_reasons = _check_asset(asset)
    return {
        **asset,
        "checks": checks,
        "eligible": checks["Collection Eligibility"] == "pass",
        "blocked_reasons": blocked_reasons,
    }


def build_report(assets: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    reviewed_assets = [validate_asset(asset) for asset in (assets or BIG_CATS_ASSETS)]
    approved_assets = [asset for asset in reviewed_assets if asset["eligible"]]
    blocked_assets = [asset for asset in reviewed_assets if not asset["eligible"]]
    reviewed_count = len(reviewed_assets)
    readiness_score = round((len(approved_assets) / reviewed_count) * 100, 2) if reviewed_count else 0.0

    return {
        "report_version": REPORT_VERSION,
        "generated_at": GENERATED_AT,
        "collection": {
            "collection_id": "big-cats-of-the-world",
            "title": "Big Cats of the World",
            "publication_policy": "rights-approved-assets-only",
        },
        "validation_pipeline": PIPELINE,
        "policy": {
            "required_status": APPROVED,
            "allowed_rights_categories": sorted(ALLOWED_RIGHTS_CATEGORIES),
            "failure_rules": [
                "Unknown rights fail",
                "Missing source fails",
                "Missing attribution fails",
                "Restricted assets fail",
                "Unapproved assets fail",
            ],
        },
        "summary": {
            "assets_reviewed": reviewed_count,
            "approved_assets": len(approved_assets),
            "blocked_assets": len(blocked_assets),
            "missing_provenance": sum(
                "missing_provenance" in asset["blocked_reasons"] for asset in reviewed_assets
            ),
            "missing_attribution": sum(
                "missing_attribution" in asset["blocked_reasons"] for asset in reviewed_assets
            ),
            "publication_readiness_score": readiness_score,
        },
        "approved_assets": [asset["asset_id"] for asset in approved_assets],
        "blocked_assets": [
            {
                "asset_id": asset["asset_id"],
                "title": asset["title"],
                "blocked_reasons": asset["blocked_reasons"],
            }
            for asset in blocked_assets
        ],
        "assets": reviewed_assets,
    }


def write_report(path: Path) -> dict[str, Any]:
    report = build_report()
    path.write_text(json.dumps(report, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("collection-validation-report.json"),
        help="Path to write the generated collection validation report.",
    )
    args = parser.parse_args()
    report = write_report(args.output)
    summary = report["summary"]
    print(
        "RC19 validation complete: "
        f"{summary['approved_assets']} approved, "
        f"{summary['blocked_assets']} blocked, "
        f"readiness={summary['publication_readiness_score']}%"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
