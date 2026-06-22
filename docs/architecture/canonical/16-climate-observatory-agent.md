# Climate Observatory Agent

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Canonical |
| **Authority** | Open Grace Architecture Office |
| **Date** | 2026-06-22 |
| **Capability** | Observatories — Climate ([03-canonical-architecture.md](03-canonical-architecture.md), §5.5) |
| **Phase** | Observatories ([06-build-roadmap.md](06-build-roadmap.md), Phase 15) |

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
| [15-education-agent.md](15-education-agent.md) | Education Agent specification |
| [16-heritage-observatory-agent.md](16-heritage-observatory-agent.md) | Heritage Observatory Agent specification |
| [16-biodiversity-observatory-agent.md](16-biodiversity-observatory-agent.md) | Biodiversity Observatory Agent specification |
| [16-climate-observatory-agent.md](16-climate-observatory-agent.md) | Climate Observatory Agent specification |
| [16-tourism-observatory-agent.md](16-tourism-observatory-agent.md) | Tourism Observatory Agent specification |
| [17-language-observatory-agent.md](17-language-observatory-agent.md) | Language Observatory Agent specification |

---

## 1. Purpose

The **Climate Observatory Agent** automates the **Climate** observatory within the Observatory Network ([03-canonical-architecture.md](03-canonical-architecture.md), §5.5). It ingests climate and conservation feeds; correlates indicators with protected areas and World Heritage sites; scores heritage risk from climate stress; and emits **Observatory Observation Proposals** (JSON-LD / GeoJSON / NetCDF descriptors) for steward and curator approval before observations enter canonical observatory stores and the Knowledge Graph.

The agent does not assert site condition without evidence, publish unreviewed risk alerts to the public experience, or overwrite curator-authored conservation narratives. It proposes longitudinal observations and risk signals grounded in partner feeds and graph-linked place entities; observatory stewards and heritage curators approve.

---

## 2. Responsibilities

The agent operates three coordinated **tracks**. Each track has distinct inputs, processing patterns, and outputs; all tracks share graph anchoring, provenance, and AI Fabric governance.

| Track | Responsibility | Description |
|-------|----------------|-------------|
| **Climate impacts** | Monitor and correlate climate indicators | Ingest gridded and station climate data (temperature, precipitation, drought, sea-level, extreme-event indices); compute trends and anomalies at site, protected-area, and ecosystem scales; link indicators to graph place and ecosystem entities |
| **Protected areas** | Monitor conservation estate exposure | Ingest IUCN and national protected-area boundaries; align observatory indicators to park, reserve, and buffer geometries; detect overlap between climate stress signals and designated conservation zones; surface coverage and data-gap reports |
| **Heritage risk** | Score World Heritage climate vulnerability | Ingest UNESCO World Heritage site boundaries and state-of-conservation context; apply climate-exposure and hazard models; rank sites by composite heritage-risk score; emit threat summaries and recommended monitoring priorities for curator review |

---

## 3. Reference Models

The agent synthesizes patterns from three primary reference models ([02-reference-models.md](02-reference-models.md)):

| Model | Pattern Applied | Agent Behavior |
|-------|-----------------|----------------|
| **UNESCO** | World Heritage monitoring, state-of-conservation reporting, outstanding universal value framing, state-party cooperation | Anchor every heritage-risk output to World Heritage site graph entities; respect boundary and buffer definitions; route high-significance risk signals through curator queues; align terminology with state-of-conservation practice |
| **GBIF** | Federated occurrence data, Darwin Core event records, spatial aggregation, open research publishing | Publish approved observatory packages to Research Registry with DOI-ready metadata; use Darwin Core–compatible event descriptors where biodiversity overlap is analyzed; treat partner feeds as federated sources with explicit attribution |
| **National Geographic** | Public science storytelling, map-forward dashboards, longitudinal field observation | Produce researcher and public dashboard feeds with trend visualization; support alert thresholds without sensationalism; link observatory narratives to published exhibits when Publishing approves |

Supporting standards follow [07-reference-standards.md](07-reference-standards.md): JSON-LD, GeoJSON, WGS 84 / EPSG:4326, NetCDF (Permitted for gridded climate archives), CIDOC-CRM place and event modeling, PREMIS for observatory dataset provenance.

---

## 4. Position in Architecture

```
Partner climate feeds + protected-area registries + UNESCO site boundaries
        ↓
Field sensors + community observations + Research Fabric datasets
        ↓
Knowledge Graph place / site / ecosystem entities
        ↓
Climate Observatory Agent
  ├── Track: Climate impacts
  ├── Track: Protected areas
  └── Track: Heritage risk
        ↓
Observatory Observation Proposals — candidate, pending steward or curator approval
        ↓
Approved observatory records → Ingestion → Preservation → Graph annotations
        ↓
Observatory dashboards, Research Registry packages, Public Experience maps, Education (cleared datasets)
```

The agent operates in the **Experience Plane** Observatory Network — Climate subgraph ([04-system-diagram.md](04-system-diagram.md), §2). All outputs pass through the AI Fabric governance chain before affecting canonical systems ([04-system-diagram.md](04-system-diagram.md), §2.2).

**Upstream inputs:** Ingestion observatory feeds ([03-canonical-architecture.md](03-canonical-architecture.md), §4.2), Knowledge Graph place and site entities ([12-knowledge-graph-agent.md](12-knowledge-graph-agent.md)), Source Discovery candidate feeds for new climate and conservation data sources ([09-source-discovery-agent.md](09-source-discovery-agent.md)), quality and rights clearance from the Quality Review Agent ([13-quality-review-agent.md](13-quality-review-agent.md)).

**Downstream consumers:** Observatory public and researcher dashboards, Research Fabric (citation-ready datasets), Public Experience (maps and entity risk panels), Education Agent (classroom-cleared observatory datasets), Publishing (conservation narrative packages), Digital Twin geospatial layers (Phase 16+).

**Peer observatories:** Heritage, Biodiversity, Conservation, Tourism, and Sustainability observatories consume approved climate outputs; the Climate Observatory Agent does not duplicate heritage condition field assessments owned by the Heritage observatory — it supplies climate-exposure context.

---

## 5. Operational Tracks

### 5.1 Climate Impacts

| Attribute | Specification |
|-----------|---------------|
| **Sources** | NOAA, Copernicus, NASA Earthdata, national meteorological services, IPCC indicator definitions, partner gridded reanalysis and station networks |
| **Processing pattern** | Feed validation → temporal harmonization → spatial join to graph places → trend and anomaly computation → threshold evaluation → proposal emission |
| **Output entities** | Climate indicator time series, anomaly surfaces, extreme-event tallies, and site-level exposure summaries with measurement provenance |
| **Standards** | CF conventions for NetCDF where archived; JSON-LD `Observation` and `Dataset` descriptors; WGS 84 geometries; ISO 8601 temporal bounds |

**Indicator scope (minimum):**

| Indicator family | Use |
|------------------|-----|
| Temperature | Mean, minimum, maximum; heating-degree and cooling-degree anomalies where relevant |
| Precipitation | Totals, drought indices, seasonality shift |
| Hydrology | River discharge proxies, flood-frequency signals where feeds exist |
| Cryosphere | Glacier and permafrost proximity stress for alpine heritage |
| Coastal | Sea-level trend, storm-surge exposure, erosion proxies |
| Extremes | Heatwave, wildfire-weather, and storm indices aligned to partner feed availability |

### 5.2 Protected Areas

| Attribute | Specification |
|-----------|---------------|
| **Sources** | WDPA / Protected Planet, national park service boundaries, UNESCO buffer zones, partner covenant geospatial layers |
| **Processing pattern** | Boundary ingestion → graph entity reconciliation → spatial overlay with climate indicators → exposure scoring per protected unit → gap detection for unmonitored estates |
| **Output entities** | Protected-area exposure profiles, overlap maps, monitoring coverage reports, and candidate alerts when climate stress exceeds steward-defined thresholds |
| **Standards** | GeoJSON / GeoPackage interchange; SKOS labels for protected-area categories; graph `geo:hasGeometry` linkage to canonical place URIs |

The agent treats protected areas as **conservation observatory context**: it reports climate stress on designated estates but does not assert management decisions or boundary changes.

### 5.3 Heritage Risk

| Attribute | Specification |
|-----------|---------------|
| **Sources** | UNESCO World Heritage List geometries, state-of-conservation reports, ICCROM / ICOMOS published guidance, climate overlays from Track 5.1, curator-authored significance notes |
| **Processing pattern** | Site boundary join → hazard exposure scoring (flood, fire, coastal, freeze-thaw, humidity) → composite risk index → confidence tiering → curator-queue routing for high-significance sites |
| **Output entities** | Heritage Risk Assessments with hazard breakdown, trend direction, monitoring recommendations, and explicit uncertainty bounds |
| **Standards** | CIDOC-CRM site and event modeling; JSON-LD risk descriptors with `prov:wasDerivedFrom` links to climate observations and curator sources |

**Composite risk factors (illustrative):**

| Factor | Weighting approach |
|--------|-------------------|
| Exposure | Climate indicator anomaly magnitude at site polygon |
| Hazard | Domain-specific models (coastal inundation, wildfire probability, hydrological stress) |
| Sensitivity | Curator-supplied material and setting sensitivity flags when available |
| Adaptive capacity | Optional steward annotations; never machine-invented |
| Trend | Direction and velocity of exposure change over observatory baseline window |

Machine-generated risk ranks are **candidates** until a heritage curator or observatory steward approves public or research release.

---

## 6. Outputs

### 6.1 Observatory Observation Proposals

Each candidate observation or derived indicator is emitted as an **Observatory Observation Proposal** with:

| Field | Requirement |
|-------|-------------|
| **Track** | `climate-impacts`, `protected-areas`, or `heritage-risk` |
| **Temporal bounds** | Observation period with ISO 8601 start/end |
| **Spatial footprint** | GeoJSON geometry or graph place URI reference |
| **Indicator or hazard** | Typed indicator code, unit, and value or distribution summary |
| **Source feed** | Partner dataset URI, retrieval timestamp, and license expression |
| **Graph anchors** | Canonical place, site, protected-area, or ecosystem entity URIs |
| **Provenance** | Agent version, processing pipeline ID, upstream observation URIs |
| **Confidence tier** | `feed-direct`, `machine-derived`, or `steward-reviewed` |
| **Review requirement** | Auto-approvable (low-significance indicators), standard steward review, or curator queue (heritage-risk public release) |

### 6.2 Alert Proposals

When indicators cross steward-defined thresholds, the agent emits **Alert Proposals** containing:

- Affected entity URIs and human-readable place labels (via Translation Fabric)
- Threshold breached, current value, and baseline comparison window
- Recommended monitoring actions (not management directives)
- Expiry or re-evaluation schedule

Alerts do not reach the public experience without steward approval.

### 6.3 Observatory Coverage Reports

Each processing run emits a coverage report containing:

- Feeds ingested vs. targeted; failed or stale feeds
- Protected areas and World Heritage sites with vs. without current climate coverage
- Heritage-risk queue depth and approval turnaround metrics
- Spatial and temporal gaps with recommended Source Discovery targets

### 6.4 Research Registry Packages

Approved observation sets are packaged for Research Fabric with:

- DOI-ready descriptive metadata
- Citation block and reproducible query snapshot reference
- NetCDF or GeoPackage artifacts in Preservation storage
- Rights and attribution per partner feed licenses

---

## 7. AI Fabric Governance

| Gate | Requirement |
|------|-------------|
| **Agent Registry** | Agent version, supported indicator registries, hazard model versions, threshold policies, and feed allowlists registered before production runs |
| **Benchmarks** | Spatial join accuracy (human spot-check), feed freshness SLA compliance, false-alert rate on held-out steward validations, heritage-risk ranking stability across model versions |
| **Evaluations** | Periodic review against Phase 15 Observatories success criteria |
| **Safety Reviews** | Verify agent does not publish unapproved high-significance heritage-risk claims, misattribute partner data, or assert management or boundary changes |
| **Human Approval** | Observatory stewards approve Observation Proposals and alerts; heritage curators approve public heritage-risk releases for World Heritage sites |

**Council assignment:** Research Council (indicator science, hazard models, feed expansion) and Implementation Council (ingestion pipelines, dashboard feeds). Architecture Council reviews cross-observatory contracts with Heritage and Biodiversity observatories.

---

## 8. Phase Alignment

| Phase | Agent Scope |
|-------|-------------|
| **Knowledge Graph (Phase 5)** | Readiness only: place, site, and protected-area entity coverage for spatial joins |
| **Research Fabric (Phase 8)** | Research Registry export path for approved observatory packages |
| **Publishing (Phase 10)** | Conservation narrative hooks; no public risk storytelling without curator approval |
| **Public Experience (Phase 11)** | Map layers and entity risk panels consume approved observations only |
| **Observatories (Phase 15)** | Full three-track operation: climate impacts, protected areas, heritage risk; steward and curator review queues; live dashboards |
| **Education (Phase 13)** | Classroom-cleared observatory datasets exposed to Education Agent ([15-education-agent.md](15-education-agent.md)) |
| **Digital Twin (Phase 16)** | Approved climate and risk layers feed geospatial simulation substrates |

---

## 9. Success Criteria

Aligned with Observatories phase completion criteria ([06-build-roadmap.md](06-build-roadmap.md), Phase 15):

- Climate impacts track operational with ≥ 3 partner feeds ingested on schedule
- Protected areas track covers ≥ 80% of graph-linked protected units in pilot regions with exposure profiles
- Heritage risk track produces baseline assessments for ≥ 50 World Heritage sites
- ≥ 95% of public-facing observatory records pass steward or curator approval with full provenance
- Observatory data packages published in Research Registry with citation metadata
- End-to-end demonstration: partner feed → spatial join → observation proposal → steward approval → dashboard and Research Registry → graph-anchored public map layer

---

## 10. Constraints

- **No public heritage-risk publish without approval.** The agent proposes; observatory stewards and heritage curators approve.
- **Graph anchors mandatory.** Every spatial observation links to a canonical place, site, or protected-area entity ([03-canonical-architecture.md](03-canonical-architecture.md), Provenance).
- **Partner attribution non-negotiable.** Every indicator carries source feed URI, license, and retrieval provenance.
- **Uncertainty explicit.** Heritage-risk outputs state confidence tier, model version, and known gaps — never implied precision.
- **Peer observatory boundaries.** Climate exposure supplements but does not replace Heritage observatory condition assessments ([16-heritage-observatory-agent.md](16-heritage-observatory-agent.md), Conservation status track).
- **Free access preserved.** Observatory data packages must not gate access to underlying canonical public memory ([01-mission.md](01-mission.md)).
- **No management assertions.** The agent reports stress and risk signals; it does not direct conservation interventions or alter protected-area designations.

---

*Previous: [15-education-agent.md](15-education-agent.md) · Next: [04-system-diagram.md](04-system-diagram.md)*
