import Link from "next/link";
import { notFound } from "next/navigation";
import { BackLink, DetailSection, MetaGrid } from "@/components/DetailSection";
import { LifecycleBadge } from "@/components/LifecycleBadge";
import { ReferenceModelTags } from "@/components/ReferenceModelTags";
import { getAudit, loadRegistryData } from "@/lib/data";

interface PageProps {
  params: Promise<{ id: string }>;
}

export function generateStaticParams() {
  return loadRegistryData().audits.map((a) => ({ id: a.audit_id }));
}

function subjectHref(subjectType: string, subjectId: string): string | null {
  switch (subjectType) {
    case "agent":
      return `/agents/${encodeURIComponent(subjectId)}`;
    case "capability":
      return `/capabilities/${encodeURIComponent(subjectId)}`;
    case "model":
      return `/models/${encodeURIComponent(subjectId)}`;
    case "benchmark":
      return `/benchmarks/${encodeURIComponent(subjectId)}`;
    default:
      return null;
  }
}

export default async function AuditDetailPage({ params }: PageProps) {
  const { id } = await params;
  const audit = getAudit(decodeURIComponent(id));
  if (!audit) notFound();

  const subjectLink = subjectHref(audit.subject_type, audit.subject_id);

  return (
    <>
      <BackLink href="/audits" label="All audits" />
      <div className="page-header">
        <h1>{audit.display_name}</h1>
        <p className="muted">{audit.audit_id}</p>
      </div>

      <MetaGrid
        items={[
          { label: "Outcome", value: <span className={`outcome ${audit.outcome}`}>{audit.outcome}</span> },
          { label: "Lifecycle", value: <LifecycleBadge stage={audit.lifecycle_stage} /> },
          { label: "Subject type", value: audit.subject_type },
          {
            label: "Subject",
            value: subjectLink ? (
              <Link href={subjectLink}>{audit.subject_id}</Link>
            ) : (
              audit.subject_id
            ),
          },
          { label: "Reviewer", value: audit.reviewer_id ?? "—" },
          { label: "Evidence", value: audit.evidence_ref },
          { label: "Trace", value: audit.trace_id ?? "—" },
          { label: "Recorded", value: new Date(audit.created_at).toLocaleString() },
          { label: "Reference models", value: <ReferenceModelTags slugs={audit.reference_models} /> },
        ]}
      />

      <DetailSection title="Steward">
        <p>{audit.steward_actor ?? "—"}</p>
      </DetailSection>
    </>
  );
}
