# RC12 Traffic Plan

**Status:** Marketing launch traffic plan  
**Authority:** architecture-v1.0 (`architecture-v1.0`, ADR-011)  
**Scope:** Marketing traffic planning only — no governance changes, no Architecture v1.0 changes, no agents, no ADRs

---

## 1. Objective

RC12 uses Pinterest, YouTube, SEO, and email newsletter channels to validate audience demand for Nature & Culture collections, educational series, and read-only product concepts. Traffic goals measure discovery, engagement, and product interest without adding checkout, payment, fulfillment, user accounts, or new platform write paths.

---

## 2. Channel strategy

### Pinterest

Primary role:

- Visual discovery.
- Product-interest validation.
- Collection and heritage/wildlife audience targeting.

Campaign assets:

- `data/marketing/pinterest_campaigns.json`
- Top 25 Collection Pins
- Top 25 Product Pins
- Top 25 Heritage Pins
- Top 25 Wildlife Pins

Primary metrics:

- Pin impressions.
- Saves.
- Outbound clicks.
- Product page views.
- Wishlist and buy-intent events after Pinterest referral.

### YouTube

Primary role:

- Educational reach.
- Narrative trust-building.
- Search-driven video discovery.

Campaign assets:

- `data/marketing/youtube_campaigns.json`
- 25 videos across World Heritage, Big Cats, Endangered Species, Ancient Civilizations, and Historic Maps.

Primary metrics:

- Views.
- Average view duration.
- Click-through to collections/series.
- Subscribers or newsletter signups when implemented.

### SEO

Primary role:

- Durable discovery.
- Collection landing page traffic.
- Long-tail educational queries.

Campaign assets:

- `data/marketing/seo_landing_pages.json`
- 100 SEO landing page definitions.

Primary metrics:

- Organic impressions.
- Organic clicks.
- Search event volume.
- Collection and series views from organic traffic.

### Email newsletter

Primary role:

- Retention.
- Editorial launch cadence.
- Product validation prompts.

Suggested cadence:

- Week 1: Nature & Culture mission and Top 10 launch collections.
- Week 2: Big Cats and flagship species.
- Week 3: World Heritage and historic maps.
- Week 4: Product validation and education resources.

Primary metrics:

- Open rate.
- Click rate.
- Collection views.
- Series views.
- Wishlist and buy-intent events.

---

## 3. Traffic goals

### 30 days

| Channel | Goal |
|---------|------|
| Pinterest | 25,000 impressions, 750 outbound clicks, 150 product-interest events |
| YouTube | 5,000 views, 250 site clicks, average 35% video completion |
| SEO | 2,500 organic visits, 300 collection views, 100 search events |
| Email newsletter | 1,000 subscribers or imported readers, 35% open rate, 8% click rate |

Beta success threshold:

- 10,000 total site sessions.
- 1,000 collection views.
- 500 series views.
- 300 product views.
- 100 wishlist events.
- 50 buy-intent events.

### 90 days

| Channel | Goal |
|---------|------|
| Pinterest | 150,000 impressions, 5,000 outbound clicks, 900 product-interest events |
| YouTube | 35,000 views, 1,750 site clicks, 40% average completion on top videos |
| SEO | 20,000 organic visits, 2,500 collection views, 800 search events |
| Email newsletter | 5,000 subscribers/readers, 38% open rate, 10% click rate |

Growth success threshold:

- 75,000 total site sessions.
- 7,500 collection views.
- 3,000 series views.
- 2,000 product views.
- 600 wishlist events.
- 250 buy-intent events.

### 12 months

| Channel | Goal |
|---------|------|
| Pinterest | 1,500,000 impressions, 50,000 outbound clicks, 10,000 product-interest events |
| YouTube | 300,000 views, 18,000 site clicks, 45% average completion on evergreen videos |
| SEO | 250,000 organic visits, 40,000 collection views, 15,000 search events |
| Email newsletter | 50,000 subscribers/readers, 40% open rate, 12% click rate |

Annual success threshold:

- 750,000 total site sessions.
- 100,000 collection views.
- 45,000 series views.
- 40,000 product views.
- 12,000 wishlist events.
- 5,000 buy-intent events.

---

## 4. Measurement plan

Use RC10 analytics event names:

- `page_view`
- `collection_view`
- `series_view`
- `product_view`
- `wishlist`
- `buy_intent`
- `outbound_click`
- `search`
- `session_duration`

Campaign attribution:

- Use UTM parameters for Pinterest, YouTube, SEO experiments, and email.
- Store campaign data only at the anonymous session/event level.
- Compare landing page variants from `data/portfolio/landing_page_experiments.json`.

---

## 5. Content operating model

Weekly launch rhythm:

1. Publish 10-15 Pinterest pins.
2. Publish 1-2 YouTube videos.
3. Publish or refresh 5-10 SEO landing pages.
4. Send one newsletter.
5. Review analytics dashboard for product-interest and content-depth signals.

---

## 6. ADR-011 compliance

RC12 follows ADR-011:

- No Architecture v1.0 documents modified.
- No governance files modified.
- No agents added.
- No ADRs added.
- No payment, order, preservation, or platform write path introduced.
