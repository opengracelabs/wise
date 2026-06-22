import { notFound } from "next/navigation";
import { MapPin } from "lucide-react";

import { DemandTracker } from "@/components/demand-tracker";
import { InterestPanel } from "@/components/interest-panel";
import { PageHero } from "@/components/page-hero";
import { ConservationStatusBadge, GateBadge } from "@/components/status-badge";
import { TrackedLink } from "@/components/tracked-link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { getRelatedPlaces, getSpecies } from "@/lib/api";

export default async function SpeciesPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const species = await getSpecies(id);

  if (!species) {
    notFound();
  }

  const relatedPlaces = await getRelatedPlaces(species.id);

  return (
    <div className="space-y-10">
      <DemandTracker assetId={species.id} assetType="species" label={species.commonName} />
      <PageHero
        badges={species.sourceBadges}
        description={species.summary}
        eyebrow="Species page · Read-only Platform API consumer"
        imageUrl={species.imageUrl}
        title={species.commonName}
      />

      <section className="grid gap-6 lg:grid-cols-[1fr_360px]">
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Taxonomy and conservation</CardTitle>
            </CardHeader>
            <CardContent className="grid gap-5 md:grid-cols-2">
              <Fact label="Scientific name" value={species.scientificName} />
              <Fact label="Range" value={species.range} />
              <Fact label="Population trend" value={species.populationTrend} />
              <div>
                <p className="text-sm font-semibold text-[var(--muted-foreground)]">Conservation status</p>
                <div className="mt-2">
                  <ConservationStatusBadge status={species.conservationStatus} />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Related protected areas</CardTitle>
            </CardHeader>
            <CardContent className="grid gap-4 md:grid-cols-2">
              {relatedPlaces.map((place) => (
                <TrackedLink
                  key={place.id}
                  assetId={place.id}
                  assetType="place"
                  className="rounded-2xl border border-[var(--border)] p-4 transition hover:bg-[var(--muted)]"
                  eventType="cta_click"
                  href={`/places/${place.id}`}
                  label={place.title}
                >
                  <span className="flex items-center gap-2 font-bold">
                    <MapPin className="h-4 w-4" aria-hidden="true" />
                    {place.title}
                  </span>
                  <span className="mt-2 block text-sm text-[var(--muted-foreground)]">{place.summary}</span>
                </TrackedLink>
              ))}
            </CardContent>
          </Card>
        </div>

        <aside className="space-y-5">
          <Card>
            <CardHeader>
              <CardTitle>Readiness gates</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-wrap gap-2">
              <GateBadge>Darwin Core</GateBadge>
              <GateBadge>GBIF linked</GateBadge>
              <GateBadge>Quality approved</GateBadge>
              <GateBadge>Rights verified</GateBadge>
            </CardContent>
          </Card>
          <InterestPanel assetId={species.id} assetType="species" />
        </aside>
      </section>
    </div>
  );
}

function Fact({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-sm font-semibold text-[var(--muted-foreground)]">{label}</p>
      <p className="mt-1 text-lg font-bold">{value}</p>
    </div>
  );
}
