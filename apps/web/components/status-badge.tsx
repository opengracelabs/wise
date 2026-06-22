import { Badge } from "@/components/ui/badge";
import type { ConservationStatus } from "@/lib/types";

const statusTone: Record<ConservationStatus, string> = {
  "Least Concern": "border-emerald-200 bg-emerald-50 text-emerald-800",
  "Near Threatened": "border-lime-200 bg-lime-50 text-lime-800",
  Vulnerable: "border-amber-200 bg-amber-50 text-amber-800",
  Endangered: "border-orange-200 bg-orange-50 text-orange-800",
  "Critically Endangered": "border-red-200 bg-red-50 text-red-800",
};

export function ConservationStatusBadge({ status }: { status: ConservationStatus }) {
  return <Badge className={statusTone[status]}>{status}</Badge>;
}

export function GateBadge({ children }: { children: string }) {
  return <Badge className="border-[var(--primary)]/20 bg-[#edf7ef] text-[var(--primary)]">{children}</Badge>;
}
