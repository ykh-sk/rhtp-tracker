function usd(n) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(n);
}

function esc(str) {
  const d = document.createElement("div");
  d.textContent = str == null ? "" : String(str);
  return d.innerHTML;
}

// Capitalizes the first letter of each word without touching existing case
// elsewhere in the word — "RFA issued" -> "RFA Issued", not "Rfa Issued".
// Applied only to status labels themselves, never to surrounding sentence
// text (so "Stage 4 of 5" keeps a lowercase "of").
function titleCase(str) {
  return str.replace(/\b\w/g, c => c.toUpperCase());
}

function splitFlag(notes) {
  const i = notes.indexOf("FLAG:");
  if (i === -1) return { main: notes, flag: null };
  return { main: notes.slice(0, i).trim(), flag: notes.slice(i + 5).trim() };
}

function fmtDate(iso) {
  return new Date(iso + "T00:00:00").toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

function daysUntil(iso) {
  const ms = new Date(iso + "T00:00:00") - new Date(new Date().toDateString());
  return Math.round(ms / 86400000);
}

const RECENT_CHANGE_WINDOW_DAYS = 5;

// Most recent changelog entry for a state, if it's within the "recently
// updated" window — null otherwise. Drives the pink "Updated" badge; badges
// disappear on their own once an edit ages out, no manual cleanup needed.
function recentChange(s) {
  const log = s.changelog || [];
  if (!log.length) return null;
  const latest = log[0];
  return -daysUntil(latest.changed_at) <= RECENT_CHANGE_WINDOW_DAYS ? latest : null;
}

let STAGES = [];
let STATES = [];
let DEADLINES = [];
let COMMENTARY = [];
let FEDERAL_MILESTONES = [];
let SEARCH_INDEX = [];
let currentStatus = [];
let currentState = null;
let currentView = null;
let currentSort = "stage";

function stageVar(status) {
  const s = STAGES.find(s => s.key === status);
  return s ? `var(${s.var})` : "var(--muted)";
}

function stagePillHtml(status) {
  const v = stageVar(status);
  return `<span class="stage-pill" style="--stage-color:${v}"><span class="dot" style="background:${v}"></span>${esc(titleCase(status))}</span>`;
}

function stageIndex(status) {
  return STAGES.findIndex(s => s.key === status);
}

function parseHash() {
  const params = new URLSearchParams(location.hash.replace(/^#/, ""));
  const statusParam = params.get("status");
  return {
    status: statusParam ? statusParam.split(",").map(decodeURIComponent) : [],
    state: params.get("state"),
    view: params.get("view"),
  };
}

// Multi-select: clicking a stage toggles it in/out of the current set
// rather than replacing it, so several stages can be compared at once.
function goStatus(status) {
  const set = new Set(currentStatus);
  if (set.has(status)) set.delete(status); else set.add(status);
  const next = [...set];
  location.hash = next.length ? "status=" + next.map(encodeURIComponent).join(",") : "";
}

async function boot() {
  const [statesRes, deadlinesRes, commentaryRes, federalRes] = await Promise.all([
    fetch("/api/states").then(r => r.json()),
    fetch("/api/deadlines").then(r => r.json()),
    fetch("/api/commentary").then(r => r.json()),
    fetch("/api/federal_milestones").then(r => r.json()).catch(() => []),
  ]);

  STAGES = statesRes.status_taxonomy.map((key, i) => ({ key, order: i + 1, var: `--stage-${i + 1}` }));
  STATES = statesRes.states;
  DEADLINES = deadlinesRes;
  COMMENTARY = commentaryRes;
  FEDERAL_MILESTONES = federalRes;
  SEARCH_INDEX = buildSearchIndex();

  document.getElementById("stamp").textContent = `${STATES.length} states · FY26`;

  const maxVerified = STATES.reduce((max, s) => {
    const v = (s.current_award || {}).verified_at;
    return v && v > max ? v : max;
  }, "");
  document.getElementById("last-updated").textContent = maxVerified ? `Updated ${fmtDate(maxVerified)}` : "";
  document.getElementById("footer-note").textContent = `Tracking ${STATES.length} states as of ${maxVerified}.`;

  window.addEventListener("hashchange", renderAll);
  document.getElementById("filter-clear").addEventListener("click", () => { location.hash = ""; });
  document.getElementById("segbar").addEventListener("click", e => {
    const el = e.target.closest("[data-status]");
    if (el) goStatus(el.dataset.status);
  });
  document.getElementById("legend").addEventListener("click", e => {
    const el = e.target.closest("[data-status]");
    if (el && !el.disabled) goStatus(el.dataset.status);
  });
  document.getElementById("map-toggle").addEventListener("click", e => {
    const btn = e.target.closest("button[data-metric]");
    if (!btn) return;
    mapMetric = btn.dataset.metric;
    document.querySelectorAll("#map-toggle button").forEach(b => b.classList.toggle("active", b === btn));
    renderMap();
  });
  document.getElementById("sort-select").addEventListener("change", e => {
    currentSort = e.target.value;
    renderDashboard();
  });

  document.getElementById("cal-state-filter").addEventListener("input", e => {
    calStateFilter = e.target.value;
    renderCalendar();
  });

  ["federal-info-btn-dash", "federal-info-btn-cal"].forEach(id => {
    document.getElementById(id).addEventListener("click", openFederalModal);
  });
  document.getElementById("detail").addEventListener("click", e => {
    if (e.target.closest("[data-open-federal-modal]")) openFederalModal();
  });
  document.getElementById("federal-modal-close").addEventListener("click", closeFederalModal);
  document.getElementById("federal-modal-overlay").addEventListener("click", e => {
    if (e.target.id === "federal-modal-overlay") closeFederalModal();
  });
  window.addEventListener("keydown", e => {
    if (e.key === "Escape") closeFederalModal();
  });

  initSiteSearch();

  renderAll();
}

// ---- federal guidelines modal ----

function federalMilestoneHtml(m) {
  const flagged = m.confidence !== "confirmed";
  const personal = m.confidence === "personal";
  const range = m.end_date ? `${fmtDate(m.start_date)} &ndash; ${fmtDate(m.end_date)}` : fmtDate(m.start_date);
  const categoryLabel = titleCase(m.category === "other" ? "" : m.category);
  return `
    <div class="cal-item">
      <div class="cal-when">${range}${flagged ? `<span class="caution-tag${personal ? " personal" : ""}">${personal ? "Personal" : "Unverified"}</span>` : ""}</div>
      <div class="cal-body">
        <h3>${esc(m.title)}</h3>
        ${categoryLabel ? `<div class="cal-state federal-category">${esc(categoryLabel)}</div>` : ""}
        ${flagged
          ? `<div class="caution${personal ? " personal" : ""}">${esc(m.notes || "")}</div>`
          : (m.notes ? `<p class="cal-notes">${esc(m.notes)}</p>` : "")}
        <a href="${esc(m.source_url)}" target="_blank" rel="noopener">Source ↗</a>
      </div>
    </div>
  `;
}

function renderFederalModalBody() {
  const body = document.getElementById("federal-modal-body");
  if (!FEDERAL_MILESTONES.length) {
    body.innerHTML = `<div class="cal-empty">No federal milestones added yet.</div>`;
    return;
  }
  const sorted = [...FEDERAL_MILESTONES].sort((a, b) => a.start_date.localeCompare(b.start_date));
  body.innerHTML = sorted.map(federalMilestoneHtml).join("");
}

function openFederalModal() {
  renderFederalModalBody();
  document.getElementById("federal-modal-overlay").hidden = false;
  document.body.classList.add("modal-open");
}

function closeFederalModal() {
  document.getElementById("federal-modal-overlay").hidden = true;
  document.body.classList.remove("modal-open");
}

// ---- site search ----

function buildSearchIndex() {
  const idx = [];
  STATES.forEach(s => {
    const haystack = [s.state, s.lead_agency, s.current_status, (s.overview || {}).emphasis, latestNote(s)]
      .filter(Boolean).join(" ").toLowerCase();
    idx.push({ group: "States", label: s.state, sub: titleCase(s.current_status), hash: `state=${encodeURIComponent(s.state)}`, haystack });
  });
  DEADLINES.forEach(d => {
    const haystack = [d.title, d.state, d.notes].filter(Boolean).join(" ").toLowerCase();
    idx.push({ group: "Deadlines", label: d.title, sub: `${d.state} · ${fmtDate(d.start_date)}`, hash: "view=calendar", haystack });
  });
  COMMENTARY.forEach(c => {
    const haystack = [c.title, c.summary, c.source_name].filter(Boolean).join(" ").toLowerCase();
    idx.push({ group: "Commentary", label: c.title, sub: c.source_name, hash: "view=commentary", haystack });
  });
  FEDERAL_MILESTONES.forEach(m => {
    const haystack = [m.title, m.notes, m.category].filter(Boolean).join(" ").toLowerCase();
    idx.push({ group: "Federal guidelines", label: m.title, sub: fmtDate(m.start_date), openFederal: true, haystack });
  });
  return idx;
}

function initSiteSearch() {
  const input = document.getElementById("site-search-input");
  const results = document.getElementById("site-search-results");

  function renderResults(query) {
    const q = query.trim().toLowerCase();
    if (q.length < 2) {
      results.hidden = true;
      results.innerHTML = "";
      return;
    }
    const matches = SEARCH_INDEX.filter(r => r.haystack.includes(q)).slice(0, 20);
    if (!matches.length) {
      results.innerHTML = `<div class="search-empty">No matches for "${esc(query)}".</div>`;
      results.hidden = false;
      return;
    }
    const groups = [];
    matches.forEach(m => {
      let g = groups.find(g => g.group === m.group);
      if (!g) { g = { group: m.group, items: [] }; groups.push(g); }
      g.items.push(m);
    });
    results.innerHTML = groups.map(g => `
      <div class="search-group">
        <div class="search-group-label">${esc(g.group)}</div>
        ${g.items.map((m, i) => `
          <button type="button" class="search-result" data-index="${SEARCH_INDEX.indexOf(m)}">
            <span class="sr-label">${esc(m.label)}</span>
            <span class="sr-sub">${esc(m.sub || "")}</span>
          </button>
        `).join("")}
      </div>
    `).join("");
    results.hidden = false;
  }

  input.addEventListener("input", () => renderResults(input.value));
  input.addEventListener("focus", () => { if (input.value.trim().length >= 2) renderResults(input.value); });

  results.addEventListener("click", e => {
    const btn = e.target.closest(".search-result");
    if (!btn) return;
    const item = SEARCH_INDEX[+btn.dataset.index];
    if (!item) return;
    input.value = "";
    results.hidden = true;
    if (item.openFederal) {
      location.hash = "";
      openFederalModal();
    } else {
      location.hash = item.hash;
    }
  });

  document.addEventListener("click", e => {
    if (!e.target.closest("#site-search")) { results.hidden = true; }
  });
  input.addEventListener("keydown", e => {
    if (e.key === "Escape") { results.hidden = true; input.blur(); }
  });
}

function sortStates(list) {
  const arr = [...list];
  switch (currentSort) {
    case "alpha":
      return arr.sort((a, b) => a.state.localeCompare(b.state));
    case "award":
      return arr.sort((a, b) => b.total_awarded - a.total_awarded);
    case "subawards":
      return arr.sort((a, b) => {
        const av = (a.current_award && a.current_award.subawards_amount) ?? -1;
        const bv = (b.current_award && b.current_award.subawards_amount) ?? -1;
        return bv - av;
      });
    case "updated": {
      const latestDate = s => (s.status_events || []).reduce((max, e) => (e.event_date > max ? e.event_date : max), "");
      return arr.sort((a, b) => latestDate(b).localeCompare(latestDate(a)));
    }
    case "stage":
    default:
      return arr.sort((a, b) => stageIndex(b.current_status) - stageIndex(a.current_status) || a.state.localeCompare(b.state));
  }
}

function renderAll() {
  const { status, state, view } = parseHash();
  currentStatus = state ? [] : status;
  currentState = state;
  currentView = state ? null : view;

  document.querySelectorAll("nav.tabs a").forEach(a => {
    const tab = a.dataset.tab;
    const active = !currentState && (tab === currentView || (tab === "dashboard" && !currentView));
    a.classList.toggle("active", active);
  });

  document.getElementById("dashboard").hidden = true;
  document.getElementById("detail").hidden = true;
  document.getElementById("calendar").hidden = true;
  document.getElementById("commentary").hidden = true;

  if (currentState) {
    document.getElementById("detail").hidden = false;
    renderDetail(currentState);
    return;
  }

  if (currentView === "calendar") {
    document.getElementById("calendar").hidden = false;
    renderCalendar();
    return;
  }

  if (currentView === "commentary") {
    document.getElementById("commentary").hidden = false;
    renderCommentary();
    return;
  }

  document.getElementById("dashboard").hidden = false;
  renderDashboard();
}

// ---- dashboard ----

function renderDashboard() {
  const counts = STAGES.map(st => ({ ...st, count: STATES.filter(s => s.current_status === st.key).length }));

  document.getElementById("m-states").textContent = STATES.length;
  document.getElementById("m-total").textContent = usd(STATES.reduce((a, s) => a + s.total_awarded, 0));

  document.getElementById("segbar").innerHTML = counts
    .filter(c => c.count > 0)
    .map(c => `<span data-status="${esc(c.key)}" class="${currentStatus.length && !currentStatus.includes(c.key) ? "dim" : ""}"
        style="width:${(c.count / STATES.length) * 100}%; background:var(${c.var})"
        title="${esc(titleCase(c.key))} — ${c.count} state${c.count === 1 ? "" : "s"}"></span>`)
    .join("");

  document.getElementById("legend").innerHTML = counts
    .map((c, i) => {
      const active = currentStatus.includes(c.key);
      const btn = `<button type="button" class="step${active ? " active" : ""}"
          data-status="${esc(c.key)}" ${c.count === 0 ? "disabled" : ""}
          aria-pressed="${active}" style="--stage-color:var(${c.var})">
          <span class="step-num">${c.order}</span>
          <span class="dot" style="background:var(${c.var})"></span>
          ${esc(titleCase(c.key))} (${c.count})
        </button>`;
      return i < counts.length - 1 ? btn + `<span class="arrow" aria-hidden="true">&rarr;</span>` : btn;
    })
    .join("");

  const banner = document.getElementById("filter-banner");
  if (currentStatus.length) {
    const n = STATES.filter(s => currentStatus.includes(s.current_status)).length;
    const labels = currentStatus.map(k => `"${titleCase(k)}"`).join(", ");
    document.getElementById("filter-banner-text").textContent =
      `Showing ${labels} — ${n} of ${STATES.length} states. This view is linkable: copy the URL to share it.`;
    banner.hidden = false;
  } else {
    banner.hidden = true;
  }

  const visible = currentStatus.length ? STATES.filter(s => currentStatus.includes(s.current_status)) : STATES;
  const ordered = sortStates(visible);

  // Computed once per state and shared by both the desktop table and the
  // mobile card list below, so the two views can never silently drift apart
  // on what counts as "flagged", "has a subaward figure", or "recent".
  const views = ordered.map(s => {
    const { main, flag } = splitFlag(latestNote(s));
    return {
      s,
      main,
      hasFlag: !!flag,
      sub: s.current_award && s.current_award.subawards_amount != null ? s.current_award.subawards_amount : null,
      recent: recentChange(s),
    };
  });

  const rows = views.map(({ s, main, hasFlag, sub, recent }) => `
      <tr>
        <td class="cell-state">
          <div class="state-name-row">
            <a class="state-name" href="#state=${encodeURIComponent(s.state)}">${esc(s.state)}</a>
            ${recent ? `<span class="updated-badge" title="${esc(recent.summary)}">Updated</span>` : ""}
            <a class="official-badge" href="${esc(s.official_url)}" target="_blank" rel="noopener">Official ↗</a>
          </div>
          <div class="state-agency">${esc(s.lead_agency)}</div>
        </td>
        <td>${stagePillHtml(s.current_status)}</td>
        <td class="num amount">${usd(s.total_awarded)}</td>
        <td class="num sub${sub != null ? "" : " empty"}">
          ${sub != null ? `${usd(sub)}<span class="sa-label">${esc(s.current_award.subawards_label)}</span>` : "—"}
        </td>
        <td class="cell-notes" title="${esc(latestNote(s))}"><span class="cell-notes-inner">${hasFlag ? '<span class="flag-mark">⚑</span>' : ""}${esc(main)}</span></td>
        <td class="cell-links">
          <a class="details-link" href="#state=${encodeURIComponent(s.state)}">Details &rarr;</a>
        </td>
      </tr>
    `).join("");

  document.getElementById("states-tbody").innerHTML =
    rows || `<tr><td colspan="6" style="text-align:center; color:var(--muted); padding:24px;">No states currently in this stage.</td></tr>`;

  const cards = views.map(({ s, main, hasFlag, sub, recent }) => `
      <div class="state-card">
        <div class="sc-top">
          <div class="sc-name-wrap">
            <a class="sc-name" href="#state=${encodeURIComponent(s.state)}">${esc(s.state)}</a>
            ${recent ? `<span class="updated-badge" title="${esc(recent.summary)}">Updated</span>` : ""}
          </div>
          <a class="official-badge" href="${esc(s.official_url)}" target="_blank" rel="noopener">Official ↗</a>
        </div>
        <div class="sc-agency">${esc(s.lead_agency)}</div>
        <div class="sc-stage-row">${stagePillHtml(s.current_status)}</div>
        <div class="sc-amounts">
          <div class="sc-amount">${usd(s.total_awarded)}</div>
          <div class="sc-amount-label">FY26 award &middot; verified ${esc((s.current_award || {}).verified_at || "")}</div>
          ${sub != null ? `<div class="sc-sub">${usd(sub)} <span class="sa-label">${esc(s.current_award.subawards_label)}</span></div>` : ""}
        </div>
        <div class="sc-notes">${hasFlag ? '<span class="flag-mark">⚑</span>' : ""}${esc(main)}</div>
        <div class="sc-links">
          <a class="details-link" href="#state=${encodeURIComponent(s.state)}">Details &rarr;</a>
        </div>
      </div>
    `).join("");

  document.getElementById("states-cards").innerHTML =
    cards || `<p style="text-align:center; color:var(--muted); padding:24px;">No states currently in this stage.</p>`;

  renderMap();
}

// ---- award map ----

let usTopo = null;
let mapMetric = "total";

async function ensureUsTopo() {
  if (!usTopo) {
    const res = await fetch("https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json");
    usTopo = await res.json();
  }
  return usTopo;
}

// "sub" is a ratio (subawards disbursed / total award), not a raw dollar
// figure — a $144M subaward on a $203M award and a $30M subaward on a $190M
// award are differently far along, and only the percentage says so. Fixed
// 0–100% domain (not the observed min/max) so the scale means the same
// thing everywhere it's read, not just relative to this batch of states.
function stateMapValue(s, metric) {
  if (metric === "sub") {
    const a = s.current_award;
    if (!a || !a.subawards_amount || !s.total_awarded) return null;
    return a.subawards_amount / s.total_awarded;
  }
  return s.total_awarded || null;
}

async function renderMap() {
  if (typeof d3 === "undefined" || typeof topojson === "undefined") return; // CDN blocked/offline: skip gracefully
  const container = document.getElementById("us-map");
  let topo;
  try {
    topo = await ensureUsTopo();
  } catch {
    container.innerHTML = `<p style="text-align:center; color:var(--muted); font-size:12px;">Map data unavailable right now.</p>`;
    return;
  }

  const geo = topojson.feature(topo, topo.objects.states).features;
  const byName = {};
  STATES.forEach(s => { byName[s.state] = s; });

  const values = STATES.map(s => stateMapValue(s, mapMetric)).filter(v => v != null);
  // Total-award domain spans the observed min–max so relative differences
  // between states are visible (they cluster in a narrow band; anchoring at
  // $0 made every one of them look "high"). Subawards domain is fixed 0–1
  // since it's already a percentage — a strict, portable scale rather than
  // one relative to whichever states happen to be tracked.
  const domain = mapMetric === "sub" ? [0, 1] : [Math.min(...values), Math.max(1, ...values)];
  const colorScale = d3.scaleSequential(d3.interpolateReds).domain(domain);

  const width = 960, height = 600;
  const projection = d3.geoAlbersUsa().scale(1180).translate([width / 2, height / 2]);
  const path = d3.geoPath(projection);

  const svg = d3.select(container).selectAll("svg").data([null]).join("svg")
    .attr("viewBox", `0 0 ${width} ${height}`)
    .attr("role", "img")
    .attr("aria-label", "US map colored by state funding");

  const tooltip = d3.select("body").selectAll(".map-tooltip").data([null]).join("div").attr("class", "map-tooltip");
  tooltip.style("display", "none");

  // When a pipeline-stage filter is active (clicked in the legend/segbar),
  // echo it on the map: matching states get a bold accent outline, other
  // tracked states dim — same "dim" convention the segbar already uses, so
  // the two controls read as one filter rather than two different ideas.
  svg.selectAll("path.state")
    .data(geo, d => d.properties.name)
    .join("path")
    .attr("class", d => "state" + (byName[d.properties.name] ? "" : " untracked"))
    .attr("d", path)
    .attr("fill", d => {
      const s = byName[d.properties.name];
      if (!s) return "var(--border)";
      const v = stateMapValue(s, mapMetric);
      return v == null ? "var(--surface-2)" : colorScale(v);
    })
    .attr("stroke", d => {
      const s = byName[d.properties.name];
      // A hue outside the red fill scale (not --ink) so the outline reads
      // as a highlight against every fill color, dark reds included.
      return currentStatus.length && s && currentStatus.includes(s.current_status) ? "var(--accent)" : "var(--surface)";
    })
    .attr("stroke-width", d => {
      const s = byName[d.properties.name];
      return currentStatus.length && s && currentStatus.includes(s.current_status) ? 3.5 : 1;
    })
    .attr("opacity", d => {
      const s = byName[d.properties.name];
      return currentStatus.length && s && !currentStatus.includes(s.current_status) ? 0.3 : 1;
    })
    .attr("filter", d => {
      const s = byName[d.properties.name];
      return currentStatus.length && s && currentStatus.includes(s.current_status)
        ? "drop-shadow(0 0 3px var(--accent))"
        : null;
    })
    .attr("paint-order", "stroke")
    .on("mousemove", (event, d) => {
      const s = byName[d.properties.name];
      const v = s ? stateMapValue(s, mapMetric) : null;
      let label = "Not yet tracked";
      if (s && mapMetric === "sub") {
        label = v == null
          ? "No subawards figure yet"
          : `${(v * 100).toFixed(0)}% of award disbursed (${usd(s.current_award.subawards_amount)} of ${usd(s.total_awarded)})`;
      } else if (s) {
        label = usd(v);
      }
      tooltip
        .style("display", "block")
        .style("left", (event.clientX + 14) + "px")
        .style("top", (event.clientY + 14) + "px")
        .html(`<div class="mt-state">${esc(d.properties.name)}</div><div class="mt-value">${label}</div>`);
    })
    .on("mouseleave", () => tooltip.style("display", "none"))
    .on("click", (event, d) => {
      const s = byName[d.properties.name];
      if (s) location.hash = "state=" + encodeURIComponent(s.state);
    });

  const steps = [0, 0.25, 0.5, 0.75, 1];
  const [dMin, dMax] = domain;
  const lowLabel = mapMetric === "sub" ? "0%" : usd(dMin);
  const highLabel = mapMetric === "sub" ? "100%" : usd(dMax);
  document.getElementById("map-legend").innerHTML = `
    <span class="map-legend-label">${lowLabel}</span>
    <div class="map-legend-scale">${steps.map(t => `<span style="background:${colorScale(dMin + t * (dMax - dMin))}"></span>`).join("")}</div>
    <span class="map-legend-label">${highLabel}</span>
  `;

  document.getElementById("map-caption").textContent = mapMetric === "sub"
    ? "Colored by percentage of the total award disbursed as subawards, where a source states a figure — not the raw dollar amount, so states with different-sized awards compare fairly. Light-gray tracked states have no subawards figure yet. Untracked states are neutral gray."
    : "Colored by total FY26 award, scaled to the range actually observed among tracked states (not from $0) so relative differences are visible. Untracked states are neutral gray.";
}

function latestConfirmedEvent(s) {
  const events = s.status_events || [];
  const confirmed = events.filter(e => e.confidence === "confirmed");
  const pool = confirmed.length ? confirmed : events;
  return pool.length ? pool[pool.length - 1] : null;
}

function latestNote(s) {
  const e = latestConfirmedEvent(s);
  return e ? e.notes : "";
}

// ---- detail ----

function renderDetail(name) {
  const root = document.getElementById("detail");
  const s = STATES.find(x => x.state === name);

  if (!s) {
    root.innerHTML = `<a class="back-link" href="#">&larr; All states</a><p>No state named "${esc(name)}" was found.</p>`;
    return;
  }

  const latest = s.current_award || {};
  const events = [...s.status_events].sort((a, b) => b.event_date.localeCompare(a.event_date));

  const timelineHtml = events.map((e, i) => {
    const unverified = e.confidence === "unverified";
    const personal = e.confidence === "personal";
    const flagged = unverified || personal;
    const dotColor = unverified ? "var(--warn)" : personal ? "var(--personal)" : stageVar(e.status);
    const tagText = unverified ? "Unverified lead" : personal ? "Personal source" : "";
    const { main, flag } = splitFlag(e.notes);
    return `
      <li>
        <div class="tl-date">${fmtDate(e.event_date)}</div>
        <div class="tl-rail">
          <span class="tl-dot" style="background:${dotColor}"></span>
          ${i < events.length - 1 ? '<span class="tl-line"></span>' : ""}
        </div>
        <div>
          <div class="tl-status">${esc(e.status)}${flagged ? `<span class="caution-tag${personal ? " personal" : ""}">${tagText}</span>` : ""}</div>
          ${flagged
            ? `<div class="caution${personal ? " personal" : ""}">${esc(main)}</div>`
            : `<p class="tl-notes">${esc(main)}</p>${flag ? `<div class="flag">FLAG — ${esc(flag)}</div>` : ""}`}
          <a class="tl-source" href="${esc(e.source_url)}" target="_blank" rel="noopener">Source ↗</a>
        </div>
      </li>
    `;
  }).join("");

  const rank = s.rank;
  const pros = s.analysis.pros || [];
  const cons = s.analysis.cons || [];
  const overview = s.overview || {};
  const pillars = s.pillars || [];
  const recent = recentChange(s);

  const overviewHtml = `
    <div class="overview-section">
      <h2>Program overview</h2>
      <p class="overview-caption">A brief summary derived from the sources on this page — not a direct quote from the state program. See History below for the underlying facts it's based on.</p>
      ${recent ? `<div class="changelog-banner"><strong>Updated ${fmtDate(recent.changed_at)}:</strong> ${esc(recent.summary)}</div>` : ""}
      <div class="overview-grid">
        <div>
          <div class="overview-field">
            <h3>Emphasis</h3>
            <p>${esc(overview.emphasis || "Not yet detailed in current sources.")}</p>
          </div>
          <div class="overview-field">
            <h3>Pillars / initiative tracks</h3>
            ${pillars.length
              ? `<div class="pillar-list">${pillars.map(p => `<span class="pillar-chip">${esc(p)}</span>`).join("")}</div>`
              : `<p>Not yet named in current sources.</p>`}
          </div>
          <div class="overview-field">
            <h3>Who they're looking for</h3>
            <p>${esc(overview.applicant_profile || "Not yet detailed in current sources.")}</p>
          </div>
        </div>
        <div class="overview-field">
          <h3>Contact</h3>
          <div class="contact-block">
            ${overview.contact_name ? `<div class="contact-name">${esc(overview.contact_name)}</div>` : ""}
            ${overview.contact_email
              ? `<div><a href="mailto:${esc(overview.contact_email)}">${esc(overview.contact_email)}</a></div>`
              : `<div>N/A</div>`}
            ${overview.contact_note ? `<div class="contact-muted">${esc(overview.contact_note)}</div>` : ""}
          </div>
        </div>
      </div>
    </div>
  `;

  root.innerHTML = `
    <a class="back-link" href="#">&larr; All states</a>
    <div class="detail-head">
      <div>
        <div class="stage-pill" style="--stage-color:${stageVar(s.current_status)}">
          <span class="dot" style="background:${stageVar(s.current_status)}"></span>
          Stage ${stageIndex(s.current_status) + 1} of ${STAGES.length} &mdash; ${esc(titleCase(s.current_status))}
        </div>
        <div class="title-row">
          <h1>${esc(s.state)}</h1>
          <a class="official-badge" href="${esc(s.official_url)}" target="_blank" rel="noopener">Official page ↗</a>
        </div>
        <div class="agency">${esc(s.lead_agency)}</div>
      </div>
      <div class="detail-amount">
        <div class="amount">${usd(s.total_awarded)}</div>
        <div class="amount-label">FY26 award &middot; verified ${esc(latest.verified_at || "")}</div>
        ${latest.subawards_amount ? `<div class="sub">${usd(latest.subawards_amount)} <span class="sa-label">${esc(latest.subawards_label)}</span></div>` : ""}
      </div>
    </div>
    ${overviewHtml}
    <div class="detail-body">
      <div class="detail-main">
        <h2>History</h2>
        <ul class="timeline" style="margin-top:0; padding-top:0; border-top:none;">${timelineHtml}</ul>
      </div>
      <aside class="detail-side">
        <h2>Sources</h2>
        <a href="${esc(s.official_url)}" target="_blank" rel="noopener">Official program page ↗</a>
        <a href="${esc(latest.source_url)}" target="_blank" rel="noopener">Latest source article ↗</a>
        <h2 class="deadlines-heading">Deadlines</h2>
        ${stateDeadlinesHtml(s.state)}
        <button type="button" class="info-btn info-btn-block" data-open-federal-modal>ⓘ Federal guidelines &amp; deadlines</button>
      </aside>
      <div class="compare">
        <div class="compare-head"><h2>How ${esc(s.state)} compares</h2></div>
        <p class="compare-caption">Editorial notes derived from the sources above — a starting point for comparison, not official guidance. Verify anything decision-critical directly with the state agency.</p>
        <div class="rank-line"><strong>#${rank}</strong> of ${STATES.length} states by total FY26 award &middot; ${usd(s.total_awarded)}</div>
        <div class="pros-cons">
          <div class="pros"><h3>Pros</h3><ul>${pros.map(p => `<li>${esc(p)}</li>`).join("") || "<li>—</li>"}</ul></div>
          <div class="cons"><h3>Cons</h3><ul>${cons.map(c => `<li>${esc(c)}</li>`).join("") || "<li>—</li>"}</ul></div>
        </div>
      </div>
    </div>
  `;
}

// ---- calendar ----

let calStateFilter = "";

function stateDeadlinesHtml(stateName) {
  const items = DEADLINES.filter(d => d.state === stateName).sort((a, b) => a.start_date.localeCompare(b.start_date));
  if (!items.length) return `<p class="side-empty">No dated deadlines published for this state yet.</p>`;
  return `<ul class="side-deadline-list">${items.map(d => {
    const flagged = d.confidence !== "confirmed";
    const personal = d.confidence === "personal";
    const range = d.end_date ? `${fmtDate(d.start_date)}&ndash;${fmtDate(d.end_date)}` : fmtDate(d.start_date);
    return `
      <li>
        <div class="sd-when">${range}</div>
        <div class="sd-title">${esc(d.title)}${flagged ? `<span class="caution-tag${personal ? " personal" : ""}">${personal ? "Personal" : "Unverified"}</span>` : ""}</div>
      </li>
    `;
  }).join("")}</ul>`;
}

function renderCalendar() {
  const confirmedCount = DEADLINES.filter(d => d.confidence === "confirmed").length;
  const unverifiedCount = DEADLINES.length - confirmedCount;
  document.getElementById("cal-caption").textContent =
    `${confirmedCount} confirmed dated deadline${confirmedCount === 1 ? "" : "s"}` +
    (unverifiedCount ? ` plus ${unverifiedCount} unverified lead${unverifiedCount === 1 ? "" : "s"} (flagged below)` : "") +
    ` across the ${STATES.length} states — RFA/subaward application windows, funds-obligation deadlines, and similar dated ` +
    `milestones a source explicitly states, never an estimate. A state can be further along in its pipeline (see its Stage ` +
    `on the dashboard) without a specific dated item appearing here — this list only reflects what has a published date, ` +
    `not the state's overall progress.`;

  if (!DEADLINES.length) {
    document.getElementById("cal-list").innerHTML = `<div class="cal-empty">No confirmed deadlines yet.</div>`;
    return;
  }

  const q = calStateFilter.trim().toLowerCase();
  const filtered = q ? DEADLINES.filter(d => d.state.toLowerCase().includes(q)) : DEADLINES;
  const sorted = [...filtered].sort((a, b) => b.start_date.localeCompare(a.start_date));

  if (!sorted.length) {
    document.getElementById("cal-list").innerHTML = `<div class="cal-empty">No deadlines match "${esc(calStateFilter)}".</div>`;
    return;
  }

  document.getElementById("cal-list").innerHTML = sorted.map(d => {
    const unverified = d.confidence === "unverified";
    const personal = d.confidence === "personal";
    const flagged = unverified || personal;
    const closes = d.end_date || d.start_date;
    const n = daysUntil(closes);
    const dayLabel = n > 0 ? `${n} day${n === 1 ? "" : "s"} left` : n === 0 ? "closes today" : "closed";
    const range = d.end_date ? `${fmtDate(d.start_date)} &ndash; ${fmtDate(d.end_date)}` : fmtDate(d.start_date);
    return `
      <div class="cal-item">
        <div class="cal-when">${range}<span class="cal-days">${dayLabel}</span>${flagged ? `<span class="caution-tag${personal ? " personal" : ""}">${personal ? "Personal" : "Unverified"}</span>` : ""}</div>
        <div class="cal-body">
          <h3>${esc(d.title)}</h3>
          <a class="cal-state" href="#state=${encodeURIComponent(d.state)}">${esc(d.state)}</a>
          ${flagged
            ? `<div class="caution${personal ? " personal" : ""}">${esc(d.notes || "")}</div>`
            : (d.notes ? `<p class="cal-notes">${esc(d.notes)}</p>` : "")}
          <a href="${esc(d.source_url)}" target="_blank" rel="noopener">Source ↗</a>
        </div>
      </div>
    `;
  }).join("");
}

// ---- commentary ----

function renderCommentary() {
  const sorted = [...COMMENTARY].sort((a, b) => (b.published_date || "").localeCompare(a.published_date || ""));

  document.getElementById("commentary-list").innerHTML = sorted.map(c => `
    <div class="cal-item">
      <div class="cal-when">${c.published_date ? fmtLoose(c.published_date) : "Undated"}</div>
      <div class="cal-body">
        <h3>${esc(c.title)}<span class="angle-tag">${esc(c.angle)}</span></h3>
        <div class="cal-state">${esc(c.source_name)}${c.state ? ` &middot; ${esc(c.state)}` : " &middot; National"}</div>
        ${c.summary ? `<p class="cal-notes">${esc(c.summary)}</p>` : ""}
        <a href="${esc(c.url)}" target="_blank" rel="noopener">Read ↗</a>
      </div>
    </div>
  `).join("") || `<div class="cal-empty">No commentary gathered yet.</div>`;
}

function fmtLoose(s) {
  const parts = s.split("-");
  if (parts.length === 3) return fmtDate(s);
  if (parts.length === 2) return new Date(parts[0], parts[1] - 1, 1).toLocaleDateString("en-US", { month: "short", year: "numeric" });
  return s;
}

// ---- dark mode toggle ----
// A stored preference (set by the button) always wins; with none stored, the
// site follows the OS/browser's prefers-color-scheme, same as before this
// toggle existed. The inline script in index.html's <head> applies any
// stored choice before first paint so there's no flash of the wrong theme.
// localStorage access is wrapped because this runs before boot() — an
// exception here (e.g. storage blocked by a privacy setting) must not take
// the rest of the page down with it.
function getStoredTheme() {
  try { return localStorage.getItem("theme"); } catch { return null; }
}

function setStoredTheme(value) {
  try { localStorage.setItem("theme", value); } catch { /* ignore — toggle still works for this page view */ }
}

function effectiveTheme() {
  const stored = getStoredTheme();
  if (stored === "dark" || stored === "light") return stored;
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

function updateThemeToggleIcon() {
  const btn = document.getElementById("theme-toggle");
  const dark = effectiveTheme() === "dark";
  btn.textContent = dark ? "☀️" : "🌙";
  btn.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
}

function initThemeToggle() {
  const btn = document.getElementById("theme-toggle");
  updateThemeToggleIcon();
  btn.addEventListener("click", () => {
    const next = effectiveTheme() === "dark" ? "light" : "dark";
    setStoredTheme(next);
    document.documentElement.setAttribute("data-theme", next);
    updateThemeToggleIcon();
  });
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
    if (!getStoredTheme()) updateThemeToggleIcon();
  });
}

initThemeToggle();
boot();
