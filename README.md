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
