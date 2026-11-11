# RHTP Tracker

Tracks Rural Health Transformation Program funding, status, and sources across all 50 states.

## Two pages, one backend

- `/` — **Rural Health Radar** (`static/index.html` + `app.js`): the state-by-state RHTP funding tracker.
- `/atlas` — **Health Systems Atlas** (`static/atlas.html` + `atlas.js` + `bd.js`): the map, landscape and
  outreach views of U.S. health systems. A separate page with its own identity, linked both ways; it uses
  the Radar's API only to show each system's home-state RHTP stage as optional context.
- Each state page on the Radar has a small zoomable map of that state's health systems and hospitals
  (`/api/atlas_state/<ST>`), with an "Open in the Health Systems Atlas" link that opens `/atlas?state=<State>` already filtered.
- `static/common.js` holds the helpers both pages share (escaping, date/money formats, theme toggle,
  pipeline-stage colors). Both pages use the same Flask API and database.
- The Atlas's **Outreach** tab (who has been contacted, by whom) is invisible until a team member signs in
  (one shared password, `BD_PASSWORD`; see "Deploying"). Signed out, the page shows no status controls at all
  and the API refuses the data (401).

## Local setup

Requires a Postgres database (this project uses [Neon](https://neon.tech)). Get a connection
string first (see "Deploying" below if you don't have one yet), then:

```bash
pip3 install -r requirements.txt
export DATABASE_URL="postgres://...neon connection string..."
python3 app/seed.py   # creates the schema and loads seed data
python3 app/main.py   # serves the dashboard at http://localhost:5050
```

## Data model (Postgres via `DATABASE_URL`)

- `sources` — one row per state: official program page + lead agency.
- `awards` — FY26 award amount, status, subawards figure (if known), and the source article.
- `status_events` — append-only status history per state. Corrections are added as new dated rows,
  never edited in place, so a state's page reads as a thread rather than a value that silently changed.
- `deadlines` — dated application windows, each with a `confidence` of `confirmed` or `unverified`
  (unverified ones render with a caution flag instead of being dropped).
- `state_analysis` — editorial pros/cons per state, clearly separated from sourced facts.
- `commentary` — third-party opinion/analysis/investigative/news links, shown on their own page.
- `state_overview` / `state_pillars` — the Program Overview section (emphasis, pillars, applicant
  profile, contact). `contact_email` is left `NULL` with a `contact_note` explaining why whenever a
  state hasn't published one — never guessed or constructed from a name.
- `state_changelog` — see "Update policy" below.
- `health_systems` — the "Health Systems" tab's data: a curated (not bulk-imported) list of notable
  hospital/health-system operators, sized small/mid/large/major by hospital count, each with a
  `source_url` and a `confidence` of `confirmed` or `approximate`. See
  `app/health_systems_data.py` for the sourced dataset — extend it the same way you'd extend
  `seed_data.py`.
- `hospital_roster` — one row per hospital in a curated operator's own official location directory.
  Used client-side to tag an individual hospital on the per-facility CMS map layer as "part of
  `<company>`" by matching name/city/state — matching requires at least one shared, non-generic
  name token even when only one roster hospital shares that city+state (a city having exactly one
  *rostered* hospital doesn't mean it only has one hospital), so a weak or absent match reads as
  "parent operator not identified" rather than guessing. The Health Systems tab's "Compare operator
  size" button opens a table of every curated operator sorted by size, with a live-computed count of
  matched hospitals from the CMS layer next to each operator's own reported count — no bed or
  patient-volume column: CMS's dataset doesn't publish bed counts, and no public source reports
  patient volume per-operator in a comparable, verifiable way. See `app/health_system_rosters_data.py`
  for the sourced roster and how to add more operators or states to it.
- `cms_hospitals` / `cms_hospitals_meta` — the per-facility map layer: every U.S. hospital in CMS's
  "Hospital General Information" dataset (Medicare-registered hospitals), geocoded once server-side
  and stored, not fetched live from the browser (see "How this data stays current" below for why).
  `app/data/cms_hospitals.json` is the checked-in snapshot `seed.py` loads from; there's no
  hand-maintained Python source file for this one since it's a bulk import, not a curated pick.

- `bd_profiles` — the BD layer's taxonomy, merged in from the standalone "Health System Atlas": a
  `category` (academic / faith-based / secular nonprofit / for-profit / payer-provider / public /
  specialty), `strategy_tags` (venture arm, digital pilots, value-based care, rural focus, ...) and a
  one-line `note` per system. **Every row is `confidence = 'unverified'`**: unlike `health_systems`,
  nothing here has a per-row source (compiled from general public knowledge, Sept 2026). A profile
  attaches to a curated operator through the hand-written `OPERATOR_CROSSWALK` in
  `app/bd_profiles_data.py` (exact / renamed / partial matches, no fuzzy matching); profiles with no
  operator record render as "profile only" pins with no hospital count. Where both exist the operator's
  sourced fields (hospital count, ownership, HQ, source) win; the profile only adds category, signals
  and the note. Two systems the team has dealt with directly (Marshall Health Network, Vandalia Health)
  were added from the team's own target list rather than from Atlas, and say so in `basis`.
- `bd_outreach` — private contact tracking (status / owner / notes per system), written only through the
  password-gated `/api/bd/*` routes. **`seed.py` never clears this table** — it's hand-entered working
  data, not seed data. Keys are slugs (`slug(operator name)` or the profile's own key).
- `bd_login_failures` — failed unlock attempts, kept only to throttle guessing (8 per IP per 15 min).

- `ahrq_systems` / `ahrq_crosswalk` — AHRQ's free **Compendium of U.S. Health Systems, 2023** (system file,
  `app/data/ahrq/chsp-compendium-2023-rev.csv`): 639 systems with hospital, bed, discharge, physician and
  net-revenue counts, ownership and a few teaching / safety-net flags. `app/ahrq_data.py` says exactly what
  is used and why: counts and the flags whose names are self-explanatory are used as published; the
  ownership code is decoded by **inference** (AHRQ's technical documentation could not be read);
  `sys_multistate`, `sys_teachint` and `deg_children` are not used because their code meanings are
  unconfirmed. Home-office coordinates are derived from CMS hospital locations (AHRQ gives only city and
  state). `ahrq_crosswalk` is a hand-written link from our systems to AHRQ's (136 links, in
  `app/ahrq_crosswalk_data.py`; nothing is fuzzy-matched at runtime). The 503 AHRQ systems with no match
  in our lists appear as their own entries (outreach key `ahrq-<id>`). The 2023 file predates later
  mergers. **Not loaded:** AHRQ's separate *hospital linkage file* (hospital CCN -> system), which would let
  the CMS hospital layer show each hospital's parent system.

The Health Systems tab is systems-first: the unified list (`SYSTEMS_UNIFIED` in `static/bd.js`) is every
curated operator plus every profile-only system. The RHTP stage of a system's HQ state is shown as an
optional "tailwind" and a filter, never as a requirement for a system to appear. The tab's **Landscape**
view breaks the national picture down by category x size, by state (CMS hospital counts by ownership,
critical-access count, systems HQ'd, RHTP stage) and by hospital type. Known gap: the CMS layer has no
parent-system field, so only the hospitals matched through the curated rosters (about a quarter) are tied
to a system; the free AHRQ Compendium of U.S. Health Systems would close most of that gap by linking CMS
hospital IDs to systems.

## How each entry is classified ("Type")

Every entry in the Atlas carries one Type, shown as a chip and usable as a filter:

| Type | What it is | Where it comes from | Size / ownership |
|---|---|---|---|
| **Sourced operator** | Hospital operator in the curated list | `app/health_systems_data.py` (source link + verified date) | Own hospital count; ownership as reported by the source |
| **Profile system** | System from the BD profile list | `app/bd_profiles_data.py` (**unverified** category / strategy / note) | From AHRQ when matched, else none |
| **AHRQ system** | System that appears only in AHRQ's 2023 file | `app/data/ahrq/…csv` | AHRQ's counts; ownership decoded from AHRQ's code (inferred) |
| **Community provider** | A single provider, not a system: community health center (FQHC), home health agency or community hospital. West Virginia (92 entries) plus health centers in NV, AZ, TN, KY, CO, AK, WY (139) | `wv_providers_data.py`, `focus_fqhc_data.py`, generated from HRSA and CMS public data (each row names its source) | None |
| **Network / association / other** | Not a hospital system: hospital network, association, university, tribal health organization | `bd_profiles_data.py` categories `network`, `association`, `tribal`, `university` | None |

Overlaps are handled by hand-written files, not guessed at runtime:

- `ahrq_crosswalk_data.py` links our entries to AHRQ systems (136 links) and lists AHRQ 2023 systems that have
  since **merged** into one of our entries (ThedaCare, Lehigh Valley, Nuvance): those are not listed twice; the
  surviving entry says "AHRQ also lists …".
- `PART_OF` in `bd_profiles_data.py` marks brands and members of a larger entry (e.g. MercyOne, part of Trinity
  Health), shown as "Part of …".
- Two different organizations with the same name (e.g. Memorial Health System in IL and OH) are shown with
  their state.

### West Virginia providers and seeded outreach

`wv_providers_data.py` adds West Virginia's 30 HRSA health-center grantees, 33 Medicare-certified home health
agencies and 29 community hospitals (CMS hospitals not already counted inside a listed system; their parent
systems were not researched, so each says "verify"). `focus_fqhc_data.py` adds the HRSA health-center grantees of Nevada, Arizona, Tennessee, Kentucky, Colorado, Alaska and Wyoming; other states have only systems for now.

`app/bd_initial_data.py` holds the private starting records for the password-protected Outreach tab. It is
**gitignored** because this repository is public; `seed.py` loads it only when the file exists locally, so seed
from the machine that has it. Seeding never overwrites later edits.

## How this data stays current

Two very different freshness models live on this site, and it's worth being explicit about which
is which:

- **A server-side snapshot, refreshed by re-running the fetch — not curated by hand, and not live**:
  the Health Systems tab's per-facility map layer used to query HIFLD/FEMA's public ArcGIS feature
  service directly from the visitor's browser on every page load. That turned out to be misleading:
  "fetched live" described the *retrieval*, not the *data's age* — HIFLD's hospital layer's own
  last-edit date was 2018-02-05, and the newest per-record date among its 7,109 "open" hospitals was
  March 2017, so it was a frozen snapshot silently going stale in the UI (hospitals that closed,
  opened, were renamed, or were sold since 2017 weren't reflected, which also broke roster matching
  against current company names).

  It's now CMS's own "Hospital General Information" dataset instead — 5,419 Medicare-registered
  hospitals, actively maintained by CMS (last modified 2026-07-22 as of this snapshot), pulled and
  geocoded once server-side (`data.cms.gov` sends no CORS headers, so a browser can't fetch it
  directly, and the dataset has no coordinates of its own — see `app/seed.py` for the Census
  batch-geocoder + ZIP/city-centroid fallback pipeline that built `app/data/cms_hospitals.json`) and
  served from this site's own DB via `/api/cms_hospitals`, the same as every other table here. That
  makes it a **snapshot with a known, honestly-labeled age** (the map's status line shows both CMS's
  own last-modified date and when this site last pulled it) rather than a live feed — refreshing it
  means re-running the fetch/geocode pipeline and re-seeding, not something that happens automatically.
  It also runs smaller than HIFLD's count: CMS's dataset excludes most freestanding long-term-care and
  rehabilitation hospitals (they report through separate CMS quality programs, not this file) — a
  scope difference, not missing data, and it's stated in the UI rather than left for someone to notice.
- **Curated snapshots, re-checked manually**: everything else — the RHTP funding data, the
  `health_systems` operator list, and the `hospital_roster` parent-operator rosters — is a dated,
  sourced snapshot, the same as the rest of this site's data (see "Update policy" below). The
  `hospital_roster` in particular can't be fetched live: most operators' own site directories don't
  expose a stable public API, so building it out (more operators, fuller state coverage) means
  re-running the same manual gathering process against each company's official directory and
  bumping `verified_at` — not an automated refresh.

### Keeping the 26 operators current

There's no single "as of" date for this dataset — each operator was verified independently, and the
Health Systems tab's "Compare operator size" popup and each entry's own card show that date rather than
implying a site-wide refresh happened. A realistic cadence: re-run the same per-company gathering
process roughly **quarterly**, prioritized by how likely an operator is to have actually changed
(divestitures/mergers — ScionHealth and Sanford both needed mid-cycle corrections in 2026 — matter more
than a stale-but-unchanged roster). There's no cheap way to detect drift automatically, since the
underlying source is each operator's own website, not an API with a last-modified date; a changed
`hospital_count` on an operator's own site, noticed on a manual spot-check, is usually what triggers a
re-check rather than a fixed schedule catching it first.

### What the 26 operators don't cover

This list is explicitly **notable multi-state/regional operators**, not the whole hospital ownership
landscape — and there's no stated hospital-count floor for inclusion; the `tier` cutoffs (major ≥90,
large 40–89, mid 15–39, small <15) are a labeling scheme applied to whatever got picked, not a
selection gate. It so happens the two smallest entries (Essentia Health, Baptist Health Kentucky) have
10–14 hospitals each, but that's a byproduct of how the list was built — from name-recognition sources
(Becker's "100 largest" rankings, Wikipedia) plus targeted follow-ups on rural-relevant systems — not a
rule that excluded anything smaller. A genuinely small (4–5 hospital) system that's locally notable,
especially in one of the states this tracker follows, is in scope; it just hasn't been looked up yet.
Small regional systems in that range, and the much larger population of single-hospital independents,
aren't represented here at all — and there are hundreds of the former and thousands of the latter
nationally. Every one of them still shows up as an individual pin on the CMS facility layer; they just
read as "parent operator not identified" rather than being tied to a named company, which is accurate
(no roster claims them) rather than a bug. Extending curated coverage down to that tier isn't a
scaled-up version of the current per-company approach — at 4–5 hospitals apiece it would take hundreds
more individually-researched operators — so it would need either a bulk system-affiliation dataset (e.g.
AHA Annual Survey or a CMS ownership crosswalk, most of which require a paid license) or accepting that
"not identified" will always cover a meaningful share of the live layer.

## Update policy

`app/nov_pass_data.py` holds a follow-up sweep (Oct 1 - Nov 10, 2026 developments the first Nov 10 pass
missed: named awards, solicitation deadlines, a few corrections). It is merged at the bottom of
`seed_data.py`, like `new_states_data.py`, so earlier entries stay untouched. New events never lower a
state's stage, so sub-program solicitations carry the state's current stage. Year 2 award amounts (CMS table
of Nov 9) are not modeled; the award table is FY26.

This site gets re-checked and edited roughly every couple of days. Two different kinds of "update"
need different handling:

**Sourced facts** (`status_events`, `deadlines`, award figures) — already append-only. A correction is
a *new* dated row referencing what changed; the original stays visible. Never edit these rows in place.

**Editorial/summary content** (`state_overview`, `state_pillars`, `state_analysis`) — these are
"current snapshot" fields, not a thread. The rule for editing them:

- **Cosmetic** (wording, typo fixes, tightening a sentence with no new facts) — just edit it. No
  changelog entry, no visible notice. The audience doesn't need to know a sentence got smoother.
- **Material** (a number changes, a contact appears, a pillar list changes, a status/stage moves,
  anything that would change someone's actual decision) — add a row to `state_changelog`
  (`state`, `changed_at`, `summary`) describing what changed, in `app/seed_data.py`'s
  `STATE_CHANGELOG` list, and bump that state's `updated_at` in `STATE_OVERVIEW` to the same date.

A state with a changelog entry from the last 5 days (`RECENT_CHANGE_WINDOW_DAYS` in `static/app.js`)
gets a pink "Updated" badge next to its name on the dashboard and a banner on its detail page showing
the changelog summary — then the badge quietly disappears once it ages out. No manual cleanup needed.
Adjust the 5-day window there if the re-check cadence changes.

When in doubt about cosmetic vs. material: if it would be *wrong* for a returning visitor to keep
believing what the old text said, it's material.

Status taxonomy: `plan approved` → `admin structure named` → `RFA issued` → `subawards announced` → `funds obligated`.

To add a new status update: `POST /api/status_events` with `state`, `status`, `source_url`, `event_date`, `notes`
(optionally `confidence`, defaults to `confirmed`). Same pattern for `POST /api/deadlines`.

`docs/rhtp-seed-data.md` is kept as the original verified snapshot; `app/seed_data.py` is its structured,
re-runnable form — edit `seed_data.py` and re-run `python3 app/seed.py` (pointed at your `DATABASE_URL`)
to refresh the database. Re-running `seed.py` clears and reloads every table, so it's always safe to re-run,
but any data you added purely via the API (not in `seed_data.py`) will be wiped — treat `seed_data.py` as
the source of truth and the API as a way to preview additions before folding them in there.

## Deploying (Vercel + Neon)

1. Push this repo to GitHub, then import it in Vercel as a new project.
2. In the Vercel project: **Storage** tab → **Connect Database** → **Neon** → follow the prompts. This
   creates a Neon Postgres project and sets `DATABASE_URL` in your Vercel environment automatically.
3. Copy that same `DATABASE_URL` into your local shell and run `python3 app/seed.py` once to populate it.
3b. Set `BD_PASSWORD` (Vercel → Settings → Environment Variables, and locally) to enable contact
   tracking. The login ID is fixed and not secret — `bd` by default, overridable with `BD_USERNAME`; the
   password is what protects the data, and it must only ever live in the environment, never in the repo. Unset, every `/api/bd/*` write/read fails closed with a 503 and the UI says it isn't set up.
   Use a long random password; changing it logs every existing session out. Re-seeding is required once
   after this release (new tables/columns) but never touches `bd_outreach`.
4. Deploy (Vercel does this automatically on push). The API runs as a serverless function
   (`api/index.py`); `static/` is served directly by Vercel's CDN.
5. Point your domain at this Vercel project under **Settings → Domains**.
