// BD layer for the Health Systems tab. Loaded before app.js; everything here runs after
// app.js has fetched its data (it uses STATES / HEALTH_SYSTEMS / CMS_HOSPITALS_RAW / helpers
// from app.js at call time).
//
// The unit of record is a SYSTEM, not an RHTP state. One list merges:
//   - the sourced operator list (health_systems: size, ownership, HQ, source), and
//   - the unverified Atlas profiles (bd_profiles: category, strategy signals, note),
// joined by the hand-written crosswalk in app/bd_profiles_data.py. RHTP is only an optional
// overlay — the HQ state's pipeline stage — shown as a possible tailwind, never required.


const BD_CATEGORIES = {
  academic:      { label: "Academic Medical Center",      varName: "--cat-academic" },
  faith:         { label: "Faith-Based Nonprofit",        varName: "--cat-faith" },
  secular:       { label: "Secular Nonprofit",            varName: "--cat-secular" },
  forprofit:     { label: "Investor-Owned (For-Profit)",  varName: "--cat-forprofit" },
  payerprovider: { label: "Payer-Provider Integrated",    varName: "--cat-payerprovider" },
  public:        { label: "Public / Safety-Net",          varName: "--cat-public" },
  specialty:     { label: "Specialty (Peds / Oncology)",  varName: "--cat-specialty" },
  network:       { label: "Hospital network / alliance",  varName: "--cat-network" },
  association:   { label: "Association / intermediary",   varName: "--cat-association" },
  tribal:        { label: "Tribal / Indian health",       varName: "--cat-tribal" },
  university:    { label: "University",                   varName: "--cat-university" },
  fqhc:          { label: "Community health center (FQHC)", varName: "--cat-fqhc" },
  homehealth:    { label: "Home health agency",            varName: "--cat-homehealth" },
  hospital:      { label: "Community hospital",            varName: "--cat-hospital" },
};

const BD_STRATEGY_TAGS = {
  venture_arm: "Venture / innovation arm",
  digital_pilot: "Digital health pilots",
  vbc_leader: "Value-based care leader",
  rural_focus: "Rural / underserved focus",
  research_intensive: "Research-intensive",
  health_equity: "Health equity focus",
  limited_innovation: "Limited known innovation infra",
};

const BD_STATUS_ORDER = ["not_contacted", "researching", "contacted", "in_discussion", "piloting", "declined"];
const BD_STATUSES = {
  not_contacted: { label: "Not contacted", varName: "--bd-not_contacted" },
  researching:   { label: "Researching",   varName: "--bd-researching" },
  contacted:     { label: "Contacted",     varName: "--bd-contacted" },
  in_discussion: { label: "Intro in progress", varName: "--bd-in_discussion" },
  piloting:      { label: "Piloting",      varName: "--bd-piloting" },
  declined:      { label: "Declined",      varName: "--bd-declined" },
};

// What kind of entry each system is — shown as a "Type" label everywhere and usable as a filter:
//   operator   = hospital operator in the sourced list (hospital count + source link)
//   profile    = system from the BD profile list (category/strategy unverified; size from AHRQ when matched)
//   ahrq       = system that appears only in AHRQ's 2023 Compendium (sourced size and ownership)
//   nonsystem  = not a hospital system: a network, association, university or tribal health organization
//   provider   = a single community provider, not a system: health center (FQHC), home health agency, community hospital
const BD_TYPES = {
  operator:  { label: "Sourced operator",   hint: "Hospital operator in this site's sourced list, with a hospital count and source link" },
  profile:   { label: "Profile system",     hint: "System from the BD profile list; category and strategy are unverified, size comes from AHRQ when matched" },
  ahrq:      { label: "AHRQ system",        hint: "System from AHRQ's 2023 Compendium that is not in the curated list" },
  nonsystem: { label: "Network / association / other", hint: "Not a hospital system: a network, association, university or tribal health organization" },
  provider:  { label: "Community provider", hint: "A single provider, not a system: community health center (FQHC), home health agency or community hospital — from free public data (HRSA, CMS)" },
};
const BD_NONSYSTEM_CATEGORIES = new Set(["network", "association", "tribal", "university"]);
const BD_PROVIDER_CATEGORIES = new Set(["fqhc", "homehealth", "hospital"]);
function entityType(sys) {
  if (sys.profile && BD_NONSYSTEM_CATEGORIES.has(sys.profile.category)) return "nonsystem";
  if (sys.profile && BD_PROVIDER_CATEGORIES.has(sys.profile.category)) return "provider";
  if (sys.op) return "operator";
  return sys.profile ? "profile" : "ahrq";
}

const BD_TIER_ORDER = ["major", "large", "mid", "small", "unsized"];
const BD_RHTP_LABELS = {
  money: "Subawards announced or later",
  early: "Before subawards (RFA stage or earlier)",
  none: "State not tracked",
};

let BD_PROFILES = [];
let AHRQ_SYSTEMS = [];   // /api/ahrq_systems: AHRQ Compendium 2023 system file
let AHRQ_META = null;
let hsCardLimit = 60;    // cards rendered below the map; "Show more" raises it
let SYSTEMS_UNIFIED = [];
let BD_AUTH = { configured: false, authed: false };
let BD_OUTREACH = {}; // bd_key -> {status, owner, notes, updated_at}
let BD_STATE_NOTES = {}; // state abbr -> free-text note (private, e.g. how a round of email outreach went)

const hsFilters = { category: "all", strategy: "all", rhtp: "all", state: "all", status: "all", source: "all", q: "" };
let hsColorMode = "ownership"; // ownership | category | status
let hsView = "map";            // map | landscape
let lsSort = { key: "hospitals", dir: -1 };

function bdSlug(s) {
  return s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
}

function escAttr(s) {
  return esc(s).replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

function stateNameToAbbr(name) {
  return Object.keys(STATE_ABBR).find(k => STATE_ABBR[k] === name) || "";
}

// ---------- unified systems model ----------

function rhtpSignal(stateName) {
  const s = STATES.find(x => x.state === stateName);
  if (!s) return null;
  const ev = latestConfirmedEvent(s);
  return {
    state: s.state,
    stage: ev ? ev.status : null,
    idx: ev ? stageIndex(ev.status) : -1,
    amount: s.total_awarded != null ? s.total_awarded : null,
  };
}

function rhtpBucket(sig) {
  if (!sig || sig.idx < 0) return "none";
  return sig.idx >= 3 ? "money" : "early";
}

function buildUnifiedSystems() {
  const profileByOperator = {};
  BD_PROFILES.forEach(p => { if (p.operator_name) profileByOperator[p.operator_name] = p; });
  const ahrqByKey = {};
  AHRQ_SYSTEMS.forEach(a => { if (a.bd_key) ahrqByKey[a.bd_key] = a; });
  const out = [];

  HEALTH_SYSTEMS.forEach(h => {
    const p = profileByOperator[h.name] || null;
    out.push({
      key: bdSlug(h.name), name: h.name, op: h, profile: p,
      ahrq: ahrqByKey[bdSlug(h.name)] || null,
      state: h.hq_state, city: h.hq_city, lat: h.hq_lat, lon: h.hq_lon,
      category: p ? p.category : null, tags: p ? p.strategy_tags : [],
    });
  });

  BD_PROFILES.filter(p => !p.operator_name).forEach(p => {
    const i = p.hq_place.lastIndexOf(", ");
    const city = i < 0 ? p.hq_place : p.hq_place.slice(0, i);
    const abbr = i < 0 ? "" : p.hq_place.slice(i + 2);
    out.push({
      key: p.bd_key, name: p.name, op: null, profile: p,
      ahrq: ahrqByKey[p.bd_key] || null,
      state: STATE_ABBR[abbr] || abbr, city, lat: p.hq_lat, lon: p.hq_lon,
      category: p.category, tags: p.strategy_tags,
    });
  });

  // AHRQ systems that match nothing in our own lists become entries of their own.
  const byKey = {};
  out.forEach(s => { byKey[s.key] = s; });
  AHRQ_SYSTEMS.filter(a => !a.bd_key).forEach(a => {
    if (a.merged_into && byKey[a.merged_into]) {      // 2023 system that has since merged into one of ours
      (byKey[a.merged_into].ahrqAlso = byKey[a.merged_into].ahrqAlso || []).push(a);
      return;
    }
    out.push({
      key: "ahrq-" + a.sys_id.toLowerCase(), name: a.name, op: null, profile: null, ahrq: a,
      state: STATE_ABBR[a.state] || a.state, city: a.city, lat: a.lat, lon: a.lon,
      category: null, tags: [],
    });
  });

  out.forEach(s => {
    s.ahrqMatch = s.ahrq ? s.ahrq.match_type || null : null;
    s.partOf = s.profile ? s.profile.part_of : null;
    s.type = entityType(s);
    s.rhtp = rhtpSignal(s.state);
    s.rhtpBucket = rhtpBucket(s.rhtp);
    s.plotLat = s.lat;
    s.plotLon = s.lon;
  });

  // Systems headquartered in the same city would stack into one pin. Spread each such group on a
  // small ring (about 3 miles) so every one stays clickable; lat/lon keep the true city position.
  const groups = {};
  out.forEach(s => { (groups[`${s.lat.toFixed(2)},${s.lon.toFixed(2)}`] = groups[`${s.lat.toFixed(2)},${s.lon.toFixed(2)}`] || []).push(s); });
  Object.values(groups).filter(g => g.length > 1).forEach(g => {
    g.sort((a, b) => a.name.localeCompare(b.name)).forEach((s, i) => {
      const angle = (2 * Math.PI * i) / g.length;
      s.plotLat = s.lat + 0.045 * Math.sin(angle);
      s.plotLon = s.lon + 0.06 * Math.cos(angle);
    });
  });
  // Two different organizations can share a name (Memorial Health System in IL and OH): say which.
  const nameCount = {};
  out.forEach(s => { nameCount[s.name] = (nameCount[s.name] || 0) + 1; });
  out.forEach(s => { if (nameCount[s.name] > 1) s.name = `${s.name} (${stateNameToAbbr(s.state) || s.state})`; });
  return out;
}

// Same cutoffs as the operator tiers (major >= 90 hospitals, large 40-89, mid 15-39, small < 15). A
// system's size comes from its own sourced operator record when it has one, else from AHRQ's count.
function tierFromHospitals(n) {
  if (n == null) return "unsized";
  return n >= 90 ? "major" : n >= 40 ? "large" : n >= 15 ? "mid" : "small";
}
function systemTier(sys) {
  if (sys.op) return sys.op.tier;
  return sys.ahrq ? tierFromHospitals(sys.ahrq.hospitals) : "unsized";
}
function systemSizeKey(sys) {
  if (sys.op) return sys.op.hospital_count;
  return sys.ahrq && sys.ahrq.hospitals != null ? sys.ahrq.hospitals : -1;
}

// Profile-only systems have no sourced ownership; it's derived from their (unverified)
// category, which is only used for the ownership filter and the default marker color.
function systemOwnership(sys) {
  if (sys.op) return sys.op.ownership_type;
  if (sys.ahrq && sys.ahrq.ownership) return sys.ahrq.ownership === "investor-owned" ? "for-profit" : sys.ahrq.ownership === "government" ? "government" : "nonprofit";
  if (sys.category === "public") return "government";
  if (sys.category === "forprofit") return "for-profit";
  return "nonprofit";
}

function systemStatus(key) {
  return (BD_OUTREACH[key] && BD_OUTREACH[key].status) || "not_contacted";
}

function currentFilteredSystems(ignoreStatus) {
  return SYSTEMS_UNIFIED.filter(sys => {
    if (hsTierFilter !== "all" && systemTier(sys) !== hsTierFilter) return false;
    if (hsOwnershipFilter !== "all" && systemOwnership(sys) !== hsOwnershipFilter) return false;
    if (hsFilters.category !== "all") {
      if (hsFilters.category === "none" ? !!sys.category : sys.category !== hsFilters.category) return false;
    }
    if (hsFilters.strategy !== "all" && !sys.tags.includes(hsFilters.strategy)) return false;
    if (hsFilters.rhtp !== "all" && sys.rhtpBucket !== hsFilters.rhtp) return false;
    if (hsFilters.state !== "all" && sys.state !== hsFilters.state) return false;
    if (hsFilters.source !== "all" && sys.type !== hsFilters.source) return false;
    if (hsFilters.q && !(sys.name + " " + sys.city).toLowerCase().includes(hsFilters.q)) return false;
    if (!ignoreStatus && hsFilters.status !== "all" && BD_AUTH.authed && systemStatus(sys.key) !== hsFilters.status) return false;
    return true;
  });
}

function systemColorVar(sys) {
  if (hsColorMode === "category" && sys.category) return BD_CATEGORIES[sys.category].varName;
  if (hsColorMode === "category") return "--owner-unknown";
  if (hsColorMode === "status" && BD_AUTH.authed) return BD_STATUSES[systemStatus(sys.key)].varName;
  const own = systemOwnership(sys);
  return own === "for-profit" ? "--owner-forprofit" : own === "government" ? "--owner-government" : "--owner-nonprofit";
}

// ---------- popup / card pieces ----------

function profileChipsHtml(sys) {
  if (!sys.profile) return "";
  const cat = BD_CATEGORIES[sys.profile.category];
  return `<span class="bd-chip bd-chip-cat" style="--chip:var(${cat.varName})">${esc(cat.label)}</span>`
    + sys.tags.map(t => `<span class="bd-chip">${esc(BD_STRATEGY_TAGS[t])}</span>`).join("");
}

function rhtpLineHtml(sys) {
  const r = sys.rhtp;
  if (!r || !r.stage) return `<div class="hs-popup-meta">RHTP: ${esc(sys.state)} isn't tracked on this site.</div>`;
  return `<div class="hs-popup-meta">RHTP tailwind (HQ state ${esc(r.state)}): ${esc(titleCase(r.stage))}`
    + `${r.amount ? ` · ${usdCompact(r.amount)} FY26 award` : ""}`
    + ` · <a href="/#state=${encodeURIComponent(r.state)}">state page</a> — a possible advantage, not a requirement.</div>`;
}

function statusPillHtml(key) {
  const st = BD_STATUSES[systemStatus(key)];
  return `<span class="bd-status-pill" style="--chip:var(${st.varName})">${esc(st.label)}</span>`;
}

function fmtN(n) { return n == null ? "—" : n.toLocaleString(); }

const AHRQ_OWNERSHIP_LABELS = {
  "nonprofit": "Nonprofit", "nonprofit-church": "Nonprofit (church-affiliated)",
  "government": "Government", "investor-owned": "Investor-owned",
};

// AHRQ's published figures for a system, as one line. Ownership is decoded from AHRQ's numeric
// code by inference (see app/ahrq_data.py), so it is labeled as such.
function ahrqLineHtml(sys) {
  const a = sys.ahrq;
  if (!a) return "";
  const bits = [
    `${fmtN(a.hospitals)} hospital${a.hospitals === 1 ? "" : "s"}`,
    a.beds != null ? `${fmtN(a.beds)} beds` : null,
    a.discharges != null ? `${fmtN(a.discharges)} discharges` : null,
    a.net_revenue ? `${usdCompact(a.net_revenue)} hospital net revenue` : null,
    a.physicians != null ? `${fmtN(a.physicians)} physicians` : null,
  ].filter(Boolean).join(" · ");
  const flags = [
    a.very_major_teaching ? "very major teaching hospital" : a.major_teaching ? "major teaching hospital" : null,
    a.high_dsh ? "high safety-net share (DSH)" : null,
    a.high_uc_burden ? "high uncompensated-care burden" : null,
    a.offers_insurance ? "offers an insurance product" : null,
    a.ownership ? `${AHRQ_OWNERSHIP_LABELS[a.ownership]} (AHRQ code, inferred)` : null,
  ].filter(Boolean);
  const matched = sys.ahrqMatch && sys.ahrqMatch !== "exact" ? ` Matched to AHRQ's "${esc(a.name)}" (${sys.ahrqMatch}).` : "";
  return `AHRQ ${AHRQ_META ? AHRQ_META.data_year : 2023}: ${bits}${flags.length ? " — " + flags.join(", ") : ""}.${matched}`;
}

function ahrqAlsoHtml(sys) {
  return (sys.ahrqAlso || []).map(a =>
    `AHRQ's 2023 file also lists <strong>${esc(a.name)}</strong> (${fmtN(a.hospitals)} hospitals) as a separate system — ${esc(a.merged_note || "since merged")}.`).join(" ");
}

function ahrqPlaceNote(sys) {
  return sys.ahrq && sys.ahrq.geo_precision === "state"
    ? " (pin at the state's hospital center: no hospital in the home-office city)" : "";
}

function systemPopupHtml(sys) {
  const h = sys.op, p = sys.profile, a = sys.ahrq;
  const own = systemOwnership(sys);
  const parts = [`<div class="hs-popup-title">${esc(sys.name)}</div>`,
    `<div class="hs-popup-meta" title="${escAttr(BD_TYPES[sys.type].hint)}">${esc(BD_TYPES[sys.type].label)}${sys.partOf ? ` · part of ${esc(sys.partOf)}` : ""}</div>`];
  if (h) {
    parts.push(`<div>${titleCase(h.tier)} operator · ${own === "for-profit" ? "For-profit" : "Nonprofit"}</div>`);
    parts.push(`<div>${h.hospital_count} hospitals · HQ ${esc(h.hq_city)}, ${esc(h.hq_state)}</div>`);
    if (h.confidence === "approximate") parts.push(`<div class="hs-popup-caution">Approximate count</div>`);
  } else if (p) {
    parts.push(`<div>${a ? "Profile + AHRQ figures" : "Profile only — no hospital-count record"}</div>`);
    parts.push(`<div>HQ ${esc(p.hq_place)}</div>`);
  } else if (a) {
    parts.push(`<div>${titleCase(systemTier(sys))} system · from AHRQ's Compendium (not in the curated list)</div>`);
    parts.push(`<div>Home office ${esc(a.city)}, ${esc(a.state)}${esc(ahrqPlaceNote(sys))}</div>`);
  }
  if (a) parts.push(`<div class="hs-popup-meta">${ahrqLineHtml(sys)}</div>`);
  if (sys.ahrqAlso) parts.push(`<div class="hs-popup-meta">${ahrqAlsoHtml(sys)}</div>`);
  if (p) {
    parts.push(`<div class="bd-chip-row">${profileChipsHtml(sys)}</div>`);
    parts.push(`<div>${esc(p.note)}</div>`);
    parts.push(`<div class="hs-popup-caution">Unverified profile — category, strategy signals and note have no per-row source.</div>`);
  }
  parts.push(rhtpLineHtml(sys));
  if (h) {
    parts.push(`<div class="hs-popup-meta">Verified ${esc(h.verified_at || "date unknown")}</div>`);
    parts.push(`<a href="${esc(h.source_url)}" target="_blank" rel="noopener">Source ↗</a>`);
  } else if (a && AHRQ_META) {
    parts.push(`<a href="${esc(AHRQ_META.source_url)}" target="_blank" rel="noopener">AHRQ Compendium ↗</a>`);
  }
  if (BD_AUTH.authed) {
    parts.push(`<div class="bd-popup-status">${statusPillHtml(sys.key)} <button type="button" class="bd-edit-link" data-bd-key="${escAttr(sys.key)}">Edit outreach</button></div>`);
  }
  return `<div class="hs-popup">${parts.join("")}</div>`;
}

function systemCardHtml(sys) {
  const h = sys.op, p = sys.profile, a = sys.ahrq;
  const own = systemOwnership(sys);
  const ownLabel = own === "for-profit" ? "For-profit" : own === "government" ? "Government" : "Nonprofit";
  const ownVar = own === "for-profit" ? "--owner-forprofit" : own === "government" ? "--owner-government" : "--owner-nonprofit";
  const tier = systemTier(sys);
  const sizePill = tier !== "unsized"
    ? `<span class="stage-pill" style="--stage-color:var(${tierColorVar(tier)})">${titleCase(tier)}</span>`
    : `<span class="stage-pill" style="--stage-color:var(--owner-unknown)">Unsized</span>`;
  const derived = !h && !a;
  const r = sys.rhtp;
  const rhtpPill = r && r.stage
    ? `<span class="bd-chip bd-chip-rhtp" title="RHTP stage of the HQ state — a possible tailwind, not a requirement">RHTP · ${esc(r.state)} · ${esc(titleCase(r.stage))}</span>`
    : "";
  const where = h ? `${esc(h.hq_city)}, ${esc(h.hq_state)}` : p ? esc(p.hq_place) : `${esc(a.city)}, ${esc(a.state)}`;
  return `
    <div class="hs-card" id="hs-row-${escAttr(sys.key)}">
      <div class="hs-card-head">
        ${sizePill}
        <h3>${esc(sys.name)}</h3>
        <span class="stage-pill" style="--stage-color:var(${ownVar})">${ownLabel}${derived ? " (derived)" : ""}</span>
        ${BD_AUTH.authed ? statusPillHtml(sys.key) : ""}
        ${h && h.confidence === "approximate" ? `<span class="caution-tag">Approximate count</span>` : ""}
      </div>
      <div class="hs-card-body">
        ${h ? `<span>${h.hospital_count} hospitals</span><span>HQ: ${where}</span><span>Verified ${esc(h.verified_at || "date unknown")}</span>`
            : `<span>${a ? `${fmtN(a.hospitals)} hospital${a.hospitals === 1 ? "" : "s"} (AHRQ)` : "No hospital-count record"}</span><span>${p ? "HQ" : "Home office"}: ${where}</span>`}
      </div>
      ${a ? `<p class="hs-notes">${ahrqLineHtml(sys)}</p>` : ""}
      <div class="bd-chip-row">
        <span class="bd-chip bd-chip-type" title="${escAttr(BD_TYPES[sys.type].hint)}">${esc(BD_TYPES[sys.type].label)}</span>
        ${sys.partOf ? `<span class="bd-chip">Part of ${esc(sys.partOf)}</span>` : ""}
        ${a && (h || p) ? `<span class="bd-chip" title="Also found in AHRQ's 2023 Compendium (${esc(sys.ahrqMatch || "exact")} match)">also in AHRQ</span>` : ""}
        ${p ? profileChipsHtml(sys) : ""}${rhtpPill}
      </div>
      ${sys.ahrqAlso ? `<p class="hs-notes">${ahrqAlsoHtml(sys)}</p>` : ""}
      ${h && h.notes ? `<p class="hs-notes">${esc(h.notes)}</p>` : ""}
      ${p ? `<p class="hs-notes bd-unverified">${esc(p.note)} <span class="caution-tag">Unverified profile</span></p>` : ""}
      ${h ? `<a class="tl-source" href="${esc(h.source_url)}" target="_blank" rel="noopener">Source ↗</a>`
          : a && AHRQ_META ? `<a class="tl-source" href="${esc(AHRQ_META.source_url)}" target="_blank" rel="noopener">AHRQ Compendium ↗</a>` : ""}
    </div>`;
}

function renderSystemCards(list) {
  const sorted = [...list].sort((a, b) => {
    const d = systemSizeKey(b) - systemSizeKey(a);
    return d !== 0 ? d : a.name.localeCompare(b.name);
  });
  const shown = sorted.slice(0, hsCardLimit);
  const more = sorted.length - shown.length;
  document.getElementById("hs-list").innerHTML = (shown.map(systemCardHtml).join("")
    || `<p style="text-align:center; color:var(--muted); padding:24px 0;">No systems match these filters.</p>`)
    + (more > 0 ? `<button type="button" class="hs-compare-btn hs-more-btn" id="hs-more-btn">Show ${Math.min(60, more)} more (${more.toLocaleString()} not shown)</button>` : "");
}

// ---------- legend ----------

function hsColorLegendHtml() {
  let title, items;
  if (hsColorMode === "category") {
    title = "Color = category (unverified profile)";
    items = Object.keys(BD_CATEGORIES).map(k =>
      `<span class="hs-legend-item"><span class="hs-dot" style="background:var(${BD_CATEGORIES[k].varName})"></span>${esc(BD_CATEGORIES[k].label)}</span>`)
      .concat(`<span class="hs-legend-item"><span class="hs-dot" style="background:var(--owner-unknown)"></span>No profile yet</span>`);
  } else if (hsColorMode === "status" && BD_AUTH.authed) {
    title = "Color = contact status";
    items = BD_STATUS_ORDER.map(k =>
      `<span class="hs-legend-item"><span class="hs-dot" style="background:var(${BD_STATUSES[k].varName})"></span>${esc(BD_STATUSES[k].label)}</span>`);
  } else {
    title = "Color = ownership";
    items = [
      `<span class="hs-legend-item" title="Tax-exempt / mission-driven operator, as reported by the source"><span class="hs-dot" style="background:var(--owner-nonprofit)"></span>Nonprofit</span>`,
      `<span class="hs-legend-item" title="Investor- or privately-owned operator, as reported by the source"><span class="hs-dot" style="background:var(--owner-forprofit)"></span>For-profit</span>`,
      `<span class="hs-legend-item" title="Federal, state, or county-run facility. For profile-only systems this is derived from their unverified category"><span class="hs-dot" style="background:var(--owner-government)"></span>Government</span>`,
    ];
  }
  return `
    <div class="hs-legend-group"><span class="hs-legend-title">${title}</span>${items.join("")}</div>
    <div class="hs-legend-group"><span class="hs-legend-item" title="Systems from the Atlas profile list that have no sourced hospital count"><svg width="14" height="14"><circle cx="7" cy="7" r="5" fill="var(--muted)" fill-opacity="0.35" stroke="var(--ink)" stroke-width="1.5" stroke-dasharray="3 2"/></svg>Dashed outline = profile only (no hospital-count record)</span></div>`;
}

// ---------- BD API + session ----------

async function bdFetch(path, opts = {}) {
  const res = await fetch(path, {
    credentials: "same-origin",
    ...opts,
    headers: { "Content-Type": "application/json", ...(opts.headers || {}) },
  });
  let data = null;
  try { data = await res.json(); } catch { /* non-JSON error body */ }
  return { ok: res.ok, status: res.status, data };
}

async function refreshBdSession() {
  try {
    const s = await bdFetch("/api/bd/session");
    if (s.ok && s.data) BD_AUTH = { configured: !!s.data.configured, authed: !!s.data.authed };
    if (BD_AUTH.authed) { await loadOutreach(); await loadStateNotes(); }
  } catch { /* leave locked */ }
  syncHsControls();
  refreshHsAll();
}

async function loadStateNotes() {
  BD_STATE_NOTES = {};
  const r = await bdFetch("/api/bd/state_notes");
  if (r.ok) r.data.forEach(x => { BD_STATE_NOTES[x.abbr] = x.note; });
}

const stateNoteTimers = {};
function saveStateNote(abbr, note, rowEl) {
  BD_STATE_NOTES[abbr] = note;
  const ind = rowEl && rowEl.querySelector(".bd-save-note");
  if (ind) ind.textContent = "Saving…";
  clearTimeout(stateNoteTimers[abbr]);
  stateNoteTimers[abbr] = setTimeout(async () => {
    try {
      const r = await bdFetch(`/api/bd/state_notes/${abbr}`, { method: "PUT", body: JSON.stringify({ note: BD_STATE_NOTES[abbr] }) });
      if (ind) ind.textContent = r.ok ? "Saved" : ((r.data && r.data.error) || "Couldn't save.");
    } catch { if (ind) ind.textContent = "Couldn't reach the server."; }
  }, 600);
}

function renderStateNotes() {
  const el = document.getElementById("bd-state-notes-body");
  if (!el) return;
  const abbrs = Object.keys(BD_STATE_NOTES).sort((a, b) => STATE_ABBR[a].localeCompare(STATE_ABBR[b]));
  const free = Object.keys(STATE_ABBR).filter(a => !(a in BD_STATE_NOTES));
  el.innerHTML = (abbrs.map(a => `
      <div class="bd-state-note">
        <label for="sn-${a}">${esc(STATE_ABBR[a])}</label>
        <textarea id="sn-${a}" rows="4" maxlength="5000" data-state-note="${a}">${esc(BD_STATE_NOTES[a])}</textarea>
        <span class="bd-save-note"></span>
      </div>`).join("") || `<p class="ls-note">No state notes yet.</p>`)
    + `<div class="bd-state-add"><select id="bd-state-add" aria-label="State">${free.map(a => `<option value="${a}">${esc(STATE_ABBR[a])}</option>`).join("")}</select>
        <button type="button" class="hs-compare-btn" id="bd-state-add-btn">Add a state note</button></div>`;
}

async function loadOutreach() {
  const r = await bdFetch("/api/bd/outreach");
  if (r.status === 401) { BD_AUTH.authed = false; BD_OUTREACH = {}; return; }
  if (!r.ok) return;
  BD_OUTREACH = {};
  r.data.forEach(row => { BD_OUTREACH[row.bd_key] = row; });
}

async function bdLogin(username, password) {
  const r = await bdFetch("/api/bd/login", { method: "POST", body: JSON.stringify({ username, password }) });
  if (!r.ok) return (r.data && r.data.error) || "Couldn't unlock.";
  BD_AUTH.authed = true;
  await loadOutreach();
  await loadStateNotes();
  return null;
}

async function bdLogout() {
  await bdFetch("/api/bd/logout", { method: "POST" });
  BD_AUTH.authed = false;
  BD_OUTREACH = {};
  BD_STATE_NOTES = {};
  if (hsColorMode === "status") hsColorMode = "ownership";
  hsFilters.status = "all";
}

const bdTimers = {};
const bdPending = {}; // key -> fields edited since the last save; merged so rapid edits to different fields all go out
function saveOutreach(key, patch, rowEl) {
  BD_OUTREACH[key] = { bd_key: key, status: "not_contacted", owner: "", notes: "", ...(BD_OUTREACH[key] || {}), ...patch };
  bdPending[key] = { ...(bdPending[key] || {}), ...patch };
  const note = rowEl && rowEl.querySelector(".bd-save-note");
  if (note) note.textContent = "Saving…";
  clearTimeout(bdTimers[key]);
  bdTimers[key] = setTimeout(async () => {
    const body = bdPending[key];
    delete bdPending[key];
    try {
      const r = await bdFetch(`/api/bd/outreach/${encodeURIComponent(key)}`, { method: "PUT", body: JSON.stringify(body) });
      if (r.status === 401) { BD_AUTH.authed = false; syncHsControls(); refreshHsAll(); setHsView("map"); openSignIn(); return; }
      if (!r.ok) {
        bdPending[key] = { ...body, ...(bdPending[key] || {}) }; // retry with the next edit
        if (note) note.textContent = (r.data && r.data.error) || "Couldn't save.";
        return;
      }
      BD_OUTREACH[key] = { ...r.data, ...(bdPending[key] || {}) }; // keep anything typed while this request was in flight
      if (note) note.textContent = "Saved";
      refreshHsAll(true); // counts update; the table is left alone so the row being edited doesn't jump away
    } catch {
      bdPending[key] = { ...body, ...(bdPending[key] || {}) };
      if (note) note.textContent = "Couldn't reach the server — will retry on your next edit.";
    }
  }, 500);
}

// ---------- BD modal ----------

let bdModalSearch = "";

function openSignIn() {
  document.getElementById("bd-overlay").hidden = false;
  document.body.classList.add("modal-open");
  renderSignIn();
}

// Opens the Outreach tab (optionally pre-searched); signed-out visitors get the sign-in dialog instead.
function openOutreach(searchText) {
  if (!BD_AUTH.authed) { openSignIn(); return; }
  bdModalSearch = searchText || "";
  if (searchText) { // looking up one system: clear the other filters so it can't be hidden by them
    Object.assign(hsFilters, { category: "all", strategy: "all", rhtp: "all", state: "all", status: "all", source: "all", q: "" });
    hsTierFilter = "all"; hsOwnershipFilter = "all";
    syncHsControls();
    refreshHsAll();
  }
  setHsView("outreach");
}

function closeBdModal() {
  document.getElementById("bd-overlay").hidden = true;
  document.body.classList.remove("modal-open");
}

function bdRowHtml(sys) {
  const rec = BD_OUTREACH[sys.key] || { status: "not_contacted", owner: "", notes: "", updated_at: null };
  const cat = sys.category ? BD_CATEGORIES[sys.category].label : "—";
  const opts = BD_STATUS_ORDER.map(k => `<option value="${k}"${rec.status === k ? " selected" : ""}>${esc(BD_STATUSES[k].label)}</option>`).join("");
  return `
    <tr data-bd-row="${escAttr(sys.key)}">
      <td class="bd-col-name"><strong>${esc(sys.name)}</strong><div class="bd-sub">${esc(BD_TYPES[sys.type].label)} · ${esc(cat)}${sys.op ? ` · ${sys.op.hospital_count} hospitals` : sys.ahrq ? ` · ${fmtN(sys.ahrq.hospitals)} hospitals (AHRQ)` : " · unsized"}</div></td>
      <td>${esc(sys.state)}</td>
      <td><select data-bd-field="status" data-bd-key="${escAttr(sys.key)}">${opts}</select></td>
      <td><input type="text" maxlength="120" data-bd-field="owner" data-bd-key="${escAttr(sys.key)}" value="${escAttr(rec.owner)}" placeholder="Who owns this"></td>
      <td><textarea rows="1" maxlength="5000" data-bd-field="notes" data-bd-key="${escAttr(sys.key)}" placeholder="Contact history, next step…">${esc(rec.notes)}</textarea></td>
      <td class="bd-col-meta"><span class="bd-save-note">${rec.updated_at ? esc(new Date(rec.updated_at).toLocaleDateString("en-US", { month: "short", day: "numeric" })) : ""}</span></td>
    </tr>`;
}

function renderBdTable() {
  const wrap = document.getElementById("bd-table-wrap");
  if (!wrap) return;
  const q = bdModalSearch.trim().toLowerCase();
  // Follows the filters above (state, type, status pills …); only the search box is local to this table.
  const rows = currentFilteredSystems()
    .filter(s => !q || (s.name + " " + s.state).toLowerCase().includes(q))
    .sort((a, b) => a.name.localeCompare(b.name));
  const count = document.getElementById("bd-count");
  if (count) count.textContent = `${rows.length.toLocaleString()} of ${SYSTEMS_UNIFIED.length.toLocaleString()} systems — follows the filters above`;
  wrap.innerHTML = `
    <table class="bd-table">
      <thead><tr><th>System</th><th>HQ state</th><th>Status</th><th>Owner</th><th>Notes</th><th></th></tr></thead>
      <tbody>${rows.map(bdRowHtml).join("") || `<tr><td colspan="6" class="bd-empty">No systems match.</td></tr>`}</tbody>
    </table>`;
}

function renderSignIn() {
  const body = document.getElementById("bd-modal-body");
  if (!BD_AUTH.configured) {
    body.innerHTML = `<p class="modal-caption">Sign-in isn't set up on this server yet. Set the <code>BD_PASSWORD</code> environment variable and redeploy.</p>`;
    return;
  }
  body.innerHTML = `
    <p class="modal-caption">For the team: signing in opens the Outreach tab — who has been contacted, by whom, and what's next. Everything else in the Atlas is public.</p>
    <form id="bd-login-form" class="bd-login">
      <input type="text" id="bd-username" autocomplete="username" value="bd" aria-label="ID" required>
      <input type="password" id="bd-password" autocomplete="current-password" placeholder="Password" aria-label="Password" required>
      <button type="submit" class="hs-compare-btn">Sign in</button>
    </form>
    <p class="bd-login-error" id="bd-login-error" role="alert"></p>`;
  document.getElementById("bd-password").focus(); // the ID is prefilled; the password is what the person types
}

function renderOutreachPanel() {
  const el = document.getElementById("hs-outreach");
  if (!el) return;
  if (!BD_AUTH.authed) { el.innerHTML = ""; return; }
  el.innerHTML = `
    <p class="cal-caption">Anything not logged here is "Not contacted". Edits save automatically and are shared with everyone who has the password. Use the filters and status buttons above (for example State → West Virginia) to narrow the list.</p>
    <p class="cal-caption" id="bd-count"></p>
    <details class="bd-state-notes" open>
      <summary>State notes</summary>
      <div id="bd-state-notes-body"></div>
    </details>
    <div class="bd-toolbar">
      <input type="search" id="bd-search" placeholder="Search system or state…" value="${escAttr(bdModalSearch)}" aria-label="Search systems">
      <button type="button" class="hs-compare-btn" id="bd-lock-btn">Sign out</button>
    </div>
    <div class="bd-table-wrap" id="bd-table-wrap"></div>`;
  renderStateNotes();
  renderBdTable();
}

// ---------- national landscape ----------

function facilityBucket(owner) {
  return facilityOwnerColorVar(owner).replace("--owner-", ""); // nonprofit | forprofit | government | unknown
}

function lsCell(n) { return n ? `<td class="num">${n.toLocaleString()}</td>` : `<td class="num ls-zero">·</td>`; }

function sumOf(list, key) { return list.reduce((n, s) => n + (s[key] || 0), 0); }

// National breakdown from AHRQ's Compendium (all 639 systems, sourced figures): size band x ownership,
// then which kinds of systems have which features. Independent of the curated list.
function ahrqSectionHtml() {
  if (!AHRQ_SYSTEMS.length) return `<p class="ls-note">AHRQ data isn't available right now.</p>`;
  const bands = [
    ["90+ hospitals", n => n >= 90], ["40–89", n => n >= 40 && n < 90], ["15–39", n => n >= 15 && n < 40],
    ["5–14", n => n >= 5 && n < 15], ["2–4", n => n >= 2 && n < 5], ["1 hospital", n => n === 1],
  ];
  const owns = ["nonprofit", "nonprofit-church", "government", "investor-owned"];
  const sized = AHRQ_SYSTEMS.filter(s => s.hospitals != null);
  const bandRows = bands.map(([label, test]) => {
    const g = sized.filter(s => test(s.hospitals));
    return `<tr><td>${label}</td>${owns.map(o => lsCell(g.filter(s => s.ownership === o).length)).join("")}
      <td class="num"><strong>${g.length}</strong></td>${lsCell(sumOf(g, "hospitals"))}${lsCell(sumOf(g, "beds"))}
      <td class="num">${sumOf(g, "net_revenue") ? usdCompact(sumOf(g, "net_revenue")) : "·"}</td></tr>`;
  }).join("");
  const tot = o => sized.filter(s => s.ownership === o).length;
  const bedsAll = sumOf(AHRQ_SYSTEMS, "beds");
  const features = [
    ["Includes a major teaching hospital", s => s.major_teaching],
    ["Includes a very major teaching hospital", s => s.very_major_teaching],
    ["Includes a high-safety-net-share (DSH) hospital", s => s.high_dsh],
    ["High uncompensated-care burden", s => s.high_uc_burden],
    ["Offers an insurance product", s => s.offers_insurance],
  ];
  const featRows = features.map(([label, test]) => {
    const known = AHRQ_SYSTEMS.filter(s => test(s) != null);
    const yes = known.filter(s => test(s));
    return `<tr><td>${label}</td>${lsCell(yes.length)}<td class="num">${known.length ? Math.round(yes.length / known.length * 100) + "%" : "·"}</td>
      ${lsCell(sumOf(yes, "hospitals"))}${lsCell(sumOf(yes, "beds"))}<td class="num">${bedsAll ? Math.round(sumOf(yes, "beds") / bedsAll * 100) + "%" : "·"}</td></tr>`;
  }).join("");
  const year = AHRQ_META ? AHRQ_META.data_year : 2023;
  return `
    <h3 class="ls-h">All U.S. health systems by size and ownership (AHRQ ${year})</h3>
    <div class="ls-wrap"><table class="ls-table">
      <thead><tr><th>System size</th><th class="num">Nonprofit</th><th class="num">Nonprofit, church-affiliated</th><th class="num">Government</th><th class="num">Investor-owned</th>
        <th class="num">Systems</th><th class="num">Hospitals</th><th class="num">Beds</th><th class="num">Hospital net revenue</th></tr></thead>
      <tbody>${bandRows}</tbody>
      <tfoot><tr><td>All AHRQ systems</td>${owns.map(o => `<td class="num">${tot(o)}</td>`).join("")}<td class="num">${sized.length}</td>
        <td class="num">${sumOf(sized, "hospitals").toLocaleString()}</td><td class="num">${bedsAll.toLocaleString()}</td><td class="num">${usdCompact(sumOf(AHRQ_SYSTEMS, "net_revenue"))}</td></tr></tfoot>
    </table></div>
    <ul class="ls-notes">
      <li>A system = at least one hospital and one physician group under common ownership. Stand-alone and specialty hospitals aren't counted.</li>
      <li>2023 data: later mergers aren't reflected.</li>
      <li>Ownership is decoded from AHRQ's numeric code by inference — check AHRQ's documentation before relying on one system's label.</li>
    </ul>

    <h3 class="ls-h">What those systems include (AHRQ ${year})</h3>
    <div class="ls-wrap"><table class="ls-table">
      <thead><tr><th>Feature</th><th class="num">Systems</th><th class="num">Share of systems</th><th class="num">Their hospitals</th><th class="num">Their beds</th><th class="num">Share of all beds</th></tr></thead>
      <tbody>${featRows}</tbody>
    </table></div>`;
}

function renderLandscape() {
  const el = document.getElementById("hs-landscape");
  if (!el) return;

  // A. category x size, over the unified list
  const cats = [...Object.keys(BD_CATEGORIES), "none"];
  const grid = {};
  cats.forEach(c => { grid[c] = {}; BD_TIER_ORDER.forEach(t => { grid[c][t] = 0; }); });
  SYSTEMS_UNIFIED.forEach(s => { grid[s.category || "none"][systemTier(s)]++; });
  const tierLabel = { major: "Major (90+)", large: "Large (40–89)", mid: "Mid (15–39)", small: "Small (<15)", unsized: "Unsized" };
  const colTot = {}; BD_TIER_ORDER.forEach(t => { colTot[t] = cats.reduce((n, c) => n + grid[c][t], 0); });
  const catRows = cats.map(c => {
    const label = c === "none" ? "No profile yet (sourced size only)" : BD_CATEGORIES[c].label;
    const dot = c === "none" ? "--owner-unknown" : BD_CATEGORIES[c].varName;
    const total = BD_TIER_ORDER.reduce((n, t) => n + grid[c][t], 0);
    return `<tr><td><span class="hs-dot" style="background:var(${dot})"></span> ${esc(label)}</td>
      ${BD_TIER_ORDER.map(t => grid[c][t]
        ? `<td class="num"><button type="button" class="ls-cell" data-ls-cat="${c}" data-ls-tier="${t}">${grid[c][t]}</button></td>`
        : `<td class="num ls-zero">·</td>`).join("")}
      <td class="num"><strong>${total}</strong></td></tr>`;
  }).join("");

  // B. states
  const haveCms = Array.isArray(CMS_HOSPITALS_RAW);
  const perState = {};
  Object.keys(STATE_ABBR).forEach(a => { perState[a] = { abbr: a, name: STATE_ABBR[a], total: 0, nonprofit: 0, forprofit: 0, government: 0, other: 0, critical: 0, systems: 0, unsized: 0, beds: 0, contacted: 0 }; });
  if (haveCms) {
    CMS_HOSPITALS_RAW.forEach(p => {
      const row = perState[p.state];
      if (!row) return;
      row.total++;
      const bk = facilityBucket(p.ownership);
      if (bk === "nonprofit" || bk === "forprofit" || bk === "government") row[bk]++; else row.other++;
      if (p.type === "Critical Access Hospitals") row.critical++;
    });
  }
  SYSTEMS_UNIFIED.forEach(s => {
    const row = perState[stateNameToAbbr(s.state)];
    if (!row) return;
    row.systems++;
    if (systemTier(s) === "unsized") row.unsized++;
    if (s.ahrq && s.ahrq.beds) row.beds += s.ahrq.beds;
    if (BD_AUTH.authed && systemStatus(s.key) !== "not_contacted") row.contacted++;
  });
  const stateRows = Object.values(perState).map(r => {
    const sig = rhtpSignal(r.name);
    return { ...r, rhtp: sig, rhtpIdx: sig ? sig.idx : -2, award: sig && sig.amount ? sig.amount : 0 };
  });
  const sortKeys = { name: r => r.name, hospitals: r => r.total, nonprofit: r => r.nonprofit, forprofit: r => r.forprofit,
    government: r => r.government, critical: r => r.critical, systems: r => r.systems, beds: r => r.beds, rhtp: r => r.rhtpIdx, award: r => r.award };
  const keyFn = sortKeys[lsSort.key] || sortKeys.hospitals;
  stateRows.sort((a, b) => {
    const x = keyFn(a), y = keyFn(b);
    const c = typeof x === "string" ? x.localeCompare(y) : x - y;
    return c !== 0 ? c * lsSort.dir : a.name.localeCompare(b.name);
  });
  const th = (key, label, num) => `<th class="${num ? "num " : ""}ls-sortable${lsSort.key === key ? " sorted" : ""}" data-ls-sort="${key}">${label}${lsSort.key === key ? (lsSort.dir < 0 ? " ↓" : " ↑") : ""}</th>`;
  const stateBody = stateRows.map(r => `
    <tr>
      <td><button type="button" class="ls-cell ls-state" data-ls-state="${r.abbr}">${esc(r.name)}</button></td>
      ${haveCms ? lsCell(r.total) + lsCell(r.nonprofit) + lsCell(r.forprofit) + lsCell(r.government) + lsCell(r.critical) : `<td class="num" colspan="5">—</td>`}
      <td class="num">${r.systems ? `${r.systems}${r.unsized ? ` <span class="ls-sub">(${r.unsized} unsized)</span>` : ""}` : `<span class="ls-zero">·</span>`}${BD_AUTH.authed && r.systems ? ` <span class="ls-sub">${r.contacted} contacted</span>` : ""}</td>
      ${lsCell(r.beds)}
      <td>${r.rhtp && r.rhtp.stage ? `<span class="stage-pill" style="--stage-color:${stageVar(r.rhtp.stage)}">${esc(titleCase(r.rhtp.stage))}</span>` : `<span class="ls-zero">not tracked</span>`}</td>
      <td class="num">${r.award ? usdCompact(r.award) : "·"}</td>
    </tr>`).join("");

  // C. facility types and parent attribution
  let typeBlock = `<p class="ls-note">Loading the CMS hospital layer…</p>`;
  if (haveCms) {
    const types = {};
    CMS_HOSPITALS_RAW.forEach(p => { const t = p.type || "Unknown"; types[t] = (types[t] || 0) + 1; });
    const max = Math.max(...Object.values(types));
    const named = hsAllFacilityMarkers.filter(m => m.companyKey !== "unmatched").length;
    typeBlock = `
      <div class="ls-bars">
        ${Object.entries(types).sort((a, b) => b[1] - a[1]).map(([t, n]) => `
          <div class="ls-bar-row"><span class="ls-bar-label">${esc(titleCase(t.toLowerCase()))}</span>
            <span class="ls-bar"><span style="width:${Math.max(2, Math.round(n / max * 100))}%"></span></span>
            <span class="ls-bar-n">${n.toLocaleString()}</span></div>`).join("")}
      </div>
      <ul class="ls-notes">
        <li><strong>${named.toLocaleString()}</strong> of ${CMS_HOSPITALS_RAW.length.toLocaleString()} hospitals (${Math.round(named / CMS_HOSPITALS_RAW.length * 100)}%) are tied to a named parent.</li>
        <li>"Parent not identified" is a limit of the sourced rosters, not proof a hospital is independent.</li>
      </ul>`;
  }

  el.innerHTML = `
    <ul class="atlas-about">
      <li><strong>${SYSTEMS_UNIFIED.length.toLocaleString()}</strong> systems listed individually (operators, BD profiles, AHRQ systems); CMS adds every Medicare hospital but not its owner.</li>
      <li>Click a count or a state to open the map filtered to it.</li>
    </ul>

    ${ahrqSectionHtml()}

    <h3 class="ls-h">This site's systems by category and size</h3>
    <div class="ls-wrap"><table class="ls-table">
      <thead><tr><th>Category (unverified profile)</th>${BD_TIER_ORDER.map(t => `<th class="num">${tierLabel[t]}</th>`).join("")}<th class="num">Total</th></tr></thead>
      <tbody>${catRows}</tbody>
      <tfoot><tr><td>All systems</td>${BD_TIER_ORDER.map(t => `<td class="num">${colTot[t]}</td>`).join("")}<td class="num">${SYSTEMS_UNIFIED.length}</td></tr></tfoot>
    </table></div>
    <ul class="ls-notes">
      <li>Size = the operator's own hospital count, else AHRQ's. "Unsized" = neither (networks, associations, some profiles).</li>
      <li>Categories exist only for the curated profiles.</li>
    </ul>

    <h3 class="ls-h">By state</h3>
    <div class="ls-wrap"><table class="ls-table ls-states">
      <thead><tr>${th("name", "State")}${th("hospitals", "CMS hospitals", true)}${th("nonprofit", "Nonprofit", true)}${th("forprofit", "For-profit", true)}${th("government", "Government", true)}${th("critical", "Critical access", true)}${th("systems", "Systems HQ'd here", true)}${th("beds", "Their beds (AHRQ)", true)}${th("rhtp", "RHTP stage")}${th("award", "FY26 award", true)}</tr></thead>
      <tbody>${stateBody}</tbody>
    </table></div>
    <ul class="ls-notes">
      <li>RHTP columns are context only — systems are listed whether or not their state is moving.</li>
      <li>"Their beds" = AHRQ beds of systems headquartered in the state, wherever those beds are.</li>
    </ul>

    <h3 class="ls-h">Hospitals by type (CMS)</h3>
    ${typeBlock}`;
}

// ---------- controls + refresh ----------

function setHsView(view) {
  if (view === "outreach" && !BD_AUTH.authed) view = "map";
  hsView = view;
  const map = view === "map";
  document.getElementById("hs-map-section").hidden = !map;
  document.getElementById("hs-list").hidden = !map;
  document.getElementById("hs-landscape").hidden = view !== "landscape";
  document.getElementById("hs-outreach").hidden = view !== "outreach";
  document.querySelectorAll("#hs-view-toggle button").forEach(b => b.classList.toggle("active", b.dataset.view === view));
  if (map) {
    if (hsMap) hsMap.invalidateSize();
  } else if (view === "landscape") {
    renderLandscape();
    if (typeof ensureFacilitiesLoaded === "function") ensureFacilitiesLoaded();
  } else {
    renderOutreachPanel();
  }
}

function fillSelect(id, options, current) {
  const sel = document.getElementById(id);
  sel.innerHTML = options.map(([v, l]) => `<option value="${escAttr(v)}">${esc(l)}</option>`).join("");
  sel.value = current;
}

function syncHsControls() {
  fillSelect("hs-category-filter", [["all", "All categories"], ...Object.keys(BD_CATEGORIES).map(k => [k, BD_CATEGORIES[k].label]), ["none", "No profile yet"]], hsFilters.category);
  fillSelect("hs-strategy-filter", [["all", "Any signal"], ...Object.keys(BD_STRATEGY_TAGS).map(k => [k, BD_STRATEGY_TAGS[k]])], hsFilters.strategy);
  fillSelect("hs-rhtp-filter", [["all", "Any (RHTP optional)"], ["money", BD_RHTP_LABELS.money], ["early", BD_RHTP_LABELS.early], ["none", BD_RHTP_LABELS.none]], hsFilters.rhtp);
  fillSelect("hs-state-filter", [["all", "All states"], ...Object.keys(STATE_ABBR).map(a => [STATE_ABBR[a], STATE_ABBR[a]])], hsFilters.state);
  fillSelect("hs-source-filter", [["all", "All types"], ...Object.keys(BD_TYPES).map(k => [k, BD_TYPES[k].label])], hsFilters.source);
  document.querySelectorAll("#hs-tier-toggle button").forEach(b => b.classList.toggle("active", b.dataset.tier === hsTierFilter));
  document.querySelectorAll("#hs-ownership-toggle button").forEach(b => b.classList.toggle("active", b.dataset.ownership === hsOwnershipFilter));
  document.getElementById("hs-color-status-btn").hidden = !BD_AUTH.authed;
  document.querySelectorAll("#hs-color-toggle button").forEach(b => b.classList.toggle("active", b.dataset.color === hsColorMode));
  document.getElementById("hs-outreach-tab").hidden = !BD_AUTH.authed;
  const signin = document.getElementById("team-signin");
  signin.hidden = !BD_AUTH.configured;
  signin.textContent = BD_AUTH.authed ? "Sign out" : "Team sign-in";
}

function renderBdStrip() {
  const el = document.getElementById("hs-bd-strip");
  if (!el) return;
  const shown = currentFilteredSystems();
  const withSize = shown.filter(s => systemTier(s) !== "unsized").length;
  let html = `<span class="bd-strip-count"><strong>${shown.length.toLocaleString()}</strong> of ${SYSTEMS_UNIFIED.length.toLocaleString()} systems shown <span class="ls-sub">(${withSize.toLocaleString()} with a sourced size · ${(shown.length - withSize).toLocaleString()} unsized)</span></span>`;
  if (BD_AUTH.authed) {
    const counts = {};
    // The breakdown covers every filter except the status one, so choosing a state shows all its statuses
    // and picking one status doesn't zero out the others.
    currentFilteredSystems(true).forEach(s => { const st = systemStatus(s.key); counts[st] = (counts[st] || 0) + 1; });
    html += `<span class="bd-strip-statuses">${BD_STATUS_ORDER.map(k =>
      `<button type="button" class="bd-status-pill${hsFilters.status === k ? " selected" : ""}" style="--chip:var(${BD_STATUSES[k].varName})" data-bd-status="${k}" title="Filter to ${esc(BD_STATUSES[k].label)}">${esc(BD_STATUSES[k].label)} · ${counts[k] || 0}</button>`).join("")}</span>`;
  }
  el.innerHTML = html;
}

// Re-renders everything on the Health Systems tab that depends on filters / colors / status.
let lastFilterSig = "";
function refreshHsAll(keepTable) {
  if (!SYSTEMS_UNIFIED.length) return;
  const sig = JSON.stringify([hsFilters, hsTierFilter, hsOwnershipFilter]);
  if (sig !== lastFilterSig) { hsCardLimit = 60; lastFilterSig = sig; } // a new filter starts the card list over
  renderBdStrip();
  renderSystemCards(currentFilteredSystems());
  renderHsLegend();
  renderOperatorLayer();
  if (hsFacilitiesLoaded) applyFacilityFilter();
  if (hsView === "landscape") renderLandscape();
  if (hsView === "outreach" && !keepTable && BD_AUTH.authed) renderBdTable();
}

function zoomToState(abbr) {
  if (!hsMap || !Array.isArray(CMS_HOSPITALS_RAW)) return;
  const pts = CMS_HOSPITALS_RAW.filter(p => p.state === abbr && Number.isFinite(p.lat) && Number.isFinite(p.lon)).map(p => [p.lat, p.lon]);
  if (pts.length) hsMap.fitBounds(L.latLngBounds(pts).pad(0.15));
}

async function signInOrOut() {
  if (!BD_AUTH.authed) { openSignIn(); return; }
  await bdLogout();
  syncHsControls(); refreshHsAll();
  setHsView(hsView === "outreach" ? "map" : hsView);
}

function wireHsBdControls() {
  syncHsControls();

  const bindSelect = (id, key) => document.getElementById(id).addEventListener("change", e => { hsFilters[key] = e.target.value; refreshHsAll(); });
  bindSelect("hs-category-filter", "category");
  bindSelect("hs-strategy-filter", "strategy");
  bindSelect("hs-rhtp-filter", "rhtp");
  bindSelect("hs-source-filter", "source");
  document.getElementById("hs-search").addEventListener("input", e => {
    hsFilters.q = e.target.value.trim().toLowerCase();
    refreshHsAll();
  });
  document.getElementById("hs-state-filter").addEventListener("change", e => {
    hsFilters.state = e.target.value;
    refreshHsAll();
    if (hsFilters.state !== "all") zoomToState(stateNameToAbbr(hsFilters.state));
  });

  document.getElementById("hs-color-toggle").addEventListener("click", e => {
    const btn = e.target.closest("button[data-color]");
    if (!btn) return;
    hsColorMode = btn.dataset.color;
    syncHsControls();
    refreshHsAll();
  });
  document.getElementById("hs-view-toggle").addEventListener("click", e => {
    const btn = e.target.closest("button[data-view]");
    if (btn) setHsView(btn.dataset.view);
  });
  document.getElementById("team-signin").addEventListener("click", signInOrOut);
  document.getElementById("bd-modal-close").addEventListener("click", closeBdModal);
  document.getElementById("bd-overlay").addEventListener("click", e => { if (e.target.id === "bd-overlay") closeBdModal(); });
  window.addEventListener("keydown", e => { if (e.key === "Escape") closeBdModal(); });

  // Landscape: jump to the map with a filter applied; sort the state table.
  document.getElementById("hs-landscape").addEventListener("click", e => {
    const cell = e.target.closest("[data-ls-cat]");
    if (cell) {
      hsFilters.category = cell.dataset.lsCat;
      hsTierFilter = cell.dataset.lsTier;
      syncHsControls(); setHsView("map"); refreshHsAll();
      return;
    }
    const st = e.target.closest("[data-ls-state]");
    if (st) {
      hsFilters.state = STATE_ABBR[st.dataset.lsState];
      syncHsControls(); setHsView("map"); refreshHsAll(); zoomToState(st.dataset.lsState);
      return;
    }
    const sort = e.target.closest("[data-ls-sort]");
    if (sort) {
      const key = sort.dataset.lsSort;
      lsSort = { key, dir: lsSort.key === key ? -lsSort.dir : (key === "name" ? 1 : -1) };
      renderLandscape();
    }
  });

  // Strip + popup buttons (delegated: both are re-rendered often).
  document.addEventListener("click", e => {
    const statusBtn = e.target.closest("[data-bd-status]");
    if (statusBtn && statusBtn.closest("#hs-bd-strip")) {
      hsFilters.status = hsFilters.status === statusBtn.dataset.bdStatus ? "all" : statusBtn.dataset.bdStatus;
      refreshHsAll();
      return;
    }
    if (e.target.closest("#hs-more-btn")) { hsCardLimit += 60; renderSystemCards(currentFilteredSystems()); return; }
    const edit = e.target.closest(".bd-edit-link");
    if (edit) {
      const sys = SYSTEMS_UNIFIED.find(s => s.key === edit.dataset.bdKey);
      openOutreach(sys ? sys.name : "");
    }
  });

  // Modal body (login form, filters, row edits) — delegated since it re-renders.
  const body = document.getElementById("bd-modal-body");
  body.addEventListener("submit", async e => {
    if (e.target.id !== "bd-login-form") return;
    e.preventDefault();
    const err = await bdLogin(document.getElementById("bd-username").value, document.getElementById("bd-password").value);
    if (err) { document.getElementById("bd-login-error").textContent = err; return; }
    closeBdModal(); syncHsControls(); refreshHsAll(); setHsView("outreach");
  });
  const panel = document.getElementById("hs-outreach");
  panel.addEventListener("input", e => {
    if (e.target.dataset.stateNote) { saveStateNote(e.target.dataset.stateNote, e.target.value, e.target.closest(".bd-state-note")); return; }
    if (e.target.id === "bd-search") { bdModalSearch = e.target.value; renderBdTable(); return; }
    const f = e.target.dataset.bdField;
    if (f === "owner" || f === "notes") saveOutreach(e.target.dataset.bdKey, { [f]: e.target.value }, e.target.closest("tr"));
  });
  panel.addEventListener("change", e => {
    if (e.target.dataset.bdField === "status") saveOutreach(e.target.dataset.bdKey, { status: e.target.value }, e.target.closest("tr"));
  });
  panel.addEventListener("click", e => {
    if (e.target.id === "bd-lock-btn") { signInOrOut(); return; }
    if (e.target.id === "bd-state-add-btn") {
      const abbr = document.getElementById("bd-state-add").value;
      if (!abbr) return;
      BD_STATE_NOTES[abbr] = "";
      renderStateNotes();
      const box = document.getElementById("sn-" + abbr);
      if (box) box.focus();
    }
  });
}
