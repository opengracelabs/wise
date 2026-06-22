# Orchestration Phase 0 — Implementation Plan

**Status:** Implemented  
**Authority:** architecture-v1.0 (`architecture-v1.0`, ADR-011)  
**Scope:** Orchestration Foundation only — no governance redesign, no new capabilities

---

## Delivered

### Repository structure

```
data/registry/
  agents/manifest.yaml              # 15 canonical agents
  capabilities/manifest.yaml        # 12 canonical capabilities

packages/
  wise-contracts/                   # + orchestration.py contracts
  wise-registry/                    # + agent/capability models, migrations 003–004
  wise-orchestration/               # LangGraph graphs, validation, checkpointer
    src/wise_orchestration/data/    # packaged manifest copies for containers

services/
  orchestrator-service/             # FastAPI control plane (:8005)

infrastructure/
  n8n/                              # sidecar config + WF-02 steward webhook stub
  docker/postgres/init/             # + orchestration schema

tests/orchestration/                # unit + integration tests
```

### Migrations

| Revision | Purpose |
|----------|---------|
| `003_agent_capability_registry` | `registry.agents`, `registry.capabilities`, `registry.agent_runs`, `orchestration.steward_tasks` |
| `004_seed_agents_capabilities` | Seed 15 agents + 12 capabilities from manifests |

### Contracts (`wise-contracts.orchestration`)

- `AgentRegistryEntry`, `CapabilityRegistryEntry`, `CapabilityAgentLink`
- `RunStartRequest`, `RunResumeRequest`, `AgentRunRecord`
- `BenchmarkReport`, `StandardsComplianceReport` (read-only governance outputs)

### Startup validation

`orchestrator-service` calls `validate_registry_alignment()` on startup. Service **fails to start** if:

- Agent manifest count ≠ 15
- Capability manifest count ≠ 12
- Database rows diverge from manifests
- `langgraph_graph_id` set ≠ `GRAPH_REGISTRY` keys
- Read-only governance graphs include `canonical_write` nodes

### Human approval gates

Writable agent graphs: `propose_output` → `await_steward_approval` (LangGraph `interrupt`) → `canonical_write_guard`.

- `POST /api/v1/runs` — starts run, creates `steward_tasks` row on interrupt
- `POST /api/v1/runs/{thread_id}/resume` — steward approve/reject, resumes graph
- `canonical_write_guard` raises if `approval_status != approved` or `read_only == true`

Governance agents (`standards`, `benchmark`): read-only graph ending at `governance_report` — no steward task, no canonical write path.

### n8n sidecar

```bash
docker compose --profile orchestration up -d orchestrator-service n8n
```

WF-02 steward approval webhook stub at `infrastructure/n8n/workflows/wf-02-steward-approval-queue.json`.

---

## Phase 1 next steps (not in this delivery)

1. RC1 pipeline graph wiring discovery → preservation → metadata → knowledge-graph services
2. n8n WF-01 scheduled harvest for Stonehenge
3. Benchmark Agent subgraph with gold datasets in MinIO
4. Standards Agent SHACL/DwC validators
5. OpenTelemetry on `registry.agent_runs`

---

## Verification

```bash
# Install
pip install -e packages/wise-common -e packages/wise-contracts \
  -e packages/wise-registry -e packages/wise-orchestration \
  -e services/orchestrator-service

# Migrations (requires PostgreSQL)
cd packages/wise-registry && WISE_DATABASE_URL=... alembic upgrade head

# Tests
WISE_TEST_DATABASE_URL=postgresql://wise:wise@localhost:5432/wise pytest tests/orchestration -v
```

---

*Governance unchanged: Agent Registry → Benchmarks → Evaluations → Safety Reviews → Human Approval (04-system-diagram §2.2)*
