"""Community health centers (FQHC grantees) in the Atlas's focus states — Nevada, Arizona, Tennessee, Kentucky,
Colorado, Alaska and Wyoming — from HRSA's free "Health Center Service Delivery and Look-Alike Sites" file
(https://data.hrsa.gov/data/download), active sites only, grantees based in the state. Grantees that are
already an Atlas entry under another name (Denver Health, SEARHC, Maury Regional, Erlanger's hospital
authority, Valleywise's county district, the University of Colorado and of Kentucky) are left out.

Added so each focus state has enough organizations to track, as West Virginia has (see wv_providers_data.py).
Each row becomes a bd_profiles row (profile-only, no AHRQ link, confidence 'unverified'; the category is ours).
"""

FOCUS_FQHC_ROWS = [
 {
  "name": "Aleutian Pribilof Islands Association, Inc.",
  "city": "Anchorage",
  "state": "AK",
  "lat": 61.1744,
  "lon": -149.8613,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Anchorage, AK; 4 active sites on its HRSA scope (other).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Anchorage Neighborhood Health Center, Inc.",
  "city": "Anchorage",
  "state": "AK",
  "lat": 61.1759,
  "lon": -149.8877,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Anchorage, AK; 1 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Bethel Family Clinic",
  "city": "Bethel",
  "state": "AK",
  "lat": 60.7958,
  "lon": -161.762,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Bethel, AK; 2 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Bristol Bay Area Health Corporation",
  "city": "Dillingham",
  "state": "AK",
  "lat": 59.0001,
  "lon": -158.5355,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Dillingham, AK; 26 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Bristol Bay Borough of",
  "city": "Naknek",
  "state": "AK",
  "lat": 58.683,
  "lon": -156.67,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Naknek, AK; 3 active sites on its HRSA scope (u.s. government entity).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Copper River Native Association",
  "city": "Glennallen",
  "state": "AK",
  "lat": 62.1129,
  "lon": -145.5267,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Glennallen, AK; 2 active sites on its HRSA scope (na).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Council of Athabascan Tribal Governments, Inc.",
  "city": "Fort Yukon",
  "state": "AK",
  "lat": 66.5675,
  "lon": -145.2422,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Fort Yukon, AK; 5 active sites on its HRSA scope (other).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Cross Road Health Ministries, Inc.",
  "city": "Glennallen",
  "state": "AK",
  "lat": 62.1079,
  "lon": -145.5329,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Glennallen, AK; 5 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Dena Nena Henash",
  "city": "Fairbanks",
  "state": "AK",
  "lat": 64.8444,
  "lon": -147.7089,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Fairbanks, AK; 25 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Eastern Aleutian Tribes Inc.",
  "city": "Anchorage",
  "state": "AK",
  "lat": 61.1898,
  "lon": -149.8872,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Anchorage, AK; 8 active sites on its HRSA scope (other).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Girdwood Health Clinic Inc.",
  "city": "Girdwood",
  "state": "AK",
  "lat": 60.9636,
  "lon": -149.1341,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Girdwood, AK; 1 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Iliuliuk Family and Health Services, Inc.",
  "city": "Unalaska",
  "state": "AK",
  "lat": 53.8723,
  "lon": -166.5394,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Unalaska, AK; 1 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Interior Community Health Center",
  "city": "Fairbanks",
  "state": "AK",
  "lat": 64.8265,
  "lon": -147.7424,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Fairbanks, AK; 2 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Jamhi Health & Wellness Inc.",
  "city": "Juneau",
  "state": "AK",
  "lat": 58.3319,
  "lon": -134.4711,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Juneau, AK; 2 active sites on its HRSA scope (na).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Kodiak Area Native Association",
  "city": "Kodiak",
  "state": "AK",
  "lat": 57.8118,
  "lon": -152.3551,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Kodiak, AK; 8 active sites on its HRSA scope (other).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Kodiak Island Health Care Foundation",
  "city": "Kodiak",
  "state": "AK",
  "lat": 57.8134,
  "lon": -152.3569,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Kodiak, AK; 3 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Maniilaq Association",
  "city": "Kotzebue",
  "state": "AK",
  "lat": 66.895,
  "lon": -162.5921,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Kotzebue, AK; 13 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Mat-Su Health Services, Inc.",
  "city": "Wasilla",
  "state": "AK",
  "lat": 61.6014,
  "lon": -149.4857,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Wasilla, AK; 4 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Municipality of Skagway",
  "city": "Skagway",
  "state": "AK",
  "lat": 59.4607,
  "lon": -135.3065,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Skagway, AK; 1 active sites on its HRSA scope (u.s. government entity).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Native Village of Eyak",
  "city": "Cordova",
  "state": "AK",
  "lat": 60.5427,
  "lon": -145.765,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Cordova, AK; 2 active sites on its HRSA scope (other).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Norton Sound Health Corp",
  "city": "Nome",
  "state": "AK",
  "lat": 64.4995,
  "lon": -165.3784,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Nome, AK; 16 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Peninsula Community Health Services of Alaska, Inc.",
  "city": "Soldotna",
  "state": "AK",
  "lat": 60.4955,
  "lon": -151.0644,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Soldotna, AK; 4 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Seldovia Village Tribe",
  "city": "Seldovia",
  "state": "AK",
  "lat": 59.6504,
  "lon": -151.5219,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Seldovia, AK; 4 active sites on its HRSA scope (other).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Seward Community Health Center, Inc.",
  "city": "Seward",
  "state": "AK",
  "lat": 60.1054,
  "lon": -149.4465,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Seward, AK; 2 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Southcentral Foundation",
  "city": "Anchorage",
  "state": "AK",
  "lat": 61.1824,
  "lon": -149.7956,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Anchorage, AK; 18 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Sunshine Community Health Center Incorporated",
  "city": "Talkeetna",
  "state": "AK",
  "lat": 62.1312,
  "lon": -150.0439,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Talkeetna, AK; 4 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Yakutat Tlingit Tribe",
  "city": "Yakutat",
  "state": "AK",
  "lat": 59.5428,
  "lon": -139.7255,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Yakutat, AK; 2 active sites on its HRSA scope (other).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Yukon-Kuskokwim Health Corp",
  "city": "Bethel",
  "state": "AK",
  "lat": 60.7898,
  "lon": -161.7748,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Bethel, AK; 35 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Adelante Healthcare Inc.",
  "city": "Phoenix",
  "state": "AZ",
  "lat": 33.4837,
  "lon": -112.0731,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Phoenix, AZ; 15 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Black Canyon Community Health Center",
  "city": "Black Canyon City",
  "state": "AZ",
  "lat": 34.06,
  "lon": -112.1479,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Black Canyon City, AZ; 4 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Canyonlands Community Health Care",
  "city": "Page",
  "state": "AZ",
  "lat": 36.9214,
  "lon": -111.461,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Page, AZ; 14 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Chiricahua Community Health Centers Inc.",
  "city": "Elfrida",
  "state": "AZ",
  "lat": 31.6984,
  "lon": -109.6869,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Elfrida, AZ; 35 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Circle the City",
  "city": "Phoenix",
  "state": "AZ",
  "lat": 33.492,
  "lon": -112.0787,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Phoenix, AZ; 10 active sites on its HRSA scope (other).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Creek Valley Health Clinic",
  "city": "Colorado City",
  "state": "AZ",
  "lat": 37.0081,
  "lon": -112.967,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Colorado City, AZ; 2 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Desert Senita Community Health Center",
  "city": "Ajo",
  "state": "AZ",
  "lat": 32.3756,
  "lon": -112.8637,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Ajo, AZ; 8 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "El Rio Santa Cruz Neighborhood Health Center Inc.",
  "city": "Tucson",
  "state": "AZ",
  "lat": 32.2235,
  "lon": -110.9792,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Tucson, AZ; 32 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Horizon Health and Wellness, Inc.",
  "city": "Apache Junction",
  "state": "AZ",
  "lat": 33.4208,
  "lon": -111.55,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Apache Junction, AZ; 10 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Marana Health Center, Inc.",
  "city": "Marana",
  "state": "AZ",
  "lat": 32.4495,
  "lon": -111.2132,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Marana, AZ; 13 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Mariposa Community Health Center, Inc.",
  "city": "Nogales",
  "state": "AZ",
  "lat": 31.3473,
  "lon": -110.9311,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Nogales, AZ; 16 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Mountain Park Health Center",
  "city": "Phoenix",
  "state": "AZ",
  "lat": 33.4825,
  "lon": -112.0731,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Phoenix, AZ; 15 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Native Health",
  "city": "Phoenix",
  "state": "AZ",
  "lat": 33.494,
  "lon": -112.0727,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Phoenix, AZ; 3 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Neighborhood Outreach Access to Health",
  "city": "Phoenix",
  "state": "AZ",
  "lat": 33.5464,
  "lon": -112.0433,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Phoenix, AZ; 8 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Sun Life Family Health Center Inc.",
  "city": "Casa Grande",
  "state": "AZ",
  "lat": 32.8792,
  "lon": -111.6924,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Casa Grande, AZ; 13 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Sunset Community Health Center, Inc.",
  "city": "Somerton",
  "state": "AZ",
  "lat": 32.7147,
  "lon": -114.6504,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Somerton, AZ; 10 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Terros Inc.",
  "city": "Phoenix",
  "state": "AZ",
  "lat": 33.4825,
  "lon": -112.0731,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Phoenix, AZ; 15 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Tuba City Regional Health Care Corporation",
  "city": "Tuba City",
  "state": "AZ",
  "lat": 36.1357,
  "lon": -111.2357,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Tuba City, AZ; 5 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "United Community Health Center-Maria Auxiliadora Inc.",
  "city": "Green Valley",
  "state": "AZ",
  "lat": 31.8528,
  "lon": -110.9739,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Green Valley, AZ; 14 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Valle Del Sol, Inc.",
  "city": "Phoenix",
  "state": "AZ",
  "lat": 33.492,
  "lon": -112.0644,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Phoenix, AZ; 37 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Wesley Community Center Inc.",
  "city": "Phoenix",
  "state": "AZ",
  "lat": 33.4333,
  "lon": -112.101,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Phoenix, AZ; 6 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Yavapai County Government Prescott",
  "city": "Prescott",
  "state": "AZ",
  "lat": 34.6083,
  "lon": -112.4612,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Prescott, AZ; 6 active sites on its HRSA scope (u.s. government entity).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Clinica Campesina/family Health Services",
  "city": "Lafayette",
  "state": "CO",
  "lat": 39.8289,
  "lon": -105.0078,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Lafayette, CO; 24 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "High Plains Community Health Center",
  "city": "Lamar",
  "state": "CO",
  "lat": 38.0886,
  "lon": -102.6211,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Lamar, CO; 5 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Inner City Health Center",
  "city": "Denver",
  "state": "CO",
  "lat": 39.7694,
  "lon": -104.9595,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Denver, CO; 2 active sites on its HRSA scope (na).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "La Clinica Tepeyac, Inc.",
  "city": "Denver",
  "state": "CO",
  "lat": 39.7825,
  "lon": -104.9648,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Denver, CO; 3 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Marillac Clinic, Inc.",
  "city": "Grand Junction",
  "state": "CO",
  "lat": 39.0806,
  "lon": -108.5052,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Grand Junction, CO; 6 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Metro Community Provider Network Inc.",
  "city": "Wheat Ridge",
  "state": "CO",
  "lat": 39.7594,
  "lon": -105.0807,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Wheat Ridge, CO; 13 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Mountain Family Health Centers",
  "city": "Glenwood Springs",
  "state": "CO",
  "lat": 39.5235,
  "lon": -107.3239,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Glenwood Springs, CO; 9 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Northwest Colorado Visiting Nurse Association",
  "city": "Steamboat Springs",
  "state": "CO",
  "lat": 40.4652,
  "lon": -106.8241,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Steamboat Springs, CO; 9 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Olathe Community Clinic, Inc.",
  "city": "Olathe",
  "state": "CO",
  "lat": 38.6059,
  "lon": -107.9838,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Olathe, CO; 3 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Peak Vista Community Health Centers",
  "city": "Colorado Springs",
  "state": "CO",
  "lat": 38.8266,
  "lon": -104.788,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Colorado Springs, CO; 26 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Pueblo Community Health Center",
  "city": "Pueblo",
  "state": "CO",
  "lat": 38.2576,
  "lon": -104.6231,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Pueblo, CO; 15 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Salud Family Health, Inc.",
  "city": "Fort Lupton",
  "state": "CO",
  "lat": 40.0778,
  "lon": -104.8058,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Fort Lupton, CO; 24 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Southwest Colorado Mental Health Center, Inc.",
  "city": "Durango",
  "state": "CO",
  "lat": 37.2401,
  "lon": -107.8677,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Durango, CO; 8 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Summit Community Care Clinic, Inc.",
  "city": "Frisco",
  "state": "CO",
  "lat": 39.5702,
  "lon": -106.0762,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Frisco, CO; 21 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Sunrise Community Health",
  "city": "Evans",
  "state": "CO",
  "lat": 40.3886,
  "lon": -104.6927,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Evans, CO; 15 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "The Colorado Coalition for the Homeless",
  "city": "Denver",
  "state": "CO",
  "lat": 39.7516,
  "lon": -104.9879,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Denver, CO; 20 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Uncompahgre Combined Clinics",
  "city": "Norwood",
  "state": "CO",
  "lat": 38.1293,
  "lon": -108.2982,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Norwood, CO; 1 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Uptown Community Health Center Inc.",
  "city": "Denver",
  "state": "CO",
  "lat": 39.7467,
  "lon": -104.9743,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Denver, CO; 6 active sites on its HRSA scope (na).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Valley-Wide Health Systems",
  "city": "Alamosa",
  "state": "CO",
  "lat": 37.9862,
  "lon": -103.5539,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Alamosa, CO; 38 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Community Health Alliance",
  "city": "Reno",
  "state": "NV",
  "lat": 39.5024,
  "lon": -119.762,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Reno, NV; 11 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "First Person Care Clinic",
  "city": "Las Vegas",
  "state": "NV",
  "lat": 33.4037,
  "lon": -111.9267,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Las Vegas, NV; 6 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Firstmed Health and Wellness Center",
  "city": "Las Vegas",
  "state": "NV",
  "lat": 36.129,
  "lon": -115.1191,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Las Vegas, NV; 6 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Hope Christian Health Center",
  "city": "North Las Vegas",
  "state": "NV",
  "lat": 36.233,
  "lon": -115.1615,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in North Las Vegas, NV; 12 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Nevada Health Centers, Inc.",
  "city": "Carson City",
  "state": "NV",
  "lat": 39.1892,
  "lon": -119.7498,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Carson City, NV; 27 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Northern Nevada HIV Outpatient Program, Education and Services",
  "city": "Reno",
  "state": "NV",
  "lat": 39.5298,
  "lon": -119.8214,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Reno, NV; 5 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Safe Harbor Medical, Inc.",
  "city": "Las Vegas",
  "state": "NV",
  "lat": 36.2147,
  "lon": -115.251,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Las Vegas, NV; 5 active sites on its HRSA scope (na).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Southern Nevada Health Dist",
  "city": "Las Vegas",
  "state": "NV",
  "lat": 36.1709,
  "lon": -115.2095,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Las Vegas, NV; 3 active sites on its HRSA scope (u.s. government entity).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Chattanooga C. A. R. E. S, Inc.",
  "city": "Chattanooga",
  "state": "TN",
  "lat": 35.0477,
  "lon": -85.2903,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Chattanooga, TN; 6 active sites on its HRSA scope (na).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Cherokee Health Systems",
  "city": "Knoxville",
  "state": "TN",
  "lat": 36.1752,
  "lon": -83.4012,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Knoxville, TN; 44 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Chota Community Health Services",
  "city": "Madisonville",
  "state": "TN",
  "lat": 35.5053,
  "lon": -84.3711,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Madisonville, TN; 16 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Christ Community Health Services Inc.",
  "city": "Memphis",
  "state": "TN",
  "lat": 35.1352,
  "lon": -89.9737,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Memphis, TN; 13 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Community Health of East Tennessee, Inc.",
  "city": "La Follette",
  "state": "TN",
  "lat": 36.353,
  "lon": -84.1581,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in La Follette, TN; 2 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Citizens of Lake County for Health Care, Inc.",
  "city": "Tiptonville",
  "state": "TN",
  "lat": 36.3696,
  "lon": -89.4676,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Tiptonville, TN; 4 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Dayspring Health, Inc.",
  "city": "Jellico",
  "state": "TN",
  "lat": 36.5875,
  "lon": -84.127,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Jellico, TN; 7 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "East Tennessee State University",
  "city": "Johnson City",
  "state": "TN",
  "lat": 36.3017,
  "lon": -82.3664,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Johnson City, TN; 5 active sites on its HRSA scope (u.s. government entity).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Hardeman County Community Health Center",
  "city": "Bolivar",
  "state": "TN",
  "lat": 35.2664,
  "lon": -89.0012,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Bolivar, TN; 6 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Hardin County Regional Health Center",
  "city": "Savannah",
  "state": "TN",
  "lat": 35.2133,
  "lon": -88.2386,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Savannah, TN; 6 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Hope Family Health Services",
  "city": "Westmoreland",
  "state": "TN",
  "lat": 36.5525,
  "lon": -86.24,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Westmoreland, TN; 4 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Matthew Walker Comprehensive Health Center, Inc.",
  "city": "Nashville",
  "state": "TN",
  "lat": 36.1703,
  "lon": -86.8012,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Nashville, TN; 4 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Memphis Health Center Inc.",
  "city": "Memphis",
  "state": "TN",
  "lat": 35.1249,
  "lon": -90.0502,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Memphis, TN; 7 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Mercy Health Services, Inc.",
  "city": "Franklin",
  "state": "TN",
  "lat": 35.8961,
  "lon": -86.8625,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Franklin, TN; 24 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Morgan County Health Council, Inc.",
  "city": "Wartburg",
  "state": "TN",
  "lat": 36.1011,
  "lon": -84.5929,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Wartburg, TN; 1 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Mountain Peoples' Health Councils, Inc.",
  "city": "Oneida",
  "state": "TN",
  "lat": 36.5003,
  "lon": -84.5244,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Oneida, TN; 12 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Ocoee Regional Health Corp",
  "city": "Benton",
  "state": "TN",
  "lat": 35.1866,
  "lon": -84.6358,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Benton, TN; 6 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Perry County Medical Center, Inc.",
  "city": "Linden",
  "state": "TN",
  "lat": 35.9084,
  "lon": -87.3353,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Linden, TN; 4 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Rural Health Services Consortium, Inc.",
  "city": "Rogersville",
  "state": "TN",
  "lat": 36.4609,
  "lon": -82.9413,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Rogersville, TN; 16 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Rural Medical Services, Inc.",
  "city": "Newport",
  "state": "TN",
  "lat": 35.9656,
  "lon": -83.1821,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Newport, TN; 10 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Rutherford County Primary Care Clinic Inc.",
  "city": "Murfreesboro",
  "state": "TN",
  "lat": 35.8715,
  "lon": -86.4238,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Murfreesboro, TN; 4 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Tennessee Department of Health",
  "city": "Nashville",
  "state": "TN",
  "lat": 36.2138,
  "lon": -86.7416,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Nashville, TN; 21 active sites on its HRSA scope (u.s. government entity).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Tri State Community Health Center",
  "city": "Memphis",
  "state": "TN",
  "lat": 35.0644,
  "lon": -89.9286,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Memphis, TN; 3 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "United Neighborhood Health Services, Inc.",
  "city": "Nashville",
  "state": "TN",
  "lat": 36.1766,
  "lon": -86.7564,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Nashville, TN; 14 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "University Community Health Services, Inc.",
  "city": "Nashville",
  "state": "TN",
  "lat": 36.1383,
  "lon": -86.6978,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Nashville, TN; 5 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Cheyenne Health and Wellness Center",
  "city": "Cheyenne",
  "state": "WY",
  "lat": 41.1324,
  "lon": -104.8199,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Cheyenne, WY; 4 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Community Action of Laramie County, Inc.",
  "city": "Cheyenne",
  "state": "WY",
  "lat": 41.1253,
  "lon": -104.8395,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Cheyenne, WY; 1 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Community Health Center of Central Wyoming, Inc.",
  "city": "Casper",
  "state": "WY",
  "lat": 42.8421,
  "lon": -106.2579,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Casper, WY; 4 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Friends of the Community Action Partnership of Natrona County",
  "city": "Casper",
  "state": "WY",
  "lat": 42.8444,
  "lon": -106.327,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Casper, WY; 3 active sites on its HRSA scope (u.s. government entity).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "University of Wyoming",
  "city": "Laramie",
  "state": "WY",
  "lat": 41.3207,
  "lon": -105.5615,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Laramie, WY; 3 active sites on its HRSA scope (u.s. government entity).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "A+ Family Healthcare, LLC",
  "city": "Brownsville",
  "state": "KY",
  "lat": 37.1914,
  "lon": -86.2647,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Brownsville, KY; 9 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Audubon Area Community Care Clinic, Inc.",
  "city": "Owensboro",
  "state": "KY",
  "lat": 37.7598,
  "lon": -87.1126,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Owensboro, KY; 13 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Big Sandy Health Care",
  "city": "Prestonsburg",
  "state": "KY",
  "lat": 37.6946,
  "lon": -82.7711,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Prestonsburg, KY; 22 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Bluegrass Primary Health Care Center, Inc.",
  "city": "Lexington",
  "state": "KY",
  "lat": 38.0492,
  "lon": -84.5218,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Lexington, KY; 7 active sites on its HRSA scope (other).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Bowling Green-Warren County Primary Care Center, Inc.",
  "city": "Bowling Green",
  "state": "KY",
  "lat": 36.967,
  "lon": -86.3998,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Bowling Green, KY; 1 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Clover Fork Outpatient Medical Project Inc.",
  "city": "Evarts",
  "state": "KY",
  "lat": 36.9717,
  "lon": -82.9763,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Evarts, KY; 24 active sites on its HRSA scope (na).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Community Health Centers of Western Kentucky, Inc.",
  "city": "Greenville",
  "state": "KY",
  "lat": 37.1967,
  "lon": -87.191,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Greenville, KY; 6 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Cumberland Family Medical Center, Inc.",
  "city": "Burkesville",
  "state": "KY",
  "lat": 37.0611,
  "lon": -85.0672,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Burkesville, KY; 232 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "East Kentucky Health Service Center",
  "city": "Hindman",
  "state": "KY",
  "lat": 37.3134,
  "lon": -82.9357,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Hindman, KY; 1 active sites on its HRSA scope (na).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Faith Healthcare Inc.",
  "city": "Monticello",
  "state": "KY",
  "lat": 37.1077,
  "lon": -84.0735,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Monticello, KY; 9 active sites on its HRSA scope (na).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Family Health Centers, Inc.",
  "city": "Louisville",
  "state": "KY",
  "lat": 38.2706,
  "lon": -85.7847,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Louisville, KY; 14 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Grace Community Health Center",
  "city": "Corbin",
  "state": "KY",
  "lat": 36.9285,
  "lon": -84.1045,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Corbin, KY; 41 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Health First Bluegrass",
  "city": "Lexington",
  "state": "KY",
  "lat": 38.0207,
  "lon": -84.529,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Lexington, KY; 22 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Health Help, Incorporated",
  "city": "Richmond",
  "state": "KY",
  "lat": 37.733,
  "lon": -84.3078,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Richmond, KY; 12 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Health Point Family Care, Inc.",
  "city": "Newport",
  "state": "KY",
  "lat": 39.0878,
  "lon": -84.4936,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Newport, KY; 32 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Helping Hands Health Clinic, Inc.",
  "city": "Elkton",
  "state": "KY",
  "lat": 36.7952,
  "lon": -87.1619,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Elkton, KY; 1 active sites on its HRSA scope (na).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Juniper Health, Inc.",
  "city": "Beattyville",
  "state": "KY",
  "lat": 37.5597,
  "lon": -83.3949,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Beattyville, KY; 24 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Kentucky Mountain Health Alliance, Inc.",
  "city": "Hazard",
  "state": "KY",
  "lat": 37.2811,
  "lon": -83.2196,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Hazard, KY; 5 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Kentucky River Foothills Development Council",
  "city": "Richmond",
  "state": "KY",
  "lat": 37.8536,
  "lon": -83.9163,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Richmond, KY; 8 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Lewis County Primary Care Center Inc.",
  "city": "Vanceburg",
  "state": "KY",
  "lat": 38.5825,
  "lon": -83.3278,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Vanceburg, KY; 21 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Monticello Medical Associates, Inc.",
  "city": "Monticello",
  "state": "KY",
  "lat": 36.8184,
  "lon": -84.8714,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Monticello, KY; 6 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Mountain Comprehensive Care Center, Inc.",
  "city": "Prestonsburg",
  "state": "KY",
  "lat": 37.4798,
  "lon": -82.5181,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Prestonsburg, KY; 26 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Mountain Comprehensive Health Corporation",
  "city": "Whitesburg",
  "state": "KY",
  "lat": 36.6255,
  "lon": -83.7033,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Whitesburg, KY; 34 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "One Cross Community Inc.",
  "city": "Campbellsville",
  "state": "KY",
  "lat": 37.3518,
  "lon": -85.3548,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Campbellsville, KY; 2 active sites on its HRSA scope (na).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Park Duvalle Community Health Center Inc.",
  "city": "Louisville",
  "state": "KY",
  "lat": 38.2272,
  "lon": -85.8071,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Louisville, KY; 7 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Pennyroyal Healthcare Services, Inc.",
  "city": "Princeton",
  "state": "KY",
  "lat": 37.1116,
  "lon": -87.8801,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Princeton, KY; 4 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Ramey-Estep Homes Inc.",
  "city": "Rush",
  "state": "KY",
  "lat": 38.2936,
  "lon": -82.7725,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Rush, KY; 1 active sites on its HRSA scope (na).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Regional Health Care Affiliates, Inc.",
  "city": "Providence",
  "state": "KY",
  "lat": 37.398,
  "lon": -87.7597,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Providence, KY; 11 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Shawnee Christian Healthcare Center Inc.",
  "city": "Louisville",
  "state": "KY",
  "lat": 38.2604,
  "lon": -85.8137,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Louisville, KY; 3 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Sterling Health Solutions, Inc.",
  "city": "Mount Sterling",
  "state": "KY",
  "lat": 38.0544,
  "lon": -83.9467,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Mount Sterling, KY; 33 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Triad Health Systems Inc.",
  "city": "Warsaw",
  "state": "KY",
  "lat": 38.7848,
  "lon": -84.9016,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Warsaw, KY; 24 active sites on its HRSA scope (corporate entity, federal tax exempt).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 },
 {
  "name": "Trinity Family Health, Inc.",
  "city": "Corbin",
  "state": "KY",
  "lat": 36.9599,
  "lon": -84.0749,
  "category": "fqhc",
  "note": "HRSA-funded community health center (FQHC) grantee based in Corbin, KY; 2 active sites on its HRSA scope (na).",
  "src": "HRSA Health Center Service Delivery and Look-Alike Sites data (data.hrsa.gov), downloaded 2026-11-10"
 }
]
