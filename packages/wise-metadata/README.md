# Metadata Agent v1 — Knowledge Modeling (Phase B)

PostgreSQL schema, SQLAlchemy models, Pydantic schemas, and processing pipeline for institutional metadata normalization per [10-metadata-agent.md](../../docs/architecture/canonical/10-metadata-agent.md).

## Scope

- Metadata normalization (UNESCO, Wikidata, Wikimedia Commons, OpenStreetMap)
- Schema mapping crosswalks (CIDOC-CRM, Dublin Core, SKOS; Darwin Core stub)
- Source and rights validation against Source Registry
- Provenance preservation (modeling + registry chain)
- Evidence Output Profile on all assertion-making outputs (§6.6)
- Authority record proposals (no Knowledge Graph placement)

## Schema (`modeling`)

| Table | Purpose |
|-------|---------|
| `provenance_events` | Modeling-layer PREMIS-aligned events |
| `normalized_records` | Normalized metadata with preserved originals |
| `schema_mappings` | Source field → ontology crosswalk rules |
| `mapping_runs` | Mapping execution audit |
| `entity_assertion_proposals` | RDF-ready proposals (steward-gated) |
| `authority_record_proposals` | GeoNames/Wikidata reconciliation candidates |
| `validation_results` | Source, rights, schema validation outcomes |

All tables include audit fields: `created_at`, `updated_at`, `created_by`, `updated_by`, `row_version`.

## Prerequisites

Apply Source Registry migrations first:

```bash
cd packages/wise-registry && alembic upgrade head
```

## Migrations

```bash
export WISE_DATABASE_URL=postgresql+psycopg://wise:wise@localhost:5432/wise
cd packages/wise-metadata
pip install -e ../wise-registry -e .
alembic upgrade head
```

## Tests

```bash
pip install -e packages/wise-registry -e packages/wise-metadata
pytest tests/metadata -m "not integration" -v
export WISE_TEST_DATABASE_URL=postgresql+psycopg://wise:wise@localhost:5432/wise
pytest tests/metadata -m integration -v
```

## Deferred

- Knowledge Graph placement (Phase 5 / Agent 12)
- SHACL validation engine (validation domain stubs recorded)
- Observatory agents
