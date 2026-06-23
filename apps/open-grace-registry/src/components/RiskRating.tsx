import type { RiskRecord } from "@/lib/types";

const SEVERITY_COLORS: Record<string, string> = {
  low: "#6b7280",
  medium: "#d97706",
  high: "#ea580c",
  critical: "#dc2626",
};

export function RiskRating({ risk }: { risk: RiskRecord }) {
  return (
    <div className="risk-card">
      <div className="risk-header">
        <strong>{risk.display_name}</strong>
        <span
          className="severity"
          style={{ backgroundColor: SEVERITY_COLORS[risk.severity] ?? "#6b7280" }}
        >
          {risk.severity}
        </span>
      </div>
      <p className="muted">
        {risk.framework} {risk.control_id}
      </p>
      <p>{risk.mitigation}</p>
    </div>
  );
}
