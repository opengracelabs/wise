"""Unit tests for discovery enumerations."""

from wise_discovery.enums import ApprovalStatus, ReachabilityStatus, ValidationStatus


def test_approval_status_values():
    assert ApprovalStatus.PROPOSED.value == "proposed"
    assert len(ApprovalStatus) == 4


def test_validation_status_values():
    assert {member.value for member in ValidationStatus} == {"pass", "warn", "fail"}


def test_reachability_status_values():
    assert ReachabilityStatus.REACHABLE.value == "reachable"
