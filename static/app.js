// A small seal/shield glyph for the USASpending-certified mark — deliberately
// not a checkmark, so it can't be confused with the confirmed/unverified
// sourcing-confidence dots used everywhere else in the UI.
const USASPENDING_ICON = '<svg class="verified-icon" viewBox="0 0 16 18" width="12" height="13" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M8 1.2 L14.3 3.3 V8.4 C14.3 12.4 11.7 15.5 8 16.8 C4.3 15.5 1.7 12.4 1.7 8.4 V3.3 Z"/></svg>';

function usd(n) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(n);
}

// Abbreviated form ("$9.98B", "$1.23M") for large summary figures where
// scannability matters more than the exact dollar — every other dollar
// figure on the site still uses usd() at full precision.
function usdCompact(n) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", notation: "compact", maximumFractionDigits: 2 }).format(n);
}

// Share of a state's total award reflected in its recorded subawards figure.
// Shared by the map's "Subawards disbursed" toggle and the progress bar shown
// next to the subawards figure everywhere else — one calculation, one meaning.
function disbShare(s) {
  const a = s.current_award;
  if (!a || !a.subawards_amount || !s.total_awarded) return null;
  return a.subawards_amount / s.total_awarded;
}

// Renders as a plain percentage against the total award — not a claim that
// the underlying subawards figure itself is a complete, final tally. Where a
// source's own wording says otherwise ("first round", "Region 7 only", a
// specific initiative rather than the full award), that scope lives in the
// subawards_label text shown right next to this bar, not in a separate
// confidence system that could end up disagreeing with it.
function disbBarHtml(share) {
  const pct = Math.round(share * 100);
  return `<div class="disb-bar" title="${pct}% of the total award reflected in the subawards figure above"><div class="disb-fill" style="width:${pct}%"></div></div><div class="disb-pct">${pct}% of award</div>`;
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

function fmtDateTime(d) {
  return d.toLocaleString("en-US", { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" });
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
let HEALTH_SYSTEMS = [];
let HOSPITAL_ROSTER = [];
let SEARCH_INDEX = [];
let currentStatus = [];
let currentState = null;
let currentView = null;
let currentSort = "stage";
let hsTierFilter = "all";
let hsOwnershipFilter = "all";
let hsCompanyFilter = "all";

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
  const [statesRes, deadlinesRes, commentaryRes, federalRes, healthSystemsRes, hospitalRosterRes] = await Promise.all([
    fetch("/api/states").then(r => r.json()),
    fetch("/api/deadlines").then(r => r.json()),
    fetch("/api/commentary").then(r => r.json()),
    fetch("/api/federal_milestones").then(r => r.json()).catch(() => []),
    fetch("/api/health_systems").then(r => r.json()).catch(() => []),
    fetch("/api/hospital_roster").then(r => r.json()).catch(() => []),
  ]);

  STAGES = statesRes.status_taxonomy.map((key, i) => ({ key, order: i + 1, var: `--stage-${i + 1}` }));
  STATES = statesRes.states;
  DEADLINES = deadlinesRes;
  COMMENTARY = commentaryRes;
  FEDERAL_MILESTONES = federalRes;
  HEALTH_SYSTEMS = healthSystemsRes;
  HOSPITAL_ROSTER = hospitalRosterRes;
  buildRosterIndex();
  populateCompanyFilter();
  SEARCH_INDEX = buildSearchIndex();

  document.getElementById("stamp").textContent = `${STATES.length} states · FY26`;

  const maxVerified = STATES.reduce((max, s) => {
    const v = (s.current_award || {}).verified_at;
    return v && v > max ? v : max;
  }, "");
  document.getElementById("last-updated").textContent = maxVerified ? `Updated ${fmtDate(maxVerified)}` : "";
  document.getElementById("last-updated").hidden = !maxVerified;
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

  document.getElementById("last-updated").addEventListener("click", openWhatsNewModal);
  document.getElementById("whatsnew-modal-close").addEventListener("click", closeWhatsNewModal);
  document.getElementById("whatsnew-modal-overlay").addEventListener("click", e => {
    if (e.target.id === "whatsnew-modal-overlay") closeWhatsNewModal();
  });
  document.getElementById("whatsnew-modal-body").addEventListener("click", e => {
    const link = e.target.closest("a[data-state]");
    if (link) closeWhatsNewModal();
  });

  window.addEventListener("keydown", e => {
    if (e.key !== "Escape") return;
    closeFederalModal();
    closeWhatsNewModal();
    closeCompareModal();
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

// ---- what's new modal ----
// Site-wide feed of every state's changelog (material overview/award/status
// changes, per state_changelog), newest first — the "Updated" header badge
// is the entry point, same underlying data that drives each state's own
// pink changelog banner.

function buildChangelogFeed() {
  const rows = [];
  STATES.forEach(s => {
    (s.changelog || []).forEach(entry => rows.push({ state: s.state, ...entry }));
  });
  return rows.sort((a, b) => b.changed_at.localeCompare(a.changed_at));
}

function renderWhatsNewModalBody() {
  const body = document.getElementById("whatsnew-modal-body");
  const feed = buildChangelogFeed();
  if (!feed.length) {
    body.innerHTML = `<div class="cal-empty">No material changes recorded yet.</div>`;
    return;
  }
  body.innerHTML = feed.map(entry => `
    <div class="cal-item">
      <div class="cal-when">${fmtDate(entry.changed_at)}</div>
      <div class="cal-body">
        <h3>${esc(entry.state)}</h3>
        <p class="cal-notes">${esc(entry.summary)}</p>
        <a href="#state=${encodeURIComponent(entry.state)}" data-state="${esc(entry.state)}">View ${esc(entry.state)}'s page &rarr;</a>
      </div>
    </div>
  `).join("");
}

function openWhatsNewModal() {
  renderWhatsNewModalBody();
  document.getElementById("whatsnew-modal-overlay").hidden = false;
  document.body.classList.add("modal-open");
}

function closeWhatsNewModal() {
  document.getElementById("whatsnew-modal-overlay").hidden = true;
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
      // Prefer the changelog date (what actually drives the red "Updated"
      // badge) so badged states sort to the top; states with no changelog
      // entry fall back to their latest status-event date.
      const latestDate = s => {
        const changelogDate = s.changelog && s.changelog[0] ? s.changelog[0].changed_at : "";
        const eventDate = (s.status_events || []).reduce((max, e) => (e.event_date > max ? e.event_date : max), "");
        return changelogDate > eventDate ? changelogDate : eventDate;
      };
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

  document.querySelectorAll("[data-tab]").forEach(a => {
    const tab = a.dataset.tab;
    const active = !currentState && (tab === currentView || (tab === "dashboard" && !currentView));
    a.classList.toggle("active", active);
  });

  document.getElementById("dashboard").hidden = true;
  document.getElementById("detail").hidden = true;
  document.getElementById("calendar").hidden = true;
  document.getElementById("commentary").hidden = true;
  document.getElementById("health-systems").hidden = true;

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

  if (currentView === "health-systems") {
    document.getElementById("health-systems").hidden = false;
    renderHealthSystems();
    return;
  }

  document.getElementById("dashboard").hidden = false;
  renderDashboard();
}

// ---- dashboard ----

function renderDashboard() {
  const counts = STAGES.map(st => ({ ...st, count: STATES.filter(s => s.current_status === st.key).length }));

  // When a pipeline-stage filter is active, the two headline metrics reflect
  // only the filtered states — otherwise "$10B total" stays fixed while the
  // rest of the page filters down to a handful of states, which reads as if
  // that whole $10B belongs to just the ones shown.
  const filtered = currentStatus.length ? STATES.filter(s => currentStatus.includes(s.current_status)) : STATES;

  document.getElementById("m-states").textContent = filtered.length;
  const totalAwarded = filtered.reduce((a, s) => a + s.total_awarded, 0);
  const mTotal = document.getElementById("m-total");
  mTotal.textContent = usdCompact(totalAwarded);
  mTotal.title = usd(totalAwarded);
  document.getElementById("m-states-label").textContent = currentStatus.length ? "States in this stage" : "States tracked";
  document.getElementById("m-total-label").textContent = currentStatus.length ? "Awarded to this stage, FY26" : "Total awarded, FY26";

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

  const ordered = sortStates(filtered);

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
        <td class="num amount">${usd(s.total_awarded)}${s.current_award && s.current_award.usaspending_url ? `<a class="usaspending-mark" href="${esc(s.current_award.usaspending_url)}" target="_blank" rel="noopener" title="Award amount certified against the federal award record on USASpending.gov">${USASPENDING_ICON}</a>` : ""}</td>
        <td class="num sub${sub != null ? "" : " empty"}">
          ${sub != null ? `${usd(sub)}<span class="sa-label">${esc(s.current_award.subawards_label)}</span>${disbShare(s) != null ? disbBarHtml(disbShare(s)) : ""}` : "—"}
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
          <div class="sc-amount">${usd(s.total_awarded)}${s.current_award && s.current_award.usaspending_url ? `<a class="usaspending-mark" href="${esc(s.current_award.usaspending_url)}" target="_blank" rel="noopener" title="Award amount certified against the federal award record on USASpending.gov">${USASPENDING_ICON}</a>` : ""}</div>
          <div class="sc-amount-label">FY26 award &middot; verified ${esc((s.current_award || {}).verified_at || "")}</div>
          ${sub != null ? `<div class="sc-sub">${usd(sub)} <span class="sa-label">${esc(s.current_award.subawards_label)}</span>${disbShare(s) != null ? disbBarHtml(disbShare(s)) : ""}</div>` : ""}
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
  if (metric === "sub") return disbShare(s);
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

// ---- health systems map ----
// Two Leaflet layers on one real pan/zoom tile map: a small curated layer of
// health-system OPERATORS (companies — from our own sourced dataset, shown
// at every zoom level since there are only a couple dozen) and a live layer
// of every individual hospital FACILITY nationwide, queried straight from
// HIFLD/FEMA's public ArcGIS feature service and clustered so all ~7,100 of
// them stay usable at every zoom level — nothing about the live layer is
// stored on this site, so it's only ever as current as HIFLD.

const HIFLD_HOSPITALS_URL = "https://services2.arcgis.com/FiaPA4ga0iQKduv3/arcgis/rest/services/Hospitals/FeatureServer/0/query";
const HIFLD_PAGE_SIZE = 2000; // the service's own maxRecordCount — paged through fully, once, rather than per pan/zoom

let hsMap = null;
let hsOperatorLayer = null;
let hsFacilityLayer = null; // an L.markerClusterGroup once the plugin loads, else a plain layerGroup
let hsShowOperators = true;
let hsShowFacilities = true;
let hsFacilitiesLoaded = false;
let hsFacilitiesLoading = false;
let hsFacilitiesCount = 0;
let hsFetchedAt = null; // when the live HIFLD pull last completed, for an on-page "as of" timestamp
let hsNewestSourceDate = null; // newest per-record SOURCEDATE in the pull — HIFLD's hospital layer is a frozen snapshot, so "fetched live" says nothing about how current it is
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

// HIFLD's OWNER field is a free-ish text taxonomy (NON-PROFIT, PROPRIETARY,
// GOVERNMENT - STATE/FEDERAL/..., NOT AVAILABLE) — coarser-matched here into
// the same three-way split used elsewhere on the map/legend.
function facilityOwnerColorVar(owner) {
  const o = (owner || "").toUpperCase();
  if (o.includes("NON-PROFIT") || o.includes("NONPROFIT")) return "--owner-nonprofit";
  if (o.includes("PROPRIETARY")) return "--owner-forprofit";
  if (o.includes("GOVERNMENT")) return "--owner-government";
  return "--owner-unknown";
}

function facilityRadius(beds) {
  const b = Math.max(0, Number(beds) || 0); // HIFLD uses -999 as a "no data" sentinel, not a real bed count
  return Math.max(4, Math.min(13, 3 + Math.sqrt(b) * 0.8));
}

function currentFilteredOperators() {
  return HEALTH_SYSTEMS.filter(h =>
    (hsTierFilter === "all" || h.tier === hsTierFilter) &&
    (hsOwnershipFilter === "all" || h.ownership_type === hsOwnershipFilter)
  );
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

function operatorPopupHtml(h) {
  return `
    <div class="hs-popup">
      <div class="hs-popup-title">${esc(h.name)}</div>
      <div>${titleCase(h.tier)} operator · ${h.ownership_type === "for-profit" ? "For-profit" : "Nonprofit"}</div>
      <div>${h.hospital_count} hospitals · HQ ${esc(h.hq_city)}, ${esc(h.hq_state)}</div>
      ${h.confidence === "approximate" ? `<div class="hs-popup-caution">Approximate count</div>` : ""}
      <div class="hs-popup-meta">Verified ${esc(h.verified_at || "date unknown")}</div>
      <a href="${esc(h.source_url)}" target="_blank" rel="noopener">Source ↗</a>
    </div>
  `;
}

function renderOperatorLayer() {
  if (!hsOperatorLayer) return;
  hsOperatorLayer.clearLayers();
  if (!hsShowOperators) return;
  currentFilteredOperators().forEach(h => {
    L.circleMarker([h.hq_lat, h.hq_lon], {
      radius: tierRadius(h.tier),
      color: "var(--surface)",
      weight: 2,
      fillColor: `var(${ownershipColorVar(h.ownership_type)})`,
      fillOpacity: 0.92,
      pane: "operators",
    })
      .bindPopup(operatorPopupHtml(h), HS_POPUP_OPTIONS)
      .addTo(hsOperatorLayer);
  });
}

// ---- parent-operator matching ----
// Ties an individual live HIFLD facility back to a curated operator roster
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

// HIFLD leaves plenty of fields blank per facility — text fields as the
// literal string "NOT AVAILABLE", numeric fields (BEDS, TTL_STAFF) as a
// -999 sentinel — each line below is only shown when the source actually
// has that value, rather than padding the popup with placeholders.
function facilityPopupHtml(p, match) {
  const na = v => v && String(v).toUpperCase() !== "NOT AVAILABLE";
  const num = v => (Number.isFinite(v) && v >= 0 ? v : null); // filters the -999 "no data" sentinel
  const address = [p.ADDRESS, `${p.CITY || ""}, ${p.STATE || ""}${na(p.COUNTY) ? ` (${p.COUNTY} County)` : ""}`]
    .filter(Boolean).join(", ");
  const phoneDigits = na(p.TELEPHONE) ? String(p.TELEPHONE).replace(/[^\d+]/g, "") : null;
  const website = na(p.WEBSITE) ? (/^https?:\/\//.test(p.WEBSITE) ? p.WEBSITE : "https://" + p.WEBSITE) : null;
  const sourceDate = na(p.SOURCEDATE) ? fmtDate(String(p.SOURCEDATE).slice(0, 10)) : null;
  // "Cite it when we can't link it" — an explicit, visible line either way,
  // never silently omitted, so absence of a match reads as "not identified"
  // rather than "not part of anything."
  const parentLine = match
    ? `<div>Part of <strong>${esc(match.company)}</strong> (roster verified ${esc(match.verified_at || "date unknown")}) · <a href="${esc(match.source_url)}" target="_blank" rel="noopener">Source</a></div>`
    : `<div class="hs-popup-caution">Parent operator not identified</div>`;

  return `
    <div class="hs-popup">
      <div class="hs-popup-title">${esc(p.NAME || "Unnamed facility")}</div>
      <div>${esc(titleCase(p.TYPE || "Hospital"))} · ${esc(titleCase((p.OWNER || "Ownership not available").replace(/\s*-\s*/g, " ")))}</div>
      <div>${address}</div>
      <div>${[
        num(p.BEDS) ? `${p.BEDS} beds` : null,
        num(p.TTL_STAFF) ? `${p.TTL_STAFF} staff` : null,
        na(p.TRAUMA) ? `Trauma level ${p.TRAUMA}` : null,
        String(p.HELIPAD).toUpperCase() === "Y" ? "Helipad" : null,
      ].filter(Boolean).map(esc).join(" · ")}</div>
      ${parentLine}
      ${phoneDigits ? `<div><a href="tel:${esc(phoneDigits)}">${esc(p.TELEPHONE)}</a></div>` : ""}
      ${website ? `<div><a href="${esc(website)}" target="_blank" rel="noopener">Website ↗</a></div>` : ""}
      ${sourceDate ? `<div class="hs-popup-caution">HIFLD source data as of ${esc(sourceDate)}</div>` : ""}
    </div>
  `;
}

function updateHsStatus(message) {
  const el = document.getElementById("hs-status");
  if (el) el.textContent = message;
}

function offFacilitiesMessage() {
  return `Live hospital layer is off — turn on “All hospitals (HIFLD)” above to show all ${hsFacilitiesCount ? hsFacilitiesCount.toLocaleString() + " " : ""}U.S. hospitals, clustered.`;
}

function loadedFacilitiesMessage() {
  const newest = hsNewestSourceDate
    ? ` Caution: the newest record in this dataset is dated ${fmtDate(hsNewestSourceDate)} — hospitals that have opened, closed, or been renamed or sold since then aren't reflected.`
    : "";
  const fetched = hsFetchedAt ? ` (Retrieved from HIFLD ${fmtDateTime(hsFetchedAt)}.)` : "";
  return `Showing ${hsFacilitiesCount.toLocaleString()} hospitals from HIFLD's federal hospital layer, clustered — zoom in to split a cluster apart, click any marker for details.${newest}${fetched}`;
}

// Fetches the full nationwide dataset once (paginating through HIFLD's own
// 2,000-record page size) and hands it all to the cluster group in one
// batch, rather than re-fetching a viewport slice on every pan/zoom — the
// clustering plugin is what makes rendering all of them at once workable.
async function ensureFacilitiesLoaded() {
  if (hsFacilitiesLoaded || hsFacilitiesLoading || !hsFacilityLayer) return;
  hsFacilitiesLoading = true;

  const allFeatures = [];
  let offset = 0;
  try {
    for (;;) {
      updateHsStatus(`Loading hospitals from HIFLD… (${allFeatures.length.toLocaleString()} so far)`);
      const params = new URLSearchParams({
        where: "STATUS='OPEN'",
        outFields: "NAME,ADDRESS,CITY,STATE,COUNTY,TELEPHONE,BEDS,TTL_STAFF,OWNER,TYPE,TRAUMA,HELIPAD,WEBSITE,SOURCEDATE",
        resultOffset: String(offset),
        resultRecordCount: String(HIFLD_PAGE_SIZE),
        f: "geojson",
      });
      const res = await fetch(`${HIFLD_HOSPITALS_URL}?${params}`);
      const data = await res.json();
      const page = data.features || [];
      allFeatures.push(...page);
      if (page.length < HIFLD_PAGE_SIZE) break; // last page
      offset += HIFLD_PAGE_SIZE;
    }
  } catch {
    hsFacilitiesLoading = false;
    updateHsStatus("Couldn't reach HIFLD's hospital data right now — the operator layer above is still unaffected.");
    return;
  }

  // A handful of HIFLD rows carry null/placeholder geometry (unmapped
  // facilities) — skip those rather than hand Leaflet a NaN center, which
  // renders as a broken SVG path.
  const markers = allFeatures
    .filter(f => {
      const c = f.geometry && f.geometry.coordinates;
      return Array.isArray(c) && Number.isFinite(c[0]) && Number.isFinite(c[1]);
    })
    .map(f => {
      const p = f.properties || {};
      const [lon, lat] = f.geometry.coordinates;
      const match = matchParentCompany(p.NAME, p.CITY, p.STATE);
      const marker = L.circleMarker([lat, lon], {
        radius: facilityRadius(p.BEDS),
        color: "var(--surface)",
        weight: 1.5,
        fillColor: `var(${facilityOwnerColorVar(p.OWNER)})`,
        fillOpacity: 0.88,
      }).bindPopup(facilityPopupHtml(p, match), HS_POPUP_OPTIONS);
      marker.companyKey = match ? match.company : "unmatched";
      marker.beds = Number.isFinite(p.BEDS) && p.BEDS >= 0 ? p.BEDS : 0; // -999 sentinel already excluded
      return marker;
    });

  hsNewestSourceDate = allFeatures
    .map(f => String((f.properties || {}).SOURCEDATE || "").slice(0, 10))
    .filter(s => /^\d{4}-\d{2}-\d{2}$/.test(s))
    .sort().pop() || null;
  hsAllFacilityMarkers = markers;
  hsFacilitiesCount = markers.length;
  hsFacilitiesLoaded = true;
  hsFacilitiesLoading = false;
  hsFetchedAt = new Date();
  applyFacilityFilter();
  updateHsStatus(hsShowFacilities ? loadedFacilitiesMessage() : offFacilitiesMessage());
  if (!document.getElementById("hs-compare-overlay").hidden) renderCompareModalBody(); // fill in live columns if the modal was opened before the fetch finished
}

// Re-populates the cluster group from the already-loaded marker set — no
// re-fetch — whenever the parent-operator dropdown or the layer toggle
// changes which subset should be visible.
function applyFacilityFilter() {
  if (!hsFacilityLayer || !hsFacilitiesLoaded) return;
  hsFacilityLayer.clearLayers();
  const filtered = hsCompanyFilter === "all"
    ? hsAllFacilityMarkers
    : hsAllFacilityMarkers.filter(m => m.companyKey === hsCompanyFilter);
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
    <div class="hs-legend-group">
      <span class="hs-legend-title">Color = ownership</span>
      <span class="hs-legend-item" title="Tax-exempt / mission-driven operator, as reported by the source"><span class="hs-dot" style="background:var(--owner-nonprofit)"></span>Nonprofit</span>
      <span class="hs-legend-item" title="Investor- or privately-owned operator, as reported by the source"><span class="hs-dot" style="background:var(--owner-forprofit)"></span>For-profit</span>
      <span class="hs-legend-item" title="Federal, state, or county-run facility — appears only in the per-facility hospital layer, since none of the curated operators above are government agencies"><span class="hs-dot" style="background:var(--owner-government)"></span>Government (hospital layer only)</span>
    </div>
  `;
}

// Tier/ownership filters only touch the curated operator layer — refresh
// just that (and the list) rather than re-checking the map/live layer too.
function refreshHsOperators() {
  renderHealthSystemsList(currentFilteredOperators());
  renderOperatorLayer();
}

// ---- compare-operators modal ----
// "Live matched" columns are computed on the spot from whatever HIFLD data
// is already loaded (or being loaded) for the live layer — not a stored
// figure — so they're always as current as that layer, and read as "—"
// rather than 0 until the fetch finishes.
function operatorLiveStats(name) {
  if (!hsFacilitiesLoaded) return null;
  const matched = hsAllFacilityMarkers.filter(m => m.companyKey === name);
  return { count: matched.length, beds: matched.reduce((sum, m) => sum + (m.beds || 0), 0) };
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
          <th>Matched beds${liveNote}</th>
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
              <td>${live && live.beds ? live.beds.toLocaleString() : "—"}</td>
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
  renderHealthSystemsList(currentFilteredOperators());
  renderHsLegend();
  renderCuratedFreshness();

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

function renderHealthSystemsList(list) {
  const sorted = [...list].sort((a, b) => b.hospital_count - a.hospital_count);
  document.getElementById("hs-list").innerHTML = sorted.map(h => `
    <div class="hs-card" id="hs-row-${h.id}">
      <div class="hs-card-head">
        <span class="stage-pill" style="--stage-color:var(${tierColorVar(h.tier)})">${titleCase(h.tier)}</span>
        <h3>${esc(h.name)}</h3>
        <span class="stage-pill" style="--stage-color:var(${ownershipColorVar(h.ownership_type)})">${h.ownership_type === "for-profit" ? "For-profit" : "Nonprofit"}</span>
        ${h.confidence === "approximate" ? `<span class="caution-tag">Approximate count</span>` : ""}
      </div>
      <div class="hs-card-body">
        <span>${h.hospital_count} hospitals</span>
        <span>HQ: ${esc(h.hq_city)}, ${esc(h.hq_state)}</span>
        <span>Verified ${esc(h.verified_at || "date unknown")}</span>
      </div>
      ${h.notes ? `<p class="hs-notes">${esc(h.notes)}</p>` : ""}
      <a class="tl-source" href="${esc(h.source_url)}" target="_blank" rel="noopener">Source ↗</a>
    </div>
  `).join("") || `<p style="text-align:center; color:var(--muted); padding:24px 0;">No systems match this filter.</p>`;
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
              ? `<ul class="pillar-detail-list">${pillars.map(p => `
                  <li class="pillar-detail-item">
                    <div class="pillar-name">${esc(p.name)}</div>
                    ${p.description ? `<div class="pillar-desc">${esc(p.description)}</div>` : `<div class="pillar-desc pillar-desc-empty">Not yet detailed in current sources.</div>`}
                  </li>
                `).join("")}</ul>`
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
        ${latest.usaspending_url ? `<a class="usaspending-badge" href="${esc(latest.usaspending_url)}" target="_blank" rel="noopener" title="This FY26 award amount is cross-checked against the federal award record on USASpending.gov">${USASPENDING_ICON} USASpending Certified</a>` : ""}
        ${latest.subawards_amount ? `<div class="sub">${usd(latest.subawards_amount)} <span class="sa-label">${esc(latest.subawards_label)}</span>${disbShare(s) != null ? disbBarHtml(disbShare(s)) : ""}</div>` : ""}
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
        ${latest.usaspending_url ? `<a href="${esc(latest.usaspending_url)}" target="_blank" rel="noopener">Federal award record (USASpending.gov) ↗</a>` : ""}
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
