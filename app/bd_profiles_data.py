"""BD profiles for the Health Systems map: a taxonomy (category + strategy signals) and a
one-line editorial note per system, merged in from the standalone "Health System Atlas".

PROVENANCE — read before trusting anything here. Unlike health_systems_data.py, these rows have
NO per-row citation. They were compiled by Claude from general public knowledge (Sept 2026) and
every row is stored with confidence='unverified'. Hospital counts, ownership, HQ and tier live in
health_systems_data.py (sourced); this file only adds category / strategy signals / a note.
Where an Atlas system matches a curated operator (OPERATOR_CROSSWALK) the profile attaches to that
operator and the operator's sourced fields win; the rest render as their own "profile only" pins.

Taxonomy:
  category  academic | faith | secular | forprofit | payerprovider | public | specialty |
            network | association | tribal | university   (the last four are not hospital systems)
  strategy  venture_arm | digital_pilot | vbc_leader | rural_focus | research_intensive |
            health_equity | limited_innovation
"""

import re

BASIS = (
    "Compiled by Claude from general public knowledge (Health System Atlas draft, Sept 2026). "
    "No per-row citation — verify before relying on it."
)

CATEGORIES = {
    "academic": "Academic Medical Center",
    "faith": "Faith-Based Nonprofit",
    "secular": "Secular Nonprofit",
    "forprofit": "Investor-Owned (For-Profit)",
    "payerprovider": "Payer-Provider Integrated",
    "public": "Public / Safety-Net",
    "specialty": "Specialty (Peds / Oncology)",
    "network": "Hospital network / alliance",
    "association": "Association / intermediary",
    "tribal": "Tribal / Indian health",
    "university": "University",
    "fqhc": "Community health center (FQHC)",
    "homehealth": "Home health agency",
    "hospital": "Community hospital",
}

STRATEGY_TAGS = {
    "venture_arm": "Venture / innovation arm",
    "digital_pilot": "Digital health pilots",
    "vbc_leader": "Value-based care leader",
    "rural_focus": "Rural / underserved focus",
    "research_intensive": "Research-intensive",
    "health_equity": "Health equity focus",
    "limited_innovation": "Limited known innovation infra",
}


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


# (atlas name, HQ "City, ST", lon, lat, category, strategy tags, note)
ATLAS_SOURCE = [
    ("HCA Healthcare", "Nashville, TN", -86.7816, 36.1627, "forprofit", ["vbc_leader"], "Largest for-profit hospital operator; centralized, standardized-care playbook."),
    ("CommonSpirit Health", "Chicago, IL", -87.6298, 41.8781, "faith", ["venture_arm"], "Formed from Catholic Health Initiatives + Dignity Health; has corporate venture/innovation activity (verify specifics)."),
    ("Ascension", "St. Louis, MO", -90.1994, 38.6270, "faith", ["digital_pilot"], "Large Catholic nonprofit system; ongoing EHR and operations modernization."),
    ("Providence", "Renton, WA", -122.2171, 47.4829, "faith", ["venture_arm", "digital_pilot"], "Digital Innovation Group builds and pilots products in-house."),
    ("Trinity Health", "Livonia, MI", -83.3527, 42.3684, "faith", ["venture_arm"], "National Catholic system; Trinity Health Ventures invests in digital health."),
    ("Kaiser Permanente", "Oakland, CA", -122.2712, 37.8044, "payerprovider", ["venture_arm", "vbc_leader"], "Integrated payer + provider; Kaiser Permanente Ventures invests in care-delivery startups."),
    ("Advocate Health", "Charlotte, NC", -80.8431, 35.2271, "secular", ["digital_pilot"], "Formed from the Advocate Aurora + Atrium Health combination; large combined footprint."),
    ("AdventHealth", "Altamonte Springs, FL", -81.3656, 28.6611, "faith", ["digital_pilot"], "National Adventist system with an innovation function (verify specifics)."),
    ("Tenet Healthcare", "Dallas, TX", -96.7970, 32.7767, "forprofit", ["vbc_leader"], "For-profit acute care plus a large ambulatory surgery segment (USPI)."),
    ("Community Health Systems", "Franklin, TN", -86.8689, 35.9251, "forprofit", ["limited_innovation"], "For-profit, largely rural/community hospital footprint; centralized corporate decisions."),
    ("Universal Health Services", "King of Prussia, PA", -75.3733, 40.0879, "forprofit", ["limited_innovation"], "For-profit acute care plus a large behavioral-health division."),
    ("Bon Secours Mercy Health", "Cincinnati, OH", -84.5120, 39.1031, "faith", ["digital_pilot"], "Catholic system across OH/VA/SC/KY with growing digital-health partnerships."),
    ("Sutter Health", "Sacramento, CA", -121.4944, 38.5816, "secular", ["digital_pilot"], "Northern California nonprofit network; early EHR/telehealth adopter."),
    ("Intermountain Health", "Salt Lake City, UT", -111.8910, 40.7608, "secular", ["venture_arm", "vbc_leader"], "Long-standing value-based care and precision-medicine track record; has an in-house venture/innovation function (verify specifics)."),
    ("Sanford Health", "Sioux Falls, SD", -96.7313, 43.5460, "secular", ["rural_focus", "digital_pilot"], "One of the largest rural-focused systems; owns Sanford Health Plan."),
    ("Banner Health", "Phoenix, AZ", -112.0740, 33.4484, "secular", ["vbc_leader"], "Arizona-anchored regional system with strong population-health/ACO infrastructure."),
    ("Baylor Scott & White Health", "Dallas, TX", -96.7970, 32.7767, "secular", ["digital_pilot"], "Large Texas nonprofit system; active digital front-door investments."),
    ("Memorial Hermann Health System", "Houston, TX", -95.3698, 29.7604, "secular", [], "Houston-area nonprofit network with an accountable-care focus."),
    ("Houston Methodist", "Houston, TX", -95.3698, 29.7604, "academic", ["digital_pilot"], "Center for Innovation runs structured startup pilot/evaluation programs."),
    ("Texas Health Resources", "Arlington, TX", -97.1081, 32.7357, "faith", [], "Large DFW-area nonprofit system."),
    ("CHRISTUS Health", "Irving, TX", -96.9489, 32.8140, "faith", ["rural_focus"], "Catholic system spanning TX/LA plus Latin America."),
    ("Mass General Brigham", "Somerville, MA", -71.0995, 42.3876, "academic", ["venture_arm", "research_intensive"], "Large academic system with an innovation/digital group; heavy device and AI pilot activity."),
    ("Yale New Haven Health", "New Haven, CT", -72.9279, 41.3083, "academic", ["research_intensive"], "Anchor academic system for Connecticut."),
    ("Northwell Health", "New Hyde Park, NY", -73.6851, 40.7440, "secular", ["venture_arm", "digital_pilot"], "One of the largest systems in New York State; Northwell Ventures plus an in-house innovation studio."),
    ("NewYork-Presbyterian", "New York, NY", -74.0060, 40.7128, "academic", ["digital_pilot"], "Dual academic affiliation (Columbia + Weill Cornell); active digital-health partnerships."),
    ("Mount Sinai Health System", "New York, NY", -73.9527, 40.7903, "academic", ["research_intensive", "digital_pilot"], "Academic system known for AI/genomics research partnerships."),
    ("NYU Langone Health", "New York, NY", -73.9740, 40.7420, "academic", ["research_intensive"], "Academic medical center with a fast-growing ambulatory network."),
    ("Northwestern Medicine", "Chicago, IL", -87.6298, 41.8781, "academic", ["digital_pilot"], "Academic-community hybrid; digital front-door and operations pilots."),
    ("Rush University System for Health", "Chicago, IL", -87.6636, 41.8742, "academic", ["health_equity"], "Academic anchor with a community health-equity strategy."),
    ("UChicago Medicine", "Chicago, IL", -87.6034, 41.7897, "academic", ["research_intensive"], "South Side Chicago academic anchor."),
    ("Cleveland Clinic", "Cleveland, OH", -81.6212, 41.5027, "academic", ["venture_arm", "research_intensive"], "Cleveland Clinic Innovations is a long-running hospital-based commercialization/venture arm."),
    ("UPMC", "Pittsburgh, PA", -79.9959, 40.4406, "payerprovider", ["venture_arm", "digital_pilot"], "UPMC Enterprises is a prolific health-system corporate venture arm; also runs UPMC Health Plan."),
    ("Geisinger", "Danville, PA", -76.6127, 40.9612, "payerprovider", ["vbc_leader", "research_intensive"], "Integrated payer-provider; genomics (MyCode) and value-based care pioneer."),
    ("Penn Medicine", "Philadelphia, PA", -75.1932, 39.9500, "academic", ["venture_arm", "research_intensive"], "Has an internal innovation center (Penn Medicine Center for Health Care Innovation)."),
    ("Jefferson Health", "Philadelphia, PA", -75.1503, 39.9496, "academic", ["digital_pilot"], "Academic system with an early telehealth program (JeffConnect)."),
    ("Main Line Health", "Radnor, PA", -75.3585, 40.0437, "secular", [], "Philadelphia-suburb nonprofit system."),
    ("WellSpan Health", "York, PA", -76.7277, 39.9626, "secular", ["rural_focus"], "South-central Pennsylvania regional nonprofit network."),
    ("Hackensack Meridian Health", "Edison, NJ", -74.4121, 40.5187, "secular", ["digital_pilot"], "New Jersey's largest system; has a medical-school affiliation (Seton Hall)."),
    ("RWJBarnabas Health", "West Orange, NJ", -74.2391, 40.7987, "academic", [], "New Jersey system anchored by an academic partnership with Rutgers."),
    ("Johns Hopkins Medicine", "Baltimore, MD", -76.5929, 39.2970, "academic", ["venture_arm", "research_intensive"], "Johns Hopkins Technology Innovation Center licenses and pilots external technology."),
    ("Sentara Health", "Norfolk, VA", -76.2859, 36.8508, "payerprovider", ["vbc_leader"], "Integrated system with its own health plan across VA/NC."),
    ("VCU Health", "Richmond, VA", -77.4360, 37.5407, "academic", ["health_equity"], "Academic system for central Virginia."),
    ("Duke Health", "Durham, NC", -78.8986, 35.9940, "academic", ["research_intensive"], "Academic anchor for the Research Triangle; deep clinical-trials infrastructure."),
    ("Novant Health", "Winston-Salem, NC", -80.2442, 36.0999, "secular", ["digital_pilot"], "Carolinas nonprofit system with an active digital-experience roadmap."),
    ("WellStar Health System", "Marietta, GA", -84.5499, 33.9526, "secular", [], "Metro-Atlanta nonprofit network."),
    ("Emory Healthcare", "Atlanta, GA", -84.3226, 33.7970, "academic", ["research_intensive"], "Georgia's largest academic system."),
    ("Piedmont Healthcare", "Atlanta, GA", -84.3733, 33.8467, "secular", [], "Fast-growing Georgia nonprofit network."),
    ("Ochsner Health", "New Orleans, LA", -90.1120, 29.9403, "academic", ["digital_pilot"], "Louisiana's largest system; Ochsner Innovation Lab runs a digital-medicine program."),
    ("LCMC Health", "New Orleans, LA", -90.0715, 29.9511, "secular", [], "New Orleans nonprofit network."),
    ("Baptist Health (Florida)", "Coral Gables, FL", -80.2683, 25.7215, "faith", [], "South Florida nonprofit system."),
    ("Vanderbilt University Medical Center", "Nashville, TN", -86.8027, 36.1447, "academic", ["research_intensive", "venture_arm"], "Academic medical center with an active clinical-informatics research program."),
    ("Henry Ford Health", "Detroit, MI", -83.0458, 42.3314, "secular", ["venture_arm"], "Michigan system with the Henry Ford Innovation Institute; expanded via an Ascension Michigan transaction (verify structure)."),
    ("Corewell Health", "Grand Rapids, MI", -85.6681, 42.9634, "secular", ["digital_pilot"], "Formed from Beaumont Health + Spectrum Health; among Michigan's largest systems."),
    ("UnityPoint Health", "Des Moines, IA", -93.6250, 41.5868, "secular", ["rural_focus"], "Multi-state Midwest nonprofit network."),
    ("MercyOne", "Des Moines, IA", -93.6250, 41.5868, "faith", ["rural_focus"], "Iowa-anchored Catholic system within Trinity Health's national network."),
    ("Mercy", "St. Louis, MO", -90.1994, 38.6270, "faith", ["digital_pilot"], "Mercy Virtual was one of the first dedicated virtual-care hospitals in the US."),
    ("BJC HealthCare", "St. Louis, MO", -90.1994, 38.6270, "academic", ["research_intensive"], "St. Louis system academically affiliated with Washington University."),
    ("SSM Health", "St. Louis, MO", -90.1994, 38.6270, "faith", [], "Catholic system spanning MO/IL/OK/WI."),
    ("Froedtert & the Medical College of Wisconsin", "Milwaukee, WI", -87.9065, 43.0389, "academic", ["research_intensive"], "Milwaukee academic medical center partnership."),
    ("Marshfield Clinic Health System", "Marshfield, WI", -90.1718, 44.6688, "secular", ["rural_focus"], "Rural-Wisconsin system with its own research institute; verify current ownership/affiliation."),
    ("ThedaCare", "Appleton, WI", -88.4154, 44.2619, "secular", ["rural_focus"], "Northeast Wisconsin community system (now part of Froedtert ThedaCare Health)."),
    ("Essentia Health", "Duluth, MN", -92.1005, 46.7867, "faith", ["rural_focus"], "Rural-serving system across MN/WI/ND."),
    ("Allina Health", "Minneapolis, MN", -93.2650, 44.9778, "secular", [], "Twin Cities-anchored nonprofit network."),
    ("HealthPartners", "Bloomington, MN", -93.2983, 44.8408, "payerprovider", ["vbc_leader"], "Consumer-governed integrated payer-provider with a long value-based-care record."),
    ("M Health Fairview", "Minneapolis, MN", -93.2650, 44.9778, "academic", [], "System academically affiliated with the University of Minnesota."),
    ("Avera Health", "Sioux Falls, SD", -96.7313, 43.5460, "faith", ["rural_focus", "digital_pilot"], "Avera eCARE is a nationally recognized rural telehealth/virtual-hospital program."),
    ("UCHealth", "Aurora, CO", -104.8319, 39.7392, "academic", ["digital_pilot"], "University of Colorado partnership with a strong digital front-door push."),
    ("PeaceHealth", "Vancouver, WA", -122.6615, 45.6387, "faith", ["rural_focus"], "Pacific Northwest Catholic system spanning WA/OR/AK."),
    ("MultiCare Health System", "Tacoma, WA", -122.4443, 47.2529, "secular", [], "South Puget Sound nonprofit network."),
    ("Virginia Mason Franciscan Health", "Seattle, WA", -122.3321, 47.6062, "faith", [], "Seattle-area system formed from a Virginia Mason + CHI Franciscan combination."),
    ("Legacy Health", "Portland, OR", -122.6784, 45.5152, "secular", [], "Portland-metro nonprofit network."),
    ("Stanford Health Care", "Stanford, CA", -122.1756, 37.4331, "academic", ["venture_arm", "research_intensive"], "Silicon Valley ties; a startup-friendly academic system for pilots."),
    ("UCSF Health", "San Francisco, CA", -122.4577, 37.7627, "academic", ["research_intensive"], "Top NIH-funded academic system with biotech/AI research partnerships."),
    ("UCLA Health", "Los Angeles, CA", -118.4460, 34.0656, "academic", ["research_intensive"], "Major academic system for Southern California."),
    ("UC Davis Health", "Sacramento, CA", -121.4622, 38.5545, "academic", ["rural_focus"], "Academic anchor for the Central Valley/Sacramento region; telehealth track record."),
    ("Cedars-Sinai", "Los Angeles, CA", -118.3799, 34.0754, "academic", ["venture_arm", "digital_pilot"], "Cedars-Sinai Accelerator is a well-known hospital-run digital-health startup program."),
    ("Scripps Health", "San Diego, CA", -117.2210, 32.8328, "secular", ["research_intensive"], "San Diego nonprofit system tied to the Scripps Research Translational Institute."),
    ("Sharp HealthCare", "San Diego, CA", -117.1478, 32.7581, "payerprovider", ["vbc_leader"], "San Diego integrated system with its own health plan."),
    ("John Muir Health", "Walnut Creek, CA", -122.0652, 37.9101, "secular", [], "East Bay nonprofit network."),
    ("Adventist Health", "Roseville, CA", -121.2880, 38.7521, "faith", ["rural_focus"], "West Coast Adventist system with significant rural/frontier presence."),
    ("El Camino Health", "Mountain View, CA", -122.0839, 37.3861, "secular", ["digital_pilot"], "Small Silicon Valley hospital system close to the tech sector."),
    ("Mayo Clinic", "Rochester, MN", -92.4699, 44.0225, "academic", ["venture_arm", "research_intensive", "digital_pilot"], "Runs Mayo Clinic Platform, a hospital-run AI/digital-health platform business."),
    ("NYC Health + Hospitals", "New York, NY", -74.0060, 40.7128, "public", ["health_equity"], "Largest US municipal public health system; large Medicaid and uninsured population."),
    ("Denver Health", "Denver, CO", -104.9903, 39.7392, "public", ["health_equity"], "Colorado's primary safety-net system and Level I trauma center."),
    ("Cook County Health", "Chicago, IL", -87.6298, 41.8781, "public", ["health_equity"], "Chicago-area public safety-net system."),
    ("Grady Health System", "Atlanta, GA", -84.3880, 33.7490, "public", ["health_equity"], "Atlanta's primary public safety-net and Level I trauma system."),
    ("Parkland Health", "Dallas, TX", -96.8236, 32.8072, "public", ["health_equity"], "Dallas County public hospital system."),
    ("Boston Medical Center Health System", "Boston, MA", -71.0743, 42.3350, "public", ["health_equity"], "Large New England safety-net provider with a health-equity focus."),
    ("St. Jude Children's Research Hospital", "Memphis, TN", -90.0490, 35.1495, "specialty", ["research_intensive"], "Pediatric oncology/research hospital."),
    ("Children's Hospital of Philadelphia", "Philadelphia, PA", -75.1932, 39.9500, "specialty", ["research_intensive", "venture_arm"], "Pediatric hospital with a large research and commercialization operation."),
    ("Boston Children's Hospital", "Boston, MA", -71.0589, 42.3601, "specialty", ["venture_arm", "digital_pilot"], "Innovation and Digital Health Accelerator is a well-known pediatric pilot program."),
    ("Texas Children's Hospital", "Houston, TX", -95.3968, 29.7079, "specialty", ["research_intensive"], "One of the largest pediatric hospitals in the US."),
    ("MD Anderson Cancer Center", "Houston, TX", -95.3985, 29.7069, "specialty", ["research_intensive", "venture_arm"], "Top oncology center with an industry-partnership office."),
    ("Memorial Sloan Kettering Cancer Center", "New York, NY", -73.9564, 40.7648, "specialty", ["research_intensive"], "Leading oncology center with deep pharma/biotech trial relationships."),
    ("City of Hope", "Duarte, CA", -117.9930, 34.1478, "specialty", ["research_intensive"], "Oncology system; acquired Cancer Treatment Centers of America (2022)."),
    ("OSF HealthCare", "Peoria, IL", -89.5890, 40.6936, "faith", ["digital_pilot", "rural_focus"], "OSF Innovation runs a mature rural-telehealth and digital-pilot program."),
]

# Organizations added by the BD team that are not in the Atlas list: hospital systems, plus networks,
# associations, universities and tribal health organizations (not hospital systems, but plausible
# partners). Same unverified status. Coordinates are the HQ city's center; where an organization
# publishes no HQ the note says where the pin was placed.
ADDED_BASIS = (
    "Added by the BD team (not from Atlas). Category and note have no per-row citation — "
    "verify before relying on them."
)
ADDED_SOURCE = [
    ("Marshall Health Network", "Huntington, WV", -82.4452, 38.4192, "academic", ["rural_focus"], "Academic health system based in Huntington, WV, serving parts of West Virginia, southern Ohio and eastern Kentucky."),
    ("Vandalia Health", "Charleston, WV", -81.6326, 38.3498, "secular", ["rural_focus"], "Charleston, WV-based nonprofit system (Charleston Area Medical Center and Mon Health)."),
    # --- networks / associations / universities / tribal organizations ---
    ("Nevada Rural Hospital Partners", "Reno, NV", -119.8138, 39.5296, "network", ["rural_focus"], "Alliance of 13 critical access hospitals in rural Nevada (office in Reno)."),
    ("University of Nevada, Reno", "Reno, NV", -119.8165, 39.5441, "university", ["rural_focus", "research_intensive"], "Public university in Reno with a rural-health presence."),
    ("Community Outreach and Patient Empowerment (COPE)", "Gallup, NM", -108.7426, 35.5281, "tribal", ["rural_focus", "health_equity"], "Native-controlled nonprofit working with Navajo Nation healthcare programs and providers; office in Gallup, NM."),
    ("Fort Defiance Indian Hospital Board", "Fort Defiance, AZ", -109.0770, 35.7414, "tribal", ["rural_focus", "health_equity"], "Governing board of the Fort Defiance Indian Hospital on the Navajo Nation."),
    ("Alaska Hospital & Healthcare Association", "Anchorage, AK", -149.9003, 61.2181, "association", ["rural_focus"], "Statewide hospital and healthcare association for Alaska."),
    ("West Virginia Primary Care Association", "Charleston, WV", -81.6326, 38.3498, "association", ["rural_focus", "health_equity"], "State primary care association serving West Virginia's community health centers."),
    ("VHHA Foundation", "Glen Allen, VA", -77.5063, 37.6654, "association", [], "Foundation arm of the Virginia Hospital & Healthcare Association."),
    ("Ohio High Value Network", "Chillicothe, OH", -82.9824, 39.3331, "network", ["rural_focus", "vbc_leader"], "Clinically integrated network of rural Ohio hospitals (launched April 2025), managed by Cibolo Health. HQ is not published; the pin is at the city of the launch announcement."),
    ("Nebraska High Value Network", "West Point, NE", -96.7114, 41.8386, "network", ["rural_focus", "vbc_leader"], "Clinically integrated network of Nebraska critical access hospitals (launched June 2025), managed by Cibolo Health. HQ is not published; the pin is at the city of the launch announcement."),
    ("Arkansas Rural Health Partnership", "Lake Village, AR", -91.2829, 33.3287, "network", ["rural_focus"], "Arkansas rural health nonprofit and hospital network; headquarters in Lake Village."),
    # --- hospital systems / regional hospitals not in the sourced operator list ---
    ("UK HealthCare", "Lexington, KY", -84.5051, 38.0307, "academic", ["research_intensive", "rural_focus"], "University of Kentucky's academic health system; reaches Appalachian Kentucky."),
    ("Appalachian Regional Healthcare", "Lexington, KY", -84.5037, 38.0406, "secular", ["rural_focus"], "Multi-hospital nonprofit system across central Appalachia (KY / WV)."),
    ("Pikeville Medical Center", "Pikeville, KY", -82.5188, 37.4793, "secular", ["rural_focus"], "Large independent hospital in eastern Kentucky."),
    ("OhioHealth", "Columbus, OH", -82.9988, 39.9612, "secular", [], "Columbus-based nonprofit system with hospitals across Ohio."),
    ("Ohio State University Wexner Medical Center", "Columbus, OH", -83.0187, 39.9973, "academic", ["research_intensive"], "Academic medical center with an Ohio affiliate network."),
    ("Holzer Health System", "Gallipolis, OH", -82.2024, 38.8098, "secular", ["rural_focus"], "Southeast Ohio regional system."),
    ("Southeastern Ohio Regional Medical Center", "Cambridge, OH", -81.5885, 40.0312, "secular", ["rural_focus"], "Rural Appalachian Ohio hospital."),
    ("Carilion Clinic", "Roanoke, VA", -79.9414, 37.2710, "academic", ["rural_focus"], "Roanoke academic system serving rural southwest Virginia."),
    ("UVA Health", "Charlottesville, VA", -78.5006, 38.0316, "academic", ["research_intensive"], "University of Virginia's academic health system."),
    ("University of Tennessee Medical Center", "Knoxville, TN", -83.9444, 35.9380, "academic", ["rural_focus"], "Knoxville academic medical center serving rural East Tennessee."),
    ("Baxter Health", "Mountain Home, AR", -92.3846, 36.3359, "secular", ["rural_focus"], "North-central Arkansas regional health system."),
    ("St. Bernards Healthcare", "Jonesboro, AR", -90.7043, 35.8423, "secular", ["rural_focus"], "Northeast Arkansas regional health system."),
    ("Memorial Hospital at Gulfport", "Gulfport, MS", -89.0928, 30.3674, "secular", [], "Gulf Coast regional hospital system."),
    ("University of Mississippi Medical Center", "Jackson, MS", -90.1700, 32.3000, "academic", ["research_intensive", "rural_focus"], "Mississippi's academic medical center."),
    ("Forrest General Hospital", "Hattiesburg, MS", -89.2903, 31.3271, "secular", ["rural_focus"], "Regional hospital hub for south Mississippi."),
    ("South Central Regional Medical Center", "Laurel, MS", -89.1306, 31.6941, "secular", ["rural_focus"], "Rural regional hospital in Laurel, Mississippi."),
    ("Regional West Medical Center", "Scottsbluff, NE", -103.6672, 41.8666, "secular", ["rural_focus"], "Independent regional hospital in western Nebraska."),
    ("Mary Lanning Healthcare", "Hastings, NE", -98.3903, 40.5861, "secular", ["rural_focus"], "Independent regional hospital in central Nebraska."),
    ("Deborah Heart and Lung Center", "Browns Mills, NJ", -74.5693, 39.9715, "specialty", [], "Specialty cardiopulmonary hospital serving South Jersey."),
    ("Parrish Medical Center", "Titusville, FL", -80.8076, 28.6122, "secular", [], "Community hospital on Florida's Space Coast."),
]

# Atlas name -> (name of the curated operator in health_systems_data.py, match type).
# Hand-written, not fuzzy-matched, so each line can be checked. Anything absent here has no
# operator record and renders as a "profile only" pin.
#   exact   = same organization
#   renamed = same organization under its current/long name in the operator list
#   partial = operator record covers only part of what the Atlas row describes
OPERATOR_CROSSWALK = {
    "HCA Healthcare": ("HCA Healthcare", "exact"),
    "CommonSpirit Health": ("CommonSpirit Health", "exact"),
    "Ascension": ("Ascension", "exact"),
    "Providence": ("Providence", "exact"),
    "Trinity Health": ("Trinity Health", "exact"),
    "Kaiser Permanente": ("Kaiser Permanente", "exact"),
    "Advocate Health": ("Advocate Health", "exact"),
    "AdventHealth": ("AdventHealth", "exact"),
    "Tenet Healthcare": ("Tenet Healthcare", "exact"),
    "Community Health Systems": ("Community Health Systems", "exact"),
    "Universal Health Services": ("Universal Health Services", "exact"),
    "Bon Secours Mercy Health": ("Bon Secours Mercy Health", "exact"),
    "Sutter Health": ("Sutter Health", "exact"),
    "Intermountain Health": ("Intermountain Health", "exact"),
    "Sanford Health": ("Sanford Health", "exact"),
    "Banner Health": ("Banner Health", "exact"),
    "Baylor Scott & White Health": ("Baylor Scott & White Health", "exact"),
    "CHRISTUS Health": ("Christus Health", "renamed"),
    "Mass General Brigham": ("Mass General Brigham", "exact"),
    "Yale New Haven Health": ("Yale New Haven Health System", "renamed"),
    "Northwell Health": ("Northwell Health", "exact"),
    "Northwestern Medicine": ("Northwestern Medicine", "exact"),
    "Cleveland Clinic": ("Cleveland Clinic", "exact"),
    "UPMC": ("UPMC", "exact"),
    "Jefferson Health": ("Jefferson Health", "exact"),
    "RWJBarnabas Health": ("RWJBarnabas Health", "exact"),
    "Johns Hopkins Medicine": ("Johns Hopkins Medicine", "exact"),
    "Sentara Health": ("Sentara Health", "exact"),
    "Duke Health": ("Duke Health", "exact"),
    "Novant Health": ("Novant Health", "exact"),
    "Piedmont Healthcare": ("Piedmont Healthcare", "exact"),
    "Ochsner Health": ("Ochsner Health", "exact"),
    "Corewell Health": ("Corewell Health", "exact"),
    "UnityPoint Health": ("UnityPoint Health", "exact"),
    "Mercy": ("Mercy (Missouri)", "renamed"),
    "Froedtert & the Medical College of Wisconsin": ("Froedtert ThedaCare Health", "renamed"),
    "ThedaCare": ("Froedtert ThedaCare Health", "renamed"),
    "Essentia Health": ("Essentia Health", "exact"),
    "Avera Health": ("Avera Health", "exact"),
    "UCHealth": ("UCHealth", "exact"),
    "MultiCare Health System": ("MultiCare Health System", "exact"),
    "Legacy Health": ("Legacy Health", "exact"),
    "Adventist Health": ("Adventist Health", "exact"),
    "Mayo Clinic": ("Mayo Clinic Health System", "partial"),
    "OSF HealthCare": ("OSF HealthCare", "exact"),
}


# Entries that are a brand or member of another entry (or of an AHRQ system), so a reader doesn't
# mistake them for independent organizations. Shown as "Part of X" in the Atlas.
PART_OF = {
    "MercyOne": "Trinity Health",
    "Virginia Mason Franciscan Health": "CommonSpirit Health",
    "UCSF Health": "University of California Health",
    "UCLA Health": "University of California Health",
    "UC Davis Health": "University of California Health",
}


def _build_profiles():
    """One profile per operator/organization. Two Atlas rows that map to the same operator
    (Froedtert + ThedaCare) fold into one profile: tag union, notes joined."""
    profiles = {}
    rows = [(r, BASIS) for r in ATLAS_SOURCE] + [(r, ADDED_BASIS) for r in ADDED_SOURCE]
    for (name, city, lon, lat, category, tags, note), basis in rows:
        operator, match = OPERATOR_CROSSWALK.get(name, (None, None))
        key = slugify(operator or name)
        if key in profiles:
            p = profiles[key]
            p["strategy_tags"] = sorted(set(p["strategy_tags"]) | set(tags))
            p["note"] = f'{p["note"]} {note}'
            p["atlas_names"].append(name)
            continue
        profiles[key] = {
            "bd_key": key,
            "name": operator or name,
            "operator_name": operator,
            "match_type": match,
            "hq_place": city,
            "hq_lat": lat,
            "hq_lon": lon,
            "category": category,
            "strategy_tags": list(tags),
            "note": note,
            "atlas_names": [name],
            "basis": basis,
            "part_of": PART_OF.get(operator or name),
        }
    out = []
    for p in profiles.values():
        p["atlas_names"] = " + ".join(p["atlas_names"])
        p["confidence"] = "unverified"
        out.append(p)
    return out


BD_PROFILES = _build_profiles()


# West Virginia community health centers, home health agencies and community hospitals (public data; see file).
from wv_providers_data import WV_PROVIDER_ROWS  # noqa: E402

for _r in WV_PROVIDER_ROWS:
    BD_PROFILES.append({
        "bd_key": slugify(_r["name"]), "name": _r["name"], "operator_name": None, "match_type": None,
        "hq_place": f'{_r["city"]}, WV', "hq_lat": _r["lat"], "hq_lon": _r["lon"], "category": _r["category"],
        "strategy_tags": [], "note": _r["note"], "atlas_names": _r["name"], "part_of": None,
        "basis": "Name, place and facts from free public data: " + _r["src"] + ". The category label is ours.",
        "confidence": "unverified",
    })

# Community health centers in the focus states (public HRSA data; see file).
from focus_fqhc_data import FOCUS_FQHC_ROWS  # noqa: E402

for _r in FOCUS_FQHC_ROWS:
    BD_PROFILES.append({
        "bd_key": slugify(_r["name"]), "name": _r["name"], "operator_name": None, "match_type": None,
        "hq_place": f'{_r["city"]}, {_r["state"]}', "hq_lat": _r["lat"], "hq_lon": _r["lon"], "category": _r["category"],
        "strategy_tags": [], "note": _r["note"], "atlas_names": _r["name"], "part_of": None,
        "basis": "Name, place and facts from free public data: " + _r["src"] + ". The category label is ours.",
        "confidence": "unverified",
    })
