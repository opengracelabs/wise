# RC17 Rights & Provenance Infrastructure Report

| Field | Value |
|-------|-------|
| **Status** | Implemented |
| **Date** | 2026-06-22 |
| **Scope** | Asset registry, source registry hardening, license registry linkage, provenance registry linkage, attribution registry, publication approval workflow |
| **Primary package** | `packages/wise-registry` |
| **Migration** | `007_rc17_rights_provenance` |

RC17 implements the rights and provenance publication gate:

```text
Source Verified -> License Verified -> Provenance Verified -> Rights Approved -> Publication Approved
```

No asset is publishable until every gate in that sequence is complete.

---

## 1. Implementation Summary

RC17 extends the existing `wise-registry` infrastructure rather than creating a parallel registry. The repository already contained source, license, rights status, and provenance primitives. This implementation adds the missing asset, attribution, and publication approval workflow infrastructure, and hardens source records with verification state.

| Requirement | Implementation |
|-------------|----------------|
| Asset registry | New `registry.assets` table, SQLAlchemy `Asset` model, and Pydantic schemas |
| Source registry | Existing `registry.sources` extended with `rights_status_id`, `source_verification_status`, `source_verified_at`, and `source_verified_by` |
| License registry | Existing `registry.licenses` linked to sources, assets, and attribution records |
| Provenance registry | Existing `registry.provenance_events` linked to assets through `provenance_event_id` |
| Attribution registry | New `registry.attributions` table, SQLAlchemy `Attribution` model, and Pydantic schemas |
| Publication approval workflow | New `registry.publication_approvals` table, SQLAlchemy `PublicationApproval` model, Pydantic schemas, and publication gate helpers |

---

## 2. Registry Entities

### 2.1 Source Registry

Existing source records now carry explicit source verification and rights status linkage:

- `rights_status_id`
- `source_verification_status`
- `source_verified_at`
- `source_verified_by`

This allows RC17 to distinguish a registered source from a verified source.

### 2.2 License Registry

The existing `License` registry remains the license authority. RC17 links licenses to:

- `Source`
- `Asset`
- `Attribution`

An asset cannot mark the License Verified gate as complete unless `license_id` is present.

### 2.3 Provenance Registry

The existing PREMIS-aligned `ProvenanceEvent` registry remains the provenance authority. RC17 assets link to a provenance event through `provenance_event_id`.

An asset cannot mark the Provenance Verified gate as complete unless `provenance_event_id` is present.

### 2.4 Asset Registry

The new `Asset` registry records publication-relevant asset state:

- stable asset identifier
- asset title and type
- source reference
- optional source record URI and canonical URI
- license reference
- rights status reference
- provenance event reference
- gate state for source, license, provenance, rights, and publication
- verifier and approver fields for each gate

The model exposes:

- `rc17_sequence_complete`
- `publishable`

### 2.5 Attribution Registry

The new `Attribution` registry records the display obligations required for publication:

- asset reference
- source reference
- license reference
- rights status reference
- display text
- credit line
- attribution URI
- required flag
- sort order

### 2.6 Publication Approval Workflow

The new `PublicationApproval` registry records human publication approval:

- asset reference
- approval status
- requester and approval metadata
- publication channel and URI
- source/license/provenance/rights gate snapshots
- attribution snapshot
- decision notes

---

## 3. Gate Enforcement

RC17 uses both model-level and database-level controls.

### 3.1 Model-level controls

`wise_registry.publication` adds:

- `RC17_GATE_SEQUENCE`
- `PublicationGateSnapshot`
- `gate_snapshot(asset)`
- `require_publishable(asset)`

`require_publishable(asset)` raises `PublicationGateError` unless every gate is complete.

### 3.2 Database-level controls

Migration `007_rc17_rights_provenance` adds check constraints:

| Constraint | Purpose |
|------------|---------|
| `ck_assets_verified_license_has_license` | License Verified requires a license reference |
| `ck_assets_verified_provenance_has_event` | Provenance Verified requires a provenance event reference |
| `ck_assets_approved_rights_has_status` | Rights Approved requires a rights status reference |
| `ck_assets_publication_requires_rc17_sequence` | Publication Approved requires Source, License, Provenance, and Rights gates to be complete |
| `ck_publication_approvals_requires_rc17_sequence` | Approved publication approval records require complete gate snapshots and approval timestamp |

---

## 4. Files Added or Updated

### 4.1 Models

- `packages/wise-registry/src/wise_registry/models/asset.py`
- `packages/wise-registry/src/wise_registry/models/attribution.py`
- `packages/wise-registry/src/wise_registry/models/publication_approval.py`
- `packages/wise-registry/src/wise_registry/models/source.py`
- `packages/wise-registry/src/wise_registry/models/license.py`
- `packages/wise-registry/src/wise_registry/models/rights_status.py`
- `packages/wise-registry/src/wise_registry/models/provenance_event.py`
- `packages/wise-registry/src/wise_registry/models/__init__.py`

### 4.2 Schemas and helpers

- `packages/wise-registry/src/wise_registry/schemas/asset.py`
- `packages/wise-registry/src/wise_registry/schemas/attribution.py`
- `packages/wise-registry/src/wise_registry/schemas/publication_approval.py`
- `packages/wise-registry/src/wise_registry/schemas/source.py`
- `packages/wise-registry/src/wise_registry/schemas/__init__.py`
- `packages/wise-registry/src/wise_registry/publication.py`
- `packages/wise-registry/src/wise_registry/enums.py`

### 4.3 Migration

- `packages/wise-registry/migrations/versions/007_rc17_rights_provenance.py`
- `packages/wise-registry/migrations/env.py`

### 4.4 Tests and docs

- `tests/registry/test_enums.py`
- `tests/registry/test_models.py`
- `tests/registry/test_schemas.py`
- `tests/registry/test_migrations.py`
- `tests/registry/test_publication.py`
- `packages/wise-registry/README.md`
- `docs/implementation/rc17-rights-provenance-report.md`

---

## 5. Publication Rule

An asset is publishable only when:

| Gate | Required state |
|------|----------------|
| Source Verified | `source_verification_status == verified` |
| License Verified | `license_verification_status == verified` and `license_id IS NOT NULL` |
| Provenance Verified | `provenance_verification_status == verified` and `provenance_event_id IS NOT NULL` |
| Rights Approved | `rights_approval_status == approved` and `rights_status_id IS NOT NULL` |
| Publication Approved | `publication_approval_status == approved` and `publication_approved_at IS NOT NULL` |

Publication approval records must snapshot all prerequisite gates as complete before they can be approved.

---

## 6. Validation

Commands run:

```bash
python3 -m pytest tests/registry -q
python3 scripts/validate_alembic_heads.py
python3 -c '<markdown link check for this report and packages/wise-registry/README.md>'
git diff --check
```

Results:

- Registry tests: 46 passed, 22 skipped because `WISE_TEST_DATABASE_URL` was not set
- Alembic head validation: passed, single head `007_rc17_rights_provenance`
- Markdown link check: 2 links checked, 0 broken
- Whitespace validation: passed

---

## 7. Remaining Work

The RC17 registry infrastructure is now present. Future integration work should wire these registry states into:

1. metadata pipeline rights validation outputs
2. discovery-service rights posture endpoints
3. API assembler publication gating
4. orchestration steward task queues
5. end-to-end publication surfaces

Those integrations should use the RC17 asset and publication approval registries as the source of truth.
