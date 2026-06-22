"""Discovery Agent enumerations."""

from enum import StrEnum


class ApprovalStatus(StrEnum):
    """Steward approval workflow states (Quality Review compatible)."""

    PROPOSED = "proposed"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"


class ValidationStatus(StrEnum):
    """Outcome of source validation checks."""

    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


class ReachabilityStatus(StrEnum):
    """Outcome of HTTP reachability probe."""

    REACHABLE = "reachable"
    UNREACHABLE = "unreachable"
    SKIPPED = "skipped"
