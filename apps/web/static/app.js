/** RC11 static public beta renderer. */

(function () {
  const app = () => document.getElementById("app");

  async function loadJson(path) {
    const response = await fetch(path);
    if (!response.ok) throw new Error(`Unable to load ${path}`);
    return response.json();
  }

  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text) node.textContent = text;
    return node;
  }

  function metric(label, value) {
    return el("span", "metric", `${label}: ${value}`);
  }

  function card(title, body) {
    const article = el("article", "card");
    article.tabIndex = 0;
    const heading = el("h3", "", title);
    const paragraph = el("p", "", body);
    article.append(heading, paragraph);
    return article;
  }

  function hero(eyebrow, title, subtitle) {
    const section = el("section", "hero");
    section.append(el("p", "eyebrow", eyebrow), el("h1", "", title), el("p", "subtitle", subtitle));
    return section;
  }

  function grid(items) {
    const section = el("section", "grid");
    items.forEach((item) => section.appendChild(item));
    return section;
  }

  function renderSearch(allItems) {
    const form = el("form", "search-form");
    const input = document.createElement("input");
    input.type = "search";
    input.name = "q";
    input.placeholder = "Search collections, series, products";
    input.setAttribute("aria-label", "Search collections, series, products");
    const button = el("button", "button primary", "Search");
    button.type = "submit";
    const status = el("p", "muted");
    status.setAttribute("role", "status");
    status.setAttribute("aria-live", "polite");
    form.append(input, button, status);
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const query = input.value.trim();
      const results = allItems.filter((item) =>
        JSON.stringify(item).toLowerCase().includes(query.toLowerCase())
      );
      status.textContent = query ? `${results.length} prototype results for "${query}"` : "Enter a search term.";
      window.NC_ANALYTICS.track("search", {
        entity_type: "search",
        search_query: "",
        metadata: {
          result_count: results.length,
          query_length: query.length,
          zero_results: query.length > 0 && results.length === 0,
          query_redacted: true,
        },
      });
    });
    return form;
  }

  function collectionCard(collection) {
    const article = card(collection.title, `${collection.domain} / ${collection.theme} / ${collection.country}`);
    article.append(
      metric("Region", collection.geography_region),
      metric("Education", `${Math.round(collection.educational_value_score * 100)}%`),
      metric("Product potential", `${Math.round(collection.product_potential_score * 100)}%`)
    );
    article.addEventListener("mouseenter", () => {
      window.NC_ANALYTICS.track("collection_view", {
        entity_type: "collection",
        entity_id: collection.collection_id,
        entity_title: collection.title,
        collection_id: collection.collection_id,
        metadata: {
          geography_region: collection.geography_region,
          domain: collection.domain,
          theme: collection.theme,
        },
      });
    }, { once: true });
    article.addEventListener("focusin", () => {
      window.NC_ANALYTICS.track("collection_view", {
        entity_type: "collection",
        entity_id: collection.collection_id,
        entity_title: collection.title,
        collection_id: collection.collection_id,
        metadata: {
          geography_region: collection.geography_region,
          domain: collection.domain,
          theme: collection.theme,
          source_component: "keyboard_focus",
        },
      });
    }, { once: true });
    return article;
  }

  function seriesCard(series) {
    const article = card(series.title, series.educational_narrative);
    article.append(metric("Theme", series.theme), metric("Level", series.education_level));
    article.addEventListener("mouseenter", () => {
      window.NC_ANALYTICS.track("series_view", {
        entity_type: "series",
        entity_id: series.series_id,
        entity_title: series.title,
        series_id: series.series_id,
        metadata: {
          education_level: series.education_level,
          narrative_theme: series.theme,
        },
      });
    }, { once: true });
    article.addEventListener("focusin", () => {
      window.NC_ANALYTICS.track("series_view", {
        entity_type: "series",
        entity_id: series.series_id,
        entity_title: series.title,
        series_id: series.series_id,
        metadata: {
          education_level: series.education_level,
          narrative_theme: series.theme,
          source_component: "keyboard_focus",
        },
      });
    }, { once: true });
    return article;
  }

  function productCard(product) {
    const article = card(product.title, product.demand_rationale);
    article.append(
      metric("Category", product.category),
      metric("Demand", `${Math.round(product.demand_score * 100)}%`),
      metric("Commercial", `${Math.round(product.commercial_score * 100)}%`)
    );

    const actions = el("div");
    const view = el("button", "button", "Product View");
    const wishlist = el("button", "button", "Wishlist");
    const buy = el("button", "button primary", "Buy Intent");
    view.setAttribute("aria-label", `Record product view for ${product.title}`);
    wishlist.setAttribute("aria-label", `Record wishlist interest for ${product.title}`);
    buy.setAttribute("aria-label", `Record buy intent for ${product.title}`);
    [view, wishlist, buy].forEach((button) => {
      button.type = "button";
      actions.appendChild(button);
    });
    view.addEventListener("click", () => trackProduct("product_view", product));
    wishlist.addEventListener("click", () => trackProduct("wishlist", product));
    buy.addEventListener("click", () => trackProduct("buy_intent", product));
    article.appendChild(actions);
    return article;
  }

  function bigCatsAssetCard(asset) {
    const article = card(asset.common_name, asset.display_note);
    article.id = asset.common_name.toLowerCase();
    article.append(
      metric("Rights", asset.rights_status),
      metric("License", asset.license_name),
      metric("Approval", asset.approval_status)
    );

    const source = el("p", "muted", `Source: ${asset.source_authority}`);
    const credit = el("p", "muted", asset.required_credit_line);
    article.append(source, credit);
    return article;
  }

  function renderBigCatsCollection(collection) {
    const fragment = document.createDocumentFragment();
    fragment.appendChild(hero(
      "Rights-gated public collection",
      collection.title,
      collection.summary
    ));

    const notice = el("section", "panel");
    notice.append(
      el("h2", "", "Demonstration notice"),
      el("p", "", collection.notice),
      el("p", "", collection.product_cta)
    );
    fragment.appendChild(notice);

    const speciesNav = el("section", "panel");
    speciesNav.appendChild(el("h2", "", "Species detail links"));
    const list = el("ul");
    collection.species_links.forEach((link) => {
      const item = el("li");
      const anchor = el("a", "", link.label);
      anchor.href = link.href;
      item.appendChild(anchor);
      list.appendChild(item);
    });
    speciesNav.appendChild(list);
    fragment.appendChild(speciesNav);

    const rights = el("section", "panel");
    rights.append(
      el("h2", "", "Rights and attribution"),
      el("p", "", "Only approved non-restricted RC17 assets are displayed. Restricted or Unknown rights assets are excluded from this public collection.")
    );
    fragment.appendChild(rights);
    fragment.appendChild(grid(collection.assets.map(bigCatsAssetCard)));

    const education = el("section", "panel");
    education.append(el("h2", "", collection.education.title), el("p", "", collection.education.body));
    fragment.appendChild(education);
    return fragment;
  }

  function trackProduct(eventName, product) {
    window.NC_ANALYTICS.track(eventName, {
      entity_type: "product",
      entity_id: product.product_id,
      entity_title: product.title,
      collection_id: product.collection_id,
      product_category: product.category,
      metadata: {
        commercial_score: product.commercial_score,
        product_fit_score: product.commercial_score,
        source_component: "showcase_product_card",
        price_placeholder_visible: true,
      },
    });
  }

  function analyticsDashboard() {
    const events = window.NC_ANALYTICS.events();
    const byName = events.reduce((acc, event) => {
      acc[event.event_name] = (acc[event.event_name] || 0) + 1;
      return acc;
    }, {});
    const topProducts = events
      .filter((event) => ["product_view", "wishlist", "buy_intent"].includes(event.event_name))
      .reduce((acc, event) => {
        const key = event.entity_title || event.entity_id || "Unknown product";
        acc[key] = acc[key] || { title: key, product_view: 0, wishlist: 0, buy_intent: 0 };
        acc[key][event.event_name] += 1;
        return acc;
      }, {});

    const section = document.createDocumentFragment();
    section.appendChild(hero("Admin Analytics", "Audience Validation Dashboard", "Browser-local RC10 analytics events for public beta route and product validation."));
    section.appendChild(grid(window.NC_ANALYTICS.eventNames.map((name) => card(name, `${byName[name] || 0} events`))));
    const list = el("ol", "analytics-list");
    Object.values(topProducts)
      .sort((a, b) => b.buy_intent + b.wishlist + b.product_view - (a.buy_intent + a.wishlist + a.product_view))
      .slice(0, 10)
      .forEach((product) => {
        const item = el("li", "analytics-row");
        item.append(
          el("span", "", product.title),
          el("strong", "", `${product.product_view} views / ${product.wishlist} wishlist / ${product.buy_intent} buy intent`)
        );
        list.appendChild(item);
      });
    const panel = el("section", "panel");
    panel.append(el("h2", "", "Top product interest"), list);
    section.appendChild(panel);
    return section;
  }

  async function render() {
    const page = document.body.dataset.page;
    const root = app();
    root.innerHTML = "";
    root.setAttribute("aria-busy", "true");

    window.NC_ANALYTICS.track("page_view", {
      entity_type: "page",
      entity_title: document.title,
      metadata: {
        route_group: page,
        is_landing_page: page === "home",
      },
    });

    if (page === "analytics") {
      root.appendChild(analyticsDashboard());
      root.setAttribute("aria-busy", "false");
      return;
    }

    if (page === "big-cats-collection") {
      const collection = await loadJson("/data/big_cats_public_collection.json");
      root.appendChild(renderBigCatsCollection(collection));
      window.NC_ANALYTICS.track("collection_view", {
        entity_type: "collection",
        entity_id: collection.collection_id,
        entity_title: collection.title,
        collection_id: collection.collection_id,
        metadata: {
          rights_gated: true,
          displayed_asset_count: collection.assets.length,
        },
      });
      root.setAttribute("aria-busy", "false");
      return;
    }

    const [collections, series, products] = await Promise.all([
      loadJson("/data/top_25_showcase_collections.json"),
      loadJson("/data/top_25_showcase_series.json"),
      loadJson("/data/top_25_showcase_products.json"),
    ]);

    root.appendChild(renderSearch([...collections, ...series, ...products]));

    if (page === "home") {
      root.prepend(hero(
        "Public Beta",
        "Permanent digital memory of humanity's heritage, nature, and culture.",
        "Explore showcase collections, educational series, species, places, research, and read-only product validation."
      ));
      root.append(
        grid([
          card("Collections", "Top 25 public beta collections selected for global representation and educational value."),
          card("Series", "Narrative series connect collections and assets through educational storytelling."),
          card("Shop", "Read-only product validation measures wishlist and buy intent without payment processing."),
        ])
      );
      root.setAttribute("aria-busy", "false");
      return;
    }

    if (page === "collections") {
      root.prepend(hero("Collections", "Top 25 Showcase Collections", "Selected from the Top 100 for visual appeal, educational value, global representation, and product potential."));
      root.appendChild(grid(collections.map(collectionCard)));
      root.setAttribute("aria-busy", "false");
      return;
    }

    if (page === "series") {
      root.prepend(hero("Series", "Top 25 Showcase Series", "Educational narratives that connect collections and assets."));
      root.appendChild(grid(series.map(seriesCard)));
      root.setAttribute("aria-busy", "false");
      return;
    }

    if (page === "shop") {
      root.prepend(hero("Shop", "Top 25 Showcase Products", "Read-only validation for product interest. No checkout, payment, or fulfillment."));
      root.appendChild(grid(products.map(productCard)));
      root.setAttribute("aria-busy", "false");
      return;
    }

    if (page === "species") {
      root.prepend(hero("Species", "Flagship Species", "Explore species-led collections and conservation narratives."));
      root.appendChild(grid(collections.filter((item) => item.domain === "Nature").map(collectionCard)));
      root.setAttribute("aria-busy", "false");
      return;
    }

    if (page === "places") {
      root.prepend(hero("Places", "Explore by Place", "Heritage, maps, landscapes, and regional memory across the public beta portfolio."));
      root.appendChild(grid(collections.filter((item) => ["Heritage", "History"].includes(item.domain)).map(collectionCard)));
      root.setAttribute("aria-busy", "false");
      return;
    }

    if (page === "education") {
      root.prepend(hero("Education", "Learning from Collections", "Series, cards, puzzles, and classroom-ready narratives for source-aware learning."));
      root.appendChild(grid(series.slice(0, 12).map(seriesCard)));
      root.setAttribute("aria-busy", "false");
      return;
    }

    if (page === "research") {
      root.prepend(hero("Research", "Source-aware public memory", "Research readiness centers attribution, provenance, open collections, and audience validation."));
      root.appendChild(grid([
        card("Analytics schema", "page_view, collection_view, series_view, product_view, wishlist, buy_intent, outbound_click, search, session_duration."),
        card("Portfolio data", "Showcase datasets are derived from Top 100 collections, series, assets, and Top 50 products."),
        card("Outbound sources", "Outbound clicks are tracked by domain only for privacy-conscious source follow-through."),
      ]));
      root.setAttribute("aria-busy", "false");
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    render().catch((err) => {
      console.error(err);
      const root = app();
      if (root) {
        root.textContent = "Unable to load public beta data.";
      }
    });
  });
})();
