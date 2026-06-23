import Link from "next/link";
import type { ReactNode } from "react";

interface DetailSectionProps {
  title: string;
  children: ReactNode;
}

export function DetailSection({ title, children }: DetailSectionProps) {
  return (
    <section className="detail-section">
      <h2>{title}</h2>
      {children}
    </section>
  );
}

export function MetaGrid({ items }: { items: { label: string; value: ReactNode }[] }) {
  return (
    <dl className="meta-grid">
      {items.map((item) => (
        <div key={item.label} className="meta-item">
          <dt>{item.label}</dt>
          <dd>{item.value}</dd>
        </div>
      ))}
    </dl>
  );
}

export function BackLink({ href, label }: { href: string; label: string }) {
  return (
    <p className="back-link">
      <Link href={href}>← {label}</Link>
    </p>
  );
}
