import type { StandardRecord } from "@/lib/types";
import { ReferenceModelTags } from "./ReferenceModelTags";

export function StandardsList({ standards }: { standards: StandardRecord[] }) {
  if (!standards.length) {
    return <p className="muted">No standards bound.</p>;
  }

  return (
    <ul className="standards-list">
      {standards.map((standard) => (
        <li key={standard.standard_id}>
          <div className="standard-row">
            <div>
              <strong>{standard.display_name}</strong>
              <p className="muted">{standard.standard_id}</p>
            </div>
            <span className="tag">{standard.conformance_level}</span>
          </div>
          <p>
            <a href={standard.binding_uri} target="_blank" rel="noreferrer">
              {standard.binding_uri}
            </a>
          </p>
          <ReferenceModelTags slugs={standard.reference_models} />
        </li>
      ))}
    </ul>
  );
}
