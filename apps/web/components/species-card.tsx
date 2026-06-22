import { ArrowRight } from "lucide-react";

import { Card, CardContent } from "@/components/ui/card";
import { ConservationStatusBadge } from "@/components/status-badge";
import { TrackedLink } from "@/components/tracked-link";
import type { SpeciesSummary } from "@/lib/types";

export function SpeciesCard({ species }: { species: SpeciesSummary }) {
  return (
    <Card className="group overflow-hidden">
      <div className="aspect-[4/3] overflow-hidden bg-[var(--muted)]">
        <img
          alt={`${species.commonName} in habitat`}
          className="h-full w-full object-cover transition duration-500 group-hover:scale-105"
          src={species.imageUrl}
        />
      </div>
      <CardContent className="space-y-4 p-5">
        <div className="flex items-start justify-between gap-3">
          <div>
            <h3 className="text-xl font-bold">{species.commonName}</h3>
            <p className="text-sm italic text-[var(--muted-foreground)]">{species.scientificName}</p>
          </div>
          <ConservationStatusBadge status={species.conservationStatus} />
        </div>
        <p className="line-clamp-3 text-sm leading-6 text-[var(--muted-foreground)]">{species.summary}</p>
        <TrackedLink
          assetId={species.id}
          assetType="species"
          className="inline-flex items-center gap-2 text-sm font-bold text-[var(--primary)]"
          eventType="species_click"
          href={`/species/${species.id}`}
          label={species.commonName}
        >
          Open species page
          <ArrowRight className="h-4 w-4" aria-hidden="true" />
        </TrackedLink>
      </CardContent>
    </Card>
  );
}
