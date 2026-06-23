import Link from "next/link";
import { Suspense } from "react";
import { LifecycleBadge } from "@/components/LifecycleBadge";
import { ReferenceModelTags } from "@/components/ReferenceModelTags";
import { SearchFilterBar } from "@/components/SearchFilterBar";
import { loadRegistryData } from "@/lib/data";
import { filterAgents, uniqueValues } from "@/lib/search";

interface PageProps {
  searchParams: Promise<{ q?: string; stage?: string; plane?: string; ref?: string }>;
}

export default async function AgentsPage({ searchParams }: PageProps) {
  const params = await searchParams;
  const data = loadRegistryData();
  const agents = filterAgents(data.agents, {
    query: params.q,
    lifecycleStage: params.stage,
    plane: params.plane,
    referenceModel: params.ref,
  });

  const stages = uniqueValues(data.agents, (a) => a.lifecycle_stage);
  const planes = uniqueValues(data.agents, (a) => a.plane);
  const refs = uniqueValues(
    data.agents.flatMap((a) => a.reference_models),
    (r) => r,
  );

  return (
    <>
      <div className="page-header">
        <h1>Agents</h1>
        <p>{agents.length} of {data.agents.length} governed agents</p>
      </div>
      <Suspense>
        <SearchFilterBar
          basePath="/agents"
          searchPlaceholder="Search agents…"
          filters={[
            { name: "stage", label: "Lifecycle", options: stages.map((v) => ({ value: v, label: v })) },
            { name: "plane", label: "Plane", options: planes.map((v) => ({ value: v, label: v })) },
            { name: "ref", label: "Reference model", options: refs.map((v) => ({ value: v, label: v })) },
          ]}
        />
      </Suspense>
      <table className="registry-table">
        <thead>
          <tr>
            <th>Agent</th>
            <th>Plane</th>
            <th>Lifecycle</th>
            <th>Service</th>
            <th>Reference models</th>
          </tr>
        </thead>
        <tbody>
          {agents.map((agent) => (
            <tr key={agent.agent_id}>
              <td>
                <Link href={`/agents/${encodeURIComponent(agent.agent_id)}`}>
                  <strong>{agent.display_name}</strong>
                </Link>
                <p className="muted">{agent.agent_id}</p>
              </td>
              <td>{agent.plane}</td>
              <td>
                <LifecycleBadge stage={agent.lifecycle_stage} />
              </td>
              <td>{agent.service_binding ?? "—"}</td>
              <td>
                <ReferenceModelTags slugs={agent.reference_models} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}
