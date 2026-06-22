# Preservation Agent

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Canonical |
| **Authority** | Open Grace Architecture Office |
| **Date** | 2026-06-22 |
| **Capability** | Preservation ([03-canonical-architecture.md](03-canonical-architecture.md), §4.3) |
| **Phase** | Preservation ([06-build-roadmap.md](06-build-roadmap.md), Phase 3) |

## Document Map

| Document | Purpose |
|----------|---------|
| [01-mission.md](01-mission.md) | Mission, charter, and constitutional relationship |
| [02-reference-models.md](02-reference-models.md) | Institutional reference models informing design |
| [03-canonical-architecture.md](03-canonical-architecture.md) | Canonical 100-year logical architecture |
| [04-system-diagram.md](04-system-diagram.md) | Canonical system diagram |
| [05-physical-architecture.md](05-physical-architecture.md) | Physical and geographic architecture |
| [06-build-roadmap.md](06-build-roadmap.md) | Implementation roadmap and founder build order |
| [07-reference-standards.md](07-reference-standards.md) | Standards, protocols, and interoperability |
| [08-decision-record.md](08-decision-record.md) | Architecture decision records |
| [09-source-discovery-agent.md](09-source-discovery-agent.md) | Source Discovery Agent specification |
| [10-metadata-agent.md](10-metadata-agent.md) | Metadata Agent specification |
| [11-preservation-agent.md](11-preservation-agent.md) | Preservation Agent specification |
| [12-knowledge-graph-agent.md](12-knowledge-graph-agent.md) | Knowledge Graph Agent specification |
| [13-quality-review-agent.md](13-quality-review-agent.md) | Quality Review Agent specification |
| [14-translation-agent.md](14-translation-agent.md) | Translation Agent specification |

---

## 1. Purpose

The **Preservation Agent** automates the Preservation capability ([03-canonical-architecture.md](03-canonical-architecture.md), §4.3). It verifies file integrity, generates and maintains checksums, tracks provenance through preservation events, and monitors preservation risk across the canonical object store.

The agent does not acquire bitstreams (Ingestion), assert knowledge-graph entities (Knowledge Modeling), or publish to the public experience. It stores, protects, and perpetually maintains digital objects — emitting fixity records, preservation events, and risk reports for steward review when policy requires human approval.

---

## 2. Responsibilities

| Responsibility | Description |
|----------------|-------------|
| **Verify files** | Validate bitstream integrity on deposit and on schedule; compare replicas for consistency; alert and initiate restore workflows on fixity failure |
| **Generate checksums** | Compute SHA-256 fixity digests at ingest acceptance and on tier transitions; maintain a checksum registry linked to ARK identifiers |
| **Track provenance** | Emit **Preservation Events** in PREMIS; extend the immutable provenance chain ([03-canonical-architecture.md](03-canonical-architecture.md), §6.2); log migrations, tier transitions, and restore actions |
| **Monitor preservation risk** | Score format obsolescence (PRONOM/DROID), rank migration candidacy, assess replica and vault health, and surface fixity-failure and corruption signals |

---

## 3. Reference Models

The agent synthesizes patterns from two primary reference models:

| Model | Pattern Applied | Agent Behavior |
|-------|-----------------|----------------|
| **OAIS** (ISO 14721) | Archival Storage, audit trail, AIP packaging, preservation planning | Accept validated SIPs from Ingestion; store and replicate objects; emit AIPs to Knowledge Modeling; log fixity and migration events per OAIS Audit requirements ([07-reference-standards.md](07-reference-standards.md), §3) |
| **Internet Archive** ([02-reference-models.md](02-reference-models.md), §12) | Permanence ethic, format migration pipeline, temporal versioning, web archive capture | Continuous fixity verification; proactive migration queue for at-risk formats; retain all object versions permanently; support WARC/ARC ingest paths when Ingestion delivers web-archive packages |

Supporting institutional patterns from Harvard and MIT ([02-reference-models.md](02-reference-models.md), §10, §8) inform ARK assignment, special-collections handling, and repository stewardship — but OAIS and Internet Archive define the agent's operational model.

---

## 4. Position in Architecture

```
Ingestion (BagIt + PREMIS SIP)
        ↓
Preservation Agent
        ↓
Canonical Object Store (MinIO) + ARK Registry + Fixity Registry
        ↓
Fixity Records + Preservation Events (PREMIS) + Risk Reports — pending steward review where required
        ↓
Knowledge Modeling (Preserved Object Descriptor / OAIS AIP)
```

The agent operates in the **Preserve** subgraph of the Platform Plane ([04-system-diagram.md](04-system-diagram.md), §3). All high-impact outputs (migration execution, restore from vault, tier demotion) pass through the AI Fabric governance chain before affecting canonical storage ([04-system-diagram.md](04-system-diagram.md), §2.2).

**Upstream inputs:** Ingest packages from Ingestion ([03-canonical-architecture.md](03-canonical-architecture.md), §7); stewardship policy from Open Grace ([03-canonical-architecture.md](03-canonical-architecture.md), Governance Plane).

**Downstream consumers:** Knowledge Modeling (AIP descriptors), Quality Platform (migration validation), Research Fabric (preserved object access), Observability plane (fixity and audit events).

---

## 5. Operational Targets

### 5.1 Canonical Object Store

| Attribute | Specification |
|-----------|---------------|
| **Storage** | Erasure-coded object store (MinIO) across T0–T3 tiers ([05-physical-architecture.md](05-physical-architecture.md)) |
| **Identifiers** | ARK assignment on first deposit; version history retained permanently |
| **Replication** | ≥ 2 geographic replicas at acceptance; 3+ replicas at Phase 3 completion |
| **Standards** | OAIS Archival Storage, ARK, PREMIS ([07-reference-standards.md](07-reference-standards.md)) |

### 5.2 Fixity Registry

| Attribute | Specification |
|-----------|---------------|
| **Algorithm** | SHA-256 (required) |
| **Events** | Checksum computed at deposit, tier transition, migration, and scheduled re-verification |
| **Linkage** | Each fixity record references ARK, storage tier, replica location, and agent version |
| **Standards** | PREMIS `fixity` events, OAIS Audit ([07-reference-standards.md](07-reference-standards.md), §3) |

### 5.3 Format Risk Monitor

| Attribute | Specification |
|-----------|---------------|
| **Identification** | PRONOM/DROID on ingest; annual corpus-wide obsolescence scan |
| **Scoring** | Risk = format obsolescence × access frequency × replica coverage gaps |
| **Queue** | Quarterly migration priority ranking ([07-reference-standards.md](07-reference-standards.md), §13) |
| **Execution** | Agent proposes migrations; stewards approve before conversion; original bitstream never deleted |

### 5.4 Web Archives

| Attribute | Specification |
|-----------|---------------|
| **Formats** | WARC, ARC ([07-reference-standards.md](07-reference-standards.md), §12) |
| **Pattern** | Internet Archive temporal versioning — each capture is a versioned preservation object |
| **Provenance** | Capture timestamp, source URI, and crawl run linked in PREMIS event log |

---

## 6. Outputs

### 6.1 Fixity Records

Each fixity verification emits:

- ARK identifier and object version
- SHA-256 digest, algorithm URI, and verification timestamp
- Storage tier and replica locations verified
- Result (`pass`, `fail`, `replica_mismatch`)
- Agent version and verification run identifier

Failed verifications trigger alert workflows per [05-physical-architecture.md](05-physical-architecture.md), §7.1 (alert + restore from replica).

### 6.2 Preservation Events (PREMIS)

Each preservation action extends the provenance chain:

```
Source → Discovery Event → Ingest Event → Preservation Event → …
```

| Event Type | When Emitted |
|------------|--------------|
| `fixity` | Deposit, scheduled verification, post-restore |
| `migration` | Format conversion completed and validated |
| `replication` | Replica sync or new geographic copy confirmed |
| `storage` | Tier transition (T0 ↔ T1 ↔ T2 ↔ T3) |
| `rights` | Rights metadata update affecting preservation posture |

### 6.3 Preserved Object Descriptor (OAIS AIP)

Each stored object emits an AIP descriptor to Knowledge Modeling:

| Field | Requirement |
|-------|-------------|
| **ARK** | Persistent identifier with NAAN registry binding |
| **Fixity** | Current SHA-256 digest and last-verified timestamp |
| **Format** | PRONOM identifier and preservation-format classification |
| **Provenance** | Chain link to ingest event and latest preservation event |
| **Tier** | Current storage tier and replica count |
| **Rights** | Machine-readable rights declaration from ingest package |

### 6.4 Preservation Risk Reports

Periodic and event-driven reports covering:

- Format obsolescence scores by media type and corpus segment
- Migration candidacy queue (ranked, with risk rationale)
- Replica lag, vault integrity status, and fixity-failure counts
- Objects approaching prohibited-format policy ([07-reference-standards.md](07-reference-standards.md), §6.2)

Risk reports are informational. Migration execution and vault restore require steward approval.

---

## 7. AI Fabric Governance

| Gate | Requirement |
|------|-------------|
| **Agent Registry** | Agent version, fixity schedule, migration thresholds, and tier policies registered before production runs |
| **Benchmarks** | Fixity pass rate, mean time to restore, replica consistency, format-risk coverage, migration backlog age |
| **Evaluations** | Periodic review against Phase 3 success criteria |
| **Safety Reviews** | Verify agent does not delete originals, bypass replication minimums, or execute unapproved migrations |
| **Human Approval** | Stewards approve migration execution, vault restores, and tier demotions below policy minimums |

**Council assignment:** Implementation Council (fixity pipelines, PREMIS event schemas) and Execution Council (scheduled verification runs, replica sync). Research Council advises on format obsolescence signals and migration tooling.

---

## 8. Phase Alignment

| Phase | Agent Scope |
|-------|-------------|
| **Ingestion (Phase 2)** | Accept checksum-verified ingest packages; validate BagIt structure; compute deposit fixity; prepare ARK assignment workflow |
| **Preservation (Phase 3)** | Full fixity monitoring (weekly per object); replica consistency checks; PREMIS preservation events; format risk scanning; ingest-to-store pipeline hardened |
| **Knowledge Modeling (Phase 4)** | Emit AIP descriptors on deposit and on preservation-event updates |
| **Quality Platform (Phase 7)** | Feed migration validation results; accept quality signals on migrated object fidelity |

---

## 9. Success Criteria

Aligned with Preservation phase completion criteria ([06-build-roadmap.md](06-build-roadmap.md)):

- Objects retrievable by ARK with current fixity digest
- Weekly SHA-256 fixity checks passing across ≥ 2 geographic replicas
- PREMIS preservation events queryable for every deposited object
- Format obsolescence scan operational with steward-facing migration queue
- End-to-end demonstration: ingest package → agent deposit → fixity verification → AIP descriptor → knowledge modeling candidacy
- Fixity failure alert and restore workflow demonstrated within RTO targets ([05-physical-architecture.md](05-physical-architecture.md), §7.3)

---

## 10. Constraints

- **No canonical writes without approval.** Routine fixity and replication are automated; migrations, restores, and policy exceptions require steward approval.
- **Originals are permanent.** Follow Internet Archive and OAIS practice: migrated copies are additive; source bitstreams are never deleted ([05-physical-architecture.md](05-physical-architecture.md), §7.2).
- **Provenance chain intact.** Every preservation action traces to an ingest event, agent version, and logged PREMIS event ([03-canonical-architecture.md](03-canonical-architecture.md), §6.2).
- **OAIS boundary respect.** Agent performs Archival Storage and contributes to Preservation Planning; Ingest validation remains with Ingestion; access APIs remain with Search and Research Fabric.
- **Experience Plane isolation.** No public-facing component writes directly to preservation storage (ADR-003, [08-decision-record.md](08-decision-record.md)).
