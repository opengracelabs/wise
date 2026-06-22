"""Unit tests for Source Registry enumerations."""

from __future__ import annotations

import enum

from wise_registry.enums import (
    ApprovalWorkflowStatus,
    ProvenanceEventType,
    TrustLevel,
    VerificationStatus,
)


def test_trust_level_values():
    assert TrustLevel.AUTHORITATIVE.value == "authoritative"
    assert TrustLevel.UNVERIFIED.value == "unverified"
    assert len(TrustLevel) == 5


def test_provenance_event_type_values():
    assert ProvenanceEventType.REGISTER.value == "register"
    assert ProvenanceEventType.HARVEST.value == "harvest"
    assert len(ProvenanceEventType) == 6


def test_verification_status_values():
    assert VerificationStatus.PENDING.value == "pending"
    assert VerificationStatus.VERIFIED.value == "verified"
    assert VerificationStatus.FAILED.value == "failed"


def test_approval_workflow_status_values():
    assert ApprovalWorkflowStatus.PENDING.value == "pending"
    assert ApprovalWorkflowStatus.APPROVED.value == "approved"
    assert ApprovalWorkflowStatus.REJECTED.value == "rejected"
    assert ApprovalWorkflowStatus.REVOKED.value == "revoked"


def test_all_enums_are_str_enums():
    for enum_cls in (
        TrustLevel,
        ProvenanceEventType,
        VerificationStatus,
        ApprovalWorkflowStatus,
    ):
        assert issubclass(enum_cls, str)
        assert issubclass(enum_cls, enum.Enum)
