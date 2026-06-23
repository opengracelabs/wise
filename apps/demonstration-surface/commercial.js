/** Reference Capability 7 commercial product intelligence surface. */

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
    subtitle: "RC4 collection commercial validation with RC7 product intelligence",
    rightsNote:
      "Read-only validation surface using cleared demonstration metadata. No payment processing or fulfillment.",
    curatorialNote:
      "Product concepts follow museum-store and conservation-magazine merchandising patterns: field-note storytelling, specimen-label clarity, education-forward copy, and conservation context.",
  };

  const products = [
    {
      slug: "big-cats-poster",
      type: "Poster",
      productCategory: "Poster",
      collectionTitle: "Big Cats Collection",
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
      product_category_score: 0.92,
      product_fit_score: 0.91,
      estimated_giftability: 0.88,
      estimated_repeat_purchase: 0.42,
      routeGroup: "gifts",
      featured: true,
    },
    {
      slug: "big-cats-framed-print",
      type: "Framed Print",
      productCategory: "Framed Print",
      collectionTitle: "Big Cats Collection",
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
      product_category_score: 0.9,
      product_fit_score: 0.86,
      estimated_giftability: 0.84,
      estimated_repeat_purchase: 0.36,
      routeGroup: "gifts",
      featured: true,
    },
    {
      slug: "big-cats-canvas",
      type: "Canvas",
      productCategory: "Canvas Prints",
      collectionTitle: "Big Cats Collection",
      title: "Big Cats Habitat Canvas",
      pricePlaceholder: "Price TBD",
      format: "Gallery-wrap canvas print concept",
      dimensions: "30 x 40 in validation format",
      deck:
        "A habitat-led canvas concept pairing big-cat presence with the landscape systems that sustain them.",
      detail:
        "Tests large-format decor demand for a conservation-first image treatment, balancing premium giftability with education-forward copy.",
      merchandisingPattern: "National Geographic habitat storytelling translated into museum-store decor.",
      audience: "Members, conservation supporters, and premium gift buyers",
      conservationCue: "Frames species protection through habitats, not isolated trophy imagery.",
      product_category_score: 0.88,
      product_fit_score: 0.89,
      estimated_giftability: 0.86,
      estimated_repeat_purchase: 0.34,
      routeGroup: "gifts",
      featured: true,
    },
    {
      slug: "big-cats-metal-print",
      type: "Metal Print",
      productCategory: "Metal Prints",
      collectionTitle: "Big Cats Collection",
      title: "Big Cats Conservation Metal Print",
      pricePlaceholder: "Price TBD",
      format: "Satin metal print concept",
      dimensions: "16 x 24 in validation format",
      deck:
        "A durable metal print concept for dramatic big-cat imagery with concise conservation labeling.",
      detail:
        "Tests appetite for contemporary premium materials while keeping the product grounded in species literacy and habitat context.",
      merchandisingPattern: "Museum store premium wall decor with National Geographic visual intensity.",
      audience: "Premium gift buyers, members, and contemporary decor shoppers",
      conservationCue: "Connects visual impact with habitat and species status rather than spectacle.",
      product_category_score: 0.87,
      product_fit_score: 0.85,
      estimated_giftability: 0.83,
      estimated_repeat_purchase: 0.31,
      routeGroup: "gifts",
    },
    {
      slug: "big-cats-puzzle",
      type: "Puzzle",
      productCategory: "Puzzle",
      collectionTitle: "Big Cats Collection",
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
      product_category_score: 0.84,
      product_fit_score: 0.82,
      estimated_giftability: 0.78,
      estimated_repeat_purchase: 0.57,
      routeGroup: "gifts",
      featured: true,
    },
    {
      slug: "big-cats-calendar",
      type: "Calendar",
      productCategory: "Calendar",
      collectionTitle: "Big Cats Collection",
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
      product_category_score: 0.78,
      product_fit_score: 0.74,
      estimated_giftability: 0.82,
      estimated_repeat_purchase: 0.65,
      routeGroup: "gifts",
      featured: true,
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
      productCategory: "Coffee Table Book",
      collectionTitle: "Big Cats Collection",
      product_category_score: 0.86,
      product_fit_score: 0.84,
      estimated_giftability: 0.92,
      estimated_repeat_purchase: 0.29,
      routeGroup: "gifts",
    },
    {
      slug: "world-heritage-museum-print",
      type: "Museum Print",
      productCategory: "Museum Prints",
      collectionTitle: "World Heritage Collection",
      title: "World Heritage Museum Print",
      pricePlaceholder: "Price TBD",
      format: "Institutional print concept",
      dimensions: "18 x 24 in validation format",
      deck:
        "A heritage-object print treatment with captioning inspired by exhibition labels and collection provenance.",
      detail:
        "Tests World Heritage display demand through museum-label clarity, site context, and restrained archival design.",
      merchandisingPattern: "British Museum object-label pattern with Europeana source transparency.",
      audience: "Cultural travelers, educators, and heritage supporters",
      conservationCue: "Connects cultural memory, preservation, and responsible site interpretation.",
      product_category_score: 0.91,
      product_fit_score: 0.87,
      estimated_giftability: 0.8,
      estimated_repeat_purchase: 0.32,
      routeGroup: "gifts",
      featured: true,
    },
    {
      slug: "world-heritage-historic-map",
      type: "Historic Map",
      productCategory: "Historic Maps",
      collectionTitle: "World Heritage Collection",
      title: "World Heritage Historic Map",
      pricePlaceholder: "Price TBD",
      format: "Historic map print concept",
      dimensions: "24 x 36 in validation format",
      deck:
        "A map-led exploration product showing place, memory, and routes through globally significant heritage sites.",
      detail:
        "Validates demand for geography-first cultural storytelling, pairing historic map aesthetics with modern source notes.",
      merchandisingPattern: "Europeana map discovery meets Google Arts & Culture place-based exploration.",
      audience: "Map collectors, cultural travelers, and classrooms",
      conservationCue: "Positions maps as a gateway to heritage stewardship and place literacy.",
      product_category_score: 0.89,
      product_fit_score: 0.88,
      estimated_giftability: 0.77,
      estimated_repeat_purchase: 0.38,
      routeGroup: "maps",
      featured: true,
    },
    {
      slug: "world-heritage-coffee-table-book",
      type: "Coffee Table Book",
      productCategory: "Coffee Table Book",
      collectionTitle: "World Heritage Collection",
      title: "World Heritage Coffee Table Book",
      pricePlaceholder: "Price TBD",
      format: "Large-format heritage book concept",
      dimensions: "Prototype chapter architecture",
      deck:
        "A premium editorial book concept joining heritage essays, maps, object records, and cultural context.",
      detail:
        "Tests whether World Heritage records can support a Smithsonian-style catalog with National Geographic pacing.",
      merchandisingPattern: "Exhibition catalog, travel atlas, and cultural memory volume.",
      audience: "Patrons, travelers, libraries, and cultural gift buyers",
      conservationCue: "Promotes responsible cultural memory and source-grounded interpretation.",
      product_category_score: 0.86,
      product_fit_score: 0.84,
      estimated_giftability: 0.92,
      estimated_repeat_purchase: 0.29,
      routeGroup: "gifts",
      featured: true,
    },
    {
      slug: "education-big-cats-card-set",
      type: "Educational Card Set",
      productCategory: "Educational Card Sets",
      collectionTitle: "Education Collection",
      title: "Big Cats Educational Card Set",
      pricePlaceholder: "Price TBD",
      format: "Classroom card set concept",
      dimensions: "48-card validation format",
      deck:
        "Species cards for taxonomy, range, behavior, and conservation vocabulary across the Big Cats collection.",
      detail:
        "A repeat-use educational product that fits classroom stations, museum carts, and family learning.",
      merchandisingPattern: "Smithsonian classroom extension with field-guide clarity.",
      audience: "Teachers, families, and museum educators",
      conservationCue: "Turns species facts into discussion prompts for stewardship.",
      product_category_score: 0.82,
      product_fit_score: 0.79,
      estimated_giftability: 0.7,
      estimated_repeat_purchase: 0.71,
      routeGroup: "education",
    },
    {
      slug: "education-discovery-pack",
      type: "Discovery Pack",
      productCategory: "Discovery Packs",
      collectionTitle: "Education Collection",
      title: "Nature & Culture Discovery Pack",
      pricePlaceholder: "Price TBD",
      format: "Activity bundle concept",
      dimensions: "Family activity validation format",
      deck:
        "A take-home discovery bundle combining collection prompts, mini maps, observation cards, and learning challenges.",
      detail:
        "Tests bundled family learning demand across nature and culture content without introducing fulfillment.",
      merchandisingPattern: "Museum family pack with Google Arts & Culture exploration cues.",
      audience: "Families, camps, and youth programs",
      conservationCue: "Encourages observation, place literacy, and source-aware curiosity.",
      product_category_score: 0.8,
      product_fit_score: 0.78,
      estimated_giftability: 0.75,
      estimated_repeat_purchase: 0.68,
      routeGroup: "education",
    },
    {
      slug: "education-paint-by-numbers",
      type: "Paint-by-Numbers",
      productCategory: "Paint-by-Numbers",
      collectionTitle: "Education Collection",
      title: "Big Cats Paint-by-Numbers",
      pricePlaceholder: "Price TBD",
      format: "Creative learning concept",
      dimensions: "12 x 16 in validation format",
      deck:
        "An accessible creative product that pairs big-cat imagery with color, habitat, and species notes.",
      detail:
        "Tests whether craft-led learning can broaden entry points into biodiversity collections.",
      merchandisingPattern: "Museum activity kit with natural history reference notes.",
      audience: "Families, youth programs, and casual gift buyers",
      conservationCue: "Uses creative engagement to introduce habitat and species literacy.",
      product_category_score: 0.74,
      product_fit_score: 0.7,
      estimated_giftability: 0.81,
      estimated_repeat_purchase: 0.52,
      routeGroup: "education",
    },
    {
      slug: "education-classroom-kit",
      type: "Classroom Kit",
      productCategory: "Classroom Kits",
      collectionTitle: "Education Collection",
      title: "Nature & Culture Classroom Kit",
      pricePlaceholder: "Price TBD",
      format: "Educator kit concept",
      dimensions: "Lesson bundle validation format",
      deck:
        "A classroom-ready kit for place, species, and theme exploration across Nature & Culture records.",
      detail:
        "Designed to validate educator demand for repeat-use materials built from preserved records and curated context.",
      merchandisingPattern: "Smithsonian education kit with Europeana source literacy.",
      audience: "Teachers, schools, libraries, and learning programs",
      conservationCue: "Links curriculum use with stewardship and cultural memory.",
      product_category_score: 0.85,
      product_fit_score: 0.83,
      estimated_giftability: 0.58,
      estimated_repeat_purchase: 0.76,
      routeGroup: "education",
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
      product_category: product.productCategory,
      collection_id: collection.id,
      collection_title: product.collectionTitle,
      product_fit_score: product.product_fit_score,
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

    const filter = document.body.dataset.shopFilter;
    const visibleProducts = filter
      ? products.filter((product) => product.routeGroup === filter)
      : products;

    grid.innerHTML = "";
    visibleProducts.forEach((product) => {
      const card = createElement("article", "product-card");
      card.setAttribute("aria-labelledby", `${product.slug}-title`);

      const label = createElement("p", "eyebrow", `${product.collectionTitle} / ${product.type}`);
      const title = createElement("h2", "", product.title);
      title.id = `${product.slug}-title`;
      const deck = createElement("p", "", product.deck);
      const price = createElement("p", "price-placeholder", product.pricePlaceholder);
      const pattern = createElement("p", "commercial-note", product.merchandisingPattern);
      const intelligence = createElement(
        "p",
        "commercial-note",
        `Fit ${formatScore(product.product_fit_score)} / Giftability ${formatScore(product.estimated_giftability)}`
      );

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

      card.append(label, title, deck, price, pattern, intelligence, actions);
      grid.appendChild(card);
    });
  }

  function renderFeaturedProductBlocks() {
    const target = document.getElementById("featured-product-blocks");
    if (!target) {
      return;
    }

    const featuredCollections = ["Big Cats Collection", "World Heritage Collection"];
    target.innerHTML = "";
    featuredCollections.forEach((collectionTitle) => {
      const block = createElement("article", "commercial-panel featured-product-block");
      const title = createElement("h2", "", collectionTitle);
      const list = createElement("ul", "featured-product-list");
      products
        .filter((product) => product.collectionTitle === collectionTitle && product.featured)
        .forEach((product) => {
          const item = createElement("li");
          const anchor = createElement("a", "", `${product.type}: ${product.title}`);
          anchor.href = `/shop/products/${product.slug}`;
          item.appendChild(anchor);
          list.appendChild(item);
        });
      block.append(title, list);
      target.appendChild(block);
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
    text("collection-title", product.collectionTitle);
    text("collection-note", collection.curatorialNote);
    text("product-category", product.productCategory);
    text("product-category-score", formatScore(product.product_category_score));
    text("product-fit-score", formatScore(product.product_fit_score));
    text("estimated-giftability", formatScore(product.estimated_giftability));
    text("estimated-repeat-purchase", formatScore(product.estimated_repeat_purchase));

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
      product_score: 0,
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
      product.product_score =
        product.product_fit_score + product.buy_interest * 0.08 + product.add_to_wishlist * 0.04;
    });

    return stats;
  }

  function categoryStats(productsWithStats) {
    const categories = new Map();
    productsWithStats.forEach((product) => {
      const current = categories.get(product.productCategory) || {
        productCategory: product.productCategory,
        product_count: 0,
        product_view: 0,
        add_to_wishlist: 0,
        buy_interest: 0,
        product_category_score: 0,
      };
      current.product_count += 1;
      current.product_view += product.product_view;
      current.add_to_wishlist += product.add_to_wishlist;
      current.buy_interest += product.buy_interest;
      current.product_category_score += product.product_category_score;
      categories.set(product.productCategory, current);
    });

    return [...categories.values()].map((category) => ({
      ...category,
      product_category_score: category.product_category_score / category.product_count,
    }));
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

  function renderCategoryRanking(targetId, rows, metric, formatter) {
    const target = document.getElementById(targetId);
    if (!target) {
      return;
    }

    target.innerHTML = "";
    rows.slice(0, 5).forEach((category, index) => {
      const item = createElement("li", "analytics-row");
      const label = createElement("span", "", `${index + 1}. ${category.productCategory}`);
      const value = createElement("strong", "", formatter(category[metric], category));
      item.append(label, value);
      target.appendChild(item);
    });
  }

  function formatScore(score) {
    return `${Math.round(score * 100)}%`;
  }

  function renderDashboard() {
    const events = readEvents();
    const stats = productStats();
    const categories = categoryStats(stats);
    text("analytics-event-count", events.length.toLocaleString());
    text("analytics-last-updated", events.length ? events[events.length - 1].occurred_at : "No events yet");

    renderRanking(
      "most-viewed-products",
      [...stats].sort((a, b) => b.product_view - a.product_view),
      "product_view",
      (value) => `${value} views`
    );
    renderRanking(
      "top-products",
      [...stats].sort((a, b) => b.product_score - a.product_score),
      "product_score",
      (value, product) =>
        `${formatScore(product.product_fit_score)} fit / ${product.buy_interest} buy interest`
    );
    renderCategoryRanking(
      "top-categories",
      [...categories].sort((a, b) => b.product_category_score - a.product_category_score),
      "product_category_score",
      (value, category) =>
        `${formatScore(value)} category score / ${category.product_view} views`
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
    renderRanking(
      "highest-product-fit-score",
      [...stats].sort((a, b) => b.product_fit_score - a.product_fit_score),
      "product_fit_score",
      (value, product) => `${formatScore(value)} fit / ${product.productCategory}`
    );
  }

  function initialize() {
    renderProductCards();
    renderFeaturedProductBlocks();

    const productSlug =
      document.body.dataset.productSlug ||
      (document.getElementById("product-detail-actions")
        ? window.location.pathname.split("/").filter(Boolean).pop()
        : "");
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
