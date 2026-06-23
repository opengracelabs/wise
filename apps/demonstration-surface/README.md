# demonstration-surface

Founder Demonstration Surface — steward-gated read-only preview for Phases 1–3.

This is **not** Public Experience (Phase 11). See `06-build-roadmap.md` §3.1.

Frontend scaffold will be added in Reference Capability 1 implementation.
Backend routes are served by `services/api-service`.

## RC6 Commercial Validation Surface / RC7 Product Intelligence / RC8 Brand Experience

Read-only commercial demand validation and product intelligence for Nature & Culture.

Routes:

- `/` — Nature & Culture homepage and brand experience.
- `/shop` — static product-card surface for featured nature, culture, map, education, and gift concepts.
- `/shop/maps` — Historic Maps validation route.
- `/shop/education` — Educational Card Sets, Discovery Packs, Paint-by-Numbers, and Classroom Kits validation route.
- `/shop/gifts` — gift-oriented validation route.
- `/shop/products/{slug}` — static product detail page with price placeholders, local demand buttons, and RC7 intelligence scores.
- `/admin/commercial` — local browser analytics dashboard for product views, wishlist interest, buy intent, category ranking, and product fit.

Safeguards:

- No payment processing, order creation, fulfillment, or server-side writes.
- Demand events are stored in local browser storage only.
- Vercel rewrites are provided at repository root for static serving of RC6-RC8 routes.
- Architecture v1.0 remains frozen; ADR-011 followed.
