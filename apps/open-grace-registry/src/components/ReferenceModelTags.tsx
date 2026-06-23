import { getReferenceModel } from "@/lib/data";

export function ReferenceModelTags({ slugs }: { slugs: string[] }) {
  if (!slugs.length) return <span className="muted">—</span>;
  return (
    <div className="tag-list">
      {slugs.map((slug) => {
        const profile = getReferenceModel(slug);
        return (
          <span key={slug} className="tag" title={profile?.governance_use}>
            {profile?.display_name ?? slug}
          </span>
        );
      })}
    </div>
  );
}
