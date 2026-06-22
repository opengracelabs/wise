# Agent Checks Audit — Remediation Report

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Complete |
| **Authority** | Open Grace Architecture Office |
| **Date** | 2026-06-22 |
| **Remediation batch** | P0–P3 (Evidence, Provenance, Compliance normalization) |

---

## Findings Accepted

The Agent Checks Audit findings are **accepted** in full:

1. **Evidence** — inconsistently modeled across assertion-making agents; no shared output profile.
2. **Provenance** — strong overall with terminology drift; Metadata and Education agents lacked **Provenance chain intact** constitutional language; Biodiversity and Climate observatories used anchor-only constraints.
3. **Compliance** — strong at governance agents; Benchmark Agent fleet enumeration was incomplete (Heritage, Tourism, Standards, self-checks missing).
4. **Cross-cutting** — no unified agent-checks registry; duplicate document prefix numbering created registry ambiguity.

---

## Files Changed

| File | Change |
|------|--------|
| [03-canonical-architecture.md](../../architecture/canonical/03-canonical-architecture.md) | Added §6.6 Evidence Output Profile (normative field set) |
| [10-metadata-agent.md](../../architecture/canonical/10-metadata-agent.md) | Evidence profile on Entity Assertions; **Provenance chain intact** constraint |
| [12-knowledge-graph-agent.md](../../architecture/canonical/12-knowledge-graph-agent.md) | Evidence Output Profile on link and relationship proposals |
| [16-education-agent.md](../../architecture/canonical/16-education-agent.md) | **Provenance chain intact** constraint |
| [17-biodiversity-observatory-agent.md](../../architecture/canonical/17-biodiversity-observatory-agent.md) | **Provenance chain intact** (retains taxon anchors); Evidence profile on outputs |
| [18-climate-observatory-agent.md](../../architecture/canonical/18-climate-observatory-agent.md) | **Provenance chain intact** (retains graph anchors and partner attribution); Evidence profile on outputs |
| [19-heritage-observatory-agent.md](../../architecture/canonical/19-heritage-observatory-agent.md) | Evidence profile on Observation Proposals |
| [20-tourism-observatory-agent.md](../../architecture/canonical/20-tourism-observatory-agent.md) | Evidence profile on Observation Proposals |
| [21-language-observatory-agent.md](../../architecture/canonical/21-language-observatory-agent.md) | Evidence profile on Vitality Observations |
| [23-benchmark-agent.md](../../architecture/canonical/23-benchmark-agent.md) | §5.4 Registered Canonical Agent Fleet (all 15 agents); self-checks; Evidence profile compliance check in §5.3 |
| [agent-checks-registry.md](../agent-checks-registry.md) | **Created** — fleet-wide Evidence / Provenance / Compliance / Benchmark matrix |
| [agent-checks-audit-remediation.md](agent-checks-audit-remediation.md) | **Created** — this report |

**Note:** Remediation was applied to current on-disk paths. The audit referenced `19-benchmark-agent.md` and `15-education-agent.md`; the repository had already been partially renumbered to `23-benchmark-agent.md` and `16-education-agent.md` before this patch.

---

## Numbering Conflicts

This patch did **not** renumber files. The following conflicts were identified at audit time and their disposition is recorded here.

### Historical duplicate `15-*` prefixes

| Path (audit era) | Agent | Disposition |
|------------------|-------|-------------|
| `15-education-agent.md` | Education Agent | Renamed to `16-education-agent.md` (pre-remediation) |
| `15-publishing-agent.md` | Publishing Agent | Retains `15-publishing-agent.md` |

**Current state:** No `15-*` collision remains. Publishing remains at prefix `15`; Education at `16`.

### Historical duplicate `16-*` prefixes

| Path (audit era) | Agent | Disposition |
|------------------|-------|-------------|
| `16-biodiversity-observatory-agent.md` | Biodiversity Observatory | Renamed to `17-biodiversity-observatory-agent.md` |
| `16-climate-observatory-agent.md` | Climate Observatory | Renamed to `18-climate-observatory-agent.md` |
| `16-heritage-observatory-agent.md` | Heritage Observatory | Renamed to `19-heritage-observatory-agent.md` |
| `16-tourism-observatory-agent.md` | Tourism Observatory | Renamed to `20-tourism-observatory-agent.md` |

**Current state:** No `16-*` collision remains. Education occupies `16`; observatories occupy `17`–`21`.

### Recommended stable future numbering

Adopt the current contiguous agent-spec sequence as the Agent Registry authority prefix:

| Prefix range | Domain |
|--------------|--------|
| `09`–`14` | Platform agents (Discovery through Translation) |
| `15` | Publishing |
| `16` | Education |
| `17`–`21` | Observatory agents (Biodiversity → Language) |
| `22` | Standards Agent |
| `23` | Benchmark Agent |

Future agents MUST receive the next available prefix (`24+`). Cross-references in [03-canonical-architecture.md](../../architecture/canonical/03-canonical-architecture.md) and [04-system-diagram.md](../../architecture/canonical/04-system-diagram.md) should be updated in a dedicated link-hygiene pass if any stale `16-*` observatory or `18-standards` / `19-benchmark` references remain.

---

## Remaining Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Stale cross-links in docs outside this patch may still reference pre-renumber paths | Medium | Dedicated link-hygiene ADR or doc sweep |
| Quality Review and Standards Agent both check provenance completeness — potential duplicate validation | Low | Document validator ownership in Implementation Council runbooks |
| Evidence Output Profile not yet required on non-assertion agents (Preservation fixity records use PREMIS natively) | Low | Acceptable; PREMIS is the evidence contract for preservation |
| Agent Registry implementation may lag spec enumeration | Medium | Register all §5.4 agents before first production Benchmark run |
| Benchmark Agent Evidence profile check is schema-level only until validators ship | Medium | Implementation Council to add SHACL/JSON Schema profile for §6.6 |

---

## Follow-Up Actions

| Priority | Action | Owner |
|----------|--------|-------|
| P1 | Link-hygiene pass on `03-canonical-architecture.md`, `04-system-diagram.md`, `06-build-roadmap.md`, `07-reference-standards.md` for renumbered agent paths | Architecture Office |
| P1 | Register all 15 agents in Agent Registry with benchmark suites per §5.4 | Implementation Council |
| P2 | Ship JSON Schema / SHACL shape for Evidence Output Profile §6.6 | Implementation Council |
| P2 | Deduplicate provenance validation between Quality Review Agent §5.1 and Standards Agent §5.1 | Architecture Council |
| P3 | Consider elevating Evidence sufficiency to a fourth Benchmark evaluation sub-domain | Architecture Office (ADR if adopted) |

---

## Outcome

Evidence, Provenance, and Compliance checks are **normalized** across the canonical agent suite without expanding the logical architecture. Assertion-making agents share a single Evidence Output Profile; provenance constitutional language is aligned; the Benchmark Agent enumerates the full fleet including self-checks; governance registries provide a single audit index.

---

*Registry: [agent-checks-registry.md](../agent-checks-registry.md) · Fleet: [23-benchmark-agent.md](../../architecture/canonical/23-benchmark-agent.md) §5.4*
