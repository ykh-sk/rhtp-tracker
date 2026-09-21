# RHTP Tracker

Tracks Rural Health Transformation Program funding, status, and sources across 10 states.

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
  Used client-side to tag an individual hospital on the live HIFLD map layer as "part of
  `<company>`" by matching name/city/state — matching requires at least one shared, non-generic
  name token even when only one roster hospital shares that city+state (a city having exactly one
  *rostered* hospital doesn't mean it only has one hospital), so a weak or absent match reads as
  "parent operator not identified" rather than guessing. The Health Systems tab's "Compare operator
  size" button opens a table of every curated operator sorted by size, with a live-computed count of
  matched hospitals and total beds from today's HIFLD pull next to each operator's own reported
  count — patient volume isn't shown there, since no public source reports it per-operator in a
  comparable, verifiable way. See `app/health_system_rosters_data.py` for the sourced roster and how
  to add more operators or states to it.

## How this data stays current

Two very different freshness models live on this site, and it's worth being explicit about which
is which:

- **Fetched live, but not current**: the Health Systems tab's per-facility map layer queries HIFLD/FEMA's
  public ArcGIS feature service directly from the visitor's browser every time the page loads, and
  nothing about individual hospitals is stored here. But "fetched live" describes the *retrieval*, not the
  *data's age*: as of 2026-09-21 the HIFLD Hospitals layer's own last-edit date is 2018-02-05, and the
  newest per-record `SOURCEDATE` among its 7,109 open hospitals is March 2017 (most are 2016–early 2017;
  validation dates run 2013–2017). So it's a frozen snapshot: hospitals that closed, opened, were renamed
  or were sold since then aren't reflected, which also hurts roster matching (a 2026 roster name won't
  match a hospital HIFLD still lists under its 2016 name). The map's status line computes and shows the
  newest record date from the data itself so this can't silently go stale in the UI. A current
  replacement would be CMS's Hospital General Information dataset (5,419 Medicare-registered hospitals,
  updated regularly, no coordinates or bed counts — would need server-side geocoding, e.g. the free Census
  batch geocoder, and a stored table rather than a live browser fetch, since CMS's API sends no CORS headers).
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
nationally. Every one of them still shows up as an individual pin on the live HIFLD layer; they just
read as "parent operator not identified" rather than being tied to a named company, which is accurate
(no roster claims them) rather than a bug. Extending curated coverage down to that tier isn't a
scaled-up version of the current per-company approach — at 4–5 hospitals apiece it would take hundreds
more individually-researched operators — so it would need either a bulk system-affiliation dataset (e.g.
AHA Annual Survey or a CMS ownership crosswalk, most of which require a paid license) or accepting that
"not identified" will always cover a meaningful share of the live layer.

## Update policy

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
4. Deploy (Vercel does this automatically on push). The API runs as a serverless function
   (`api/index.py`); `static/` is served directly by Vercel's CDN.
5. Point your domain at this Vercel project under **Settings → Domains**.
