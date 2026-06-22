# RC0 Stabilization Report

**Branch:** `cursor/setup-dev-environment-f9bd`
**Date:** 2026-06-22
**Scope:** RC0 stabilization — application + migration defects blocking Reference
Capability 1 (`GET /v1/objects/stonehenge`) and the RC1/registry/metadata test
paths. Architecture v1.0 frozen per [ADR-011](../architecture/canonical/08-decision-record.md#adr-011-architecture-freeze-v10):
no architecture, agent, or governance changes. This is implementation
stabilization only, the priority ADR-011 designates after the freeze.

## Summary

| # | Defect | Severity | Disposition |
|---|--------|----------|-------------|
| 1 | RC1 aggregate read raises 500 — `joinedload(...).one()` without `.unique()` | P0 | **Fixed** |
| 2 | Registry migrations silently roll back (exit 0, no tables) | P0 | **Fixed** |
| 3 | Metadata migration aborts with `KeyError` (cross-package `depends_on`) | P0 | **Fixed** |
| 4 | RC1 e2e aggregate asserts wrong UNESCO `stable_id` (surfaced by #1 fix) | P1 | **Fixed** |
| 5 | `tests/registry` v1.1 migration **downgrade** leaves `previous_event_id` | P2 | Deferred (out of scope) |
| 6 | Cross-schema ORM `NoReferencedTableError` in metadata/discovery tests | P2 | Deferred (out of scope) |
| 7 | `wise-discovery/alembic.ini` relative `script_location` | P2 | Deferred (out of scope) |

CI on `main` was red prior to this sprint. Defects 1–4 are fixed and validated;
defects 5–7 are documented for a follow-up sprint (no fix attempted, per scope).

---

## Defect 1 — RC1 aggregate read crashes (`repository.py`)

### Defect
`GET /v1/objects/stonehenge` returned **HTTP 500**;
`tests/e2e/test_reference_capability_1.py::{test_heritage_object_aggregate,
test_api_object_endpoint}` errored.

```
sqlalchemy.exc.InvalidRequestError: The unique() method must be invoked on this
Result, as it contains results that include joined eager loads against collections
```

### Root cause
`services/api-service/src/wise_api/repository.py::get_heritage_object` eager-loads
two **collection** relationships — `PreservationObject.premis_events` and
`GraphEntity.external_links` — with `joinedload(...)`, then calls `.one()`.
SQLAlchemy 2.0 requires `.unique()` before fetching when a query carries a joined
eager load against a collection (the joined rows must be de-duplicated in Python).
The RC2/RC3 repositories avoid this by loading those collections in separate
queries, which is why only the RC1 object path failed.

### Proposed fix (applied)
Add `.unique()` before `.one()` on the two collection-eager-load queries:

```python
preservation = session.scalars(
    select(PreservationObject)
    .where(PreservationObject.stable_id == stable_id)
    .options(joinedload(PreservationObject.premis_events))
).unique().one()
...
graph_entity = session.scalars(
    select(GraphEntity)
    .where(GraphEntity.stable_id == stable_id)
    .options(joinedload(GraphEntity.external_links))
).unique().one()
```

### Validation evidence
Determination requested in the sprint: **`joinedload(...).unique().one()` resolves
`GET /v1/objects/stonehenge`** (now HTTP 200) and **`test_api_object_endpoint`**,
and is necessary for `test_heritage_object_aggregate` — but the aggregate test
required a second, independent fix (Defect 4) to pass fully.

- Before: `GET /v1/objects/stonehenge` → `HTTP 500`; RC1 e2e `2 failed, 1 passed`.
- After: `GET /v1/objects/stonehenge` → `HTTP 200`
  (`title=Stonehenge`, `ark=ark:/99999/373/stonehenge/`,
  `quality_review.disposition=accepted`, `graph_entity` Wikidata `Q39671`,
  6 provenance events); RC1 e2e `3 passed` (with Defect 4).
- Browser walkthrough of the public object page `/objects/stonehenge` rendering
  end-to-end (composite quality score 0.96) recorded as RC0 validation evidence.

---

## Defect 2 — Registry migrations silently roll back

### Defect
`(cd packages/wise-registry && alembic upgrade head)` exited `0` and logged every
`Running upgrade …`, but **no tables persisted**:
`to_regclass('registry.sources')` was `NULL` and `alembic_version_registry` did
not exist. Downstream symptoms: `GET /v1/objects/*` source resolution failed, and
~21 `tests/registry` integration tests failed with
`relation "registry.source_types" does not exist`.

### Root cause
`packages/wise-registry/migrations/env.py::run_migrations_online` opened the
connection with `connectable.connect()` (commit-as-you-go) and, **before**
`context.begin_transaction()`, executed a statement via
`_ensure_version_table_width(connection)`. Under SQLAlchemy 2.0 that statement
auto-begins a transaction on the connection. Alembic's `begin_transaction()` then
detects the connection is already in a transaction, treats it as an
externally-managed transaction, and does **not** commit it. Because `env.py` used
`.connect()` (not `.begin()`) and never called `connection.commit()`, the
`with connectable.connect()` block rolled the whole migration back on close — so
the exit code was `0` but nothing was committed.

The sibling `wise-reference/env.py` does **not** exhibit this because it uses
`connectable.begin()` (which commits on block exit); `wise-discovery`/
`wise-metadata` avoid it because they do not execute before
`context.begin_transaction()`.

### Proposed fix (applied)
Mirror the working `wise-reference/env.py`: use `connectable.begin()` and let the
context manager own the single transaction (drop the redundant inner
`context.begin_transaction()` wrapper):

```python
with connectable.begin() as connection:
    _ensure_version_table_width(connection)
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
        version_table="alembic_version_registry",
    )
    context.run_migrations()
```

### Validation evidence
On a freshly created database (`01-extensions.sql` only), with **plain** alembic
(no AUTOCOMMIT workaround):

- Before: `alembic upgrade head` exit `0`; `to_regclass('registry.sources') = NULL`;
  `alembic_version_registry = NULL`.
- After: `alembic upgrade head` exit `0`; `registry.sources` present with **9 rows**;
  `alembic_version_registry` present at head.
- `tests/registry`: **52 passed, 1 failed** (was 21 failed; the 1 remaining is
  Defect 5, a downgrade test out of scope).

---

## Defect 3 — Metadata migration aborts (`KeyError`)

### Defect
`(cd packages/wise-metadata && alembic upgrade head)` exited **non-zero** during
revision-graph construction — before any DDL ran:

```
KeyError: '001_initial_source_registry'
  ... alembic/script/revision.py _add_depends_on
```

This is a **revision-graph resolution failure**, not a transaction rollback: the
metadata `env.py` is structurally identical to the working `wise-discovery/env.py`
and commits correctly once the graph resolves.

### Root cause
`packages/wise-metadata/migrations/versions/001_initial_modeling_schema.py`
declared a cross-package Alembic dependency:

```python
depends_on = ("001_initial_source_registry",)
```

`001_initial_source_registry` lives in the **`wise-registry`** version directory,
which is not on the `wise-metadata` revision path. When Alembic builds the metadata
revision map it cannot resolve the referenced revision and raises `KeyError`,
aborting the migration. The intended ordering (registry before metadata) does not
require an Alembic `depends_on`: it is already guaranteed operationally and by the
foreign keys the modeling tables declare into `registry.sources` /
`registry.provenance_events` (which fail at DDL time if registry is absent).

### Proposed fix (applied)
Remove the unresolvable cross-package `depends_on` and document the ordering
requirement in the revision module:

```python
# NOTE: the registry schema must be applied before this migration — the modeling
# tables declare FKs into registry.sources / registry.provenance_events. Ordering
# is enforced operationally (registry → metadata) and by those FK constraints.
depends_on = None
```

### Validation evidence
- Before: `alembic upgrade head` exit `1` (`KeyError: '001_initial_source_registry'`).
- After (registry applied first, fresh DB, plain alembic): `alembic upgrade head`
  exit `0`; `modeling.schema_mappings` and the full modeling schema persist.
- `tests/metadata`: **23 passed, 1 failed** (was 4 collection errors; the 1
  remaining is Defect 6, out of scope).

---

## Defect 4 — RC1 e2e asserts wrong UNESCO `stable_id`

### Defect
After Defect 1, `test_heritage_object_aggregate` still failed:

```
AssertionError: assert 'unesco-whc' == 'unesco'
  view.source_registry.stable_id
```

### Root cause
The canonical registry seed
`packages/wise-registry/migrations/versions/002_seed_initial_sources.py` defines
the UNESCO source with `canonical_name = "unesco"` and
`stable_id = "unesco-whc"`. The Stonehenge discovery record's
`source_registry_ref = "unesco"` resolves via `canonical_name`
(`source_lookup.resolve_source`), so the resolved source's `stable_id` is
`"unesco-whc"`. The test asserted `== "unesco"`, conflating `stable_id` with
`canonical_name`. RC2/RC3 tests pass only because those sources have identical
`canonical_name` and `stable_id` (`gbif`, `ramsar`). The seed is authoritative:
`tests/discovery/test_agent_integration.py` asserts
`source.stable_id == "unesco-whc"`, `tests/registry/test_migrations.py` pairs
`("unesco", "unesco-whc")`, and `packages/wise-registry/README.md` documents
`unesco-whc` as a `stable_id` example.

### Proposed fix (applied)
Correct the test assertion to the canonical `stable_id` (test-only change; the
seed is left untouched):

```python
assert view.source_registry.stable_id == "unesco-whc"
```

### Validation evidence
- `tests/e2e/test_reference_capability_1.py`: **3 passed** (fresh DB, fixture
  builds the full schema through the now-fixed migrations).

---

## Consolidated validation

All runs use PostgreSQL 16 + PostGIS + pgvector and the `postgresql+psycopg`
driver; integration suites run against a freshly created database.

| Check | Before | After |
|-------|--------|-------|
| `GET /v1/objects/stonehenge` | HTTP 500 | HTTP 200 |
| registry `alembic upgrade head` persistence | rolled back (0 tables) | 9 source rows, version table present |
| metadata `alembic upgrade head` | `KeyError` (exit 1) | applies, schema persists |
| `pytest tests/ -m smoke` | 10 passed | 10 passed |
| `tests/reference` + RC1/RC2/RC3 e2e + contracts | RC1 errored | **37 passed** |
| `tests/registry` | 21 failed | 52 passed, 1 failed (Defect 5) |
| `tests/metadata` | 4 errors | 23 passed, 1 failed (Defect 6) |
| `tests/discovery` | 6 failed | 21 passed, 1 failed (Defect 6) |

---

## Out of scope (deferred; no change made)

Per ADR-011 and the sprint's stated scope, the following pre-existing defects were
characterized but **not** modified:

- **Defect 5** — `tests/registry/test_migrations.py::test_v1_1_migration_upgrade_downgrade`:
  the v1.1 provenance migration's `downgrade()` does not remove `previous_event_id`.
- **Defect 6** — `tests/metadata/test_pipeline.py::test_pipeline_processes_wikidata_record`
  and `tests/discovery/test_agent_integration.py::test_create_discovery_record_persists_chain`:
  SQLAlchemy `NoReferencedTableError` for FKs from `modeling.*` / `discovery.records`
  into `registry.*` — the registry models are not imported into the same mapper
  registry at configuration time.
- **Defect 7** — `packages/wise-discovery/alembic.ini` uses a relative
  `script_location = migrations`, so bare `alembic`/`command.upgrade` only resolves
  it from the package directory (the integration conftests already override it to
  an absolute path).

No architecture, agent specification, or governance artifact was added or changed.

---

*Authority: implementation map only. Canonical architecture:
[docs/architecture/canonical/](../architecture/canonical/) ·
Freeze: [ADR-011](../architecture/canonical/08-decision-record.md#adr-011-architecture-freeze-v10).*
