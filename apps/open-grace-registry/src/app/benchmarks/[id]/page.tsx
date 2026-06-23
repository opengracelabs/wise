import Link from "next/link";
import { notFound } from "next/navigation";
import { BackLink, DetailSection, MetaGrid } from "@/components/DetailSection";
import { BenchmarkScoreCard } from "@/components/BenchmarkScoreCard";
import { LifecycleBadge } from "@/components/LifecycleBadge";
import { ReferenceModelTags } from "@/components/ReferenceModelTags";
import { getBenchmark, getBenchmarkScore, loadRegistryData } from "@/lib/data";

interface PageProps {
  params: Promise<{ id: string }>;
}

export function generateStaticParams() {
  return loadRegistryData().benchmarks.map((b) => ({ id: b.benchmark_id }));
}

export default async function BenchmarkDetailPage({ params }: PageProps) {
  const { id } = await params;
  const benchmark = getBenchmark(decodeURIComponent(id));
  if (!benchmark) notFound();

  const score = getBenchmarkScore(benchmark.benchmark_id);

  return (
    <>
      <BackLink href="/benchmarks" label="All benchmarks" />
      <div className="page-header">
        <h1>{benchmark.display_name}</h1>
        <p className="muted">{benchmark.benchmark_id}</p>
      </div>

      <MetaGrid
        items={[
          { label: "Lifecycle", value: <LifecycleBadge stage={benchmark.lifecycle_stage} /> },
          { label: "Agent", value: (
            <Link href={`/agents/${encodeURIComponent(benchmark.agent_id)}`}>
              {benchmark.agent_id}
            </Link>
          ) },
          { label: "Metric", value: benchmark.metric },
          { label: "Unit", value: benchmark.unit },
          { label: "Threshold min", value: benchmark.threshold_min ?? "—" },
          { label: "Threshold max", value: benchmark.threshold_max ?? "—" },
          { label: "Gold dataset", value: benchmark.gold_dataset_ref ?? "—" },
          { label: "Reference models", value: <ReferenceModelTags slugs={benchmark.reference_models} /> },
        ]}
      />

      <DetailSection title="Observed score">
        {score ? <BenchmarkScoreCard score={score} /> : (
          <p className="muted">No observed score recorded.</p>
        )}
      </DetailSection>
    </>
  );
}
