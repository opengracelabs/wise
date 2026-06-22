"use client";

import { useEffect } from "react";

import { endPageView, startPageView, type DemandEvent } from "@/lib/demand-events";

interface DemandTrackerProps {
  assetId: string;
  assetType: DemandEvent["assetType"];
  label: string;
}

export function DemandTracker({ assetId, assetType, label }: DemandTrackerProps) {
  useEffect(() => {
    const startedAt = Date.now();
    const eventId = startPageView({ assetId, assetType, label });

    const finish = () => {
      endPageView(eventId, (Date.now() - startedAt) / 1000);
    };

    window.addEventListener("pagehide", finish);
    return () => {
      finish();
      window.removeEventListener("pagehide", finish);
    };
  }, [assetId, assetType, label]);

  return null;
}
