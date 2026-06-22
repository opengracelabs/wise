"use client";

import { useEffect, useMemo, useState } from "react";
import { BarChart3, MousePointerClick, RefreshCcw, Timer } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  backendItemToAssetInsight,
  fetchBackendInsights,
  type BackendInsightsResponse,
} from "@/lib/analytics-insights";
import { getDemandInsights, readDemandEvents, type AssetInsight, type DemandEvent } from "@/lib/demand-events";

function useInsights() {
  const [insights, setInsights] = useState<AssetInsight[]>([]);
  const [events, setEvents] = useState<DemandEvent[]>([]);
  const [backendInsights, setBackendInsights] = useState<BackendInsightsResponse | null>(null);

  useEffect(() => {
    const refresh = async () => {
      const backend = await fetchBackendInsights();
      setBackendInsights(backend);
      setInsights(getDemandInsights());
      setEvents(readDemandEvents());
    };

    void refresh();
    window.addEventListener("wise-demand-events-updated", refresh);
    return () => window.removeEventListener("wise-demand-events-updated", refresh);
  }, []);

  return { insights, events, backendInsights };
}

export function InsightsDashboard() {
  const { insights, events, backendInsights } = useInsights();
  const collections = useMemo(
    () =>
      backendInsights
        ? backendInsights.top_viewed_collections.map(backendItemToAssetInsight)
        : insights.filter((insight) => insight.assetType === "collection"),
    [backendInsights, insights],
  );
  const series = useMemo(
    () =>
      backendInsights
        ? backendInsights.top_series_engagement.map(backendItemToAssetInsight)
        : insights.filter((insight) => insight.assetType === "series"),
    [backendInsights, insights],
  );
  const topClicked = useMemo(
    () =>
      backendInsights
        ? backendInsights.top_clicked_species.map(backendItemToAssetInsight)
        : insights.filter((insight) => insight.clicks > 0).slice(0, 8),
    [backendInsights, insights],
  );
  const totalClicks = insights.reduce((sum, insight) => sum + insight.clicks + insight.ctaClicks, 0);
  const totalDwell = insights.reduce((sum, insight) => sum + insight.dwellTimeSeconds, 0);
  const conversion = backendInsights?.cta_response_conversion_rate;

  return (
    <div className="space-y-8">
      <Card>
        <CardContent className="p-5 text-sm text-[var(--muted-foreground)]">
          Insight source:{" "}
          <span className="font-bold text-[var(--foreground)]">
            {backendInsights ? "analytics-service user_events" : "local fallback"}
          </span>
        </CardContent>
      </Card>
      <div className="grid gap-4 md:grid-cols-3">
        <MetricCard icon={<MousePointerClick />} label="Tracked clicks" value={totalClicks.toString()} />
        <MetricCard icon={<Timer />} label="Dwell seconds" value={Math.round(totalDwell).toString()} />
        <MetricCard icon={<BarChart3 />} label="Events stored" value={events.length.toString()} />
      </div>

      <InsightTable title="Top clicked assets" insights={topClicked} empty="No click events yet." />
      <InsightTable title="Collection interest ranking" insights={collections} empty="No collection interest yet." />
      <InsightTable title="Series interest ranking" insights={series} empty="No series interest yet." />
      <Card>
        <CardHeader>
          <CardTitle>CTA response conversion rate</CardTitle>
        </CardHeader>
        <CardContent className="grid gap-4 md:grid-cols-4">
          <MetricCard icon={<BarChart3 />} label="Yes" value={(conversion?.yes ?? 0).toString()} />
          <MetricCard icon={<BarChart3 />} label="Maybe" value={(conversion?.maybe ?? 0).toString()} />
          <MetricCard icon={<BarChart3 />} label="No" value={(conversion?.no ?? 0).toString()} />
          <MetricCard icon={<BarChart3 />} label="Total" value={(conversion?.total ?? 0).toString()} />
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex-row items-center justify-between gap-4">
          <CardTitle>Local demo controls</CardTitle>
          <Button
            variant="outline"
            onClick={() => {
              window.localStorage.removeItem("wise:demand-events");
              window.localStorage.removeItem("wise:interest-votes");
              window.dispatchEvent(new Event("wise-demand-events-updated"));
            }}
          >
            <RefreshCcw className="h-4 w-4" aria-hidden="true" />
            Reset local data
          </Button>
        </CardHeader>
      </Card>
    </div>
  );
}

function MetricCard({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) {
  return (
    <Card>
      <CardContent className="flex items-center gap-4 p-6">
        <span className="flex h-12 w-12 items-center justify-center rounded-2xl bg-[var(--muted)] text-[var(--primary)]">
          {icon}
        </span>
        <div>
          <p className="text-sm text-[var(--muted-foreground)]">{label}</p>
          <p className="text-3xl font-black">{value}</p>
        </div>
      </CardContent>
    </Card>
  );
}

function InsightTable({ title, insights, empty }: { title: string; insights: AssetInsight[]; empty: string }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        {insights.length === 0 ? (
          <p className="text-sm text-[var(--muted-foreground)]">{empty}</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full min-w-[680px] text-left text-sm">
              <thead className="text-xs uppercase tracking-wide text-[var(--muted-foreground)]">
                <tr>
                  <th className="py-3">Asset</th>
                  <th>Type</th>
                  <th>Clicks</th>
                  <th>Dwell</th>
                  <th>CTA rate</th>
                  <th>Yes / Maybe / No</th>
                  <th>Score</th>
                </tr>
              </thead>
              <tbody>
                {insights.map((insight) => (
                  <tr key={`${insight.assetType}:${insight.assetId}`} className="border-t border-[var(--border)]">
                    <td className="py-4 font-semibold">{insight.label}</td>
                    <td>{insight.assetType}</td>
                    <td>{insight.clicks}</td>
                    <td>{Math.round(insight.dwellTimeSeconds)}s</td>
                    <td>{insight.ctaRate.toFixed(2)}</td>
                    <td>
                      {insight.yesVotes} / {insight.maybeVotes} / {insight.noVotes}
                    </td>
                    <td className="font-bold">{insight.engagementScore}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
