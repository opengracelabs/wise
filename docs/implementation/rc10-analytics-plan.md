# RC10 Analytics Plan

**Status:** Prototype analytics plan  
**Authority:** architecture-v1.0 (`architecture-v1.0`, ADR-011)  
**Scope:** Audience validation instrumentation design only — no governance changes, no Architecture v1.0 changes, no agents, no ADRs

---

## 1. Objective

RC10 defines the audience validation analytics model for the Nature & Culture public beta. The plan measures whether visitors understand the mission, explore collections and series, show product interest, and move through the read-only commercial validation funnel.

This plan does **not** add payment processing, production data collection infrastructure, user accounts, or a new platform component. It defines the schema and instrumentation contract that can be implemented through an approved Experience Plane analytics endpoint or external analytics tool in a later implementation step.

---

## 2. Event taxonomy

| Event | Required trigger | Primary question answered |
|-------|------------------|---------------------------|
| `page_view` | Any route load | Which pages attract audience attention? |
| `collection_view` | Collection card/detail impression | Which collections earn deeper exploration? |
| `series_view` | Series card/detail impression | Which editorial narratives perform best? |
| `product_view` | Product detail load or product card click | Which products earn interest? |
| `wishlist` | Wishlist intent action | Which products are saved or emotionally valued? |
| `buy_intent` | Buy Interest action | Which products show commercial demand without checkout? |
| `outbound_click` | External/source link click | Which sources and references create follow-through? |
| `search` | Search submit | What are visitors trying to find? |
| `session_duration` | Session end or heartbeat aggregate | Are visitors engaged beyond initial landing? |

Event naming intentionally uses `wishlist` and `buy_intent` for RC10. Existing RC6/RC7 local prototype aliases (`add_to_wishlist`, `buy_interest`) should map to these names at aggregation time.

---

## 3. Analytics schema

### `analytics_sessions`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `session_id` | string | Yes | Anonymous UUID generated client-side. |
| `started_at` | ISO datetime | Yes | Session start timestamp. |
| `ended_at` | ISO datetime | No | Session end timestamp when available. |
| `duration_seconds` | integer | No | Derived session duration. |
| `landing_path` | string | Yes | First route in session. |
| `referrer_domain` | string | No | Domain-only referrer; no full URL storage by default. |
| `utm_source` | string | No | Campaign source when present. |
| `utm_medium` | string | No | Campaign medium when present. |
| `utm_campaign` | string | No | Campaign name when present. |
| `device_class` | enum | No | `desktop`, `tablet`, `mobile`, or `unknown`. |
| `consent_state` | enum | Yes | `not_required`, `granted`, `denied`, or `unknown`. |

### `analytics_events`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `event_id` | string | Yes | Anonymous UUID. |
| `session_id` | string | Yes | Links to `analytics_sessions.session_id`. |
| `event_name` | enum | Yes | One of the RC10 event names. |
| `occurred_at` | ISO datetime | Yes | Client timestamp. |
| `page_path` | string | Yes | Current route path. |
| `page_title` | string | No | Document title or page label. |
| `entity_type` | enum | No | `page`, `collection`, `series`, `product`, `asset`, `source`, or `search`. |
| `entity_id` | string | No | Stable local ID for collection/series/product/asset. |
| `entity_title` | string | No | Human-readable entity title. |
| `collection_id` | string | No | Collection ID when relevant. |
| `series_id` | string | No | Series ID when relevant. |
| `product_category` | string | No | Product category when relevant. |
| `experiment_id` | string | No | Landing experiment ID. |
| `variant_id` | string | No | Landing experiment variant ID. |
| `search_query` | string | No | Search query after privacy filtering. |
| `outbound_domain` | string | No | Domain-only outbound target. |
| `metadata` | object | No | Small structured event-specific details. |

### Event-specific metadata

| Event | Metadata keys |
|-------|---------------|
| `page_view` | `route_group`, `is_landing_page` |
| `collection_view` | `geography_region`, `domain`, `theme` |
| `series_view` | `education_level`, `narrative_theme` |
| `product_view` | `commercial_score`, `product_fit_score` |
| `wishlist` | `source_component`, `product_category` |
| `buy_intent` | `source_component`, `product_category`, `price_placeholder_visible` |
| `outbound_click` | `outbound_domain`, `source_family` |
| `search` | `result_count`, `query_length`, `zero_results` |
| `session_duration` | `duration_seconds`, `page_count`, `engaged_event_count` |

---

## 4. Event aliases from current prototype

| Current local event | RC10 normalized event |
|---------------------|-----------------------|
| `product_view` | `product_view` |
| `add_to_wishlist` | `wishlist` |
| `buy_interest` | `buy_intent` |
| `checkout_intent` | `buy_intent` metadata: `simulated_checkout_intent: true` |

---

## 5. Landing page experiments

Experiment ID: `rc10-landing-message`

| Variant | Headline | Measures |
|---------|----------|----------|
| A | Explore Humanity's Greatest Heritage | clicks, engagement, product interest |
| B | Discover Nature, Culture, and History | clicks, engagement, product interest |
| C | Permanent Digital Memory of Humanity | clicks, engagement, product interest |

Primary metrics:

- Click-through from homepage to collection/series/shop routes.
- Engagement depth: page views per session and session duration.
- Product interest: product views, wishlist events, buy intent events.

---

## 6. Privacy requirements

1. Use anonymous session IDs only.
2. Do not collect names, emails, payment data, account identifiers, or precise location.
3. Store referrer and outbound data as domains by default.
4. Filter or hash search query terms if they contain personal data patterns.
5. Honor consent requirements before production analytics collection.
6. Keep `/admin/commercial` local/prototype until authentication and production data policy are approved.

---

## 7. Dashboard requirements

The public beta dashboard should report:

- Top landing variants by click-through.
- Top collections by `collection_view`.
- Top series by `series_view`.
- Top products by `product_view`.
- Top wishlist products.
- Top buy-intent products.
- Search terms and zero-result rate.
- Outbound source clicks.
- Median and 75th percentile session duration.

---

## 8. ADR-011 compliance

RC10 follows ADR-011:

- No Architecture v1.0 documents modified.
- No governance files modified.
- No agents added.
- No ADRs added.
- No payment, order, preservation, or platform write path introduced by this plan.
