# Orchestration Phase 1 — RC1 Wiring

**Status:** Implemented  
**Authority:** architecture-v1.0 (ADR-011)  
**Depends on:** Phase 0 Orchestration Foundation

---

## Delivered

### Graph state schema (`RC1GraphState`)

Extended fields for Phase 1:

| Field | Purpose |
|-------|---------|
| `orchestrator_run_id`, `thread_id` | Linked to `registry.agent_runs` |
| `current_provenance_event_id` | Latest PREMIS-aligned event in chain |
| `source_registry_refs` | Accumulated Source Registry canonical names |
| `evidence_profiles` | Evidence Output Profile per artifact (03 §6.6) |
| `standards_reports` | Standards Agent pre-approval validation (22) |
| `pipeline_benchmark_report` | Benchmark Agent composite on completion (23) |

### Service integrations

| Agent | Service endpoint | Shared logic |
|-------|------------------|--------------|
| 09 Source Discovery | `POST /v1/rc1/discovery/propose` | `wise_reference.rc1_agents.propose_discovery_record` + Source Registry lookup |
| 11 Preservation | `POST /v1/rc1/preservation/propose` | `propose_preservation` |
| 10 Metadata | `POST /v1/rc1/metadata/propose` | `propose_metadata` |
| 12 Knowledge Graph | `POST /v1/rc1/graph/propose` | `propose_graph_entity` |
| 13 Quality Review | `POST /v1/rc1/quality/propose` | `propose_quality_review` |

Nodes call services via `HttpRC1AgentClient` (default) or `InlineRC1AgentClient` when `WISE_ORCHESTRATION_INLINE=1`.

### Pipeline flow (per stage)

```
agent → benchmark hook → standards hook → steward approval gate → advance
```

Terminal: `complete → pipeline benchmark`

### Orchestrator API

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/v1/rc1/runs` | Start Stonehenge RC1 pipeline |
| POST | `/api/v1/rc1/runs/{thread_id}/resume` | Steward approve/reject |
| GET | `/api/v1/rc1/runs/{thread_id}` | Run record from `registry.agent_runs` |
| GET | `/api/v1/rc1/runs/{thread_id}/state` | LangGraph state snapshot |

---

## Verification

```bash
export WISE_ORCHESTRATION_INLINE=1
export WISE_TEST_DATABASE_URL=postgresql://wise:wise@localhost:5432/wise

pip install -e packages/wise-reference -e packages/wise-orchestration \
  -e services/orchestrator-service -e services/discovery-service

pytest tests/orchestration/test_stonehenge_e2e.py tests/orchestration/test_rc1_service_integration.py -v
```

---

*Governance unchanged — no new capabilities or constitutional structures.*
