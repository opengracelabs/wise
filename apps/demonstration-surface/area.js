/** Reference Capability 3 protected area page loader with Leaflet map. */

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

  function renderMap(boundaryGeojson, label) {
    const mapEl = document.getElementById("area-map");
    if (!mapEl || typeof L === "undefined" || !boundaryGeojson) return;

    const map = L.map(mapEl, { scrollWheelZoom: false });
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      maxZoom: 18,
    }).addTo(map);

    const layer = L.geoJSON(boundaryGeojson, {
      style: {
        color: "#1f4d3a",
        weight: 2,
        fillOpacity: 0.25,
      },
    }).addTo(map);

    map.fitBounds(layer.getBounds(), { padding: [16, 16] });
    layer.bindPopup(label);
    mapEl.setAttribute("aria-label", `Map showing boundary of ${label}`);
  }

  async function load(stableId) {
    const errorPanel = document.getElementById("load-error");
    try {
      const [areaResponse, mapResponse] = await Promise.all([
        fetch(`/v1/areas/${stableId}`),
        fetch(`/v1/map/areas/${stableId}`),
      ]);
      if (!areaResponse.ok) throw new Error(`HTTP ${areaResponse.status}`);
      const data = await areaResponse.json();
      const mapData = mapResponse.ok ? await mapResponse.json() : data.protected_area;

      document.title = `${data.title} — WISE Reference Capability 3`;
      text("area-title", data.title);
      text("area-subtitle", data.metadata.description || data.discovery.description);
      text("area-description", data.discovery.description);
      text("ramsar-id", data.discovery.external_identifiers.ramsar);
      text("wikidata-id", data.discovery.external_identifiers.wikidata);
      text("unesco-id", data.discovery.external_identifiers.unesco_whc);
      text("geonames-id", data.discovery.external_identifiers.geonames);
      text("object-ark", data.preservation.ark);
      text("rights-status", data.discovery.rights_uri);
      text("iucn-category", data.protected_area.conservation_metadata.iucn_category);
      text("designation-type", data.protected_area.designation_type);
      text("area-hectares", data.protected_area.conservation_metadata.area_hectares?.toLocaleString());
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
      setBadge(
        document.getElementById("geospatial-badge"),
        "Geospatial",
        data.geospatial_indexed
      );

      const chain = document.getElementById("provenance-chain");
      chain.innerHTML = "";
      data.provenance_chain.forEach((eventId) => {
        const item = document.createElement("li");
        item.textContent = eventId;
        chain.appendChild(item);
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

      renderMap(
        mapData.boundary_geojson || data.protected_area.boundary_geojson,
        data.title
      );
    } catch (err) {
      console.error(err);
      if (errorPanel) errorPanel.hidden = false;
    }
  }

  window.WISE_AREA = { load };
})();
