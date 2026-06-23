import Link from "next/link";
import { Suspense } from "react";
import { LifecycleBadge } from "@/components/LifecycleBadge";
import { ReferenceModelTags } from "@/components/ReferenceModelTags";
import { SearchFilterBar } from "@/components/SearchFilterBar";
import { loadRegistryData } from "@/lib/data";
import { filterCapabilities, uniqueValues } from "@/lib/search";

interface PageProps {
  searchParams: Promise<{ q?: string; stage?: string; ref?: string }>;
}

export default async function CapabilitiesPage({ searchParams }: PageProps) {
  const params = await searchParams;
  const data = loadRegistryData();
  const capabilities = filterCapabilities(data.capabilities, {
    query: params.q,
    lifecycleStage: params.stage,
    referenceModel: params.ref,
  });

  const stages = uniqueValues(data.capabilities, (c) => c.lifecycle_stage);
  const refs = uniqueValues(
    data.capabilities.flatMap((c) => c.reference_models),
    (r) => r,
  );

  return (
    <>
      <div className="page-header">
        <h1>Capabilities</h1>
        <p>{capabilities.length} of {data.capabilities.length} capability classes</p>
      </div>
      <Suspense>
        <SearchFilterBar
          basePath="/capabilities"
          searchPlaceholder="Search capabilities…"
          filters={[
            { name: "stage", label: "Lifecycle", options: stages.map((v) => ({ value: v, label: v })) },
            { name: "ref", label: "Reference model", options: refs.map((v) => ({ value: v, label: v })) },
          ]}
        />
      </Suspense>
      <table className="registry-table">
        <thead>
          <tr>
            <th>Capability</th>
            <th>Owner</th>
            <th>Lifecycle</th>
            <th>Benchmarks</th>
            <th>Reference models</th>
          </tr>
        </thead>
        <tbody>
          {capabilities.map((cap) => (
            <tr key={cap.id}>
              <td>
                <Link href={`/capabilities/${encodeURIComponent(cap.id)}`}>
                  <strong>{cap.name}</strong>
                </Link>
                <p className="muted">{cap.id}</p>
              </td>
              <td>{cap.owner}</td>
              <td>
                <LifecycleBadge stage={cap.lifecycle_stage} />
              </td>
              <td>{cap.benchmark_set.length}</td>
              <td>
                <ReferenceModelTags slugs={cap.reference_models} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}
