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

### Migrations — known gotcha (pre-existing, do not "fix" casually)

Run migrations with `WISE_DATABASE_URL` set to the target DB (psycopg3 driver).
Apply in order: registry → reference → discovery.

- `packages/wise-registry/migrations/env.py` (and `wise-metadata`) open the
  connection with `connectable.connect()` and run a statement before
  `context.begin_transaction()`, so alembic defers the commit and SQLAlchemy 2.0
  **rolls the migration back on close** (exit code is still 0, but no tables are
  created). `wise-reference`/`wise-discovery` use `connectable.begin()` and work
  normally. To actually persist the registry migrations, run them through an
  AUTOCOMMIT engine using the override config saved at
  `~/wise_registry_autocommit.ini` (it sets `sqlalchemy.isolation_level = AUTOCOMMIT`
  and an absolute `script_location`):
  ```bash
  export WISE_DATABASE_URL=postgresql+psycopg://wise:wise@localhost:5432/wise
  (cd packages/wise-registry && alembic -c ~/wise_registry_autocommit.ini upgrade head)
  (cd packages/wise-reference && alembic upgrade head)
  (cd packages/wise-discovery && alembic upgrade head)   # adds discovery.records.source_id + FK; needs registry.sources to exist
  ```
- `packages/wise-discovery/alembic.ini` uses a **relative** `script_location =
  migrations`, so `alembic`/`command.upgrade(...)` only resolves it when the CWD
  is `packages/wise-discovery`.

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

- Set `WISE_TEST_DATABASE_URL` (and `WISE_DATABASE_URL`/`DATABASE_URL`) to the
  `wise_test` psycopg3 URL. Reference/e2e fixtures re-run migrations, so run
  those suites from `packages/wise-discovery` (relative `script_location`, see
  above), e.g.
  `cd packages/wise-discovery && pytest /workspace/tests/reference /workspace/tests/e2e/test_reference_capability_2.py /workspace/tests/e2e/test_reference_capability_3.py`.
- Green suites: smoke (`pytest tests/ -m smoke`), `tests/reference`,
  `tests/e2e/test_reference_capability_2.py`, `tests/e2e/test_reference_capability_3.py`,
  `tests/metadata` (unit), and many `tests/registry` / `tests/discovery` unit tests.

### Known pre-existing breakage (CI is red on `main` — not caused by setup)

- RC1 object path (`services/api-service/src/wise_api/repository.py`) uses
  `joinedload(...).one()` without `.unique()`, so `GET /v1/objects/stonehenge`
  and `tests/e2e/test_reference_capability_1.py` raise 500 / error under
  SQLAlchemy 2.0.
- Several `tests/registry` and `tests/discovery` integration tests fail because
  their fixtures apply the registry migrations via the buggy `env.py` above
  (tables roll back → `relation "registry.source_types" does not exist`).

These are application/migration code defects; do not paper over them as part of
environment setup.
