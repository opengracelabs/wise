"use client";

import Link from "next/link";
import type { ComponentProps } from "react";

import { recordDemandEvent, type DemandEventType } from "@/lib/demand-events";

interface TrackedLinkProps extends ComponentProps<typeof Link> {
  eventType: Extract<DemandEventType, "collection_click" | "species_click" | "series_click" | "cta_click">;
  assetId: string;
  assetType: "collection" | "series" | "species" | "place" | "cta";
  label: string;
}

export function TrackedLink({
  eventType,
  assetId,
  assetType,
  label,
  onClick,
  ...props
}: TrackedLinkProps) {
  return (
    <Link
      {...props}
      onClick={(event) => {
        recordDemandEvent({ type: eventType, assetId, assetType, label });
        onClick?.(event);
      }}
    />
  );
}
