"""West Virginia providers beyond the hospital systems — community health centers (FQHCs), Medicare-certified
home health agencies and community hospitals — so the Atlas lists the whole West Virginia field, not only systems.

Generated 2026-11-10 from free public data (nothing here is editorial except the category label):
  * fqhc       — HRSA "Health Center Service Delivery and Look-Alike Sites" file, grantees based in WV, active sites
                 (https://data.hrsa.gov/data/download).
  * homehealth — CMS Provider Data Catalog, "Home Health Care Agencies", state = WV
                 (https://data.cms.gov/provider-data/dataset/6jpm-sxkc); coordinates from the Census batch geocoder
                 (a town-center position for two agencies it could not place).
  * hospital   — CMS Hospital General Information rows already in app/data/cms_hospitals.json, excluding VA
                 hospitals and hospitals that are already counted inside a system listed in the Atlas (WVU Medicine,
                 Vandalia Health incl. CAMC and Mon Health, Marshall/Mountain Health Network, Davis Health System,
                 LifePoint, ScionHealth, UHS). Parent systems of the remaining hospitals were NOT researched, so each
                 note says "verify".

Each row becomes a bd_profiles row (profile-only, no AHRQ link, confidence 'unverified').
"""

WV_PROVIDER_ROWS = [
 {
  "name": "E. A. Hawse Health Center, Inc.",
  "city": "Baker",
  "lat": 39.1453,
  "lon": -78.8112,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Baker, WV; 24 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Shenandoah Valley Medical System, Inc.",
  "city": "Martinsburg",
  "lat": 39.4808,
  "lon": -77.9508,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Martinsburg, WV; 16 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Lincoln County Primary Care Center, Inc.",
  "city": "Hamlin",
  "lat": 38.2782,
  "lon": -82.1035,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Hamlin, WV; 28 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Monroe County Health Department",
  "city": "Union",
  "lat": 37.5893,
  "lon": -80.5461,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Union, WV; 11 active sites on its HRSA scope (u.s. government entity).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Camden-on-Gauley Medical Center, Inc.",
  "city": "Camden On Gauley",
  "lat": 38.3653,
  "lon": -80.6108,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Camden On Gauley, WV; 28 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Community Care of West Virginia, Inc.",
  "city": "Rock Cave",
  "lat": 38.4751,
  "lon": -81.0798,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Rock Cave, WV; 83 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Wirt County Health Service Association, Inc.",
  "city": "Elizabeth",
  "lat": 38.9555,
  "lon": -81.7677,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Elizabeth, WV; 29 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "CHANGE, Inc.",
  "city": "Weirton",
  "lat": 40.4056,
  "lon": -80.5895,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Weirton, WV; 22 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Community Health Systems Inc. (Beckley, WV health center)",
  "city": "Beckley",
  "lat": 37.7881,
  "lon": -81.1997,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Beckley, WV; 35 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Valley Health Systems Inc.",
  "city": "Huntington",
  "lat": 38.4156,
  "lon": -82.4457,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Huntington, WV; 46 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Rainelle Medical Center",
  "city": "Rainelle",
  "lat": 37.9685,
  "lon": -80.7786,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Rainelle, WV; 31 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Womencare, Inc.",
  "city": "Scott Depot",
  "lat": 38.4526,
  "lon": -81.9362,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Scott Depot, WV; 36 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Ritchie County Primary Care Association",
  "city": "Harrisville",
  "lat": 39.3895,
  "lon": -81.2077,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Harrisville, WV; 21 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Minnie Hamilton Health Care Center, Inc.",
  "city": "Grantsville",
  "lat": 38.9366,
  "lon": -80.8157,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Grantsville, WV; 14 active sites on its HRSA scope (corporate entity, not federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "New River Health Association Inc.",
  "city": "Oak Hill",
  "lat": 38.013,
  "lon": -81.1269,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Oak Hill, WV; 20 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Cabin Creek Health Systems, Inc.",
  "city": "Charleston",
  "lat": 38.3043,
  "lon": -81.5657,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Charleston, WV; 13 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Valley Health Care Inc.",
  "city": "Mill Creek",
  "lat": 38.9154,
  "lon": -79.8397,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Mill Creek, WV; 17 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Williamson Health & Wellness Center, Inc.",
  "city": "Williamson",
  "lat": 37.6716,
  "lon": -82.2777,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Williamson, WV; 15 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Pendleton Community Care, Inc.",
  "city": "Franklin",
  "lat": 38.9214,
  "lon": -79.5239,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Franklin, WV; 10 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Bluestone Health Association Inc.",
  "city": "Princeton",
  "lat": 37.2982,
  "lon": -81.2538,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Princeton, WV; 12 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Rural Health Access Corporation",
  "city": "Chapmanville",
  "lat": 37.9571,
  "lon": -82.0187,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Chapmanville, WV; 11 active sites on its HRSA scope (na).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "St George Medical Clinic Inc.",
  "city": "Parsons",
  "lat": 39.0991,
  "lon": -79.6742,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Parsons, WV; 8 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Monongahela Valley Association of Health Centers, Inc.",
  "city": "Fairmont",
  "lat": 39.48,
  "lon": -80.1646,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Fairmont, WV; 6 active sites on its HRSA scope (other).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Tug River Health Association Inc.",
  "city": "Gary",
  "lat": 37.3665,
  "lon": -81.5528,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Gary, WV; 8 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Preston Taylor Community Health Centers Inc.",
  "city": "Grafton",
  "lat": 39.3451,
  "lon": -80.0185,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Grafton, WV; 12 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Belington Community Medical Services Association",
  "city": "Belington",
  "lat": 39.0237,
  "lon": -79.9359,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Belington, WV; 4 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Mountaineer Community Health Center Inc.",
  "city": "Paw Paw",
  "lat": 39.5249,
  "lon": -78.4532,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Paw Paw, WV; 1 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Logan-Mingo Area Mental Health, Inc.",
  "city": "Logan",
  "lat": 37.8615,
  "lon": -82.0449,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Logan, WV; 6 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Clay-Battelle Health Services Association",
  "city": "Blacksville",
  "lat": 39.7196,
  "lon": -80.2073,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Blacksville, WV; 2 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Roane County Family Health Care, Inc.",
  "city": "Spencer",
  "lat": 38.7973,
  "lon": -81.3521,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Spencer, WV; 1 active sites on its HRSA scope (corporate entity, not federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "West Virginia Home Health",
  "city": "Buckhannon",
  "lat": 38.9942,
  "lon": -80.2273,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Buckhannon, WV (proprietary); offers nursing, physical therapy; CMS quality-of-care rating 3 of 5.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "Panhandle Home Health, Inc.",
  "city": "Martinsburg",
  "lat": 39.4676,
  "lon": -77.987,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Martinsburg, WV (non-profit); offers nursing, physical therapy, occupational therapy, speech pathology, medical social services, home health aide.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "Preston Memorial Homecare",
  "city": "Kingwood",
  "lat": 39.4768,
  "lon": -79.7018,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Kingwood, WV (proprietary); offers nursing, physical therapy, occupational therapy, speech pathology, medical social services, home health aide.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "Pleasant Valley Home Health",
  "city": "Point Pleasant",
  "lat": 38.867,
  "lon": -82.1272,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Point Pleasant, WV (non-profit); offers nursing, physical therapy, occupational therapy, speech pathology, medical social services, home health aide; CMS quality-of-care rating 3 of 5.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "Pendleton Home Health Services",
  "city": "Franklin",
  "lat": 38.6506,
  "lon": -79.3273,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Franklin, WV (proprietary); offers nursing, physical therapy, occupational therapy, home health aide; CMS quality-of-care rating 3 of 5.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "Centerwell Home Health",
  "city": "South Charleston",
  "lat": 38.3547,
  "lon": -81.7297,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in South Charleston, WV (proprietary); offers nursing, physical therapy, occupational therapy, speech pathology.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "Home Care Plus, Incorporated",
  "city": "Lewisburg",
  "lat": 37.7905,
  "lon": -80.4478,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Lewisburg, WV (proprietary); offers nursing, physical therapy, occupational therapy, speech pathology, medical social services, home health aide.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "WVUHS Home Care",
  "city": "Clarksburg",
  "lat": 39.2699,
  "lon": -80.3741,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Clarksburg, WV (non-profit); offers nursing, physical therapy, occupational therapy, speech pathology, medical social services, home health aide.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "Adoration Home Health",
  "city": "Beckley",
  "lat": 37.791,
  "lon": -81.2198,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Beckley, WV (proprietary); offers nursing, physical therapy, occupational therapy, speech pathology, medical social services, home health aide.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "St Mary's Home Health Service",
  "city": "Huntington",
  "lat": 38.4102,
  "lon": -82.4295,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Huntington, WV (proprietary); offers nursing, physical therapy, occupational therapy, speech pathology, medical social services, home health aide.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "Homeplus",
  "city": "Elkins",
  "lat": 38.9277,
  "lon": -79.8545,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Elkins, WV (proprietary); offers nursing, physical therapy, occupational therapy, home health aide.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "Grant Memorial Homecare",
  "city": "Petersburg",
  "lat": 39.0018,
  "lon": -79.1381,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Petersburg, WV (proprietary); offers nursing, physical therapy, medical social services; CMS quality-of-care rating 4 of 5.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "Valley Health Home Health/West Virginia",
  "city": "Romney",
  "lat": 39.3362,
  "lon": -78.7474,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Romney, WV (proprietary); offers nursing, physical therapy, occupational therapy, speech pathology, medical social services, home health aide; CMS quality-of-care rating 4 of 5.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "Beckley ARH Home Health",
  "city": "Beckley",
  "lat": 37.7993,
  "lon": -81.1689,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Beckley, WV (proprietary); offers nursing, physical therapy, medical social services, home health aide; CMS quality-of-care rating 3 of 5.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "PCH Home Health",
  "city": "Princeton",
  "lat": 37.3698,
  "lon": -81.0927,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Princeton, WV (proprietary); offers nursing, physical therapy, occupational therapy, home health aide.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "Mountaineer Homecare",
  "city": "Charleston",
  "lat": 38.359,
  "lon": -81.5997,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Charleston, WV (proprietary); offers nursing, physical therapy, occupational therapy, speech pathology, home health aide; CMS quality-of-care rating 3 of 5.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "Boone Memorial Homecare",
  "city": "Danville",
  "lat": 38.0645,
  "lon": -81.8485,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Danville, WV (proprietary); offers nursing, physical therapy.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "Interim Health Care of Morgantown",
  "city": "Morgantown",
  "lat": 39.6492,
  "lon": -79.9005,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Morgantown, WV (proprietary); offers nursing, physical therapy, occupational therapy.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "Care Partners Home Health",
  "city": "Westover",
  "lat": 39.6299,
  "lon": -79.9849,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Westover, WV (proprietary); offers nursing, physical therapy, occupational therapy, speech pathology, medical social services, home health aide; CMS quality-of-care rating 3 of 5.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "Housecalls Home Health",
  "city": "Parkersburg",
  "lat": 39.2703,
  "lon": -81.5602,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Parkersburg, WV (proprietary); offers nursing, physical therapy, occupational therapy.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "Weirton Medical Center Home Health",
  "city": "Weirton",
  "lat": 40.3942,
  "lon": -80.5292,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Weirton, WV (non-profit); offers nursing, physical therapy, occupational therapy, speech pathology, medical social services, home health aide.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "Stonerise Home Health South Charleston",
  "city": "Charleston",
  "lat": 38.3238,
  "lon": -81.5936,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Charleston, WV (proprietary); offers nursing, physical therapy, speech pathology, medical social services; CMS quality-of-care rating 2 of 5.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "Logan ARH Home Health Agency",
  "city": "Logan",
  "lat": 37.8462,
  "lon": -81.9941,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Logan, WV (non-profit); offers nursing, physical therapy, occupational therapy, speech pathology, medical social services, home health aide; CMS quality-of-care rating 4 of 5.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "Holzer Home Care, Mason County",
  "city": "Point Pleasant",
  "lat": 38.8702,
  "lon": -82.1256,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Point Pleasant, WV (non-profit); offers nursing, physical therapy, occupational therapy.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "Caring Angels Home Health, LLC",
  "city": "Inwood",
  "lat": 39.3604,
  "lon": -78.0396,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Inwood, WV (proprietary); offers nursing, physical therapy, occupational therapy.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "West Virginia Home Health LLC",
  "city": "Martinsburg",
  "lat": 39.4616,
  "lon": -77.9872,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Martinsburg, WV (proprietary); offers nursing, physical therapy, occupational therapy, home health aide.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "Personal Touch Home Care of W. VA, Inc.",
  "city": "Hurricane",
  "lat": 38.4631,
  "lon": -81.9315,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Hurricane, WV (proprietary); offers nursing, physical therapy, occupational therapy, speech pathology, medical social services, home health aide.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "Ohio Valley Home Health Services, Inc.",
  "city": "Chester",
  "lat": 40.6137,
  "lon": -80.5595,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Chester, WV (non-profit); offers nursing, physical therapy, occupational therapy, speech pathology, home health aide.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "Carter Healthcare",
  "city": "Wheeling",
  "lat": 40.0457,
  "lon": -80.6602,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Wheeling, WV (proprietary); offers nursing, physical therapy; CMS quality-of-care rating 3 of 5.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "Lots of Hearts Homecare, LLC",
  "city": "Charleston",
  "lat": 38.3847,
  "lon": -81.6318,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Charleston, WV (proprietary); offers nursing, physical therapy, occupational therapy, home health aide.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "Home Health of West Virginia",
  "city": "Charleston",
  "lat": 38.3672,
  "lon": -81.6652,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Charleston, WV (-); CMS quality-of-care rating 4 of 5.",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates from the Census geocoder or the city's hospital centroid"
 },
 {
  "name": "Beckley ARH Hospital",
  "city": "Beckley",
  "lat": 37.79927,
  "lon": -81.16893,
  "category": "hospital",
  "note": "Acute Care Hospitals in Beckley, WV (voluntary non-profit - private). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Boone Memorial Hospital",
  "city": "Madison",
  "lat": 38.04616,
  "lon": -81.80804,
  "category": "hospital",
  "note": "Critical Access Hospitals in Madison, WV (government - local). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Braxton County Memorial Hospital, Inc.",
  "city": "Gassaway",
  "lat": 38.65918,
  "lon": -80.74926,
  "category": "hospital",
  "note": "Critical Access Hospitals in Gassaway, WV (voluntary non-profit - private). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Grafton City Hospital, Inc.",
  "city": "Grafton",
  "lat": 39.35404,
  "lon": -80.01875,
  "category": "hospital",
  "note": "Critical Access Hospitals in Grafton, WV (government - local). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Grant Memorial Hospital",
  "city": "Petersburg",
  "lat": 39.00157,
  "lon": -79.13794,
  "category": "hospital",
  "note": "Critical Access Hospitals in Petersburg, WV (voluntary non-profit - other). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Hampshire Memorial Hospital",
  "city": "Romney",
  "lat": 39.33258,
  "lon": -78.69831,
  "category": "hospital",
  "note": "Critical Access Hospitals in Romney, WV (voluntary non-profit - private). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Highland Hospital",
  "city": "Charleston",
  "lat": 38.31495,
  "lon": -81.56931,
  "category": "hospital",
  "note": "Psychiatric in Charleston, WV (voluntary non-profit - private). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Highland-Clarksburg Hospital, Inc.",
  "city": "Clarksburg",
  "lat": 39.28643,
  "lon": -80.37269,
  "category": "hospital",
  "note": "Psychiatric in Clarksburg, WV (voluntary non-profit - private). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Jackson General Hospital",
  "city": "Ripley",
  "lat": 38.78851,
  "lon": -81.69254,
  "category": "hospital",
  "note": "Critical Access Hospitals in Ripley, WV (voluntary non-profit - private). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Mildred Mitchell-Bateman Hospital",
  "city": "Huntington",
  "lat": 38.40635,
  "lon": -82.36254,
  "category": "hospital",
  "note": "Psychiatric in Huntington, WV (government - state). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Minnie Hamilton Health System",
  "city": "Grantsville",
  "lat": 38.92354,
  "lon": -81.09207,
  "category": "hospital",
  "note": "Critical Access Hospitals in Grantsville, WV (voluntary non-profit - private). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Montgomery General Hospital",
  "city": "Montgomery",
  "lat": 38.18282,
  "lon": -81.32398,
  "category": "hospital",
  "note": "Critical Access Hospitals in Montgomery, WV (voluntary non-profit - other). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Pocahontas Memorial Hospital",
  "city": "Buckeye",
  "lat": 38.20035,
  "lon": -80.10887,
  "category": "hospital",
  "note": "Critical Access Hospitals in Buckeye, WV (government - local). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Preston Memorial Hospital",
  "city": "Kingwood",
  "lat": 39.48813,
  "lon": -79.70988,
  "category": "hospital",
  "note": "Critical Access Hospitals in Kingwood, WV (proprietary). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Princeton Community Hospital Assn Inc.",
  "city": "Princeton",
  "lat": 37.36289,
  "lon": -81.11183,
  "category": "hospital",
  "note": "Acute Care Hospitals in Princeton, WV (government - local). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Rivers Health",
  "city": "Point Pleasant",
  "lat": 38.86854,
  "lon": -82.12257,
  "category": "hospital",
  "note": "Acute Care Hospitals in Point Pleasant, WV (voluntary non-profit - private). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Roane General Hospital",
  "city": "Spencer",
  "lat": 38.81355,
  "lon": -81.36891,
  "category": "hospital",
  "note": "Critical Access Hospitals in Spencer, WV (voluntary non-profit - private). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Sistersville General Hospital",
  "city": "Sistersville",
  "lat": 39.55864,
  "lon": -81.00382,
  "category": "hospital",
  "note": "Critical Access Hospitals in Sistersville, WV (proprietary). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Stonewall Jackson Memorial Hospital Company",
  "city": "Weston",
  "lat": 39.04789,
  "lon": -80.49145,
  "category": "hospital",
  "note": "Acute Care Hospitals in Weston, WV (voluntary non-profit - private). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Summers County ARH Hospital",
  "city": "Hinton",
  "lat": 37.6552,
  "lon": -80.8755,
  "category": "hospital",
  "note": "Critical Access Hospitals in Hinton, WV (voluntary non-profit - private). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Summersville Regional Medical Center",
  "city": "Summersville",
  "lat": 38.29212,
  "lon": -80.83232,
  "category": "hospital",
  "note": "Critical Access Hospitals in Summersville, WV (voluntary non-profit - private). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Thomas Memorial Hospital",
  "city": "South Charleston",
  "lat": 38.3556,
  "lon": -81.72628,
  "category": "hospital",
  "note": "Acute Care Hospitals in South Charleston, WV (voluntary non-profit - private). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Valley Health War Memorial Hospital",
  "city": "Berkeley Springs",
  "lat": 39.54875,
  "lon": -78.22147,
  "category": "hospital",
  "note": "Critical Access Hospitals in Berkeley Springs, WV (voluntary non-profit - private). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Webster Memorial Hospital",
  "city": "Webster Springs",
  "lat": 38.48257,
  "lon": -80.4098,
  "category": "hospital",
  "note": "Critical Access Hospitals in Webster Springs, WV (voluntary non-profit - private). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Weirton Medical Center, Inc.",
  "city": "Weirton",
  "lat": 40.39421,
  "lon": -80.52919,
  "category": "hospital",
  "note": "Acute Care Hospitals in Weirton, WV (government - local). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Welch Community Hospital",
  "city": "Welch",
  "lat": 37.43908,
  "lon": -81.58922,
  "category": "hospital",
  "note": "Acute Care Hospitals in Welch, WV (government - state). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Wetzel County Hospital",
  "city": "New Martinsville",
  "lat": 39.68052,
  "lon": -80.85759,
  "category": "hospital",
  "note": "Acute Care Hospitals in New Martinsville, WV (government - local). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "William R Sharpe, Jr Hospital",
  "city": "Weston",
  "lat": 39.041,
  "lon": -80.49735,
  "category": "hospital",
  "note": "Psychiatric in Weston, WV (government - state). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Williamson Memorial Inc.",
  "city": "Williamson",
  "lat": 37.67865,
  "lon": -82.27204,
  "category": "hospital",
  "note": "Acute Care Hospitals in Williamson, WV (voluntary non-profit - private). Parent system not determined here — it may belong to a larger system; verify.",
  "src": "CMS Hospital General Information (data.cms.gov), as loaded in app/data/cms_hospitals.json"
 },
 {
  "name": "Stonerise Home Health",
  "city": "Barboursville",
  "lat": 38.4087,
  "lon": -82.2943,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Barboursville, WV (proprietary).",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates are the town's city-center position"
 },
 {
  "name": "Dignity Home Health",
  "city": "Chapmanville",
  "lat": 37.9718,
  "lon": -81.8812,
  "category": "homehealth",
  "note": "Medicare-certified home health agency in Chapmanville, WV (proprietary).",
  "src": "CMS Provider Data Catalog, Home Health Care Agencies (data.cms.gov), retrieved 2026-11-10; coordinates are the town's city-center position"
 }
]
