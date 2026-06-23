"""RC17 publication approval helpers."""

from __future__ import annotations

from dataclasses import dataclass

from wise_registry.enums import ApprovalWorkflowStatus, VerificationStatus
from wise_registry.models.asset import Asset

RC17_GATE_SEQUENCE = (
    "source_verified",
    "license_verified",
    "provenance_verified",
    "rights_approved",
    "publication_approved",
)


class PublicationGateError(ValueError):
    """Raised when an asset is not eligible for publication."""


@dataclass(frozen=True)
class PublicationGateSnapshot:
    """Point-in-time RC17 gate state for publication approval."""

    source_verified: bool
    license_verified: bool
    provenance_verified: bool
    rights_approved: bool
    publication_approved: bool

    @property
    def publishable(self) -> bool:
        return all(
            (
                self.source_verified,
                self.license_verified,
                self.provenance_verified,
                self.rights_approved,
                self.publication_approved,
            )
        )


def gate_snapshot(asset: Asset) -> PublicationGateSnapshot:
    """Build the RC17 publication gate snapshot for an asset."""
    return PublicationGateSnapshot(
        source_verified=asset.source_verification_status == VerificationStatus.VERIFIED,
        license_verified=asset.license_verification_status == VerificationStatus.VERIFIED,
        provenance_verified=asset.provenance_verification_status == VerificationStatus.VERIFIED,
        rights_approved=asset.rights_approval_status == ApprovalWorkflowStatus.APPROVED,
        publication_approved=asset.publication_approval_status == ApprovalWorkflowStatus.APPROVED,
    )


def require_publishable(asset: Asset) -> None:
    """Raise unless the asset has passed every RC17 publication gate."""
    snapshot = gate_snapshot(asset)
    if snapshot.publishable:
        return

    missing = [
        gate
        for gate in RC17_GATE_SEQUENCE
        if not getattr(snapshot, gate)
    ]
    raise PublicationGateError(
        "Asset is not publishable; missing RC17 gates: " + ", ".join(missing)
    )
