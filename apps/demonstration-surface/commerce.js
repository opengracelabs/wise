/** RC7 Commerce & Distribution Prototype page loaders. */

(function () {
  function text(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value ?? "—";
  }

  function formatPercent(value) {
    return `${Math.round((value || 0) * 100)}%`;
  }

  async function fetchJson(path) {
    const response = await fetch(path);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  }

  function renderProductCards(products) {
    const list = document.getElementById("product-list");
    if (!list) return;
    list.innerHTML = "";

    products.forEach((product) => {
      const item = document.createElement("article");
      item.className = "card product-card";

      const title = document.createElement("h3");
      title.textContent = product.title;

      const meta = document.createElement("p");
      meta.className = "eyebrow";
      meta.textContent = `${product.category} · ${product.collection}`;

      const description = document.createElement("p");
      description.textContent = product.description;

      const signals = document.createElement("ul");
      signals.className = "compact-list";
      product.intelligence_signals.forEach((signal) => {
        const signalItem = document.createElement("li");
        signalItem.textContent = `${signal.layer}: ${formatPercent(signal.score)} — ${signal.summary}`;
        signals.appendChild(signalItem);
      });

      const badge = document.createElement("span");
      badge.className = "badge pass";
      badge.textContent = product.payment_processing_enabled
        ? "Payments enabled"
        : "Validation only · no payments";

      item.append(meta, title, description, signals, badge);
      list.appendChild(item);
    });
  }

  function renderProviders(providers) {
    const list = document.getElementById("provider-list");
    if (!list) return;
    list.innerHTML = "";

    providers.forEach((provider) => {
      const item = document.createElement("article");
      item.className = "card";
      item.innerHTML = `
        <p class="eyebrow">${provider.provider}</p>
        <h3>${provider.display_name}</h3>
        <p>${provider.role}</p>
        <p><strong>Status:</strong> ${provider.status}</p>
        <p><strong>Disabled:</strong> ${provider.disabled_capabilities.join(", ")}</p>
      `;
      list.appendChild(item);
    });
  }

  function renderPipeline(stages) {
    const list = document.getElementById("pipeline-list");
    if (!list) return;
    list.innerHTML = "";

    stages.forEach((stage, index) => {
      const item = document.createElement("li");
      item.className = "pipeline-step";
      item.innerHTML = `
        <span class="step-number">${index + 1}</span>
        <div>
          <h3>${stage.label}</h3>
          <p>${stage.description}</p>
          <p><strong>Gate:</strong> ${stage.governance_gate}</p>
        </div>
      `;
      list.appendChild(item);
    });
  }

  function renderPinterestAssets(assets) {
    const list = document.getElementById("asset-list");
    if (!list) return;
    list.innerHTML = "";

    assets.forEach((asset) => {
      const item = document.createElement("article");
      item.className = "card asset-card";
      item.innerHTML = `
        <p class="eyebrow">${asset.asset_type} · ${asset.size_px}</p>
        <h3>${asset.title}</h3>
        <p>${asset.alt_text}</p>
        <p><strong>Target:</strong> ${asset.target_url}</p>
      `;
      list.appendChild(item);
    });
  }

  async function loadShop(category) {
    try {
      const prototype = await fetchJson("/v1/commerce/prototype");
      const path = category ? `/v1/commerce/catalog/${category}` : "/v1/commerce/catalog";
      const products = await fetchJson(path);

      document.title = category
        ? `${category} — RC7 Commerce & Distribution Prototype`
        : "Shop — RC7 Commerce & Distribution Prototype";
      text("page-title", category ? `Shop ${category}` : "Shop");
      text("product-count", `${products.length} validation products`);
      text("prototype-name", prototype.name);
      text("youtube-route", prototype.youtube_promo_route);
      renderProductCards(products);
      renderProviders(prototype.providers);
      renderPipeline(prototype.promotion_pipeline);
      renderPinterestAssets(prototype.pinterest_assets);
    } catch (err) {
      console.error(err);
      const errorPanel = document.getElementById("load-error");
      if (errorPanel) errorPanel.hidden = false;
    }
  }

  async function loadMarketingDashboard() {
    try {
      const dashboard = await fetchJson("/v1/commerce/marketing-dashboard");
      text("pinterest-clicks", dashboard.pinterest_clicks);
      text("product-views", dashboard.product_views);
      text("wishlist-rate", formatPercent(dashboard.wishlist_rate));
      text("buy-intent", formatPercent(dashboard.buy_intent));
      text("conversion-estimate", formatPercent(dashboard.conversion_estimate));

      const surfaces = document.getElementById("tracked-surfaces");
      if (surfaces) {
        surfaces.innerHTML = "";
        dashboard.tracked_surfaces.forEach((surface) => {
          const item = document.createElement("li");
          item.textContent = surface;
          surfaces.appendChild(item);
        });
      }
    } catch (err) {
      console.error(err);
      const errorPanel = document.getElementById("load-error");
      if (errorPanel) errorPanel.hidden = false;
    }
  }

  async function loadYoutubePromo() {
    try {
      const pipeline = await fetchJson("/v1/commerce/promotion-pipeline");
      const assets = await fetchJson("/v1/commerce/pinterest-assets");
      renderPipeline(pipeline);
      renderPinterestAssets(assets);
    } catch (err) {
      console.error(err);
      const errorPanel = document.getElementById("load-error");
      if (errorPanel) errorPanel.hidden = false;
    }
  }

  window.WISE_COMMERCE = {
    loadMarketingDashboard,
    loadShop,
    loadYoutubePromo,
  };
})();
