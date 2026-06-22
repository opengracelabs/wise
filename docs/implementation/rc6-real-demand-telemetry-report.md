# RC6 Real Demand Telemetry Implementation Report

| Field | Value |
|-------|-------|
| **Capability** | RC6 Real Demand Telemetry Ingestion |
| **Status** | Implemented |
| **Architecture posture** | Architecture v1.0 remains frozen; ADR-011 followed |
| **Governance posture** | No new agents, governance layers, ADRs, or architecture changes |
| **Privacy posture** | Anonymous session telemetry only; no payments, checkout, names, emails, or personal customer data |

---

## Files Changed

### Analytics service

- `services/analytics-service/pyproject.toml`
- `services/analytics-service/README.md`
- `services/analytics-service/Dockerfile`
- `services/analytics-service/src/wise_analytics/__init__.py`
- `services/analytics-service/src/wise_analytics/settings.py`
- `services/analytics-service/src/wise_analytics/models.py`
- `services/analytics-service/src/wise_analytics/schemas.py`
- `services/analytics-service/src/wise_analytics/database.py`
- `services/analytics-service/src/wise_analytics/repository.py`
- `services/analytics-service/src/wise_analytics/main.py`
- `services/analytics-service/src/wise_analytics/routes/events.py`
- `services/analytics-service/migrations/versions/001_user_events.py`

### Demand intelligence package

- `packages/wise-demand-intelligence/pyproject.toml`
- `packages/wise-demand-intelligence/README.md`
- `packages/wise-demand-intelligence/src/wise_demand_intelligence/__init__.py`
- `packages/wise-demand-intelligence/src/wise_demand_intelligence/insights.py`
- `packages/README.md`

### Web demonstration surface

- `apps/web/.env.example`
- `apps/web/lib/demand-events.ts`
- `apps/web/lib/analytics-insights.ts`
- `apps/web/components/insights-dashboard.tsx`

### Platform wiring and tests

- `docker-compose.yml`
- `services/README.md`
- `tests/analytics/conftest.py`
- `tests/analytics/test_events.py`

---

## Database Changes

Created PostgreSQL table:

```sql
user_events (
  id integer primary key,
  type varchar(64) not null,
  entity_id varchar(256) not null,
  entity_type varchar(128) not null,
  timestamp timestamptz not null,
  session_id varchar(128) not null,
  metadata jsonb not null,
  created_at timestamptz not null default now()
)
```

Indexes:

- `type`
- `entity_id`
- `entity_type`
- `timestamp`
- `session_id`

Migration:

- `services/analytics-service/migrations/versions/001_user_events.py`

---

## API Endpoints

### `POST /api/events`

Accepts anonymous demand events:

```json
{
  "type": "page_view | collection_click | series_click | species_click | cta_click",
  "entity_id": "string",
  "entity_type": "string",
  "timestamp": "ISO8601",
  "session_id": "anon_string",
  "metadata": {
    "dwell_time": 12,
    "referrer": "https://example.org",
    "device_type": "desktop"
  }
}
```

Validation:

- Rejects event types outside the RC6 list.
- Rejects extra metadata fields.
- Requires `session_id` to start with `anon_`.
- Rejects obvious personal identifiers such as email-like values.

### `GET /admin/insights`

Returns backend-powered insights:

- `top_viewed_collections`
- `top_clicked_species`
- `top_series_engagement`
- `cta_response_conversion_rate`

---

## Privacy Constraints

Implemented constraints:

- Anonymous session IDs only.
- Browser session IDs are generated as `anon_<uuid>`.
- No names collected.
- No emails collected.
- No payment data collected.
- No checkout events implemented.
- No personal customer identifiers collected.
- Metadata is restricted to:
  - `dwell_time`
  - `referrer`
  - `device_type`
- Browser referrer telemetry strips query strings and fragments before ingestion.
- Extra metadata fields are rejected by the backend schema.
- Local fallback remains browser-local and is not synchronized when backend ingestion fails.

---

## Metrics Implemented

### Event metrics

- Page views
- Collection clicks
- Series clicks
- Species clicks
- CTA clicks
- Dwell time

### Aggregated insights

- Top viewed collections
- Top clicked species
- Top series engagement
- CTA response conversion counts:
  - yes
  - maybe
  - no

### Engagement score

The real telemetry aggregation preserves the RC4/RC5 scoring pattern:

```text
engagement_score = clicks + dwell_time + CTA_rate
```

---

## Tests Run

Backend:

```bash
python3 -m pytest tests/analytics -q
```

Result:

```text
5 passed
```

Frontend:

```bash
cd apps/web
npm run typecheck
npm run build
npm audit --omit=dev
```

Results:

- Typecheck passed.
- Production build passed.
- `npm audit --omit=dev` found 0 vulnerabilities.

---

## Known Gaps

- Analytics migrations are included, but this branch does not add a migration runner for `analytics-service`.
- Admin insights currently expose aggregate counts only; no time-window filters are implemented.
- CTA yes/maybe/no conversion is encoded through anonymous `cta_click` entity types such as `collection:yes`.
- No rate limiting is implemented yet.
- No bot filtering is implemented yet.
- No cross-device identity stitching is implemented by design, to preserve anonymous behavior.
- No payment, checkout, or revenue telemetry is implemented.

---

## Next Recommended Release

Recommended next release: **RC6.1 Privacy-Preserving Demand Analytics Hardening**

Scope:

1. Add migration execution wiring for `analytics-service`.
2. Add rate limiting for `POST /api/events`.
3. Add time-window query parameters for `GET /admin/insights`.
4. Add bot/user-agent filtering without storing personal identifiers.
5. Add deployment documentation for `NEXT_PUBLIC_ANALYTICS_API_URL` and CORS origins.
6. Add dashboard date-range controls backed by aggregate-only API responses.

No governance, agent, ADR, or Architecture v1.0 changes are required for RC6.1.
