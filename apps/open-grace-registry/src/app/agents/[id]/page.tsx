import Link from "next/link";
import { notFound } from "next/navigation";
import { AuditTimeline } from "@/components/AuditTimeline";
import { BackLink, DetailSection, MetaGrid } from "@/components/DetailSection";
import { BenchmarkScoreCard } from "@/components/BenchmarkScoreCard";
import { LifecycleBadge } from "@/components/LifecycleBadge";
import { ReferenceModelTags } from "@/components/ReferenceModelTags";
import {
  getAgent,
  getAuditsForSubject,
  getBenchmarkScoresForAgent,
  getCapabilitiesForAgent,
  loadRegistryData,
} from "@/lib/data";

interface PageProps {
  params: Promise<{ id: string }>;
}

export function generateStaticParams() {
  return loadRegistryData().agents.map((agent) => ({
    id: agent.agent_id,
  }));
}

export default async function AgentDetailPage({ params }: PageProps) {
  const { id } = await params;
  const agent = getAgent(decodeURIComponent(id));
  if (!agent) notFound();

  const capabilities = getCapabilitiesForAgent(agent.agent_id);
  const scores = getBenchmarkScoresForAgent(agent.agent_id);
  const audits = getAuditsForSubject(agent.agent_id);

  return (
    <>
      <BackLink href="/agents" label="All agents" />
      <div className="page-header">
        <h1>{agent.display_name}</h1>
        <p className="muted">{agent.agent_id}</p>
      </div>

      <MetaGrid
        items={[
          { label: "Lifecycle", value: <LifecycleBadge stage={agent.lifecycle_stage} /> },
          { label: "Plane", value: agent.plane },
          { label: "Build phase", value: agent.build_phase ?? "—" },
          { label: "Service", value: agent.service_binding ?? "—" },
          { label: "LangGraph", value: agent.langgraph_graph_id },
          { label: "Read only", value: agent.read_only ? "yes" : "no" },
          { label: "Steward", value: agent.steward_actor ?? "—" },
          { label: "Reference models", value: <ReferenceModelTags slugs={agent.reference_models} /> },
        ]}
      />

      <DetailSection title="Specification">
        <p>{agent.spec_path}</p>
        <p className="muted">Output schema: {agent.output_schema_uri}</p>
      </DetailSection>

      {capabilities.length > 0 && (
        <DetailSection title="Capability bindings">
          <ul>
            {capabilities.map((cap) => (
              <li key={cap.id}>
                <Link href={`/capabilities/${encodeURIComponent(cap.id)}`}>{cap.name}</Link>
              </li>
            ))}
          </ul>
        </DetailSection>
      )}

      {scores.length > 0 && (
        <DetailSection title="Benchmark scores">
          {scores.map((score) => (
            <BenchmarkScoreCard key={score.benchmark_id} score={score} />
          ))}
        </DetailSection>
      )}

      <DetailSection title="Audit history">
        <AuditTimeline audits={audits} />
      </DetailSection>
    </>
  );
}
