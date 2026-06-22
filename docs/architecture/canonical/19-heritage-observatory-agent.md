# Heritage Observatory Agent

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Canonical |
| **Authority** | Open Grace Architecture Office |
| **Date** | 2026-06-22 |
| **Capability** | Observatories — Heritage domain ([03-canonical-architecture.md](03-canonical-architecture.md), §5.5) |
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
| [25-research-agent.md](25-research-agent.md) | Research Agent specification |

---

## 1. Purpose

The **Heritage Observatory Agent** automates the **Heritage** observatory within the Observatory Network ([03-canonical-architecture.md](03-canonical-architecture.md), §5.5). It **observes** UNESCO-aligned reference data and partner feeds; **assesses** World Heritage site condition, threats, and conservation status against registered baselines; and **proposes** **Observatory Observation Proposals** (JSON-LD / GeoJSON) for steward approval before observations enter canonical observatory stores, public dashboards, or Research Fabric export workflows.

The agent does not replace state-party reporting authority, write canonical Knowledge Graph assertions, bypass steward approval, or publish observatory outputs to the public experience, Research Registry, or dashboards. It monitors, correlates, and surfaces heritage condition intelligence grounded in registered sources and graph-linked site entities; observatory stewards and heritage curators approve disposition.

**Governing authority:** [ADR-011 Architecture Freeze v1.0](08-decision-record.md#adr-011-architecture-freeze-v10), Observatories ([03-canonical-architecture.md](03-canonical-architecture.md), §5.5), Evidence Output Profile ([03-canonical-architecture.md](03-canonical-architecture.md), §6.6), AI Fabric governance chain ([04-system-diagram.md](04-system-diagram.md), §2.2).

---

## 2. Responsibilities

The agent operates three coordinated **tracks**. Each track has distinct inputs, processing patterns, and outputs; all tracks share graph anchoring, provenance, Evidence Output Profile compliance, and AI Fabric governance.

| Track | Responsibility | Description |
|-------|----------------|-------------|
| **World Heritage** | Maintain site registry and identity | Align UNESCO World Heritage List entries, boundaries, and state-party affiliations with Knowledge Graph place entities; establish baseline site profiles for all monitored locations |
| **Threats** | Monitor and classify threat signals | Ingest, classify, and time-stamp threat observations using the canonical Threat Classification Vocabulary (§6.2); correlate multi-source signals; emit threshold-based alert proposals when escalation rules match |
| **Conservation status** | Record condition and trends | Capture periodic condition assessments using the Heritage Condition Scale (§6.3); maintain longitudinal status time series per site; support dashboards comparing current status to baseline and prior reporting cycles |

---

## 3. Reference Models

The agent synthesizes patterns from UNESCO and its advisory bodies, plus open longitudinal-data practice:

| Model | Pattern Applied | Agent Behavior |
|-------|-----------------|----------------|
| **UNESCO** | World Heritage framework, state-party cooperation, State of Conservation reporting, outstanding universal value, in-danger listing | Sync World Heritage site reference data; map SOC threat and status vocabularies to institutional extensions; respect state-party as authoritative reporter; align multilingual site metadata |
| **ICOMOS** | World Heritage evaluation practice, heritage-at-risk framing, authenticity and integrity assessment, conservation charters | Apply ICOMOS-aligned condition and threat terminology where published guidance exists; route high-significance authenticity and integrity assessments through heritage curator queues; treat ICOMOS advisory outputs as evidence sources, not automatic canonical truth |
| **ICCROM** | Conservation methodology, risk preparedness, capacity-building frameworks, preventive conservation | Ingest ICCROM-published guidance and training-derived assessment patterns as methodological references; align preventive-conservation and risk-preparedness indicators with steward-approved profiles; never substitute ICCROM methodology for state-party SOC authority |
| **National Geographic** | Field documentation, geospatial storytelling, longitudinal place monitoring | Integrate partner field assessments and georeferenced observations; support researcher dashboard narratives with provenance-linked evidence |
| **GBIF** (patterns) | Federated observation ingest, Darwin Core event records, open longitudinal datasets | Model heritage observations as time-stamped, georeferenced events with standardized fields; supply cleared datasets to Research Fabric export workflows after steward approval |

Supporting standards alignment follows [07-reference-standards.md](07-reference-standards.md): GeoJSON, ISO 19115, EML, SKOS (threat and condition vocabularies), CIDOC-CRM place and event bindings, PREMIS for observatory dataset provenance.

---

## 4. Position in Architecture

```
UNESCO reference data + ICOMOS/ICCROM published guidance + partner feeds + field sensors + steward assessments
        ↓
Source Registry + Knowledge Graph site entities (read-only anchors from Source Discovery, Metadata, Graph agents)
        ↓
Heritage Observatory Agent
  ├── Track: World Heritage
  ├── Track: Threats
  └── Track: Conservation status
        ↓
Observatory Observation Proposals — candidate, pending steward approval
        ↓
Steward approval → Quality Review (publication readiness) → approved observatory catalog
        ↓
Research Agent (dataset review) → Research Fabric packages · Public Experience dashboards · Education (cleared datasets)
```

The agent operates in the **Experience Plane** Observatory Network — Heritage subgraph ([04-system-diagram.md](04-system-diagram.md), §2). All outputs pass through the AI Fabric governance chain before affecting canonical systems ([04-system-diagram.md](04-system-diagram.md), §2.2).

**Upstream inputs:** World Heritage site reference data from the Source Discovery Agent ([09-source-discovery-agent.md](09-source-discovery-agent.md)); modeled place and site entities from Knowledge Modeling and the Knowledge Graph Agent ([12-knowledge-graph-agent.md](12-knowledge-graph-agent.md)) — **read-only**; ingested observation packages from partner feeds and field collectors; quality and rights clearance signals from the Quality Review Agent ([13-quality-review-agent.md](13-quality-review-agent.md)).

**Downstream consumers (approved outputs only):** Public Experience (heritage condition dashboards), Research Fabric (observatory dataset exports reviewed by the Research Agent, [25-research-agent.md](25-research-agent.md)), Education Agent (classroom-cleared observatory datasets, [16-education-agent.md](16-education-agent.md)), Digital Twin conservation intelligence layer.

**Peer observatories (inputs and correlation only; no scope duplication):**

| Observatory | Relationship |
|-------------|--------------|
| [Climate Observatory Agent](18-climate-observatory-agent.md) | Supplies climate-exposure and heritage-risk context; does not replace Heritage conservation status assessments |
| [Tourism Observatory Agent](20-tourism-observatory-agent.md) | Supplies visitor-pressure and sustainability indicators; correlates with threat signals; does not assert site condition |
| [Biodiversity Observatory Agent](17-biodiversity-observatory-agent.md) | Supplies ecological threat and threatened-taxa signals at natural and mixed sites; does not assess cultural heritage condition |

---

## 5. Agent Boundary Clarification

Explicit separation of responsibilities across assertion-making and observatory agents. Architecture v1.0 is frozen per [ADR-011](08-decision-record.md#adr-011-architecture-freeze-v10); boundaries below clarify scope within the frozen observatory set — they do not add layers, observatories, or governance structures.

### 5.1 Heritage Observatory Agent

| Verb | Scope |
|------|-------|
| **Observes** | Ingests UNESCO, ICOMOS, ICCROM, and partner feeds; monitors World Heritage site identity, threats, and conservation status over time |
| **Assesses** | Classifies threats (§6.2), rates condition (§6.3), scores confidence, and correlates multi-source signals against baselines |
| **Proposes** | Emits Observatory Observation Proposals and alert proposals with complete Evidence Output Profile (§7.2) for steward review |

### 5.2 Sibling Agents

| Agent | Scope |
|-------|-------|
| [Knowledge Graph Agent](12-knowledge-graph-agent.md) | **Models relationships** — proposes entity links, relationship assertions, and merge candidates; curators approve canonical graph writes |
| [Research Agent](25-research-agent.md) | **Evaluates scholarship** — literature review, dataset review, FAIR and citation readiness for Research Fabric packages; does not emit observatory observations |
| [Quality Review Agent](13-quality-review-agent.md) | **Validates publication readiness** — metadata, rights, accessibility, and completeness gates before approved observatory outputs reach public dashboards or Research Registry |
| [Climate Observatory Agent](18-climate-observatory-agent.md) | Climate impacts, protected-area exposure, heritage-risk scoring — supplies exposure context only |
| [Tourism Observatory Agent](20-tourism-observatory-agent.md) | Visitor patterns and sustainability indicators — supplies pressure context only |
| [Biodiversity Observatory Agent](17-biodiversity-observatory-agent.md) | Species, occurrence, and threatened-taxa tracking — supplies ecological context at applicable sites |

### 5.3 Prohibited Actions

The Heritage Observatory Agent **must not**:

- **Write canonical graph assertions** — no Entity Assertions, RDF triples, `sameAs` links, or relationship placements; graph updates remain the Knowledge Graph Agent's responsibility after curator approval
- **Bypass steward approval** — no auto-publication of alerts, condition ratings, or baselines outside Agent Registry pre-approved low-risk profiles registered before production runs
- **Publish observatory outputs** — no direct writes to public dashboards, Research Registry, Public Experience, or canonical observatory catalog; approved disposition flows through steward approval, Quality Review, and downstream platform layers

Agents without sufficient supporting material MUST NOT emit the observation; they route to steward review or emit a data-gap signal instead ([03-canonical-architecture.md](03-canonical-architecture.md), §6.6).

---

## 6. Observatory Tracks

The Heritage Observatory Agent organizes monitoring across three tracks. Each track produces typed observation proposals linked to a canonical site entity and a registered source.

### 6.1 World Heritage

| Attribute | Specification |
|-----------|---------------|
| **Scope** | UNESCO World Heritage sites (cultural, natural, mixed); inscribed, tentative, and delisted states where reference data is available |
| **Sources** | UNESCO World Heritage List, state-party boundary submissions, ICOMOS evaluation reports (where licensed), Source Discovery site registry, Knowledge Graph place entities |
| **Processing pattern** | Site identity resolution → boundary geometry normalization → state-party and inscription metadata sync → baseline profile establishment |
| **Output entities** | Site registry records with UNESCO ID, graph entity URI, boundary geometry (GeoJSON), inscription year, criteria, state-party affiliations, multilingual labels |
| **Standards** | SKOS site-type vocabularies, GeoJSON boundaries, ISO 639-3 labels, World Heritage metadata practices ([07-reference-standards.md](07-reference-standards.md)) |

### 6.2 Threats

| Attribute | Specification |
|-----------|---------------|
| **Scope** | Identified and potential threats to outstanding universal value and site integrity |
| **Sources** | UNESCO State of Conservation reports, World Heritage Centre in-danger listings, ICOMOS heritage-at-risk publications, ICCROM risk-preparedness guidance, partner monitoring programs, remote sensing change detection (where licensed), steward field assessments |
| **Processing pattern** | Threat signal ingest → controlled vocabulary classification (below) → spatial and temporal anchoring → severity scoring → deduplication against prior observations → alert proposal evaluation |
| **Output entities** | Threat observation proposals with `threatType` (SKOS URI from vocabulary below), severity tier, affected zone geometry, Evidence Output Profile, and review requirement |
| **Standards** | Institutional Threat Classification Vocabulary (SKOS concept scheme, UNESCO/ICOMOS-aligned); GeoJSON for affected areas; ISO 19115 observation metadata; PREMIS-aligned provenance |

**Threat Classification Vocabulary (controlled, canonical):**

Each threat observation MUST use exactly one primary `threatType` from this vocabulary. Multi-threat situations emit one proposal per primary threat or a composite proposal with a ranked primary type and secondary types in `evidenceSummary`.

| Term | SKOS prefLabel | Typical UNESCO/ICOMOS alignment |
|------|----------------|-----------------------------------|
| `threat:ClimateChange` | Climate Change | SOC climate-related ascertained and potential dangers |
| `threat:SeaLevelRise` | Sea Level Rise | Coastal inundation and erosion stress |
| `threat:Wildfire` | Wildfire | Fire damage to attributes and settings |
| `threat:Flooding` | Flooding | Hydrological and storm-surge damage |
| `threat:Earthquake` | Earthquake | Seismic structural and setting damage |
| `threat:Conflict` | Conflict | Armed conflict affecting site integrity |
| `threat:Vandalism` | Vandalism | Deliberate damage to attributes |
| `threat:Looting` | Looting | Illicit removal of cultural property |
| `threat:UrbanDevelopment` | Urban Development | Urban encroachment and incompatible land use |
| `threat:InfrastructureExpansion` | Infrastructure Expansion | Roads, dams, extractive and industrial infrastructure |
| `threat:MassTourism` | Mass Tourism | Large-scale visitation exceeding carrying capacity |
| `threat:VisitorPressure` | Visitor Pressure | Sustained physical wear from visitation |
| `threat:Pollution` | Pollution | Air, water, soil, and noise degradation |
| `threat:Neglect` | Neglect | Inadequate maintenance, management, or legislative protection |
| `threat:Unknown` | Unknown | Insufficient evidence for classification; triggers steward review |

### 6.3 Conservation Status

| Attribute | Specification |
|-----------|---------------|
| **Scope** | Periodic condition and conservation-state assessments per monitored site |
| **Sources** | UNESCO SOC assessments, state-party periodic reporting, ICOMOS monitoring missions, ICCROM conservation surveys, partner field documentation, steward-reviewed assessments |
| **Processing pattern** | Status report ingest → Heritage Condition Scale normalization (below) → baseline comparison → trend computation → snapshot proposal emission |
| **Output entities** | Conservation status snapshot proposals with `conditionRating`, component ratings (authenticity, integrity, management effectiveness where applicable), trend direction, reporting cycle, and Evidence Output Profile |
| **Standards** | Heritage Condition Scale (SKOS concept scheme); ISO 19115 for observation metadata; JSON-LD status snapshots with temporal validity intervals |

**Heritage Condition Scale (canonical):**

Each conservation status observation MUST use exactly one `conditionRating` from this scale. UNESCO SOC narrative assessments map to this scale during ingest; state-party SOC text remains authoritative when mapping is ambiguous.

| Rating | SKOS prefLabel | Meaning |
|--------|----------------|---------|
| `condition:Excellent` | Excellent | Outstanding universal value attributes fully sustained; no ascertained or potential danger |
| `condition:Good` | Good | Attributes sustained with minor concerns; corrective measures effective or in progress |
| `condition:Fair` | Fair | Ascertained or potential dangers present; sustained attention and measures required |
| `condition:Poor` | Poor | Significant deterioration or danger; corrective measures insufficient or delayed |
| `condition:Critical` | Critical | Severe ascertained danger to outstanding universal value; in-danger criteria may apply |
| `condition:Unknown` | Unknown | Insufficient evidence for rating; triggers data-gap alert for stewards |

---

## 7. Outputs

### 7.1 Observatory Observation Proposals

Each observation is emitted as **JSON-LD** with:

| Field | Requirement |
|-------|-------------|
| **Site anchor** | UNESCO World Heritage ID and canonical Knowledge Graph place entity URI |
| **Track** | `world-heritage`, `threats`, or `conservation-status` |
| **Observation type** | Track-specific type (e.g., `boundary-sync`, `threat-signal`, `status-snapshot`) |
| **Temporal bounds** | Observation timestamp; validity interval for status snapshots (ISO 8601) |
| **Spatial anchor** | GeoJSON geometry for site boundary or affected zone |
| **Threat or condition code** | `threatType` (§6.2) or `conditionRating` (§6.3) SKOS URI when applicable |
| **Review requirement** | Auto-approvable (pre-registered low-risk types only), standard steward review, or curator/sensitivity queue |
| **Provenance** | Agent version, ingest run identifier, steward attribution when human-reviewed |

Observation proposals are **candidates** until a steward approves them through the human-approval gate when policy requires review (public alerts, sensitive security threats, first-time baseline for a site, all `threat:Conflict`, `threat:Looting`, and `threat:Vandalism` signals unless pre-approved in Agent Registry).

### 7.2 Evidence Output Profile

Every Observatory Observation Proposal MUST include all normative Evidence Output Profile fields ([03-canonical-architecture.md](03-canonical-architecture.md), §6.6). Proposals with incomplete profiles are rejected by the AI Fabric governance chain and routed to steward review or data-gap handling. The agent MUST NOT emit a proposal when supporting material is insufficient ([03-canonical-architecture.md](03-canonical-architecture.md), §6.6).

| Field | Requirement |
|-------|-------------|
| **evidenceURIs[]** | URIs of supporting source records, preserved objects, UNESCO/ICOMOS/ICCROM publications, partner feeds, or steward-reviewed documents |
| **confidence** | Numeric score (0.0–1.0) or enumerated confidence tier (`feed-direct`, `machine-derived`, `steward-reviewed`) |
| **evidenceSummary** | Human-readable summary of supporting material, derivation context, and mapping rationale (e.g., SOC text → condition rating) |
| **method** | Derivation method identifier (e.g., `feed-direct`, `rule-based`, `spatial-join`, `machine-inferred`, `steward-reviewed`, `soc-mapping`) |
| **sourceRegistryRefs[]** | Registered Source Registry entry URIs for all upstream sources |
| **provenanceEventId** | PREMIS-aligned or institutional event identifier linking the output to the agent run |

Threat Alert Proposals (§7.3) and Conservation Status Snapshots (§7.4) inherit the profile from their triggering Observation Proposals.

### 7.3 Threat Alert Proposals

Threshold-triggered alert proposals include:

- Alert severity (`informational`, `watch`, `warning`, `critical`)
- Affected site URIs and optional zone geometry
- Triggering observation proposal URIs and rule identifier
- Recommended steward actions (review, escalate to state-party contact, hold from public)
- Public disclosure disposition (`public`, `researcher-only`, `steward-only`)
- Complete Evidence Output Profile (§7.1) — alerts without sufficient evidence MUST NOT be emitted

Alert proposals do not reach dashboards or the public experience without steward approval.

### 7.3 Conservation Status Snapshots

Periodic status bundles per site include:

- Current `conditionRating` and per-component ratings
- Trend vs. prior reporting cycle (`improving`, `stable`, `declining`, `insufficient-data`)
- Baseline comparison (distance from establishment baseline)
- Linked threat observation proposals active in the same reporting window
- Dashboard-ready time series pointers (activated only after steward approval and Quality Review clearance)

### 7.4 Research Registry Data Packages

Approved observatory datasets are packaged for Research Fabric export after Quality Review and Research Agent dataset review:

- DOI assignment via Research Fabric (not by this agent)
- Coverage manifest (sites, date range, tracks included)
- Methodology and source lineage documentation with full Evidence Output Profile on package manifest
- GeoJSON and JSON-LD exports with ISO 19115 metadata

---

## 8. AI Fabric Governance

| Gate | Requirement |
|------|-------------|
| **Agent Registry** | Agent version, connector scope, Threat Classification Vocabulary bindings, Heritage Condition Scale mappings, alert thresholds, auto-approval profiles, and public-disclosure rules registered before production runs |
| **Benchmarks** | Site coverage, observation ingest latency, threat classification accuracy, condition-rating agreement with steward review, false-alert rate, Evidence Output Profile completeness rate |
| **Evaluations** | Periodic review against Phase 15 success criteria and constitutional heritage observatory targets |
| **Safety Reviews** | Verify agent does not publish security-sensitive threat details, write graph assertions, override state-party authority, or assert unverified destruction or damage claims without evidence |
| **Human Approval** | Stewards approve observation proposals, public alert publication, sensitive threat records, baseline establishment for new sites, and cross-domain conservation intelligence bundles |

**Council assignment:** Research Council (UNESCO/ICOMOS/ICCROM alignment, threat taxonomy, conservation methodology) and Implementation Council (ingest pipelines, dashboard integration). Execution Council runs scheduled sync and alert evaluation. State-party and partner contacts participate in escalation workflows per covenant framework.

---

## 9. Phase Alignment

| Phase | Agent Scope |
|-------|-------------|
| **Knowledge Graph (Phase 5)** | Read-only: resolve World Heritage site entity URIs for observatory anchoring; no graph writes |
| **Research Fabric (Phase 8)** | Approved packages enter Research Agent review and Research Fabric export path |
| **Quality Platform (Phase 7)** | Quality Review Agent validates publication readiness of steward-approved observatory outputs |
| **Observatories (Phase 15)** | Full three-track monitoring operational; real-time or near-real-time partner feed ingest; steward review queues |
| **Public Experience (Phase 11)** | Dashboards consume approved observations only |
| **Digital Twin (post-founder)** | Feed conservation intelligence layer with threat correlation across heritage, biodiversity, and climate observatories ([06-build-roadmap.md](06-build-roadmap.md), Section 7) |

---

## 10. Success Criteria

Aligned with Observatories phase completion criteria ([06-build-roadmap.md](06-build-roadmap.md), Phase 15):

- Heritage observatory covers ≥ 50 World Heritage sites with baseline condition data across all three tracks
- World Heritage track: site registry aligned with UNESCO reference data and Knowledge Graph place entities
- Threats track: operational ingest from ≥ 2 authoritative sources (UNESCO SOC plus one partner or remote-sensing feed); 100% threat proposals use Threat Classification Vocabulary terms
- Conservation status track: longitudinal snapshots for ≥ 2 reporting cycles on monitored sites; 100% status proposals use Heritage Condition Scale ratings
- ≥ 95% of observation proposals include complete Evidence Output Profile fields before steward review
- Public and researcher dashboards with trend visualization and configurable alert thresholds (approved outputs only)
- Observatory data packages published in Research Registry with citation metadata after Research Agent review
- End-to-end demonstration: partner feed → agent ingest → observation proposal → steward approval → Quality Review → dashboard → Research Registry export
- Zero unapproved critical alerts published to public channels

---

## 11. Constraints

- **No canonical writes without approval.** The agent proposes observations and alerts; stewards approve when policy requires. Pre-approved auto-ingest is permitted only for registered sources and observation types listed in Agent Registry.
- **No graph assertions.** The agent reads Knowledge Graph place and site entities; Entity Assertions and relationship placements are the Knowledge Graph Agent's responsibility ([12-knowledge-graph-agent.md](12-knowledge-graph-agent.md)).
- **No publication without gates.** Observatory outputs reach public dashboards and Research Registry only after steward approval and Quality Review publication-readiness clearance ([13-quality-review-agent.md](13-quality-review-agent.md)).
- **Evidence mandatory.** Every observation and alert proposal includes complete Evidence Output Profile fields ([03-canonical-architecture.md](03-canonical-architecture.md), §6.6).
- **State-party authority respected.** UNESCO and state-party reports take precedence over third-party threat signals; conflicting assessments route to steward reconciliation, not automatic overwrite.
- **Security-sensitive threats are gated.** `threat:Conflict`, `threat:Looting`, and `threat:Vandalism` default to `steward-only` or `researcher-only` disposition until explicitly cleared for public disclosure.
- **Provenance chain intact.** Every observation traces to a registered source, ingest event, `provenanceEventId`, and agent version ([03-canonical-architecture.md](03-canonical-architecture.md), §6.2).
- **Graph-linked, not siloed.** Site identity always resolves to a Knowledge Graph place entity; observatory data does not maintain a parallel unidentified site catalog.
- **Peer observatory boundaries.** Climate exposure ([18-climate-observatory-agent.md](18-climate-observatory-agent.md)), tourism pressure ([20-tourism-observatory-agent.md](20-tourism-observatory-agent.md)), and biodiversity stress ([17-biodiversity-observatory-agent.md](17-biodiversity-observatory-agent.md)) supplement but do not replace Heritage conservation status assessments on the Conservation status track.
- **Covenant before privileged feeds.** Partner monitoring feeds and restricted SOC materials require covenant framework approval ([03-canonical-architecture.md](03-canonical-architecture.md), Covenant Framework).
- **Free access preserved.** Observatory data packages must not gate access to underlying canonical public memory ([01-mission-and-constitutional-charter.md](01-mission-and-constitutional-charter.md)).

---

*Previous: [18-climate-observatory-agent.md](18-climate-observatory-agent.md) · Next: [20-tourism-observatory-agent.md](20-tourism-observatory-agent.md) · Observatory peers: [17-biodiversity-observatory-agent.md](17-biodiversity-observatory-agent.md), [21-language-observatory-agent.md](21-language-observatory-agent.md)*
