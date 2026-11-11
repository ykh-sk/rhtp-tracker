// Helpers shared by the Rural Health Radar (app.js) and the Health Systems Atlas (atlas.js).

const STATE_ABBR = {
  AL: "Alabama", AK: "Alaska", AZ: "Arizona", AR: "Arkansas", CA: "California", CO: "Colorado",
  CT: "Connecticut", DE: "Delaware", DC: "District of Columbia", FL: "Florida", GA: "Georgia",
  HI: "Hawaii", ID: "Idaho", IL: "Illinois", IN: "Indiana", IA: "Iowa", KS: "Kansas", KY: "Kentucky",
  LA: "Louisiana", ME: "Maine", MD: "Maryland", MA: "Massachusetts", MI: "Michigan", MN: "Minnesota",
  MS: "Mississippi", MO: "Missouri", MT: "Montana", NE: "Nebraska", NV: "Nevada", NH: "New Hampshire",
  NJ: "New Jersey", NM: "New Mexico", NY: "New York", NC: "North Carolina", ND: "North Dakota",
  OH: "Ohio", OK: "Oklahoma", OR: "Oregon", PA: "Pennsylvania", RI: "Rhode Island",
  SC: "South Carolina", SD: "South Dakota", TN: "Tennessee", TX: "Texas", UT: "Utah", VT: "Vermont",
  VA: "Virginia", WA: "Washington", WV: "West Virginia", WI: "Wisconsin", WY: "Wyoming",
};

function stateAbbrOf(name) {
  return Object.keys(STATE_ABBR).find(k => STATE_ABBR[k] === name) || "";
}

function usd(n) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(n);
}

// Abbreviated form ("$9.98B", "$1.23M") for large summary figures where
// scannability matters more than the exact dollar — every other dollar
// figure on the site still uses usd() at full precision.
function usdCompact(n) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", notation: "compact", maximumFractionDigits: 2 }).format(n);
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

function fmtDate(iso) {
  return new Date(iso + "T00:00:00").toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

function stageVar(status) {
  const s = STAGES.find(s => s.key === status);
  return s ? `var(${s.var})` : "var(--muted)";
}

function stageIndex(status) {
  return STAGES.findIndex(s => s.key === status);
}

function latestConfirmedEvent(s) {
  const events = s.status_events || [];
  const confirmed = events.filter(e => e.confidence === "confirmed");
  const pool = confirmed.length ? confirmed : events;
  return pool.length ? pool[pool.length - 1] : null;
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

