"use client";

import type { InterestResponse } from "./types";

export type DemandEventType =
  | "page_view"
  | "collection_click"
  | "species_click"
  | "series_click"
  | "cta_click";

export interface DemandEvent {
  id: string;
  type: DemandEventType;
  assetId: string;
  assetType: "home" | "collection" | "series" | "species" | "place" | "cta";
  label: string;
  path: string;
  timestamp: number;
  dwellTimeSeconds?: number;
}

export interface InterestVote {
  assetId: string;
  assetType: DemandEvent["assetType"];
  response: InterestResponse;
  timestamp: number;
}

export interface AssetInsight {
  assetId: string;
  assetType: DemandEvent["assetType"];
  label: string;
  clicks: number;
  pageViews: number;
  dwellTimeSeconds: number;
  ctaClicks: number;
  ctaRate: number;
  yesVotes: number;
  maybeVotes: number;
  noVotes: number;
  engagementScore: number;
}

const EVENTS_KEY = "wise:demand-events";
const VOTES_KEY = "wise:interest-votes";

function readJson<T>(key: string, fallback: T): T {
  if (typeof window === "undefined") {
    return fallback;
  }

  try {
    const raw = window.localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : fallback;
  } catch {
    return fallback;
  }
}

function writeJson<T>(key: string, value: T) {
  if (typeof window === "undefined") {
    return;
  }

  window.localStorage.setItem(key, JSON.stringify(value));
  window.dispatchEvent(new Event("wise-demand-events-updated"));
}

function createId() {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }

  return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

export function recordDemandEvent(input: Omit<DemandEvent, "id" | "timestamp" | "path"> & { path?: string }) {
  const events = readDemandEvents();
  const event: DemandEvent = {
    ...input,
    id: createId(),
    path: input.path ?? window.location.pathname,
    timestamp: Date.now(),
  };

  writeJson(EVENTS_KEY, [event, ...events].slice(0, 500));
  return event.id;
}

export function startPageView(input: Omit<DemandEvent, "id" | "timestamp" | "path" | "type">) {
  return recordDemandEvent({
    ...input,
    type: "page_view",
  });
}

export function endPageView(eventId: string, dwellTimeSeconds: number) {
  const events = readDemandEvents();
  const updated = events.map((event) =>
    event.id === eventId
      ? {
          ...event,
          dwellTimeSeconds: Math.max(event.dwellTimeSeconds ?? 0, Math.round(dwellTimeSeconds)),
        }
      : event,
  );

  writeJson(EVENTS_KEY, updated);
}

export function readDemandEvents(): DemandEvent[] {
  return readJson<DemandEvent[]>(EVENTS_KEY, []);
}

export function saveInterestVote(vote: Omit<InterestVote, "timestamp">) {
  const votes = readInterestVotes().filter(
    (item) => !(item.assetId === vote.assetId && item.assetType === vote.assetType),
  );

  writeJson(VOTES_KEY, [{ ...vote, timestamp: Date.now() }, ...votes]);
  recordDemandEvent({
    type: "cta_click",
    assetId: vote.assetId,
    assetType: vote.assetType,
    label: `Interest response: ${vote.response}`,
  });
}

export function readInterestVotes(): InterestVote[] {
  return readJson<InterestVote[]>(VOTES_KEY, []);
}

export function getDemandInsights(): AssetInsight[] {
  const events = readDemandEvents();
  const votes = readInterestVotes();
  const insights = new Map<string, AssetInsight>();

  for (const event of events) {
    const key = `${event.assetType}:${event.assetId}`;
    const existing = insights.get(key) ?? {
      assetId: event.assetId,
      assetType: event.assetType,
      label: event.label,
      clicks: 0,
      pageViews: 0,
      dwellTimeSeconds: 0,
      ctaClicks: 0,
      ctaRate: 0,
      yesVotes: 0,
      maybeVotes: 0,
      noVotes: 0,
      engagementScore: 0,
    };

    existing.label = existing.label || event.label;
    existing.pageViews += event.type === "page_view" ? 1 : 0;
    existing.clicks += event.type.endsWith("_click") && event.type !== "cta_click" ? 1 : 0;
    existing.ctaClicks += event.type === "cta_click" ? 1 : 0;
    existing.dwellTimeSeconds += event.dwellTimeSeconds ?? 0;
    insights.set(key, existing);
  }

  for (const vote of votes) {
    const key = `${vote.assetType}:${vote.assetId}`;
    const existing = insights.get(key) ?? {
      assetId: vote.assetId,
      assetType: vote.assetType,
      label: vote.assetId,
      clicks: 0,
      pageViews: 0,
      dwellTimeSeconds: 0,
      ctaClicks: 0,
      ctaRate: 0,
      yesVotes: 0,
      maybeVotes: 0,
      noVotes: 0,
      engagementScore: 0,
    };

    existing.yesVotes += vote.response === "yes" ? 1 : 0;
    existing.maybeVotes += vote.response === "maybe" ? 1 : 0;
    existing.noVotes += vote.response === "no" ? 1 : 0;
    insights.set(key, existing);
  }

  return Array.from(insights.values())
    .map((insight) => {
      const ctaRate = insight.pageViews > 0 ? insight.ctaClicks / insight.pageViews : 0;
      return {
        ...insight,
        ctaRate,
        engagementScore: Number(
          (insight.clicks + insight.dwellTimeSeconds + ctaRate).toFixed(2),
        ),
      };
    })
    .sort((a, b) => b.engagementScore - a.engagementScore);
}
