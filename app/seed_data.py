"""
Seed data transcribed from docs/rhtp-seed-data.md (verified 2026-09-02),
plus derived fields (subawards figures, deadlines, analysis) added afterward.
This is the source of truth for the initial database load — see seed.py.
"""

SOURCES = [
    {"state": "West Virginia", "official_url": "https://health.wv.gov/rural-health-transformation-program", "lead_agency": "WV Department of Health"},
    {"state": "Kentucky", "official_url": "https://ruralhealthplan.ky.gov/Pages/index.aspx", "lead_agency": "Dept for Public Health (\"A3 Team\")"},
    {"state": "Ohio", "official_url": "https://odh.ohio.gov/know-our-programs/rural-health-transformation-program/rural-health-transformation-program", "lead_agency": "Ohio Department of Health"},
    {"state": "Tennessee", "official_url": "https://www.tn.gov/health/rural.html", "lead_agency": "Tennessee Department of Health"},
    {"state": "Virginia", "official_url": "https://www.ruralhealthtransformationva.virginia.gov/", "lead_agency": "HHR / DMAS"},
    {"state": "North Carolina", "official_url": "https://www.ncdhhs.gov/divisions/office-rural-health/rural-health-transformation-program", "lead_agency": "NCDHHS Office of Rural Health"},
    {"state": "Pennsylvania", "official_url": "https://www.pa.gov/agencies/dhs/programs-services/healthcare/rural-health", "lead_agency": "PA Dept of Human Services"},
    {"state": "Georgia", "official_url": "https://greathealth.georgia.gov/faqs", "lead_agency": "Dept of Community Health"},
    {"state": "Alabama", "official_url": "https://adeca.alabama.gov/alruralhealth/", "lead_agency": "ADECA"},
    {"state": "Mississippi", "official_url": "https://mississippirhtp.com/", "lead_agency": "Governor's Office (RHTP Office)"},
]

# subawards_amount / subawards_label are populated only when a source states a
# concrete disbursed-to-date figure distinct from the total award. Left null
# otherwise per state — never estimated.
AWARDS = [
    {"state": "West Virginia", "fiscal_year": "FY26", "amount": 199000000, "status": "subawards announced", "source_url": "https://governor.wv.gov/article/governor-morrisey-announces-first-2856-million-rural-health-transformation-funding", "verified_at": "2026-09-02", "subawards_amount": 28560000, "subawards_label": "first tranche opened"},
    {"state": "Kentucky", "fiscal_year": "FY26", "amount": 212900000, "status": "RFA issued", "source_url": "https://www.kentuckytoday.com/news/kentuckys-rural-health-transformation-plan-secures-212-9m-in-federal-funding/article_2adc2281-3461-4430-995d-07f6a6973df4.html", "verified_at": "2026-09-02", "subawards_amount": None, "subawards_label": None},
    {"state": "Ohio", "fiscal_year": "FY26", "amount": 202000000, "status": "subawards announced", "source_url": "https://governor.ohio.gov/media/news-and-media/governor-dewine-announces-first-rural-health-transformation-program-award-to-ohio-university-for-10-million", "verified_at": "2026-09-02", "subawards_amount": 10000000, "subawards_label": "first award announced"},
    {"state": "Tennessee", "fiscal_year": "FY26", "amount": 206888882, "status": "RFA issued", "source_url": "https://www.tn.gov/health/news/2026/5/15/tennessee-to-release-1st-grant-funding-opportunity-of-rural-health-transformation-program.html", "verified_at": "2026-09-02", "subawards_amount": None, "subawards_label": None},
    {"state": "Virginia", "fiscal_year": "FY26", "amount": 189544888, "status": "admin structure named", "source_url": "https://dmas.virginia.gov/data-reporting/programs-services/rural-health-transformation/", "verified_at": "2026-09-02", "subawards_amount": None, "subawards_label": None},
    {"state": "North Carolina", "fiscal_year": "FY26", "amount": 213000000, "status": "subawards announced", "source_url": "https://www.ncdhhs.gov/divisions/office-rural-health/rural-health-transformation-program", "verified_at": "2026-09-02", "subawards_amount": None, "subawards_label": None},
    {"state": "Pennsylvania", "fiscal_year": "FY26", "amount": 193000000, "status": "subawards announced", "source_url": "https://www.pa.gov/agencies/dhs/programs-services/healthcare/rural-health/rhtp-funding-opportunities", "verified_at": "2026-09-02", "subawards_amount": 1800000, "subawards_label": "6 awards, FQHC track"},
    {"state": "Georgia", "fiscal_year": "FY26", "amount": 218862169, "status": "subawards announced", "source_url": "https://dch.georgia.gov/announcement/2026-07-16/georgia-issues-30-million-phase-2-great-health-awards-advance-rural", "verified_at": "2026-09-02", "subawards_amount": 43300000, "subawards_label": "committed across 2 phases"},
    {"state": "Alabama", "fiscal_year": "FY26", "amount": 203404327, "status": "subawards announced", "source_url": "https://governor.alabama.gov/newsroom/2026/08/governor-ivey-announces-first-grants-in-major-new-rural-healthcare-program-totaling-more-than-144-million/", "verified_at": "2026-09-02", "subawards_amount": 144000000, "subawards_label": "138 grants, 5 of 10 initiatives"},
    {"state": "Mississippi", "fiscal_year": "FY26", "amount": 205907220, "status": "RFA issued", "source_url": "https://mississippirhtp.com/", "verified_at": "2026-09-02", "subawards_amount": None, "subawards_label": None},
]

# `confidence` is 'confirmed' (default) or 'unverified'. Unverified entries are
# kept — not discarded — but rendered with a caution flag in the UI, per a
# secondary source or a direct-fetch failure on the official page. Corrections
# are appended as NEW dated rows rather than edited in place: nothing here is
# ever rewritten once published, so a state's history reads as a thread, not
# a value that silently changed underneath a prior reader.
STATUS_EVENTS = [
    {"state": "West Virginia", "status": "subawards announced", "source_url": "https://governor.wv.gov/article/governor-morrisey-announces-first-2856-million-rural-health-transformation-funding", "event_date": "2026-04-28", "notes": "First $28.56M tranche opened for MSCF, HealthTech Appalachia, Connected Care Grid. FLAG: WV Dept of Health page cites $199M award; a hospital-association source cited $233.5M — needs reconciliation, do not treat as resolved.", "confidence": "confirmed"},
    {"state": "West Virginia", "status": "subawards announced", "source_url": "https://governor.wv.gov/article/governor-morrisey-announces-first-2856-million-rural-health-transformation-funding", "event_date": "2026-09-02", "notes": "Re-check on the $199M/$233.5M discrepancy above: an extensive search found no current source citing $233.5M. All live official sources (governor.wv.gov, health.wv.gov) and the WV Hospital Association consistently cite $199M (one figure specifies $199,476,098.72). Origin of the $233.5M figure could not be traced — the discrepancy is not resolved, but the weight of current evidence favors $199M.", "confidence": "confirmed"},
    {"state": "Kentucky", "status": "RFA issued", "source_url": "https://www.kentuckytoday.com/news/kentuckys-rural-health-transformation-plan-secures-212-9m-in-federal-funding/article_2adc2281-3461-4430-995d-07f6a6973df4.html", "event_date": "2025-12-29", "notes": "5 branded initiatives (PoWERing, Rooted in Health, Crisis to Care, Rapid Response to Recovery, Rural Community Hubs) via \"A3 Team\".", "confidence": "confirmed"},
    {"state": "Ohio", "status": "subawards announced", "source_url": "https://governor.ohio.gov/media/news-and-media/governor-dewine-announces-first-rural-health-transformation-program-award-to-ohio-university-for-10-million", "event_date": "2026-07-01", "notes": "First award: $10M to Ohio University for workforce (\"Health Workforce Ohio\").", "confidence": "confirmed"},
    {"state": "Tennessee", "status": "RFA issued", "source_url": "https://www.tn.gov/health/news/2026/5/15/tennessee-to-release-1st-grant-funding-opportunity-of-rural-health-transformation-program.html", "event_date": "2026-05-15", "notes": "Rolling RFAs released weekly through July 10, 2026; 30-day application windows.", "confidence": "confirmed"},
    {"state": "Virginia", "status": "admin structure named", "source_url": "https://dmas.virginia.gov/data-reporting/programs-services/rural-health-transformation/", "event_date": "2026-01-13", "notes": "DMAS hiring core team in early 2026; program branded \"VA Rural Vitality.\" Sparsest official documentation of the 10 — verify further before treating as current.", "confidence": "confirmed"},
    {"state": "North Carolina", "status": "subawards announced", "source_url": "https://www.ncdhhs.gov/divisions/office-rural-health/rural-health-transformation-program", "event_date": "2026-04-01", "notes": "NC ROOTS hubs and Rural Health Infrastructure Fund (RHIF) launched. RHTP Director named (Maggie Woods).", "confidence": "confirmed"},
    {"state": "Pennsylvania", "status": "subawards announced", "source_url": "https://www.pa.gov/agencies/dhs/programs-services/healthcare/rural-health/rhtp-funding-opportunities", "event_date": "2026-07-27", "notes": "EHR/HIO onboarding payment round opened July 27–Aug 14, 2026; $1.8M across 6 awards.", "confidence": "confirmed"},
    {"state": "Pennsylvania", "status": "subawards announced", "source_url": "https://www.pa.gov/agencies/dhs/programs-services/healthcare/rural-health/rhtp-funding-opportunities", "event_date": "2026-09-02", "notes": "Correction to the entry above: the $1.8M/6-award figure was misattributed to the EHR/HIO round. It actually belongs to a separate FQHC onboarding round (deadline Aug 7, 2026). The EHR/HIO round is a distinct $25M track whose award outcome is not yet confirmed on the official page. A further Rapid Response Stabilization Round 2 ($35M, Aug 17–24) has also opened since the original entry.", "confidence": "confirmed"},
    {"state": "Georgia", "status": "subawards announced", "source_url": "https://dch.georgia.gov/announcement/2026-07-16/georgia-issues-30-million-phase-2-great-health-awards-advance-rural", "event_date": "2026-07-16", "notes": "GREAT Health program; Phase 1 ($12.73M, June 8) + Phase 2 ($30.6M, July 16) = $43.3M committed to date.", "confidence": "confirmed"},
    {"state": "Georgia", "status": "subawards announced", "source_url": "https://allongeorgia.com/", "event_date": "2026-08-28", "notes": "UNVERIFIED LEAD: secondary coverage reports a Phase 4 award (~Aug 28, 2026) bringing cumulative commitment to roughly $218M — near-full Year-1 obligation. Could not confirm on dch.georgia.gov directly; status left unchanged pending official confirmation.", "confidence": "unverified"},
    {"state": "Alabama", "status": "subawards announced", "source_url": "https://governor.alabama.gov/newsroom/2026/08/governor-ivey-announces-first-grants-in-major-new-rural-healthcare-program-totaling-more-than-144-million/", "event_date": "2026-08-24", "notes": "ARHTP; 138 grants totaling $144M across 5 of 11 planned initiatives, administered by ADECA.", "confidence": "confirmed"},
    {"state": "Alabama", "status": "subawards announced", "source_url": "https://adeca.alabama.gov/alruralhealth/", "event_date": "2026-09-02", "notes": "Correction to the entry above: ADECA's own program page lists 10 total planned initiatives, not 11 — the '5 of 11' figure came from the governor's newsroom post rather than the program's own page. A second set of 5 initiatives is approved but has no announced timeline yet.", "confidence": "confirmed"},
    {"state": "Mississippi", "status": "RFA issued", "source_url": "https://mississippirhtp.com/", "event_date": "2026-04-29", "notes": "RHTP Office established under Governor's Office (director: Richard Grimes); first round drew ~700 applications for ~$82M available.", "confidence": "confirmed"},
]

# `confidence` is 'confirmed' (direct-fetched from an official .gov page) or
# 'unverified' (secondary source only, or the official page could not be
# fetched directly — kept visible with a caution flag rather than dropped).
DEADLINES = [
    {
        "state": "Tennessee", "title": "Rolling RFA cycle (weekly releases, 30-day windows)",
        "start_date": "2026-05-15", "end_date": "2026-07-10",
        "source_url": "https://www.tn.gov/health/news/2026/5/15/tennessee-to-release-1st-grant-funding-opportunity-of-rural-health-transformation-program.html",
        "notes": "New RFAs release weekly; each carries its own 30-day application window through this closing date.",
        "confidence": "confirmed",
    },
    {
        "state": "Pennsylvania", "title": "EHR/HIO onboarding round ($25M track)",
        "start_date": "2026-07-27", "end_date": "2026-08-14",
        "source_url": "https://www.pa.gov/agencies/dhs/programs-services/healthcare/rural-health/rhtp-funding-opportunities",
        "notes": "Corrected from the original seed note: this window is the separate $25M EHR/HIO track, distinct from the FQHC round below. Award outcome for this track not yet confirmed on the official page.",
        "confidence": "confirmed",
    },
    {
        "state": "Pennsylvania", "title": "FQHC onboarding round",
        "start_date": "2026-08-07", "end_date": None,
        "source_url": "https://www.pa.gov/agencies/dhs/programs-services/healthcare/rural-health/rhtp-funding-opportunities",
        "notes": "$1.8M across 6 awards — this is the round the original seed data's subawards figure actually describes.",
        "confidence": "confirmed",
    },
    {
        "state": "Pennsylvania", "title": "Rapid Response Stabilization, Round 2",
        "start_date": "2026-08-17", "end_date": "2026-08-24",
        "source_url": "https://www.pa.gov/agencies/dhs/programs-services/healthcare/rural-health/rhtp-funding-opportunities",
        "notes": "$35M available, approximately $1M per location.",
        "confidence": "confirmed",
    },
    {
        "state": "Kentucky", "title": "Rural Community Hubs — Chronic Care Innovation RFA",
        "start_date": "2026-06-01", "end_date": None,
        "source_url": "https://ruralhealthplan.ky.gov/Pages/Request_For_Applications.aspx",
        "notes": None, "confidence": "confirmed",
    },
    {
        "state": "Kentucky", "title": "Rooted in Health — Definitive Mobile Dental RFA",
        "start_date": "2026-06-12", "end_date": None,
        "source_url": "https://ruralhealthplan.ky.gov/Pages/Request_For_Applications.aspx",
        "notes": None, "confidence": "confirmed",
    },
    {
        "state": "Kentucky", "title": "Rapid Response to Recovery — CMHC Support / Telebehavioral Health RFA",
        "start_date": "2026-07-06", "end_date": None,
        "source_url": "https://ruralhealthplan.ky.gov/Pages/Request_For_Applications.aspx",
        "notes": None, "confidence": "confirmed",
    },
    {
        "state": "Kentucky", "title": "Community Health Worker Specialized Certificate RFA",
        "start_date": "2026-08-05", "end_date": None,
        "source_url": "https://ruralhealthplan.ky.gov/Pages/Request_For_Applications.aspx",
        "notes": None, "confidence": "confirmed",
    },
    {
        "state": "Virginia", "title": "Digital Productivity Tools grant",
        "start_date": "2026-09-14", "end_date": None,
        "source_url": "https://www.vhcf.org/rural-health/",
        "notes": "Applications due 5:00 PM ET. Anticipated awards $7M–$9M.",
        "confidence": "confirmed",
    },
    {
        "state": "North Carolina", "title": "Mobile Integrated Health Grant",
        "start_date": "2026-05-20", "end_date": None,
        "source_url": "https://www.ncdhhs.gov/divisions/office-rural-health/rural-health-transformation-program",
        "notes": None, "confidence": "confirmed",
    },
    {
        "state": "North Carolina", "title": "NC Minority Diabetes Prevention Program",
        "start_date": "2026-07-17", "end_date": None,
        "source_url": "https://www.ncdhhs.gov/divisions/office-rural-health/rural-health-transformation-program",
        "notes": None, "confidence": "confirmed",
    },
    {
        "state": "North Carolina", "title": "Expanding School Health Centers to Rural Areas",
        "start_date": "2026-07-29", "end_date": "2026-08-12",
        "source_url": "https://www.ncdhhs.gov/divisions/office-rural-health/rural-health-transformation-program",
        "notes": None, "confidence": "confirmed",
    },
    {
        "state": "Alabama", "title": "First 5 initiatives — application deadline",
        "start_date": "2026-08-07", "end_date": None,
        "source_url": "https://adeca.alabama.gov/alruralhealth/",
        "notes": "5:00 PM CT. This round led to the 138 grants / $144M announced August 24, 2026.",
        "confidence": "confirmed",
    },
    {
        "state": "West Virginia", "title": "Rural Health Transformation Program — first application window",
        "start_date": "2026-05-11", "end_date": None,
        "source_url": "https://westvirginiawatch.com/briefs/wv-opens-application-period-for-some-rural-health-transformation-funds/",
        "notes": "Deadline 11:59 PM. Reported by West Virginia Watch; the official page returned an error on direct fetch, so this date could not be confirmed on a primary source. Verify with WV DHHR before relying on it.",
        "confidence": "unverified",
    },
    {
        "state": "Ohio", "title": "Workforce RFP window",
        "start_date": "2026-03-10", "end_date": None,
        "source_url": "https://odh.ohio.gov/know-our-programs/rural-health-transformation-program/rural-health-transformation-program",
        "notes": "Surfaced only via secondary aggregation; the official ODH page did not load on direct fetch (404), so this date is unconfirmed and already in the past regardless.",
        "confidence": "unverified",
    },
    {
        "state": "Mississippi", "title": "EMS Capacity Assessment RFA",
        "start_date": "2026-07-24", "end_date": None,
        "source_url": "https://magnoliatribune.com/",
        "notes": "Reported by Magnolia Tribune (secondary source); not confirmed directly on mississippirhtp.com.",
        "confidence": "unverified",
    },
    {
        "state": "Mississippi", "title": "Psychiatric Emergency Services / Workforce Expansion RFA",
        "start_date": "2026-08-17", "end_date": None,
        "source_url": "https://magnoliatribune.com/",
        "notes": "Reported by Magnolia Tribune (secondary source); not confirmed directly on mississippirhtp.com.",
        "confidence": "unverified",
    },
    {
        "state": "West Virginia", "title": "Deadline to obligate FY26 award",
        "start_date": "2026-10-31", "end_date": None,
        "source_url": "https://wvpress.org/breaking-news/lawmakers-question-progress-of-rural-health-transformation-program/",
        "notes": "Reported consistently across WV Press Association, News and Sentinel, and The Intermountain: state officials are working to obligate the full ~$199M FY26 award by this federal deadline. This is a program-mechanics deadline, not an applicant-facing one.",
        "confidence": "confirmed",
    },
]

# Third-party commentary — opinion, analysis, and investigative coverage of
# the program from outside the state agencies themselves. Kept on a separate
# page from the sourced facts above: these are outside viewpoints, not
# verified data points, and are labeled by angle so a reader can weigh them
# accordingly.
COMMENTARY = [
    {
        "title": "The rural health transformation program isn't so transformational",
        "source_name": "Bloomberg Opinion", "url": "https://www.bloomberg.com/opinion/articles/2026-04-05/rural-health-transformation-program-isn-t-so-transformational",
        "published_date": "2026-04-05", "state": None, "angle": "opinion",
        "summary": "Argues the program's design — only 15% of funds may directly pay providers — leaves it unable to solve the reimbursement problem driving rural hospital closures.",
    },
    {
        "title": "The Rural Health Transformation Program could fail patients like mine",
        "source_name": "STAT News", "url": "https://www.statnews.com/2026/02/25/rural-health-transformation-program-hospitals-innovation/",
        "published_date": "2026-02-25", "state": None, "angle": "opinion",
        "summary": "A physician's first-person case that the program's emphasis on innovation funding over direct hospital support risks leaving acute-care gaps unaddressed.",
    },
    {
        "title": "$50B Rural Health Transformation Program Needs More Transparency, Groups Say",
        "source_name": "KFF Health News", "url": "https://kffhealthnews.org/rural-health/rural-health-transformation-program-transparency-50-billion-dollars-state-tracking/",
        "published_date": None, "state": None, "angle": "investigative",
        "summary": "Reports that CMS and several states aren't proactively publishing where funds are going, complicating fraud oversight and independent tracking of results — the same gap this tracker is trying to help close.",
    },
    {
        "title": "Marketplace Pulse: Rural Health Transformation Program Will Not Meet the Moment for Rural Healthcare Systems",
        "source_name": "Robert Wood Johnson Foundation", "url": "https://www.rwjf.org/en/insights/our-research/2026/03/marketplace-pulse-rural-health-transformation-program-will-not-meet-the-moment-for-rural-healthcare-systems.html",
        "published_date": "2026-03", "state": None, "angle": "analysis",
        "summary": "A foundation research note arguing the program's total funding and structure fall short of the scale of rural hospital financial distress it aims to address.",
    },
    {
        "title": "Council Post: Why Transformation, Not Funding, Is The Path Forward For Rural Health",
        "source_name": "Forbes Business Council", "url": "https://www.forbes.com/councils/forbesbusinesscouncil/2026/07/10/why-transformation-not-funding-is-the-path-forward-for-rural-health/",
        "published_date": "2026-07-10", "state": None, "angle": "opinion",
        "summary": "An industry-council perspective arguing operational and care-model transformation matters more than the dollar amount of the award itself.",
    },
    {
        "title": "Questions remain on rural health transformation funds' effects on rural hospitals",
        "source_name": "North Carolina Health News", "url": "https://www.northcarolinahealthnews.org/2026/07/26/questions-remain-on-rural-health-transformation-funds-effects-on-rural-hospitals/",
        "published_date": "2026-07-26", "state": "North Carolina", "angle": "analysis",
        "summary": "State-focused reporting on whether NC's ROOTS hubs and RHIF disbursements are reaching hospitals under the most acute financial strain.",
    },
    {
        "title": "Lawmakers question progress of Rural Health Transformation Program",
        "source_name": "WV Press Association", "url": "https://wvpress.org/breaking-news/lawmakers-question-progress-of-rural-health-transformation-program/",
        "published_date": "2026-08", "state": "West Virginia", "angle": "news",
        "summary": "Covers WV legislative interim-committee questions on contract transparency, vendor selection (including a KPMG contract amendment), and the pace of implementation ahead of the Oct 31 obligation deadline.",
    },
]

# Editorial, not sourced fact — see ANALYSIS_DISCLAIMER in main.py / the UI.
# Derived from the notes above for comparison purposes; review before relying
# on it for a real application decision.
ANALYSIS = {
    "West Virginia": {
        "pros": [
            "Subawards are already open across three named initiatives (MSCF, HealthTech Appalachia, Connected Care Grid) — a concrete path to funding now, not a future promise.",
            "Multiple parallel tracks mean more than one way in, depending on what an applicant does.",
        ],
        "cons": [
            "The total award figure is disputed ($199M official vs. $233.5M reported elsewhere) — confirm the number before relying on it for planning.",
            "Documentation is split across three initiative-specific pages rather than one central RFA.",
        ],
    },
    "Kentucky": {
        "pros": [
            "Five clearly branded initiatives make it easier to identify which track fits a given applicant.",
            "One of the larger total awards among the 10 states, suggesting room for multiple funded projects.",
        ],
        "cons": [
            "Still pre-award — RFA issued but no subawards announced yet, so expect a longer runway before funds are disbursed.",
        ],
    },
    "Ohio": {
        "pros": [
            "A first award is already made and public — proof the pipeline is moving and a working example to reference in an application.",
        ],
        "cons": [
            "Only $10M of the $202M total has been publicized so far — criteria and scope for future rounds are still thin.",
        ],
    },
    "Tennessee": {
        "pros": [
            "Rolling weekly RFA releases with defined 30-day windows give a predictable application calendar.",
        ],
        "cons": [
            "Because RFAs roll out over months, applicants need to actively monitor for the specific opportunity relevant to them.",
            "No subawards announced yet.",
        ],
    },
    "Virginia": {
        "pros": [
            "Program branding (\"VA Rural Vitality\") and DMAS ownership are established, giving applicants a clear point of contact as the program matures.",
        ],
        "cons": [
            "Sparsest official documentation of the 10 states — no RFA or subaward details published yet.",
            "Smallest total award among the 10 states tracked here.",
        ],
    },
    "North Carolina": {
        "pros": [
            "A named program director and two launched structures (NC ROOTS hubs, RHIF) suggest real operating capacity, not just a funding announcement.",
        ],
        "cons": [
            "No specific subaward dollar figure has been published yet, making it hard to gauge how much of the $213M has actually moved.",
        ],
    },
    "Pennsylvania": {
        "pros": [
            "Multiple concrete rounds have run in quick succession (FQHC, EHR/HIO, and a second Rapid Response Stabilization round) — the program is actively disbursing across several tracks, not just planning.",
        ],
        "cons": [
            "Confirmed disbursement to date ($1.8M FQHC) is small relative to the $193M total, and outcomes for the larger EHR/HIO ($25M) and Rapid Response ($35M) rounds aren't yet confirmed on the official page — most of the program is still unallocated or unconfirmed.",
        ],
    },
    "Georgia": {
        "pros": [
            "Largest total award of the 10 states, plus two funded phases already committed — sustained disbursement, not a one-off.",
        ],
        "cons": [
            "$43.3M committed is still a small fraction of the $218.9M total — most capacity remains undecided.",
        ],
    },
    "Alabama": {
        "pros": [
            "By far the most subaward activity of the 10 states — 138 grants already made, the strongest evidence that money is reaching recipients.",
            "5 of 10 planned initiatives are already open, with a second set of 5 already approved.",
        ],
        "cons": [
            "The second set of 5 initiatives has no announced timeline yet, so applicants outside the first 5 tracks have no visibility.",
        ],
    },
    "Mississippi": {
        "pros": [
            "High first-round application volume (~700 applications) signals strong demand and an active applicant community to learn from.",
        ],
        "cons": [
            "That same demand (~700 applications for ~$82M) means steep competition — worth sizing expectations accordingly.",
            "No subawards announced yet.",
        ],
    },
}

# Program overview per state — emphasis/applicant_profile are a brief summary
# derived from the sourced notes/timeline above (not a direct quote from the
# state), so treat them like the ANALYSIS section: informative, not official.
# Pillars are the actual named initiative/track titles as they appear in the
# sources — those are facts, not summary. contact_email is left null and
# contact_note explains why whenever a state hasn't published one; never
# guessed or constructed from a name/agency.
STATE_OVERVIEW = {
    "West Virginia": {
        "emphasis": "Funds are moving through three parallel, initiative-specific tracks rather than one central RFA — each with its own scope and timeline.",
        "applicant_profile": "Not detailed beyond the three initiative names in current sources.",
        "contact_name": None,
        "contact_email": None,
        "contact_note": "No public contact email found in sourced materials.",
    },
    "Kentucky": {
        "emphasis": "Five branded initiatives are administered together under a single coordinating body (\"A3 Team\"), with RFAs released per initiative.",
        "applicant_profile": "Tracks published so far span chronic care innovation, mobile dental services, telebehavioral health/CMHC support, and community health worker certification — suggesting eligibility spans clinical, community, and workforce-training organizations.",
        "contact_name": None,
        "contact_email": None,
        "contact_note": "No public contact email found in sourced materials.",
    },
    "Ohio": {
        "emphasis": "Workforce development was the first priority funded, ahead of other possible tracks.",
        "applicant_profile": "The first award went to a university for workforce programming, suggesting higher-education and workforce-training partners are eligible alongside direct care providers.",
        "contact_name": None,
        "contact_email": None,
        "contact_note": "No public contact email found in sourced materials.",
    },
    "Tennessee": {
        "emphasis": "Uses a rolling, recurring RFA cycle rather than a single funding round, with new opportunities posted weekly.",
        "applicant_profile": "Not yet detailed in current sources — specific tracks/pillars haven't been published beyond the rolling-RFA structure itself.",
        "contact_name": None,
        "contact_email": None,
        "contact_note": "No public contact email found in sourced materials.",
    },
    "Virginia": {
        "emphasis": "Program branded \"VA Rural Vitality\"; administrative staffing was still being built out as of the most recent sourced update.",
        "applicant_profile": "The one published track (Digital Productivity Tools) suggests technology vendors and/or providers adopting digital tools are an eligible category; broader applicant criteria not yet detailed.",
        "contact_name": None,
        "contact_email": None,
        "contact_note": "No public contact email found in sourced materials.",
    },
    "North Carolina": {
        "emphasis": "Combines standing regional infrastructure (hubs, an infrastructure fund) with targeted, topic-specific grant rounds.",
        "applicant_profile": "Published rounds span EMS/mobile integrated health providers, diabetes-prevention programs, and school-based health centers — a broad, multi-track eligibility pool.",
        "contact_name": "Maggie Woods (RHTP Director)",
        "contact_email": None,
        "contact_note": "A director is named publicly; no direct email address has been published in sourced materials.",
    },
    "Pennsylvania": {
        "emphasis": "Runs multiple narrow, sequential funding rounds, each scoped to a specific technology or service track rather than one broad RFA.",
        "applicant_profile": "Tracks published so far target FQHCs, health information organizations (HIOs), and facilities eligible for stabilization funding.",
        "contact_name": None,
        "contact_email": None,
        "contact_note": "No public contact email found in sourced materials.",
    },
    "Georgia": {
        "emphasis": "Disburses under a single branded program (GREAT Health) in sequential phases rather than one lump award.",
        "applicant_profile": "Not detailed in current sources beyond the phase structure itself.",
        "contact_name": None,
        "contact_email": None,
        "contact_note": "No public contact email found in sourced materials.",
    },
    "Alabama": {
        "emphasis": "Runs the broadest initiative slate of the 10 states tracked here — 10 planned initiatives total, with the first 5 already open and a second set of 5 approved.",
        "applicant_profile": "Not detailed in current sources beyond the initiative count.",
        "contact_name": None,
        "contact_email": None,
        "contact_note": "No public contact email found in sourced materials.",
    },
    "Mississippi": {
        "emphasis": "Centralized under a dedicated RHTP Office reporting to the Governor's Office, rather than an existing health-agency division.",
        "applicant_profile": "The first round drew roughly 700 applications for ~$82M, and newer unverified leads point toward EMS capacity and psychiatric emergency services as upcoming tracks (see Calendar) — suggesting broad eligibility across rural EMS and behavioral health providers.",
        "contact_name": "Richard Grimes (RHTP Office Director)",
        "contact_email": None,
        "contact_note": "A director is named publicly; no direct email address has been published in sourced materials.",
    },
}

STATE_PILLARS = {
    "West Virginia": ["MSCF", "HealthTech Appalachia", "Connected Care Grid"],
    "Kentucky": ["PoWERing", "Rooted in Health", "Crisis to Care", "Rapid Response to Recovery", "Rural Community Hubs"],
    "Ohio": ["Health Workforce Ohio"],
    "Tennessee": [],
    "Virginia": ["Digital Productivity Tools"],
    "North Carolina": ["NC ROOTS hubs", "Rural Health Infrastructure Fund (RHIF)", "Mobile Integrated Health", "NC Minority Diabetes Prevention", "School Health Centers expansion"],
    "Pennsylvania": ["FQHC onboarding", "EHR/HIO onboarding", "Rapid Response Stabilization"],
    "Georgia": ["GREAT Health — Phase 1", "GREAT Health — Phase 2"],
    "Alabama": ["ARHTP (5 of 10 initiatives open)"],
    "Mississippi": ["EMS Capacity Assessment (unverified lead)", "Psychiatric Emergency Services / Workforce Expansion (unverified lead)"],
}

STATUS_TAXONOMY = [
    "plan approved",
    "admin structure named",
    "RFA issued",
    "subawards announced",
    "funds obligated",
]
