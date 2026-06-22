/** Reference Capability 2 species page loader. */

(function () {
  function setBadge(element, label, passed) {
    element.textContent = `${label}: ${passed ? "verified" : "pending"}`;
    element.classList.add(passed ? "pass" : "fail");
    element.setAttribute("aria-label", `${label} ${passed ? "verified" : "not verified"}`);
  }

  function text(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value ?? "—";
  }

  async function load(stableId) {
    const errorPanel = document.getElementById("load-error");
    try {
      const response = await fetch(`/v1/species/${stableId}`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();

      document.title = `${data.scientific_name} — WISE Reference Capability 2`;
      text("object-title", data.scientific_name);
      text("object-subtitle", data.common_name);
      text("object-description", data.metadata.description || data.discovery.description);
      text("gbif-taxon-key", data.species_registry.gbif_taxon_key);
      text("gbif-usage-key", data.species_registry.gbif_usage_key);
      text("wikidata-id", data.discovery.external_identifiers.wikidata);
      text("eol-id", data.discovery.external_identifiers.eol);
      text("taxon-rank", data.species_registry.taxonomic_rank);
      text("object-ark", data.preservation.ark);
      text("rights-status", data.discovery.rights_uri);
      text("family", data.species_registry.darwin_core.family);
      text("genus", data.species_registry.darwin_core.genus);
      text("fixity-digest", data.preservation.fixity.digest);
      text("storage-tier", data.preservation.storage_tier);
      text("entity-type", data.graph_entity.entity_type);
      text("quality-finding", data.quality_review.finding);
      text("quality-score", data.quality_review.composite_score.toFixed(2));

      setBadge(document.getElementById("rights-badge"), "Rights", data.rights_verified);
      setBadge(document.getElementById("quality-badge"), "Quality", data.quality_approved);
      setBadge(
        document.getElementById("accessibility-badge"),
        "Accessibility",
        data.accessibility_compliant
      );

      const chain = document.getElementById("provenance-chain");
      chain.innerHTML = "";
      data.provenance_chain.forEach((eventId) => {
        const item = document.createElement("li");
        item.textContent = eventId;
        chain.appendChild(item);
      });

      const backbone = document.getElementById("taxonomic-backbone");
      backbone.innerHTML = "";
      data.taxonomic_backbone.forEach((node) => {
        const item = document.createElement("li");
        item.textContent = `${node.taxonomic_rank}: ${node.scientific_name} (GBIF ${node.gbif_usage_key})`;
        backbone.appendChild(item);
      });

      const premis = document.getElementById("premis-events");
      premis.innerHTML = "";
      data.preservation_events.forEach((event) => {
        const item = document.createElement("li");
        item.textContent = `${event.event_type}: ${event.event_detail}`;
        premis.appendChild(item);
      });

      const links = document.getElementById("external-links");
      links.innerHTML = "";
      data.graph_entity.external_links.forEach((link) => {
        const item = document.createElement("li");
        const anchor = document.createElement("a");
        if (link.external_authority === "wikidata") {
          anchor.href = `https://www.wikidata.org/wiki/${link.external_identifier}`;
        } else if (link.external_authority === "eol") {
          anchor.href = `https://eol.org/pages/${link.external_identifier}`;
        } else {
          anchor.href = "#";
        }
        anchor.textContent = `${link.external_authority}:${link.external_identifier} (${link.link_type})`;
        anchor.rel = "noopener noreferrer";
        item.appendChild(anchor);
        links.appendChild(item);
      });
    } catch (err) {
      console.error(err);
      if (errorPanel) errorPanel.hidden = false;
    }
  }

  window.WISE_SPECIES = { load };
})();
