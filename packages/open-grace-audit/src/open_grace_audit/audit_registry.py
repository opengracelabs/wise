"""Audit registry and lifecycle evidence trail."""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from open_grace_governance.lifecycle import LifecycleStage
from open_grace_governance.schemas import AuditRegistryRecord
from open_grace_governance.store.base import JsonRegistryStore
from open_grace_governance.validation import validate_entry

_PACKAGE_DATA = Path(__file__).resolve().parent / "data"


class AuditRegistry:
    def __init__(self, store_path: Path | None = None) -> None:
        self._store = JsonRegistryStore(
            store_path or _PACKAGE_DATA / "audit_registry.json",
            AuditRegistryRecord,
            "audit_id",
        )

    def list(self) -> list[AuditRegistryRecord]:
        return self._store.all()

    def for_subject(self, subject_id: str) -> list[AuditRegistryRecord]:
        return [record for record in self._store.all() if record.subject_id == subject_id]

    def get(self, audit_id: str) -> AuditRegistryRecord | None:
        return self._store.get(audit_id)

    def record(self, entry: AuditRegistryRecord) -> AuditRegistryRecord:
        result = validate_entry(entry)
        if not result.valid:
            raise ValueError("; ".join(result.errors))
        self._store.upsert(entry)
        self._store.save()
        return entry


def record_lifecycle_audit(
    registry: AuditRegistry,
    *,
    subject_type: str,
    subject_id: str,
    from_stage: LifecycleStage,
    to_stage: LifecycleStage,
    reviewer_id: str,
    evidence_ref: str,
    trace_id: str | None = None,
    outcome: str = "pass",
) -> AuditRegistryRecord:
    """Append an audit record for a lifecycle transition."""
    slug = subject_id.rsplit(".", maxsplit=1)[-1]
    audit_id = f"wise.audit.{slug}-{to_stage.value}-{uuid4().hex[:8]}"
    entry = AuditRegistryRecord(
        audit_id=audit_id,
        display_name=f"Lifecycle {from_stage.value} to {to_stage.value}",
        subject_type=subject_type,  # type: ignore[arg-type]
        subject_id=subject_id,
        evidence_ref=evidence_ref,
        trace_id=trace_id,
        outcome=outcome,  # type: ignore[arg-type]
        reviewer_id=reviewer_id,
        lifecycle_stage=LifecycleStage.AUDIT,
        steward_actor=reviewer_id,
        reference_models=["opentelemetry", "iso-27001"],
    )
    return registry.record(entry)
