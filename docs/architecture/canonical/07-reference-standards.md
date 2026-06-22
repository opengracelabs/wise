# Reference Standards

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
| [18-standards-agent.md](18-standards-agent.md) | Standards Agent specification |

---

## 1. Purpose

This document defines the **reference standards** — protocols, vocabularies, and specifications — that the Open Grace and Nature & Culture architecture adopts, adapts, or extends. Standards are selected for 100-year durability, open governance, and broad institutional adoption.

Standards inform implementation across all platform layers defined in [03-canonical-architecture.md](03-canonical-architecture.md). Deviations require an ADR in [08-decision-record.md](08-decision-record.md).

---

## 2. Standards Governance

### 2.1 Adoption Levels

| Level | Meaning | Binding |
|-------|---------|---------|
| **Required** | Must implement for compliance | Milestone gate blocker |
| **Recommended** | Should implement when applicable | Architecture Office review |
| **Permitted** | May use where appropriate | Document in implementation ADR |
| **Prohibited** | Must not use | Constitutional violation |

### 2.2 Standards Registry Maintenance

The Open Grace Architecture Office maintains this registry. New standards are added via ADR. Deprecated standards remain listed with migration guidance for historical objects.

---

## 3. Preservation Standards

| Standard | Version | Level | Application |
|----------|---------|-------|-------------|
| **OAIS** (ISO 14721) | 2012 | Required | Preservation layer reference model ([03-canonical-architecture.md](03-canonical-architecture.md), Section 4.3) |
| **PREMIS** | 3.0 | Required | Preservation metadata embedded in ingest packages |
| **BagIt** | IETF RFC 8493 | Required | Ingest package format |
| **ARK** (Archival Resource Key) | NAAN registry | Required | Persistent identifiers for canonical objects |
| **DOI** | ISO 26324 | Required | Research datasets and publications |
| **Handle System** | — | Permitted | Legacy identifier interoperability |
| **METS** | 1.12 | Recommended | Complex object packaging (multi-file artifacts) |
| **Audit** (OAIS audit trail) | — | Required | Fixity and migration event logging |

### 3.1 OAIS Functional Mapping

| OAIS Function | Architecture Layer |
|--------------|-------------------|
| Ingest | Ingestion ([06-build-roadmap.md](06-build-roadmap.md), Phase 2) |
| Archival Storage | Preservation (Phase 3) |
| Data Management | Knowledge Modeling (Phase 4) |
| Access | Search, Research Fabric, Public Experience |
| Preservation Planning | Open Grace Stewardship Policy |
| Administration | Quality Platform (Phase 7) |

---

## 4. Metadata Standards

### 4.1 Heritage and Culture

| Standard | Level | Application |
|----------|-------|-------------|
| **CIDOC-CRM** | Required | Conceptual ontology for cultural heritage entities |
| **Dublin Core** | Required | Base descriptive metadata (DC Terms) |
| **EDM** (Europeana Data Model) | Required | Cross-institutional metadata aggregation |
| **RiC-O** (Records in Contexts) | Recommended | Archival authority records |
| **Schema.org** | Recommended | Web-facing structured data |
| **SKOS** | Required | Controlled vocabularies and thesauri |
| **Wikidata** | Required | External entity linking |

### 4.2 Nature and Biodiversity

| Standard | Level | Application |
|----------|-------|-------------|
| **Darwin Core** | Required | Species occurrence and taxonomic data |
| **GBIF Taxonomic Backbone** | Required | Species name resolution |
| **DwC-A** (Darwin Core Archive) | Required | Biodiversity data exchange format |
| **EML** (Ecological Metadata Language) | Recommended | Dataset-level ecological metadata |
| **ISO 19115** | Recommended | Geospatial metadata for observations |

### 4.3 Rights and Licensing

| Standard | Level | Application |
|----------|-------|-------------|
| **RightsStatements.org** | Required | Machine-readable rights categories |
| **Creative Commons** | Required | License expression (CC REL) |
| **ODRL** | Recommended | Complex rights policy expression |

---

## 5. Data Exchange Standards

| Standard | Level | Application |
|----------|-------|-------------|
| **JSON-LD** | Required | Primary structured data serialization |
| **RDF 1.1** | Required | Knowledge graph triple serialization |
| **RDFa** | Permitted | Embedded metadata in HTML publications |
| **OAI-PMH** | Required | Metadata harvesting from partner institutions |
| **IIIF Presentation API** | Required | Image and media collection publishing |
| **IIIF Image API** | Required | Image delivery and manipulation |
| **SPARQL 1.1** | Required | Knowledge graph query protocol |
| **GraphQL** | Required | Application-layer API for experience plane |
| **REST (OpenAPI 3.1)** | Required | Research Fabric and partner APIs |
| **Activity Streams 2.0** | Recommended | Provenance and event streaming |
| **GeoJSON** | Required | Geospatial data exchange |
| **GeoSPARQL** | Recommended | Geospatial graph queries |

---

## 6. Media and Format Standards

### 6.1 Preservation Formats (Required Normalization Targets)

| Media Type | Preservation Format | Notes |
|-----------|-------------------|-------|
| Text | UTF-8 plain text + PDF/A-2 | PDF/A for formatted documents |
| Images | TIFF (uncompressed) + JPEG 2000 | TIFF for master; JP2 for access |
| Audio | WAV (Broadcast Wave Format) | 48kHz/24-bit minimum for born-digital |
| Video | FFV1 in MKV (lossless) | H.264/H.265 access derivatives |
| 3D | OBJ + glTF | OBJ for preservation; glTF for access |
| Geospatial | GeoTIFF + GeoJSON | Per ISO 19115 metadata |
| Tabular | CSV (UTF-8) + Parquet | CSV for longevity; Parquet for analytics |

### 6.2 Prohibited Preservation Formats

| Format | Reason |
|--------|--------|
| Proprietary raw camera formats without open specification | Migration risk |
| DRM-protected media | Access and preservation conflict |
| Executable binaries (as preservation target) | Emulation burden without OAIS justification |
| Password-protected archives | Key management beyond 100-year horizon |

### 6.3 Format Identification

| Tool/Standard | Level | Application |
|--------------|-------|-------------|
| **PRONOM** (DROID) | Required | Format identification on ingest |
| **FIDO** | Recommended | Alternative format identification |
| **Wikidata format entities** | Recommended | Format registry linking |

---

## 7. Web and Accessibility Standards

| Standard | Level | Application |
|----------|-------|-------------|
| **HTML5** | Required | Public Experience markup |
| **WCAG 2.1 Level AA** | Required | Accessibility compliance |
| **ARIA 1.2** | Required | Accessible rich interactions |
| **HTTP/2** | Required | Transport protocol |
| **TLS 1.3** | Required | Encryption in transit |
| **Content Security Policy** | Required | XSS prevention |
| **hreflang** | Required | Multilingual page linking |
| **BCP 47** | Required | Language tag specification |

---

## 8. Security Standards

| Standard | Level | Application |
|----------|-------|-------------|
| **OWASP ASVS** Level 2 | Required | Application security verification |
| **NIST SP 800-207** | Recommended | Zero-trust architecture principles |
| **ISO 27001** | Recommended | Information security management |
| **FIDO2/WebAuthn** | Recommended | Contributor and curator authentication |
| **OAuth 2.1 / OIDC** | Required | API authentication and partner federation |
| **SHA-256** | Required | Fixity checksums |
| **AES-256-GCM** | Required | Encryption at rest |

---

## 9. Translation and Localization Standards

| Standard | Level | Application |
|----------|-------|-------------|
| **XLIFF 2.1** | Required | Translation interchange format |
| **TMX 1.4b** | Required | Translation memory exchange |
| **TBX** | Recommended | Terminology database exchange |
| **Unicode CLDR** | Required | Locale data (dates, numbers, collation) |
| **BCP 47** | Required | Language identification |
| **ISO 639-3** | Required | Language codes (including endangered languages) |
| **ISO 15924** | Required | Script codes |

---

## 10. Identifier Registries

| Registry | Authority | Application |
|----------|-----------|-------------|
| **ARK NAAN** | California Digital Library | Canonical object identifiers |
| **DOI Foundation** | International DOI Foundation | Research datasets and publications |
| **ORCID** | ORCID Inc. | Researcher identification |
| **ISNI** | ISO 27729 | Contributor identification |
| **GeoNames** | GeoNames.org | Place name authority |
| **GBIF Taxonomic Backbone** | GBIF | Species name authority |
| **Wikidata** | Wikimedia Foundation | Cross-domain entity authority |
| **VIAF** | OCLC | Person/name authority |
| **ISO 3166** | ISO | Country and region codes |

---

## 11. Standards by Architecture Layer

| Layer | Primary Standards |
|-------|------------------|
| Discovery | OAI-PMH, EDM, JSON-LD |
| Ingestion | BagIt, PREMIS, PRONOM, Dublin Core |
| Preservation | OAIS, ARK, PREMIS, preservation formats (Section 6.1) |
| Knowledge Modeling | CIDOC-CRM, Darwin Core, SKOS, RDF |
| Knowledge Graph | RDF, SPARQL, GeoSPARQL, Wikidata |
| Search | JSON-LD, GeoJSON, schema.org |
| Quality Platform | PREMIS (audit), SKOS (authority reconciliation) |
| Research Fabric | DOI, DwC-A, REST/OpenAPI, RDF |
| Translation Fabric | XLIFF, TMX, BCP 47, ISO 639-3 |
| Publishing | IIIF, EDM, HTML5, JSON-LD |
| Public Experience | HTML5, WCAG 2.1, IIIF, hreflang |
| Products | OpenAPI, OAuth 2.1, JSON-LD |
| Education | SCORM (Permitted), HTML5, WCAG 2.1 |
| Community | Activity Streams, OAuth 2.1, ORCID |
| Observatories | Darwin Core, GeoJSON, EML, ISO 19115 |

---

## 12. Standards by Reference Model

Cross-reference to [02-reference-models.md](02-reference-models.md):

| Reference Model | Standards Contributed |
|----------------|----------------------|
| UNESCO | Multilingual (ISO 639-3), World Heritage metadata practices |
| Smithsonian | Dublin Core, LIDO (Permitted) |
| GBIF | Darwin Core, DwC-A, EML |
| Europeana | EDM, RightsStatements.org, OAI-PMH |
| Wikimedia | Wikidata, Creative Commons, MediaWiki API patterns |
| MIT | DSpace (Recommended), open access metadata |
| Stanford | IIIF, Bibframe (Recommended) |
| Harvard | METS, MODS (Recommended), ARK |
| Google | schema.org, Knowledge Graph patterns |
| Internet Archive | ARC/WARC (Required for web archives), ARK |
| National Geographic | IPTC Photo Metadata (Recommended) |

---

## 13. Format Migration Schedule

To maintain 100-year readability ([01-mission.md](01-mission.md), Section 4):

| Assessment | Frequency | Action |
|-----------|-----------|--------|
| Format obsolescence scan | Annual | Identify at-risk formats in corpus |
| Migration priority queue | Quarterly | Rank by risk × access frequency |
| Migration execution | Continuous | Convert to current preservation targets |
| Original retention | Permanent | Original bitstream never deleted |
| Migration documentation | Per event | PREMIS migration event in provenance |

---

## 14. Compliance Verification

Milestone gates ([06-build-roadmap.md](06-build-roadmap.md), Section 6) require standards compliance verification:

1. **Automated** — [Standards Agent](18-standards-agent.md) conformance checks (CIDOC-CRM SHACL, Darwin Core term and DwC-A validation, schema.org JSON-LD profiles); schema validation, format identification, API contract testing
2. **Manual** — Architecture Office review for Recommended standards
3. **External** — Partner institution audit for covenant compliance

Non-compliance blocks phase progression until remediated or granted a documented waiver via ADR.

---

## 15. Standards Authority

Additions, modifications, or deprecations to this registry require an ADR in [08-decision-record.md](08-decision-record.md).

---

*Previous: [06-build-roadmap.md](06-build-roadmap.md) · Next: [08-decision-record.md](08-decision-record.md)*
