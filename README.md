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
