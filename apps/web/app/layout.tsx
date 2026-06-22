import type { Metadata } from "next";

import "./globals.css";
import { SiteHeader } from "@/components/site-header";

export const metadata: Metadata = {
  title: "WISE Live Demonstration Surface",
  description: "Read-only RC4 and RC5 demand validation surface.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <SiteHeader />
        <main className="mx-auto max-w-7xl px-5 py-8 md:py-12">{children}</main>
      </body>
    </html>
  );
}
