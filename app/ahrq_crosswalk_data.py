"""Hand-written crosswalk: this site's systems -> AHRQ Compendium of U.S. Health Systems (2023) system IDs.

Not fuzzy-matched at runtime: every line was checked by name (and HQ state where names repeat)
against app/data/ahrq/chsp-compendium-2023-rev.csv, so each can be verified by eye. Keys are the
names used in health_systems_data.py (operators) or bd_profiles_data.py (profile-only systems).

match type:
  exact   = same organization, same or trivially different name
  renamed = same organization under another name in AHRQ's 2023 file (a later rename or merger)
  partial = AHRQ's system is only part of what our record describes (or the reverse)

Deliberately NOT matched (left as separate entries rather than guessed): UCSF Health, UCLA Health and
UC Davis Health (AHRQ lists only the whole 'University of California Health'), Marshall Health
Network (the only Marshall in AHRQ is a California system; Cabell Huntington is its closest part),
the specialty hospitals AHRQ does not list (St. Jude, MD Anderson, Memorial Sloan Kettering, City of
Hope), and every network / association / tribal / university organization (not hospital systems).
ThedaCare is a separate AHRQ system (2023, before its merger with Froedtert) and stays AHRQ-only.
"""

AHRQ_CROSSWALK = {
    # name in this site's data: (AHRQ health_sys_id, match type)
    "HCA Healthcare": ("HSI00000492", "exact"),
    "CommonSpirit Health": ("HSI00001427", "exact"),
    "LifePoint Health": ("HSI00000584", "exact"),
    "Ascension": ("HSI00000055", "renamed"),            # AHRQ: "Ascension Health"
    "ScionHealth": ("HSI00001475", "exact"),
    "Trinity Health": ("HSI00001106", "exact"),          # Trinity Health, MI
    "Trinity Health (Minot, ND)": ("HSI00001107", "exact"),
    "Advocate Health": ("HSI00001526", "exact"),
    "Christus Health": ("HSI00000152", "exact"),
    "Community Health Systems": ("HSI00000249", "exact"),
    "Sanford Health": ("HSI00000958", "exact"),
    "AdventHealth": ("HSI00000010", "exact"),
    "Baylor Scott & White Health": ("HSI00000096", "exact"),
    "Providence": ("HSI00000852", "exact"),
    "Tenet Healthcare": ("HSI00001066", "exact"),
    "Bon Secours Mercy Health": ("HSI00001428", "exact"),
    "UPMC": ("HSI00001126", "exact"),
    "Kaiser Permanente": ("HSI00000536", "exact"),
    "Avera Health": ("HSI00000068", "exact"),
    "Intermountain Health": ("HSI00000516", "renamed"),  # AHRQ: "Intermountain Healthcare"
    "Banner Health": ("HSI00000073", "exact"),
    "Universal Health Services": ("HSI00001148", "exact"),
    "Cleveland Clinic": ("HSI00001078", "exact"),
    "Ballad Health": ("HSI00001284", "exact"),
    "Novant Health": ("HSI00000773", "exact"),
    "Essentia Health": ("HSI00000350", "exact"),
    "MaineHealth": ("HSI00000611", "exact"),
    "University of Vermont Health Network": ("HSI00001185", "exact"),
    "Mass General Brigham": ("HSI00000813", "exact"),
    "Yale New Haven Health System": ("HSI00001272", "exact"),
    "Northwell Health": ("HSI00000767", "exact"),
    "RWJBarnabas Health": ("HSI00000863", "exact"),
    "Jefferson Health": ("HSI00000048", "exact"),        # Jefferson Health, PA (not Jefferson Healthcare, WA)
    "ChristianaCare": ("HSI00000218", "exact"),
    "Johns Hopkins Medicine": ("HSI00000531", "renamed"),  # AHRQ: "Johns Hopkins Health System"
    "Sentara Health": ("HSI00000972", "renamed"),          # AHRQ: "Sentara Healthcare"
    "Prisma Health": ("HSI00001378", "exact"),
    "Piedmont Healthcare": ("HSI00000826", "exact"),
    "Orlando Health": ("HSI00000796", "exact"),
    "UAB Medicine": ("HSI00001116", "renamed"),            # AHRQ: "UAB Health System"
    "North Mississippi Health Services": ("HSI00000750", "exact"),
    "University Hospitals": ("HSI00001156", "exact"),      # University Hospitals, OH
    "Corewell Health": ("HSI00001021", "exact"),
    "Indiana University Health": ("HSI00000510", "exact"),
    "Northwestern Medicine": ("HSI00000770", "exact"),
    "OSF HealthCare": ("HSI00000776", "exact"),
    "Mayo Clinic Health System": ("HSI00000631", "exact"),
    "UnityPoint Health": ("HSI00001146", "exact"),
    "Bryan Health": ("HSI00000143", "exact"),
    "Norton Healthcare": ("HSI00000771", "exact"),
    "INTEGRIS Health": ("HSI00000507", "exact"),
    "Ochsner Health": ("HSI00000780", "exact"),
    "Monument Health": ("HSI00000868", "exact"),
    "Presbyterian Healthcare Services": ("HSI00000843", "exact"),
    "HonorHealth": ("HSI00000491", "exact"),
    "Renown Health": ("HSI00000874", "exact"),
    "MultiCare Health System": ("HSI00000714", "exact"),
    "Legacy Health": ("HSI00000576", "exact"),
    "Sutter Health": ("HSI00001050", "exact"),
    "Adventist Health": ("HSI00000011", "exact"),          # Adventist Health, CA (not Adventist Healthcare, MD)
    "University of Kansas Health System": ("HSI00001173", "exact"),
    "Memorial Hermann Health System": ("HSI00000654", "exact"),
    "Houston Methodist": ("HSI00001081", "exact"),
    "Texas Health Resources": ("HSI00001072", "exact"),
    "Mount Sinai Health System": ("HSI00000711", "exact"),
    "NYU Langone Health": ("HSI00000717", "exact"),
    "Geisinger": ("HSI00000388", "exact"),
    "Main Line Health": ("HSI00000608", "exact"),
    "WellSpan Health": ("HSI00001243", "exact"),
    "Hackensack Meridian Health": ("HSI00000439", "exact"),
    "VCU Health": ("HSI00001213", "exact"),
    "WellStar Health System": ("HSI00001244", "exact"),
    "Emory Healthcare": ("HSI00000342", "exact"),
    "LCMC Health": ("HSI00000555", "exact"),
    "Henry Ford Health": ("HSI00000475", "exact"),
    "BJC HealthCare": ("HSI00000070", "exact"),
    "SSM Health": ("HSI00000902", "exact"),
    "Marshfield Clinic Health System": ("HSI00000621", "exact"),
    "Allina Health": ("HSI00000029", "exact"),
    "HealthPartners": ("HSI00000464", "exact"),
    "PeaceHealth": ("HSI00000814", "exact"),
    "Stanford Health Care": ("HSI00001033", "exact"),
    "Cedars-Sinai": ("HSI00000190", "exact"),
    "Scripps Health": ("HSI00000968", "exact"),
    "Sharp HealthCare": ("HSI00000977", "exact"),
    "John Muir Health": ("HSI00000530", "exact"),
    "El Camino Health": ("HSI00000336", "exact"),
    "Cook County Health": ("HSI00000274", "exact"),
    "Grady Health System": ("HSI00000412", "exact"),
    "Parkland Health": ("HSI00000298", "exact"),
    "Boston Medical Center Health System": ("HSI00000131", "exact"),
    "Appalachian Regional Healthcare": ("HSI00000041", "exact"),
    "Pikeville Medical Center": ("HSI00001423", "exact"),
    "OhioHealth": ("HSI00000784", "exact"),
    "Ohio State University Wexner Medical Center": ("HSI00001086", "exact"),
    "Holzer Health System": ("HSI00000490", "exact"),
    "Carilion Clinic": ("HSI00000170", "exact"),
    "University of Tennessee Medical Center": ("HSI00001153", "exact"),
    "Memorial Hospital at Gulfport": ("HSI00000655", "exact"),
    "University of Mississippi Medical Center": ("HSI00001155", "exact"),
    "South Central Regional Medical Center": ("HSI00001441", "exact"),
    "Regional West Medical Center": ("HSI00000871", "renamed"),   # AHRQ: "Regional West Health Services"
    "Mary Lanning Healthcare": ("HSI00000623", "exact"),
    "Parrish Medical Center": ("HSI00000812", "exact"),
    # checked by hand where the names differ
    "Dartmouth Health": ("HSI00000299", "renamed"),               # AHRQ: "Dartmouth-Hitchcock"
    "Brown University Health": ("HSI00000585", "renamed"),        # AHRQ: "Lifespan" (renamed Brown University Health)
    "Duke Health": ("HSI00000323", "renamed"),                    # AHRQ: "Duke University Health System"
    "Baptist Health (Kentucky)": ("HSI00000080", "renamed"),      # AHRQ: "Baptist Healthcare System", KY
    "Baptist Health (Arkansas)": ("HSI00000074", "exact"),
    "Baptist Health (Florida)": ("HSI00000077", "renamed"),       # AHRQ: "Baptist Health South Florida"
    "Baptist Memorial Health Care (Tennessee)": ("HSI00000081", "renamed"),
    "Mercy (Missouri)": ("HSI00000660", "exact"),
    "Froedtert ThedaCare Health": ("HSI00000386", "partial"),     # AHRQ 2023: Froedtert and MCW only
    "UCHealth": ("HSI00001169", "renamed"),                       # AHRQ: "University of Colorado Health"
    "University of Utah Health": ("HSI00001184", "renamed"),      # AHRQ: "University of Utah Hospitals and Clinics"
    "St. Luke's Health System": ("HSI00000934", "exact"),         # Saint Lukes, ID
    "The Queen's Health Systems": ("HSI00001087", "exact"),
    "NewYork-Presbyterian": ("HSI00000731", "renamed"),           # AHRQ: "New York Presbyterian Healthcare System"
    "Rush University System for Health": ("HSI00000897", "renamed"),
    "UChicago Medicine": ("HSI00001089", "renamed"),
    "Penn Medicine": ("HSI00000820", "renamed"),                  # AHRQ: "University of Pennsylvania Health System"
    "Vanderbilt University Medical Center": ("HSI00001222", "renamed"),
    "M Health Fairview": ("HSI00000357", "renamed"),              # AHRQ: "Fairview Health Services"
    "NYC Health + Hospitals": ("HSI00000730", "renamed"),
    "Denver Health": ("HSI00000307", "exact"),
    "Boston Children's Hospital": ("HSI00000130", "exact"),
    "Children's Hospital of Philadelphia": ("HSI00001075", "exact"),
    "Texas Children's Hospital": ("HSI00001069", "exact"),
    "WVU Medicine": ("HSI00001251", "renamed"),                   # AHRQ: "West Virginia University Health System"
    "Vandalia Health": ("HSI00000147", "partial"),                # AHRQ 2023: CAMC Health System (before the Mon Health merger)
    "Marshall Health Network": ("HSI00000154", "partial"),        # AHRQ: Cabell Huntington Hospital, a Marshall Health Network member
    "UK HealthCare": ("HSI00001174", "renamed"),                  # AHRQ: "University of Kentucky Healthcare"
    "UVA Health": ("HSI00001186", "renamed"),                     # AHRQ: "University of Virginia Health System"
    "St. Bernards Healthcare": ("HSI00000911", "exact"),
    "Baxter Health": ("HSI00000090", "renamed"),                  # AHRQ: "Baxter Regional Medical Center"
    "Forrest General Hospital": ("HSI00000371", "partial"),       # AHRQ: "Forrest Health", the system that owns it
}


# AHRQ's file is 2023 data. These systems were separate then but have since merged into one of OUR
# entries, so they are not listed as entries of their own (that would show one organization twice);
# they stay in the national AHRQ tables, and the surviving entry shows them as "AHRQ also lists".
# Merger facts are from general knowledge (ThedaCare: this site's own operator record) — verify.
#   AHRQ sys_id: (our entry it merged into, short note)
AHRQ_MERGED = {
    "HSI00001092": ("Froedtert ThedaCare Health", "ThedaCare merged with Froedtert Health in 2024"),
    "HSI00000577": ("Jefferson Health", "Lehigh Valley Health Network joined Jefferson Health in 2024"),
    "HSI00001253": ("Northwell Health", "Nuvance Health joined Northwell Health in 2025"),
}
