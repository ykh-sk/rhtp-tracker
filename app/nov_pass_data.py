"""Supplemental RHTP updates from the Nov 10 follow-up sweep of Oct 1 - Nov 10, 2026 developments
that the earlier Nov 10 pass (commit 62abcd1) had not captured: named awards, solicitation
deadlines, and a few corrections. Merged into the tables at the bottom of seed_data.py, the same
way new_states_data.py is, so the earlier entries stay untouched and easy to diff.

Rules followed (README "Update policy"): sourced facts are appended as new dated rows, never edited
in place; every row's source was opened and read when marked 'confirmed'; anything seen only in a
search snippet or a page that could not be opened is 'unverified'. A new event never lowers a
state's stage, so sub-program solicitations carry the state's current stage ("subawards announced").
Year 2 award amounts (CMS table of Nov 9) are not modeled here — the tracker's award table is FY26.
"""

SA = "subawards announced"

STATUS_EVENTS_ADD = [
    # ---- Alabama ----
    {"state": "Alabama", "status": SA, "event_date": "2026-10-04",
     "source_url": "https://www.fox10tv.com/2026/10/04/mobile-area-health-systems-receive-grants-state-rural-health-program/",
     "notes": "FOX10 (Oct 4, 2026) names recipients and amounts from the second round: Alabama Community College System $20.6M (rural workforce pipeline); Alabama School of Healthcare Sciences $7.27M (residential high school, Demopolis); Infirmary Health $1.79M (maternal-fetal hub) and $1.37M (breast cancer network); University of South Alabama $1.63M (maternity network) and $164,450; Franklin Primary Health Center $534,937; Andalusia Health $305,428; Children's Hospital of Alabama $288,542. FLAG: the article lists only some of the 34 grants.",
     "confidence": "confirmed"},
    # ---- Delaware ----
    {"state": "Delaware", "status": SA, "event_date": "2026-10-14",
     "source_url": "https://news.delaware.gov/2026/10/14/delaware-announces-rural-health-transformation-funding-to-strengthen-physician-workforce/",
     "notes": "DHSS release (posted Oct 14, 2026): two physician-workforce programs for rural Kent and Sussex counties. (1) Medical-student educational awards through the Delaware Health Care Commission and Thomas Jefferson University's Sidney Kimmel Medical College: two awards of $70,000 each in year one ($140,000). (2) Residency housing and relocation awards: about $1.24M budgeted, roughly 61 awards averaging $20,000, for GME programs at Bayhealth, Beebe, ChristianaCare, Nemours and TidalHealth. Institutions are collecting applications now; 5-year rural service commitment. FLAG: the release lists no application deadlines and no named individual recipients. This is a solicitation, so the state stays at 'subawards announced'.",
     "confidence": "confirmed"},
    # ---- Nevada ----
    {"state": "Nevada", "status": SA, "event_date": "2026-11-10",
     "source_url": "https://www.gov.nv.gov/press-releases/nevada-announces-another-$27-million-in-awards-to-improve-rural-health-care/",
     "notes": "RE-CHECK (2026-11-10 is the verification date, not an announcement date): the Governor's Aug 6, 2026 release says Nevada \"has now awarded nearly $150 million in Rural Health Transformation Program awards\" supporting 158 projects across 17 counties, with final amounts possibly changing. This confirms the state's own cumulative claim that the Sept 2 unverified lead quoted. FLAG: the release gives no breakdown by initiative, so about $37M of the ~$150M is not itemized (the three itemized rounds total $112.9M).",
     "confidence": "confirmed"},
    # ---- Oklahoma ----
    {"state": "Oklahoma", "status": SA, "event_date": "2026-11-09",
     "source_url": "https://oklahoma.gov/health/news---events/newsroom/2026/oklahoma-receives-second-year-notice-of-award-for-rural-health-t.html",
     "notes": "OSDH release (Nov 9, 2026): CMS awarded $227,097,542.59 for Year 2 (budget period two); total financial assistance award printed as $450,574,491.21. Lists Year 1 milestones including \"Awarded over 500 organizations through direct funding and partnerships\" and mentions 29 RHTP programs. FLAG: gives no dollar total for subawards and does not say whether Year 1 funds are fully obligated.",
     "confidence": "confirmed"},
    # ---- Texas ----
    {"state": "Texas", "status": SA, "event_date": "2026-11-10",
     "source_url": "https://www.hhs.texas.gov/news/2026/11/gov-abbott-hhsc-announce-281-million-second-year-rural-texas-strong",
     "notes": "HHSC release (Nov 10, 2026): HHSC will receive $281 million for the second year of Rural Texas Strong. FLAG: the page gives no Year 2 initiative details, application dates or Year 1 award totals. HHSC's RHTP page shows its recipient-list spreadsheet \"Updated 11/5/2026\" (contents could not be read).",
     "confidence": "confirmed"},
    # ---- Wyoming ----
    {"state": "Wyoming", "status": SA, "event_date": "2026-10-23",
     "source_url": "https://www.barrasso.senate.gov/rural-health-transformation-awardees-highlight-key-components-of-federal-dollars/",
     "notes": "Sen. Barrasso's release (Oct 23, 2026): Gov. Gordon, Sen. Barrasso and WDH Director Johannson announced Year 1 awards with four hospital CEOs (Carbon, Johnson, Converse and Hot Springs counties) and say allocations, applications and awards were completed for Year 1 as of October 2026. This is the official source behind the CMS Oct 23 entry above. FLAG: no per-awardee amounts, and it does not say all funds are \"obligated\"; Barrasso: \"More funding will follow over the next four years.\"",
     "confidence": "confirmed"},
    {"state": "Wyoming", "status": SA, "event_date": "2026-10-26",
     "source_url": "https://wyofile.com/how-will-wyoming-spend-205m-in-federal-healthcare-money-on-rural-hospitals-first-responders-and-workforce-programs/",
     "notes": "WyoFile (published Oct 26, updated Oct 28) itemizes named amounts: Memorial Hospital of Carbon County $5.8M; Memorial Hospital of Converse County \"more than $5 million\"; Johnson County Hospital District $4.8M; Wyoming Innovation Partnership \"more than $35 million\" (fiscal agent); University of Wyoming $6.2M GME; University of Utah $9.3M GME; statewide telehealth specialist program $3.5M. Category totals: emergency care $91.8M, workforce $56.3M, Make Wyoming Healthy Again $38.6M, health technology $16.9M; $17.6M left over earmarked for EMS and labor and delivery via the Wyoming Hospital Association; WDH administration $1.3M (0.7%). FLAG: \"finalized its year-one funding obligations\" is the reporter's wording, not an official statement that all funds are obligated. Named amounts are partial and overlap the category totals, so no subaward total is recorded.",
     "confidence": "confirmed"},
]

DEADLINES_ADD = [
    {"state": "New Hampshire", "title": "FHC (GO-NORTH hub) Primary Care Access RFA — initial deadline",
     "start_date": "2026-10-15", "end_date": None, "source_url": "https://healthynh.org/initiatives/rural-health-transformation-program/",
     "notes": "5:00 PM ET. Rolling applications continue while funds last; initial cohort expected late October / early November, rolling cohorts notified within 45–60 days. No dollar amount printed. Info session was held Sept 2.",
     "confidence": "confirmed"},
    {"state": "New Hampshire", "title": "FHC (GO-NORTH hub) Critical Access and Acute Care Hospital RFA — priority cohort deadline",
     "start_date": "2026-11-12", "end_date": None, "source_url": "https://healthynh.org/initiatives/rural-health-transformation-program/",
     "notes": "5:00 PM ET; portal opens late October 2026, rolling after the priority cohort while funds last; initial cohort notified mid-December 2026. No dollar amount printed. FHC also lists a Home Health and Community Care RFA as \"upcoming\" (portal expected late October) and says its Technology & Digital Infrastructure RFA was withdrawn.",
     "confidence": "confirmed"},
    {"state": "Oklahoma", "title": "Community Paramedicine Consulting Services RFP — due",
     "start_date": "2026-11-18", "end_date": None, "source_url": "https://oklahoma.gov/content/sok-wcm/en/rhtp/rhtp-funding",
     "notes": "3:00 PM CST (OSDH funding page, last modified Oct 22, 2026). No amount printed.", "confidence": "confirmed"},
    {"state": "Oklahoma", "title": "OSU Tech Co-Op and consumer-facing tech enrollment forms — due",
     "start_date": "2026-12-01", "end_date": None, "source_url": "https://oklahoma.gov/content/sok-wcm/en/rhtp/rhtp-funding",
     "notes": "Provider, needs and readiness forms due Dec 1, 2026; the Clinic/Site Profile Survey is due Dec 15, 2026.", "confidence": "confirmed"},
    {"state": "Oklahoma", "title": "OHCA EHR Expansion RFI (Year 1) — due",
     "start_date": "2026-12-01", "end_date": None, "source_url": "https://oklahoma.gov/content/sok-wcm/en/rhtp/rhtp-funding",
     "notes": "Active request for information; no amount printed.", "confidence": "confirmed"},
    {"state": "Oklahoma", "title": "OHCA HIE & EHR Assistance (Year 1) application — due",
     "start_date": "2026-12-31", "end_date": None, "source_url": "https://oklahoma.gov/content/sok-wcm/en/rhtp/rhtp-funding",
     "notes": "Active application; no amount printed.", "confidence": "confirmed"},
    {"state": "Texas", "title": "Initiative 2 (Rural Texas Patients in the Driver's Seat) — application deadline (estimated)",
     "start_date": "2027-01-12", "end_date": None, "source_url": "https://pfd.hhs.texas.gov/rural-health-transformation-program",
     "notes": "ALL DATES ON THE HHSC PAGE ARE ESTIMATES: program start Nov 9, 2026; notice of award Mar 8, 2027; contracts routed Jul 6, 2027. No amount printed.", "confidence": "confirmed"},
    {"state": "Texas", "title": "Initiative 3 (Lonestar Advanced AI and Telehealth) — application deadline (estimated)",
     "start_date": "2027-01-12", "end_date": None, "source_url": "https://pfd.hhs.texas.gov/rural-health-transformation-program",
     "notes": "Estimated: program start Nov 25, 2026; notice of award Mar 29, 2027; contracts Jul 19, 2027. No amount printed.", "confidence": "confirmed"},
    {"state": "Texas", "title": "Initiative 5 (Unified Care Infrastructure and Rural Cyber Protection) — application deadline (estimated)",
     "start_date": "2027-01-19", "end_date": None, "source_url": "https://pfd.hhs.texas.gov/rural-health-transformation-program",
     "notes": "Estimated: program start Dec 1, 2026; notice of award Mar 5, 2027; contracts Aug 31, 2027. Initiative 6 Part 2 (Infrastructure and Capital Investments) shows a program start of Nov 1, 2027 with other dates TBD. HHSC says procurements will be announced via GovDelivery, ESBD and its Grants Page; the page prints no opening dates.", "confidence": "confirmed"},
]

# Field overrides for the existing FY26 award row of a state (subawards figure + its label).
AWARD_OVERRIDES = {
    "Ohio": {
        "subawards_amount": 160150000,
        "subawards_label": "FLOOR figure, no official aggregate published: $10M Ohio University + $3.15M pharmacy connectivity + $92M CMS/DeWine Oct 16–19 (networks $31.4M, maternal care $30.3M, hospitals $30.3M) + \"over $55 million\" DeWine Nov 2–3 (over $18M OhioSEE, over $17M OhioDENTAL, over $20M school-based health centers). The $55M is printed as \"over\"; the categories appear distinct but overlap was not verified",
    },
}

COMMENTARY_ADD = [
    {"title": "How will Wyoming spend $205M in federal healthcare money? On rural hospitals, first responders and workforce programs",
     "source_name": "WyoFile", "url": "https://wyofile.com/how-will-wyoming-spend-205m-in-federal-healthcare-money-on-rural-hospitals-first-responders-and-workforce-programs/",
     "published_date": "2026-10-26", "state": "Wyoming", "angle": "news",
     "summary": "Details Wyoming's finalized Year 1 spending by category with named hospital, EMS, university and workforce awardees, and the state's hope for 'some expansion' in Year 2."},
]

CHANGELOG_ADD = [
    {"state": "Alabama", "changed_at": "2026-11-10", "summary": "Named second-round recipients added to the timeline (Oct 4 FOX10: e.g. Alabama Community College System $20.6M, Infirmary Health, University of South Alabama)."},
    {"state": "Delaware", "changed_at": "2026-11-10", "summary": "Physician-workforce solicitations added (Oct 14 DHSS: medical-student awards and ~$1.24M residency housing/relocation awards)."},
    {"state": "New Hampshire", "changed_at": "2026-11-10", "summary": "Hub RFA deadlines added: hospital RFA priority cohort due Nov 12; primary care RFA initial deadline was Oct 15."},
    {"state": "Nevada", "changed_at": "2026-11-10", "summary": "State's cumulative claim confirmed on the official Aug 6 release: nearly $150M across 158 projects (about $37M not itemized)."},
    {"state": "Ohio", "changed_at": "2026-11-10", "summary": "Subaward total raised from $105.2M to a $160.2M floor by adding the $55M+ announced Nov 2–3 (children's health, dental, school-based care); no official aggregate exists."},
    {"state": "Oklahoma", "changed_at": "2026-11-10", "summary": "Year 2 award of $227.1M noted; four open solicitation deadlines added (Nov 18 – Dec 31)."},
    {"state": "Texas", "changed_at": "2026-11-10", "summary": "Year 2 award of $281M announced (Nov 10); estimated Year 2 application dates for Initiatives 2, 3 and 5 added (Jan 2027)."},
    {"state": "Wyoming", "changed_at": "2026-11-10", "summary": "Named Year 1 awards added from WyoFile (Oct 26): hospitals, university GME and category totals; official Oct 23 release linked."},
]

# States whose overview 'updated_at' is bumped because a material change was recorded above.
TOUCHED_STATES = {"Alabama", "Delaware", "New Hampshire", "Nevada", "Ohio", "Oklahoma", "Texas", "Wyoming"}

# ============================ batches 2 and 6 (AK, FL, KS, MN, NJ, OR, UT / CO, IL, MD, NE, ND, SD, WI) ============================
STATUS_EVENTS_ADD += [
    {"state": "Alaska", "status": SA, "event_date": "2026-10-04",
     "source_url": "https://www.adn.com/alaska-journal/news/2026/10/04/alaska-to-launch-second-round-of-funding-for-federal-rural-healthcare-program/",
     "notes": "Anchorage Daily News (Oct 4, 2026): Year 2 applications opened Sept 30 while public comment on the Year 2 evaluation criteria stayed open until Oct 9; Year 2 focus areas are pay-for-value, care coordination and EMS. As of the article: $242.6M to 250 projects (median award $421,000), $31M to 13 organizations for value-based care projects, nearly 1,800 proposals received. FLAG: the Year 2 criteria were not final when the portal opened.",
     "confidence": "confirmed"},
    {"state": "Maryland", "status": SA, "event_date": "2026-09-14",
     "source_url": "https://health.maryland.gov/pophealth/Pages/Rural-Health-Transformation-Program.aspx",
     "notes": "MDH's RHTP page (stamped last updated 09-14-2026) states \"$163.7 million in Budget Period 1 subawards,\" of which $134.8 million goes through competitive procurement. FLAG: this is a planned allocation, not a list of announced awards. The table amounts printed on the page sum to only $107.8M (some rows carry no amount), and the tracker's $96.4M is the narrower sum of awards announced so far.",
     "confidence": "confirmed"},
    {"state": "Nebraska", "status": SA, "event_date": "2026-10-10",
     "source_url": "https://www.wowt.com/2026/10/10/dr-oz-trump-medicaid-director-nebraska-root-state-rural-health-program-big-red/",
     "notes": "WOWT (Oct 10, 2026): state officials say $177 million of the $218.5M first-year money is \"deployed\" (a late-July update put awards at about $98 million). Cited counts: about 200 rural community health workers, 172 recruitment/retention award contracts, 45 facilities with remote monitoring (68 devices), 28 rural pharmacies, 35 farmers and food producers. FLAG: the article reports no \"obligated\" figure, and Oz mentioned a possible clawback tied to the first-year rollout.",
     "confidence": "confirmed"},
    {"state": "Nebraska", "status": SA, "event_date": "2026-10-23",
     "source_url": "https://nebraskapublicmedia.org/en/news/news-articles/applications-open-for-emerging-rural-health-technology-fund-through-nebraska-dhhs/",
     "notes": "Nebraska Rural Health Technology Catalyst Fund (NETECH, run by Invest Nebraska for DHHS) opened Cohort 1 applications Oct 23, closing Nov 9. Initial target awards $250,000-$1M, maximum $3M per company, milestone-based; described as $100M over five years within the RHTP allocation. This is a solicitation, so the state stays at 'subawards announced'. nebraskaruralhealthtech.com/apply says Cohort 1 is closed and under review.",
     "confidence": "confirmed"},
    {"state": "Oregon", "status": SA, "event_date": "2026-09-30",
     "source_url": "https://content.govdelivery.com/accounts/ORHA/bulletins/42d438c",
     "notes": "OHA bulletin (Sept 30, 2026): about $2M for clinical supervision and psychiatric mental health nurse practitioner preceptorships at about 12 rural community mental health programs. FLAG: amounts and budgets are still being finalized and no recipients are named.",
     "confidence": "confirmed"},
    {"state": "Oregon", "status": SA, "event_date": "2026-10-02",
     "source_url": "https://content.govdelivery.com/accounts/ORHA/bulletins/42d4594",
     "notes": "OHA bulletin (Oct 2, 2026): about $7.3M in direct RHTP funding for rural FQHCs (34 eligible), about $500,000 of it to the Oregon Primary Care Association for grant management and technical assistance, the remainder to participating FQHCs. FLAG: amounts are still being finalized, awards depend on OHA approving each project plan, and no FQHC is named.",
     "confidence": "confirmed"},
    {"state": "Utah", "status": "RFA issued", "event_date": "2026-10-23",
     "source_url": "https://dhhs.utah.gov/ruralhealth/funding-opportunities",
     "notes": "Two more solicitations opened Oct 23, 2026, both closing Nov 20 at 5:00 PM MDT: (1) the UETN SPRINT Consortium for SUPPORT 6.1-6.5 and LINCS 7.1-7.2, and (2) SHIFT 3.1, RISE 2.5, FAST 4.2 and FAST 4.3 through the Utah Hospital Association. Year 1 component amounts printed include SHIFT 3.1 $26.3M, FAST 4.2 $9.0M, FAST 4.3 $3.0M, RISE 2.5 $9,397,152, SUPPORT 6.1 $9.4M. FLAG: the page lists no awardees, and its layout makes some date pairings uncertain.",
     "confidence": "confirmed"},
    {"state": "Wisconsin", "status": "RFA issued", "event_date": "2026-10-13",
     "source_url": "https://www.dhs.wisconsin.gov/rhtp/index.htm",
     "notes": "DHS RHTP page (revised Oct 13, 2026) lists every application window as closed: dental ($10M planned), rural technology (up to $61M in round 1; only organizations named in the CMS application are eligible), community health workers ($20M planned for year one), care coordination (up to $10M in 2026 for 6-month planning), plus DWD's WIG: HEART ($4.9M year one). DHS 2026 grant amounts total \"$101 million.\" FLAG: no awardees are named and every amount is contingent on CMS approval; the tracker's earlier $40M figure omitted the technology fund.",
     "confidence": "confirmed"},
]

DEADLINES_ADD += [
    {"state": "Alaska", "title": "Year 2 Fall 2026 funding cycle applications",
     "start_date": "2026-09-30", "end_date": "2026-10-28", "source_url": "https://health.alaska.gov/en/education/rural-health-transformation-program/for-rhtp-applicants/",
     "notes": "Closed Wed Oct 28 at 11:59 PM Alaska time. DOH \"intends to award approximately $75 million in total\" in this cycle (Planning and Implementation pathways, six initiatives, up to 5 applications per organization); earliest award start Jan 1, 2027. Year 1 continuation requests and Category J facility renovation requests are excluded until Spring 2027.",
     "confidence": "confirmed"},
    {"state": "Kansas", "title": "Year 2 NEMT and CHW + Accountable Food is Medicine RFAs — due",
     "start_date": "2026-10-16", "end_date": "2026-11-18", "source_url": "https://www.kdhe.ks.gov/DocumentCenter/View/60870/261016---NEMT-RFA-PDF",
     "notes": "UNVERIFIED: KDHE pages returned errors, so this rests on search-result snippets of the KDHE newsflash and RFA PDFs. Both RFAs reportedly opened Oct 16 and close Nov 18, 2026; CHW+AFIM awardees expected by Dec 14, 2026. Amounts are stated as pending CMS approval of the Year 2 budget.",
     "confidence": "unverified"},
    {"state": "Nebraska", "title": "Rural Health Technology Catalyst Fund (NETECH) Cohort 1 applications",
     "start_date": "2026-10-23", "end_date": "2026-11-09", "source_url": "https://nebraskapublicmedia.org/en/news/news-articles/applications-open-for-emerging-rural-health-technology-fund-through-nebraska-dhhs/",
     "notes": "Closed Nov 9 per nebraskaruralhealthtech.com/apply. No Cohort 2 date is published.", "confidence": "confirmed"},
    {"state": "Utah", "title": "UETN SPRINT (SUPPORT/LINCS) and Utah Hospital Association (SHIFT 3.1/RISE 2.5/FAST 4.2-4.3) solicitations — due",
     "start_date": "2026-10-23", "end_date": "2026-11-20", "source_url": "https://dhhs.utah.gov/ruralhealth/funding-opportunities",
     "notes": "Both close Nov 20, 2026 at 5:00 PM MDT.", "confidence": "confirmed"},
]

AWARD_OVERRIDES["Alaska"] = {
    "subawards_amount": 248976548,
    "subawards_label": "Sum of \"Award Amount (Preliminary)\" across all 254 rows of DOH's published Notice of Intent to Award spreadsheet ($248,976,547.51); consistent with DOH's Oct 22 \"just under $249 million to 254 projects.\" DOH says subaward budgets are still being finalized, so amounts may change",
}

COMMENTARY_ADD += [
    {"title": "Congress gave Nebraska millions for rural health care. Most isn't getting to rural hospitals", "source_name": "Flatwater Free Press (via WOWT)",
     "url": "https://www.wowt.com/2026/11/04/congress-gave-nebraska-millions-rural-healthcare-most-isnt-getting-rural-hospitals/?outputType=amp",
     "published_date": "2026-11-04", "state": "Nebraska", "angle": "investigative",
     "summary": "Flatwater's analysis of state data (through end of August) found Nebraska had earmarked $153 million, with about 18% ($28M) going to critical access and rural emergency hospitals, at least 11 such hospitals receiving nothing, and one hospital denied $828,231."},
    {"title": "Alaska to launch second round of funding for federal rural healthcare program", "source_name": "Anchorage Daily News / Alaska Journal of Commerce",
     "url": "https://www.adn.com/alaska-journal/news/2026/10/04/alaska-to-launch-second-round-of-funding-for-federal-rural-healthcare-program/",
     "published_date": "2026-10-04", "state": "Alaska", "angle": "news",
     "summary": "Reports that Year 2 applications opened before the evaluation criteria were final, with the state hospital association's Jared Kosin criticizing the overlapping timelines and the five-year program length."},
]

CHANGELOG_ADD += [
    {"state": "Alaska", "changed_at": "2026-11-10", "summary": "Subaward total revised from $242.6M to $249.0M (sum of DOH's published Notice of Intent to Award spreadsheet, 254 projects); Year 2 fall cycle (~$75M, closed Oct 28) added."},
    {"state": "Maryland", "changed_at": "2026-11-10", "summary": "Official aggregate recorded: MDH states $163.7M in Budget Period 1 subawards (planned allocation, not all announced); recorded awards total stays $96.4M."},
    {"state": "Nebraska", "changed_at": "2026-11-10", "summary": "State officials' $177M 'deployed' (Oct 10) and the $100M-over-5-years NETECH tech fund (applications Oct 23 - Nov 9) added."},
    {"state": "Oregon", "changed_at": "2026-11-10", "summary": "Two OHA bulletins added: ~$2M for mental-health preceptorships (Sept 30) and ~$7.3M for rural FQHCs (Oct 2), amounts still being finalized."},
    {"state": "Utah", "changed_at": "2026-11-10", "summary": "Two solicitations opened Oct 23 (UETN SPRINT; Utah Hospital Association SHIFT/RISE/FAST), both due Nov 20."},
    {"state": "Wisconsin", "changed_at": "2026-11-10", "summary": "DHS page (Oct 13) shows all windows closed and about $101M in 2026 grants planned (technology fund up to $61M); no awardees named."},
    {"state": "Kansas", "changed_at": "2026-11-10", "summary": "Unverified: two more Year 2 RFAs (NEMT; CHW + Food is Medicine) reportedly open Oct 16 - Nov 18."},
]

TOUCHED_STATES |= {"Alaska", "Maryland", "Nebraska", "Oregon", "Utah", "Wisconsin", "Kansas"}

# ============================ batches 3, 4 and 5 (AZ, KY, ... / AR, MO, VA, ... / CA, ID, ME, MT, NC, ...) ============================
STATUS_EVENTS_ADD += [
    {"state": "Arizona", "status": "RFA issued", "event_date": "2026-09-18",
     "source_url": "https://www.azahcccs.gov/AHCCCS/Initiatives/RHTP/",
     "notes": "AHCCCS RHTP page lists two Governor's Office of Economic Opportunity solicitations released Sept 18, 2026: Provider Retention and Well-Being Microgrant Program ($1,000,000) and Transition to Practice Program ($3,000,000); questions due Oct 9, applications due Oct 23. The page also lists eight other Year 1 solicitations released Jul 10 - Aug 3 (e.g. Telehealth $17,000,000, Medical Diagnostic Equipment/EHR $30,000,100.32, Rural Health Innovative Care Pilot $21,000,000, Patient Navigator $5,000,000). FLAG: the page posts no awards or obligation totals, and its \"fully obligated by Oct 30\" is a plan, not a confirmation.",
     "confidence": "confirmed"},
    {"state": "Kentucky", "status": SA, "event_date": "2026-10-20",
     "source_url": "https://apps.legislature.ky.gov/CommitteeDocuments/366/44341/10%2020%202026%203.%20Walton%20RHTP%20Update%20CMS.pdf",
     "notes": "Tom Walton's \"Kentucky Rural Health Transformation October 2026 Update\" to the Interim Joint Committee on Health Services (Oct 20, 2026) shows \"Total Awarded\" by initiative: PoWERing Rural Maternal & Infant Health $4,616,006; Rapid Response to Recovery $6,301,480; Rooted in Health $6,555,540; Chronic Care Innovation $2,409,013; Workforce Development $2,500,000, broken out across the 15 Area Development Districts, plus a separate list of statewide activities under contract (UK, UofL, KPCA, KHIE, AHECs and others). CMS \"anticipates issuing a Notice of Award on October 30, 2026\" and Budget Period 2 begins Oct 31. FLAG: text was extracted from a compressed PDF, so line-item alignment is approximate; the deck states no all-in total and does not say Year 1 is fully obligated.",
     "confidence": "confirmed"},
    {"state": "Arkansas", "status": SA, "event_date": "2026-10-12",
     "source_url": "https://www.uaex.uada.edu/media-resources/news/2026/october/10-12-2026-ark-rural-health-grant.aspx",
     "notes": "University of Arkansas Division of Agriculture (Oct 12, 2026): the Cooperative Extension Service received $2.65M for \"ROOT of Rural Health\" (childhood wellness, chronic disease, health literacy), funding period Oct 1, 2026 - Sept 30, 2027, handed over at a Sept 24 Governor's Mansion ceremony. This is one named award inside the already-recorded $54.6M second round; no new total is stated.",
     "confidence": "confirmed"},
    {"state": "Missouri", "status": SA, "event_date": "2026-10-13",
     "source_url": "https://content.govdelivery.com/accounts/MODSS/bulletins/42d24b6",
     "notes": "DSS bulletin (Oct 13, 2026): $1.46M to Kids Win Missouri, with the Children's Trust Fund, to expand the Child Care Works program for rural health employers. DSS's same-day update also announces a certified nurse midwife training partnership with the University of Missouri Sinclair School of Nursing (targeting a Fall 2029 opening; no dollar amount listed).",
     "confidence": "confirmed"},
    {"state": "Missouri", "status": SA, "event_date": "2026-10-29",
     "source_url": "https://dss.mo.gov/mhd/rural-health",
     "notes": "DSS program page lists Rural Healthcare Workforce funding (about $11M) posted 10/29/2026: providers submit proposals through their ToRCH Care Hub coordinator in a Nov 2-22 window, each of 27 Hubs allocated about $412,000 over two program years, contingent on CMS Year 2 approval (informational webinar Nov 12). This is a solicitation, so the state stays at 'subawards announced'. FLAG: the same page prints about $39.4M for the Smart Growth and Service Line Modernization awards, while CMS's Oct 30 release says $39.7M for 26 providers; neither names awardees.",
     "confidence": "confirmed"},
    {"state": "Virginia", "status": SA, "event_date": "2026-10-02",
     "source_url": "https://www.vhcf.org/2026/10/02/virginia-takes-another-step-in-transforming-rural-health-care-through-major-technology-investments/",
     "notes": "Virginia Health Care Foundation (administering for DMAS) announced its first RHTP awards: $14.39M across 25 awards under Provider Interoperability: network capacity 6 awards $2.895M; EHR modernization 5 awards $2.245M; cybersecurity 6 awards $2.105M; data exchange 8 awards $7.145M. Named recipients include Ballad Health $2.0M, Eastern Shore Rural Health System $2.0M, Sentara Health $1.7M, Virginia Community Healthcare Association $1.5M and Valley Health System $1.165M and $835K. A new Interoperability RFA is expected in March 2027.",
     "confidence": "confirmed"},
    {"state": "Virginia", "status": SA, "event_date": "2026-10-16",
     "source_url": "https://www.vhcf.org/2026/10/16/vhcf-invests-8-6-million-to-strengthen-rural-health-care-practices-across-virginia/",
     "notes": "VHCF: $8.6M across 23 awards to 21 organizations under Provider Productivity (digital tools such as AI decision support). Named awards include Ballad, Carilion, Sentara, Valley Health and VCU Health at $1.0M each; Buchanan General $418K and $121K; Central Virginia Health Services $504K. The listed awards sum to $8,644,000, matching the headline. The release calls it nearly $23M in October technology investments together with the Oct 2 round. FLAG: it is unclear whether this falls inside the $122M CMS reported as disbursed on Aug 28, so the recorded total is unchanged.",
     "confidence": "confirmed"},
    {"state": "California", "status": SA, "event_date": "2026-10-26",
     "source_url": "https://hcai.ca.gov/wp-content/uploads/2026/10/CalRHT_BP1_Tribal_Set_Aside_RFA_v1.4-FINAL.pdf",
     "notes": "HCAI Budget Period 1 Tribal Set-Aside RFA (document dated Oct 21, 2026): application window Oct 26 - Nov 20, 2026 at 3 PM PT; $11.65 million, entire amount committed to eligible Tribal Health Programs. Award = $200,000 base per rural Tribal Health Program plus a per-site amount (the balance of the $11.65M after bases); $100,000 base for non-rural. HCAI's FAQ describes it as noncompetitive. This is a solicitation, so the state stays at 'subawards announced'.",
     "confidence": "confirmed"},
    {"state": "Idaho", "status": SA, "event_date": "2026-10-29",
     "source_url": "https://govtech.com/security/cybersecurity-is-among-beneficiaries-in-186m-idaho-award",
     "notes": "GovTech (Oct 29, 2026) names additional subgrants beyond those in the CMS Oct 28 entry: Bonner General Health $5.8 million total; St. Mary's Health (Cottonwood) $4.8 million; a mobile dental clinic (Kootenai, Bonner and Benewah counties) $1.53 million. FLAG: no total count is given; the article says the full list is on the DHW site.",
     "confidence": "confirmed"},
    {"state": "Idaho", "status": SA, "event_date": "2026-11-03",
     "source_url": "https://healthandwelfare.idaho.gov/providers/rural-health-transformation-program-grant/funding-opportunities-rural-health",
     "notes": "DHW funding-opportunities page (last updated Nov 3, 2026) links a \"list of awardees as of Oct. 16\" (PDF not opened) and says all Year 1 funding opportunities are closed (last closings Sept 17-21). FLAG: the page states no obligated total or award count; DHW's about page lists \"Oct. 30, 2026: All Year 1 funds obligated\" as a milestone, not as a completion statement, so the stage is not advanced.",
     "confidence": "confirmed"},
    {"state": "Maine", "status": SA, "event_date": "2026-10-09",
     "source_url": "https://www.mainepublic.org/health/2026-10-09/penobscot-community-health-care-avoids-bankruptcy-with-2-8-million-from-rural-health-program",
     "notes": "Maine Public (Oct 9, 2026): Penobscot Community Health Care says it is avoiding imminent bankruptcy after $2.8 million from Maine's RHTP, for a transition to a new EMR system and alternative payment models (it had said in late August it needed $3 million). FLAG: the article does not say whether this is a grant, which RHTP pool it came from, or what conditions apply.",
     "confidence": "confirmed"},
    {"state": "Montana", "status": SA, "event_date": "2026-10-13",
     "source_url": "https://dphhs.mt.gov/RuralHealthTransformationProgram/Grants",
     "notes": "DPHHS Grants page lists the FY26 Community Integrated Health Pilot Site Grant Application (opened Sept 1, closed Sept 15, 2026) as \"Awarded Oct. 13, 2026,\" $3.63 million. This is DPHHS's award date for the amount CMS publicized on Oct 16. FLAG: the page does not name the agencies.",
     "confidence": "confirmed"},
    {"state": "North Carolina", "status": SA, "event_date": "2026-10-07",
     "source_url": "https://www.ncdhhs.gov/news/press-releases/2026/10/07/governor-stein-ncdhhs-announce-more-17-million-investment-mental-health-services-through-north",
     "notes": "NCDHHS (Oct 7, 2026): \"more than $17 million\" for mental health: CCBHCs $4M to three unnamed LME/MCOs; MOUD units $3M (Graham, Rutherford, Cumberland, Bertie and Columbus counties); MORES teams $4M; first-episode psychosis $3M; Rural Crisis Partnerships $2.9M; NC MATTERS $800K per year. FLAG: recipients are mostly unnamed, the table lines sum to about $17.7M, and the release gives no total; this wave is outside the recorded $134.7M.",
     "confidence": "confirmed"},
]

DEADLINES_ADD += [
    {"state": "Arizona", "title": "AOEO Provider Retention and Well-Being Microgrant Program ($1,000,000) — applications due",
     "start_date": "2026-09-18", "end_date": "2026-10-23", "source_url": "https://www.azahcccs.gov/AHCCCS/Initiatives/RHTP/",
     "notes": "Questions were due Oct 9, 2026.", "confidence": "confirmed"},
    {"state": "Arizona", "title": "AOEO Transition to Practice Program ($3,000,000) — applications due",
     "start_date": "2026-09-18", "end_date": "2026-10-23", "source_url": "https://www.azahcccs.gov/AHCCCS/Initiatives/RHTP/",
     "notes": "Questions were due Oct 9, 2026. Other Year 1 solicitations on the same page closed Aug 7 - Aug 31, 2026.", "confidence": "confirmed"},
    {"state": "California", "title": "CalRHT Budget Period 1 Tribal Set-Aside applications (noncompetitive, $11.65M)",
     "start_date": "2026-10-26", "end_date": "2026-11-20", "source_url": "https://hcai.ca.gov/wp-content/uploads/2026/10/CalRHT_BP1_Tribal_Set_Aside_RFA_v1.4-FINAL.pdf",
     "notes": "Closes 3 PM PT. Questions: info@calruralhealth.org.", "confidence": "confirmed"},
    {"state": "Kentucky", "title": "Rural Community Hub Lead RFA (Foundation for a Healthy Kentucky) — complete-RFA deadline",
     "start_date": "2026-12-18", "end_date": None, "source_url": "https://healthy-ky.org/rch",
     "notes": "6:00 PM EDT. The application portal \"will be posted here in mid-November\" (no exact date). Martin County Health Department (Big Sandy), Lake Cumberland District Health Department and Purchase District Health Department are listed as selected hub leads, with no printed dates.", "confidence": "confirmed"},
    {"state": "Missouri", "title": "Rural Healthcare Workforce funding (~$11M): hub proposal window",
     "start_date": "2026-11-02", "end_date": "2026-11-22", "source_url": "https://dss.mo.gov/mhd/rural-health",
     "notes": "Leadership Board review Nov 23 - Dec 7; Hub Anchor submits an aggregated proposal by Dec 7; review, approval and participation agreements Dec 7-18, to finish by CMS's Dec 31 deadline. Informational webinar Nov 12, 2-3 PM CT.", "confidence": "confirmed"},
    {"state": "Montana", "title": "FY26 DPHHS Community Integrated Health Pilot Site Grant application",
     "start_date": "2026-09-01", "end_date": "2026-09-15", "source_url": "https://dphhs.mt.gov/RuralHealthTransformationProgram/Grants",
     "notes": "Awarded Oct 13, 2026, $3.63 million.", "confidence": "confirmed"},
    {"state": "Montana", "title": "DPHHS EMS Equipment Grant application",
     "start_date": "2026-07-16", "end_date": "2026-08-15", "source_url": "https://dphhs.mt.gov/RuralHealthTransformationProgram/Grants",
     "notes": "Awarded Sept 29, 2026, $8.7 million (already in the timeline; the application dates were missing).", "confidence": "confirmed"},
]

AWARD_OVERRIDES["Missouri"] = {
    "subawards_amount": 86760000,
    "subawards_label": "$45.6M (Sept 22 CMS/DSS) + $39.7M for 26 providers per CMS (Oct 30; DSS's own page prints about $39.4M; recipients not named) + $1.46M Kids Win Missouri (DSS, Oct 13). Left out: the $732,660.43 Missouri Doula Association award (DSS release, undated) and ToRCH hub/workforce funds not yet awarded. No official aggregate is published; possible double-counting is not ruled out",
}
AWARD_OVERRIDES["Kentucky"] = {
    "subawards_amount": 22382039,
    "subawards_label": "FLOOR, not a total: sum of the five per-initiative \"Total Awarded\" figures on slides 9-15 of the Oct 20, 2026 legislative update (4,616,006 + 6,301,480 + 6,555,540 + 2,409,013 + 2,500,000). Excludes the statewide activities under contract (slides 16-17) and the Rural Community Hub lead awards. No official all-in total is published",
}

COMMENTARY_ADD += [
    {"title": "Arizona will get more than $30M less from federal rural healthcare program than expected", "source_name": "KJZZ",
     "url": "https://www.kjzz.org/the-show/2026-10-06/arizona-will-get-more-than-30m-less-from-federal-rural-healthcare-program-than-expected",
     "published_date": "2026-10-06", "state": "Arizona", "angle": "news",
     "summary": "University of Arizona's Center for Rural Health director Dan Derksen says Arizona got about $167M a year versus the roughly $200M requested, that awards are expected within weeks, and that Medicaid changes could raise uncompensated care for rural providers."},
]

CHANGELOG_ADD += [
    {"state": "Arizona", "changed_at": "2026-11-10", "summary": "Two Governor's Office solicitations added ($1M microgrants, $3M transition-to-practice; both due Oct 23); still no awards or obligation total posted."},
    {"state": "Kentucky", "changed_at": "2026-11-10", "summary": "Stage advanced to 'subawards announced': Oct 20 legislative update shows $22.4M awarded across five initiatives (a floor; statewide contracts excluded); hub-lead RFA due Dec 18."},
    {"state": "Arkansas", "changed_at": "2026-11-10", "summary": "Named award added: Cooperative Extension Service $2.65M 'ROOT of Rural Health' (inside the recorded second round)."},
    {"state": "Missouri", "changed_at": "2026-11-10", "summary": "Subaward total raised from $85.3M to $86.8M (+$1.46M Kids Win, Oct 13); ~$11M workforce proposal window (Nov 2-22) added."},
    {"state": "Virginia", "changed_at": "2026-11-10", "summary": "VHCF's first awards added: $14.39M (25 awards, Oct 2) and $8.64M (23 awards, Oct 16) with named recipients; recorded total unchanged because overlap with the $122M disbursement is unclear."},
    {"state": "California", "changed_at": "2026-11-10", "summary": "Tribal Set-Aside RFA added ($11.65M, noncompetitive, applications Oct 26 - Nov 20)."},
    {"state": "Idaho", "changed_at": "2026-11-10", "summary": "Additional named subgrants added (Bonner General $5.8M, St. Mary's Health $4.8M, mobile dental $1.53M); DHW lists all Year 1 funding opportunities as closed."},
    {"state": "Maine", "changed_at": "2026-11-10", "summary": "Named award added: Penobscot Community Health Care $2.8M (Oct 9 report)."},
    {"state": "Montana", "changed_at": "2026-11-10", "summary": "DPHHS award date for the $3.63M community integrated health pilot corrected to Oct 13 (CMS publicized it Oct 16)."},
    {"state": "North Carolina", "changed_at": "2026-11-10", "summary": "Oct 7 mental-health wave added: 'more than $17 million' across CCBHCs, MOUD units, MORES teams and crisis partnerships (outside the recorded $134.7M)."},
]

TOUCHED_STATES |= {"Arizona", "Kentucky", "Arkansas", "Missouri", "Virginia", "California", "Idaho", "Maine", "Montana", "North Carolina"}
