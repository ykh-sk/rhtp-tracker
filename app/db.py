import os

import psycopg2
import psycopg2.extras

SCHEMA = """
CREATE TABLE IF NOT EXISTS sources (
    state TEXT PRIMARY KEY,
    official_url TEXT NOT NULL,
    lead_agency TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS awards (
    id SERIAL PRIMARY KEY,
    state TEXT NOT NULL REFERENCES sources(state),
    fiscal_year TEXT NOT NULL,
    amount INTEGER NOT NULL,
    status TEXT NOT NULL,
    source_url TEXT NOT NULL,
    verified_at TEXT NOT NULL,
    subawards_amount INTEGER,
    subawards_label TEXT
);

CREATE TABLE IF NOT EXISTS status_events (
    id SERIAL PRIMARY KEY,
    state TEXT NOT NULL REFERENCES sources(state),
    status TEXT NOT NULL,
    source_url TEXT NOT NULL,
    event_date TEXT NOT NULL,
    notes TEXT NOT NULL,
    confidence TEXT NOT NULL DEFAULT 'confirmed' CHECK (confidence IN ('confirmed', 'unverified', 'personal'))
);

CREATE TABLE IF NOT EXISTS deadlines (
    id SERIAL PRIMARY KEY,
    state TEXT NOT NULL REFERENCES sources(state),
    title TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT,
    source_url TEXT NOT NULL,
    notes TEXT,
    confidence TEXT NOT NULL DEFAULT 'confirmed' CHECK (confidence IN ('confirmed', 'unverified', 'personal'))
);

CREATE TABLE IF NOT EXISTS state_analysis (
    id SERIAL PRIMARY KEY,
    state TEXT NOT NULL REFERENCES sources(state),
    kind TEXT NOT NULL CHECK (kind IN ('pro', 'con')),
    sort_order INTEGER NOT NULL,
    text TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS commentary (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    source_name TEXT NOT NULL,
    url TEXT NOT NULL,
    published_date TEXT,
    state TEXT REFERENCES sources(state),
    angle TEXT NOT NULL CHECK (angle IN ('opinion', 'analysis', 'investigative', 'news')),
    summary TEXT
);

CREATE TABLE IF NOT EXISTS state_overview (
    state TEXT PRIMARY KEY REFERENCES sources(state),
    emphasis TEXT,
    applicant_profile TEXT,
    contact_name TEXT,
    contact_email TEXT,
    contact_note TEXT,
    updated_at TEXT NOT NULL
);

-- One row per MATERIAL change to a state's overview/pillars/analysis/award
-- figures (a number, a status, a contact, a pillar list changing) — not for
-- wording/copy-editing touch-ups. This is what "Updated" badges read from,
-- and it's the audience-facing record of what changed and why.
CREATE TABLE IF NOT EXISTS state_changelog (
    id SERIAL PRIMARY KEY,
    state TEXT NOT NULL REFERENCES sources(state),
    changed_at TEXT NOT NULL,
    summary TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS state_pillars (
    id SERIAL PRIMARY KEY,
    state TEXT NOT NULL REFERENCES sources(state),
    sort_order INTEGER NOT NULL,
    name TEXT NOT NULL,
    source_url TEXT
);

-- Federal-level (not state-specific) statutory/programmatic milestones for
-- the Rural Health Transformation Program itself: the law, NOFO release,
-- application windows, award notifications, the funds-obligation deadline,
-- reporting cadence. Rendered as its own "Federal guidelines" panel and
-- cross-referenced from the calendar, distinct from any one state's deadlines.
CREATE TABLE IF NOT EXISTS federal_milestones (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL CHECK (category IN ('statute', 'application', 'award', 'obligation', 'reporting', 'other')),
    start_date TEXT NOT NULL,
    end_date TEXT,
    source_url TEXT NOT NULL,
    notes TEXT,
    confidence TEXT NOT NULL DEFAULT 'confirmed' CHECK (confidence IN ('confirmed', 'unverified', 'personal'))
);
"""


_DSN_ENV_VARS = ("DATABASE_URL", "POSTGRES_URL", "DATABASE_URL_UNPOOLED", "POSTGRES_URL_NON_POOLING")


def get_connection():
    dsn = next((os.environ[name] for name in _DSN_ENV_VARS if os.environ.get(name)), None)
    if not dsn:
        raise RuntimeError(
            "No database connection string found. Set DATABASE_URL to your Neon connection string "
            "(export DATABASE_URL=... locally — Vercel's Neon integration sets this, or one of "
            f"{_DSN_ENV_VARS[1:]}, automatically in production)."
        )
    return psycopg2.connect(dsn, cursor_factory=psycopg2.extras.RealDictCursor)


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(SCHEMA)
    conn.commit()
    conn.close()


def query(conn, sql, params=None):
    """SELECT helper: returns a list of dict-like rows."""
    cur = conn.cursor()
    cur.execute(sql, params or {})
    return cur.fetchall()


def execute(conn, sql, params=None):
    """INSERT/UPDATE/DELETE helper for a single statement."""
    cur = conn.cursor()
    cur.execute(sql, params or {})


def execute_many(conn, sql, param_list):
    cur = conn.cursor()
    cur.executemany(sql, param_list)
