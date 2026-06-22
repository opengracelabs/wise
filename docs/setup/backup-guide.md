# Backup Guide

| Field | Value |
|-------|-------|
| **Status** | Operational documentation (non-governance) |
| **Date** | 2026-06-22 |
| **Scope** | Backing up WISE state: PostgreSQL, MinIO object store, and configuration |
| **Authority** | Companion to `05-physical-architecture.md` (tiered storage, zones), `ADR-009` (OAIS preservation). Does not modify Architecture v1.0, governance, ADRs, or the Agent Registry. |

> Preservation-grade durability (multi-zone, fixity, OAIS) is an architectural commitment (ADR-007, ADR-009). This guide covers **operational** backups of the running system; it is not a substitute for the canonical preservation tiers.

## 1. What to back up

| Asset | Store | Criticality | Method |
|-------|-------|-------------|--------|
| Canonical relational data (registry, discovery, modeling, graph, quality, conservation, species) | PostgreSQL | **Critical** | `pg_dump` / base backup |
| Preserved bitstreams & BagIt packages | MinIO bucket `wise-preservation` | **Critical** | `mc mirror` / versioning |
| Alembic version state | PostgreSQL (`alembic_version_*` tables) | Critical | included in `pg_dump` |
| Reference/seed data | git (`data/reference/`, `data/portfolio/`) | Recoverable | git history |
| Config / env | secrets manager + `.env` | Critical | secrets backup (never commit secrets) |
| n8n workflows | git (`infrastructure/n8n/`) + `n8n_data` volume | Recoverable | git + volume snapshot |

## 2. PostgreSQL

### Logical dump (per database)
```bash
PGPASSWORD=wise pg_dump -h localhost -U wise -d wise -Fc \
  -f backups/wise_$(date +%Y%m%dT%H%M%S).dump          # custom format, compressed
```
- Use `-Fc` (custom) for selective/parallel restore. Dump `wise` (and any other live DBs).
- PostGIS/pgvector: ensure the extensions exist on the restore target before restore (the `01-extensions.sql` init handles this).

### Physical / PITR (production)
For point-in-time recovery, run continuous archiving (`archive_mode=on`, WAL archiving) plus periodic base backups (`pg_basebackup`). Recommended for production; logical dumps are sufficient for dev/staging.

### Verify
```bash
pg_restore --list backups/wise_*.dump | head     # backup is readable
```

## 3. MinIO (object storage)

```bash
mc alias set wise http://localhost:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"
mc mirror --overwrite wise/wise-preservation  backups/minio/wise-preservation
```
- Enable **bucket versioning** in production so overwrites/deletes are recoverable.
- Bitstreams are the irreplaceable artifacts — prioritize off-site/multi-zone copies (05-physical-architecture §3, tiers T0→Deep).

## 4. Schedule & retention (recommended)

| Tier | Frequency | Retention |
|------|-----------|-----------|
| PostgreSQL logical dump | daily | 30 days |
| PostgreSQL base backup + WAL | continuous + weekly base | 90 days |
| MinIO mirror | daily (or versioning, continuous) | per preservation policy |
| Config/secrets | on change | versioned |

Automate via cron / scheduled job (or an n8n workflow). Store backups in a different zone from the primary (ADR-007).

## 5. Restore drills

A backup is only valid if it restores. Run the **Recovery Guide** (`recovery-guide.md`) procedure against a scratch database at least quarterly and record the result. Track RPO (target ≤ 24h with daily dumps; minutes with PITR) and RTO.

---

*Operational documentation. Does not modify Architecture v1.0, governance, ADRs, or the Agent Registry.*
