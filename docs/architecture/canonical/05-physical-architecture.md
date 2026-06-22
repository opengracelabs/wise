# Physical Architecture

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Canonical |
| **Authority** | Open Grace Architecture Office |
| **Date** | 2026-06-22 |

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
| [12-knowledge-graph-agent.md](12-knowledge-graph-agent.md) | Knowledge Graph Agent specification |
| [11-preservation-agent.md](11-preservation-agent.md) | Preservation Agent specification |

---

## 1. Purpose

This document defines the **physical architecture** — where digital objects live, how they are replicated, and how geographic distribution supports the 100-year durability mandate described in [01-mission.md](01-mission.md) and [03-canonical-architecture.md](03-canonical-architecture.md).

The physical deployment diagram is in [04-system-diagram.md](04-system-diagram.md), Section 7.

---

## 2. Physical Architecture Principles

| Principle | Rationale |
|-----------|-----------|
| **No single point of failure** | Geographic, vendor, and media redundancy |
| **Tiered storage economics** | Active content on fast media; archives on economical media |
| **Sovereignty respect** | Data residency options for partner nations and institutions |
| **Offline survivability** | Deep archive copies readable without network or vendor |
| **Provable integrity** | Checksums, fixity monitoring, and replication proofs |
| **Energy proportionality** | Storage tier matches access frequency |

Reference models: Harvard (tiered preservation), Internet Archive (offline vaults), Google (global distribution) — see [02-reference-models.md](02-reference-models.md).

---

## 3. Storage Tiers

### 3.1 Tier Overview

| Tier | Name | Access Latency | Use Case | Retention |
|------|------|---------------|----------|-----------|
| **T0** | Hot | Milliseconds | Public Experience, Search, active APIs | Active objects |
| **T1** | Warm | Seconds–minutes | Research Fabric, Publishing, batch processing | Recently accessed |
| **T2** | Cold | Minutes–hours | Archival retrieval, migration source | Long-term archive |
| **T3** | Deep | Days (manual) | Offline vault, disaster recovery, format migration source | Permanent |

### 3.2 Tier Transitions

```
Ingest → T0 (Hot) ──[30 days no access]──▶ T1 (Warm)
              │
              └──[curatorial designation]──▶ T2 (Cold)
                                              │
                                              └──[annual migration]──▶ T3 (Deep)
```

Transitions are automated with curatorial override. All transitions are logged in the provenance chain ([03-canonical-architecture.md](03-canonical-architecture.md), Section 6.2).

### 3.3 Storage Technology Requirements

| Tier | Minimum Requirements |
|------|---------------------|
| T0 Hot | SSD/NVMe, erasure-coded, sub-10ms read |
| T1 Warm | Object storage, erasure-coded, lifecycle policies |
| T2 Cold | Object storage or tape library, immutable snapshots |
| T3 Deep | LTO tape or optical archive, air-gapped, geographic vault |

Formats stored at every tier must comply with [07-reference-standards.md](07-reference-standards.md).

---

## 4. Geographic Architecture

### 4.1 Region Model

The physical architecture deploys across **three minimum geographic zones**:

| Zone | Role | Contents |
|------|------|----------|
| **Zone Alpha** | Primary operations | Hot storage, compute, graph database, search indexes |
| **Zone Beta** | Synchronous replica | Warm storage, read replicas, failover compute |
| **Zone Gamma** | Archival vault | Cold storage, deep archive, air-gapped copies |

### 4.2 Geographic Separation Requirements

- Zones must be separated by **≥ 500 km** to survive regional disasters
- Zones should span **≥ 2 continents** where politically feasible
- Deep archive (T3) must exist in **≥ 2 independent vault locations**

### 4.3 Zone Diagram

```
                    ┌─────────────────────────────────┐
                    │         GLOBAL CDN / EDGE          │
                    │   (Public Experience delivery)   │
                    └───────────────┬─────────────────┘
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          │                         │                         │
          ▼                         ▼                         ▼
   ┌─────────────┐          ┌─────────────┐          ┌─────────────┐
   │ ZONE ALPHA  │◄────────►│ ZONE BETA   │          │ ZONE GAMMA  │
   │  (Primary)  │  sync    │ (Replica)   │──archive►│  (Vault)    │
   │             │          │             │          │             │
   │ T0 Hot      │          │ T1 Warm     │          │ T2 Cold     │
   │ Compute     │          │ Read Replica│          │ T3 Deep     │
   │ Graph DB    │          │ Failover    │          │ Air-gap     │
   └─────────────┘          └─────────────┘          └─────────────┘
```

### 4.4 Data Residency

Partner institutions and contributing nations may require data sovereignty guarantees:

- **Residency tags** on objects determine permissible storage zones
- Objects tagged `sovereign:{nation}` are stored only in approved zones
- Metadata indexes may be global; bitstreams respect residency constraints
- Covenant framework governs residency agreements ([01-mission.md](01-mission.md))

---

## 5. Compute Architecture

### 5.1 Workload Classes

| Class | Workloads | Deployment |
|-------|-----------|------------|
| **Interactive** | Public Experience, Search API | Zone Alpha + CDN edge |
| **Batch** | Ingestion, migration, indexing | Zone Alpha, burst to Beta |
| **Analytical** | Research Fabric queries, observatory processing | Zone Alpha/Beta |
| **Graph** | Knowledge Graph queries (SPARQL/GraphQL) | Zone Alpha primary, Beta replica |
| **ML** | Translation, visual similarity, quality scoring | Zone Alpha GPU pool |

### 5.2 Compute Requirements

- Stateless application tiers for horizontal scaling
- Graph database with synchronous replication to Zone Beta
- Search index replicas in Alpha and Beta
- GPU availability for Translation Fabric and visual search

---

## 6. Network Architecture

### 6.1 Traffic Classes

| Class | Path | Requirements |
|-------|------|-------------|
| **Public** | CDN → Public Experience | DDoS protection, TLS 1.3, global PoPs |
| **Partner** | VPN/secure API → Ingestion | Mutual TLS, rate limiting, audit logging |
| **Internal** | Zone Alpha ↔ Beta ↔ Gamma | Private backbone, encrypted transit |
| **Research** | API gateway → Research Fabric | Authenticated, quota-managed, logged |
| **Vault** | Gamma air-gap | Sneakernet or one-way diode for T3 writes |

### 6.2 Bandwidth Planning

| Flow | Estimated Scale (Year 10) |
|------|--------------------------|
| Public Experience egress | Multi-Pb/month via CDN |
| Partner ingestion ingress | 10–100 Tb/month |
| Inter-zone replication | Continuous, proportional to ingest rate |
| Research bulk export | Burst to 10 Gbps |

---

## 7. Preservation Infrastructure

### 7.1 Fixity Monitoring

All preserved objects undergo continuous fixity verification:

| Check | Frequency | Action on Failure |
|-------|-----------|-------------------|
| Checksum verification (SHA-256) | Weekly per object | Alert + restore from replica |
| Replica consistency | Daily per tier | Re-sync from authoritative copy |
| Format viability assessment | Annual | Queue for migration ([07-reference-standards.md](07-reference-standards.md)) |
| Vault integrity (T3) | Annual physical audit | Restore from alternate vault |

### 7.2 Format Migration Pipeline

Physical infrastructure for format migration:

1. **Source** — Object retrieved from T2 or T3
2. **Emulation/Conversion** — Compute pool in Zone Alpha
3. **Validation** — Quality Platform verifies migrated object
4. **Deposit** — New version ingested to T0 with provenance link to original
5. **Archive** — Original retained in T3 permanently

### 7.3 Backup and Recovery

| Scenario | RTO | RPO | Recovery Source |
|----------|-----|-----|-----------------|
| Zone Alpha failure | 4 hours | 0 (sync replica) | Zone Beta promotion |
| Zone Alpha + Beta failure | 72 hours | 24 hours | Zone Gamma cold restore |
| Catastrophic multi-zone loss | 30 days | 0 for T3 | Deep vault sneakernet recovery |
| Ransomware / corruption | 4 hours | Last fixity-good snapshot | Immutable cold copies |

---

## 8. Observability Infrastructure

Non-public infrastructure supporting operations:

| Component | Function | Retention |
|-----------|----------|-----------|
| Metrics | Capacity, latency, error rates | 2 years hot, 10 years cold |
| Logs | Audit trail, access logs, provenance events | 7 years minimum |
| Traces | Request flow across platform layers | 90 days |
| Alerts | Fixity failures, capacity thresholds, security events | Real-time |

Observability data is subject to Open Grace stewardship policy. It is not part of the public canonical memory.

---

## 9. Security Architecture

### 9.1 Security Zones

```
┌─────────────────────────────────────────────────────────────┐
│  PUBLIC ZONE — CDN, Public Experience (read-only, no PII)   │
├─────────────────────────────────────────────────────────────┤
│  APPLICATION ZONE — Platform APIs (authenticated writes)    │
├─────────────────────────────────────────────────────────────┤
│  DATA ZONE — Storage, Graph DB (no direct external access)  │
├─────────────────────────────────────────────────────────────┤
│  VAULT ZONE — T3 Deep Archive (air-gapped, manual access)   │
├─────────────────────────────────────────────────────────────┤
│  GOVERNANCE ZONE — Open Grace tools (restricted, audited)   │
└─────────────────────────────────────────────────────────────┘
```

### 9.2 Key Management

- Hardware security modules (HSM) in Zone Alpha and Beta
- Key ceremony for vault access documented and witnessed
- Annual key rotation for application-tier encryption
- Separate key domains for public, partner, and vault zones

---

## 10. Environmental and Sustainability

100-year architecture requires sustainable operations:

| Measure | Target |
|---------|--------|
| PUE (Power Usage Effectiveness) | ≤ 1.3 for new data centers |
| Renewable energy | ≥ 80% for Zone Alpha/Beta by Year 5 |
| Storage efficiency | Lifecycle tiering reduces hot storage footprint ≥ 60% |
| Carbon reporting | Annual public sustainability report |

---

## 11. Physical Build Phases

Physical infrastructure aligns with [06-build-roadmap.md](06-build-roadmap.md):

| Phase | Physical Milestone |
|-------|-------------------|
| Preservation (Phase 3) | Zone Alpha T0/T1 operational, single-region |
| Knowledge Graph (Phase 5) | Graph database cluster deployed |
| Search (Phase 6) | Search index infrastructure, CDN for public |
| Public Experience (Phase 11) | Global CDN, multi-region Alpha/Beta |
| Observatories (Phase 15) | Real-time ingestion pipeline, edge collectors |
| Year 10 | Zone Gamma vault operational, T3 deep archive |
| Year 30 | Fourth zone for sovereignty partners if required |

---

## 12. Vendor and Technology Independence

Physical architecture must not create single-vendor lock-in:

- Storage APIs abstracted behind internal object store interface
- Graph database portable via standard RDF export
- Compute workloads containerized
- T3 deep archive uses industry-standard media (LTO tape, M-DISC optical)
- Annual vendor dependency review by Architecture Office

---

## 13. Physical Architecture Authority

Changes to zone topology, tier definitions, or recovery objectives require an ADR in [08-decision-record.md](08-decision-record.md).

---

*Previous: [04-system-diagram.md](04-system-diagram.md) · Next: [06-build-roadmap.md](06-build-roadmap.md)*
