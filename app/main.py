import functools
import hashlib
import hmac
import os
import time
from pathlib import Path

from flask import Flask, jsonify, request
from itsdangerous import BadSignature, URLSafeTimedSerializer

from ahrq_crosswalk_data import AHRQ_MERGED
from ahrq_data import AHRQ_DATA_YEAR, AHRQ_SOURCE_URL
from bd_profiles_data import slugify
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


@app.route("/atlas")
def atlas():
    return app.send_static_file("atlas.html")


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
        pillars_by_state.setdefault(p["state"], []).append({"name": p["name"], "description": p["description"]})
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


@app.route("/api/health_systems")
def api_health_systems():
    conn = get_connection()
    rows = rows_to_dicts(query(conn, "SELECT * FROM health_systems ORDER BY hospital_count DESC"))
    conn.close()
    return jsonify(rows)


STATE_NAMES = {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'DC': 'District of Columbia', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'}


@app.route("/api/atlas_state/<abbr>")
def api_atlas_state(abbr):
    """Everything the Radar's per-state mini map needs: the systems headquartered in the state (our
    sourced operators, profile-only systems, and AHRQ systems matching neither) plus its CMS hospitals."""
    abbr = abbr.upper()
    name = STATE_NAMES.get(abbr)
    if not name:
        return jsonify({"error": "Unknown state."}), 404
    conn = get_connection()
    systems = []
    for r in query(conn, """SELECT h.name, h.hq_city AS city, h.hq_lat AS lat, h.hq_lon AS lon, h.hospital_count AS hospitals,
                                   a.beds, h.ownership_type AS ownership
                            FROM health_systems h
                            LEFT JOIN ahrq_crosswalk c ON c.bd_key = regexp_replace(lower(h.name), '[^a-z0-9]+', '-', 'g')
                            LEFT JOIN ahrq_systems a ON a.sys_id = c.sys_id
                            WHERE h.hq_state = %(s)s""", {"s": name}):
        systems.append({**dict(r), "kind": "operator"})
    for r in query(conn, """SELECT b.name, split_part(b.hq_place, ', ', 1) AS city, b.hq_lat AS lat, b.hq_lon AS lon,
                                   a.hospitals, a.beds, a.ownership
                            FROM bd_profiles b
                            LEFT JOIN ahrq_crosswalk c ON c.bd_key = b.bd_key
                            LEFT JOIN ahrq_systems a ON a.sys_id = c.sys_id
                            WHERE b.operator_name IS NULL AND b.hq_place LIKE %(like)s""", {"like": "%, " + abbr}):
        systems.append({**dict(r), "kind": "profile"})
    for r in query(conn, """SELECT name, city, lat, lon, hospitals, beds, ownership FROM ahrq_systems
                            WHERE state = %(a)s AND sys_id NOT IN (SELECT sys_id FROM ahrq_crosswalk)
                              AND sys_id <> ALL(%(m)s)""", {"a": abbr, "m": list(AHRQ_MERGED)}):
        systems.append({**dict(r), "kind": "ahrq"})
    hospitals = rows_to_dicts(query(
        conn, "SELECT id, name, city, type, ownership, lat, lon FROM cms_hospitals WHERE state = %(a)s ORDER BY city, name", {"a": abbr}))
    conn.close()
    return jsonify({"state": name, "abbr": abbr, "systems": systems, "hospitals": hospitals})


@app.route("/api/ahrq_systems")
def api_ahrq_systems():
    conn = get_connection()
    rows = rows_to_dicts(query(
        conn,
        """SELECT a.*, c.bd_key, c.match_type
           FROM ahrq_systems a LEFT JOIN ahrq_crosswalk c ON c.sys_id = a.sys_id
           ORDER BY a.hospitals DESC NULLS LAST, a.name""",
    ))
    conn.close()
    for r in rows:
        merged = AHRQ_MERGED.get(r["sys_id"])
        r["merged_into"] = slugify(merged[0]) if merged else None
        r["merged_note"] = merged[1] if merged else None
    return jsonify({
        "meta": {"data_year": AHRQ_DATA_YEAR, "source_url": AHRQ_SOURCE_URL, "row_count": len(rows)},
        "systems": rows,
    })


@app.route("/api/hospital_roster")
def api_hospital_roster():
    conn = get_connection()
    rows = rows_to_dicts(query(conn, "SELECT * FROM hospital_roster ORDER BY company, state, city"))
    conn.close()
    return jsonify(rows)


@app.route("/api/cms_hospitals")
def api_cms_hospitals():
    conn = get_connection()
    hospitals = rows_to_dicts(query(conn, "SELECT * FROM cms_hospitals ORDER BY state, city"))
    meta = query(conn, "SELECT dataset_modified, geocoded_at, row_count, source_url FROM cms_hospitals_meta WHERE id = 1")
    conn.close()
    return jsonify({"meta": rows_to_dicts(meta)[0] if meta else None, "hospitals": hospitals})


@app.route("/api/bd_profiles")
def api_bd_profiles():
    conn = get_connection()
    rows = rows_to_dicts(query(conn, "SELECT * FROM bd_profiles ORDER BY name"))
    conn.close()
    return jsonify(rows)


# ---- BD outreach tracking: password-gated ----
# Everything under /api/bd/ except the public read of bd_profiles above. The password comes
# from the BD_PASSWORD environment variable (never stored in the repo); with it unset every
# gated route fails closed with 503. A correct login sets a signed, HttpOnly, SameSite=Strict
# cookie. The signing key is derived from the password, so changing BD_PASSWORD logs everyone out.

BD_COOKIE = "bd_session"
BD_SESSION_SECONDS = 7 * 24 * 3600
BD_STATUSES = ("not_contacted", "researching", "contacted", "in_discussion", "piloting", "declined")
BD_LOGIN_MAX_FAILURES = 8        # per IP ...
BD_LOGIN_WINDOW_MINUTES = 15     # ... within this window


def _bd_password():
    return os.environ.get("BD_PASSWORD") or ""


def _bd_username():
    # A fixed, non-secret login name (default "bd") — it only gives the form a second field; the
    # password is what protects the data.
    return os.environ.get("BD_USERNAME") or "bd"


def _bd_serializer():
    key = (_bd_username() + "\0" + _bd_password()).encode()
    secret = hmac.new(key, b"rhtp-bd-session-v1", hashlib.sha256).hexdigest()
    return URLSafeTimedSerializer(secret, salt="bd-session")


def _bd_json(payload, status=200):
    resp = jsonify(payload)
    resp.status_code = status
    resp.headers["Cache-Control"] = "no-store"
    return resp


def _is_https():
    forwarded = request.headers.get("X-Forwarded-Proto", "").split(",")[0].strip()
    return request.is_secure or forwarded == "https"


def _client_ip():
    forwarded = request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
    return forwarded or request.remote_addr or "unknown"


def bd_is_authed():
    token = request.cookies.get(BD_COOKIE)
    if not _bd_password() or not token:
        return False
    try:
        return _bd_serializer().loads(token, max_age=BD_SESSION_SECONDS) == {"bd": 1}
    except BadSignature:  # also covers an expired signature
        return False


def bd_required(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if not _bd_password():
            return _bd_json({"error": "BD tracking is not configured (BD_PASSWORD is not set on the server)."}, 503)
        if not bd_is_authed():
            return _bd_json({"error": "Password required."}, 401)
        return fn(*args, **kwargs)
    return wrapper


@app.route("/api/bd/session")
def bd_session():
    return _bd_json({"configured": bool(_bd_password()), "authed": bd_is_authed()})


@app.route("/api/bd/login", methods=["POST"])
def bd_login():
    password = _bd_password()
    if not password:
        return _bd_json({"error": "BD tracking is not configured (BD_PASSWORD is not set on the server)."}, 503)

    ip = _client_ip()
    conn = get_connection()
    failures = query(
        conn,
        "SELECT count(*) AS n FROM bd_login_failures WHERE ip = %(ip)s AND at > now() - make_interval(mins => %(mins)s)",
        {"ip": ip, "mins": BD_LOGIN_WINDOW_MINUTES},
    )[0]["n"]
    if failures >= BD_LOGIN_MAX_FAILURES:
        conn.close()
        return _bd_json({"error": f"Too many failed attempts. Try again in {BD_LOGIN_WINDOW_MINUTES} minutes."}, 429)

    payload = request.get_json(silent=True) or {}
    supplied = payload.get("password")
    supplied_user = payload.get("username")
    # Both comparisons always run so a wrong username and a wrong password look the same.
    user_ok = isinstance(supplied_user, str) and hmac.compare_digest(supplied_user.encode(), _bd_username().encode())
    pass_ok = isinstance(supplied, str) and hmac.compare_digest(supplied.encode(), password.encode())
    if not (user_ok and pass_ok):
        execute(conn, "DELETE FROM bd_login_failures WHERE at < now() - interval '1 day'")
        execute(conn, "INSERT INTO bd_login_failures (ip) VALUES (%(ip)s)", {"ip": ip})
        conn.commit()
        conn.close()
        time.sleep(1)
        return _bd_json({"error": "Wrong ID or password."}, 401)

    execute(conn, "DELETE FROM bd_login_failures WHERE ip = %(ip)s", {"ip": ip})
    conn.commit()
    conn.close()
    resp = _bd_json({"ok": True})
    resp.set_cookie(
        BD_COOKIE, _bd_serializer().dumps({"bd": 1}),
        max_age=BD_SESSION_SECONDS, httponly=True, samesite="Strict", secure=_is_https(), path="/",
    )
    return resp


@app.route("/api/bd/logout", methods=["POST"])
def bd_logout():
    resp = _bd_json({"ok": True})
    resp.delete_cookie(BD_COOKIE, path="/", samesite="Strict", secure=_is_https(), httponly=True)
    return resp


@app.route("/api/bd/outreach")
@bd_required
def bd_outreach_list():
    conn = get_connection()
    rows = rows_to_dicts(query(conn, "SELECT bd_key, status, owner, notes, updated_at FROM bd_outreach"))
    conn.close()
    for r in rows:
        r["updated_at"] = r["updated_at"].isoformat()
    return _bd_json(rows)


@app.route("/api/bd/outreach/<key>", methods=["PUT"])
@bd_required
def bd_outreach_put(key):
    # Requiring a JSON body (which a cross-site form can't send without a CORS preflight) is the
    # CSRF guard alongside the SameSite=Strict cookie.
    if not request.is_json:
        return _bd_json({"error": "Send application/json."}, 415)
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return _bd_json({"error": "Body must be a JSON object."}, 400)

    fields = {}
    if "status" in payload:
        if payload["status"] not in BD_STATUSES:
            return _bd_json({"error": f"status must be one of {list(BD_STATUSES)}"}, 400)
        fields["status"] = payload["status"]
    for name, limit in (("owner", 120), ("notes", 5000)):
        if name in payload:
            if not isinstance(payload[name], str) or len(payload[name]) > limit:
                return _bd_json({"error": f"{name} must be text of at most {limit} characters."}, 400)
            fields[name] = payload[name]
    if not fields:
        return _bd_json({"error": "Nothing to update."}, 400)

    conn = get_connection()
    valid_keys = {slugify(r["name"]) for r in query(conn, "SELECT name FROM health_systems")}
    valid_keys |= {r["bd_key"] for r in query(conn, "SELECT bd_key FROM bd_profiles")}
    # AHRQ systems with no match in our own lists are their own trackable entries: key "ahrq-<id>".
    valid_keys |= {
        "ahrq-" + r["sys_id"].lower()
        for r in query(
            conn,
            "SELECT sys_id FROM ahrq_systems WHERE sys_id NOT IN (SELECT sys_id FROM ahrq_crosswalk) AND sys_id <> ALL(%(m)s)",
            {"m": list(AHRQ_MERGED)},
        )
    }
    if key not in valid_keys:
        conn.close()
        return _bd_json({"error": "Unknown system."}, 404)

    # Only the fields sent are written, so two people editing different fields of one row don't
    # overwrite each other.
    cols = list(fields)
    execute(
        conn,
        f"""INSERT INTO bd_outreach (bd_key, {', '.join(cols)}) VALUES (%(bd_key)s, {', '.join(f'%({c})s' for c in cols)})
            ON CONFLICT (bd_key) DO UPDATE SET {', '.join(f'{c} = EXCLUDED.{c}' for c in cols)}, updated_at = now()""",
        {"bd_key": key, **fields},
    )
    row = rows_to_dicts(query(conn, "SELECT bd_key, status, owner, notes, updated_at FROM bd_outreach WHERE bd_key = %(k)s", {"k": key}))[0]
    conn.commit()
    conn.close()
    row["updated_at"] = row["updated_at"].isoformat()
    return _bd_json(row)


@app.route("/api/bd/state_notes")
@bd_required
def bd_state_notes_list():
    conn = get_connection()
    rows = rows_to_dicts(query(conn, "SELECT abbr, note, updated_at FROM bd_state_notes ORDER BY abbr"))
    conn.close()
    for r in rows:
        r["updated_at"] = r["updated_at"].isoformat()
    return _bd_json(rows)


@app.route("/api/bd/state_notes/<abbr>", methods=["PUT"])
@bd_required
def bd_state_notes_put(abbr):
    abbr = abbr.upper()
    if abbr not in STATE_NAMES:
        return _bd_json({"error": "Unknown state."}, 404)
    if not request.is_json:
        return _bd_json({"error": "Send application/json."}, 415)
    payload = request.get_json(silent=True)
    note = payload.get("note") if isinstance(payload, dict) else None
    if not isinstance(note, str) or len(note) > 5000:
        return _bd_json({"error": "note must be text of at most 5000 characters."}, 400)
    conn = get_connection()
    execute(
        conn,
        """INSERT INTO bd_state_notes (abbr, note) VALUES (%(abbr)s, %(note)s)
           ON CONFLICT (abbr) DO UPDATE SET note = EXCLUDED.note, updated_at = now()""",
        {"abbr": abbr, "note": note},
    )
    row = rows_to_dicts(query(conn, "SELECT abbr, note, updated_at FROM bd_state_notes WHERE abbr = %(a)s", {"a": abbr}))[0]
    conn.commit()
    conn.close()
    row["updated_at"] = row["updated_at"].isoformat()
    return _bd_json(row)


if __name__ == "__main__":
    app.run(debug=True, port=5050)
