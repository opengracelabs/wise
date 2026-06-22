# WISE n8n Workflow Catalog

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Implementation design |
| **Architecture** | architecture-v1.0 (frozen) |
| **Authority** | Maps to `04-system-diagram.md` §2.1 engineering stack extension |

Operational orchestration for WISE using **n8n**. Intelligence remains in **LangGraph** (`packages/wise-orchestration`) and platform FastAPI services. n8n triggers, schedules, routes, notifies, and persists operational state only.

**Workflow exports:** `infrastructure/n8n/workflows/`  
**Infrastructure README:** `infrastructure/n8n/README.md`

---

## 1. Architecture boundary

```mermaid
flowchart TB
    subgraph Ops["Operations plane — n8n"]
        CRON[Schedule triggers]
        WH[Webhooks]
        PG_OPS[(ops.workflow_runs)]
        NOTIFY[Email / Slack]
        GH[GitHub issues & dispatch]
    end

    subgraph Intelligence["Intelligence plane — LangGraph + agents"]
        LG[wise-orchestration<br/>LangGraph RC1 graph]
        DS[discovery-service :8001]
        PS[preservation-service :8003]
        MS[metadata-service :8002]
        KG[knowledge-graph-service :8004]
        BA[Benchmark evaluation hook]
    end

    subgraph Data["Data plane — PostgreSQL"]
        REG[(registry.*)]
        DISC[(discovery.*)]
        PRES[(preservation.*)]
        MOD[(modeling.*)]
        GRP[(graph.*)]
        QLT[(quality.*)]
    end

    CRON -->|POST /orchestration/v1/runs| LG
    CRON -->|POST /v1/discovery/runs| DS
    CRON -->|POST /v1/sources/{id}/harvest| DS
    CRON -->|POST /v1/benchmarks/runs| BA
    WH --> GH

    LG --> DS
    LG --> PS
    LG --> MS
    LG --> KG
    LG --> BA

    DS --> REG
    DS --> DISC
    PS --> PRES
    MS --> MOD
    KG --> GRP
    MS --> QLT

    CRON -->|SELECT aggregates| QLT
    CRON -->|SELECT proposed| DISC
    CRON -->|SELECT proposed| MOD
    CRON -->|SELECT proposed| GRP
    CRON -->|SELECT proposed| QLT

    Ops --> PG_OPS
    Ops --> NOTIFY
    Ops --> GH
```

### Service URLs (docker-compose defaults)

| Service | Internal URL | Port |
|---------|--------------|------|
| `api-service` | `http://api-service:8000` | 8000 |
| `discovery-service` | `http://discovery-service:8001` | 8001 |
| `metadata-service` | `http://metadata-service:8002` | 8002 |
| `preservation-service` | `http://preservation-service:8003` | 8003 |
| `knowledge-graph-service` | `http://knowledge-graph-service:8004` | 8004 |
| PostgreSQL | `postgresql://wise:wise@postgres:5432/wise` | 5432 |

LangGraph RC1 is invoked via a thin **orchestration HTTP adapter** (planned on `api-service` or sidecar) that wraps `build_rc1_graph()` from `packages/wise-orchestration`. n8n never imports Python or calls LangGraph libraries directly.

---

## 2. What n8n does NOT do

n8n is **orchestration only**. The following remain outside n8n by architectural mandate:

| Responsibility | Owner | Why |
|----------------|-------|-----|
| Agent reasoning, scoring, classification | LangGraph nodes + agent services | AI Fabric governance (04 §2.2) |
| Discovery Record generation | Source Discovery Agent (09) via LangGraph or `discovery-service` | Covenant and rights pre-screening |
| Harvest parsing and normalization | `discovery-service` connectors | Domain logic, not cron glue |
| Steward approve/reject decisions | Human stewards via Demonstration Surface / API | Constitutional human-approval gate |
| Resuming LangGraph after approval | Steward-authenticated `POST …/resume` | n8n must not auto-approve |
| Benchmark scoring and compliance checks | Benchmark Agent (23) evaluation hook | Registered benchmark suites |
| Quality review scoring | Quality Review Agent (13) | Curatorial authority |
| Canonical writes (`approved` status) | Platform services after steward action | No shadow write paths |
| Architecture or agent registry changes | Architecture Office / councils | Constitutional plane |
| Choosing which sources to trust | Agent + steward review | n8n may only pass `source_id` from registry query |
| Retry/backoff policy for agent failures | LangGraph `recovery.py` | n8n logs and escalates; does not re-run agent logic |
| Deduplication, entity linking, CIDOC-CRM mapping | Agents 10–12 | Platform intelligence |

**Rule of thumb:** If the step requires reading agent specs (09–13, 23) to implement correctly, it does not belong in n8n.

---

## 3. Operational state schema (`ops`)

n8n persists run metadata in a dedicated schema (migration planned; not yet in repo). Application agents do not depend on these tables.

```sql
CREATE SCHEMA IF NOT EXISTS ops;

CREATE TABLE ops.workflow_runs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id     TEXT NOT NULL,           -- e.g. wise-daily-discovery-run
    trigger_type    TEXT NOT NULL,           -- schedule | webhook | manual
    started_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    finished_at     TIMESTAMPTZ,
    status          TEXT NOT NULL,           -- running | succeeded | failed | partial
    external_ref    TEXT,                    -- LangGraph thread_id, harvest job_id, etc.
    summary         JSONB NOT NULL DEFAULT '{}',
    error_message   TEXT
);

CREATE TABLE ops.workflow_run_events (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id          UUID NOT NULL REFERENCES ops.workflow_runs(id),
    event_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    level           TEXT NOT NULL,           -- info | warn | error
    message         TEXT NOT NULL,
    payload         JSONB
);

CREATE TABLE ops.steward_notifications (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    queue_type      TEXT NOT NULL,           -- discovery | modeling | graph | quality
    artifact_ref    TEXT NOT NULL,
    notified_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    channel         TEXT NOT NULL,           -- email | slack
    dedupe_key      TEXT NOT NULL UNIQUE
);
```

---

## 4. Workflow catalog

| # | Workflow ID | Name | Cron (UTC) | Trigger | Export file |
|---|-------------|------|------------|---------|-------------|
| 1 | `wise-daily-discovery-run` | Daily Discovery Run | `0 2 * * *` | Schedule | `01-daily-discovery-run.json` |
| 2 | `wise-daily-harvest-jobs` | Daily Harvest Jobs | `30 2 * * *` | Schedule | `02-daily-harvest-jobs.json` |
| 3 | `wise-daily-quality-report` | Daily Quality Report | `0 6 * * *` | Schedule | `03-daily-quality-report.json` |
| 4 | `wise-daily-benchmark-report` | Weekly Benchmark Report | `0 7 * * 1` | Schedule | `04-daily-benchmark-report.json` |
| 5 | `wise-steward-approval-notifications` | Steward Approval Notifications | `*/30 * * * *` | Schedule | `05-steward-approval-notifications.json` |
| 6 | `wise-ci-failure-escalation` | CI Failure Escalation | — | GitHub webhook | `06-ci-failure-escalation.json` |

---

## 5. Workflow specifications

### 5.1 `wise-daily-discovery-run`

**Purpose:** Start scheduled Reference Capability discovery pipeline runs. LangGraph executes the agent chain (09→11→10→12→13); n8n only fires the run and records outcome.

| Attribute | Value |
|-----------|-------|
| **Schedule** | `0 2 * * *` (02:00 UTC daily) |
| **Trigger type** | Cron → n8n Schedule Trigger |

**Nodes (summary)**

1. **Schedule Trigger** — daily 02:00 UTC
2. **Postgres** — `INSERT INTO ops.workflow_runs (workflow_id, trigger_type, status) VALUES ('wise-daily-discovery-run', 'schedule', 'running') RETURNING id`
3. **HTTP Request** — `POST {{$env.WISE_API_BASE_URL}}/orchestration/v1/runs`
   - Body: `{ "pipeline": "rc1", "stable_id": "stonehenge", "mode": "scheduled", "stop_on_interrupt": true }`
   - Headers: `X-WISE-Trigger: n8n`, `X-WISE-Run-Id: {{$json.id}}`
4. **Wait / Poll** — `GET …/orchestration/v1/runs/{{$json.run_id}}` until `status` ∈ `completed`, `interrupted`, `failed` (max 4h)
5. **Postgres** — update `ops.workflow_runs` with `external_ref` = LangGraph `thread_id`, `summary` = response JSON
6. **IF interrupted** — `pending_interrupt=true` → invoke sub-workflow `wise-steward-approval-notifications` (or rely on its 30-min poll)
7. **IF failed** — GitHub Create Issue + Email error summary
8. **Postgres** — `INSERT ops.workflow_run_events`

**Inputs**

| Input | Source |
|-------|--------|
| RC1 target list | Env `WISE_RC1_TARGETS` (comma-separated `stable_id`) or Postgres config table |
| Orchestration API auth | HTTP Header credential |

**Outputs**

| Output | Destination |
|--------|-------------|
| LangGraph run / thread ID | `ops.workflow_runs.external_ref` |
| Proposed artifacts | Written by LangGraph to `discovery.*`, `preservation.*`, etc. (`status=proposed`) |
| Steward interrupt signal | `approval_gate` in LangGraph state; surfaced via orchestration API |

**PostgreSQL tables touched**

| Table | Access |
|-------|--------|
| `ops.workflow_runs` | INSERT, UPDATE |
| `ops.workflow_run_events` | INSERT |
| `discovery.records` | READ (post-run verification count only) |
| `registry.provenance_events` | READ (optional audit) |

**LangGraph / API endpoints**

| Method | Endpoint | Notes |
|--------|----------|-------|
| `POST` | `/orchestration/v1/runs` | Starts RC1 graph; maps to `build_rc1_graph().invoke()` |
| `GET` | `/orchestration/v1/runs/{run_id}` | Poll run status |
| `POST` | `/orchestration/v1/runs/{run_id}/resume` | **Steward only — not called by n8n** |

**Error handling**

| Failure | Action |
|---------|--------|
| HTTP 5xx / timeout | 3 retries (5m apart); then `status=failed`, GitHub issue `label:ops-discovery`, email ops |
| `interrupted` | Expected at steward gates; not an error |
| `failed` / `dead_letter` | GitHub issue + steward email with `thread_id` |
| Partial RC1 target list failure | `status=partial`; continue other targets; aggregate in summary |

**Steward notification path**

Interrupt → LangGraph sets `pending_interrupt=true` → `wise-steward-approval-notifications` picks up `proposed` rows → email/Slack with link to Demonstration Surface approval UI.

---

### 5.2 `wise-daily-harvest-jobs`

**Purpose:** Trigger harvest jobs for active Source Registry endpoints. Monitoring and logging only — harvest intelligence lives in `discovery-service`.

| Attribute | Value |
|-----------|-------|
| **Schedule** | `30 2 * * *` (02:30 UTC daily, after discovery kickoff) |
| **Trigger type** | Cron |

**Nodes (summary)**

1. **Schedule Trigger**
2. **Postgres** — `INSERT ops.workflow_runs …`
3. **Postgres** — `SELECT id, canonical_name, api_url FROM registry.sources WHERE active = true AND api_url IS NOT NULL`
4. **Split In Batches** — one source per iteration
5. **HTTP Request** — `POST {{$env.WISE_DISCOVERY_URL}}/v1/sources/{{$json.id}}/harvest`
   - Body: `{ "trigger": "n8n-scheduled", "workflow_run_id": "…" }`
6. **Wait / Poll** — `GET …/v1/harvest/jobs/{{$json.job_id}}` until terminal state
7. **Postgres** — verify `registry.provenance_events` row with `event_type='harvest'` for source (READ)
8. **Postgres** — `INSERT ops.workflow_run_events` per source
9. **Aggregate** — Set parent run `status` succeeded/partial/failed
10. **IF any failure** — GitHub issue listing failed `canonical_name`s

**Inputs**

| Input | Source |
|-------|--------|
| Active sources | `registry.sources` |
| Discovery service URL | `WISE_DISCOVERY_URL` |

**Outputs**

| Output | Destination |
|--------|-------------|
| Harvest job IDs | `ops.workflow_run_events.payload` |
| Discovery candidates | `discovery.records` (written by service, `proposed`) |
| Provenance | `registry.provenance_events` (`harvest`) |

**PostgreSQL tables touched**

| Table | Access |
|-------|--------|
| `registry.sources` | READ |
| `registry.provenance_events` | READ (verify) |
| `discovery.records` | READ (count new `proposed` since run) |
| `ops.workflow_runs` | INSERT, UPDATE |
| `ops.workflow_run_events` | INSERT |

**LangGraph / API endpoints**

| Method | Endpoint |
|--------|----------|
| `POST` | `/v1/sources/{source_id}/harvest` |
| `GET` | `/v1/harvest/jobs/{job_id}` |

**Error handling**

| Failure | Action |
|---------|--------|
| Single source harvest fail | Log event, continue batch; mark parent `partial` |
| All sources fail | `failed`, GitHub issue, email |
| Job timeout (>2h) | Mark job failed in event payload; escalate |

**Steward notification path**

New `discovery.records` with `status=proposed` appear in steward queue via workflow 5. No harvest-failure email to stewards unless zero records harvested for authoritative source (warn threshold).

---

### 5.3 `wise-daily-quality-report`

**Purpose:** Aggregate `quality.reviews` into a steward-facing daily report. **No scoring** — SQL aggregation and templated email/Slack only.

| Attribute | Value |
|-----------|-------|
| **Schedule** | `0 6 * * *` (06:00 UTC daily) |
| **Trigger type** | Cron |

**Nodes (summary)**

1. **Schedule Trigger**
2. **Postgres** — multiple read queries (see below)
3. **Code** — assemble markdown report from query results (formatting only)
4. **Postgres** — `INSERT ops.workflow_runs`, store report in `summary`
5. **Email** — send report to steward distribution list
6. **Slack** (optional) — post summary + link to full report in `ops` or object storage
7. **IF** open `proposed` count > threshold → additional alert subject line

**SQL aggregates (read-only)**

```sql
-- By status
SELECT status, COUNT(*) FROM quality.reviews GROUP BY status;

-- By domain and severity (last 24h)
SELECT review_domain, severity, COUNT(*)
FROM quality.reviews
WHERE reviewed_at >= now() - interval '24 hours'
GROUP BY review_domain, severity;

-- Pending steward disposition
SELECT entity_uri, review_domain, severity, composite_score, finding
FROM quality.reviews
WHERE status = 'proposed'
ORDER BY severity DESC, composite_score ASC
LIMIT 50;

-- Cross-check graph coverage
SELECT
  (SELECT COUNT(*) FROM graph.entities WHERE status = 'approved') AS approved_entities,
  (SELECT COUNT(*) FROM quality.reviews WHERE status = 'proposed') AS pending_reviews;
```

**Inputs:** `quality.reviews`, `graph.entities` (READ)

**Outputs**

| Output | Destination |
|--------|-------------|
| Daily quality digest | Email, optional Slack |
| Report snapshot | `ops.workflow_runs.summary` |

**PostgreSQL tables touched**

| Table | Access |
|-------|--------|
| `quality.reviews` | READ |
| `quality.annotations` | READ (if present; count by disposition) |
| `graph.entities` | READ |
| `ops.workflow_runs` | INSERT |

**LangGraph / API endpoints:** None (reporting only). Optional `GET /v1/quality/reviews?status=proposed` if SQL bypass is undesirable.

**Error handling:** Query failure → retry once; on persistent failure GitHub issue `label:ops-quality-report`.

**Steward notification path:** Primary deliverable is the email digest. High-severity `proposed` backlog triggers redundant ping via workflow 5.

---

### 5.4 `wise-daily-benchmark-report`

**Purpose:** Trigger Benchmark Agent evaluation hook (23), collect metrics, distribute fleet scorecard. n8n schedules and delivers; Benchmark Agent scores.

| Attribute | Value |
|-----------|-------|
| **Schedule** | `0 7 * * 1` (07:00 UTC every Monday) |
| **Trigger type** | Cron (weekly; daily micro-benchmarks optional via env flag) |

**Nodes (summary)**

1. **Schedule Trigger**
2. **Postgres** — `INSERT ops.workflow_runs`
3. **HTTP Request** — `POST {{$env.WISE_API_BASE_URL}}/v1/benchmarks/runs`
   - Body: `{ "domain": "composite", "agents": ["09","10","11","12","13"], "trigger": "n8n-scheduled" }`
4. **Poll** — `GET /v1/benchmarks/runs/{run_id}`
5. **Postgres** — READ `registry` agent registry tables when available; store benchmark JSON in `ops.workflow_runs.summary`
6. **IF** any `result` ∈ `fail`, `regression` → GitHub issue `label:benchmark-regression`
7. **Email** — fleet scorecard to Architecture Office + stewards
8. **Slack** (optional) — regression watchlist

**Inputs:** Benchmark API, optional Prometheus/OpenTelemetry endpoints (read by benchmark service, not n8n)

**Outputs**

| Output | Destination |
|--------|-------------|
| Benchmark Reports (JSON-LD) | Returned by API; archived in `ops.workflow_runs.summary` |
| Regression issues | GitHub |

**PostgreSQL tables touched**

| Table | Access |
|-------|--------|
| `ops.workflow_runs` | INSERT, UPDATE |
| `ops.workflow_run_events` | INSERT |
| LangGraph checkpoint tables | READ via benchmark service only |

**LangGraph / API endpoints**

| Method | Endpoint |
|--------|----------|
| `POST` | `/v1/benchmarks/runs` |
| `GET` | `/v1/benchmarks/runs/{run_id}` |
| `GET` | `/v1/benchmarks/reports/{report_id}` |

Benchmark hook aligns with `BenchmarkReportRef` in `wise_orchestration.state` (per-stage `pass|warn|fail|regression`).

**Error handling:** Benchmark timeout 6h; retry once; failure → GitHub issue blocking release notes (informational, not auto-blocking deploy).

**Steward notification path:** Email scorecard; `fail`/`regression` copies Implementation Council distribution.

---

### 5.5 `wise-steward-approval-notifications`

**Purpose:** Human-in-the-loop queue alerts for all `proposed` artifacts awaiting steward action.

| Attribute | Value |
|-----------|-------|
| **Schedule** | `*/30 * * * *` (every 30 minutes) |
| **Trigger type** | Cron (+ optional webhook from orchestration on interrupt) |

**Nodes (summary)**

1. **Schedule Trigger** (or Webhook `POST /webhook/wise-steward-queue`)
2. **Postgres** — union query across approval queues
3. **Filter** — exclude rows already in `ops.steward_notifications` (dedupe by `dedupe_key`)
4. **Split In Batches**
5. **Email** — per-queue template with artifact summary and approval deep link
6. **Slack** (optional) — channel post with counts by queue
7. **Postgres** — `INSERT ops.steward_notifications`

**Union queue query**

```sql
SELECT 'discovery' AS queue_type, stable_id AS artifact_ref, title AS label,
       created_at, 'discovery-record' AS approval_path
FROM discovery.records WHERE status = 'proposed'
UNION ALL
SELECT 'preservation', stable_id, ark, created_at, 'preservation-object'
FROM preservation.objects WHERE status = 'proposed'
UNION ALL
SELECT 'modeling', stable_id, title, created_at, 'metadata-record'
FROM modeling.metadata_records WHERE status = 'proposed'
UNION ALL
SELECT 'graph', stable_id, label, created_at, 'graph-entity'
FROM graph.entities WHERE status = 'proposed'
UNION ALL
SELECT 'quality', entity_uri, review_domain, created_at, 'quality-review'
FROM quality.reviews WHERE status = 'proposed';
```

**Inputs:** Proposed rows across WISE schemas

**Outputs:** Email/Slack notifications; dedupe log

**PostgreSQL tables touched**

| Table | Access |
|-------|--------|
| `discovery.records` | READ |
| `preservation.objects` | READ |
| `modeling.metadata_records` | READ |
| `modeling.entity_assertions` | READ |
| `graph.entities` | READ |
| `quality.reviews` | READ |
| `ops.steward_notifications` | INSERT, READ |

**LangGraph / API endpoints:** Optional webhook receiver only; no agent calls.

**Error handling:** SMTP failure → retry 3×; persist failed notifications for next poll.

**Steward notification path:** Primary workflow. Deep links target `api-service` / Demonstration Surface routes, e.g. `{{$env.WISE_PUBLIC_URL}}/steward/approvals/{{queue_type}}/{{artifact_ref}}`.

---

### 5.6 `wise-ci-failure-escalation`

**Purpose:** GitHub integration for CI failures — create issues, optionally dispatch remediation workflows. Supports platform reliability; not agent logic.

| Attribute | Value |
|-----------|-------|
| **Schedule** | — |
| **Trigger type** | Webhook (GitHub `workflow_run` completed with failure) |

**Nodes (summary)**

1. **Webhook** — GitHub App or generic webhook
2. **IF** — `conclusion == 'failure'` and branch is `main`
3. **GitHub** — Get workflow run logs URL
4. **GitHub** — Create Issue with checklist (link to run, failed job names)
5. **Email** — notify ops (optional)
6. **GitHub** — `workflow_dispatch` → `infrastructure/github/workflows/ci.yml` with `rerun: true` only on manual steward approval sub-branch (disabled by default)

**PostgreSQL tables touched:** `ops.workflow_runs` (log escalation event)

**LangGraph / API endpoints:** None

**Error handling:** Duplicate issues prevented by searching open issues with same `workflow_run.id`.

---

## 6. Integration matrix

| Integration | Workflows | Operations | Credentials |
|-------------|-----------|------------|-------------|
| **PostgreSQL** | All | Read WISE schemas; read/write `ops.*` | `WISE_DATABASE_URL`, role `n8n_ops` |
| **HTTP (api-service)** | 1, 4 | Orchestration + benchmark triggers | API key header |
| **HTTP (discovery-service)** | 1 (alt), 2 | Discovery + harvest jobs | Internal network |
| **LangGraph** | 1 | Via orchestration adapter only | Thread/checkpoint IDs in responses |
| **GitHub** | 1, 2, 4, 6 | Issues, CI status, workflow dispatch | `GITHUB_TOKEN`, repo scope |
| **Email (SMTP)** | 3, 4, 5, 6 | Steward and ops digests | `STEWARD_EMAIL_*` |
| **Slack** | 3, 4, 5 | Optional channel alerts | `SLACK_WEBHOOK_URL` |

---

## 7. Example cron schedules

All times **UTC**. Adjust for local operations timezone in n8n UI.

| Workflow | Cron | Local example (Europe/London, BST) |
|----------|------|-------------------------------------|
| Discovery run | `0 2 * * *` | 03:00 daily |
| Harvest jobs | `30 2 * * *` | 03:30 daily |
| Quality report | `0 6 * * *` | 07:00 daily |
| Benchmark report | `0 7 * * 1` | 08:00 Mondays |
| Steward notifications | `*/30 * * * *` | Every 30 minutes |
| CI escalation | Webhook | On `workflow_run.completed` failure |

**Stagger rationale:** Discovery at 02:00 → harvest at 02:30 (registry endpoints) → quality digest at 06:00 (after overnight agent runs) → benchmark weekly before council review.

---

## 8. Planned HTTP contracts (orchestration adapter)

These endpoints are **not yet implemented** in services (scaffold phase). n8n workflows target this contract for implementation alignment.

### `POST /orchestration/v1/runs`

```json
{
  "pipeline": "rc1",
  "stable_id": "stonehenge",
  "mode": "scheduled",
  "stop_on_interrupt": true
}
```

Response: `{ "run_id": "…", "thread_id": "…", "status": "running" }`

### `POST /v1/sources/{source_id}/harvest`

Response: `{ "job_id": "…", "status": "queued" }`

### `POST /v1/benchmarks/runs`

```json
{
  "domain": "composite",
  "agents": ["09", "10", "11", "12", "13"],
  "trigger": "n8n-scheduled"
}
```

---

## 9. Related documentation

| Document | Relevance |
|----------|-----------|
| [`architecture-overview.md`](../../architecture-overview.md) | Service map, PostgreSQL schemas |
| [`packages/wise-orchestration/README.md`](../../packages/wise-orchestration/README.md) | LangGraph RC1 pipeline |
| [`docs/architecture/canonical/09-source-discovery-agent.md`](../architecture/canonical/09-source-discovery-agent.md) | Discovery + harvest |
| [`docs/architecture/canonical/13-quality-review-agent.md`](../architecture/canonical/13-quality-review-agent.md) | Quality queues |
| [`docs/architecture/canonical/23-benchmark-agent.md`](../architecture/canonical/23-benchmark-agent.md) | Benchmark hooks |
| [`docker-compose.yml`](../../docker-compose.yml) | Service URLs |

---

*Architecture v1.0 frozen. n8n scope: orchestration, notification, and operational persistence only.*
