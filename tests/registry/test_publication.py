"""Unit tests for RC17 publication gate helpers."""

from __future__ import annotations

from uuid import uuid4

import pytest

from wise_registry.enums import ApprovalWorkflowStatus, VerificationStatus
from wise_registry.models import Asset
from wise_registry.publication import PublicationGateError, gate_snapshot, require_publishable


def _asset(**overrides) -> Asset:
    values = {
        "stable_id": "asset-1",
        "title": "Asset One",
        "asset_type": "image",
        "source_id": uuid4(),
        "source_verification_status": VerificationStatus.PENDING,
        "license_verification_status": VerificationStatus.PENDING,
        "provenance_verification_status": VerificationStatus.PENDING,
        "rights_approval_status": ApprovalWorkflowStatus.PENDING,
        "publication_approval_status": ApprovalWorkflowStatus.PENDING,
    }
    values.update(overrides)
    return Asset(**values)


def test_gate_snapshot_blocks_default_asset():
    snapshot = gate_snapshot(_asset())

    assert snapshot.publishable is False
    assert snapshot.source_verified is False
    assert snapshot.publication_approved is False


def test_require_publishable_reports_missing_gates():
    with pytest.raises(PublicationGateError, match="source_verified"):
        require_publishable(_asset())


def test_require_publishable_accepts_full_rc17_sequence():
    asset = _asset(
        source_verification_status=VerificationStatus.VERIFIED,
        license_verification_status=VerificationStatus.VERIFIED,
        provenance_verification_status=VerificationStatus.VERIFIED,
        rights_approval_status=ApprovalWorkflowStatus.APPROVED,
        publication_approval_status=ApprovalWorkflowStatus.APPROVED,
    )

    require_publishable(asset)
    assert gate_snapshot(asset).publishable is True
