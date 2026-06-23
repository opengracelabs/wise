import Link from "next/link";
import { Suspense } from "react";
import { LifecycleBadge } from "@/components/LifecycleBadge";
import { ReferenceModelTags } from "@/components/ReferenceModelTags";
import { SearchFilterBar } from "@/components/SearchFilterBar";
import { loadRegistryData } from "@/lib/data";
import { filterModels, uniqueValues } from "@/lib/search";

interface PageProps {
  searchParams: Promise<{ q?: string; stage?: string; ref?: string }>;
}

export default async function ModelsPage({ searchParams }: PageProps) {
  const params = await searchParams;
  const data = loadRegistryData();
  const models = filterModels(data.models, {
    query: params.q,
    lifecycleStage: params.stage,
    referenceModel: params.ref,
  });

  const stages = uniqueValues(data.models, (m) => m.lifecycle_stage);
  const refs = uniqueValues(
    data.models.flatMap((m) => m.reference_models),
    (r) => r,
  );

  return (
    <>
      <div className="page-header">
        <h1>Models</h1>
        <p>{models.length} of {data.models.length} council models</p>
      </div>
      <Suspense>
        <SearchFilterBar
          basePath="/models"
          searchPlaceholder="Search models…"
          filters={[
            { name: "stage", label: "Lifecycle", options: stages.map((v) => ({ value: v, label: v })) },
            { name: "ref", label: "Reference model", options: refs.map((v) => ({ value: v, label: v })) },
          ]}
        />
      </Suspense>
      <table className="registry-table">
        <thead>
          <tr>
            <th>Model</th>
            <th>Provider</th>
            <th>Council role</th>
            <th>Safety tier</th>
            <th>Reference models</th>
          </tr>
        </thead>
        <tbody>
          {models.map((model) => (
            <tr key={model.model_id}>
              <td>
                <Link href={`/models/${encodeURIComponent(model.model_id)}`}>
                  <strong>{model.model_name}</strong>
                </Link>
                <p className="muted">{model.model_id}</p>
              </td>
              <td>{model.provider}</td>
              <td>{model.council_role ?? "—"}</td>
              <td>
                <span className="tag">{model.safety_tier}</span>
              </td>
              <td>
                <ReferenceModelTags slugs={model.reference_models} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}
