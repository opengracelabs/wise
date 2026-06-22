/** Reference Capability 1 public object page loader. */

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
      const response = await fetch(`/v1/objects/${stableId}`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();

      document.title = `${data.title} — WISE Reference Capability 1`;
      text("object-title", data.title);
      text("object-subtitle", data.metadata.description || data.discovery.description);
      text("object-description", data.discovery.description);
      text("unesco-id", data.discovery.external_identifiers.unesco_whc);
      text("wikidata-id", data.discovery.external_identifiers.wikidata);
      text("object-ark", data.preservation.ark);
      text("rights-status", data.discovery.rights_uri);
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
        anchor.href =
          link.external_authority === "wikidata"
            ? `https://www.wikidata.org/wiki/${link.external_identifier}`
            : "#";
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

  window.WISE_OBJECT = { load };
})();
