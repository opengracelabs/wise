"""Enumerations for Reference Capability 1 schemas."""

from enum import StrEnum


class ApprovalStatus(StrEnum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"
