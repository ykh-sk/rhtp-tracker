"""Load app/seed_data.py into the Postgres database at DATABASE_URL.

Safe to re-run: clears and reloads all rows. Usage:
    export DATABASE_URL="<your Neon connection string>"
    python3 app/seed.py
"""

from db import get_connection, init_db, execute, execute_many
from seed_data import (
    SOURCES, AWARDS, STATUS_EVENTS, DEADLINES, ANALYSIS, COMMENTARY,
    STATE_OVERVIEW, STATE_PILLARS,
)


def seed():
    init_db()
    conn = get_connection()

    execute(conn, "DELETE FROM state_pillars")
    execute(conn, "DELETE FROM state_overview")
    execute(conn, "DELETE FROM commentary")
    execute(conn, "DELETE FROM state_analysis")
    execute(conn, "DELETE FROM deadlines")
    execute(conn, "DELETE FROM status_events")
    execute(conn, "DELETE FROM awards")
    execute(conn, "DELETE FROM sources")

    execute_many(
        conn,
        "INSERT INTO sources (state, official_url, lead_agency) VALUES (%(state)s, %(official_url)s, %(lead_agency)s)",
        SOURCES,
    )
    execute_many(
        conn,
        """INSERT INTO awards (state, fiscal_year, amount, status, source_url, verified_at, subawards_amount, subawards_label)
           VALUES (%(state)s, %(fiscal_year)s, %(amount)s, %(status)s, %(source_url)s, %(verified_at)s, %(subawards_amount)s, %(subawards_label)s)""",
        AWARDS,
    )
    execute_many(
        conn,
        """INSERT INTO status_events (state, status, source_url, event_date, notes, confidence)
           VALUES (%(state)s, %(status)s, %(source_url)s, %(event_date)s, %(notes)s, %(confidence)s)""",
        STATUS_EVENTS,
    )
    execute_many(
        conn,
        """INSERT INTO deadlines (state, title, start_date, end_date, source_url, notes, confidence)
           VALUES (%(state)s, %(title)s, %(start_date)s, %(end_date)s, %(source_url)s, %(notes)s, %(confidence)s)""",
        DEADLINES,
    )
    execute_many(
        conn,
        """INSERT INTO commentary (title, source_name, url, published_date, state, angle, summary)
           VALUES (%(title)s, %(source_name)s, %(url)s, %(published_date)s, %(state)s, %(angle)s, %(summary)s)""",
        COMMENTARY,
    )

    analysis_rows = []
    for state, entry in ANALYSIS.items():
        for i, text in enumerate(entry.get("pros", [])):
            analysis_rows.append({"state": state, "kind": "pro", "sort_order": i, "text": text})
        for i, text in enumerate(entry.get("cons", [])):
            analysis_rows.append({"state": state, "kind": "con", "sort_order": i, "text": text})
    execute_many(
        conn,
        "INSERT INTO state_analysis (state, kind, sort_order, text) VALUES (%(state)s, %(kind)s, %(sort_order)s, %(text)s)",
        analysis_rows,
    )

    overview_rows = [{"state": state, **entry} for state, entry in STATE_OVERVIEW.items()]
    execute_many(
        conn,
        """INSERT INTO state_overview (state, emphasis, applicant_profile, contact_name, contact_email, contact_note)
           VALUES (%(state)s, %(emphasis)s, %(applicant_profile)s, %(contact_name)s, %(contact_email)s, %(contact_note)s)""",
        overview_rows,
    )

    pillar_rows = []
    for state, names in STATE_PILLARS.items():
        for i, name in enumerate(names):
            pillar_rows.append({"state": state, "sort_order": i, "name": name, "source_url": None})
    execute_many(
        conn,
        "INSERT INTO state_pillars (state, sort_order, name, source_url) VALUES (%(state)s, %(sort_order)s, %(name)s, %(source_url)s)",
        pillar_rows,
    )

    conn.commit()
    conn.close()
    print(
        f"Seeded {len(SOURCES)} sources, {len(AWARDS)} awards, {len(STATUS_EVENTS)} status events, "
        f"{len(DEADLINES)} deadlines, {len(COMMENTARY)} commentary links, {len(analysis_rows)} analysis rows, "
        f"{len(overview_rows)} overviews, {len(pillar_rows)} pillars."
    )


if __name__ == "__main__":
    seed()
