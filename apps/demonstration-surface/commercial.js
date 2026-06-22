/** Reference Capability 6 read-only commercial validation surface. */

(function () {
  const STORAGE_KEY = "wise.rc6.commercial.events";
  const ALLOWED_EVENTS = new Set([
    "product_view",
    "add_to_wishlist",
    "buy_interest",
    "checkout_intent",
  ]);

  const collection = {
    id: "rc4-big-cats-of-the-world",
    title: "Big Cats of the World",
    subtitle: "RC4 collection commercial validation",
    rightsNote:
      "Read-only validation surface using cleared demonstration metadata. No payment processing or fulfillment.",
    curatorialNote:
      "Product concepts follow museum-store and conservation-magazine merchandising patterns: field-note storytelling, specimen-label clarity, education-forward copy, and conservation context.",
  };

  const products = [
    {
      slug: "big-cats-poster",
      type: "Poster",
      title: "Big Cats of the World Field Poster",
      pricePlaceholder: "Price TBD",
      format: "Archival matte poster concept",
      dimensions: "24 x 36 in validation format",
      deck:
        "A field-guide wall print pairing silhouettes, ranges, and conservation status for the world's big cats.",
      detail:
        "Designed like a museum exhibition takeaway: clear taxonomy, range cues, and a restrained conservation palette suitable for classrooms, visitor centers, and home study spaces.",
      merchandisingPattern: "Smithsonian-style educational wall chart with National Geographic field context.",
      audience: "Families, educators, and natural history visitors",
      conservationCue: "Highlights habitat pressure and species diversity without implying commercial exploitation.",
    },
    {
      slug: "big-cats-framed-print",
      type: "Framed Print",
      title: "Panthera Portrait Framed Print",
      pricePlaceholder: "Price TBD",
      format: "Museum-framed print concept",
      dimensions: "18 x 24 in framed validation format",
      deck:
        "A gallery-style big-cat portrait treatment with captioning modeled on institutional object labels.",
      detail:
        "The concept tests appetite for premium decor that still reads as educational: title block, collection source, species context, and restrained archival framing.",
      merchandisingPattern: "Museum store premium print with editorial caption and provenance panel.",
      audience: "Collectors, members, and design-led supporters",
      conservationCue: "Positions decor as a prompt for species literacy and habitat stewardship.",
    },
    {
      slug: "big-cats-puzzle",
      type: "Puzzle",
      title: "Big Cats Range Map Puzzle",
      pricePlaceholder: "Price TBD",
      format: "Family puzzle concept",
      dimensions: "500-piece validation format",
      deck:
        "A tactile range-map puzzle that turns geography, species recognition, and conservation status into a family activity.",
      detail:
        "Built around the education-through-play pattern common to museum shops: a durable object, a reference insert, and repeated engagement with species geography.",
      merchandisingPattern: "Hands-on museum learning product with magazine-quality map storytelling.",
      audience: "Families, classrooms, and gift buyers",
      conservationCue: "Connects play with habitat ranges and threatened ecosystems.",
    },
    {
      slug: "big-cats-calendar",
      type: "Calendar",
      title: "Twelve Months of Big Cats Calendar",
      pricePlaceholder: "Price TBD",
      format: "Editorial wall calendar concept",
      dimensions: "12-month validation format",
      deck:
        "A month-by-month editorial journey through big-cat habitats, field notes, and stewardship prompts.",
      detail:
        "Tests recurring engagement with the collection through short captions, seasonal field themes, and calls to learn more rather than calls to transact.",
      merchandisingPattern: "National Geographic-style monthly story cadence with institutional source notes.",
      audience: "Members, subscribers, and seasonal gift shoppers",
      conservationCue: "Each month frames a habitat or conservation challenge for continued learning.",
    },
    {
      slug: "big-cats-coffee-table-book",
      type: "Coffee Table Book",
      title: "Big Cats of the World Coffee Table Book",
      pricePlaceholder: "Price TBD",
      format: "Large-format editorial book concept",
      dimensions: "Prototype chapter architecture",
      deck:
        "A premium book concept combining collection essays, species profiles, conservation maps, and visual storytelling.",
      detail:
        "The highest-commitment product concept for validating whether the RC4 collection can support a long-form retail artifact with museum authority and magazine pacing.",
      merchandisingPattern: "Institutional exhibition catalog meets conservation photo essay.",
      audience: "Patrons, collectors, libraries, and conservation supporters",
      conservationCue: "Prioritizes literacy, stewardship, and source transparency over sales conversion.",
    },
  ];

  function getProduct(slug) {
    return products.find((product) => product.slug === slug);
  }

  function readEvents() {
    try {
      const raw = window.localStorage.getItem(STORAGE_KEY);
      const events = raw ? JSON.parse(raw) : [];
      return Array.isArray(events) ? events : [];
    } catch (err) {
      console.warn("Unable to read RC6 commercial analytics", err);
      return [];
    }
  }

  function writeEvents(events) {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(events.slice(-500)));
  }

  function trackDemand(eventType, productSlug, source) {
    if (!ALLOWED_EVENTS.has(eventType)) {
      throw new Error(`Unsupported RC6 commercial event: ${eventType}`);
    }

    const product = getProduct(productSlug);
    if (!product) {
      throw new Error(`Unknown RC6 commercial product: ${productSlug}`);
    }

    const event = {
      id:
        window.crypto && typeof window.crypto.randomUUID === "function"
          ? window.crypto.randomUUID()
          : `${Date.now()}-${Math.random().toString(16).slice(2)}`,
      event_type: eventType,
      product_slug: product.slug,
      product_type: product.type,
      collection_id: collection.id,
      collection_title: collection.title,
      source: source || "commercial_surface",
      occurred_at: new Date().toISOString(),
    };

    const events = readEvents();
    events.push(event);
    writeEvents(events);
    window.dispatchEvent(new CustomEvent("wise:commercial-demand", { detail: event }));
    return event;
  }

  function setStatus(message) {
    const status = document.getElementById("commercial-action-status");
    if (status) {
      status.textContent = message;
    }
  }

  function text(id, value) {
    const element = document.getElementById(id);
    if (element) {
      element.textContent = value;
    }
  }

  function createElement(tagName, className, textContent) {
    const element = document.createElement(tagName);
    if (className) {
      element.className = className;
    }
    if (textContent) {
      element.textContent = textContent;
    }
    return element;
  }

  function createActionButton(label, eventType, product, source) {
    const button = createElement("button", "button secondary", label);
    button.type = "button";
    button.addEventListener("click", () => {
      trackDemand(eventType, product.slug, source);
      if (eventType === "buy_interest") {
        trackDemand("checkout_intent", product.slug, source);
        setStatus(
          `Recorded buy_interest and checkout_intent for ${product.type}. No checkout or payment was started.`
        );
      } else {
        setStatus(`Recorded ${eventType} for ${product.type}.`);
      }
    });
    return button;
  }

  function renderProductCards() {
    const grid = document.getElementById("product-grid");
    if (!grid) {
      return;
    }

    grid.innerHTML = "";
    products.forEach((product) => {
      const card = createElement("article", "product-card");
      card.setAttribute("aria-labelledby", `${product.slug}-title`);

      const label = createElement("p", "eyebrow", product.type);
      const title = createElement("h2", "", product.title);
      title.id = `${product.slug}-title`;
      const deck = createElement("p", "", product.deck);
      const price = createElement("p", "price-placeholder", product.pricePlaceholder);
      const pattern = createElement("p", "commercial-note", product.merchandisingPattern);

      const details = createElement("a", "button", "View details");
      details.href = `/shop/products/${product.slug}`;
      details.addEventListener("click", () => {
        trackDemand("product_view", product.slug, "shop_card_detail_link");
      });

      const actions = createElement("div", "product-actions");
      actions.append(
        details,
        createActionButton("Add to Wishlist", "add_to_wishlist", product, "shop_card"),
        createActionButton("Buy Interest", "buy_interest", product, "shop_card")
      );

      card.append(label, title, deck, price, pattern, actions);
      grid.appendChild(card);
    });
  }

  function renderProductDetail(slug) {
    const product = getProduct(slug);
    if (!product) {
      const panel = document.getElementById("load-error");
      if (panel) {
        panel.hidden = false;
      }
      return;
    }

    document.title = `${product.title} — RC6 Commercial Validation Surface`;
    text("product-type", product.type);
    text("product-title", product.title);
    text("product-deck", product.deck);
    text("product-price", product.pricePlaceholder);
    text("product-format", product.format);
    text("product-dimensions", product.dimensions);
    text("product-detail", product.detail);
    text("product-pattern", product.merchandisingPattern);
    text("product-audience", product.audience);
    text("product-conservation", product.conservationCue);
    text("collection-title", collection.title);
    text("collection-note", collection.curatorialNote);

    const actions = document.getElementById("product-detail-actions");
    if (actions) {
      actions.innerHTML = "";
      actions.append(
        createActionButton("Add to Wishlist", "add_to_wishlist", product, "product_detail"),
        createActionButton("Buy Interest", "buy_interest", product, "product_detail")
      );
    }

    trackDemand("product_view", product.slug, "product_detail");
  }

  function productStats() {
    const stats = products.map((product) => ({
      ...product,
      product_view: 0,
      add_to_wishlist: 0,
      buy_interest: 0,
      checkout_intent: 0,
      wishlist_rate: 0,
    }));
    const bySlug = new Map(stats.map((product) => [product.slug, product]));

    readEvents().forEach((event) => {
      const product = bySlug.get(event.product_slug);
      if (!product || !ALLOWED_EVENTS.has(event.event_type)) {
        return;
      }
      product[event.event_type] += 1;
    });

    stats.forEach((product) => {
      product.wishlist_rate =
        product.product_view > 0 ? product.add_to_wishlist / product.product_view : 0;
    });

    return stats;
  }

  function renderRanking(targetId, rows, metric, formatter) {
    const target = document.getElementById(targetId);
    if (!target) {
      return;
    }

    target.innerHTML = "";
    rows.slice(0, 5).forEach((product, index) => {
      const item = createElement("li", "analytics-row");
      const label = createElement(
        "span",
        "",
        `${index + 1}. ${product.type}: ${product.title}`
      );
      const value = createElement("strong", "", formatter(product[metric], product));
      item.append(label, value);
      target.appendChild(item);
    });
  }

  function renderDashboard() {
    const events = readEvents();
    const stats = productStats();
    text("analytics-event-count", events.length.toLocaleString());
    text("analytics-last-updated", events.length ? events[events.length - 1].occurred_at : "No events yet");

    renderRanking(
      "most-viewed-products",
      [...stats].sort((a, b) => b.product_view - a.product_view),
      "product_view",
      (value) => `${value} views`
    );
    renderRanking(
      "highest-buy-intent",
      [...stats].sort((a, b) => b.buy_interest - a.buy_interest),
      "buy_interest",
      (value, product) => `${value} buy interest / ${product.checkout_intent} checkout intent`
    );
    renderRanking(
      "highest-wishlist-rate",
      [...stats].sort((a, b) => b.wishlist_rate - a.wishlist_rate),
      "wishlist_rate",
      (value, product) =>
        `${Math.round(value * 100)}% (${product.add_to_wishlist}/${product.product_view} views)`
    );
  }

  function initialize() {
    renderProductCards();

    const productSlug = document.body.dataset.productSlug;
    if (productSlug) {
      renderProductDetail(productSlug);
    }

    if (document.getElementById("commercial-dashboard")) {
      renderDashboard();
      window.addEventListener("storage", renderDashboard);
      window.addEventListener("wise:commercial-demand", renderDashboard);
    }
  }

  window.WISE_COMMERCIAL = {
    collection,
    products,
    readEvents,
    productStats,
    trackDemand,
  };

  document.addEventListener("DOMContentLoaded", initialize);
})();
