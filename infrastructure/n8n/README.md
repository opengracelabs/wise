# n8n operational workflows (architecture-v1.0 Phase 0)

Workflow exports for the orchestration profile. Import via n8n UI or API.

| Workflow | File | Purpose |
|----------|------|---------|
| WF-02 Steward approval queue | `wf-02-steward-approval-queue.json` | Webhook stub for steward notifications on LangGraph interrupt |

Start n8n with the orchestration profile:

```bash
docker compose --profile orchestration up -d n8n orchestrator-service
```

Orchestrator API base: `http://orchestrator-service:8005/api/v1`
