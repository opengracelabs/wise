# Reference Models

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Canonical |
| **Authority** | Open Grace Architecture Office |
| **Date** | 2026-06-22 |

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

This document catalogs the **eleven canonical reference models** that inform the Open Grace and Nature & Culture architecture. These institutions represent proven patterns for preservation, access, science, culture, education, and scale. The architecture does not replicate any single model; it synthesizes durable patterns from all eleven.

Reference models are cited in [08-decision-record.md](08-decision-record.md) as evidence for architectural choices.

---

## 2. Reference Model Summary

| Model | Primary Domain | Architectural Contribution |
|-------|---------------|---------------------------|
| [UNESCO](#3-unesco) | World heritage & culture | Global mandate, intangible heritage, multilingual covenant |
| [Smithsonian](#4-smithsonian) | Museum & research | Collection stewardship, interdisciplinary research, public education |
| [GBIF](#5-gbif) | Biodiversity science | Species data infrastructure, federated publishing, Darwin Core |
| [Europeana](#6-europeana) | Cultural aggregation | Metadata aggregation, rights framework, cross-institutional discovery |
| [Wikimedia](#7-wikimedia) | Open knowledge | Community governance, open content, multilingual corpus |
| [MIT](#8-mit) | Research & open access | Open publication, research infrastructure, long-term academic stewardship |
| [Stanford](#9-stanford) | Digital humanities | Computational scholarship, library-scale digitization, spatial humanities |
| [Harvard](#10-harvard) | Library & museum preservation | Long-horizon preservation, special collections, curatorial authority |
| [Google](#11-google) | Search & knowledge scale | Search architecture, knowledge representation, global infrastructure |
| [Internet Archive](#12-internet-archive) | Web & media preservation | Permanence ethic, format migration, Wayback-scale archiving |
| [National Geographic](#13-national-geographic) | Public science storytelling | Public experience, visual narrative, global exploration ethos |

---

## 3. UNESCO

**United Nations Educational, Scientific and Cultural Organization**

### What UNESCO Teaches Us

- **Global mandate** — Heritage and culture are humanity's shared responsibility, not any nation's property.
- **Intangible heritage** — Traditions, languages, and practices require equal standing with physical artifacts.
- **World Heritage framework** — Outstanding universal value, boundary definition, and state-party cooperation.
- **Multilingual commitment** — Official UN languages model the requirement for universal linguistic access.

### Architectural Application

| Pattern | Implementation |
|---------|---------------|
| World Heritage Sites ontology | Knowledge graph place and site modeling ([03-canonical-architecture.md](03-canonical-architecture.md)) |
| Intangible heritage records | Non-object entity types in knowledge modeling layer |
| State-party cooperation model | Inter-institutional covenant under Open Grace ([01-mission-and-constitutional-charter.md](01-mission-and-constitutional-charter.md)) |
| Multilingual mandate | Translation Fabric ([06-build-roadmap.md](06-build-roadmap.md)) |

---

## 4. Smithsonian

**Smithsonian Institution**

### What the Smithsonian Teaches Us

- **Collection stewardship at scale** — 150+ million objects require systematic cataloging, conservation, and access.
- **Interdisciplinary research** — Natural history, culture, and art belong in one institutional frame.
- **Public education mission** — Research and public experience are co-equal, not sequential.
- **Federal trust model** — Institutional permanence through governance, not commercial viability.

### Architectural Application

| Pattern | Implementation |
|---------|---------------|
| Unified collection registry | Canonical object store in preservation layer |
| Research-public dual mandate | Research Fabric and Public Experience ([06-build-roadmap.md](06-build-roadmap.md)) |
| Conservation metadata | Provenance and condition records in knowledge modeling |
| Institutional trust | Open Grace constitutional governance ([01-mission-and-constitutional-charter.md](01-mission-and-constitutional-charter.md)) |

---

## 5. GBIF

**Global Biodiversity Information Facility**

### What GBIF Teaches Us

- **Federated data publishing** — Institutions publish; a central index enables global discovery.
- **Darwin Core standard** — Shared vocabulary enables interoperability across heterogeneous sources.
- **Occurrence records** — Species observations are first-class entities linked to place and time.
- **Open science infrastructure** — Free, open access to biodiversity data drives research and policy.

### Architectural Application

| Pattern | Implementation |
|---------|---------------|
| Federated ingestion | Ingestion layer accepts publisher feeds ([03-canonical-architecture.md](03-canonical-architecture.md)) |
| Taxonomic backbone | Nature domain ontology in knowledge graph |
| Occurrence linking | Spatiotemporal indexing in search layer |
| Darwin Core alignment | [07-reference-standards.md](07-reference-standards.md) |

---

## 6. Europeana

**Europeana — Europe's Digital Cultural Heritage Platform**

### What Europeana Teaches Us

- **Metadata aggregation** — Rich discovery without requiring central storage of all assets.
- **Rights expression** — Clear, machine-readable rights statements enable lawful reuse.
- **Cross-institutional discovery** — Users search one portal; content remains at source institutions.
- **Cultural diversity** — 3,000+ contributing institutions model federated scale.

### Architectural Application

| Pattern | Implementation |
|---------|---------------|
| Aggregation-with-attribution | Discovery layer federates external catalogs |
| Rights metadata | EDMO/RightsStatements in knowledge modeling |
| Provider registry | Partner institution covenant framework |
| Faceted cultural search | Search and Public Experience layers |

---

## 7. Wikimedia

**Wikimedia Foundation (Wikipedia, Wikimedia Commons, Wikidata)**

### What Wikimedia Teaches Us

- **Community governance** — Distributed contributors sustain content at planetary scale.
- **Open licensing** — Creative Commons and public domain as default access posture.
- **Wikidata knowledge graph** — Structured, multilingual, community-maintained linked data.
- **Radical accessibility** — Free, no-account-required access as non-negotiable principle.

### Architectural Application

| Pattern | Implementation |
|---------|---------------|
| Community contribution | Community platform in build roadmap |
| Wikidata interoperability | Knowledge graph external linking |
| Open license registry | Rights and license metadata standards |
| Multilingual content | Translation Fabric |

---

## 8. MIT

**Massachusetts Institute of Technology**

### What MIT Teaches Us

- **Open access publication** — MIT Open Access Policy: research outputs belong to the commons.
- **DSpace institutional repository** — Long-term research object preservation pattern.
- **Cross-disciplinary research infrastructure** — Computation applied to every domain of knowledge.
- **OpenCourseWare precedent** — Educational content freely distributed at global scale.

### Architectural Application

| Pattern | Implementation |
|---------|---------------|
| Research object preservation | Research Fabric archival deposits |
| Open access mandate | Constitutional free-access commitment ([01-mission-and-constitutional-charter.md](01-mission-and-constitutional-charter.md)) |
| Educational publishing | Education platform in build roadmap |
| Repository pattern | Preservation layer design ([05-physical-architecture.md](05-physical-architecture.md)) |

---

## 9. Stanford

**Stanford University — Libraries & Digital Humanities**

### What Stanford Teaches Us

- **Digital humanities at scale** — Computational methods applied to cultural corpora.
- **Library digitization programs** — Systematic conversion of physical collections to digital surrogates.
- **Spatial humanities** — Geographic and temporal dimensions are essential to cultural understanding.
- **Persistent identifier commitment** — PURL and archival identifier patterns for long-term linking.

### Architectural Application

| Pattern | Implementation |
|---------|---------------|
| DH research tooling | Research Fabric APIs and datasets |
| Spatial-temporal indexing | Knowledge graph and search geospatial capabilities |
| Persistent identifiers | ARK/DOI/Handle registry in preservation layer |
| Digitization pipeline | Ingestion layer workflows ([06-build-roadmap.md](06-build-roadmap.md)) |

---

## 10. Harvard

**Harvard University — Libraries, Museums, and Preservation**

### What Harvard Teaches Us

- **Centuries-scale stewardship** — Harvard Library has operated for 400+ years; preservation is a multi-century discipline.
- **Curatorial authority** — Expert judgment on authenticity, attribution, and significance.
- **Special collections handling** — Rare and fragile materials require differentiated preservation tiers.
- **Library Cloud / linked open data** — Institutional metadata published as interconnected graphs.

### Architectural Application

| Pattern | Implementation |
|---------|---------------|
| Tiered preservation | Hot/warm/cold/archive tiers ([05-physical-architecture.md](05-physical-architecture.md)) |
| Curatorial workflow | Quality Platform in build roadmap |
| Special collection handling | Enhanced provenance and condition metadata |
| Linked open data publishing | Knowledge graph and Publishing layer |

---

## 11. Google

**Google — Search, Knowledge, and Infrastructure**

### What Google Teaches Us

- **Search at planetary scale** — Indexing, ranking, and retrieval for billions of entities.
- **Knowledge Graph** — Structured entity resolution across heterogeneous sources.
- **Global infrastructure** — Geographic distribution, redundancy, and latency optimization.
- **Multilingual search** — Cross-language retrieval and entity linking.

### Architectural Application

| Pattern | Implementation |
|---------|---------------|
| Entity-centric search | Search layer architecture ([03-canonical-architecture.md](03-canonical-architecture.md)) |
| Knowledge panel pattern | Public Experience entity pages |
| Distributed infrastructure | Physical architecture zones ([05-physical-architecture.md](05-physical-architecture.md)) |
| Cross-lingual retrieval | Translation Fabric integration with search |

---

## 12. Internet Archive

**Internet Archive**

### What the Internet Archive Teaches Us

- **Permanence as mission** — "Universal access to all knowledge" as institutional north star.
- **Format migration** — Proactive conversion as formats become obsolete.
- **Wayback Machine** — Temporal versioning of web and digital content.
- **Community archive** — Anyone can contribute; the archive grows through participation.

### Architectural Application

| Pattern | Implementation |
|---------|---------------|
| Format migration pipeline | Preservation layer migration workflows |
| Temporal versioning | Object version history in canonical store |
| Web capture | Ingestion of web-origin cultural content |
| Permanence ethic | 100-year architecture horizon ([01-mission-and-constitutional-charter.md](01-mission-and-constitutional-charter.md)) |

---

## 13. National Geographic

**National Geographic Society**

### What National Geographic Teaches Us

- **Public science storytelling** — Complex knowledge made accessible through narrative and visuals.
- **Exploration ethos** — Discovery as ongoing institutional activity, not a one-time project.
- **Visual-first experience** — Images, maps, and media are primary, not supplementary.
- **Global contributor network** — Explorers, photographers, and scientists as distributed knowledge sources.

### Architectural Application

| Pattern | Implementation |
|---------|---------------|
| Visual narrative UX | Public Experience and Products layers |
| Exploration/discovery | Discovery platform in build roadmap |
| Media-rich publishing | Publishing layer with IIIF support ([07-reference-standards.md](07-reference-standards.md)) |
| Contributor network | Community and Observatories platforms |

---

## 14. Synthesis Matrix

How reference models map to architectural layers (see [04-system-diagram.md](04-system-diagram.md)):

| Architectural Layer | Primary Reference Models |
|--------------------|-------------------------|
| Governance | UNESCO, Wikimedia, Internet Archive |
| Discovery | Europeana, Google, National Geographic |
| Ingestion | Smithsonian, Stanford, GBIF |
| Preservation | Harvard, Internet Archive, MIT |
| Knowledge Modeling | Wikidata/Wikimedia, GBIF, UNESCO |
| Knowledge Graph | Google, Wikidata, Europeana |
| Search | Google, Europeana |
| Quality Platform | Harvard, Smithsonian |
| Research Fabric | MIT, Stanford, GBIF |
| Translation Fabric | UNESCO, Wikimedia |
| Publishing | Europeana, National Geographic |
| Public Experience | National Geographic, Europeana, Google |
| Products | National Geographic |
| Education | MIT, Smithsonian |
| Community | Wikimedia, Internet Archive |
| Observatories | GBIF, National Geographic, UNESCO |

---

## 15. Using Reference Models in Governance

When evaluating architectural proposals:

1. Identify which reference model(s) support the proposal
2. Document the pattern being adopted in an ADR ([08-decision-record.md](08-decision-record.md))
3. Verify alignment with constitutional commitments ([01-mission-and-constitutional-charter.md](01-mission-and-constitutional-charter.md))
4. Confirm standards compliance ([07-reference-standards.md](07-reference-standards.md))

Reference models inform; they do not override Open Grace constitutional authority.

---

*Previous: [01-mission-and-constitutional-charter.md](01-mission-and-constitutional-charter.md) · Next: [03-canonical-architecture.md](03-canonical-architecture.md)*
