"""Shared portfolio intelligence constants."""

from __future__ import annotations

from typing import Any, Mapping

RIGHTS_STATUS_APPROVED = "Approved"
RIGHTS_STATUS_REVIEW_REQUIRED = "Review Required"
RIGHTS_STATUS_RESTRICTED = "Restricted"
RIGHTS_STATUS_UNKNOWN = "Unknown"

RIGHTS_ELIGIBILITY_ELIGIBLE = "eligible"
RIGHTS_ELIGIBILITY_CANDIDATE_ONLY = "candidate_only"
RIGHTS_ELIGIBILITY_EXCLUDED = "excluded"

BALANCED_GLOBAL_PORTFOLIO_DOMAINS = (
    "heritage",
    "biodiversity",
    "protected areas",
    "art",
    "historical maps",
    "cultural traditions",
)

RIGHTS_STATUS_ALIASES = {
    "approved": RIGHTS_STATUS_APPROVED,
    "eligible": RIGHTS_STATUS_APPROVED,
    "cleared": RIGHTS_STATUS_APPROVED,
    "publishable": RIGHTS_STATUS_APPROVED,
    "open": RIGHTS_STATUS_APPROVED,
    "review required": RIGHTS_STATUS_REVIEW_REQUIRED,
    "review": RIGHTS_STATUS_REVIEW_REQUIRED,
    "candidate only": RIGHTS_STATUS_REVIEW_REQUIRED,
    "needs review": RIGHTS_STATUS_REVIEW_REQUIRED,
    "restricted": RIGHTS_STATUS_RESTRICTED,
    "blocked": RIGHTS_STATUS_RESTRICTED,
    "excluded": RIGHTS_STATUS_RESTRICTED,
    "unknown": RIGHTS_STATUS_UNKNOWN,
    "": RIGHTS_STATUS_UNKNOWN,
}

RIGHTS_STATUS_FIELD_ALIASES = (
    "rights_status",
    "rightsStatus",
    "Rights Status",
    "rc17_rights_status",
    "rc17RightsStatus",
)


def normalize_text(value: str) -> str:
    """Normalize labels for alias matching."""

    return " ".join(value.strip().lower().replace("-", " ").replace("_", " ").split())


def normalize_rights_status(value: str | None) -> str:
    """Map rights labels to canonical portfolio statuses."""

    if value is None:
        return RIGHTS_STATUS_UNKNOWN
    return RIGHTS_STATUS_ALIASES.get(normalize_text(str(value)), RIGHTS_STATUS_UNKNOWN)


def rights_eligibility(rights_status: str) -> str:
    """Return portfolio eligibility for a canonical rights status."""

    if rights_status == RIGHTS_STATUS_APPROVED:
        return RIGHTS_ELIGIBILITY_ELIGIBLE
    if rights_status == RIGHTS_STATUS_REVIEW_REQUIRED:
        return RIGHTS_ELIGIBILITY_CANDIDATE_ONLY
    return RIGHTS_ELIGIBILITY_EXCLUDED


def read_rights_status(asset: Mapping[str, Any]) -> str:
    """Read and normalize rights status from common portfolio field aliases."""

    portfolio_inputs = asset.get("portfolio_inputs")
    if isinstance(portfolio_inputs, Mapping):
        for alias in RIGHTS_STATUS_FIELD_ALIASES:
            if alias in portfolio_inputs and portfolio_inputs[alias] not in (None, ""):
                return normalize_rights_status(str(portfolio_inputs[alias]))

    for alias in RIGHTS_STATUS_FIELD_ALIASES:
        if alias in asset and asset[alias] not in (None, ""):
            return normalize_rights_status(str(asset[alias]))

    return RIGHTS_STATUS_UNKNOWN
