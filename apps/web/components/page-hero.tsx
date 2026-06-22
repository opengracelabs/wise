import { Badge } from "@/components/ui/badge";

interface PageHeroProps {
  eyebrow: string;
  title: string;
  description: string;
  imageUrl: string;
  badges?: string[];
}

export function PageHero({ eyebrow, title, description, imageUrl, badges = [] }: PageHeroProps) {
  return (
    <section className="relative overflow-hidden rounded-[2rem] border border-[var(--border)] bg-[#102819] text-white shadow-sm">
      <img
        alt=""
        className="absolute inset-0 h-full w-full object-cover opacity-35"
        src={imageUrl}
      />
      <div className="absolute inset-0 bg-gradient-to-r from-[#102819] via-[#102819]/84 to-transparent" />
      <div className="relative px-6 py-16 md:px-12 md:py-24">
        <p className="mb-4 text-sm font-bold uppercase tracking-[0.28em] text-[#f5d48a]">{eyebrow}</p>
        <h1 className="max-w-4xl text-4xl font-black tracking-tight md:text-6xl">{title}</h1>
        <p className="prose-readable mt-6 text-lg text-white/86">{description}</p>
        {badges.length > 0 ? (
          <div className="mt-8 flex flex-wrap gap-2">
            {badges.map((badge) => (
              <Badge key={badge} className="border-white/20 bg-white/15 text-white">
                {badge}
              </Badge>
            ))}
          </div>
        ) : null}
      </div>
    </section>
  );
}
