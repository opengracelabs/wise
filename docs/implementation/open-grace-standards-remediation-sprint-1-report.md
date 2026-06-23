# Open Grace Standards Remediation Sprint 1 Report

| Field | Value |
|-------|-------|
| **Version** | 1.0.0 |
| **Date** | 2026-06-23 |
| **Baseline maturity** | 61 / 100 |
| **Estimated post-sprint maturity** | **75 / 100** |

## Executive Summary

Sprint 1 delivers four workstreams addressing the highest-priority gaps from the [standards audit](./open-grace-agent-system-standards-audit.md): PostgreSQL-ready registry persistence, runtime OpenTelemetry instrumentation, OpenSSF supply-chain controls, and portal execution visibility.

## Architecture

```mermaid
flowchart TB
  subgraph persistence [Workstream 1 — Registry DB]
    YAML[Package YAML seeds]
  JSON[JsonRegistryStore JSON]
  DB[(open-grace-registry-db SQLite/Postgres)]
  YAML -->|seed_all_from_yaml| DB
  JSON -->|sync_json_store| DB
  DB -->|export_all_json| JSON
  end

  subgraph runtime [Workstream 2 — Runtime v2 OTel]
    LG[LangGraph nodes]
    INST[RuntimeInstrumentation]
    PROM[Prometheus metrics]
    LG --> INST --> PROM
  end

  subgraph cicd [Workstream 3 — OpenSSF]
    CI[open-grace-ci.yml]
    AUDIT[pip-audit]
    SBOM[CycloneDX SBOM]
    SEC[SECURITY.md]
  end

  subgraph portal [Workstream 4 — Portal]
    RT[.open-grace-runtime JSON]
    SYNC[sync-seed-data.mjs]
    PAGES[/executions pages]
    RT --> SYNC --> PAGES
  end
```

## Workstream Deliverables

### 1. Registry DB (`packages/open-grace-registry-db/`)

| Component | Path |
|-----------|------|
| SQLAlchemy models | `src/open_grace_registry_db/models.py` |
| Repository pattern | `src/open_grace_registry_db/repositories.py` |
| YAML import / JSON export | `src/open_grace_registry_db/sync.py` |
| Alembic migration | `migrations/versions/001_initial.py` |
| Tests | `tests/open_grace/test_registry_db.py` |

**Design:** Additive layer — `JsonRegistryStore` YAML/JSON path unchanged. Unified `KnowledgeEntry` table with `knowledge_type` discriminator for seven knowledge registries. JSON `payload` column preserves pydantic round-trip fidelity.

### 2. Runtime Observability

| Component | Path |
|-----------|------|
| Node instrumentation | `packages/open-grace-runtime/src/open_grace_runtime/instrumentation.py` |
| LangGraph wiring | `packages/open-grace-runtime/src/open_grace_runtime/langgraph.py` |
| Metric definitions | `packages/open-grace-observability/.../metric_definitions.yaml` |
| Report | [open-grace-observability-report.md](./open-grace-observability-report.md) |

### 3. Supply Chain

| Component | Path |
|-----------|------|
| CI workflow | `.github/workflows/open-grace-ci.yml` |
| Dependency audit | `.github/workflows/open-grace-dependency-audit.yml` |
| Secret scan placeholder | `.github/workflows/open-grace-secret-scan.yml` |
| SBOM | `.github/workflows/open-grace-sbom.yml` |
| Policy | `SECURITY.md` |
| Report | [open-grace-supply-chain-report.md](./open-grace-supply-chain-report.md) |

### 4. Portal Executions

| Component | Path |
|-----------|------|
| List page | `apps/open-grace-registry/src/app/executions/page.tsx` |
| Detail page | `apps/open-grace-registry/src/app/executions/[id]/page.tsx` |
| Seed data | `apps/open-grace-registry/data/executions.json` |
| Runtime sync | `apps/open-grace-registry/scripts/sync-seed-data.mjs` |

## Standards Mapping

| Standard | Pre-sprint | Sprint 1 change | Est. post-sprint |
|----------|-----------:|-----------------|-----------------:|
| OpenSSF | 34 | SBOM, pip-audit, CI, SECURITY.md | 58 |
| OpenTelemetry | 71 | SDK default, runtime node spans, 6 metrics | 82 |
| ISO/IEC 27001 | 63 | Audit trail in portal, SECURITY.md | 68 |
| ISO/IEC 42001 | 66 | DB asset register export, execution metrics | 72 |
| NIST AI RMF | 68 | Runtime MEASURE instrumentation | 72 |
| PROV-O | 53 | Execution → audit linkage in portal | 56 |
| MIT AI Risk | 74 | Risk gate failure metrics | 76 |
| Others | — | Unchanged this sprint | — |

**Weighted maturity estimate:** 75 / 100 (Developing → Approaching Established)

## Tests

```bash
cd /home/nathan/Projects/wise && . .venv/bin/activate && \
  pip install -e packages/open-grace-governance \
              -e packages/open-grace-agent-registry \
              -e packages/open-grace-benchmarking \
              -e packages/open-grace-audit \
              -e packages/open-grace-knowledge \
              -e packages/open-grace-observability \
              -e packages/open-grace-runtime \
              -e packages/open-grace-registry-db -q && \
  python -m pytest tests/open_grace -q
```

| Suite | New tests |
|-------|-----------|
| `test_registry_db.py` | 4 |
| `test_runtime_instrumentation.py` | 4 |
| **Total new** | **8** |

## Gaps Remaining (Sprint 2+)

1. **Critical** — SLSA provenance and Sigstore signing for release artifacts
2. **High** — Steward RBAC integration with WISE auth layer
3. **High** — PROV-O JSON-LD serialization for agent runs
4. **High** — UNESCO/community consent runtime gate
5. **Medium** — OTLP exporter production configuration
6. **Medium** — PostgreSQL production deployment for registry-db (TDE, connection pooling)
7. **Medium** — Internet Archive fixity digests on media records
8. **Low** — Fleet MIT risk dashboard aggregation

## Constraints Observed

- No changes to `docs/architecture/canonical/*`
- `JsonRegistryStore` YAML path unchanged
- All existing tests pass
- Local commit only (no push)

*Implementation report. Does not modify Architecture v1.0 or canonical governance documents.*
