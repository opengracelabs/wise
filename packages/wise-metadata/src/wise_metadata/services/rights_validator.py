"""Rights validation against registry licenses and RightsStatements.org."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from wise_registry.models.license import License
from wise_registry.models.rights_status import RightsStatus

from wise_metadata.enums import ValidationDomain, ValidationStatus
from wise_metadata.evidence import build_evidence_profile, evidence_profile_to_json


@dataclass
class RightsValidationOutcome:
    status: ValidationStatus
    severity: str
    findings: list[dict]
    evidence: dict
    license_id: UUID | None
    rights_status_id: UUID | None


def validate_rights(
    *,
    rights_uri: str | None,
    license: License | None,
    rights_status: RightsStatus | None,
    source_registry_ref: str,
    provenance_event_id: UUID | None = None,
) -> RightsValidationOutcome:
    """Validate machine-readable rights metadata is present and consistent."""
    findings: list[dict] = []
    status = ValidationStatus.PASS
    severity = "info"

    if not rights_uri:
        findings.append({"code": "missing_rights_uri", "message": "dcterms:rights URI is required"})
        status = ValidationStatus.FAIL
        severity = "blocker"
    elif not (
        rights_uri.startswith("http://creativecommons.org/")
        or rights_uri.startswith("https://creativecommons.org/")
        or rights_uri.startswith("http://rightsstatements.org/")
        or rights_uri.startswith("https://rightsstatements.org/")
        or rights_uri.startswith("https://opendatacommons.org/")
    ):
        findings.append({"code": "unrecognized_rights_uri", "message": f"Unrecognized rights URI: {rights_uri}"})
        status = ValidationStatus.WARN
        severity = "warning"

    if license is None and rights_status is None:
        findings.append(
            {
                "code": "no_registry_rights_binding",
                "message": "Neither license nor rights status linked from Source Registry",
            }
        )
        if status != ValidationStatus.FAIL:
            status = ValidationStatus.WARN
            severity = "warning"

    evidence_uris = [u for u in [rights_uri, license.uri if license else None] if u]
    evidence = evidence_profile_to_json(
        build_evidence_profile(
            evidence_uris=evidence_uris or [source_registry_ref],
            confidence=1.0 if status == ValidationStatus.PASS else 0.6,
            evidence_summary="Rights validation against Source Registry license and rights status",
            method="rule-based",
            source_registry_refs=[source_registry_ref],
            provenance_event_id=provenance_event_id,
        )
    )

    return RightsValidationOutcome(
        status=status,
        severity=severity,
        findings=findings,
        evidence=evidence,
        license_id=license.id if license else None,
        rights_status_id=rights_status.id if rights_status else None,
    )


def validation_domain() -> ValidationDomain:
    return ValidationDomain.RIGHTS
