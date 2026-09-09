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
    {"state": "West Virginia", "fiscal_year": "FY26", "amount": 199476099, "status": "subawards announced", "source_url": "https://wvpublic.org/story/government/2-4-million-awarded-to-help-w-va-residents-stay-healthy-working/", "verified_at": "2026-09-07", "subawards_amount": 30958000, "subawards_label": "cumulative across 2 tranches (Apr + Sep 2026)", "usaspending_url": "https://www.usaspending.gov/award/ASST_NON_RHTCMS332054_075"},
    {"state": "Kentucky", "fiscal_year": "FY26", "amount": 212905591, "status": "RFA issued", "source_url": "https://www.kentuckytoday.com/news/kentuckys-rural-health-transformation-plan-secures-212-9m-in-federal-funding/article_2adc2281-3461-4430-995d-07f6a6973df4.html", "verified_at": "2026-09-02", "subawards_amount": None, "subawards_label": None, "usaspending_url": "https://www.usaspending.gov/award/ASST_NON_RHTCMS332079_075"},
    {"state": "Ohio", "fiscal_year": "FY26", "amount": 202030262, "status": "subawards announced", "source_url": "https://governor.ohio.gov/media/news-and-media/governor-dewine-announces-first-rural-health-transformation-program-award-to-ohio-university-for-10-million", "verified_at": "2026-09-02", "subawards_amount": 10000000, "subawards_label": "first award announced", "usaspending_url": "https://www.usaspending.gov/award/ASST_NON_RHTCMS332087_075"},
    {"state": "Tennessee", "fiscal_year": "FY26", "amount": 206888882, "status": "subawards announced", "source_url": "https://www.tn.gov/health/news/2026/9/3/tennessee-department-of-health-announces-1st-recipients-of-rural-health-transformation-program-grants.html", "verified_at": "2026-09-07", "subawards_amount": None, "subawards_label": None, "usaspending_url": "https://www.usaspending.gov/award/ASST_NON_RHTCMS332057_075"},
    {"state": "Virginia", "fiscal_year": "FY26", "amount": 189544888, "status": "subawards announced", "source_url": "https://www.cms.gov/newsroom/press-releases/trump-administration-announces-122-million-expand-healthcare-access-workforce-innovation-across", "verified_at": "2026-09-07", "subawards_amount": 122000000, "subawards_label": "first disbursement wave, Aug 28 2026", "usaspending_url": "https://www.usaspending.gov/award/ASST_NON_RHTCMS332088_075"},
    {"state": "North Carolina", "fiscal_year": "FY26", "amount": 213008356, "status": "subawards announced", "source_url": "https://www.ncdhhs.gov/news/press-releases/2026/06/08/ncdhhs-announces-10-million-ems-workforce-through-nc-rural-health-transformation-program", "verified_at": "2026-09-08", "subawards_amount": 10000000, "subawards_label": "EMS Mobile Integrated Health grant, Jun 2026 (3 digital-health programs also launched but not yet dollar-quantified)", "usaspending_url": "https://www.usaspending.gov/award/ASST_NON_RHTCMS332042_075"},
    {"state": "Pennsylvania", "fiscal_year": "FY26", "amount": 193294054, "status": "subawards announced", "source_url": "https://www.pa.gov/agencies/dhs/programs-services/healthcare/rural-health/rhtp-funding-opportunities", "verified_at": "2026-09-02", "subawards_amount": 1800000, "subawards_label": "6 awards, FQHC track", "usaspending_url": "https://www.usaspending.gov/award/ASST_NON_RHTCMS332052_075"},
    {"state": "Georgia", "fiscal_year": "FY26", "amount": 218862169, "status": "subawards announced", "source_url": "https://allongeorgia.com/chattooga-local-news/georgia-reaches-major-milestone-with-all-year-1-great-health-awards-fully-committed", "verified_at": "2026-09-07", "subawards_amount": 218862169, "subawards_label": "Year 1 fully committed across 4 phases", "usaspending_url": "https://www.usaspending.gov/award/ASST_NON_RHTCMS332046_075"},
    {"state": "Alabama", "fiscal_year": "FY26", "amount": 203404327, "status": "subawards announced", "source_url": "https://governor.alabama.gov/newsroom/2026/08/governor-ivey-announces-first-grants-in-major-new-rural-healthcare-program-totaling-more-than-144-million/", "verified_at": "2026-09-02", "subawards_amount": 144000000, "subawards_label": "138 grants, 5 of 10 initiatives", "usaspending_url": "https://www.usaspending.gov/award/ASST_NON_RHTCMS332060_075"},
    {"state": "Mississippi", "fiscal_year": "FY26", "amount": 205907220, "status": "RFA issued", "source_url": "https://mississippirhtp.com/", "verified_at": "2026-09-02", "subawards_amount": None, "subawards_label": None, "usaspending_url": "https://www.usaspending.gov/award/ASST_NON_RHTCMS332063_075"},
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
    {"state": "West Virginia", "status": "subawards announced", "source_url": "https://wvpublic.org/story/government/2-4-million-awarded-to-help-w-va-residents-stay-healthy-working/", "event_date": "2026-09-04", "notes": "Second subaward round: ~$2.4M in first implementation awards under the worksite-clinic/employer-based-health initiative (announced as an open solicitation June 24, 2026) — Spotted Owl Healthcare Organization ($1,174,000), CAMC/Vandalia Health ($612,000), Cabell Huntington Foundation ($612,000). Governor's office says more announcements are planned over the next 60 days to distribute the remaining balance of the ~$199M award.", "confidence": "confirmed"},
    {"state": "Kentucky", "status": "RFA issued", "source_url": "https://www.kentuckytoday.com/news/kentuckys-rural-health-transformation-plan-secures-212-9m-in-federal-funding/article_2adc2281-3461-4430-995d-07f6a6973df4.html", "event_date": "2025-12-29", "notes": "5 branded initiatives (PoWERing, Rooted in Health, Crisis to Care, Rapid Response to Recovery, Rural Community Hubs) via \"A3 Team\".", "confidence": "confirmed"},
    {"state": "Ohio", "status": "subawards announced", "source_url": "https://governor.ohio.gov/media/news-and-media/governor-dewine-announces-first-rural-health-transformation-program-award-to-ohio-university-for-10-million", "event_date": "2026-07-01", "notes": "First award: $10M to Ohio University for workforce (\"Health Workforce Ohio\").", "confidence": "confirmed"},
    {"state": "Tennessee", "status": "RFA issued", "source_url": "https://www.tn.gov/health/news/2026/5/15/tennessee-to-release-1st-grant-funding-opportunity-of-rural-health-transformation-program.html", "event_date": "2026-05-15", "notes": "Rolling RFAs released weekly through July 10, 2026; 30-day application windows.", "confidence": "confirmed"},
    {"state": "Tennessee", "status": "subawards announced", "source_url": "https://www.tn.gov/health/news/2026/9/3/tennessee-department-of-health-announces-1st-recipients-of-rural-health-transformation-program-grants.html", "event_date": "2026-09-03", "notes": "TDH announced its first round of RHTP awards: 53 projects across 44 rural counties under the Healthy Active Rural Tennessee (HART) initiative (nutrition/fitness/community-support focus, not clinical infrastructure) — 31 awards (58%) to county/municipal governments, 22 (42%) to nonprofits. Full award list published as a downloadable spreadsheet on the TDH site.", "confidence": "confirmed"},
    {"state": "Virginia", "status": "admin structure named", "source_url": "https://dmas.virginia.gov/data-reporting/programs-services/rural-health-transformation/", "event_date": "2026-01-13", "notes": "DMAS hiring core team in early 2026; program branded \"VA Rural Vitality.\" Sparsest official documentation of the 10 — verify further before treating as current.", "confidence": "confirmed"},
    {"state": "Virginia", "status": "subawards announced", "source_url": "https://www.cms.gov/newsroom/press-releases/trump-administration-announces-122-million-expand-healthcare-access-workforce-innovation-across", "event_date": "2026-08-28", "notes": "CMS announced $122M of Virginia's $189.5M RHTP award disbursed, funding remote patient monitoring/virtual care, mobile clinics, maternal care, community paramedicine, allied-health career pathways, and early-stage health-tech scaling. Secondary reporting (Virginia Mercury) names initial grantees: Virginia Hospital and Healthcare Association Foundation, Virginia Foundation for Community College Education, and the Virginia Dept. for Aging and Rehabilitative Services. Next disbursement wave expected by end of October 2026. Skips directly from 'admin structure named' — no RFA-issued milestone was found in current sources.", "confidence": "confirmed"},
    {"state": "North Carolina", "status": "subawards announced", "source_url": "https://www.ncdhhs.gov/divisions/office-rural-health/rural-health-transformation-program", "event_date": "2026-04-01", "notes": "NC ROOTS hubs and Rural Health Infrastructure Fund (RHIF) launched. RHTP Director named (Maggie Woods).", "confidence": "confirmed"},
    {"state": "North Carolina", "status": "subawards announced", "source_url": "https://www.ncdhhs.gov/news/press-releases/2026/06/08/ncdhhs-announces-10-million-ems-workforce-through-nc-rural-health-transformation-program", "event_date": "2026-06-08", "notes": "$10M distributed to 39 local EMS agencies through the NC Office of EMS for Mobile Integrated Health — supports overdose follow-up care, opioid-use-disorder medication delivery in the field, and EMS workforce strengthening.", "confidence": "confirmed"},
    {"state": "North Carolina", "status": "subawards announced", "source_url": "https://www.ncdhhs.gov/news/press-releases/2026/06/24/ncdhhs-ncdit-announce-three-programs-improve-health-care-part-north-carolinas-rural-health", "event_date": "2026-06-24", "notes": "NCDHHS + NC DIT announced 3 digital-health programs under NCRHTP Initiative Six: (1) Rural Health Innovation Fund — $20M/year for 5 years, competitive applications expected to open 'in September 2026' (no specific date given); (2) NC HealthConnex (state HIE) expansion support for rural orgs; (3) Digital Health Literacy Program via NC 211 Digital Navigators, live since July 1, 2026. No new dollar figure beyond the $10M EMS grant above has been disbursed yet under these three programs.", "confidence": "confirmed"},
    {"state": "Pennsylvania", "status": "subawards announced", "source_url": "https://www.pa.gov/agencies/dhs/programs-services/healthcare/rural-health/rhtp-funding-opportunities", "event_date": "2026-07-27", "notes": "EHR/HIO onboarding payment round opened July 27–Aug 14, 2026; $1.8M across 6 awards.", "confidence": "confirmed"},
    {"state": "Pennsylvania", "status": "subawards announced", "source_url": "https://www.pa.gov/agencies/dhs/programs-services/healthcare/rural-health/rhtp-funding-opportunities", "event_date": "2026-09-02", "notes": "Correction to the entry above: the $1.8M/6-award figure was misattributed to the EHR/HIO round. It actually belongs to a separate FQHC onboarding round (deadline Aug 7, 2026). The EHR/HIO round is a distinct $25M track whose award outcome is not yet confirmed on the official page. A further Rapid Response Stabilization Round 2 ($35M, Aug 17–24) has also opened since the original entry.", "confidence": "confirmed"},
    {"state": "Pennsylvania", "status": "subawards announced", "source_url": "https://www.wellspan.org/articles/2026/07/24/12/49/web---federal-grant---rural-health", "event_date": "2026-07-24", "notes": "UNVERIFIED LEAD: WellSpan Health's own announcement states it received $2.8M from PA DHS's RHTP EHR/HIO round for upgrades at its Chambersburg, Waynesboro, and Evangelical (Lewisburg) hospitals. This would be the first named recipient for the $25M EHR/HIO track, but PA's own DHS page still lists that track's outcome as unconfirmed — this is a recipient-side claim only, not yet corroborated by the state.", "confidence": "unverified"},
    {"state": "Georgia", "status": "subawards announced", "source_url": "https://dch.georgia.gov/announcement/2026-07-16/georgia-issues-30-million-phase-2-great-health-awards-advance-rural", "event_date": "2026-07-16", "notes": "GREAT Health program; Phase 1 ($12.73M, June 8) + Phase 2 ($30.6M, July 16) = $43.3M committed to date.", "confidence": "confirmed"},
    {"state": "Georgia", "status": "subawards announced", "source_url": "https://allongeorgia.com/", "event_date": "2026-08-28", "notes": "UNVERIFIED LEAD: secondary coverage reports a Phase 4 award (~Aug 28, 2026) bringing cumulative commitment to roughly $218M — near-full Year-1 obligation. Could not confirm on dch.georgia.gov directly; status left unchanged pending official confirmation.", "confidence": "unverified"},
    {"state": "Georgia", "status": "subawards announced", "source_url": "https://allongeorgia.com/chattooga-local-news/georgia-reaches-major-milestone-with-all-year-1-great-health-awards-fully-committed", "event_date": "2026-08-27", "notes": "CONFIRMS the entry above: a Georgia DCH press release (relayed with direct quotes by AllOnGeorgia) states all Year 1 GREAT Health awards are now fully committed, totaling $218,862,169.63 — essentially the state's full FY26 award. Phase 4 breakdown: Initiative 1 (Hospital Transformation) $15.635M, Initiative 2 (Continuum of Care) $6.21M, Initiative 3 (Healthcare Access) $10.38M, Initiative 4 (Workforce) $23.6M, Initiative 5 (Technology) $37.5M. Named recipients include Georgia Health Care Association, Emory University, Georgia Hospital Association, Georgia DPH, Georgia DBHDD, Georgia EMS Association, Georgia Board of Healthcare Workforce, and Equifax. Could not locate the underlying dch.georgia.gov press release directly, so this cites the journalism relaying it.", "confidence": "confirmed"},
    {"state": "Alabama", "status": "subawards announced", "source_url": "https://governor.alabama.gov/newsroom/2026/08/governor-ivey-announces-first-grants-in-major-new-rural-healthcare-program-totaling-more-than-144-million/", "event_date": "2026-08-24", "notes": "ARHTP; 138 grants totaling $144M across 5 of 11 planned initiatives, administered by ADECA.", "confidence": "confirmed"},
    {"state": "Alabama", "status": "subawards announced", "source_url": "https://adeca.alabama.gov/alruralhealth/", "event_date": "2026-09-02", "notes": "Correction to the entry above: ADECA's own program page lists 10 total planned initiatives, not 11 — the '5 of 11' figure came from the governor's newsroom post rather than the program's own page. A second set of 5 initiatives is approved but has no announced timeline yet.", "confidence": "confirmed"},
    {"state": "Mississippi", "status": "RFA issued", "source_url": "https://mississippirhtp.com/", "event_date": "2026-04-29", "notes": "RHTP Office established under Governor's Office (director: Richard Grimes); first round drew ~700 applications for ~$82M available.", "confidence": "confirmed"},
    {"state": "Mississippi", "status": "RFA issued", "source_url": "https://www.wlbt.com/2026/08/06/mississippi-rural-health-transformation-program-begins-awarding-grants/", "event_date": "2026-08-06", "notes": "Selection completed for 3 grant programs (Rural Capital Care Gap Closure, Rural Technology Grant, Telehealth Hub Connectivity/Equipment/Education); selected applicants were being contacted to begin sub-award execution. Director Richard Grimes said awards were 'expected by the end of the month' (Aug 2026) with a goal of having all funds obligated by the October federal deadline. As of Sep 7, 2026 no formal named-recipient/dollar announcement has been found, so status is left at RFA issued pending that.", "confidence": "confirmed"},
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
        "emphasis": "Funds are moving through a series of separate, initiative-specific rounds rather than one central RFA — a second round (worksite clinics/employer-based health) has now made its first awards, with more rounds planned over the following two months.",
        "applicant_profile": "Not detailed beyond the initiative names in current sources.",
        "contact_name": None,
        "contact_email": None,
        "contact_note": "No public contact email found in sourced materials.",
        "updated_at": "2026-09-07",
    },
    "Kentucky": {
        "emphasis": "Five branded initiatives are administered together under a single coordinating body (\"A3 Team\"), with RFAs released per initiative.",
        "applicant_profile": "Tracks published so far span chronic care innovation, mobile dental services, telebehavioral health/CMHC support, and community health worker certification — suggesting eligibility spans clinical, community, and workforce-training organizations.",
        "contact_name": None,
        "contact_email": None,
        "contact_note": "No public contact email found in sourced materials.",
        "updated_at": "2026-09-02",
    },
    "Ohio": {
        "emphasis": "Workforce development was the first priority funded, ahead of other possible tracks.",
        "applicant_profile": "The first award went to a university for workforce programming, suggesting higher-education and workforce-training partners are eligible alongside direct care providers.",
        "contact_name": None,
        "contact_email": None,
        "contact_note": "No public contact email found in sourced materials.",
        "updated_at": "2026-09-02",
    },
    "Tennessee": {
        "emphasis": "Uses a rolling, recurring RFA cycle rather than a single funding round; its first subaward round has now been announced (53 projects, 44 counties) under the branded Healthy Active Rural Tennessee initiative.",
        "applicant_profile": "First round funded county/municipal governments (58%) and nonprofits (42%) for community nutrition, fitness, and support programs — not clinical infrastructure.",
        "contact_name": None,
        "contact_email": None,
        "contact_note": "No public contact email found in sourced materials.",
        "updated_at": "2026-09-08",
    },
    "Virginia": {
        "emphasis": "Program branded \"VA Rural Vitality\"; a first disbursement wave ($122M of the $189.5M award) has now been confirmed by CMS, with a second wave expected by end of October 2026.",
        "applicant_profile": "Named initial grantees include the Virginia Hospital and Healthcare Association Foundation (remote patient monitoring, rural residencies), the Virginia Foundation for Community College Education (workforce growth), and the Virginia Dept. for Aging and Rehabilitative Services.",
        "contact_name": None,
        "contact_email": None,
        "contact_note": "No public contact email found in sourced materials.",
        "updated_at": "2026-09-08",
    },
    "North Carolina": {
        "emphasis": "Combines standing regional infrastructure (hubs, an infrastructure fund) with targeted, topic-specific grant rounds; a confirmed $10M EMS grant plus three new digital-health programs have since launched.",
        "applicant_profile": "Published rounds span EMS/mobile integrated health providers, diabetes-prevention programs, school-based health centers, and (newly) digital-health/HIE and health-literacy initiatives — a broad, multi-track eligibility pool.",
        "contact_name": "Maggie Woods (RHTP Director)",
        "contact_email": None,
        "contact_note": "A director is named publicly; no direct email address has been published in sourced materials.",
        "updated_at": "2026-09-08",
    },
    "Pennsylvania": {
        "emphasis": "Runs multiple narrow, sequential funding rounds, each scoped to a specific technology or service track rather than one broad RFA.",
        "applicant_profile": "Tracks published so far target FQHCs, health information organizations (HIOs), and facilities eligible for stabilization funding.",
        "contact_name": None,
        "contact_email": None,
        "contact_note": "No public contact email found in sourced materials.",
        "updated_at": "2026-09-02",
    },
    "Georgia": {
        "emphasis": "Disburses under a single branded program (GREAT Health) in sequential phases; as of Phase 4, all Year 1 funds ($218.9M) are now fully committed.",
        "applicant_profile": "Named recipients across the 4 phases include Georgia Health Care Association, Emory University, Georgia Hospital Association, Georgia DPH, Georgia DBHDD, Georgia EMS Association, Georgia Board of Healthcare Workforce, and Equifax.",
        "contact_name": None,
        "contact_email": None,
        "contact_note": "No public contact email found in sourced materials.",
        "updated_at": "2026-09-08",
    },
    "Alabama": {
        "emphasis": "Runs the broadest initiative slate of the 10 states tracked here — 10 planned initiatives total, with the first 5 already open and a second set of 5 approved.",
        "applicant_profile": "Not detailed in current sources beyond the initiative count.",
        "contact_name": None,
        "contact_email": None,
        "contact_note": "No public contact email found in sourced materials.",
        "updated_at": "2026-09-02",
    },
    "Mississippi": {
        "emphasis": "Centralized under a dedicated RHTP Office reporting to the Governor's Office, rather than an existing health-agency division.",
        "applicant_profile": "The first round drew roughly 700 applications for ~$82M, and newer unverified leads point toward EMS capacity and psychiatric emergency services as upcoming tracks (see Calendar) — suggesting broad eligibility across rural EMS and behavioral health providers.",
        "contact_name": "Richard Grimes (RHTP Office Director)",
        "contact_email": None,
        "contact_note": "A director is named publicly; no direct email address has been published in sourced materials.",
        "updated_at": "2026-09-02",
    },
}

STATE_PILLARS = {
    "West Virginia": ["MSCF", "HealthTech Appalachia", "Connected Care Grid", "Health to Prosperity (worksite clinics)"],
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

# One entry per MATERIAL change made to a state's overview/pillars/analysis/
# award figures after initial publication (a number correction, a contact
# appearing, a pillar list changing) — not for copy-editing. Empty at launch
# since there's no prior version to have changed from yet; add an entry here
# (and bump that state's "updated_at" in STATE_OVERVIEW) whenever a real
# future edit qualifies. See README for the full policy.
STATE_CHANGELOG = [
    {"state": "Hawaii", "changed_at": "2026-09-07", "summary": "Status advanced from 'admin structure named' to 'subawards announced': $58M announced Sep 1, 2026 ($45M UH medical-school workforce program + $13M ambulances/emergency comms), ending an 8-month stall."},
    {"state": "Delaware", "changed_at": "2026-09-07", "summary": "Status advanced from 'RFA issued' to 'subawards announced': Thomas Jefferson University selected to establish Delaware's first medical school."},
    {"state": "West Virginia", "changed_at": "2026-09-07", "summary": "Second subaward round announced: ~$2.4M in first implementation awards for worksite clinics, to 3 named organizations. Cumulative subawards now ~$31.0M."},
    {"state": "Tennessee", "changed_at": "2026-09-08", "summary": "Status advanced from 'RFA issued' to 'subawards announced': first round of HART awards announced, 53 projects across 44 rural counties."},
    {"state": "Virginia", "changed_at": "2026-09-08", "summary": "Status advanced from 'admin structure named' to 'subawards announced': CMS confirmed $122M disbursed of the $189.5M award."},
    {"state": "Georgia", "changed_at": "2026-09-08", "summary": "Subaward total corrected/updated from ~$43.3M to $218.86M: all Year 1 GREAT Health awards now fully committed across 4 phases."},
    {"state": "North Carolina", "changed_at": "2026-09-08", "summary": "First subaward dollar figure recorded: $10M to 39 EMS agencies for Mobile Integrated Health, plus three new digital-health programs launched."},
    {"state": "Indiana", "changed_at": "2026-09-08", "summary": "Status advanced from 'RFA issued' to 'subawards announced': $13.1M GROW Regional Grant to South Central Indiana (Region 7), reportedly completing all 8 regions."},
    {"state": "Louisiana", "changed_at": "2026-09-08", "summary": "Status advanced from 'RFA issued' to 'subawards announced': first named recipient, University of Louisiana Monroe, $2.1M."},
    {"state": "Nevada", "changed_at": "2026-09-08", "summary": "Subaward total updated from $36M to $86M: a second $50M workforce round (residencies, apprenticeships, provider recruitment) confirmed."},
    {"state": "New Hampshire", "changed_at": "2026-09-08", "summary": "Subaward total updated from $132.6M to $154.2M: the 5th and final GO-NORTH hub grant (mental health, $21.6M) confirmed approved."},
    {"state": "New York", "changed_at": "2026-09-08", "summary": "Status advanced from 'RFA issued' to 'subawards announced': $76.2M announced across 90 RCHI awards to 56 organizations."},
    {"state": "Oklahoma", "changed_at": "2026-09-08", "summary": "First subaward dollar figure recorded: ~$3.85M across 75+ named Community-Led Wellness Hub microgrant recipients."},
    {"state": "Connecticut", "changed_at": "2026-09-08", "summary": "Status corrected from 'admin structure named' to 'RFA issued': an earlier May 2026 NOFO (Rural Health Transformation IT Program) was found predating the previously-recorded event."},
]

# Federal-level (not state-specific) statutory/programmatic milestones for the
# Rural Health Transformation Program itself — the authorizing law, CMS's
# Notice of Funding Opportunity, application/award dates, the funds-obligation
# deadline, and reporting cadence. Same sourcing discipline as everything else
# here: every entry cites a source_url, and anything not confirmed on an
# official .gov primary source is marked "unverified" rather than stated as
# settled fact. category is one of: statute, application, award, obligation,
# reporting, other.
FEDERAL_MILESTONES = [
    {
        "title": "Rural Health Transformation Program established",
        "category": "statute",
        "start_date": "2025-07-04",
        "end_date": None,
        "source_url": "https://apply07.grants.gov/apply/opportunities/instructions/PKG00291485-instructions.pdf",
        "notes": (
            "Created by Section 71401 of Public Law 119-21 (the July 2025 reconciliation act), codified at "
            "42 U.S.C. § 1397ee(h). Establishes $50B over five budget periods, $10B available each, aligned to "
            "FY2026–FY2030. Per the NOFO: \"Baseline funding: We will distribute $25 billion equally among all "
            "approved States... Workload funding: We will distribute the other $25 billion based on the content "
            "and quality of your application and rural factors.\" No more than 10% of a state's allotment for a "
            "budget period may go to administrative costs (statutory)."
        ),
        "confidence": "confirmed",
    },
    {
        "title": "CMS Notice of Funding Opportunity (NOFO) released",
        "category": "application",
        "start_date": "2025-09-15",
        "end_date": None,
        "source_url": "https://www.cms.gov/newsroom/press-releases/cms-launches-landmark-50-billion-rural-health-transformation-program",
        "notes": "CMS opens the RHT Program application window (Opportunity CMS-RHT-26-001).",
        "confidence": "confirmed",
    },
    {
        "title": "Optional Letter of Intent deadline",
        "category": "application",
        "start_date": "2025-09-30",
        "end_date": None,
        "source_url": "https://apply07.grants.gov/apply/opportunities/instructions/PKG00291485-instructions.pdf",
        "notes": "Non-binding letter of intent, due 11:59pm ET, emailed to MAHARural@cms.hhs.gov. Not required to apply.",
        "confidence": "confirmed",
    },
    {
        "title": "State application deadline",
        "category": "application",
        "start_date": "2025-11-05",
        "end_date": None,
        "source_url": "https://www.cms.gov/newsroom/press-releases/all-50-states-seek-transform-rural-health-cms",
        "notes": "Full application due 11:59pm ET. All 50 states applied. One application period covers the entire five-year program — no separate planning-grant round.",
        "confidence": "confirmed",
    },
    {
        "title": "FY2026 awards announced to all 50 states",
        "category": "award",
        "start_date": "2025-12-29",
        "end_date": None,
        "source_url": "https://www.cms.gov/newsroom/press-releases/cms-announces-50-billion-awards-strengthen-rural-health-all-50-states",
        "notes": (
            "CMS's NOFO listed an expected award date of December 31, 2025; awards were announced two days "
            "early. First-year awards averaged ~$200M, ranging $147M–$281M per state."
        ),
        "confidence": "confirmed",
    },
    {
        "title": "Budget resubmission deadline",
        "category": "reporting",
        "start_date": "2026-01-30",
        "end_date": None,
        "source_url": "https://kffhealthnews.org/news/article/rural-health-transformation-state-distribution-technical-scores-variation-deadlines/",
        "notes": (
            "KFF Health News, citing the standard Notice of Award: \"States have until Jan. 30 to resubmit "
            "their budgets, and CMS then has 30 days to respond.\" Sourced from CMS's award-notice terms via "
            "KFF's reporting, not the NOFO document itself."
        ),
        "confidence": "confirmed",
    },
    {
        "title": "Annual reporting requirement",
        "category": "reporting",
        "start_date": "2025-12-29",
        "end_date": None,
        "source_url": "https://apply07.grants.gov/apply/opportunities/instructions/PKG00291485-instructions.pdf",
        "notes": (
            "Per the NOFO: recipients submit an annual non-competing continuation (NCC) application and an "
            "annual progress report to receive funding for each subsequent budget period, plus standard federal "
            "financial/FFATA reporting. The NOFO does not specify a separate quarterly reporting cadence — only "
            "annual reporting is stated explicitly."
        ),
        "confidence": "confirmed",
    },
    {
        "title": "Budget Period 1 ends / Budget Period 2 begins (approximate)",
        "category": "obligation",
        "start_date": "2026-10-31",
        "end_date": None,
        "source_url": "https://apply07.grants.gov/apply/opportunities/instructions/PKG00291485-instructions.pdf",
        "notes": (
            "Not a literal CMS-stated date — flagged unverified because it's our own calculation. The NOFO "
            "states budget periods run \"10 months for the first budget period and 12 months for each "
            "subsequent budget period,\" starting from the ~Dec 31, 2025 award date; 10 months out lands here. "
            "CMS does not spell out the exact day itself, so treat this as an approximate marker of when Year 2 "
            "scoring/funding activity begins, not a hard deadline."
        ),
        "confidence": "unverified",
    },
    {
        "title": "Deadline to spend FY2026 (Year 1) award funds",
        "category": "obligation",
        "start_date": "2027-09-30",
        "end_date": None,
        "source_url": "https://apply07.grants.gov/apply/opportunities/instructions/PKG00291485-instructions.pdf",
        "notes": (
            "Per the NOFO: \"For each budget period, recipients will have until the end of the following fiscal "
            "year to spend awarded funding.\" The first budget period is 10 months (the remainder align to "
            "FY2026–FY2030); federal fiscal years end September 30, so FY2026 funds must be spent by the end "
            "of FY2027. The NOFO does not spell out an exact day-of-month \"obligation\" cutoff separate from "
            "this spend deadline, so none is stated here."
        ),
        "confidence": "confirmed",
    },
    {
        "title": "Policy-action commitment deadline (clawback risk)",
        "category": "obligation",
        "start_date": "2027-12-31",
        "end_date": None,
        "source_url": "https://apply07.grants.gov/apply/opportunities/instructions/PKG00291485-instructions.pdf",
        "notes": (
            "Verbatim from the NOFO's violation-of-agreement section: \"Failure to finalize State policy actions "
            "proposed in your application by the end of calendar year 2027. States will have until the end of "
            "calendar year 2028 to enact the relevant policies for factors B.2 and B.4 [Health and lifestyle; "
            "Nutrition Continuing Medical Education].\" States that pledged policy changes (e.g. licensure "
            "compacts, scope-of-practice reform) to earn technical-score funding must actually enact them by "
            "this date or CMS recovers the associated funds."
        ),
        "confidence": "confirmed",
    },
    {
        "title": "Final deadline — unspent funds return to U.S. Treasury",
        "category": "obligation",
        "start_date": "2032-10-01",
        "end_date": None,
        "source_url": "https://apply07.grants.gov/apply/opportunities/instructions/PKG00291485-instructions.pdf",
        "notes": (
            "Verbatim from the NOFO: \"Any funding that is unexpended or unobligated as of October 1, 2032, "
            "shall be returned to the Treasury of the United States.\" Statutory hard backstop for the whole "
            "five-year, $50B program."
        ),
        "confidence": "confirmed",
    },
]

STATUS_TAXONOMY = [
    "plan approved",
    "admin structure named",
    "RFA issued",
    "subawards announced",
    "funds obligated",
]

# --- Expansion to the remaining 40 states (2026-09-02 research pass) ---
# See app/new_states_data.py for the full data and sourcing notes. Merged
# here via extend/update rather than hand-merged into the lists above so
# the original 10 states' entries stay untouched and easy to diff.
from new_states_data import (  # noqa: E402
    NEW_SOURCES, NEW_AWARDS, NEW_STATUS_EVENTS, NEW_DEADLINES,
    NEW_PILLARS, NEW_OVERVIEW,
)

SOURCES.extend(NEW_SOURCES)
AWARDS.extend(NEW_AWARDS)
STATUS_EVENTS.extend(NEW_STATUS_EVENTS)
DEADLINES.extend(NEW_DEADLINES)
STATE_PILLARS.update(NEW_PILLARS)

# Per-state override for updated_at, for states whose overview text was
# revised after the initial 2026-09-02 research pass (rather than bumping
# every state's date just because one field changed).
_UPDATED_AT_OVERRIDES = {
    "Hawaii": "2026-09-07",
    "Delaware": "2026-09-07",
    "Indiana": "2026-09-08",
    "Louisiana": "2026-09-08",
    "Nevada": "2026-09-08",
    "New Hampshire": "2026-09-08",
    "New York": "2026-09-08",
    "Oklahoma": "2026-09-08",
    "Connecticut": "2026-09-08",
}

for _state, _fields in NEW_OVERVIEW.items():
    STATE_OVERVIEW[_state] = {
        "emphasis": _fields["emphasis"],
        "applicant_profile": _fields["applicant_profile"],
        "contact_name": _fields["contact_name"],
        "contact_email": _fields["contact_email"],
        "contact_note": _fields["contact_note"],
        "updated_at": _UPDATED_AT_OVERRIDES.get(_state, "2026-09-02"),
    }
