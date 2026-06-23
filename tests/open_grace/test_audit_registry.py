from open_grace_audit import AuditRegistry, record_lifecycle_audit
from open_grace_governance.lifecycle import LifecycleStage


def test_record_lifecycle_audit(tmp_path):
    registry = AuditRegistry(tmp_path / "audits.json")
    entry = record_lifecycle_audit(
        registry,
        subject_type="agent",
        subject_id="wise.agent.standards",
        from_stage=LifecycleStage.APPROVAL,
        to_stage=LifecycleStage.PUBLICATION,
        reviewer_id="architecture-office",
        evidence_ref="otel://traces/abc123",
        trace_id="abc123",
    )

    assert entry.audit_id.startswith("wise.audit.")
    assert registry.for_subject("wise.agent.standards")
