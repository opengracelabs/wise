# Tourism Observatory Agent

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Canonical |
| **Authority** | Open Grace Architecture Office |
| **Date** | 2026-06-22 |
| **Capability** | Observatories — Tourism domain ([03-canonical-architecture.md](03-canonical-architecture.md), §5.5) |
| **Phase** | Observatories ([06-build-roadmap.md](06-build-roadmap.md), Phase 15) |

## Document Map

| Document | Purpose |
|----------|---------|
| [01-mission-and-constitutional-charter.md](01-mission-and-constitutional-charter.md) | Mission, charter, and constitutional relationship |
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
| [15-publishing-agent.md](15-publishing-agent.md) | Publishing Agent specification |
| [16-education-agent.md](16-education-agent.md) | Education Agent specification |
| [17-biodiversity-observatory-agent.md](17-biodiversity-observatory-agent.md) | Biodiversity Observatory Agent specification |
| [18-climate-observatory-agent.md](18-climate-observatory-agent.md) | Climate Observatory Agent specification |
| [19-heritage-observatory-agent.md](19-heritage-observatory-agent.md) | Heritage Observatory Agent specification |
| [20-tourism-observatory-agent.md](20-tourism-observatory-agent.md) | Tourism Observatory Agent specification |
| [21-language-observatory-agent.md](21-language-observatory-agent.md) | Language Observatory Agent specification |
| [22-standards-agent.md](22-standards-agent.md) | Standards Agent specification |
| [23-benchmark-agent.md](23-benchmark-agent.md) | Benchmark Agent specification |

---

## 1. Purpose

The **Tourism Observatory Agent** automates the **Tourism** observatory within the Observatory Network ([03-canonical-architecture.md](03-canonical-architecture.md), §5.5). It ingests partner feeds and field observations; normalizes visitor-flow and sustainability metrics at heritage and natural sites; detects trend anomalies and threshold breaches; and emits **Observatory Observation Proposals** (JSON-LD / GeoJSON time series) for steward approval before longitudinal records enter the canonical observatory catalog, Knowledge Graph, and public dashboards.

The agent does not publish unverified impact claims, expose personally identifiable visitor data, or override site-management authority. It monitors, correlates, and proposes; site stewards and researchers approve.

---

## 2. Responsibilities

The agent operates two coordinated **tracks**. Each track has distinct inputs, processing patterns, and outputs; both tracks share graph anchoring, provenance, privacy gates, and AI Fabric governance.

| Track | Responsibility | Description |
|-------|----------------|-------------|
| **Visitor patterns** | Monitor visitor flow and congestion | Ingest and normalize arrivals, dwell time, seasonality, origin markets, modality, and carrying-capacity proxies at World Heritage sites, protected areas, and partner destinations; align observations to canonical place and site entities; detect overtourism, undertourism, and congestion anomalies against baselines and seasonal models |
| **Sustainability indicators** | Track SDG-aligned impact metrics | Monitor environmental load, waste and water indicators, local economic benefit proxies, and sustainable-tourism compliance signals; map indicators to SDG and institutional reporting frameworks; correlate with heritage condition and biodiversity observatory layers; surface threshold breaches and longitudinal trend shifts for steward review |

---

## 3. Reference Models

The agent synthesizes patterns from three primary reference models ([02-reference-models.md](02-reference-models.md)):

| Model | Pattern Applied | Agent Behavior |
|-------|-----------------|----------------|
| **UNESCO** | World Heritage site monitoring, sustainable tourism frameworks, state-of-conservation reporting, site-boundary authority | Bind all observations to UNESCO site identifiers and CRM place entities; apply World Heritage monitoring vocabulary for threat and impact correlation; route high-significance site alerts to heritage steward queues |
| **National Geographic** | Place-based storytelling, conservation geography, longitudinal environmental observation | Frame dashboard narratives from verified trend data; correlate visitor patterns with ecosystem and heritage observatory layers; preserve field-provenance for partner-supplied observations |
| **GBIF** | Occurrence and biodiversity trend interoperability | Cross-reference visitor-pressure anomalies with species-occurrence and ecosystem-health observatory feeds; emit correlation proposals when tourism patterns align with biodiversity stress signals |

Supporting standards alignment follows [07-reference-standards.md](07-reference-standards.md): GeoJSON, WGS 84, Dublin Core, PREMIS (observation provenance), SKOS (indicator vocabularies), SDG indicator URIs.

---

## 4. Position in Architecture

```
Partner feeds + field sensors + steward submissions + mobility aggregates (privacy-safe)
        ↓
Ingestion (observatory channel) + Knowledge Graph place/site anchors
        ↓
Tourism Observatory Agent
  ├── Track: Visitor patterns
  └── Track: Sustainability indicators
        ↓
Observatory Observation Proposals (JSON-LD / GeoJSON) — candidate, pending steward approval
        ↓
Approved observatory time series written to Observatory catalog
        ↓
Knowledge Graph (site–indicator relationships) · Research Registry packages · Public dashboards · Tourism Portal
```

The agent operates in the **Observatories** subgraph of the Experience Plane ([04-system-diagram.md](04-system-diagram.md), §2). All outputs pass through the AI Fabric governance chain before affecting canonical systems ([04-system-diagram.md](04-system-diagram.md), §2.2).

**Upstream inputs:** Knowledge Graph place and heritage-site entities ([12-knowledge-graph-agent.md](12-knowledge-graph-agent.md)), observatory feeds via Ingestion, Research Fabric datasets, quality and rights clearance signals from the Quality Review Agent ([13-quality-review-agent.md](13-quality-review-agent.md)).

**Downstream consumers:** Observatory Network dashboards, Tourism Portal, Conservation Portal, Research Fabric (citable data packages), Public Experience (trend visualizations), Education Agent (classroom-safe observatory excerpts where cleared, [16-education-agent.md](16-education-agent.md)).

**Peer observatories:** Heritage Observatory Agent (tourism-pressure threat correlation, [19-heritage-observatory-agent.md](19-heritage-observatory-agent.md)), Biodiversity Observatory Agent (ecosystem stress correlation, [17-biodiversity-observatory-agent.md](17-biodiversity-observatory-agent.md)), Climate Observatory Agent (environmental load correlation, [18-climate-observatory-agent.md](18-climate-observatory-agent.md)).

---

## 5. Observation Domains

### 5.1 Visitor Patterns

| Attribute | Specification |
|-----------|---------------|
| **Sources** | Partner destination-management feeds, ticket and gate counts, anonymized mobility aggregates, on-site sensor counts, steward field observations, scheduled event calendars, weather and accessibility overlays |
| **Processing pattern** | Feed validation → place/site entity binding → temporal aggregation (hourly, daily, seasonal) → baseline comparison → anomaly scoring → proposal emission |
| **Output entities** | Visitor-flow time series, seasonality profiles, origin-market distributions (aggregated), carrying-capacity utilization scores, congestion and dispersal alerts |
| **Standards** | GeoJSON feature collections with `dcterms:temporal` bounds; WGS 84 coordinates; SKOS indicator concepts; privacy-safe aggregation thresholds ([07-reference-standards.md](07-reference-standards.md)) |

### 5.2 Sustainability Indicators

| Attribute | Specification |
|-----------|---------------|
| **Sources** | SDG-aligned partner reports, environmental sensor networks, waste and water utility feeds (where licensed), local economic proxies, heritage condition observatory inputs, biodiversity stress signals from GBIF-linked observatories |
| **Processing pattern** | Indicator vocabulary mapping → unit normalization → SDG and institutional framework alignment → cross-domain correlation with visitor patterns → threshold evaluation → proposal emission |
| **Output entities** | Sustainability indicator time series, SDG mapping records, impact-correlation assertions, compliance and threshold-breach alerts |
| **Standards** | UN SDG indicator URIs; institutional extension properties for site-specific KPIs; PREMIS-aligned provenance for each observation event ([07-reference-standards.md](07-reference-standards.md)) |

### 5.3 Cross-Domain Correlation

| Attribute | Specification |
|-----------|---------------|
| **Sources** | Approved visitor-pattern series, approved sustainability series, heritage condition observatory feeds, biodiversity occurrence trends |
| **Processing pattern** | Temporal alignment → correlation analysis → significance scoring → correlation proposal emission with graph relationship candidates |
| **Output entities** | Cross-observatory correlation records linking tourism pressure to heritage threat or biodiversity anomaly signals |
| **Standards** | RDF correlation assertions with confidence tier; `prov:wasDerivedFrom` links to all contributing series |

### 5.4 Privacy and Aggregation

| Attribute | Specification |
|-----------|---------------|
| **Sources** | All visitor-pattern inputs carrying mobility or demographic dimensions |
| **Processing pattern** | k-anonymity threshold enforcement → aggregation to site or corridor level → PII strip and audit → block emission when thresholds fail |
| **Output entities** | Privacy-safe aggregates only; blocked-series audit events routed to compliance stewards |
| **Standards** | Institutional privacy policy; minimum aggregation cell sizes registered in Agent Registry |

---

## 6. Indicator Framework Integration

The agent maintains indicator registries; site stewards approve canonical mappings and alert thresholds.

### 6.1 Framework Scope

| Framework | Alignment Use |
|-----------|---------------|
| **UN SDGs** | SDG 8 (sustainable tourism), SDG 11 (sustainable cities and communities), SDG 12 (responsible consumption), SDG 13 (climate action), SDG 14–15 (life below water / on land) |
| **UNESCO sustainable tourism** | Carrying capacity, visitor management, heritage impact, community benefit |
| **Institutional reporting** | Open Grace stewardship KPIs: overtourism risk, undertourism equity, provenance-complete observatory packages |
| **Partner covenants** | Site-specific indicator sets and publication restrictions per covenant terms |

### 6.2 Indicator Record Output

Each sustainability indicator mapping includes:

| Field | Requirement |
|-------|-------------|
| **Indicator URI** | Stable identifier for the approved or proposed indicator series |
| **Framework code** | SDG, UNESCO, or institutional KPI identifier |
| **Graph anchors** | Canonical place, heritage-site, and ecosystem entity URIs |
| **Unit and methodology** | Normalized unit, aggregation window, and calculation provenance |
| **Confidence tier** | `machine-suggested`, `steward-reviewed`, or `researcher-approved` |
| **Threshold profile** | Alert levels, seasonal baselines, and reviewer attribution when applicable |

Machine-suggested mappings route to site stewards; the agent does not assert researcher-approved indicator bindings without human approval.

---

## 7. Outputs

### 7.1 Observatory Observation Proposals

Each candidate observation or series is emitted as an **Observatory Observation Proposal** with:

| Field | Requirement |
|-------|-------------|
| **Observation type** | `visitor-pattern` or `sustainability-indicator` |
| **Site anchor** | Canonical heritage-site or place entity URI with GeoJSON geometry |
| **Temporal extent** | `dcterms:temporal` start/end; aggregation granularity |
| **Metric values** | Normalized numeric series or snapshot with unit and methodology |
| **Source provenance** | Partner feed URI, sensor ID, steward submission reference; `prov:wasDerivedFrom` |
| **Evidence profile** | [Evidence Output Profile](03-canonical-architecture.md#66-evidence-output-profile): `evidenceURIs[]`, `confidence`, `evidenceSummary`, `method`, `sourceRegistryRefs[]`, `provenanceEventId` |
| **Privacy posture** | Aggregation level, k-anonymity attestation, PII handling declaration |
| **Framework alignment** | SDG or institutional KPI codes when applicable |
| **Anomaly signals** | Deviation scores, threshold breaches, recommended steward actions |
| **Review requirement** | Auto-approvable (pre-registered low-risk feeds), standard steward review, or researcher/sensitivity queue |

Observatory Observation Proposals are **candidates** until a site steward or researcher approves them through the human-approval gate.

### 7.2 Trend and Alert Reports

Each processing run emits reports containing:

- Sites monitored vs. targeted in the observatory registry
- Visitor-pattern anomaly count by severity and season
- Sustainability indicator threshold breaches by framework code
- Cross-domain correlations proposed (tourism pressure ↔ heritage/biodiversity signals)
- Feed health: latency, gap detection, and partner connector status
- Privacy gate outcomes: aggregates published vs. blocked

### 7.3 Research Registry Packages

Approved longitudinal series are packaged for Research Fabric release with:

- Citation metadata and DOI candidacy fields
- Methodology appendix and indicator definitions
- Provenance chain from raw feed to approved aggregate
- Rights and partner redistribution terms

---

## 8. AI Fabric Governance

| Gate | Requirement |
|------|-------------|
| **Agent Registry** | Agent version, partner connector scope, indicator vocabularies, privacy aggregation thresholds, and auto-approval profiles registered before production runs |
| **Benchmarks** | Entity-binding accuracy (human spot-check), privacy-gate pass rate, anomaly precision/recall against steward-validated incidents, feed freshness SLA |
| **Evaluations** | Periodic review against Phase 15 Observatories success criteria |
| **Safety Reviews** | Verify agent does not emit PII, fabricate impact claims without source provenance, or bypass partner covenant publication restrictions |
| **Human Approval** | Site stewards and researchers approve Observatory Observation Proposals before canonical observatory catalog writes; high-significance World Heritage alerts always require steward review |

**Council assignment:** Research Council (indicator methodology, cross-domain correlation), Implementation Council (feed connectors, time-series pipelines), Architecture Council (observatory data model alignment). Community Council advises on indigenous and local-community tourism impact framing.

---

## 9. Phase Alignment

| Phase | Agent Scope |
|-------|-------------|
| **Knowledge Graph (Phase 5)** | Readiness only: place and heritage-site entity coverage for observatory binding |
| **Research Fabric (Phase 8)** | Research Registry packaging templates; dataset clearance integration |
| **Public Experience (Phase 11)** | Tourism Portal trend visualization hooks; alert surfacing patterns |
| **Observatories (Phase 15)** | Full visitor-pattern ingestion; sustainability indicator tracking; anomaly detection; steward review queues; observatory catalog writes (approved only) |
| **Community (Phase 14)** | Steward and citizen-science observation submissions routed through ingestion and tourism observatory processing |

---

## 10. Success Criteria

Aligned with Observatories phase completion criteria ([06-build-roadmap.md](06-build-roadmap.md), Phase 15):

- Tourism observatory operational at ≥ 10 World Heritage or protected-area sites with baseline visitor-pattern data
- Sustainability indicators tracked and SDG-mapped for ≥ 5 sites with steward-approved methodology
- Real-time or near-real-time ingestion from ≥ 3 partner feeds with documented provenance
- Public and researcher dashboards display approved trend visualizations with alert thresholds
- Zero PII leakage in published aggregates; 100% of mobility-derived series pass privacy gates
- ≥ 1 approved cross-domain correlation demonstrated (visitor pressure ↔ heritage or biodiversity signal)
- Observatory data packages published in Research Registry with citation metadata
- End-to-end demonstration: partner feed → observation proposal → steward approval → graph placement → dashboard alert → research package with provenance trace

---

## 11. Constraints

- **No canonical writes without approval.** The agent proposes; site stewards and researchers approve.
- **Privacy before publication.** Visitor data is aggregated; raw mobility traces and identifiable demographics never enter the public observatory catalog.
- **Provenance mandatory.** Every metric links to source feed, sensor, or steward submission with PREMIS-aligned audit events ([03-canonical-architecture.md](03-canonical-architecture.md), Provenance).
- **Site authority respected.** UNESCO and partner site-management decisions override machine-generated recommendations on carrying capacity and access policy.
- **Covenant compliance.** Partner withholding and redistribution restrictions block publication regardless of data quality ([08-decision-record.md](08-decision-record.md)).
- **Cross-observatory integrity.** Correlation proposals require approved inputs from contributing observatory layers; the agent does not infer causation without steward or researcher validation. Tourism pressure supplements but does not replace Heritage conservation status assessments ([19-heritage-observatory-agent.md](19-heritage-observatory-agent.md)) or Biodiversity threatened-taxa signals ([17-biodiversity-observatory-agent.md](17-biodiversity-observatory-agent.md)).
- **Free access preserved.** Public dashboards expose approved aggregates without gating underlying canonical place and site memory ([01-mission-and-constitutional-charter.md](01-mission-and-constitutional-charter.md)).

---

*Previous: [16-education-agent.md](16-education-agent.md) · Observatory peers: [19-heritage-observatory-agent.md](19-heritage-observatory-agent.md), [17-biodiversity-observatory-agent.md](17-biodiversity-observatory-agent.md), [18-climate-observatory-agent.md](18-climate-observatory-agent.md)*
