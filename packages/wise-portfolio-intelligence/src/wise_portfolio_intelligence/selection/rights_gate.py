"""Rights gating for portfolio candidate selection."""

from __future__ import annotations

from dataclasses import dataclass

EXCLUDED_RIGHTS_STATUSES = {"unknown", "restricted"}
REVIEW_REQUIRED_STATUS = "review required"


@dataclass(frozen=True)
class RightsDecision:
    """Decision produced by the portfolio rights gate."""

    rights_status: str
    excluded: bool
    publishable: bool
    reason: str


def normalize_rights_status(rights_status: str | None) -> str:
    """Normalize rights status labels while preserving display casing."""

    text = str(rights_status or "Unknown").strip()
    return text or "Unknown"


def rights_gate(rights_status: str | None) -> RightsDecision:
    """Exclude blocked rights and mark review-required assets as not publishable."""

    normalized = normalize_rights_status(rights_status)
    key = normalized.lower()

    if key in EXCLUDED_RIGHTS_STATUSES:
        return RightsDecision(
            rights_status=normalized,
            excluded=True,
            publishable=False,
            reason=f"Excluded because rights status is {normalized}.",
        )

    if key == REVIEW_REQUIRED_STATUS:
        return RightsDecision(
            rights_status=normalized,
            excluded=False,
            publishable=False,
            reason="Included for internal review only; rights require steward review before publication.",
        )

    return RightsDecision(
        rights_status=normalized,
        excluded=False,
        publishable=True,
        reason=f"Rights status {normalized} permits portfolio consideration.",
    )
