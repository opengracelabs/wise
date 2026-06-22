# wise-registry

Source Registry v1 — PostgreSQL schema, SQLAlchemy models, and Pydantic schemas for institutional source authority.

Aligns with [09-source-discovery-agent.md](../../docs/architecture/canonical/09-source-discovery-agent.md) and [07-reference-standards.md](../../docs/architecture/canonical/07-reference-standards.md) (RightsStatements.org, Creative Commons).

## Entities

| Entity | Purpose |
|--------|---------|
| `SourceType` | Classification of registry sources (authority, media, geospatial) |
| `License` | Creative Commons and ODbL license URIs |
| `RightsStatus` | RightsStatements.org machine-readable categories |
| `Source` | Registered harvest endpoints and rights posture |
| `ProvenanceEvent` | PREMIS-aligned audit trail for registry changes |

All tables include provenance and audit fields: `created_at`, `updated_at`, `created_by`, `updated_by`, `row_version`.

## Migrations

```bash
export WISE_DATABASE_URL=postgresql+psycopg://wise:wise@localhost:5432/wise
cd packages/wise-registry
pip install -e .
alembic upgrade head
```

## Tests

```bash
export WISE_TEST_DATABASE_URL=postgresql+psycopg://wise:wise@localhost:5432/wise_test
pip install -e packages/wise-registry -e packages/wise-common
pytest tests/registry -v
pytest tests/registry -v -m integration  # PostgreSQL only
```
