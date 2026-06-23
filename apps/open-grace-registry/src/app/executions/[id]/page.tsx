import Link from "next/link";
import { notFound } from "next/navigation";
import { AuditTimeline } from "@/components/AuditTimeline";
import { BackLink, DetailSection, MetaGrid } from "@/components/DetailSection";
import { BenchmarkScoreCard } from "@/components/BenchmarkScoreCard";
import {
  getAuditForExecution,
  getBenchmarkRunsForExecution,
  getCapabilitiesForExecution,
  getExecution,
  loadRegistryData,
} from "@/lib/data";

interface PageProps {
  params: Promise<{ id: string }>;
}

export function generateStaticParams() {
  return loadRegistryData().executions.map((e) => ({ id: e.run_id }));
}

export default async function ExecutionDetailPage({ params }: PageProps) {
  const { id } = await params;
  const execution = getExecution(decodeURIComponent(id));
  if (!execution) notFound();

  const benchmarkRuns = getBenchmarkRunsForExecution(execution.run_id);
  const capabilities = getCapabilitiesForExecution(execution);
  const audit = getAuditForExecution(execution);

  return (
    <>
      <BackLink href="/executions" label="All executions" />
      <div className="page-header">
        <h1>{execution.run_id}</h1>
        <p className="muted">
          Agent{" "}
          <Link href={`/agents/${encodeURIComponent(execution.agent_id)}`}>
            {execution.agent_id}
          </Link>
        </p>
      </div>

      <MetaGrid
        items={[
          { label: "Status", value: <span className={`outcome ${execution.status}`}>{execution.status}</span> },
          { label: "Model", value: execution.model_id ?? "—" },
          {
            label: "Capabilities",
            value:
              capabilities.length > 0
                ? capabilities.map((c) => c.name).join(", ")
                : execution.capability_class_ids.join(", ") || "—",
          },
          { label: "Started", value: new Date(execution.started_at).toLocaleString() },
          {
            label: "Completed",
            value: execution.completed_at
              ? new Date(execution.completed_at).toLocaleString()
              : "—",
          },
          { label: "Output", value: execution.output_ref ?? "—" },
          { label: "Audit", value: execution.audit_id ?? "—" },
        ]}
      />

      {benchmarkRuns.length > 0 && (
        <DetailSection title="Benchmark scores">
          {benchmarkRuns.map((run) => (
            <BenchmarkScoreCard
              key={run.benchmark_run_id}
              score={{
                benchmark_id: run.benchmark_id,
                agent_id: run.agent_id,
                metric: "observed",
                observed_value: run.observed_value,
                passed: run.passed,
                reason: run.reason,
                unit: "ratio",
                threshold_min: null,
                threshold_max: null,
                display_name: run.benchmark_id,
              }}
            />
          ))}
        </DetailSection>
      )}

      <DetailSection title="Gate results">
        <table className="registry-table">
          <thead>
            <tr>
              <th>Gate</th>
              <th>Passed</th>
              <th>Errors</th>
            </tr>
          </thead>
          <tbody>
            {execution.gate_results.map((gate) => (
              <tr key={gate.gate_name}>
                <td>{gate.gate_name}</td>
                <td>{gate.passed ? "yes" : "no"}</td>
                <td>{gate.errors.length ? gate.errors.join("; ") : "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </DetailSection>

      {audit && (
        <DetailSection title="Audit record">
          <AuditTimeline audits={[audit]} />
        </DetailSection>
      )}
    </>
  );
}
