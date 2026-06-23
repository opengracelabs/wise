import type { LifecycleStage } from "@/lib/types";

const STAGE_COLORS: Record<LifecycleStage, string> = {
  proposal: "#6b7280",
  review: "#2563eb",
  benchmark: "#7c3aed",
  approval: "#d97706",
  publication: "#059669",
  audit: "#0891b2",
  retirement: "#9ca3af",
};

export function LifecycleBadge({ stage }: { stage: LifecycleStage }) {
  return (
    <span
      className="badge"
      style={{ backgroundColor: STAGE_COLORS[stage] ?? "#6b7280" }}
    >
      {stage}
    </span>
  );
}
