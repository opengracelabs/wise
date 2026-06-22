"use client";

import type { AssetInsight } from "./demand-events";

export interface BackendInsightItem {
  entity_id: string;
  entity_type: AssetInsight["assetType"];
  views: number;
  clicks: number;
  cta_clicks: number;
  dwell_time: number;
  engagement_score: number;
}

export interface BackendInsightsResponse {
  top_viewed_collections: BackendInsightItem[];
  top_clicked_species: BackendInsightItem[];
  top_series_engagement: BackendInsightItem[];
  cta_response_conversion_rate: {
    yes: number;
    maybe: number;
    no: number;
    total: number;
  };
  source: "user_events" | "synthetic_fallback";
}

const ANALYTICS_API_URL = process.env.NEXT_PUBLIC_ANALYTICS_API_URL;

export async function fetchBackendInsights(): Promise<BackendInsightsResponse | null> {
  if (!ANALYTICS_API_URL) {
    return null;
  }

  try {
    const response = await fetch(`${ANALYTICS_API_URL}/admin/insights`, {
      headers: { accept: "application/json" },
      cache: "no-store",
    });
    if (!response.ok) {
      return null;
    }
    return (await response.json()) as BackendInsightsResponse;
  } catch {
    return null;
  }
}

export function backendItemToAssetInsight(item: BackendInsightItem): AssetInsight {
  return {
    assetId: item.entity_id,
    assetType: item.entity_type,
    label: item.entity_id,
    clicks: item.clicks,
    pageViews: item.views,
    dwellTimeSeconds: item.dwell_time,
    ctaClicks: item.cta_clicks,
    ctaRate: item.views > 0 ? item.cta_clicks / item.views : 0,
    yesVotes: 0,
    maybeVotes: 0,
    noVotes: 0,
    engagementScore: item.engagement_score,
  };
}
