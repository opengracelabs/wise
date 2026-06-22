import { ArrowRight, Circle, CircleCheck, CircleDashed } from "lucide-react";

import { DemandTracker } from "@/components/demand-tracker";
import { InterestPanel } from "@/components/interest-panel";
import { PageHero } from "@/components/page-hero";
import { GateBadge } from "@/components/status-badge";
import { TrackedLink } from "@/components/tracked-link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { getCollection, getSeries } from "@/lib/api";
import type { SeriesSection } from "@/lib/types";

const statusIcon = {
  published: CircleCheck,
  editorial_review: CircleDashed,
  draft: Circle,
};

export default async function EndangeredEarthSeriesPage() {
  const [series, collection] = await Promise.all([
    getSeries("endangered-earth"),
    getCollection("big-cats-of-the-world"),
  ]);

  return (
    <div className="space-y-10">
      <DemandTracker assetId={series.slug} assetType="series" label={series.title} />
      <PageHero
        badges={["RC5 Series", "Ordered publishing workflow", "Benchmark validation"]}
        description={series.description}
        eyebrow="RC5 Series · Published Series Manifest"
        imageUrl={series.heroImageUrl}
        title={series.title}
      />

      <section className="grid gap-4 md:grid-cols-3">
        <GateBadge>Quality approved</GateBadge>
        <GateBadge>Benchmark validated</GateBadge>
        <GateBadge>Audit packet complete</GateBadge>
      </section>

      <section className="grid gap-8 lg:grid-cols-[1fr_360px]">
        <div className="space-y-5">
          <h2 className="text-3xl font-black">Series progression</h2>
          <div className="space-y-4">
            {series.sections
              .slice()
              .sort((a, b) => a.order - b.order)
              .map((section) => (
                <SeriesStep key={section.id} section={section} />
              ))}
          </div>
        </div>

        <aside className="space-y-5">
          <Card className="overflow-hidden">
            <img alt="" className="h-48 w-full object-cover" src={collection.heroImageUrl} />
            <CardHeader>
              <CardTitle>Featured collection</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h3 className="text-2xl font-black">{collection.title}</h3>
                <p className="mt-2 text-sm text-[var(--muted-foreground)]">{collection.subtitle}</p>
              </div>
              <Button asChild>
                <TrackedLink
                  assetId={collection.slug}
                  assetType="collection"
                  eventType="collection_click"
                  href="/collections/big-cats-of-the-world"
                  label={collection.title}
                >
                  Open featured collection
                  <ArrowRight className="h-4 w-4" aria-hidden="true" />
                </TrackedLink>
              </Button>
            </CardContent>
          </Card>
          <InterestPanel assetId={series.slug} assetType="series" />
        </aside>
      </section>
    </div>
  );
}

function SeriesStep({ section }: { section: SeriesSection }) {
  const Icon = statusIcon[section.status];

  return (
    <Card>
      <CardContent className="flex gap-5 p-5">
        <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl bg-[var(--muted)] text-[var(--primary)]">
          <Icon className="h-5 w-5" aria-hidden="true" />
        </span>
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-3">
            <p className="text-sm font-bold uppercase tracking-[0.2em] text-[var(--muted-foreground)]">
              Section {section.order}
            </p>
            <GateBadge>{section.status.replace("_", " ")}</GateBadge>
          </div>
          <h3 className="mt-2 text-2xl font-black">{section.title}</h3>
          <p className="mt-2 text-[var(--muted-foreground)]">{section.summary}</p>
          <TrackedLink
            assetId={section.id}
            assetType={section.id === "big-cats-of-the-world" ? "collection" : "series"}
            className="mt-4 inline-flex items-center gap-2 text-sm font-bold text-[var(--primary)]"
            eventType={section.id === "big-cats-of-the-world" ? "collection_click" : "series_click"}
            href={section.href}
            label={section.title}
          >
            Follow this section
            <ArrowRight className="h-4 w-4" aria-hidden="true" />
          </TrackedLink>
        </div>
      </CardContent>
    </Card>
  );
}
