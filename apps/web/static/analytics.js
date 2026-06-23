/** RC11 browser-local analytics implementation for public beta validation. */

(function () {
  const SESSION_KEY = "natureCulture.analytics.session";
  const EVENTS_KEY = "natureCulture.analytics.events";
  const EVENT_NAMES = new Set([
    "page_view",
    "collection_view",
    "series_view",
    "product_view",
    "wishlist",
    "buy_intent",
    "outbound_click",
    "search",
    "session_duration",
  ]);

  const aliases = {
    add_to_wishlist: "wishlist",
    buy_interest: "buy_intent",
    checkout_intent: "buy_intent",
  };

  function uuid() {
    if (window.crypto && typeof window.crypto.randomUUID === "function") {
      return window.crypto.randomUUID();
    }
    return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
  }

  function deviceClass() {
    const width = window.innerWidth || 0;
    if (width >= 960) return "desktop";
    if (width >= 640) return "tablet";
    if (width > 0) return "mobile";
    return "unknown";
  }

  function readJson(key, fallback) {
    try {
      const raw = window.localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (err) {
      console.warn("Unable to read analytics storage", err);
      return fallback;
    }
  }

  function writeJson(key, value) {
    window.localStorage.setItem(key, JSON.stringify(value));
  }

  function session() {
    let current = readJson(SESSION_KEY, null);
    if (current && current.session_id) {
      return current;
    }

    const params = new URLSearchParams(window.location.search);
    current = {
      session_id: uuid(),
      started_at: new Date().toISOString(),
      landing_path: window.location.pathname,
      referrer_domain: document.referrer ? new URL(document.referrer).hostname : "",
      utm_source: params.get("utm_source") || "",
      utm_medium: params.get("utm_medium") || "",
      utm_campaign: params.get("utm_campaign") || "",
      device_class: deviceClass(),
      consent_state: "not_required",
    };
    writeJson(SESSION_KEY, current);
    return current;
  }

  function events() {
    const value = readJson(EVENTS_KEY, []);
    return Array.isArray(value) ? value : [];
  }

  function normalizeEventName(eventName) {
    return aliases[eventName] || eventName;
  }

  function track(eventName, details) {
    const normalized = normalizeEventName(eventName);
    if (!EVENT_NAMES.has(normalized)) {
      throw new Error(`Unsupported analytics event: ${eventName}`);
    }

    const currentSession = session();
    const metadata = details && details.metadata ? details.metadata : {};
    if (eventName === "checkout_intent") {
      metadata.simulated_checkout_intent = true;
    }

    const event = {
      event_id: uuid(),
      session_id: currentSession.session_id,
      event_name: normalized,
      occurred_at: new Date().toISOString(),
      page_path: window.location.pathname,
      page_title: document.title,
      entity_type: details?.entity_type || "page",
      entity_id: details?.entity_id || "",
      entity_title: details?.entity_title || "",
      collection_id: details?.collection_id || "",
      series_id: details?.series_id || "",
      product_category: details?.product_category || "",
      experiment_id: details?.experiment_id || "",
      variant_id: details?.variant_id || "",
      search_query: details?.search_query || "",
      outbound_domain: details?.outbound_domain || "",
      metadata,
    };

    const nextEvents = events();
    nextEvents.push(event);
    writeJson(EVENTS_KEY, nextEvents.slice(-1000));
    window.dispatchEvent(new CustomEvent("nature-culture:analytics", { detail: event }));
    return event;
  }

  function flushSessionDuration() {
    const currentSession = session();
    const started = Date.parse(currentSession.started_at);
    const duration = Number.isFinite(started)
      ? Math.max(0, Math.round((Date.now() - started) / 1000))
      : 0;
    currentSession.ended_at = new Date().toISOString();
    currentSession.duration_seconds = duration;
    writeJson(SESSION_KEY, currentSession);
    track("session_duration", {
      entity_type: "page",
      metadata: {
        duration_seconds: duration,
        page_count: events().filter((event) => event.event_name === "page_view").length,
        engaged_event_count: events().filter((event) => event.event_name !== "page_view").length,
      },
    });
  }

  document.addEventListener("click", (event) => {
    const anchor = event.target.closest("a[href]");
    if (!anchor) return;
    const url = new URL(anchor.href, window.location.href);
    if (url.origin !== window.location.origin) {
      track("outbound_click", {
        entity_type: "source",
        entity_title: anchor.textContent.trim(),
        outbound_domain: url.hostname,
      });
    }
  });

  window.addEventListener("pagehide", flushSessionDuration);

  window.NC_ANALYTICS = {
    eventNames: [...EVENT_NAMES],
    session,
    events,
    track,
    flushSessionDuration,
  };
})();
