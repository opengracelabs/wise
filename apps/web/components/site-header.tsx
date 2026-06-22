import Link from "next/link";
import { BarChart3, Compass } from "lucide-react";

import { Button } from "@/components/ui/button";

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-30 border-b border-[var(--border)] bg-[#f8faf7]/88 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4">
        <Link className="flex items-center gap-3 font-bold" href="/">
          <span className="flex h-10 w-10 items-center justify-center rounded-2xl bg-[var(--primary)] text-white">
            <Compass className="h-5 w-5" aria-hidden="true" />
          </span>
          <span>WISE Live Demo</span>
        </Link>
        <nav className="hidden items-center gap-2 md:flex" aria-label="Primary">
          <Button asChild variant="ghost" size="sm">
            <Link href="/collections/big-cats-of-the-world">RC4 Collection</Link>
          </Button>
          <Button asChild variant="ghost" size="sm">
            <Link href="/series/endangered-earth">RC5 Series</Link>
          </Button>
          <Button asChild variant="outline" size="sm">
            <Link href="/admin/insights">
              <BarChart3 className="h-4 w-4" aria-hidden="true" />
              Insights
            </Link>
          </Button>
        </nav>
      </div>
    </header>
  );
}
