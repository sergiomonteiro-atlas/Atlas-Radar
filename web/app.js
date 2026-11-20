(() => {
  const CAT_COLORS = {
    ai: "#00d4ff",
    tech: "#a855f7",
    business: "#ffb84d",
    gaming: "#ff4d79",
  };

  // Dicionário Multi-Idioma (PT-BR, PT-PT, FR, EN)
  const I18N = {
    "pt-BR": {
      metric24h: "24H",
      metricModels: "MODELOS IA",
      modeGlobe: "Globo 3D",
      modeOrbital: "Orbital",
      modeTv: "Live TV",
      studioBtn: "Estúdio",
      verticalsTitle: "VERTICAIS ATLAS",
      searchPlaceholder: "Filtrar tema, modelo, empresa...",
      catAll: "Todos os Sinais",
      catAi: "IA & Agentes",
      catTech: "Tech & Engenharia",
      catBusiness: "Negócios & Geopolítica",
      catGaming: "Gaming (AtlasNews)",
      feedLangTitle: "IDIOMA DAS FONTES",
      windowTitle: "JANELA TEMPORAL",
      sensorsTitle: "SENSORES ATIVOS",
      harnessNote: "Conectado via <code>POST /mcp</code> ao <strong>Hermes-Agent</strong> e pronto para exportar ao <strong>Atlas-Cortex</strong>.",
      tabFeed: "FEED LIVE",
      tabModels: "MODELOS IA",
      btnCortex: "Salvar no Atlas-Cortex (.md)",
      btnPauta: "Copiar Pauta AtlasNews",
      btnHermes: "Comando Hermes",
      btnOpen: "Abrir Fonte",
      hudGlobe: "ATLASNEWS LIVE · GLOBO 3D NOTURNO",
      hudGlobeHint: "Arraste para girar · Scroll para zoom · Clique num sinal",
      hudOrbital: "ATLAS RADAR · VISÃO ORBITAL 24H",
      hudOrbitalHint: "Planetas próximos ao núcleo = últimas horas · Clique para inspecionar",
      catLabels: { ai: "IA & AGENTES", tech: "TECH", business: "NEGÓCIOS", gaming: "GAMING" },
      emptyFeed: "Nenhum sinal neste filtro. Amplie a janela para 72H ou mude o idioma.",
    },
    "pt-PT": {
      metric24h: "24H",
      metricModels: "MODELOS IA",
      modeGlobe: "Globo 3D",
      modeOrbital: "Orbital",
      modeTv: "TV Direto",
      studioBtn: "Estúdio",
      verticalsTitle: "VERTICAIS ATLAS",
      searchPlaceholder: "Filtrar tema, modelo, empresa...",
      catAll: "Todos os Sinais",
      catAi: "IA & Agentes",
      catTech: "Tech & Engenharia",
      catBusiness: "Negócios & Geopolítica",
      catGaming: "Gaming (AtlasNews)",
      feedLangTitle: "IDIOMA DAS FONTES",
      windowTitle: "JANELA TEMPORAL",
      sensorsTitle: "SENSORES ATIVOS",
      harnessNote: "Ligado via <code>POST /mcp</code> ao <strong>Hermes-Agent</strong> e pronto a exportar para o <strong>Atlas-Cortex</strong>.",
      tabFeed: "FEED DIRETO",
      tabModels: "MODELOS IA",
      btnCortex: "Guardar no Atlas-Cortex (.md)",
      btnPauta: "Copiar Pauta AtlasNews",
      btnHermes: "Comando Hermes",
      btnOpen: "Abrir Fonte",
      hudGlobe: "ATLASNEWS LIVE · GLOBO 3D NOTURNO",
      hudGlobeHint: "Arrasta para rodar · Roda do rato para zoom · Clica num sinal",
      hudOrbital: "ATLAS RADAR · VISÃO ORBITAL 24H",
      hudOrbitalHint: "Planetas perto do núcleo = últimas horas · Clica para inspecionar",
      catLabels: { ai: "IA & AGENTES", tech: "TECH", business: "NEGÓCIOS", gaming: "GAMING" },
      emptyFeed: "Sem sinais neste filtro. Alarga a janela para 72H ou muda o idioma.",
    },
    fr: {
      metric24h: "24H",
      metricModels: "MODÈLES IA",
      modeGlobe: "Globe 3D",
      modeOrbital: "Orbital",
      modeTv: "TV Direct",
      studioBtn: "Studio",
      verticalsTitle: "VERTICALES ATLAS",
      searchPlaceholder: "Filtrer sujet, modèle, entreprise...",
      catAll: "Tous les Signaux",
      catAi: "IA & Agents",
      catTech: "Tech & Ingénierie",
      catBusiness: "Business & Géopolitique",
      catGaming: "Gaming (AtlasNews)",
      feedLangTitle: "LANGUE DES SOURCES",
      windowTitle: "FENÊTRE TEMPORELLE",
      sensorsTitle: "CAPTEURS ACTIFS",
      harnessNote: "Connecté via <code>POST /mcp</code> à <strong>Hermes-Agent</strong> et prêt à exporter vers <strong>Atlas-Cortex</strong>.",
      tabFeed: "FLUX LIVE",
      tabModels: "MODÈLES IA",
      btnCortex: "Sauver dans Atlas-Cortex (.md)",
      btnPauta: "Copier Sujet AtlasNews",
      btnHermes: "Commande Hermes",
      btnOpen: "Ouvrir la Source",
      hudGlobe: "ATLASNEWS LIVE · GLOBE 3D NOCTURNE",
      hudGlobeHint: "Glissez pour tourner · Molette pour zoomer · Cliquez sur un signal",
      hudOrbital: "ATLAS RADAR · VUE ORBITALE 24H",
      hudOrbitalHint: "Planètes proches du cœur = dernières heures · Cliquez pour inspecter",
      catLabels: { ai: "IA & AGENTS", tech: "TECH", business: "BUSINESS", gaming: "GAMING" },
      emptyFeed: "Aucun signal pour ce filtre. Essayez 72H ou toutes les langues.",
    },
    en: {
      metric24h: "24H",
      metricModels: "AI MODELS",
      modeGlobe: "3D Globe",
      modeOrbital: "Orbital",
      modeTv: "Live TV",
      studioBtn: "Studio",
      verticalsTitle: "ATLAS VERTICALS",
      searchPlaceholder: "Filter topic, model, company...",
      catAll: "All Signals",
      catAi: "AI & Agents",
      catTech: "Tech & Engineering",
      catBusiness: "Business & Geopolitics",
      catGaming: "Gaming (AtlasNews)",
      feedLangTitle: "SOURCE LANGUAGE",
      windowTitle: "TIME WINDOW",
      sensorsTitle: "ACTIVE SENSORS",
      harnessNote: "Connected via <code>POST /mcp</code> to <strong>Hermes-Agent</strong> and ready to export to <strong>Atlas-Cortex</strong>.",
      tabFeed: "LIVE FEED",
      tabModels: "AI MODELS",
      btnCortex: "Save to Atlas-Cortex (.md)",
      btnPauta: "Copy AtlasNews Brief",
      btnHermes: "Hermes Command",
      btnOpen: "Open Source",
      hudGlobe: "ATLASNEWS LIVE · NIGHT 3D GLOBE",
      hudGlobeHint: "Drag to rotate · Scroll to zoom · Click any signal",
      hudOrbital: "ATLAS RADAR · 24H ORBITAL VIEW",
      hudOrbitalHint: "Closer to core = newer signals · Click to inspect",
      catLabels: { ai: "AI & AGENTS", tech: "TECH", business: "BUSINESS", gaming: "GAMING" },
      emptyFeed: "No signals for this filter. Try 72H or ALL languages.",
    },
  };

  const state = {
    uiLang: "pt-BR",
    meta: {},
    sources: [],
    aiModels: [],
    tvChannels: [],
    tvLoaded: false,
    allSignals: [],
    filtered: [],
    category: "all",
    feedLang: "all",
    hours: 24,
    query: "",
    mode: "globe", // "globe" | "orbital" | "tv"
    tvLayout: "single", // "single" | "grid"
    tvActiveId: "cnn_br",
    studio: false,
    selected: null,
    globeInstance: null,
    globeReady: false,
    // Orbital canvas
    renderedNodes: [],
    tick: 0,
  };

  // DOM refs
  const globeContainer = document.getElementById("globe-container");
  const canvas = document.getElementById("radar-canvas");
  const ctx = canvas.getContext("2d");
  const tvStage = document.getElementById("tv-stage");
  const stageHud = document.getElementById("stage-hud");
  const feedList = document.getElementById("feed-list");
  const modelsList = document.getElementById("models-list");
  const sensorsList = document.getElementById("sensors-list");
  const tickerEl = document.getElementById("ticker-content");
  const inspector = document.getElementById("inspector");
  const toastEl = document.getElementById("toast");

  function t(key) {
    return (I18N[state.uiLang] && I18N[state.uiLang][key]) || I18N["pt-BR"][key] || key;
  }

  function applyI18n() {
    document.querySelectorAll("[data-i18n]").forEach((el) => {
      const val = t(el.dataset.i18n);
      if (el.dataset.i18n === "harnessNote") el.innerHTML = val;
      else el.textContent = val;
    });
    document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
      el.placeholder = t(el.dataset.i18nPlaceholder);
    });
    updateHudLabels();
    renderFeed();
    renderTicker();
  }

  function updateHudLabels() {
    const label = document.getElementById("hud-mode-label");
    const hint = document.getElementById("hud-hint");
    if (state.mode === "globe") {
      label.textContent = t("hudGlobe");
      hint.textContent = t("hudGlobeHint");
    } else if (state.mode === "orbital") {
      label.textContent = t("hudOrbital");
      hint.textContent = t("hudOrbitalHint");
    }
  }

  function showToast(msg) {
    toastEl.textContent = msg;
    toastEl.classList.add("show");
    clearTimeout(showToast._t);
    showToast._t = setTimeout(() => toastEl.classList.remove("show"), 3200);
  }

  function formatAge(h) {
    const pfx = state.uiLang === "fr" ? "il y a " : state.uiLang === "en" ? "" : "há ";
    const sfx = state.uiLang === "en" ? " ago" : "";
    if (h < 1) return `${pfx}${Math.max(1, Math.round(h * 60))}m${sfx}`;
    if (h < 24) return `${pfx}${Math.round(h)}h${sfx}`;
    return `${pfx}${Math.round(h / 24)}d${sfx}`;
  }

  function formatNum(n) {
    if (n >= 1_000_000) return (n / 1_000_000).toFixed(1) + "M";
    if (n >= 1_000) return (n / 1_000).toFixed(1) + "K";
    return String(n || 0);
  }

  function escapeHtml(str) {
    return String(str || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  // World clocks
  function updateClocks() {
    const now = new Date();
    const fmt = (tz) =>
      new Intl.DateTimeFormat("pt-BR", {
        timeZone: tz,
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: false,
      }).format(now);
    document.getElementById("clock-utc").textContent = fmt("UTC");
    document.getElementById("clock-brt").textContent = fmt("America/Sao_Paulo");
    document.getElementById("clock-lis").textContent = fmt("Europe/Lisbon");
    document.getElementById("clock-par").textContent = fmt("Europe/Paris");
  }
  setInterval(updateClocks, 1000);
  updateClocks();

  // Initialize HD Globe.gl (Terra Noturna estilo AtlasNews)
  function initGlobe() {
    if (typeof window.Globe !== "function") {
      console.warn("Globe.gl CDN indisponível; usando fallback Orbital Canvas.");
      return false;
    }
    const rect = globeContainer.getBoundingClientRect();
    const g = window.Globe()(globeContainer)
      .width(rect.width || 800)
      .height(rect.height || 600)
      .backgroundColor("rgba(0,0,0,0)")
      .globeImageUrl("https://unpkg.com/three-globe/example/img/earth-night.jpg")
      .bumpImageUrl("https://unpkg.com/three-globe/example/img/earth-topology.png")
      .showAtmosphere(true)
      .atmosphereColor("#00a8ff")
      .atmosphereAltitude(0.22)
      .pointLat((d) => d._lat)
      .pointLng((d) => d._lon)
      .pointColor((d) => CAT_COLORS[d.category] || "#00d4ff")
      .pointAltitude((d) => 0.02 + (d.heat_score / 99) * 0.14)
      .pointRadius((d) => (state.selected?.id === d.id ? 0.72 : 0.32 + (d.heat_score / 99) * 0.22))
      .pointLabel(
        (d) =>
          `<div style="background:rgba(3,12,28,0.94);border:1px solid #00d4ff;padding:8px 10px;border-radius:7px;max-width:260px;font-family:Inter,sans-serif;font-size:11.5px;color:#fff;">
            <div style="color:${CAT_COLORS[d.category] || "#00d4ff"};font-family:JetBrains Mono,monospace;font-size:9.5px;font-weight:700;margin-bottom:4px;">${(d.source || "").toUpperCase()} · SCORE ${d.heat_score}</div>
            <div style="font-weight:600;line-height:1.3;">${escapeHtml(d.title)}</div>
          </div>`
      )
      .onPointClick((d) => selectSignal(d))
      .ringsData([])
      .ringLat((d) => d.lat)
      .ringLng((d) => d.lon)
      .ringColor(() => (t) => `rgba(0, 212, 255, ${1 - t})`)
      .ringMaxRadius(4.2)
      .ringPropagationSpeed(1.8)
      .ringRepeatPeriod(1400)
      .arcsData([])
      .arcColor((d) => d.color)
      .arcDashLength(0.45)
      .arcDashGap(1.6)
      .arcDashAnimateTime(2600)
      .arcStroke(0.55)
      .arcAltitudeAutoScale(0.32);

    g.controls().autoRotate = true;
    g.controls().autoRotateSpeed = 0.45;
    g.controls().enableDamping = true;
    g.pointOfView({ lat: 18, lng: -22, altitude: 2.15 }, 0);

    state.globeInstance = g;
    state.globeReady = true;
    return true;
  }

  function updateGlobeData() {
    if (!state.globeReady || !state.globeInstance) return;
    const hubCount = {};
    const pts = state.filtered.slice(0, 55).map((s) => {
      const hub = s.hub || { city: "Global", lat: 20, lon: 0 };
      const c = (hubCount[hub.city] = (hubCount[hub.city] || 0) + 1);
      const angle = c * 1.45;
      const spread = Math.min(6.5, (c - 1) * 1.15);
      return {
        ...s,
        _lat: hub.lat + Math.sin(angle) * spread,
        _lon: hub.lon + Math.cos(angle) * spread,
      };
    });

    // Unique active hubs for rings + arcs
    const hubs = [];
    pts.forEach((p) => {
      if (p.hub && !hubs.find((h) => h.city === p.hub.city)) hubs.push(p.hub);
    });

    const arcs = [];
    for (let i = 0; i < Math.min(hubs.length - 1, 8); i++) {
      arcs.push({
        startLat: hubs[i].lat,
        startLng: hubs[i].lon,
        endLat: hubs[(i + 1) % hubs.length].lat,
        endLng: hubs[(i + 1) % hubs.length].lon,
        color: ["#00d4ff", "#ffb84d"],
      });
    }

    state.globeInstance.pointsData(pts).ringsData(hubs.slice(0, 8)).arcsData(arcs);
  }

  function resizeStage() {
    const rect = canvas.parentElement.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    if (state.globeReady && state.globeInstance) {
      state.globeInstance.width(rect.width).height(rect.height);
    }
  }
  window.addEventListener("resize", resizeStage);

  // Load API data
  async function loadData(forceRefresh = false) {
    const btn = document.getElementById("btn-refresh");
    if (forceRefresh) {
      btn.textContent = "…";
      btn.disabled = true;
    }
    try {
      if (forceRefresh) {
        await fetch("/api/refresh", { method: "POST" });
      }
      const res = await fetch("/api/trends?hours=168&limit=160");
      const data = await res.json();
      state.meta = data.meta || {};
      state.sources = data.sources || [];
      state.aiModels = data.ai_models || [];
      state.allSignals = data.signals || [];

      renderMeta();
      renderSensors();
      renderModels();
      applyFilters();
      if (forceRefresh) {
        showToast(`AtlasRadar: ${state.meta.signals_24h || 0} sinais (24h) · ${state.aiModels.length} modelos IA`);
      }
    } catch (err) {
      showToast("Erro ao conectar ao servidor AtlasRadar.");
      console.error(err);
    } finally {
      btn.textContent = "↻";
      btn.disabled = false;
    }
  }

  function renderMeta() {
    const m = state.meta;
    document.getElementById("metric-24h").textContent = m.signals_24h ?? 0;
    document.getElementById("metric-models").textContent = m.ai_models_count ?? state.aiModels.length;

    const c = m.counts || {};
    document.getElementById("count-all").textContent = c.all ?? state.allSignals.length;
    document.getElementById("count-ai").textContent = c.ai ?? 0;
    document.getElementById("count-tech").textContent = c.tech ?? 0;
    document.getElementById("count-business").textContent = c.business ?? 0;
    document.getElementById("count-gaming").textContent = c.gaming ?? 0;

    if (m.updated_at) {
      const d = new Date(m.updated_at);
      document.getElementById("last-sync").textContent = `SYNC ${d.toLocaleTimeString("pt-BR", {
        hour: "2-digit",
        minute: "2-digit",
      })}`;
    }
  }

  function renderSensors() {
    sensorsList.innerHTML = "";
    state.sources.forEach((s) => {
      const row = document.createElement("div");
      row.className = "sensor-row";
      row.innerHTML = `
        <span class="sensor-status">
          <span class="s-dot ${s.ok ? "ok" : "err"}"></span>
          <span>${escapeHtml(s.source)}</span>
        </span>
        <span class="mono-dim">${s.ok ? s.count : "ERR"}</span>
      `;
      sensorsList.appendChild(row);
    });
  }

  function renderModels() {
    document.getElementById("models-count").textContent = state.aiModels.length;
    modelsList.innerHTML = "";
    if (!state.aiModels.length) {
      modelsList.innerHTML = `<div class="mono-dim" style="padding:18px;text-align:center;">Sem dados do Hugging Face no momento.</div>`;
      return;
    }
    state.aiModels.forEach((m, i) => {
      const a = document.createElement("a");
      a.className = "model-card";
      a.href = m.url;
      a.target = "_blank";
      a.rel = "noopener";
      a.innerHTML = `
        <div class="model-top">
          <span class="model-org">${escapeHtml(m.org)}</span>
          <span class="model-rank">#${i + 1} TRENDING</span>
        </div>
        <div class="model-name">${escapeHtml(m.name)}</div>
        <div class="model-stats">
          <span class="badge badge-ai">${escapeHtml(m.pipeline)}</span>
          <span>⬇ ${formatNum(m.downloads)} · ♥ ${formatNum(m.likes)}</span>
        </div>
      `;
      modelsList.appendChild(a);
    });
  }

  function applyFilters() {
    const q = state.query.trim().toLowerCase();
    state.filtered = state.allSignals.filter((s) => {
      if (state.category !== "all" && s.category !== state.category) return false;
      if (state.feedLang !== "all" && (s.lang || "en") !== state.feedLang) return false;
      if (state.hours > 0 && s.age_hours > state.hours) return false;
      if (q) {
        const hay = `${s.title} ${s.summary} ${s.source} ${s.hub?.city || ""}`.toLowerCase();
        if (!hay.includes(q)) return false;
      }
      return true;
    });

    renderFeed();
    renderTicker();
    updateGlobeData();
  }

  function renderFeed() {
    const labels = t("catLabels");
    document.getElementById("feed-count").textContent = state.filtered.length;
    feedList.innerHTML = "";

    if (!state.filtered.length) {
      feedList.innerHTML = `<div class="mono-dim" style="padding:18px;text-align:center;">${t("emptyFeed")}</div>`;
      return;
    }

    state.filtered.forEach((s) => {
      const card = document.createElement("div");
      card.className = "feed-card" + (state.selected?.id === s.id ? " selected" : "");
      card.innerHTML = `
        <div class="feed-meta">
          <span>
            <span class="badge badge-${s.category}">${labels[s.category] || s.category}</span>
            <span class="lang-pill">${(s.lang || "en").toUpperCase()}</span>
          </span>
          <span class="mono-dim">${formatAge(s.age_hours)} · ${s.hub?.city || "Global"}</span>
        </div>
        <div class="feed-title">${escapeHtml(s.title)}</div>
        <div class="feed-bottom">
          <span>${escapeHtml(s.source)}</span>
          <span class="heat-wrap">
            <span class="heat-bar"><span class="heat-fill" style="width:${s.heat_score}%"></span></span>
            <strong>${s.heat_score}</strong>
          </span>
        </div>
      `;
      card.addEventListener("click", () => selectSignal(s));
      feedList.appendChild(card);
    });
  }

  function renderTicker() {
    const labels = t("catLabels");
    const top = (state.filtered.length ? state.filtered : state.allSignals).slice(0, 14);
    if (!top.length) return;
    tickerEl.innerHTML = top
      .map(
        (s) =>
          `<span style="color:${CAT_COLORS[s.category] || "#00d4ff"};font-weight:700;">[${
            labels[s.category] || s.category
          }]</span> ${escapeHtml(s.title)} <span style="color:#8fb0da;">(${escapeHtml(s.source)})</span>`
      )
      .join(" &nbsp;&nbsp;◆&nbsp;&nbsp; ");
  }

  function selectSignal(s) {
    state.selected = s;
    const labels = t("catLabels");
    inspector.classList.remove("hidden");
    const badge = document.getElementById("ins-cat");
    badge.className = `badge badge-${s.category}`;
    badge.textContent = `${labels[s.category] || s.category} · SCORE ${s.heat_score}`;
    document.getElementById("ins-meta").textContent = `${s.source} · ${s.hub?.city || "Global"} · ${formatAge(s.age_hours)}`;
    document.getElementById("ins-title").textContent = s.title;
    document.getElementById("ins-summary").textContent = s.summary;
    document.getElementById("ins-link").href = s.url;

    if (state.globeReady && state.globeInstance && s.hub) {
      state.globeInstance.pointOfView({ lat: s.hub.lat, lng: s.hub.lon, altitude: 1.75 }, 850);
    }
    renderFeed();
    updateGlobeData();
  }

  // LIVE TV WALL (Resolução dinâmica em tempo real via GET /api/tv)
  async function loadTvChannels(force = false) {
    const container = document.getElementById("tv-players");
    if (!state.tvLoaded || force) {
      container.innerHTML = `<div class="mono-dim" style="padding:24px;text-align:center;">Verificando canais 24h ao vivo (PT / FR / EN)...</div>`;
      try {
        const res = await fetch(`/api/tv${force ? "?refresh=1" : ""}`);
        const data = await res.json();
        state.tvChannels = (data.channels || []).filter((c) => c.online && c.embeddable && c.embed_url);
        state.tvLoaded = true;
        if (state.tvChannels.length && !state.tvChannels.find((c) => c.id === state.tvActiveId)) {
          state.tvActiveId = state.tvChannels[0].id;
        }
      } catch (err) {
        container.innerHTML = `<div class="mono-dim" style="padding:24px;text-align:center;">Erro ao verificar canais Live TV.</div>`;
        return;
      }
    }
    renderTvControls();
    renderTvPlayers();
  }

  function renderTvControls() {
    const box = document.getElementById("tv-channel-buttons");
    box.innerHTML = "";
    state.tvChannels.forEach((ch) => {
      const btn = document.createElement("button");
      btn.className = "tv-ch-btn" + (state.tvActiveId === ch.id ? " active" : "");
      btn.textContent = `[${ch.lang}] ${ch.name}`;
      btn.addEventListener("click", () => {
        state.tvActiveId = ch.id;
        renderTvControls();
        renderTvPlayers();
      });
      box.appendChild(btn);
    });
  }

  function renderTvPlayers() {
    const container = document.getElementById("tv-players");
    container.className = `tv-players ${state.tvLayout}`;
    if (!state.tvChannels.length) {
      container.innerHTML = `<div class="mono-dim" style="padding:24px;text-align:center;">Nenhum canal embeddable ativo no momento.</div>`;
      return;
    }

    let list = [];
    if (state.tvLayout === "single") {
      list = [state.tvChannels.find((c) => c.id === state.tvActiveId) || state.tvChannels[0]];
    } else {
      // Mosaico 2x2 equilibrado: tenta pegar 1 PT, 1 FR, 1 EN + canal ativo
      const preferred = ["cnn_br", "france24_fr", "bloomberg_en", "euronews_pt", "sky_en", "dw_en"];
      preferred.forEach((pid) => {
        const found = state.tvChannels.find((c) => c.id === pid);
        if (found && list.length < 4 && !list.includes(found)) list.push(found);
      });
      state.tvChannels.forEach((c) => {
        if (list.length < 4 && !list.includes(c)) list.push(c);
      });
    }

    container.innerHTML = list
      .map(
        (ch) => `
        <div class="tv-card">
          <div class="tv-card-bar">
            <span><strong style="color:#ff4d6a;">● LIVE</strong> &nbsp;${escapeHtml(ch.name)} <span class="lang-pill">${ch.lang}</span></span>
            <a href="https://www.youtube.com/watch?v=${ch.video_id}" target="_blank" rel="noopener">↗ YouTube</a>
          </div>
          <iframe
            src="${ch.embed_url}"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
          ></iframe>
        </div>`
      )
      .join("");
  }

  // Mode switching (Globe 3D / Orbital / Live TV)
  function switchMode(newMode) {
    state.mode = newMode;
    document.querySelectorAll(".mode-btn").forEach((b) => b.classList.toggle("active", b.dataset.mode === newMode));

    globeContainer.classList.toggle("hidden", newMode !== "globe" || !state.globeReady);
    canvas.classList.toggle("hidden", !(newMode === "orbital" || (newMode === "globe" && !state.globeReady)));
    tvStage.classList.toggle("hidden", newMode !== "tv");
    stageHud.classList.toggle("hidden", newMode === "tv");

    if (newMode === "tv") {
      loadTvChannels(false);
    } else {
      updateHudLabels();
      resizeStage();
    }
  }

  // Orbital Canvas 60fps
  function drawOrbital(w, h) {
    const cx = w / 2;
    const cy = h / 2;
    const maxR = Math.min(w, h) * 0.41;

    [
      { frac: 0.26, label: "1H" },
      { frac: 0.50, label: "6H" },
      { frac: 0.75, label: "12H" },
      { frac: 1.0, label: "24H+" },
    ].forEach((ring) => {
      const rr = maxR * ring.frac;
      ctx.beginPath();
      ctx.arc(cx, cy, rr, 0, Math.PI * 2);
      ctx.strokeStyle = "rgba(0, 180, 255, 0.2)";
      ctx.setLineDash([4, 6]);
      ctx.lineWidth = 1;
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.font = "600 10px 'JetBrains Mono', monospace";
      ctx.fillStyle = "rgba(143, 176, 218, 0.8)";
      ctx.fillText(ring.label, cx + 6, cy - rr + 12);
    });

    const sweepAngle = state.tick * 0.014;
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(cx + Math.cos(sweepAngle) * maxR, cy + Math.sin(sweepAngle) * maxR);
    ctx.strokeStyle = "rgba(0, 212, 255, 0.35)";
    ctx.lineWidth = 1.6;
    ctx.stroke();

    const coreGrad = ctx.createRadialGradient(cx, cy, 4, cx, cy, 36);
    coreGrad.addColorStop(0, "rgba(0, 212, 255, 0.95)");
    coreGrad.addColorStop(0.5, "rgba(0, 120, 255, 0.38)");
    coreGrad.addColorStop(1, "rgba(3, 12, 28, 0)");
    ctx.fillStyle = coreGrad;
    ctx.beginPath();
    ctx.arc(cx, cy, 36, 0, Math.PI * 2);
    ctx.fill();

    ctx.font = "800 11px 'JetBrains Mono', monospace";
    ctx.fillStyle = "#ffffff";
    ctx.textAlign = "center";
    ctx.fillText("ATLAS", cx, cy + 4);
    ctx.textAlign = "left";

    state.renderedNodes = [];
    const items = state.filtered.slice(0, 42);
    items.forEach((s, idx) => {
      const clampedAge = Math.min(28, Math.max(0.2, s.age_hours));
      const normDist = 0.22 + (clampedAge / 28) * 0.76;
      const orbitR = maxR * normDist;
      const speed = (0.0026 / (0.4 + normDist)) * (idx % 2 === 0 ? 1 : -0.7);
      const angle = idx * 2.39996 + state.tick * speed;

      const x = cx + Math.cos(angle) * orbitR;
      const y = cy + Math.sin(angle) * orbitR;
      const color = CAT_COLORS[s.category] || "#00d4ff";
      const isSelected = state.selected?.id === s.id;
      const nodeR = isSelected ? 8 : 3.5 + (s.heat_score / 99) * 3.8;

      ctx.beginPath();
      ctx.arc(x, y, nodeR, 0, Math.PI * 2);
      ctx.fillStyle = color;
      ctx.shadowColor = color;
      ctx.shadowBlur = isSelected ? 18 : 9;
      ctx.fill();
      ctx.shadowBlur = 0;

      if (idx < 8 || isSelected) {
        ctx.font = "600 10px 'Inter', sans-serif";
        ctx.fillStyle = "rgba(243, 247, 255, 0.9)";
        const shortTitle = s.title.length > 26 ? s.title.slice(0, 26) + "…" : s.title;
        ctx.fillText(shortTitle, x + nodeR + 6, y + 3);
      }

      state.renderedNodes.push({ x, y, signal: s });
    });
  }

  canvas.addEventListener("click", (e) => {
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    for (const node of state.renderedNodes) {
      if (Math.hypot(node.x - mx, node.y - my) < 16) {
        selectSignal(node.signal);
        break;
      }
    }
  });

  function animate() {
    state.tick += 1;
    if (state.mode === "orbital" || (state.mode === "globe" && !state.globeReady)) {
      const rect = canvas.parentElement.getBoundingClientRect();
      ctx.clearRect(0, 0, rect.width, rect.height);
      drawOrbital(rect.width, rect.height);
    }
    requestAnimationFrame(animate);
  }

  // Event bindings
  document.getElementById("ui-lang-select").addEventListener("change", (e) => {
    state.uiLang = e.target.value;
    applyI18n();
  });

  document.querySelectorAll(".mode-btn").forEach((btn) =>
    btn.addEventListener("click", () => switchMode(btn.dataset.mode))
  );

  document.getElementById("btn-tv-single").addEventListener("click", (e) => {
    state.tvLayout = "single";
    e.currentTarget.classList.add("active");
    document.getElementById("btn-tv-grid").classList.remove("active");
    renderTvPlayers();
  });

  document.getElementById("btn-tv-grid").addEventListener("click", (e) => {
    state.tvLayout = "grid";
    e.currentTarget.classList.add("active");
    document.getElementById("btn-tv-single").classList.remove("active");
    renderTvPlayers();
  });

  document.querySelectorAll(".cat-btn").forEach((btn) =>
    btn.addEventListener("click", () => {
      document.querySelectorAll(".cat-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      state.category = btn.dataset.cat;
      applyFilters();
    })
  );

  document.querySelectorAll(".lf-btn").forEach((btn) =>
    btn.addEventListener("click", () => {
      document.querySelectorAll(".lf-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      state.feedLang = btn.dataset.lang;
      applyFilters();
    })
  );

  document.querySelectorAll(".win-btn[data-hours]").forEach((btn) =>
    btn.addEventListener("click", () => {
      document.querySelectorAll(".win-btn[data-hours]").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      state.hours = Number(btn.dataset.hours);
      applyFilters();
    })
  );

  document.getElementById("search-input").addEventListener("input", (e) => {
    state.query = e.target.value;
    applyFilters();
  });

  document.querySelectorAll(".rtab").forEach((btn) =>
    btn.addEventListener("click", () => {
      document.querySelectorAll(".rtab").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      const isFeed = btn.dataset.rtab === "feed";
      feedList.classList.toggle("hidden", !isFeed);
      modelsList.classList.toggle("hidden", isFeed);
    })
  );

  document.getElementById("btn-studio").addEventListener("click", (e) => {
    state.studio = !state.studio;
    document.getElementById("main-layout").classList.toggle("studio-mode", state.studio);
    e.currentTarget.classList.toggle("studio-on", state.studio);
    setTimeout(resizeStage, 270);
  });

  document.getElementById("btn-refresh").addEventListener("click", () => loadData(true));

  document.getElementById("ins-close").addEventListener("click", () => {
    state.selected = null;
    inspector.classList.add("hidden");
    renderFeed();
  });

  document.getElementById("btn-export-cortex").addEventListener("click", async () => {
    if (!state.selected) return;
    const res = await fetch("/api/export-cortex", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: state.selected.id }),
    });
    const out = await res.json();
    if (out.status === "exported") showToast(`🌌 Atlas-Cortex: ${out.file}`);
  });

  document.getElementById("btn-copy-pauta").addEventListener("click", () => {
    if (!state.selected) return;
    const s = state.selected;
    const text = `[PAUTA ATLASNEWS · ${s.category.toUpperCase()}]\nTítulo: ${s.title}\nFonte: ${s.source} (${s.url})\nResumo: ${s.summary}\nScore: ${s.heat_score}/99\nDestino: AtlasNews / AtlasClub (Club.Atlas-SI.com)`;
    navigator.clipboard.writeText(text).then(() => showToast("🎬 Pauta AtlasNews copiada!"));
  });

  document.getElementById("btn-copy-hermes").addEventListener("click", () => {
    if (!state.selected) return;
    const s = state.selected;
    const cmd = `Hermes, analise esta tendência do AtlasRadar (ID ${s.id} - "${s.title}" | ${s.url}), cruze com o Atlas-Cortex e crie um plano de conteúdo para o AtlasClub.`;
    navigator.clipboard.writeText(cmd).then(() => showToast("🤖 Comando copiado para Hermes-Agent / AtlasVoice!"));
  });

  // Boot after defer script loads
  window.addEventListener("DOMContentLoaded", () => {
    resizeStage();
    initGlobe();
    switchMode("globe");
    applyI18n();
    loadData(false);
    animate();
  });
})();
