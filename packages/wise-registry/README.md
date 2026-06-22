# wise-registry

Source Registry v1.2 — PostgreSQL schema, SQLAlchemy models, and Pydantic schemas for institutional source authority, rights, provenance, attribution, and publication approval.

Aligns with [09-source-discovery-agent.md](../../docs/architecture/canonical/09-source-discovery-agent.md) and [07-reference-standards.md](../../docs/architecture/canonical/07-reference-standards.md) (RightsStatements.org, Creative Commons).

## Entities

| Entity | Purpose |
|--------|---------|
| `SourceType` | Classification of registry sources (authority, media, geospatial) |
| `License` | Creative Commons and ODbL license URIs |
| `RightsStatus` | RightsStatements.org machine-readable categories |
| `Source` | Registered harvest endpoints and rights posture |
| `ProvenanceEvent` | PREMIS-aligned audit trail for registry changes |
| `Asset` | RC17 asset registry entry with source, license, provenance, rights, and publication gates |
| `Attribution` | Required attribution text, credit line, URI, source, license, and rights context for an asset |
| `PublicationApproval` | Human publication approval workflow with RC17 gate snapshot |

All tables include provenance and audit fields: `created_at`, `updated_at`, `created_by`, `updated_by`, `row_version`.

## v1.1 changes

| Change | Detail |
|--------|--------|
| `evidence_uris` | JSONB array on `provenance_events` from initial schema; supports multiple supporting evidence sources |
| `stable_id` | Immutable pipeline alias on `sources` from initial schema (e.g. `unesco-whc`, `ramsar`) |
| `previous_event_id` | Optional self-referential FK linking events into a per-source provenance chain (migration `005`) |

Migration `006_merge_rc3_and_v1_1` merges the RC3 conservation branch with the agent/orchestration v1.1 hardening branch.

## RC17 rights and provenance infrastructure

Migration `007_rc17_rights_provenance` adds:

| Change | Detail |
|--------|--------|
| Source verification | `sources.source_verification_status`, verifier, timestamp, and `rights_status_id` |
| Asset registry | `assets` table with source, license, provenance, rights, and publication gate states |
| Attribution registry | `attributions` table with required credit and rights display context |
| Publication approval workflow | `publication_approvals` table with approval snapshots and reviewer fields |
| Gate enforcement | Database constraints prevent publication approval unless Source, License, Provenance, and Rights gates have passed |

The RC17 publishability sequence is:

```text
Source Verified -> License Verified -> Provenance Verified -> Rights Approved -> Publication Approved
```

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
