from pathlib import Path

from flask import Flask, jsonify, request

from db import get_connection, query, execute
from seed_data import STATUS_TAXONOMY

BASE_DIR = Path(__file__).resolve().parent.parent

ANALYSIS_DISCLAIMER = (
    "Editorial notes derived from the sources linked on this page — a starting point for "
    "comparison, not official guidance. Verify anything decision-critical directly with the state agency."
)

app = Flask(
    __name__,
    static_folder=str(BASE_DIR / "static"),
    template_folder=str(BASE_DIR / "templates"),
)


def rows_to_dicts(rows):
    return [dict(row) for row in rows]


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/api/states")
def api_states():
    conn = get_connection()
    sources = rows_to_dicts(query(conn, "SELECT * FROM sources ORDER BY state"))
    awards = rows_to_dicts(query(conn, "SELECT * FROM awards ORDER BY state"))
    events = rows_to_dicts(query(conn, "SELECT * FROM status_events ORDER BY state, event_date"))
    analysis = rows_to_dicts(query(conn, "SELECT * FROM state_analysis ORDER BY state, kind, sort_order"))
    overviews = rows_to_dicts(query(conn, "SELECT * FROM state_overview"))
    pillars = rows_to_dicts(query(conn, "SELECT * FROM state_pillars ORDER BY state, sort_order"))
    changelog = rows_to_dicts(query(conn, "SELECT * FROM state_changelog ORDER BY state, changed_at DESC"))
    conn.close()

    awards_by_state = {}
    for a in awards:
        awards_by_state.setdefault(a["state"], []).append(a)
    events_by_state = {}
    for e in events:
        events_by_state.setdefault(e["state"], []).append(e)
    analysis_by_state = {}
    for row in analysis:
        bucket = analysis_by_state.setdefault(row["state"], {"pros": [], "cons": []})
        bucket["pros" if row["kind"] == "pro" else "cons"].append(row["text"])
    overview_by_state = {o["state"]: o for o in overviews}
    pillars_by_state = {}
    for p in pillars:
        pillars_by_state.setdefault(p["state"], []).append(p["name"])
    changelog_by_state = {}
    for c in changelog:
        changelog_by_state.setdefault(c["state"], []).append(c)

    # "Current" award = the latest fiscal year on record for that state, not
    # the sum of every year ever added. This matters once FY27+ rows exist:
    # ranking, dashboard totals, and subawards figures should all reflect the
    # most recent year, with older years still available in `awards` for a
    # future multi-year view — never silently blended together.
    def current_award(state):
        state_awards = awards_by_state.get(state, [])
        return max(state_awards, key=lambda a: a["fiscal_year"], default=None)

    ranked = sorted(
        sources,
        key=lambda s: (current_award(s["state"]) or {}).get("amount", 0),
        reverse=True,
    )
    rank_by_state = {s["state"]: i + 1 for i, s in enumerate(ranked)}

    result = []
    for s in sources:
        state_awards = sorted(awards_by_state.get(s["state"], []), key=lambda a: a["fiscal_year"], reverse=True)
        state_events = sorted(events_by_state.get(s["state"], []), key=lambda e: e["event_date"])
        confirmed_events = [e for e in state_events if e["confidence"] == "confirmed"]
        latest_event = (confirmed_events or state_events)[-1] if state_events else None
        latest_award = current_award(s["state"])
        result.append(
            {
                **s,
                "awards": state_awards,
                "current_award": latest_award,
                "status_events": state_events,
                "current_status": latest_event["status"] if latest_event else None,
                "total_awarded": (latest_award or {}).get("amount", 0),
                "rank": rank_by_state[s["state"]],
                "analysis": analysis_by_state.get(s["state"], {"pros": [], "cons": []}),
                "overview": overview_by_state.get(s["state"]),
                "pillars": pillars_by_state.get(s["state"], []),
                "changelog": changelog_by_state.get(s["state"], []),
            }
        )
    return jsonify(
        {
            "states": result,
            "status_taxonomy": STATUS_TAXONOMY,
            "analysis_disclaimer": ANALYSIS_DISCLAIMER,
        }
    )


@app.route("/api/awards")
def api_awards():
    conn = get_connection()
    awards = rows_to_dicts(query(conn, "SELECT * FROM awards ORDER BY amount DESC"))
    conn.close()
    return jsonify(awards)


@app.route("/api/status_events")
def api_status_events():
    conn = get_connection()
    events = rows_to_dicts(query(conn, "SELECT * FROM status_events ORDER BY event_date DESC"))
    conn.close()
    return jsonify(events)


@app.route("/api/status_events", methods=["POST"])
def add_status_event():
    payload = request.get_json(force=True)
    required = {"state", "status", "source_url", "event_date", "notes"}
    missing = required - payload.keys()
    if missing:
        return jsonify({"error": f"missing fields: {sorted(missing)}"}), 400
    payload.setdefault("confidence", "confirmed")

    conn = get_connection()
    execute(
        conn,
        """INSERT INTO status_events (state, status, source_url, event_date, notes, confidence)
           VALUES (%(state)s, %(status)s, %(source_url)s, %(event_date)s, %(notes)s, %(confidence)s)""",
        payload,
    )
    conn.commit()
    conn.close()
    return jsonify({"ok": True}), 201


@app.route("/api/deadlines")
def api_deadlines():
    conn = get_connection()
    deadlines = rows_to_dicts(query(conn, "SELECT * FROM deadlines ORDER BY start_date"))
    conn.close()
    return jsonify(deadlines)


@app.route("/api/deadlines", methods=["POST"])
def add_deadline():
    payload = request.get_json(force=True)
    required = {"state", "title", "start_date", "source_url"}
    missing = required - payload.keys()
    if missing:
        return jsonify({"error": f"missing fields: {sorted(missing)}"}), 400
    payload.setdefault("end_date", None)
    payload.setdefault("notes", None)
    payload.setdefault("confidence", "confirmed")

    conn = get_connection()
    execute(
        conn,
        """INSERT INTO deadlines (state, title, start_date, end_date, source_url, notes, confidence)
           VALUES (%(state)s, %(title)s, %(start_date)s, %(end_date)s, %(source_url)s, %(notes)s, %(confidence)s)""",
        payload,
    )
    conn.commit()
    conn.close()
    return jsonify({"ok": True}), 201


@app.route("/api/commentary")
def api_commentary():
    conn = get_connection()
    rows = rows_to_dicts(query(conn, "SELECT * FROM commentary ORDER BY published_date DESC"))
    conn.close()
    return jsonify(rows)


@app.route("/api/federal_milestones")
def api_federal_milestones():
    conn = get_connection()
    rows = rows_to_dicts(query(conn, "SELECT * FROM federal_milestones ORDER BY start_date"))
    conn.close()
    return jsonify(rows)


@app.route("/api/federal_milestones", methods=["POST"])
def add_federal_milestone():
    payload = request.get_json(force=True)
    required = {"title", "category", "start_date", "source_url"}
    missing = required - payload.keys()
    if missing:
        return jsonify({"error": f"missing fields: {sorted(missing)}"}), 400
    payload.setdefault("end_date", None)
    payload.setdefault("notes", None)
    payload.setdefault("confidence", "confirmed")

    conn = get_connection()
    execute(
        conn,
        """INSERT INTO federal_milestones (title, category, start_date, end_date, source_url, notes, confidence)
           VALUES (%(title)s, %(category)s, %(start_date)s, %(end_date)s, %(source_url)s, %(notes)s, %(confidence)s)""",
        payload,
    )
    conn.commit()
    conn.close()
    return jsonify({"ok": True}), 201


if __name__ == "__main__":
    app.run(debug=True, port=5050)
