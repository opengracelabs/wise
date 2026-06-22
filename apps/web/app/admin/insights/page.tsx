import { DemandTracker } from "@/components/demand-tracker";
import { InsightsDashboard } from "@/components/insights-dashboard";

export default function InsightsPage() {
  return (
    <div className="space-y-8">
      <DemandTracker assetId="admin-insights" assetType="home" label="Admin insights dashboard" />
      <section>
        <p className="text-sm font-bold uppercase tracking-[0.24em] text-[var(--muted-foreground)]">
          Local demand signals
        </p>
        <h1 className="mt-3 text-4xl font-black tracking-tight md:text-6xl">RC4 + RC5 insights</h1>
        <p className="prose-readable mt-4 text-[var(--muted-foreground)]">
          This dashboard reads browser-local demand events only. It shows whether the live demo is
          attracting interaction without adding a backend, governance layer, or canonical write path.
        </p>
      </section>
      <InsightsDashboard />
    </div>
  );
}
