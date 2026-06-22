"""RC17 publication rights and provenance lifecycle validation."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

LIFECYCLE_STAGES: tuple[str, ...] = (
    "Asset",
    "Source Verified",
    "License Verified",
    "Provenance Verified",
    "Rights Approved",
    "Publication Approved",
    "Publishable",
)

REGISTRY_FILES: dict[str, str] = {
    "assets": "asset-registry.json",
    "sources": "source-registry.json",
    "licenses": "license-registry.json",
    "provenance": "provenance-registry.json",
    "attributions": "attribution-registry.json",
    "approvals": "publication-approvals.json",
    "jurisdictions": "jurisdiction-rules.json",
}

APPROVED_RIGHTS_STATUSES = frozenset({"rights_approved"})
UNKNOWN_RIGHTS_STATUSES = frozenset({"unknown", "rights_unknown", "unverified", ""})


@dataclass(frozen=True)
class ValidationResult:
    """Lifecycle validation result for one asset."""

    asset_id: str
    stages: dict[str, bool]
    blockers: list[str]

    @property
    def publishable(self) -> bool:
        return self.stages["Publishable"]


def load_registries(rights_root: Path) -> dict[str, Any]:
    """Load all RC17 JSON registries from a rights directory."""

    return {
        key: json.loads((rights_root / filename).read_text(encoding="utf-8"))
        for key, filename in REGISTRY_FILES.items()
    }


def validate_registries(registries: dict[str, Any]) -> list[ValidationResult]:
    """Validate every asset in the asset registry."""

    return [
        validate_asset_lifecycle(asset["asset_id"], registries)
        for asset in registries["assets"]["assets"]
    ]


def validate_asset_lifecycle(asset_id: str, registries: dict[str, Any]) -> ValidationResult:
    """Validate an asset through the RC17 publication lifecycle."""

    assets = _index_by(registries["assets"]["assets"], "asset_id")
    sources = _index_by(registries["sources"]["sources"], "source_id")
    licenses = _index_by(registries["licenses"]["licenses"], "license_id")
    provenance = _index_by(registries["provenance"]["provenance_records"], "provenance_id")
    attributions = _index_by(registries["attributions"]["attributions"], "attribution_id")
    approvals = _index_by(registries["approvals"]["approvals"], "approval_id")
    jurisdictions = _index_by(registries["jurisdictions"]["rules"], "jurisdiction")

    stages = {stage: False for stage in LIFECYCLE_STAGES}
    blockers: list[str] = []

    asset = assets.get(asset_id)
    if asset is None:
        blockers.append("missing_asset")
        return ValidationResult(asset_id=asset_id, stages=stages, blockers=blockers)
    stages["Asset"] = True

    source = sources.get(asset.get("source_id"))
    if source is None:
        blockers.append("missing_source")
    elif not source.get("verified"):
        blockers.append("source_not_verified")
    else:
        stages["Source Verified"] = True

    license_record = licenses.get(asset.get("license_id"))
    rights_status = str(asset.get("rights_status", "")).strip().lower()
    if rights_status in UNKNOWN_RIGHTS_STATUSES:
        blockers.append("unknown_rights")
    if license_record is None:
        blockers.append("missing_license")
    elif not license_record.get("verified"):
        blockers.append("license_not_verified")
    else:
        stages["License Verified"] = True

    provenance_record = provenance.get(asset.get("provenance_id"))
    if provenance_record is None:
        blockers.append("missing_provenance")
    elif provenance_record.get("asset_id") != asset_id:
        blockers.append("provenance_asset_mismatch")
    elif provenance_record.get("source_id") != asset.get("source_id"):
        blockers.append("provenance_source_mismatch")
    elif provenance_record.get("status") != "verified":
        blockers.append("provenance_not_verified")
    elif not provenance_record.get("event_chain"):
        blockers.append("empty_provenance_chain")
    else:
        stages["Provenance Verified"] = True

    attribution = attributions.get(asset.get("attribution_id"))
    if attribution is None:
        blockers.append("missing_attribution")
    elif attribution.get("asset_id") != asset_id:
        blockers.append("attribution_asset_mismatch")
    elif attribution.get("required") and attribution.get("status") != "verified":
        blockers.append("attribution_not_verified")

    jurisdiction = jurisdictions.get(asset.get("jurisdiction"))
    if jurisdiction is None:
        blockers.append("missing_jurisdiction_rule")
    elif not jurisdiction.get("publication_allowed"):
        blockers.append("jurisdiction_publication_blocked")

    if asset.get("restricted") is True:
        blockers.append("restricted_asset")
    if license_record is not None and not license_record.get("publication_allowed"):
        blockers.append("license_publication_blocked")

    if (
        stages["Source Verified"]
        and stages["License Verified"]
        and stages["Provenance Verified"]
        and rights_status in APPROVED_RIGHTS_STATUSES
        and asset.get("restricted") is not True
        and license_record is not None
        and license_record.get("publication_allowed") is True
        and jurisdiction is not None
        and jurisdiction.get("publication_allowed") is True
    ):
        stages["Rights Approved"] = True
    elif rights_status not in APPROVED_RIGHTS_STATUSES and rights_status not in UNKNOWN_RIGHTS_STATUSES:
        blockers.append("rights_not_approved")

    approval = approvals.get(asset.get("publication_approval_id"))
    if approval is None:
        blockers.append("missing_publication_approval")
    elif approval.get("asset_id") != asset_id:
        blockers.append("publication_approval_asset_mismatch")
    elif approval.get("status") != "approved":
        blockers.append("publication_not_approved")
        blockers.extend(approval.get("blockers") or [])
    else:
        stages["Publication Approved"] = True

    stages["Publishable"] = (
        stages["Rights Approved"]
        and stages["Publication Approved"]
        and asset.get("restricted") is not True
        and not any(blocker in blockers for blocker in _publish_blockers())
    )

    return ValidationResult(
        asset_id=asset_id,
        stages=stages,
        blockers=sorted(set(blockers)),
    )


def generate_summary_metrics(results: list[ValidationResult], registries: dict[str, Any]) -> dict[str, Any]:
    """Generate summary metrics for RC17 report and JSON output."""

    asset_by_id = _index_by(registries["assets"]["assets"], "asset_id")
    source_ids = {asset["source_id"] for asset in registries["assets"]["assets"]}
    license_ids = {asset["license_id"] for asset in registries["assets"]["assets"]}
    verified_sources = {
        source["source_id"]
        for source in registries["sources"]["sources"]
        if source.get("verified")
    }
    verified_licenses = {
        license_record["license_id"]
        for license_record in registries["licenses"]["licenses"]
        if license_record.get("verified")
    }
    blockers = Counter(blocker for result in results for blocker in result.blockers)
    publishable_assets = [result.asset_id for result in results if result.publishable]
    blocked_assets = [result.asset_id for result in results if not result.publishable]

    return {
        "metrics_version": "rc17-rights-provenance-metrics/0.1.0",
        "asset_count": len(results),
        "publishable_count": len(publishable_assets),
        "blocked_count": len(blocked_assets),
        "publishable_assets": publishable_assets,
        "blocked_assets": blocked_assets,
        "source_coverage": {
            "referenced_source_count": len(source_ids),
            "verified_referenced_source_count": len(source_ids & verified_sources),
            "coverage": _coverage_ratio(source_ids, verified_sources),
        },
        "license_coverage": {
            "referenced_license_count": len(license_ids),
            "verified_referenced_license_count": len(license_ids & verified_licenses),
            "coverage": _coverage_ratio(license_ids, verified_licenses),
        },
        "rights_blockers": dict(sorted(blockers.items())),
        "publication_readiness": {
            "publishable_share": round(len(publishable_assets) / len(results), 2) if results else 0.0,
            "restricted_asset_count": sum(1 for asset in asset_by_id.values() if asset.get("restricted") is True),
        },
        "lifecycle": {
            result.asset_id: {
                "publishable": result.publishable,
                "stages": result.stages,
                "blockers": result.blockers,
            }
            for result in results
        },
    }


def _index_by(records: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {record[key]: record for record in records}


def _coverage_ratio(referenced: set[str], verified: set[str]) -> float:
    if not referenced:
        return 0.0
    return round(len(referenced & verified) / len(referenced), 2)


def _publish_blockers() -> set[str]:
    return {
        "missing_source",
        "source_not_verified",
        "unknown_rights",
        "missing_license",
        "license_not_verified",
        "missing_provenance",
        "provenance_asset_mismatch",
        "provenance_source_mismatch",
        "provenance_not_verified",
        "empty_provenance_chain",
        "missing_attribution",
        "attribution_asset_mismatch",
        "attribution_not_verified",
        "missing_jurisdiction_rule",
        "jurisdiction_publication_blocked",
        "restricted_asset",
        "license_publication_blocked",
        "rights_not_approved",
        "missing_publication_approval",
        "publication_approval_asset_mismatch",
        "publication_not_approved",
    }
