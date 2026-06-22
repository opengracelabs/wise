# wise-registry

Source Registry v1.1 — PostgreSQL schema, SQLAlchemy models, and Pydantic schemas for institutional source authority.

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

## v1.1 changes

| Change | Detail |
|--------|--------|
| `evidence_uris` | JSONB array replacing single `evidence_uri`; supports multiple supporting evidence sources |
| `previous_event_id` | Optional self-referential FK linking events into a per-source provenance chain |
| Chain validation | `wise_registry.provenance.validate_chain()` and `validate_event_link()` enforce same-source links and detect cycles |

Migration `005_registry_v1_1_provenance_hardening` backfills existing `evidence_uri` values into single-element `evidence_uris` arrays. Downgrade restores `evidence_uri` from the first array element.

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
