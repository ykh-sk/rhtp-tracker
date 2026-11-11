"""Loads AHRQ's Compendium of U.S. Health Systems, 2023 (system file) for the Health Systems map.

Source: https://www.ahrq.gov/chsp/data-resources/compendium-2023.html — a free federal dataset of 639
U.S. health systems (at least one hospital and one physician group under common ownership or joint
management). Downloaded file: app/data/ahrq/chsp-compendium-2023-rev.csv.

What is and isn't used, and why:
  * Counts and money (hospitals, beds, discharges, physicians, net revenue) are used as published.
  * The flags whose names say what they mean (system includes a major / very major teaching hospital,
    a high-disproportionate-share hospital, a high uncompensated-care burden; offers an insurance
    product) are used as booleans.
  * sys_ownership is decoded as 1 = nonprofit, 2 = nonprofit (church-affiliated), 3 = government,
    5 = investor-owned. That is INFERRED from systems whose ownership is well known (HCA/Tenet/CHS/
    UHS = 5; Cook County/Parkland/Denver Health/Grady = 3; Ascension/Providence/CommonSpirit = 2;
    Kaiser/Mayo/Sutter/Cleveland Clinic = 1) because AHRQ's technical documentation could not be
    read here — confirm against it before relying on a single system's label.
  * sys_multistate, sys_teachint and deg_children are NOT used: their code meanings could not be
    confirmed.
  * The hospital-to-system linkage file is NOT loaded (it was not provided), so individual CMS
    hospitals are not yet tied to AHRQ systems.

Headquarters coordinates: AHRQ gives only a home-office city and state. They are placed at the mean
position of the CMS hospitals in that city (precision 'city'), or from the small manual table below
for the few cities with no Medicare hospital of their own (precision 'city-manual').
"""

import csv
from collections import defaultdict
from pathlib import Path

AHRQ_CSV = Path(__file__).resolve().parent / "data" / "ahrq" / "chsp-compendium-2023-rev.csv"
AHRQ_DATA_YEAR = 2023
AHRQ_SOURCE_URL = "https://www.ahrq.gov/chsp/data-resources/compendium-2023.html"

OWNERSHIP_LABELS = {1: "nonprofit", 2: "nonprofit-church", 3: "government", 5: "investor-owned"}

# City-center coordinates (lat, lon) for AHRQ home-office cities with no CMS hospital of their own.
MANUAL_CITY_COORDS = {
    ("FL", "ALTAMONTE SPRINGS"): (28.6611, -81.3656), ("MD", "GAITHERSBURG"): (39.1434, -77.2014),
    ("TN", "BRENTWOOD"): (36.0331, -86.7828), ("CA", "EL SEGUNDO"): (33.9192, -118.4165),
    ("CA", "WEST HOLLYWOOD"): (34.0900, -118.3617), ("MA", "TEWKSBURY"): (42.6100, -71.2342),
    ("ME", "BREWER"): (44.7961, -68.7611), ("MA", "CONCORD"): (42.4604, -71.3489),
    ("NY", "GARDEN CITY"): (40.7268, -73.6343), ("FL", "ROCKLEDGE"): (28.3350, -80.7253),
    ("PA", "HUNTINGDON VALLEY"): (40.1137, -75.0693), ("NJ", "MULLICA HILL"): (39.7385, -75.2246),
    ("ID", "COEUR D ALENE"): (47.6777, -116.7805), ("MO", "PLEASANT VALLEY"): (39.2250, -94.4730),
    ("PA", "DU BOIS"): (41.1192, -78.7603), ("CA", "ONTARIO"): (34.0633, -117.6509),
    ("MS", "GAUTIER"): (30.3855, -88.6117), ("MA", "NEW BEDFORD"): (41.6362, -70.9342),
    ("IA", "WEST DES MOINES"): (41.5772, -93.7113), ("OH", "SHAKER HEIGHTS"): (41.4739, -81.5371),
    ("NJ", "RIDGEWOOD"): (40.9793, -74.1165), ("NJ", "EGG HARBOR TOWNSHIP"): (39.3768, -74.5857),
    ("NJ", "WEST ORANGE"): (40.7987, -74.2391),
}


def _int(v):
    v = (v or "").strip()
    if not v:
        return None
    try:
        return int(float(v))
    except ValueError:
        return None


def _flag(v):
    v = (v or "").strip()
    return None if v == "" else v == "1"


def load_ahrq_systems(cms_hospitals):
    """cms_hospitals: the rows of app/data/cms_hospitals.json (used only to place home-office cities)."""
    by_city = defaultdict(list)
    by_state = defaultdict(list)
    for h in cms_hospitals:
        if h.get("lat") is None:
            continue
        by_city[(h["state"], h["city"].upper().strip())].append((h["lat"], h["lon"]))
        by_state[h["state"]].append((h["lat"], h["lon"]))

    def mean(pts):
        return sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)

    out = []
    # The file is Windows-1252 (en-dashes in a few names), not UTF-8.
    with open(AHRQ_CSV, encoding="cp1252", newline="") as f:
        for r in csv.DictReader(f):
            st, city = r["health_sys_state"].strip(), r["health_sys_city"].strip()
            key = (st, city.upper())
            if key in MANUAL_CITY_COORDS:
                lat, lon = MANUAL_CITY_COORDS[key]; precision = "city-manual"
            elif key in by_city:
                lat, lon = mean(by_city[key]); precision = "city"
            elif st in by_state:
                lat, lon = mean(by_state[st]); precision = "state"
            else:
                continue
            own = _int(r["sys_ownership"])
            out.append({
                "sys_id": r["health_sys_id"], "name": r["health_sys_name"].strip(), "city": city, "state": st,
                "lat": round(lat, 4), "lon": round(lon, 4), "geo_precision": precision,
                "hospitals": _int(r["hosp_cnt"]), "acute_hospitals": _int(r["acutehosp_cnt"]),
                "beds": _int(r["sys_beds"]), "discharges": _int(r["sys_dsch"]),
                "physician_groups": _int(r["grp_cnt"]), "physicians": _int(r["total_mds"]),
                "primary_care_physicians": _int(r["prim_care_mds"]), "nurse_practitioners": _int(r["total_nps"]),
                "physician_assistants": _int(r["total_pas"]), "nursing_homes": _int(r["nh_cnt"]),
                "ownership_code": own, "ownership": OWNERSHIP_LABELS.get(own),
                "net_revenue": _int(r["hos_net_revenue"]), "total_revenue": _int(r["hos_total_revenue"]),
                "major_teaching": _flag(r["sys_incl_majteachhosp"]), "very_major_teaching": _flag(r["sys_incl_vmajteachhosp"]),
                "high_dsh": _flag(r["sys_incl_highdpphosp"]), "high_uc_burden": _flag(r["sys_highucburden"]),
                "offers_insurance": _flag(r["sys_anyins_product"]),
                "aha_sysid": (r["aha_sysid"] or "").strip() or None,
            })
    return out
