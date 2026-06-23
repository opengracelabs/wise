import Link from "next/link";
import { loadRegistryData } from "@/lib/data";

export default function HomePage() {
  const data = loadRegistryData();

  const sections = [
    { href: "/agents", title: "Agents", count: data.agents.length },
    { href: "/capabilities", title: "Capabilities", count: data.capabilities.length },
    { href: "/benchmarks", title: "Benchmarks", count: data.benchmarks.length },
    { href: "/audits", title: "Audits", count: data.audits.length },
    { href: "/models", title: "Models", count: data.models.length },
  ];

  return (
    <>
      <div className="page-header">
        <h1>Open Grace Registry Portal</h1>
        <p>
          Read-only browser for governed agents, capability classes, benchmark gates,
          audit evidence, and model council assignments. Reference models include Wikidata,
          GBIF, and UNESCO World Heritage List.
        </p>
      </div>
      <div className="home-grid">
        {sections.map((section) => (
          <Link key={section.href} href={section.href} className="home-card">
            <h2>{section.title}</h2>
            <p>{section.count} records</p>
          </Link>
        ))}
      </div>
    </>
  );
}
