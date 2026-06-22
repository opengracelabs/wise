# wise-discovery

Source Discovery Agent v1 — Discovery capability layer for WISE (architecture-v1.0, ADR-011).

## Capabilities

1. Source registration lookup (`registry.sources`)
2. Source validation (active, trust level, license)
3. Source reachability check (HTTP HEAD/GET)
4. Discovery record creation (`discovery.records`)
5. Evidence profile generation (Evidence Output Profile §6.6)
6. Provenance event creation (`registry.provenance_events`, HARVEST chain)
7. Rights posture propagation (from source license metadata)

## Migrations

Requires `wise-registry` and `wise-reference` migrations applied first:

```bash
export WISE_DATABASE_URL=postgresql+psycopg://wise:wise@localhost:5432/wise
cd packages/wise-registry && alembic upgrade head
cd ../wise-reference && alembic upgrade head
cd ../wise-discovery && alembic upgrade head
```

## Tests

```bash
export WISE_TEST_DATABASE_URL="$WISE_DATABASE_URL"
pytest tests/discovery -v
```
