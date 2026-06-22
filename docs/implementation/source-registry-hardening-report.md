# Source Registry P0 Hardening Remediation Report

**Branch:** `capability/reference-capability-1`  
**Date:** 2026-06-22  
**Scope:** P0 items only — Architecture v1.0 frozen; P1/P2 deferred.

## Findings Accepted (Hardening Review)

| Finding | Severity | Disposition |
|---------|----------|-------------|
| Multiple Alembic heads risk (RC3 branch vs agent/orchestration branch) | P0 | Fixed — explicit merge migration `006_merge_rc3_and_v1_1` |
| Seeds reference deprecated `evidence_uri` column | P0 | Fixed — `evidence_uris` JSONB from migration `001` |
| `stable_id` added late (003) without initial seeds carrying it | P0 | Fixed — `stable_id` in `001` schema; all seeds include values |
| EOL source missing register provenance event | P0 | Fixed — folded into `004_seed_eol_source` |
| No CI guard for migration graph integrity | P0 | Fixed — `scripts/validate_alembic_heads.py` + CI step |
| `rights_status_id` on sources | P1 | Deferred |
| `validate_event_link` write-path enforcement | P1 | Deferred |
| Provenance chain indexes beyond `previous_event_id` | P2 | Deferred |
| `agent_version` on provenance events | P2 | Deferred |

## Changes Made

### Migration graph

```
001_initial_source_registry
├── 002_seed_initial_sources
│   ├── 003_rc3_conservation_sources ──────────────┐
│   └── 003_agent_capability_registry              │
│       ├── 004_seed_eol_source ─────┐             │
│       └── 004_seed_agents_capabilities             │
│                    └── 005_registry_v1_1_provenance_hardening
└──────────────────────────────────── 006_merge_rc3_and_v1_1 (head)
```

- **`001`**: Added `sources.stable_id` (unique); `provenance_events.evidence_uris` JSONB from creation (no `evidence_uri`).
- **`002` / `003_rc3` / `004_seed_eol`**: Seeds use `stable_id`, `jsonb_build_array(...)` for `evidence_uris`; every seeded source gets a `register` provenance event.
- **`005`**: Simplified to add only `previous_event_id` FK + index (agent branch merge point).
- **`006_merge_rc3_and_v1_1`**: Empty merge revision joining RC3 and v1.1 branches — single head.
- **Removed** `006_seed_eol_provenance.py` (logic merged into `004_seed_eol_source`).

### Application layer

- Pydantic `SourceBase` / `SourceCreate` / `SourceRead` already exposed `stable_id` — no schema change required.
- SQLAlchemy `Source` model already mapped `stable_id` — no model change required.
- Integration tests updated for `previous_event_id` downgrade path and `stable_id` on seed sources.

### CI

- Added `scripts/validate_alembic_heads.py` — exits non-zero when head count ≠ 1.
- CI workflow runs validation before `alembic upgrade head`.

## Remaining Risks (Deferred P1/P2)

1. **`rights_status_id`** — Sources still lack direct FK to `rights_statuses`; rights posture inferred via license only.
2. **Write-path chain validation** — `validate_event_link()` is tested but not enforced at repository/service insert layer.
3. **Index coverage** — No composite index on `(source_id, event_timestamp)` for chain traversal at scale.
4. **`agent_version`** — Provenance events do not record agent semver; cross-service audit correlation limited.
5. **E2E stable_id assertion** — `test_reference_capability_1` expects `source_registry.stable_id == "unesco"` but registry seed uses `unesco-whc`; lookup by `canonical_name` still works via `resolve_source()`.

## Validation Evidence

### Alembic heads

```
$ cd packages/wise-registry && alembic heads
006_merge_rc3_and_v1_1 (head)
```

Single head confirmed.

### Final schema (head)

| Table | Column | Present at head |
|-------|--------|-----------------|
| `registry.sources` | `stable_id` | Yes (from 001) |
| `registry.provenance_events` | `evidence_uris` | Yes (from 001) |
| `registry.provenance_events` | `previous_event_id` | Yes (from 005) |
| `registry.provenance_events` | `evidence_uri` | No |

### Tests

```
$ pytest tests/registry -m "not integration" -v
32 passed, 21 deselected in 0.18s
```

```
$ pytest tests/registry -m integration -v   # requires PostgreSQL
```

Integration suite covers seed provenance, v1.1 columns, chain linking, and `stable_id` on seeded sources.
