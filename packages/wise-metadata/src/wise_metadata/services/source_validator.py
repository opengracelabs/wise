"""Source validation against Source Registry."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from wise_registry.enums import TrustLevel
from wise_registry.models.source import Source

from wise_metadata.enums import ValidationDomain, ValidationStatus
from wise_metadata.evidence import build_evidence_profile, evidence_profile_to_json


@dataclass
class SourceValidationOutcome:
    status: ValidationStatus
    severity: str
    findings: list[dict]
    evidence: dict


def validate_source(
    source: Source,
    *,
    source_registry_ref: str,
    provenance_event_id: UUID | None = None,
) -> SourceValidationOutcome:
    """Validate registered source is active and meets trust requirements."""
    findings: list[dict] = []
    status = ValidationStatus.PASS
    severity = "info"

    if not source.active:
        findings.append({"code": "source_inactive", "message": "Source is not active"})
        status = ValidationStatus.FAIL
        severity = "blocker"

    if source.trust_level == TrustLevel.UNVERIFIED:
        findings.append({"code": "trust_unverified", "message": "Source trust level is unverified"})
        status = ValidationStatus.WARN
        severity = "warning"

    if not source.homepage_url:
        findings.append({"code": "missing_homepage", "message": "Source homepage URL is missing"})
        status = ValidationStatus.WARN
        severity = "warning"

    evidence = evidence_profile_to_json(
        build_evidence_profile(
            evidence_uris=[source.homepage_url],
            confidence=1.0 if status == ValidationStatus.PASS else 0.5,
            evidence_summary=f"Source validation for {source.canonical_name}",
            method="rule-based",
            source_registry_refs=[source_registry_ref],
            provenance_event_id=provenance_event_id,
        )
    )

    return SourceValidationOutcome(
        status=status,
        severity=severity,
        findings=findings,
        evidence=evidence,
    )


def validation_domain() -> ValidationDomain:
    return ValidationDomain.SOURCE
