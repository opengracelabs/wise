import { notFound } from "next/navigation";
import { Leaf } from "lucide-react";

import { DemandTracker } from "@/components/demand-tracker";
import { InterestPanel } from "@/components/interest-panel";
import { PageHero } from "@/components/page-hero";
import { ConservationStatusBadge, GateBadge } from "@/components/status-badge";
import { TrackedLink } from "@/components/tracked-link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { getPlace, getSpecies } from "@/lib/api";

export default async function PlacePage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const place = await getPlace(id);

  if (!place) {
    notFound();
  }

  const species = (await Promise.all(place.speciesIds.map((speciesId) => getSpecies(speciesId)))).filter(
    (item): item is NonNullable<typeof item> => Boolean(item),
  );

  return (
    <div className="space-y-10">
      <DemandTracker assetId={place.id} assetType="place" label={place.title} />
      <PageHero
        badges={["Protected Planet", "OpenStreetMap", "GeoJSON", `IUCN ${place.iucnCategory}`]}
        description={place.summary}
        eyebrow="Protected area page · RC3 context for RC4/RC5 demand"
        imageUrl={place.imageUrl}
        title={place.title}
      />

      <section className="grid gap-6 lg:grid-cols-[1fr_360px]">
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Boundary preview</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex min-h-80 items-center justify-center rounded-3xl border border-dashed border-[var(--border)] bg-[var(--muted)] p-8 text-center">
                <div>
                  <p className="text-sm font-bold uppercase tracking-[0.24em] text-[var(--muted-foreground)]">
                    MapLibre placeholder
                  </p>
                  <p className="mt-3 text-2xl font-black">Read-only boundary map surface</p>
                  <p className="prose-readable mx-auto mt-3 text-[var(--muted-foreground)]">
                    The live demo renders a safe placeholder until the Platform map API supplies approved
                    GeoJSON. No frontend writes or boundary edits are possible.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Species associated with this place</CardTitle>
            </CardHeader>
            <CardContent className="grid gap-4 md:grid-cols-2">
              {species.map((item) => (
                <TrackedLink
                  key={item.id}
                  assetId={item.id}
                  assetType="species"
                  className="rounded-2xl border border-[var(--border)] p-4 transition hover:bg-[var(--muted)]"
                  eventType="species_click"
                  href={`/species/${item.id}`}
                  label={item.commonName}
                >
                  <span className="flex items-center gap-2 font-bold">
                    <Leaf className="h-4 w-4" aria-hidden="true" />
                    {item.commonName}
                  </span>
                  <span className="mt-2 flex">
                    <ConservationStatusBadge status={item.conservationStatus} />
                  </span>
                </TrackedLink>
              ))}
            </CardContent>
          </Card>
        </div>

        <aside className="space-y-5">
          <Card>
            <CardHeader>
              <CardTitle>Protected-area metadata</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <Fact label="Designation" value={place.designationType} />
              <Fact label="Country" value={place.country} />
              <Fact label="IUCN category" value={place.iucnCategory} />
              <div className="flex flex-wrap gap-2 pt-2">
                <GateBadge>GeoJSON ready</GateBadge>
                <GateBadge>Quality approved</GateBadge>
                <GateBadge>Geospatial indexed</GateBadge>
              </div>
            </CardContent>
          </Card>
          <InterestPanel assetId={place.id} assetType="place" />
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
