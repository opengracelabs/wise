import Link from "next/link";
import { Suspense } from "react";
import { LifecycleBadge } from "@/components/LifecycleBadge";
import { SearchFilterBar } from "@/components/SearchFilterBar";
import { loadRegistryData } from "@/lib/data";
import { filterAudits, uniqueValues } from "@/lib/search";

interface PageProps {
  searchParams: Promise<{ q?: string; stage?: string; outcome?: string }>;
}

export default async function AuditsPage({ searchParams }: PageProps) {
  const params = await searchParams;
  const data = loadRegistryData();
  const audits = filterAudits(data.audits, {
    query: params.q,
    lifecycleStage: params.stage,
    outcome: params.outcome,
  });

  const stages = uniqueValues(data.audits, (a) => a.lifecycle_stage);
  const outcomes = uniqueValues(data.audits, (a) => a.outcome);

  return (
    <>
      <div className="page-header">
        <h1>Audits</h1>
        <p>{audits.length} of {data.audits.length} audit records</p>
      </div>
      <Suspense>
        <SearchFilterBar
          basePath="/audits"
          searchPlaceholder="Search audits…"
          filters={[
            { name: "stage", label: "Lifecycle", options: stages.map((v) => ({ value: v, label: v })) },
            { name: "outcome", label: "Outcome", options: outcomes.map((v) => ({ value: v, label: v })) },
          ]}
        />
      </Suspense>
      <table className="registry-table">
        <thead>
          <tr>
            <th>Audit</th>
            <th>Subject</th>
            <th>Outcome</th>
            <th>Reviewer</th>
            <th>Lifecycle</th>
          </tr>
        </thead>
        <tbody>
          {audits.map((audit) => (
            <tr key={audit.audit_id}>
              <td>
                <Link href={`/audits/${encodeURIComponent(audit.audit_id)}`}>
                  <strong>{audit.display_name}</strong>
                </Link>
                <p className="muted">{audit.audit_id}</p>
              </td>
              <td>
                <span className="tag">{audit.subject_type}</span>{" "}
                {audit.subject_id}
              </td>
              <td>
                <span className={`outcome ${audit.outcome}`}>{audit.outcome}</span>
              </td>
              <td>{audit.reviewer_id ?? "—"}</td>
              <td>
                <LifecycleBadge stage={audit.lifecycle_stage} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}
