"use client";

import { useMemo, useState } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { readInterestVotes, saveInterestVote, type DemandEvent } from "@/lib/demand-events";
import type { InterestResponse } from "@/lib/types";

interface InterestPanelProps {
  assetId: string;
  assetType: DemandEvent["assetType"];
  title?: string;
}

const responses: { value: InterestResponse; label: string }[] = [
  { value: "yes", label: "Yes" },
  { value: "maybe", label: "Maybe" },
  { value: "no", label: "No" },
];

export function InterestPanel({ assetId, assetType, title = "Would you use or buy this?" }: InterestPanelProps) {
  const initialResponse = useMemo(
    () =>
      typeof window === "undefined"
        ? undefined
        : readInterestVotes().find((vote) => vote.assetId === assetId && vote.assetType === assetType)
            ?.response,
    [assetId, assetType],
  );
  const [selected, setSelected] = useState<InterestResponse | undefined>(initialResponse);

  return (
    <Card className="border-[var(--primary)]/20 bg-[#f2f7ef]">
      <CardHeader>
        <CardTitle className="text-lg">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex flex-wrap gap-3">
          {responses.map((response) => (
            <Button
              key={response.value}
              variant={selected === response.value ? "default" : "outline"}
              onClick={() => {
                setSelected(response.value);
                saveInterestVote({ assetId, assetType, response: response.value });
              }}
            >
              {response.label}
            </Button>
          ))}
        </div>
        <p className="mt-4 text-sm text-[var(--muted-foreground)]">
          Stored locally for this live demo only. No backend write path is used.
        </p>
      </CardContent>
    </Card>
  );
}
