"""Source Discovery Agent v1 service layer."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Protocol
from uuid import UUID

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session

from wise_discovery.enums import ApprovalStatus, ReachabilityStatus, ValidationStatus
from wise_discovery.evidence import build_evidence_profile, evidence_profile_to_json
from wise_discovery.models.discovery_record import DiscoveryRecord
from wise_discovery.provenance import AGENT_VERSION, append_provenance_event
from wise_discovery.schemas.discovery_record import (
    DiscoveryRecordCreate,
    ReachabilityResult,
    RightsPosture,
    SourceValidationResult,
)
from wise_discovery.schemas.evidence import EvidenceProfile
from wise_registry.enums import ProvenanceEventType, TrustLevel
from wise_registry.models.license import License
from wise_registry.models.source import Source


class HttpClient(Protocol):
    def head(self, url: str, *, timeout: float) -> httpx.Response: ...

    def get(self, url: str, *, timeout: float) -> httpx.Response: ...


def source_registry_ref(source: Source) -> str:
    return source.stable_id or source.canonical_name


def lookup_source(
    session: Session,
    *,
    source_id: UUID | None = None,
    canonical_name: str | None = None,
    stable_id: str | None = None,
) -> Source:
    """Resolve a registered source from the Source Registry."""
    if sum(1 for value in (source_id, canonical_name, stable_id) if value is not None) != 1:
        raise ValueError("Exactly one of source_id, canonical_name, or stable_id is required")

    if source_id is not None:
        source = session.get(Source, source_id)
    elif canonical_name is not None:
        source = session.scalar(select(Source).where(Source.canonical_name == canonical_name))
    else:
        source = session.scalar(select(Source).where(Source.stable_id == stable_id))

    if source is None:
        key = source_id or canonical_name or stable_id
        raise KeyError(f"Source Registry missing source: {key!r}")
    return source


def validate_source(
    source: Source,
    *,
    source_registry_ref_value: str | None = None,
    require_license: bool = False,
    provenance_event_id: UUID | None = None,
) -> SourceValidationResult:
    """Validate registered source is active and meets trust requirements."""
    findings: list[dict] = []
    status = ValidationStatus.PASS
    severity = "info"
    ref = source_registry_ref_value or source_registry_ref(source)

    if not source.active:
        findings.append({"code": "source_inactive", "message": "Source is not active"})
        status = ValidationStatus.FAIL
        severity = "blocker"

    if source.trust_level == TrustLevel.UNVERIFIED:
        findings.append({"code": "trust_unverified", "message": "Source trust level is unverified"})
        if status != ValidationStatus.FAIL:
            status = ValidationStatus.WARN
            severity = "warning"

    if require_license and source.license_id is None:
        findings.append({"code": "missing_license", "message": "Source license is required"})
        status = ValidationStatus.FAIL
        severity = "blocker"

    if not source.homepage_url:
        findings.append({"code": "missing_homepage", "message": "Source homepage URL is missing"})
        if status == ValidationStatus.PASS:
            status = ValidationStatus.WARN
            severity = "warning"

    evidence = build_evidence_profile(
        evidence_uris=[source.homepage_url] if source.homepage_url else [ref],
        confidence=1.0 if status == ValidationStatus.PASS else 0.5,
        evidence_summary=f"Source validation for {source.canonical_name}",
        method="rule-based",
        source_registry_refs=[ref],
        provenance_event_id=provenance_event_id,
    )

    return SourceValidationResult(
        status=status.value,
        severity=severity,
        findings=findings,
        evidence=evidence,
    )


def check_reachability(
    source: Source,
    *,
    client: HttpClient | None = None,
    timeout: float = 10.0,
) -> ReachabilityResult:
    """HTTP HEAD/GET reachability check on api_url or homepage_url."""
    url = source.api_url or source.homepage_url
    if not url:
        return ReachabilityResult(
            status=ReachabilityStatus.SKIPPED.value,
            url_checked=None,
            error="No api_url or homepage_url configured",
        )

    owns_client = client is None
    http = client or httpx.Client(follow_redirects=True)
    try:
        try:
            response = http.head(url, timeout=timeout)
            if response.status_code >= 400:
                response = http.get(url, timeout=timeout)
        except httpx.HTTPError:
            response = http.get(url, timeout=timeout)

        if response.status_code < 400:
            return ReachabilityResult(
                status=ReachabilityStatus.REACHABLE.value,
                url_checked=url,
                http_status=response.status_code,
            )
        return ReachabilityResult(
            status=ReachabilityStatus.UNREACHABLE.value,
            url_checked=url,
            http_status=response.status_code,
            error=f"HTTP {response.status_code}",
        )
    except httpx.HTTPError as exc:
        return ReachabilityResult(
            status=ReachabilityStatus.UNREACHABLE.value,
            url_checked=url,
            error=str(exc),
        )
    finally:
        if owns_client:
            http.close()


def propagate_rights_posture(source: Source) -> RightsPosture:
    """Propagate rights posture from source license metadata."""
    license_: License | None = source.license
    license_uri = license_.uri if license_ else None
    license_code = license_.code if license_ else None
    rights_uri = license_uri

    if license_uri:
        summary = f"Source licensed under {license_code or license_uri}"
    else:
        summary = "No license registered; rights posture unknown — steward review required"
        rights_uri = None

    return RightsPosture(
        rights_uri=rights_uri,
        license_uri=license_uri,
        license_code=license_code,
        source_registry_ref=source_registry_ref(source),
        summary=summary,
    )


def create_discovery_record(
    session: Session,
    *,
    payload: DiscoveryRecordCreate,
    source: Source | None = None,
    skip_reachability: bool = False,
    require_license: bool = False,
    http_client: HttpClient | None = None,
) -> DiscoveryRecord:
    """Create a HARVEST provenance event and discovery record with evidence profile."""
    resolved_source = source or lookup_source(session, source_id=payload.source_id)
    ref = source_registry_ref(resolved_source)

    validation = validate_source(
        resolved_source,
        source_registry_ref_value=ref,
        require_license=require_license,
    )
    if validation.status == ValidationStatus.FAIL.value:
        codes = ", ".join(finding["code"] for finding in validation.findings)
        raise ValueError(f"Source validation failed: {codes}")

    if not skip_reachability:
        reachability = check_reachability(resolved_source, client=http_client)
        if reachability.status == ReachabilityStatus.UNREACHABLE.value:
            raise ValueError(
                f"Source unreachable at {reachability.url_checked}: {reachability.error}"
            )

    rights = propagate_rights_posture(resolved_source)
    rights_uri = payload.rights_uri or rights.rights_uri

    provenance_event = append_provenance_event(
        session,
        source_id=resolved_source.id,
        event_type=ProvenanceEventType.HARVEST,
        evidence_uris=payload.evidence_uris,
        notes=f"Discovery record {payload.stable_id}",
    )

    profile = build_evidence_profile(
        evidence_uris=payload.evidence_uris,
        confidence=payload.confidence,
        evidence_summary=payload.evidence_summary,
        method=payload.method,
        source_registry_refs=[ref],
        provenance_event_id=provenance_event.id,
    )

    now = datetime.now(timezone.utc)
    record = DiscoveryRecord(
        stable_id=payload.stable_id,
        source_id=resolved_source.id,
        source_record_uri=payload.source_record_uri,
        raw_payload_ref=payload.raw_payload_ref,
        discovery_timestamp=now,
        confidence=payload.confidence,
        approval_status=payload.approval_status,
        provenance_event_id=provenance_event.id,
        evidence_uris=payload.evidence_uris,
        title=payload.title,
        source_registry_ref=ref,
        rights_uri=rights_uri,
        ingestion_candidacy_score=payload.confidence,
        external_identifiers=payload.external_identifiers,
        record_data=payload.record_data or {
            "evidence": evidence_profile_to_json(profile),
            "rights_posture": rights.model_dump(mode="json"),
        },
        discovery_event_id=f"discovery-{payload.stable_id}-{now.strftime('%Y%m%d')}",
        created_by=payload.audit.created_by,
        updated_by=payload.audit.updated_by,
    )
    session.add(record)
    session.flush()
    return record
