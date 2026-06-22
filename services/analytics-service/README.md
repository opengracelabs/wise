# analytics-service

RC6 real demand telemetry ingestion service.

| Field | Value |
|-------|-------|
| **Architecture** | architecture-v1.0 |
| **Build phase** | Platform telemetry support |
| **Agent spec** | Existing agents only; no new agent |
| **Port** | `8006` |

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness probe |
| POST | `/api/events` | Anonymous demand telemetry ingestion |
| GET | `/admin/insights` | Aggregated demand insights |

The service accepts anonymous sessions only and rejects extra metadata fields.
