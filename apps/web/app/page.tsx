import { ArrowRight, Layers3, Sparkles } from "lucide-react";

import { DemandTracker } from "@/components/demand-tracker";
import { InterestPanel } from "@/components/interest-panel";
import { PageHero } from "@/components/page-hero";
import { SpeciesCard } from "@/components/species-card";
import { GateBadge } from "@/components/status-badge";
import { TrackedLink } from "@/components/tracked-link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { getAllSpecies, getCollection, getSeries } from "@/lib/api";

export default async function HomePage() {
  const [collection, series, species] = await Promise.all([
    getCollection("big-cats-of-the-world"),
    getSeries("endangered-earth"),
    getAllSpecies(),
  ]);
  const featuredSpecies = species.slice(0, 3);

  return (
    <div className="space-y-10">
      <DemandTracker assetId="home" assetType="home" label="Home discovery page" />
      <PageHero
        badges={["Read-only demo", "RC4 Collection", "RC5 Series", "Local demand tracking"]}
        description="A Vercel-ready live demonstration surface for determining whether collection and series concepts attract real user interest before platform-scale publishing work expands."
        eyebrow="Architecture v1.0 frozen · ADR-011 compliant"
        imageUrl={series.heroImageUrl}
        title="Discover stories that connect species, places, and conservation."
      />

      <section className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <Card className="overflow-hidden">
          <div className="grid gap-0 md:grid-cols-[0.9fr_1.1fr]">
            <img
              alt="Big cats collection preview"
              className="h-full min-h-72 w-full object-cover"
              src={collection.heroImageUrl}
            />
            <div className="p-6 md:p-8">
              <div className="mb-4 flex flex-wrap gap-2">
                <GateBadge>Quality approved</GateBadge>
                <GateBadge>Benchmark validated</GateBadge>
                <GateBadge>Audit packet complete</GateBadge>
              </div>
              <h2 className="text-3xl font-black">{collection.title}</h2>
              <p className="mt-4 text-[var(--muted-foreground)]">{collection.description}</p>
              <Button asChild className="mt-6">
                <TrackedLink
                  assetId={collection.slug}
                  assetType="collection"
                  eventType="collection_click"
                  href="/collections/big-cats-of-the-world"
                  label={collection.title}
                >
                  Open RC4 collection
                  <ArrowRight className="h-4 w-4" aria-hidden="true" />
                </TrackedLink>
              </Button>
            </div>
          </div>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-[var(--muted)] text-[var(--primary)]">
              <Layers3 className="h-6 w-6" aria-hidden="true" />
            </div>
            <CardTitle>{series.title}</CardTitle>
            <CardDescription>{series.description}</CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild variant="outline">
              <TrackedLink
                assetId={series.slug}
                assetType="series"
                eventType="series_click"
                href="/series/endangered-earth"
                label={series.title}
              >
                Open RC5 series
              </TrackedLink>
            </Button>
          </CardContent>
        </Card>
      </section>

      <section className="space-y-5">
        <div className="flex items-center gap-3">
          <Sparkles className="h-5 w-5 text-[var(--accent)]" aria-hidden="true" />
          <h2 className="text-2xl font-black">Featured species signals</h2>
        </div>
        <div className="grid gap-5 md:grid-cols-3">
          {featuredSpecies.map((item) => (
            <SpeciesCard key={item.id} species={item} />
          ))}
        </div>
      </section>

      <InterestPanel assetId="home" assetType="home" title="Would this discovery experience make you explore more?" />
    </div>
  );
}
