# demonstration-surface

Founder Demonstration Surface — steward-gated read-only preview for Phases 1–3.

This is **not** Public Experience (Phase 11). See `06-build-roadmap.md` §3.1.

Frontend scaffold will be added in Reference Capability 1 implementation.
Backend routes are served by `services/api-service`.

## RC6 Commercial Validation Surface

Read-only commercial demand validation for the existing RC4 collection,
**Big Cats of the World**.

Routes:

- `/shop` — static product-card surface for Poster, Framed Print, Puzzle, Calendar, and Coffee Table Book concepts.
- `/shop/products/{slug}` — static product detail pages with price placeholders and local demand buttons.
- `/admin/commercial` — local browser analytics dashboard for product views, wishlist interest, buy interest, and checkout intent.

Safeguards:

- No payment processing, order creation, fulfillment, or server-side writes.
- Demand events are stored in local browser storage only.
- Vercel rewrites are provided at repository root for static serving of RC6 routes.
