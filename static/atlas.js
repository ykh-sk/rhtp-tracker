// Health Systems Atlas: the map, landscape and outreach views of U.S. health systems. A separate page
// from the Rural Health Radar funding tracker (app.js); both share common.js and the same API. The
// unified systems model, filters and outreach tracking live in bd.js.

let STAGES = [];
let STATES = [];          // RHTP states, only for the optional "tailwind" overlay on each system
let HEALTH_SYSTEMS = [];
let HOSPITAL_ROSTER = [];
let hsTierFilter = "all";
let hsOwnershipFilter = "all";
let hsCompanyFilter = "all";

// ---- health systems map ----
// Two Leaflet layers on one real pan/zoom tile map: a small curated layer of
// health-system OPERATORS (companies — from our own sourced dataset, shown
// at every zoom level since there are only a couple dozen) and a bulk layer
// of individual hospital FACILITIES nationwide, from our own /api/cms_hospitals
// endpoint (CMS's "Hospital General Information" dataset, geocoded once
// server-side into our DB — see app/seed.py). This used to fetch HIFLD's
// ArcGIS feature service directly from the browser, but that layer turned out
// to be a frozen 2016-17 snapshot (last edited 2018-02-05) with no CORS-free
// current replacement, so CMS's own actively-maintained dataset is fetched
// server-side instead and served from our DB like everything else curated
// here — "fetched on page load" describes retrieval, not the data's age;
// CMS_META below carries the dataset's own freshness, and the status line
// says so explicitly rather than implying "live" means "current."
let CMS_META = null;
let CMS_HOSPITALS_RAW = null; // the raw CMS rows, kept for the Landscape view's counts

let hsMap = null;
let hsOperatorLayer = null;
let hsFacilityLayer = null; // an L.markerClusterGroup once the plugin loads, else a plain layerGroup
let hsShowOperators = true;
let hsShowFacilities = true;
let hsFacilitiesLoaded = false;
let hsFacilitiesLoading = false;
let hsFacilitiesCount = 0;
let hsAllFacilityMarkers = []; // every live marker, built once; filtering re-adds a subset rather than re-fetching
let ROSTER_BY_CITY_STATE = {}; // "STATE|CITY" -> [{company, name, city, state, source_url, verified_at, tokens}]
let ROSTER_COMPANIES = [];

function tierRadius(tier) {
  return { small: 5, mid: 8, large: 12, major: 17 }[tier] || 6;
}

// Reuses the pipeline's 5-hue stage palette for the tier badge/legend, just
// borrowing hues rather than any pipeline meaning: gray→purple reads as a
// small→major size ramp the same way it already reads as early→late stage.
function tierColorVar(tier) {
  return { small: "--stage-1", mid: "--stage-2", large: "--stage-3", major: "--stage-5" }[tier] || "--stage-1";
}

function ownershipColorVar(ownership) {
  return ownership === "for-profit" ? "--owner-forprofit" : "--owner-nonprofit";
}

// CMS's ownership field is a free-ish text taxonomy ("Voluntary non-profit -
// Private/Church/Other", "Proprietary", "Physician", "Government - Federal/
// State/Local/Hospital District or Authority", "Veterans Health
// Administration", "Department of Defense", "Tribal") — coarser-matched here
// into the same three-way split used elsewhere on the map/legend.
function facilityOwnerColorVar(owner) {
  const o = (owner || "").toUpperCase();
  if (o.includes("NON-PROFIT") || o.includes("NONPROFIT")) return "--owner-nonprofit";
  if (o.includes("PROPRIETARY") || o.includes("PHYSICIAN")) return "--owner-forprofit";
  if (o.includes("GOVERNMENT") || o.includes("VETERANS") || o.includes("DEFENSE") || o.includes("TRIBAL")) return "--owner-government";
  return "--owner-unknown";
}

// CMS doesn't publish a bed count in this dataset (unlike HIFLD), so marker
// size is set by hospital type instead of scaling with beds.
const FACILITY_TYPE_RADIUS = {
  "Acute Care Hospitals": 8,
  "Childrens": 7,
  "Critical Access Hospitals": 6,
  "Psychiatric": 6,
  "Acute Care - Veterans Administration": 7,
  "Acute Care - Department of Defense": 7,
  "Rural Emergency Hospital": 5,
  "Long-term": 6,
};

function facilityRadius(type) {
  return FACILITY_TYPE_RADIUS[type] || 6;
}

function ensureHsMap() {
  if (hsMap || typeof L === "undefined") return;
  // scrollWheelZoom starts off so scrolling the page past the map doesn't
  // hijack the wheel — a click (or the +/- control, which works regardless)
  // arms it, the same pattern most embedded maps use.
  hsMap = L.map("hs-map", { scrollWheelZoom: false, worldCopyJump: true }).setView([39.5, -98.35], 4);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors',
  }).addTo(hsMap);
  hsMap.once("click", () => hsMap.scrollWheelZoom.enable());

  // Cluster bubbles live in Leaflet's marker pane (z 600), which would hide
  // the operator HQ dots drawn in the default overlay pane (z 400) — give
  // operators their own pane above the clusters so they stay visible and
  // clickable. Popups (z 700) still sit above both.
  hsMap.createPane("operators").style.zIndex = 620;
  hsOperatorLayer = L.layerGroup().addTo(hsMap);
  // Clusters into count bubbles that split apart on zoom — the only way to
  // keep ~7,100 individual hospital markers responsive at every zoom level,
  // including the whole-country view. Falls back to a plain (unclustered)
  // layer if the plugin failed to load, so the map still works either way.
  hsFacilityLayer = typeof L.markerClusterGroup === "function"
    ? L.markerClusterGroup({ maxClusterRadius: 45, disableClusteringAtZoom: 16 })
    : L.layerGroup();
}

// Keeps an opened popup panned clear of the zoom control (top-left) and the
// map edges instead of letting it sit underneath them.
const HS_POPUP_OPTIONS = { autoPanPaddingTopLeft: [50, 12], autoPanPaddingBottomRight: [12, 12] };

// One marker per system in the unified list (bd.js): sourced operators sized by hospital
// count, profile-only systems at a fixed size with a dashed outline. The popup content is a
// function so it reflects contact status changes made after the marker was created.
function renderOperatorLayer() {
  if (!hsOperatorLayer) return;
  hsOperatorLayer.clearLayers();
  if (!hsShowOperators) return;
  currentFilteredSystems().forEach(sys => {
    const tier = systemTier(sys);
    const sized = tier !== "unsized";
    L.circleMarker([sys.plotLat, sys.plotLon], {
      radius: sized ? tierRadius(tier) : 7,
      color: sized ? "var(--surface)" : "var(--ink)",
      weight: sized ? 2 : 1.5,
      dashArray: sized ? null : "3 2",
      fillColor: `var(${systemColorVar(sys)})`,
      fillOpacity: sized ? 0.92 : 0.75,
      pane: "operators",
    })
      .bindPopup(() => systemPopupHtml(sys), HS_POPUP_OPTIONS)
      .addTo(hsOperatorLayer);
  });
}

// ---- parent-operator matching ----
// Ties an individual CMS facility back to a curated operator roster
// (app/health_system_rosters_data.py) by normalized city+state, then — when
// more than one roster entry shares that city+state — by name-token overlap
// to pick the closer match. City+state alone is usually decisive since two
// different rostered operators rarely share an exact town.
const ROSTER_STOPWORDS = new Set([
  "HOSPITAL", "HOSPITALS", "MEDICAL", "CENTER", "CENTERS", "HEALTH", "HEALTHCARE",
  "SYSTEM", "CAMPUS", "THE", "OF", "AND", "REGIONAL", "GENERAL", "INC", "CARE",
]);

function normalizeMatchText(s) {
  return (s || "").toUpperCase().replace(/[^A-Z0-9 ]/g, " ").replace(/\s+/g, " ").trim();
}

function nameTokens(s) {
  return normalizeMatchText(s).split(" ").filter(t => t && !ROSTER_STOPWORDS.has(t));
}

function buildRosterIndex() {
  ROSTER_BY_CITY_STATE = {};
  const companies = new Set();
  HOSPITAL_ROSTER.forEach(row => {
    companies.add(row.company);
    const key = `${normalizeMatchText(row.state)}|${normalizeMatchText(row.city)}`;
    const entry = { ...row, tokens: nameTokens(row.name) };
    (ROSTER_BY_CITY_STATE[key] = ROSTER_BY_CITY_STATE[key] || []).push(entry);
  });
  ROSTER_COMPANIES = [...companies].sort();
}

function matchParentCompany(name, city, state) {
  const candidates = ROSTER_BY_CITY_STATE[`${normalizeMatchText(state)}|${normalizeMatchText(city)}`];
  if (!candidates || !candidates.length) return null;
  // Even with a single roster candidate for this city+state, still require at
  // least one shared name token before accepting the match — many towns have
  // more than one hospital, and a roster listing only one of them there is
  // not evidence the live facility we're looking at is that one. Better to
  // fall through to "not identified" than mislabel an unrelated hospital.
  const targetTokens = new Set(nameTokens(name));
  let best = null, bestScore = 0;
  candidates.forEach(c => {
    const score = c.tokens.filter(t => targetTokens.has(t)).length;
    if (score > bestScore) { bestScore = score; best = c; }
  });
  return bestScore > 0 ? best : null;
}

function populateCompanyFilter() {
  const select = document.getElementById("hs-company-filter");
  if (!select) return;
  const current = select.value || "all";
  select.innerHTML = `<option value="all">All hospitals</option>`
    + ROSTER_COMPANIES.map(c => `<option value="${esc(c)}">${esc(c)}</option>`).join("")
    + `<option value="unmatched">Parent not identified</option>`;
  if ([...select.options].some(o => o.value === current)) select.value = current;
}

// CMS leaves some fields blank per facility — each line below is only shown
// when the source actually has that value, rather than padding the popup
// with placeholders.
function facilityPopupHtml(p, match) {
  const has = v => v && String(v).trim() && String(v).toUpperCase() !== "NOT AVAILABLE";
  const address = [p.address, `${p.city || ""}, ${p.state || ""}${has(p.county) ? ` (${p.county} County)` : ""}`]
    .filter(Boolean).join(", ");
  const phoneDigits = has(p.phone) ? String(p.phone).replace(/[^\d+]/g, "") : null;
  const rating = has(p.rating) && /^[1-5]$/.test(p.rating) ? `${p.rating}★ CMS rating` : null;
  const geoCaveat = p.geo_precision !== "address"
    ? `Marker placed at ${p.geo_precision === "zip" ? "ZIP code" : "city"} center — CMS's own address for this hospital didn't geocode precisely.`
    : null;
  // "Cite it when we can't link it" — an explicit, visible line either way,
  // never silently omitted, so absence of a match reads as "not identified"
  // rather than "not part of anything."
  const parentLine = match
    ? `<div>Part of <strong>${esc(match.company)}</strong> (roster verified ${esc(match.verified_at || "date unknown")}) · <a href="${esc(match.source_url)}" target="_blank" rel="noopener">Source</a></div>`
    : `<div class="hs-popup-caution">Parent operator not identified</div>`;

  return `
    <div class="hs-popup">
      <div class="hs-popup-title">${esc(p.name || "Unnamed facility")}</div>
      <div>${esc(titleCase(p.type || "Hospital"))} · ${esc(titleCase((p.ownership || "Ownership not available").replace(/\s*-\s*/g, " ")))}</div>
      <div>${address}</div>
      <div>${[
        has(p.emergency) ? (p.emergency === "Yes" ? "Emergency services" : "No emergency services") : null,
        rating,
      ].filter(Boolean).map(esc).join(" · ")}</div>
      ${parentLine}
      ${phoneDigits ? `<div><a href="tel:${esc(phoneDigits)}">${esc(p.phone)}</a></div>` : ""}
      ${geoCaveat ? `<div class="hs-popup-caution">${esc(geoCaveat)}</div>` : ""}
    </div>
  `;
}

function updateHsStatus(message) {
  const el = document.getElementById("hs-status");
  if (el) el.textContent = message;
}

function offFacilitiesMessage() {
  return `Hospital layer is off — turn on “All hospitals (CMS)” above to show all ${hsFacilitiesCount ? hsFacilitiesCount.toLocaleString() + " " : ""}U.S. hospitals, clustered.`;
}

function loadedFacilitiesMessage() {
  const meta = CMS_META
    ? ` CMS's dataset was last updated ${fmtDate(CMS_META.dataset_modified)}; this site last pulled and geocoded it ${fmtDate(CMS_META.geocoded_at)}.`
    : "";
  return `Showing ${hsFacilitiesCount.toLocaleString()} hospitals from CMS's Hospital General Information dataset, clustered — zoom in to split a cluster apart, click any marker for details.${meta}`;
}

// Fetches the full nationwide dataset once from our own API (a server-side
// geocoded snapshot of CMS's dataset — see app/seed.py) and hands it all to
// the cluster group in one batch, rather than re-fetching a viewport slice
// on every pan/zoom — the clustering plugin is what makes rendering all of
// them at once workable.
async function ensureFacilitiesLoaded() {
  if (hsFacilitiesLoaded || hsFacilitiesLoading || !hsFacilityLayer) return;
  hsFacilitiesLoading = true;
  updateHsStatus("Loading hospitals…");

  let hospitals;
  try {
    const res = await fetch("/api/cms_hospitals");
    const data = await res.json();
    hospitals = data.hospitals || [];
    CMS_META = data.meta || null;
  } catch {
    hsFacilitiesLoading = false;
    updateHsStatus("Couldn't reach the hospital data right now — the operator layer above is still unaffected.");
    return;
  }

  CMS_HOSPITALS_RAW = hospitals;
  const markers = hospitals
    .filter(p => Number.isFinite(p.lat) && Number.isFinite(p.lon))
    .map(p => {
      const match = matchParentCompany(p.name, p.city, p.state);
      const marker = L.circleMarker([p.lat, p.lon], {
        radius: facilityRadius(p.type),
        color: "var(--surface)",
        weight: 1.5,
        fillColor: `var(${facilityOwnerColorVar(p.ownership)})`,
        fillOpacity: 0.88,
      }).bindPopup(facilityPopupHtml(p, match), HS_POPUP_OPTIONS);
      marker.companyKey = match ? match.company : "unmatched";
      marker.stateName = STATE_ABBR[p.state] || "";
      return marker;
    });

  hsAllFacilityMarkers = markers;
  hsFacilitiesCount = markers.length;
  hsFacilitiesLoaded = true;
  hsFacilitiesLoading = false;
  applyFacilityFilter();
  updateHsStatus(hsShowFacilities ? loadedFacilitiesMessage() : offFacilitiesMessage());
  if (!document.getElementById("hs-compare-overlay").hidden) renderCompareModalBody(); // fill in live columns if the modal was opened before the fetch finished
  if (hsView === "landscape") renderLandscape(); // the Landscape counts come from the same fetch
}

// Re-populates the cluster group from the already-loaded marker set — no
// re-fetch — whenever the parent-operator dropdown or the layer toggle
// changes which subset should be visible.
function applyFacilityFilter() {
  if (!hsFacilityLayer || !hsFacilitiesLoaded) return;
  hsFacilityLayer.clearLayers();
  const filtered = hsAllFacilityMarkers.filter(m =>
    (hsCompanyFilter === "all" || m.companyKey === hsCompanyFilter) &&
    (hsFilters.state === "all" || m.stateName === hsFilters.state));
  if (typeof hsFacilityLayer.addLayers === "function") {
    hsFacilityLayer.addLayers(filtered); // markercluster's bulk-add — much faster than adding one at a time
  } else {
    filtered.forEach(m => m.addTo(hsFacilityLayer));
  }
}

function updateFacilityVisibility() {
  if (!hsMap || !hsFacilityLayer) return;
  if (hsShowFacilities) {
    if (!hsMap.hasLayer(hsFacilityLayer)) hsFacilityLayer.addTo(hsMap);
    if (hsFacilitiesLoaded) { applyFacilityFilter(); updateHsStatus(loadedFacilitiesMessage()); }
    else if (!hsFacilitiesLoading) ensureFacilitiesLoaded();
  } else {
    if (hsMap.hasLayer(hsFacilityLayer)) hsMap.removeLayer(hsFacilityLayer);
    updateHsStatus(offFacilitiesMessage());
  }
}

// Same cutoffs documented in app/health_systems_data.py — kept here as the
// single source of truth for how the legend labels its own tier bubbles.
function tierRangeLabel(tier) {
  return { small: "under 15", mid: "15–39", large: "40–89", major: "90+" }[tier] || "";
}

function renderHsLegend() {
  document.getElementById("hs-legend").innerHTML = `
    <div class="hs-legend-group">
      <span class="hs-legend-title">Operator size = hospital count</span>
      ${["small", "mid", "large", "major"].map(t => `
        <span class="hs-legend-item" title="${titleCase(t)}: ${tierRangeLabel(t)} hospitals">
          <svg width="${tierRadius("major") * 2 + 4}" height="${tierRadius("major") * 2 + 4}">
            <circle cx="${tierRadius("major") + 2}" cy="${tierRadius("major") + 2}" r="${tierRadius(t)}" fill="var(--muted)" fill-opacity="0.5"/>
          </svg>
          ${titleCase(t)} <span class="hs-legend-range">(${tierRangeLabel(t)})</span>
        </span>
      `).join("")}
    </div>
    ${hsColorLegendHtml()}
  `;
}

// Tier/ownership filters only touch the system layer — refresh just that (and the list, strip,
// legend) rather than re-checking the live hospital layer too.
function refreshHsOperators() {
  refreshHsAll();
}

// ---- compare-operators modal ----
// Computed on the spot from whatever CMS data is already loaded (or being
// loaded) for the facility layer — not a stored figure — so it reads as "—"
// rather than 0 until the fetch finishes. No bed total: CMS's Hospital
// General Information dataset doesn't publish bed counts.
function operatorLiveStats(name) {
  if (!hsFacilitiesLoaded) return null;
  return { count: hsAllFacilityMarkers.filter(m => m.companyKey === name).length };
}

function renderCompareModalBody() {
  const wrap = document.getElementById("hs-compare-table-wrap");
  if (!wrap) return;
  const sorted = [...HEALTH_SYSTEMS].sort((a, b) => b.hospital_count - a.hospital_count);
  const liveNote = hsFacilitiesLoaded ? "" : " (loading…)";
  wrap.innerHTML = `
    <table class="hs-compare-table">
      <thead>
        <tr>
          <th>Operator</th>
          <th>Tier</th>
          <th>Curated hospital count</th>
          <th>Matched on map${liveNote}</th>
          <th>Verified</th>
        </tr>
      </thead>
      <tbody>
        ${sorted.map(h => {
          const live = operatorLiveStats(h.name);
          return `
            <tr>
              <td><span class="hs-dot" style="background:var(${ownershipColorVar(h.ownership_type)})"></span>${esc(h.name)}</td>
              <td>${titleCase(h.tier)}</td>
              <td>${h.hospital_count}${h.confidence === "approximate" ? ` <span class="hs-compare-muted">(approx.)</span>` : ""}</td>
              <td>${live ? live.count.toLocaleString() : "—"}</td>
              <td>${esc(h.verified_at || "—")}</td>
            </tr>
          `;
        }).join("")}
      </tbody>
    </table>
  `;
}

function openCompareModal() {
  renderCompareModalBody();
  document.getElementById("hs-compare-overlay").hidden = false;
  document.body.classList.add("modal-open");
  if (!hsFacilitiesLoaded && !hsFacilitiesLoading) ensureFacilitiesLoaded();
}

function closeCompareModal() {
  document.getElementById("hs-compare-overlay").hidden = true;
  document.body.classList.remove("modal-open");
}

// The 26 curated operators are re-checked individually, not on one schedule,
// so this reports the actual spread of verified_at dates rather than a
// single "as of" date that would imply every entry was just re-checked.
function renderCuratedFreshness() {
  const dates = HEALTH_SYSTEMS.map(h => h.verified_at).filter(Boolean).sort();
  const el = document.getElementById("hs-curated-freshness");
  if (!el || !dates.length) return;
  const oldest = fmtDate(dates[0]), newest = fmtDate(dates[dates.length - 1]);
  el.textContent = oldest === newest
    ? `Curated operator list: every entry verified ${newest}.`
    : `Curated operator list: entries verified between ${oldest} and ${newest} — each has its own date, see "Compare operator size" or a card's source link.`;
}

function renderHealthSystems() {
  renderBdStrip();
  renderSystemCards(currentFilteredSystems());
  renderHsLegend();
  renderCuratedFreshness();
  setHsView(hsView); // re-applies which panel (map+list vs landscape) is showing

  if (typeof L === "undefined") {
    document.getElementById("hs-map").innerHTML = `<p style="text-align:center; color:var(--muted); font-size:12px;">Map library unavailable right now.</p>`;
    return;
  }

  ensureHsMap();
  if (!hsMap) return;
  hsMap.invalidateSize(); // the container may have been display:none while on another tab
  renderOperatorLayer();
  updateFacilityVisibility();
}

async function bootAtlas() {
  const [statesRes, healthSystemsRes, hospitalRosterRes, bdProfilesRes, ahrqRes] = await Promise.all([
    fetch("/api/states").then(r => r.json()).catch(() => ({ status_taxonomy: [], states: [] })),
    fetch("/api/health_systems").then(r => r.json()).catch(() => []),
    fetch("/api/hospital_roster").then(r => r.json()).catch(() => []),
    fetch("/api/bd_profiles").then(r => r.json()).catch(() => []),
    fetch("/api/ahrq_systems").then(r => r.json()).catch(() => null),
  ]);

  STAGES = (statesRes.status_taxonomy || []).map((key, i) => ({ key, order: i + 1, var: `--stage-${i + 1}` }));
  STATES = statesRes.states || [];
  HEALTH_SYSTEMS = healthSystemsRes;
  HOSPITAL_ROSTER = hospitalRosterRes;
  BD_PROFILES = Array.isArray(bdProfilesRes) ? bdProfilesRes : [];
  AHRQ_SYSTEMS = ahrqRes && Array.isArray(ahrqRes.systems) ? ahrqRes.systems : [];
  AHRQ_META = ahrqRes ? ahrqRes.meta : null;
  SYSTEMS_UNIFIED = buildUnifiedSystems();
  buildRosterIndex();
  populateCompanyFilter();

  document.getElementById("hs-layer-toggle").addEventListener("click", e => {
    const btn = e.target.closest("button[data-layer]");
    if (!btn) return;
    btn.classList.toggle("active");
    if (btn.dataset.layer === "operators") hsShowOperators = btn.classList.contains("active");
    if (btn.dataset.layer === "facilities") hsShowFacilities = btn.classList.contains("active");
    renderOperatorLayer();
    updateFacilityVisibility();
  });
  document.getElementById("hs-tier-toggle").addEventListener("click", e => {
    const btn = e.target.closest("button[data-tier]");
    if (!btn) return;
    hsTierFilter = btn.dataset.tier;
    document.querySelectorAll("#hs-tier-toggle button").forEach(b => b.classList.toggle("active", b === btn));
    refreshHsOperators();
  });
  document.getElementById("hs-ownership-toggle").addEventListener("click", e => {
    const btn = e.target.closest("button[data-ownership]");
    if (!btn) return;
    hsOwnershipFilter = btn.dataset.ownership;
    document.querySelectorAll("#hs-ownership-toggle button").forEach(b => b.classList.toggle("active", b === btn));
    refreshHsOperators();
  });
  document.getElementById("hs-company-filter").addEventListener("change", e => {
    hsCompanyFilter = e.target.value;
    applyFacilityFilter();
  });
  document.getElementById("hs-compare-btn").addEventListener("click", openCompareModal);
  document.getElementById("hs-compare-close").addEventListener("click", closeCompareModal);
  document.getElementById("hs-compare-overlay").addEventListener("click", e => {
    if (e.target.id === "hs-compare-overlay") closeCompareModal();
  });
  window.addEventListener("keydown", e => { if (e.key === "Escape") closeCompareModal(); });

  wireHsBdControls();
  // Deep link from the Radar's state pages: /atlas?state=West%20Virginia opens already filtered to that state.
  const wantedState = new URLSearchParams(location.search).get("state");
  if (wantedState && Object.values(STATE_ABBR).includes(wantedState)) {
    hsFilters.state = wantedState;
    syncHsControls();
  }
  renderHealthSystems();
  if (hsFilters.state !== "all" && hsMap) {
    const pts = SYSTEMS_UNIFIED.filter(s => s.state === hsFilters.state).map(s => [s.plotLat, s.plotLon]);
    if (pts.length) hsMap.fitBounds(L.latLngBounds(pts).pad(0.25));
  }
  refreshBdSession(); // async: reveals the Outreach tab if this browser already holds a valid session
}

initThemeToggle();
bootAtlas();
