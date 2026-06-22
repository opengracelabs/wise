# WISE Web Demonstration Surface

Read-only live demonstration surface for Reference Capability 4 and Reference
Capability 5.

## Scope

- RC4: `Big Cats of the World`
- RC5: `Endangered Earth Series`
- Local-only demand tracking
- No backend writes
- No governance or Architecture v1.0 changes

## Routes

- `/`
- `/collections/big-cats-of-the-world`
- `/series/endangered-earth`
- `/species/[id]`
- `/places/[id]`
- `/admin/insights`

## Platform API integration

Set `NEXT_PUBLIC_PLATFORM_API_URL` to read from Platform REST APIs. When unset,
the app falls back to bundled RC4/RC5 demonstration data.

## Demand tracking

Events are stored in browser `localStorage` by `lib/demand-events.ts`.

Tracked events:

- `page_view`
- `collection_click`
- `species_click`
- `series_click`
- `cta_click`

Engagement score:

```text
clicks + dwell_time + CTA_rate
```

## Vercel

The app is deployable as a standalone Next.js project from `apps/web`.
