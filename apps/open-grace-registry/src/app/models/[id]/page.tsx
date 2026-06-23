import { notFound } from "next/navigation";
import { BackLink, DetailSection, MetaGrid } from "@/components/DetailSection";
import { LifecycleBadge } from "@/components/LifecycleBadge";
import { ReferenceModelTags } from "@/components/ReferenceModelTags";
import { getModel, loadRegistryData } from "@/lib/data";

interface PageProps {
  params: Promise<{ id: string }>;
}

export function generateStaticParams() {
  return loadRegistryData().models.map((m) => ({ id: m.model_id }));
}

export default async function ModelDetailPage({ params }: PageProps) {
  const { id } = await params;
  const model = getModel(decodeURIComponent(id));
  if (!model) notFound();

  return (
    <>
      <BackLink href="/models" label="All models" />
      <div className="page-header">
        <h1>{model.model_name}</h1>
        <p className="muted">{model.model_id}</p>
      </div>

      <MetaGrid
        items={[
          { label: "Lifecycle", value: <LifecycleBadge stage={model.lifecycle_stage} /> },
          { label: "Provider", value: model.provider },
          { label: "Council role", value: model.council_role ?? "—" },
          { label: "Safety tier", value: model.safety_tier },
          { label: "Allowed planes", value: model.allowed_planes.join(", ") },
          { label: "Steward", value: model.steward_actor ?? "—" },
          { label: "Reference models", value: <ReferenceModelTags slugs={model.reference_models} /> },
        ]}
      />

      <DetailSection title="Governance">
        <p className="muted">
          Models are assigned to capability classes via the Open Grace capability framework.
          Safety tier and plane restrictions gate agent bindings at publication.
        </p>
      </DetailSection>
    </>
  );
}
