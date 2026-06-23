import Link from "next/link";

const NAV = [
  { href: "/agents", label: "Agents" },
  { href: "/capabilities", label: "Capabilities" },
  { href: "/benchmarks", label: "Benchmarks" },
  { href: "/audits", label: "Audits" },
  { href: "/models", label: "Models" },
];

export function SiteHeader() {
  return (
    <header className="site-header">
      <div className="header-inner">
        <Link href="/" className="brand">
          Open Grace Registry
        </Link>
        <nav>
          {NAV.map((item) => (
            <Link key={item.href} href={item.href}>
              {item.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
