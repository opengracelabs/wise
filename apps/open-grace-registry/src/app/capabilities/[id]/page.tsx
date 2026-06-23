import Link from "next/link";
import { notFound } from "next/navigation";
import { AuditTimeline } from "@/components/AuditTimeline";
import { BackLink, DetailSection, MetaGrid } from "@/components/DetailSection";
import { BenchmarkScoreCard } from "@/components/BenchmarkScoreCard";
import { LifecycleBadge } from "@/components/LifecycleBadge";
import { ReferenceModelTags } from "@/components/ReferenceModelTags";
import { RiskRating } from "@/components/RiskRating";
import { StandardsList } from "@/components/StandardsList";
import {
  evaluateCapabilityBenchmarks,
  getAuditsForSubject,
  getCapability,
  getRisksForCapability,
  getStandardsForCapability,
  loadRegistryData,
} from "@/lib/data";

interface PageProps {
  params: Promise<{ id: string }>;
}

export function generateStaticParams() {
  return loadRegistryData().capabilities.map((cap) => ({ id: cap.id }));
}

export default async function CapabilityDetailPage({ params }: PageProps) {
  const { id } = await params;
  const capability = getCapability(decodeURIComponent(id));
  if (!capability) notFound();

  const data = loadRegistryData();
  const risks = getRisksForCapability(capability);
  const standards = getStandardsForCapability(capability);
  const audits = getAuditsForSubject(capability.id);
  const benchmarkResult = evaluateCapabilityBenchmarks(
    capability,
    data.benchmarkScores,
  );

  return (
    <>
      <BackLink href="/capabilities" label="All capabilities" />
      <div className="page-header">
        <h1>{capability.name}</h1>
        <p className="muted">{capability.id}</p>
      </div>

      <MetaGrid
        items={[
          { label: "Lifecycle", value: <LifecycleBadge stage={capability.lifecycle_stage} /> },
          { label: "Owner", value: capability.owner },
          { label: "Benchmark gate", value: benchmarkResult.passed ? "pass" : "fail" },
          { label: "Steward", value: capability.steward_actor ?? "—" },
          { label: "Reference models", value: <ReferenceModelTags slugs={capability.reference_models} /> },
        ]}
      />

      <DetailSection title="Description">
        <p>{capability.description}</p>
      </DetailSection>

      <DetailSection title="Benchmark scores">
        {benchmarkResult.evaluations.length ? (
          benchmarkResult.evaluations.map((score) => (
            <BenchmarkScoreCard key={score.benchmark_id} score={score} />
          ))
        ) : (
          <p className="muted">No observed benchmark scores.</p>
        )}
        {!benchmarkResult.passed && benchmarkResult.failures.length > 0 && (
          <ul>
            {benchmarkResult.failures.map((failure) => (
              <li key={failure} className="muted">{failure}</li>
            ))}
          </ul>
        )}
      </DetailSection>

      <DetailSection title="Risk ratings">
        {risks.length ? risks.map((risk) => <RiskRating key={risk.risk_id} risk={risk} />) : (
          <p className="muted">No risks in profile.</p>
        )}
      </DetailSection>

      <DetailSection title="Standards compliance">
        <StandardsList standards={standards} />
        <p className="muted">Audit requirements: {capability.audit_requirements.join(", ")}</p>
      </DetailSection>

      <DetailSection title="Approved models">
        <ul>
          {capability.approved_models.map((modelId) => (
            <li key={modelId}>
              <Link href={`/models/${encodeURIComponent(modelId)}`}>{modelId}</Link>
            </li>
          ))}
        </ul>
      </DetailSection>

      <DetailSection title="Audit history">
        <AuditTimeline audits={audits} />
      </DetailSection>
    </>
  );
}
