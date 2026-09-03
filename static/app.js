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
let currentStatus = null;
let currentState = null;
let currentView = null;

function stageVar(status) {
  const s = STAGES.find(s => s.key === status);
  return s ? `var(${s.var})` : "var(--muted)";
}

function stageIndex(status) {
  return STAGES.findIndex(s => s.key === status);
}

function parseHash() {
  const params = new URLSearchParams(location.hash.replace(/^#/, ""));
  return { status: params.get("status"), state: params.get("state"), view: params.get("view") };
}

function goStatus(status) {
  const next = status === currentStatus ? null : status;
  location.hash = next ? "status=" + encodeURIComponent(next) : "";
}

async function boot() {
  const [statesRes, deadlinesRes, commentaryRes] = await Promise.all([
    fetch("/api/states").then(r => r.json()),
    fetch("/api/deadlines").then(r => r.json()),
    fetch("/api/commentary").then(r => r.json()),
  ]);

  STAGES = statesRes.status_taxonomy.map((key, i) => ({ key, order: i + 1, var: `--stage-${i + 1}` }));
  STATES = statesRes.states;
  DEADLINES = deadlinesRes;
  COMMENTARY = commentaryRes;

  document.getElementById("stamp").textContent = `${STATES.length} states · FY26`;

  document.getElementById("footer-note").textContent =
    `Tracking ${STATES.length} states as of ${STATES.reduce((max, s) => {
      const v = (s.current_award || {}).verified_at;
      return v && v > max ? v : max;
    }, "")}.`;

  window.addEventListener("hashchange", renderAll);
  document.getElementById("filter-clear").addEventListener("click", () => goStatus(currentStatus));
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

  renderAll();
}

function renderAll() {
  const { status, state, view } = parseHash();
  currentStatus = state ? null : status;
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
    .map(c => `<span data-status="${esc(c.key)}" class="${currentStatus && currentStatus !== c.key ? "dim" : ""}"
        style="width:${(c.count / STATES.length) * 100}%; background:var(${c.var})"
        title="${esc(titleCase(c.key))} — ${c.count} state${c.count === 1 ? "" : "s"}"></span>`)
    .join("");

  document.getElementById("legend").innerHTML = counts
    .map((c, i) => {
      const btn = `<button type="button" class="step${currentStatus === c.key ? " active" : ""}"
          data-status="${esc(c.key)}" ${c.count === 0 ? "disabled" : ""}
          aria-pressed="${currentStatus === c.key}">
          <span class="step-num">${c.order}</span>
          <span class="dot" style="background:var(${c.var})"></span>
          ${esc(titleCase(c.key))} (${c.count})
        </button>`;
      return i < counts.length - 1 ? btn + `<span class="arrow" aria-hidden="true">&rarr;</span>` : btn;
    })
    .join("");

  const banner = document.getElementById("filter-banner");
  if (currentStatus) {
    const n = STATES.filter(s => s.current_status === currentStatus).length;
    document.getElementById("filter-banner-text").textContent =
      `Showing "${titleCase(currentStatus)}" — ${n} of ${STATES.length} states. This view is linkable: copy the URL to share it.`;
    banner.hidden = false;
  } else {
    banner.hidden = true;
  }

  const visible = currentStatus ? STATES.filter(s => s.current_status === currentStatus) : STATES;
  const ordered = [...visible].sort((a, b) =>
    stageIndex(b.current_status) - stageIndex(a.current_status) || a.state.localeCompare(b.state)
  );

  const rows = ordered.map(s => {
    const { main } = splitFlag(latestNote(s));
    const hasFlag = latestNote(s).includes("FLAG:");
    const sub = s.current_award && s.current_award.subawards_amount;
    const recent = recentChange(s);
    return `
      <tr>
        <td class="cell-state">
          <div class="state-name-row">
            <div class="state-name">${esc(s.state)}</div>
            ${recent ? `<span class="updated-badge" title="${esc(recent.summary)}">Updated</span>` : ""}
            <a class="official-badge" href="${s.official_url}" target="_blank" rel="noopener">Official ↗</a>
          </div>
          <div class="state-agency">${esc(s.lead_agency)}</div>
        </td>
        <td>
          <span class="stage-pill"><span class="dot" style="background:${stageVar(s.current_status)}"></span>${esc(titleCase(s.current_status))}</span>
        </td>
        <td class="num amount">${usd(s.total_awarded)}</td>
        <td class="num sub${sub ? "" : " empty"}">
          ${sub ? `${usd(sub)}<span class="sa-label">${esc(s.current_award.subawards_label)}</span>` : "—"}
        </td>
        <td class="cell-notes" title="${esc(latestNote(s))}">${hasFlag ? '<span class="flag-mark">⚑</span>' : ""}${esc(main)}</td>
        <td class="cell-links">
          <a class="details-link" href="#state=${encodeURIComponent(s.state)}">Details &rarr;</a>
        </td>
      </tr>
    `;
  }).join("");

  document.getElementById("states-tbody").innerHTML =
    rows || `<tr><td colspan="6" style="text-align:center; color:var(--muted); padding:24px;">No states currently in this stage.</td></tr>`;

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

function stateMapValue(s, metric) {
  if (metric === "sub") {
    const a = s.current_award;
    return a && a.subawards_amount ? a.subawards_amount : null;
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
  const max = Math.max(1, ...values);
  const colorScale = d3.scaleSequential(d3.interpolateReds).domain([0, max]);

  const width = 960, height = 600;
  const projection = d3.geoAlbersUsa().scale(1180).translate([width / 2, height / 2]);
  const path = d3.geoPath(projection);

  const svg = d3.select(container).selectAll("svg").data([null]).join("svg")
    .attr("viewBox", `0 0 ${width} ${height}`)
    .attr("role", "img")
    .attr("aria-label", "US map colored by state funding");

  const tooltip = d3.select("body").selectAll(".map-tooltip").data([null]).join("div").attr("class", "map-tooltip");
  tooltip.style("display", "none");

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
    .on("mousemove", (event, d) => {
      const s = byName[d.properties.name];
      const v = s ? stateMapValue(s, mapMetric) : null;
      const label = s
        ? (v == null ? "No subawards figure yet" : usd(v))
        : "Not yet tracked";
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
  document.getElementById("map-legend").innerHTML = `
    <span class="map-legend-label">Low</span>
    <div class="map-legend-scale">${steps.map(t => `<span style="background:${colorScale(t * max)}"></span>`).join("")}</div>
    <span class="map-legend-label">High</span>
  `;

  document.getElementById("map-caption").textContent = mapMetric === "sub"
    ? "Colored by subawards/disbursed amount, where a source states one. Light-gray tracked states have no subawards figure yet — that's a stage difference, not a zero. Untracked states are neutral gray."
    : "Colored by total FY26 award among tracked states. Untracked states are neutral gray.";
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
  const events = [...s.status_events].sort((a, b) => a.event_date.localeCompare(b.event_date));

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
          <a class="tl-source" href="${e.source_url}" target="_blank" rel="noopener">Source ↗</a>
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
        <div class="stage-pill">
          <span class="dot" style="background:${stageVar(s.current_status)}"></span>
          Stage ${stageIndex(s.current_status) + 1} of ${STAGES.length} &mdash; ${esc(titleCase(s.current_status))}
        </div>
        <div class="title-row">
          <h1>${esc(s.state)}</h1>
          <a class="official-badge" href="${s.official_url}" target="_blank" rel="noopener">Official page ↗</a>
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
        <a href="${s.official_url}" target="_blank" rel="noopener">Official program page ↗</a>
        <a href="${latest.source_url}" target="_blank" rel="noopener">Latest source article ↗</a>
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

function renderCalendar() {
  const confirmedCount = DEADLINES.filter(d => d.confidence === "confirmed").length;
  const unverifiedCount = DEADLINES.length - confirmedCount;
  document.getElementById("cal-caption").textContent =
    `${confirmedCount} confirmed application window${confirmedCount === 1 ? "" : "s"}` +
    (unverifiedCount ? ` plus ${unverifiedCount} unverified lead${unverifiedCount === 1 ? "" : "s"} (flagged below)` : "") +
    ` across the ${STATES.length} states. Most states haven't published a dated RFA window yet — this list only shows deadlines a source states, never an estimate.`;

  if (!DEADLINES.length) {
    document.getElementById("cal-list").innerHTML = `<div class="cal-empty">No confirmed deadlines yet.</div>`;
    return;
  }

  const sorted = [...DEADLINES].sort((a, b) => b.start_date.localeCompare(a.start_date));

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
          <div class="cal-state">${esc(d.state)}</div>
          ${flagged
            ? `<div class="caution${personal ? " personal" : ""}">${esc(d.notes || "")}</div>`
            : (d.notes ? `<p class="cal-notes">${esc(d.notes)}</p>` : "")}
          <a href="${d.source_url}" target="_blank" rel="noopener">Source ↗</a>
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
        <a href="${c.url}" target="_blank" rel="noopener">Read ↗</a>
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

boot();
