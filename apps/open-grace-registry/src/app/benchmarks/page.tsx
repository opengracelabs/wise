import Link from "next/link";
import { Suspense } from "react";
import { LifecycleBadge } from "@/components/LifecycleBadge";
import { ReferenceModelTags } from "@/components/ReferenceModelTags";
import { SearchFilterBar } from "@/components/SearchFilterBar";
import { getBenchmarkScore, loadRegistryData } from "@/lib/data";
import { filterBenchmarks, uniqueValues } from "@/lib/search";

interface PageProps {
  searchParams: Promise<{ q?: string; stage?: string; ref?: string }>;
}

export default async function BenchmarksPage({ searchParams }: PageProps) {
  const params = await searchParams;
  const data = loadRegistryData();
  const benchmarks = filterBenchmarks(data.benchmarks, {
    query: params.q,
    lifecycleStage: params.stage,
    referenceModel: params.ref,
  });

  const stages = uniqueValues(data.benchmarks, (b) => b.lifecycle_stage);
  const refs = uniqueValues(
    data.benchmarks.flatMap((b) => b.reference_models),
    (r) => r,
  );

  return (
    <>
      <div className="page-header">
        <h1>Benchmarks</h1>
        <p>{benchmarks.length} of {data.benchmarks.length} benchmark definitions</p>
      </div>
      <Suspense>
        <SearchFilterBar
          basePath="/benchmarks"
          searchPlaceholder="Search benchmarks…"
          filters={[
            { name: "stage", label: "Lifecycle", options: stages.map((v) => ({ value: v, label: v })) },
            { name: "ref", label: "Reference model", options: refs.map((v) => ({ value: v, label: v })) },
          ]}
        />
      </Suspense>
      <table className="registry-table">
        <thead>
          <tr>
            <th>Benchmark</th>
            <th>Agent</th>
            <th>Metric</th>
            <th>Score</th>
            <th>Lifecycle</th>
          </tr>
        </thead>
        <tbody>
          {benchmarks.map((benchmark) => {
            const score = getBenchmarkScore(benchmark.benchmark_id);
            return (
              <tr key={benchmark.benchmark_id}>
                <td>
                  <Link href={`/benchmarks/${encodeURIComponent(benchmark.benchmark_id)}`}>
                    <strong>{benchmark.display_name}</strong>
                  </Link>
                  <p className="muted">{benchmark.benchmark_id}</p>
                </td>
                <td>
                  <Link href={`/agents/${encodeURIComponent(benchmark.agent_id)}`}>
                    {benchmark.agent_id}
                  </Link>
                </td>
                <td>{benchmark.metric}</td>
                <td>
                  {score ? (
                    <span className={`outcome ${score.passed ? "pass" : "fail"}`}>
                      {score.observed_value} {score.unit}
                    </span>
                  ) : (
                    "—"
                  )}
                </td>
                <td>
                  <LifecycleBadge stage={benchmark.lifecycle_stage} />
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </>
  );
}
