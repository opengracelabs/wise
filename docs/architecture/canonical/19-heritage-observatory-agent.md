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

---

## 1. Purpose

The **Heritage Observatory Agent** automates the **Heritage** observatory within the Observatory Network ([03-canonical-architecture.md](03-canonical-architecture.md), §5.5). It ingests UNESCO-aligned reference data and partner feeds; maintains World Heritage site identity aligned with the Knowledge Graph; tracks threats to outstanding universal value; and records conservation status over time — emitting **Observatory Observation Proposals** (JSON-LD / GeoJSON) for steward approval before observations enter canonical observatory stores, public dashboards, and Research Registry exports.

The agent does not replace state-party reporting authority, assert unverified threat claims as fact, or publish sensitive site security information to the public experience without governance review. It monitors, correlates, and surfaces heritage condition intelligence grounded in registered sources and graph-linked site entities.

---

## 2. Responsibilities

The agent operates three coordinated **tracks**. Each track has distinct inputs, processing patterns, and outputs; all tracks share graph anchoring, provenance, and AI Fabric governance.

| Track | Responsibility | Description |
|-------|----------------|-------------|
| **World Heritage** | Maintain site registry and identity | Align UNESCO World Heritage List entries, boundaries, and state-party affiliations with Knowledge Graph place entities; establish baseline site profiles for all monitored locations |
| **Threats** | Monitor and classify threat signals | Ingest, classify, and time-stamp threat observations (climate, conflict, development, tourism pressure, natural disaster, and UNESCO State of Conservation categories); correlate multi-source signals; emit threshold-based alerts when escalation rules match |
| **Conservation status** | Record condition and trends | Capture periodic condition assessments, conservation-state ratings, and trend indicators; maintain longitudinal status time series per site; support dashboards comparing current status to baseline and prior reporting cycles |

---

## 3. Reference Models

The agent synthesizes patterns from three primary reference models ([02-reference-models.md](02-reference-models.md)):

| Model | Pattern Applied | Agent Behavior |
|-------|-----------------|----------------|
| **UNESCO** | World Heritage framework, state-party cooperation, State of Conservation reporting, outstanding universal value | Sync World Heritage site reference data; map SOC threat and status vocabularies; respect state-party as authoritative reporter; align multilingual site metadata |
| **National Geographic** | Field documentation, geospatial storytelling, longitudinal place monitoring, public science communication | Integrate partner field assessments and georeferenced observations; support researcher and public dashboard narratives with provenance-linked evidence |
| **GBIF** (patterns) | Federated observation ingest, Darwin Core event records, open longitudinal datasets | Model heritage observations as time-stamped, georeferenced events with standardized fields; publish cleared datasets through Research Fabric with citation metadata |

Supporting standards alignment follows [07-reference-standards.md](07-reference-standards.md): GeoJSON, ISO 19115, EML, SKOS threat and status vocabularies, CIDOC-CRM place and event bindings.

---

## 4. Position in Architecture

```
UNESCO reference data + partner feeds + field sensors + steward assessments
        ↓
Source Registry + Knowledge Graph site entities (from Source Discovery, Metadata, Graph agents)
        ↓
Heritage Observatory Agent
  ├── Track: World Heritage
  ├── Track: Threats
  └── Track: Conservation status
        ↓
Observatory Observation Proposals — candidate, pending steward approval
        ↓
Observatory catalog + trend dashboards + Research Registry data packages
        ↓
Public Experience, Research Fabric, Education Agent, Digital Twin conservation intelligence
```

The agent operates in the **Observatories** subgraph of the Experience Plane ([04-system-diagram.md](04-system-diagram.md), §2). All high-impact outputs (public alert publication, sensitive threat disclosure, cross-domain conservation intelligence bundles) pass through the AI Fabric governance chain before affecting canonical systems ([04-system-diagram.md](04-system-diagram.md), §2.2).

**Upstream inputs:** World Heritage site reference data from the Source Discovery Agent ([09-source-discovery-agent.md](09-source-discovery-agent.md)); modeled place and site entities from Knowledge Modeling and the Knowledge Graph Agent ([12-knowledge-graph-agent.md](12-knowledge-graph-agent.md)); ingested observation packages from partner feeds and field collectors; quality and rights clearance signals from the Quality Review Agent ([13-quality-review-agent.md](13-quality-review-agent.md)).

**Downstream consumers:** Public Experience (heritage condition dashboards), Research Fabric (observatory dataset exports), Education Agent (classroom-cleared observatory datasets, [16-education-agent.md](16-education-agent.md)), Digital Twin conservation intelligence layer, Climate Observatory Agent (heritage-risk correlation, [18-climate-observatory-agent.md](18-climate-observatory-agent.md)), Tourism Observatory Agent (visitor-impact correlation, [20-tourism-observatory-agent.md](20-tourism-observatory-agent.md)), Biodiversity Observatory Agent (ecological threat correlation, [17-biodiversity-observatory-agent.md](17-biodiversity-observatory-agent.md)).

---

## 5. Observatory Tracks

The Heritage Observatory Agent organizes monitoring across three tracks. Each track produces typed observation records linked to a canonical site entity and a registered source.

### 5.1 World Heritage

| Attribute | Specification |
|-----------|---------------|
| **Scope** | UNESCO World Heritage sites (cultural, natural, mixed); inscribed, tentative, and delisted states where reference data is available |
| **Sources** | UNESCO World Heritage List, state-party boundary submissions, Source Discovery site registry, Knowledge Graph place entities |
| **Processing pattern** | Site identity resolution → boundary geometry normalization → state-party and inscription metadata sync → baseline profile establishment |
| **Output entities** | Site registry records with UNESCO ID, graph entity URI, boundary geometry (GeoJSON), inscription year, criteria, state-party affiliations, multilingual labels |
| **Standards** | SKOS site-type vocabularies, GeoJSON boundaries, ISO 639-3 labels, World Heritage metadata practices ([07-reference-standards.md](07-reference-standards.md)) |

### 5.2 Threats

| Attribute | Specification |
|-----------|---------------|
| **Scope** | Identified and potential threats to outstanding universal value and site integrity |
| **Sources** | UNESCO State of Conservation reports, World Heritage Centre in-danger listings, partner monitoring programs, remote sensing change detection (where licensed), steward field assessments |
| **Processing pattern** | Threat signal ingest → taxonomy classification → spatial and temporal anchoring → severity scoring → deduplication against prior observations → alert evaluation |
| **Output entities** | Threat observation records with threat type, severity tier, affected zone geometry, evidence links, source attribution, and confidence score |
| **Standards** | UNESCO SOC threat categories (SKOS-aligned extension), GeoJSON for affected areas, ISO 19115 observation metadata, PREMIS-aligned provenance for derived assessments |

**Threat categories (canonical extension, UNESCO-aligned):**

| Category | Examples |
|----------|----------|
| **Climate and environment** | Sea-level rise, erosion, drought, wildfire, glacier loss |
| **Development pressure** | Urban encroachment, infrastructure, extractive industry |
| **Tourism and visitation** | Overtourism, physical wear, carrying-capacity exceedance |
| **Conflict and security** | Armed conflict, looting, deliberate destruction |
| **Natural disaster** | Earthquake, flood, cyclone, volcanic activity |
| **Biological and ecological** | Invasive species, habitat loss (natural sites) |
| **Management and governance** | Inadequate management systems, legislative gaps, funding shortfalls |

### 5.3 Conservation Status

| Attribute | Specification |
|-----------|---------------|
| **Scope** | Periodic condition and conservation-state assessments per monitored site |
| **Sources** | UNESCO SOC assessments, state-party periodic reporting, partner conservation surveys, steward-reviewed field documentation |
| **Processing pattern** | Status report ingest → rating normalization → baseline comparison → trend computation → snapshot emission |
| **Output entities** | Conservation status snapshots with overall condition rating, component ratings (authenticity, integrity, management effectiveness where applicable), trend direction, reporting cycle, and supporting evidence URIs |
| **Standards** | UNESCO SOC rating scales, ISO 19115 for observation metadata, JSON-LD status snapshots with temporal validity intervals |

**Status rating scale (canonical):**

| Rating | Meaning |
|--------|---------|
| **Good** | Outstanding universal value attributes are sustained; no ascertained or potential danger |
| **Good with concerns** | Minor ascertained or potential dangers; corrective measures in progress or planned |
| **Significant concerns** | Ascertained or potential dangers requiring sustained attention; measures needed |
| **Critical** | Ascertained danger to outstanding universal value; in-danger criteria may apply |
| **Unknown** | Insufficient evidence for rating; triggers data-gap alert for stewards |

---

## 6. Outputs

### 6.1 Observatory Observation Proposals

Each observation is emitted as **JSON-LD** with:

| Field | Requirement |
|-------|-------------|
| **Site anchor** | UNESCO World Heritage ID and canonical Knowledge Graph place entity URI |
| **Track** | `world-heritage`, `threats`, or `conservation-status` |
| **Observation type** | Track-specific type (e.g., `boundary-sync`, `threat-signal`, `status-snapshot`) |
| **Temporal bounds** | Observation timestamp; validity interval for status snapshots |
| **Spatial anchor** | GeoJSON geometry for site boundary or affected zone |
| **Source attribution** | Link to registered Source Registry entry and original report URI when available |
| **Confidence score** | Machine-derived confidence with evidence summary |
| **Provenance** | Agent version, ingest run identifier, steward attribution when human-reviewed |
| **Evidence profile** | [Evidence Output Profile](03-canonical-architecture.md#66-evidence-output-profile): `evidenceURIs[]`, `confidence`, `evidenceSummary`, `method`, `sourceRegistryRefs[]`, `provenanceEventId` |

Observation proposals are **candidates** until a steward approves them through the human-approval gate when policy requires review (public alerts, sensitive security threats, first-time baseline for a site).

### 6.2 Threat Alerts

Threshold-triggered alert events include:

- Alert severity (`informational`, `watch`, `warning`, `critical`)
- Affected site URIs and optional zone geometry
- Triggering observation URIs and rule identifier
- Recommended steward actions (review, escalate to state-party contact, hold from public)
- Public disclosure disposition (`public`, `researcher-only`, `steward-only`)

### 6.3 Conservation Status Snapshots

Periodic status bundles per site include:

- Current rating and per-component ratings
- Trend vs. prior reporting cycle (`improving`, `stable`, `declining`, `insufficient-data`)
- Baseline comparison (distance from establishment baseline)
- Linked threat observations active in the same reporting window
- Dashboard-ready time series pointers for Public Experience and Research Fabric

### 6.4 Research Registry Data Packages

Cleared observatory datasets published for citation include:

- DOI assignment via Research Fabric
- Coverage manifest (sites, date range, tracks included)
- Methodology and source lineage documentation
- GeoJSON and JSON-LD exports with ISO 19115 metadata

---

## 7. AI Fabric Governance

| Gate | Requirement |
|------|-------------|
| **Agent Registry** | Agent version, connector scope, threat taxonomy bindings, alert thresholds, and public-disclosure rules registered before production runs |
| **Benchmarks** | Site coverage, observation ingest latency, threat classification accuracy, status rating agreement with steward review, false-alert rate |
| **Evaluations** | Periodic review against Phase 15 success criteria and constitutional heritage observatory targets |
| **Safety Reviews** | Verify agent does not publish security-sensitive threat details, override state-party authority, or assert unverified destruction or damage claims without evidence |
| **Human Approval** | Stewards approve public alert publication, sensitive threat records, baseline establishment for new sites, and cross-domain conservation intelligence bundles |

**Council assignment:** Research Council (UNESCO alignment, threat taxonomy, conservation methodology) and Implementation Council (ingest pipelines, dashboard integration). Execution Council runs scheduled sync and alert evaluation. State-party and partner contacts participate in escalation workflows per covenant framework.

---

## 8. Phase Alignment

| Phase | Agent Scope |
|-------|-------------|
| **Knowledge Graph (Phase 5)** | Resolve World Heritage site entities; establish graph anchors for observatory site registry |
| **Research Fabric (Phase 8)** | Publish first observatory data packages with DOI and citation metadata |
| **Observatories (Phase 15)** | Full three-track monitoring operational; real-time or near-real-time partner feed ingest; public and researcher dashboards |
| **Digital Twin (post-founder)** | Feed conservation intelligence layer with threat correlation across heritage, biodiversity, and climate observatories ([06-build-roadmap.md](06-build-roadmap.md), Section 7) |

---

## 9. Success Criteria

Aligned with Observatories phase completion criteria ([06-build-roadmap.md](06-build-roadmap.md), Phase 15):

- Heritage observatory covers ≥ 50 World Heritage sites with baseline condition data across all three tracks
- World Heritage track: site registry aligned with UNESCO reference data and Knowledge Graph place entities
- Threats track: operational ingest from ≥ 2 authoritative sources (UNESCO SOC plus one partner or remote-sensing feed)
- Conservation status track: longitudinal snapshots for ≥ 2 reporting cycles on monitored sites
- Public and researcher dashboards with trend visualization and configurable alert thresholds
- Observatory data packages published in Research Registry with citation metadata
- End-to-end demonstration: partner feed → agent ingest → steward approval → dashboard → Research Registry export

---

## 10. Constraints

- **No canonical writes without approval.** The agent proposes observations and alerts; stewards approve when policy requires. Pre-approved auto-ingest is permitted only for registered sources and observation types listed in Agent Registry.
- **State-party authority respected.** UNESCO and state-party reports take precedence over third-party threat signals; conflicting assessments route to steward reconciliation, not automatic overwrite.
- **Security-sensitive threats are gated.** Threats affecting site security, looting risk, or conflict zones default to `steward-only` or `researcher-only` disposition until explicitly cleared for public disclosure.
- **Provenance chain intact.** Every observation traces to a registered source, ingest event, and agent version ([03-canonical-architecture.md](03-canonical-architecture.md), Provenance).
- **Graph-linked, not siloed.** Site identity always resolves to a Knowledge Graph place entity; observatory data does not maintain a parallel unidentified site catalog.
- **Peer observatory boundaries.** Climate exposure signals ([18-climate-observatory-agent.md](18-climate-observatory-agent.md)) and tourism impact metrics ([20-tourism-observatory-agent.md](20-tourism-observatory-agent.md)) supplement but do not replace heritage conservation status assessments on this agent's Conservation status track.
- **Covenant before privileged feeds.** Partner monitoring feeds and restricted SOC materials require covenant framework approval ([03-canonical-architecture.md](03-canonical-architecture.md), Covenant Framework).

---

*Previous: [16-education-agent.md](16-education-agent.md) · Observatory peers: [17-biodiversity-observatory-agent.md](17-biodiversity-observatory-agent.md), [18-climate-observatory-agent.md](18-climate-observatory-agent.md), [20-tourism-observatory-agent.md](20-tourism-observatory-agent.md)*
