"""Rights gating for portfolio candidate selection."""

from __future__ import annotations

from dataclasses import dataclass

from wise_portfolio_intelligence.constants import (
    RIGHTS_ELIGIBILITY_ELIGIBLE,
    RIGHTS_STATUS_RESTRICTED,
    RIGHTS_STATUS_REVIEW_REQUIRED,
    RIGHTS_STATUS_UNKNOWN,
    normalize_rights_status,
    read_rights_status,
    rights_eligibility,
)


@dataclass(frozen=True)
class RightsDecision:
    """Decision produced by the portfolio rights gate."""

    rights_status: str
    eligibility: str
    excluded: bool
    publishable: bool
    reason: str


def rights_gate(rights_status: str | None) -> RightsDecision:
    """Exclude blocked rights and mark review-required assets as not publishable."""

    normalized = normalize_rights_status(rights_status)
    eligibility = rights_eligibility(normalized)

    if normalized in {RIGHTS_STATUS_RESTRICTED, RIGHTS_STATUS_UNKNOWN}:
        return RightsDecision(
            rights_status=normalized,
            eligibility=eligibility,
            excluded=True,
            publishable=False,
            reason=f"Excluded because rights status is {normalized}.",
        )

    if normalized == RIGHTS_STATUS_REVIEW_REQUIRED:
        return RightsDecision(
            rights_status=normalized,
            eligibility=eligibility,
            excluded=False,
            publishable=False,
            reason="Included for internal review only; rights require steward review before publication.",
        )

    return RightsDecision(
        rights_status=normalized,
        eligibility=RIGHTS_ELIGIBILITY_ELIGIBLE,
        excluded=False,
        publishable=True,
        reason=f"Rights status {normalized} permits portfolio consideration.",
    )
