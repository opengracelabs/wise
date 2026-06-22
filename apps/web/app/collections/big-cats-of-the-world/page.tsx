import { ArrowRight, CheckCircle2 } from "lucide-react";

import { DemandTracker } from "@/components/demand-tracker";
import { InterestPanel } from "@/components/interest-panel";
import { PageHero } from "@/components/page-hero";
import { SpeciesCard } from "@/components/species-card";
import { GateBadge } from "@/components/status-badge";
import { TrackedLink } from "@/components/tracked-link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { getCollection, getCollectionMembers, getRelatedPlaces } from "@/lib/api";

export default async function BigCatsCollectionPage() {
  const collection = await getCollection("big-cats-of-the-world");
  const members = await getCollectionMembers(collection);
  const relatedPlaces = await getRelatedPlaces();

  return (
    <div className="space-y-10">
      <DemandTracker assetId={collection.slug} assetType="collection" label={collection.title} />
      <PageHero
        badges={collection.sourceRefs}
        description={collection.description}
        eyebrow="RC4 Collection · Published Collection Manifest"
        imageUrl={collection.heroImageUrl}
        title={collection.title}
      />

      <section className="grid gap-4 md:grid-cols-3 lg:grid-cols-6">
        <GateBadge>Rights verified</GateBadge>
        <GateBadge>Quality approved</GateBadge>
        <GateBadge>Accessibility compliant</GateBadge>
        <GateBadge>Standards validated</GateBadge>
        <GateBadge>Benchmark validated</GateBadge>
        <GateBadge>Audit complete</GateBadge>
      </section>

      <section className="grid gap-8 lg:grid-cols-[1fr_320px]">
        <div className="space-y-5">
          <div>
            <p className="text-sm font-bold uppercase tracking-[0.24em] text-[var(--muted-foreground)]">
              Collection members
            </p>
            <h2 className="mt-2 text-3xl font-black">Big cats with conservation signals</h2>
          </div>
          <div className="grid gap-5 md:grid-cols-2">
            {members.map(({ species }) => (
              <SpeciesCard key={species.id} species={species} />
            ))}
          </div>
        </div>

        <aside className="space-y-5">
          <Card>
            <CardHeader>
              <CardTitle>RC4 validation goals</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 text-sm text-[var(--muted-foreground)]">
              {[
                "Can users understand a graph-backed collection?",
                "Do species cards drive detail-page clicks?",
                "Does conservation status affect interest?",
              ].map((item) => (
                <p key={item} className="flex gap-2">
                  <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-[var(--primary)]" />
                  {item}
                </p>
              ))}
            </CardContent>
          </Card>
          <InterestPanel assetId={collection.slug} assetType="collection" />
        </aside>
      </section>

      <section className="space-y-5">
        <h2 className="text-3xl font-black">Related protected areas</h2>
        <div className="grid gap-5 md:grid-cols-3">
          {relatedPlaces.slice(0, 3).map((place) => (
            <Card key={place.id} className="overflow-hidden">
              <img alt="" className="h-44 w-full object-cover" src={place.imageUrl} />
              <CardContent className="space-y-3 p-5">
                <h3 className="text-lg font-bold">{place.title}</h3>
                <p className="text-sm text-[var(--muted-foreground)]">{place.summary}</p>
                <Button asChild variant="outline" size="sm">
                  <TrackedLink
                    assetId={place.id}
                    assetType="place"
                    eventType="cta_click"
                    href={`/places/${place.id}`}
                    label={place.title}
                  >
                    Open place page
                    <ArrowRight className="h-4 w-4" aria-hidden="true" />
                  </TrackedLink>
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>
    </div>
  );
}
