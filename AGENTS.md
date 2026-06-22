# AGENTS.md

## Cursor Cloud specific instructions

WISE is a Python 3.12 FastAPI microservices monorepo (see `README.md` and
`architecture-overview.md` for the full service map). The notes below capture
non-obvious, durable context for running/testing it in the Cursor Cloud VM. The
startup update script already refreshes Python dependencies (all `packages/*`
and `services/*` installed editable, plus `pytest httpx geoalchemy2`).

### Database (PostgreSQL 16 + PostGIS + pgvector)

- Postgres is installed natively (not Docker — Docker is not available in this
  VM). It does **not** auto-start; start the cluster each session:
  `sudo pg_ctlcluster 16 main start`
- Role `wise` / password `wise` (SUPERUSER). Two databases exist and are
  pre-seeded with the Reference Capability data: `wise` (dev) and `wise_test`
  (tests). Connect with the **psycopg3** driver:
  `postgresql+psycopg://wise:wise@localhost:5432/wise`
- If a database must be rebuilt: create it, apply
  `infrastructure/docker/postgres/init/01-extensions.sql` (extensions +
  schemas), then run migrations as described below.

### Migrations

Run migrations with `WISE_DATABASE_URL` set to the target DB (psycopg3 driver).
Apply in order: registry → reference → metadata → discovery. All packages now
commit normally with plain `alembic upgrade head` (the RC0 sprint fixed the
registry rollback and metadata revision-graph defects — see
`docs/implementation/rc0-stabilization-report.md`):
```bash
export WISE_DATABASE_URL=postgresql+psycopg://wise:wise@localhost:5432/wise
(cd packages/wise-registry  && alembic upgrade head)
(cd packages/wise-reference && alembic upgrade head)
(cd packages/wise-metadata  && alembic upgrade head)   # needs registry.sources (FKs)
(cd packages/wise-discovery && alembic upgrade head)   # adds discovery.records.source_id + FK
```
- Still open (out of RC0 scope): `packages/wise-discovery/alembic.ini` uses a
  **relative** `script_location = migrations`, so bare `alembic`/
  `command.upgrade(...)` only resolves it when the CWD is
  `packages/wise-discovery`. (The `tests/registry|metadata|discovery` conftests
  override `script_location` to an absolute path, so they are unaffected; only
  `tests/reference`/`tests/e2e` rely on the relative path.)

### Running services

- API gateway (the product's public read surface): from `services/api-service`,
  `DATABASE_URL=postgresql+psycopg://wise:wise@localhost:5432/wise uvicorn wise_api.main:app --port 8000`.
  `DATABASE_URL` must use the `postgresql+psycopg://` driver — a bare
  `postgresql://` URL selects the psycopg2 dialect, which is **not installed**.
- Working endpoints (real seeded data): `GET /health`,
  `GET /v1/species/panthera-leo`, `GET /v1/areas/everglades-national-park`,
  `GET /v1/map/search?bbox=-82.0,25.0,-80.0,26.0`, and the HTML pages at
  `/areas/everglades-national-park` and `/objects/panthera-leo`.
- Other services (`discovery`, `metadata`, `preservation`, `knowledge-graph`,
  `orchestrator`) are FastAPI apps run with `uvicorn <module>:app --port <port>`
  (ports 8001–8005); modules are in each service's Dockerfile `CMD`. They are
  optional for the read surface.

### Tests

- Set `WISE_TEST_DATABASE_URL` (and `WISE_DATABASE_URL`/`DATABASE_URL`) to a
  psycopg3 URL. Reference/e2e fixtures re-run migrations and rely on the relative
  discovery `script_location`, so run those suites from `packages/wise-discovery`,
  e.g.
  `cd packages/wise-discovery && pytest /workspace/tests/reference /workspace/tests/e2e`.
- The `tests/registry|metadata|discovery` conftests **drop their schemas but not
  the `alembic_version_*` tables** (which live in `public`). Reusing one database
  across different suites can therefore leave a stale version table that makes a
  later `command.upgrade(..., "head")` a no-op (skipping table creation). Run each
  integration suite against a **fresh** database (drop/recreate + apply
  `01-extensions.sql`) for reliable results.
- Green after RC0: smoke (`pytest tests/ -m smoke`), `tests/reference`, all three
  `tests/e2e/test_reference_capability_*.py`, `tests/test_contracts.py`,
  `tests/test_species_contracts.py`; `tests/registry` 52/53, `tests/metadata`
  23/24, `tests/discovery` 21/22.

### Remaining known breakage (out of RC0 scope)

- `tests/registry/test_migrations.py::test_v1_1_migration_upgrade_downgrade` —
  the v1.1 provenance migration's **downgrade** does not drop `previous_event_id`.
- `tests/metadata/test_pipeline.py::test_pipeline_processes_wikidata_record` and
  `tests/discovery/test_agent_integration.py::test_create_discovery_record_persists_chain`
  — cross-schema SQLAlchemy `NoReferencedTableError` (modeling/discovery models
  reference `registry.*` tables that are not imported into the same mapper
  registry at configuration time).

These are application/test defects; do not paper over them as part of setup.
