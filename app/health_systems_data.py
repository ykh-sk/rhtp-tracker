"""Curated dataset for the Health Systems map: notable multi-state and regional
hospital/health-system OPERATORS (the businesses that own and run hospitals),
sized small/mid/large/major by hospital count. This is a hand-picked, sourced
starting set — like seed_data.py, not a bulk import — focused on operators
active in the states this tracker follows, especially rural-relevant regional
systems. Extend it the same way: add a row with a real source_url.

Tiers are cut by hospital_count: major >=90, large 40-89, mid 15-39, small <15.
`confidence` follows the same convention as status_events/deadlines: 'confirmed'
when a source gave the figure directly for this org, 'approximate' when the
count is dated, mid-merger, or aggregated across a broader ranking page.
"""

HEALTH_SYSTEMS = [
    # --- major (90+ hospitals) ---
    {
        "name": "HCA Healthcare", "tier": "major", "ownership_type": "for-profit",
        "hq_city": "Nashville", "hq_state": "Tennessee", "hq_lat": 36.1627, "hq_lon": -86.7816,
        "hospital_count": 190, "notes": "Largest for-profit hospital operator in the US.",
        "source_url": "https://www.beckershospitalreview.com/rankings-and-ratings/100-of-the-largest-hospitals-and-health-systems-in-the-us-2026/",
        "verified_at": "2026-09-14", "confidence": "confirmed",
    },
    {
        "name": "CommonSpirit Health", "tier": "major", "ownership_type": "nonprofit",
        "hq_city": "Chicago", "hq_state": "Illinois", "hq_lat": 41.8781, "hq_lon": -87.6298,
        "hospital_count": 158, "notes": "Nonprofit Catholic system formed by the 2019 merger of Catholic Health Initiatives and Dignity Health.",
        "source_url": "https://www.beckershospitalreview.com/rankings-and-ratings/100-of-the-largest-hospitals-and-health-systems-in-the-us-2026/",
        "verified_at": "2026-09-14", "confidence": "confirmed",
    },
    {
        "name": "LifePoint Health", "tier": "major", "ownership_type": "for-profit",
        "hq_city": "Brentwood", "hq_state": "Tennessee", "hq_lat": 36.0331, "hq_lon": -86.7828,
        "hospital_count": 135, "notes": "For-profit; owns a majority of its hospitals through joint ventures with nonprofit partners.",
        "source_url": "https://www.beckershospitalreview.com/rankings-and-ratings/100-of-the-largest-hospitals-and-health-systems-in-the-us-2026/",
        "verified_at": "2026-09-14", "confidence": "confirmed",
    },
    {
        "name": "Ascension", "tier": "major", "ownership_type": "nonprofit",
        "hq_city": "St. Louis", "hq_state": "Missouri", "hq_lat": 38.6270, "hq_lon": -90.1994,
        "hospital_count": 119, "notes": "One of the largest nonprofit Catholic health systems in the US. Its own find-care.ascension.org location search caps out broken nationwide/all-distance queries at ~14 results, so the hospital_roster entry for this operator (81 hospitals) was built with per-city, radius-limited searches across its actual 9-state footprint (FL, IL, IN, KS, MD, OK, TN, TX, WI) — Michigan, sometimes cited in older references, was fully divested. Coverage searched 1-3 major metros per state at up to 100mi, so some smaller or more rural facilities further out (especially in IL, IN, and TX) may be missing.",
        "source_url": "https://about.ascension.org/news/2026/03/ascension-named-fifth-largest-health-system-in-the-nation-reflecting-strategic-mission-aligned-growth",
        "verified_at": "2026-09-14", "confidence": "confirmed",
    },
    {
        "name": "ScionHealth", "tier": "large", "ownership_type": "for-profit",
        "hq_city": "Louisville", "hq_state": "Kentucky", "hq_lat": 38.2527, "hq_lon": -85.7585,
        "hospital_count": 68, "notes": "Divested 8 community hospitals to LifePoint Health in a deal that closed March 2026; count reflects their own site's current total (62 specialty + 6 community hospitals).",
        "source_url": "https://www.scionhealth.com/find-a-location",
        "verified_at": "2026-09-17", "confidence": "confirmed",
    },
    {
        "name": "Trinity Health", "tier": "major", "ownership_type": "nonprofit",
        "hq_city": "Livonia", "hq_state": "Michigan", "hq_lat": 42.3684, "hq_lon": -83.3527,
        "hospital_count": 92, "notes": "Among the nation's three largest nonprofit Catholic health systems. Its corporate site's own location API is broken (returns zero results); the hospital_roster entry for this operator (58 hospitals) was built region-by-region from its ~10 separate regional-brand sites instead, so some states in its 23-state community footprint (e.g. AL, NC, MN, SD, CA, NJ) have no confirmed hospital and may be PACE/hospice/senior-living-only presence there.",
        "source_url": "https://www.beckershospitalreview.com/rankings-and-ratings/100-of-the-largest-hospitals-and-health-systems-in-the-us-2026/",
        "verified_at": "2026-09-14", "confidence": "confirmed",
    },
    # --- large (40-89 hospitals) ---
    {
        "name": "Advocate Health", "tier": "large", "ownership_type": "nonprofit",
        "hq_city": "Charlotte", "hq_state": "North Carolina", "hq_lat": 35.2271, "hq_lon": -80.8431,
        "hospital_count": 69, "notes": "Formed by the 2022 merger of Advocate Aurora Health and Atrium Health. Its Carolinas/Georgia/Alabama Atrium Health brand blocks automated access to its own location directory, so the hospital_roster entry for this operator (55 hospitals) is complete for Illinois and Wisconsin but likely missing some smaller Atrium-branded facilities.",
        "source_url": "https://en.wikipedia.org/wiki/Advocate_Health",
        "verified_at": "2026-09-14", "confidence": "confirmed",
    },
    {
        "name": "Christus Health", "tier": "large", "ownership_type": "nonprofit",
        "hq_city": "Irving", "hq_state": "Texas", "hq_lat": 32.8140, "hq_lon": -96.9489,
        "hospital_count": 66, "notes": "Includes long-term care facilities and international hospitals (Mexico, Chile, Colombia); their own site's US-only hospital directory (TX/LA/NM) lists 32.",
        "source_url": "https://www.beckershospitalreview.com/rankings-and-ratings/100-of-the-largest-hospitals-and-health-systems-in-the-us-2026/",
        "verified_at": "2026-09-14", "confidence": "confirmed",
    },
    {
        "name": "Community Health Systems", "tier": "large", "ownership_type": "for-profit",
        "hq_city": "Franklin", "hq_state": "Tennessee", "hq_lat": 35.9251, "hq_lon": -86.8689,
        "hospital_count": 65, "notes": None,
        "source_url": "https://www.beckershospitalreview.com/rankings-and-ratings/100-of-the-largest-hospitals-and-health-systems-in-the-us-2026/",
        "verified_at": "2026-09-14", "confidence": "confirmed",
    },
    {
        "name": "Sanford Health", "tier": "large", "ownership_type": "nonprofit",
        "hq_city": "Sioux Falls", "hq_state": "South Dakota", "hq_lat": 43.5460, "hq_lon": -96.7313,
        "hospital_count": 45, "notes": "Largest rural-focused nonprofit health system in the US, including former Marshfield Clinic Health System (WI/MI) hospitals post-merger (Jan 2025); count is their own site's current hospital location listing, below the ~59 figure reported at merger time.",
        "source_url": "https://www.sanfordhealth.org/locations",
        "verified_at": "2026-09-17", "confidence": "confirmed",
    },
    {
        "name": "AdventHealth", "tier": "large", "ownership_type": "nonprofit",
        "hq_city": "Altamonte Springs", "hq_state": "Florida", "hq_lat": 28.6611, "hq_lon": -81.3656,
        "hospital_count": 57, "notes": "Seventh-day Adventist-affiliated nonprofit system.",
        "source_url": "https://en.wikipedia.org/wiki/AdventHealth",
        "verified_at": "2026-09-14", "confidence": "approximate",
    },
    {
        "name": "Baylor Scott & White Health", "tier": "large", "ownership_type": "nonprofit",
        "hq_city": "Dallas", "hq_state": "Texas", "hq_lat": 32.7767, "hq_lon": -96.7970,
        "hospital_count": 53, "notes": None,
        "source_url": "https://en.wikipedia.org/wiki/Baylor_Scott_%26_White_Health",
        "verified_at": "2026-09-14", "confidence": "approximate",
    },
    {
        "name": "Providence", "tier": "large", "ownership_type": "nonprofit",
        "hq_city": "Renton", "hq_state": "Washington", "hq_lat": 47.4829, "hq_lon": -122.2171,
        "hospital_count": 51, "notes": "Catholic-affiliated nonprofit system spanning the West Coast and Alaska/Montana/Texas.",
        "source_url": "https://www.beckershospitalreview.com/rankings-and-ratings/100-of-the-largest-hospitals-and-health-systems-in-the-us-2026/",
        "verified_at": "2026-09-14", "confidence": "approximate",
    },
    {
        "name": "Tenet Healthcare", "tier": "large", "ownership_type": "for-profit",
        "hq_city": "Dallas", "hq_state": "Texas", "hq_lat": 32.7767, "hq_lon": -96.7970,
        "hospital_count": 50, "notes": "Acute-care and specialty hospitals, as of Dec 31, 2025.",
        "source_url": "https://en.wikipedia.org/wiki/Tenet_Healthcare",
        "verified_at": "2026-09-14", "confidence": "confirmed",
    },
    {
        "name": "Bon Secours Mercy Health", "tier": "large", "ownership_type": "nonprofit",
        "hq_city": "Cincinnati", "hq_state": "Ohio", "hq_lat": 39.1031, "hq_lon": -84.5120,
        "hospital_count": 47, "notes": "Catholic-affiliated nonprofit system.",
        "source_url": "https://www.beckershospitalreview.com/rankings-and-ratings/100-of-the-largest-hospitals-and-health-systems-in-the-us-2026/",
        "verified_at": "2026-09-14", "confidence": "approximate",
    },
    {
        "name": "UPMC", "tier": "large", "ownership_type": "nonprofit",
        "hq_city": "Pittsburgh", "hq_state": "Pennsylvania", "hq_lat": 40.4406, "hq_lon": -79.9959,
        "hospital_count": 40, "notes": "Academic-affiliated integrated system built around the University of Pittsburgh.",
        "source_url": "https://www.beckershospitalreview.com/rankings-and-ratings/100-of-the-largest-hospitals-and-health-systems-in-the-us-2026/",
        "verified_at": "2026-09-14", "confidence": "approximate",
    },
    {
        "name": "Kaiser Permanente", "tier": "large", "ownership_type": "nonprofit",
        "hq_city": "Oakland", "hq_state": "California", "hq_lat": 37.8044, "hq_lon": -122.2712,
        "hospital_count": 40, "notes": "Integrated payer-provider model, concentrated in a handful of states; relies on contracted/affiliate hospitals (not owned) in Colorado, Georgia, and the Mid-Atlantic. The hospital_roster entry for this operator (40 hospitals, region-by-region via its own location filters) matches this count almost exactly.",
        "source_url": "https://healthy.kaiserpermanente.org",
        "verified_at": "2026-09-17", "confidence": "confirmed",
    },
    # --- mid (15-39 hospitals) ---
    {
        "name": "Avera Health", "tier": "mid", "ownership_type": "nonprofit",
        "hq_city": "Sioux Falls", "hq_state": "South Dakota", "hq_lat": 43.5460, "hq_lon": -96.7313,
        "hospital_count": 38, "notes": "Faith-based regional system; most of its hospitals serve rural communities across SD, MN, IA, NE, ND.",
        "source_url": "https://en.wikipedia.org/wiki/Avera_Health",
        "verified_at": "2026-09-14", "confidence": "confirmed",
    },
    {
        "name": "Intermountain Health", "tier": "mid", "ownership_type": "nonprofit",
        "hq_city": "Salt Lake City", "hq_state": "Utah", "hq_lat": 40.7608, "hq_lon": -111.8910,
        "hospital_count": 34, "notes": "The hospital_roster entry for this operator (29 hospitals, via its location-search API) found no owned hospitals in NV, KS, or WY despite dedicated searches, which may mean the 34-hospital figure counts a broader clinic/affiliate footprint rather than owned hospitals in all 7 states — treated as unconfirmed absence, not verified zero, for those 3 states.",
        "source_url": "https://www.beckershospitalreview.com/rankings-and-ratings/100-of-the-largest-hospitals-and-health-systems-in-the-us-2026/",
        "verified_at": "2026-09-17", "confidence": "approximate",
    },
    {
        "name": "Banner Health", "tier": "mid", "ownership_type": "nonprofit",
        "hq_city": "Phoenix", "hq_state": "Arizona", "hq_lat": 33.4484, "hq_lon": -112.0740,
        "hospital_count": 33, "notes": "Operates across 6 states.",
        "source_url": "https://en.wikipedia.org/wiki/Banner_Health",
        "verified_at": "2026-09-14", "confidence": "confirmed",
    },
    {
        "name": "Universal Health Services", "tier": "mid", "ownership_type": "for-profit",
        "hq_city": "King of Prussia", "hq_state": "Pennsylvania", "hq_lat": 40.0893, "hq_lon": -75.3927,
        "hospital_count": 30, "notes": "Acute-care hospital count; also the largest US operator of behavioral-health facilities (380+ separately).",
        "source_url": "https://en.wikipedia.org/wiki/Universal_Health_Services",
        "verified_at": "2026-09-14", "confidence": "confirmed",
    },
    {
        "name": "Cleveland Clinic", "tier": "mid", "ownership_type": "nonprofit",
        "hq_city": "Cleveland", "hq_state": "Ohio", "hq_lat": 41.4993, "hq_lon": -81.6944,
        "hospital_count": 23, "notes": "Academic medical system; count includes hospitals outside the US.",
        "source_url": "https://en.wikipedia.org/wiki/Cleveland_Clinic",
        "verified_at": "2026-09-14", "confidence": "approximate",
    },
    {
        "name": "Ballad Health", "tier": "mid", "ownership_type": "nonprofit",
        "hq_city": "Johnson City", "hq_state": "Tennessee", "hq_lat": 36.3134, "hq_lon": -82.3535,
        "hospital_count": 20, "notes": "Serves 29 mostly-rural Appalachian counties across TN, VA, NC and KY — formed via a state-approved COPA merger.",
        "source_url": "https://en.wikipedia.org/wiki/Ballad_Health",
        "verified_at": "2026-09-14", "confidence": "confirmed",
    },
    {
        "name": "Novant Health", "tier": "mid", "ownership_type": "nonprofit",
        "hq_city": "Winston-Salem", "hq_state": "North Carolina", "hq_lat": 36.0999, "hq_lon": -80.2442,
        "hospital_count": 19, "notes": "Figure reported as of 2023; may undercount recent additions.",
        "source_url": "https://en.wikipedia.org/wiki/Novant_Health",
        "verified_at": "2026-09-14", "confidence": "approximate",
    },
    # --- small (<15 hospitals) ---
    {
        "name": "Essentia Health", "tier": "small", "ownership_type": "nonprofit",
        "hq_city": "Duluth", "hq_state": "Minnesota", "hq_lat": 46.7867, "hq_lon": -92.1005,
        "hospital_count": 14, "notes": "Serves rural and underserved communities across MN, WI and ND.",
        "source_url": "https://en.wikipedia.org/wiki/Essentia_Health",
        "verified_at": "2026-09-14", "confidence": "confirmed",
    },
    {
        "name": "Baptist Health (Kentucky)", "tier": "small", "ownership_type": "nonprofit",
        "hq_city": "Louisville", "hq_state": "Kentucky", "hq_lat": 38.2527, "hq_lon": -85.7585,
        "hospital_count": 10, "notes": "Founded 1924; not affiliated with the similarly-named Baptist Health systems in Florida or Arkansas.",
        "source_url": "https://en.wikipedia.org/wiki/Baptist_Health_(Kentucky_and_Southern_Indiana)",
        "verified_at": "2026-09-14", "confidence": "confirmed",
    },
]
