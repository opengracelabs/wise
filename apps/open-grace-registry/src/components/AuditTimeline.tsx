import type { AuditRecord } from "@/lib/types";
import { LifecycleBadge } from "./LifecycleBadge";

export function AuditTimeline({ audits }: { audits: AuditRecord[] }) {
  if (!audits.length) {
    return <p className="muted">No audit records for this subject.</p>;
  }

  const sorted = [...audits].sort(
    (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime(),
  );

  return (
    <ol className="audit-timeline">
      {sorted.map((audit) => (
        <li key={audit.audit_id}>
          <div className="audit-row">
            <div>
              <strong>{audit.display_name}</strong>
              <p className="muted">{audit.audit_id}</p>
            </div>
            <div className="audit-meta">
              <span className={`outcome ${audit.outcome}`}>{audit.outcome}</span>
              <LifecycleBadge stage={audit.lifecycle_stage} />
            </div>
          </div>
          <p className="muted">
            reviewer: {audit.reviewer_id ?? "—"} · evidence: {audit.evidence_ref}
          </p>
          <p className="muted">{new Date(audit.created_at).toLocaleString()}</p>
        </li>
      ))}
    </ol>
  );
}
