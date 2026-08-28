---
program: Project Mercury
business_unit: SSD
area: Amazon
total_pins_assigned: 35
tags: [project-mercury, amazon]
last_updated: 2026-08-27
last_note: "Added full RE BRS Summary (Orbital): dock doors 11-12, DP parking 40-53, power/slab/short-side specs"
---

## Background

Amazon SSD site-search program for net new SSD pins launching 2028–2031. Debrief format is **MSA-level strategy** — solve an entire MSA to 80% PDC (Topology provides guidance on calls) before engaging Topology to reassess remaining centroid locations.

**Current dataset: 7.29 recut** (Dominic Nicholas email 2026-07-30). 726 pins total across 18 KBC brokers — a net reduction of 32 centroids from the original 758. Of the 726, 417 are new assignments and 309 carried over.

**Jason's book: 35 pins across 9 MSAs** (was 41 across 16). 18 new / 17 carried per Amazon's count.

TMs still not assigned — KBC is debriefing all site opportunities out of SST.

## Status — Debriefs

Debriefs start **week of 2026-08-03**, prioritizing MSAs containing **2028 requirements**. Four of Jason's MSAs are on Amazon's 58-MSA priority list:

- [[Cincinnati]] (KY, OH)
- [[Cleveland]] (OH)
- [[Columbus]] (OH)
- [[Toledo]] (OH)

Action from Dominic: review surveys against the updated pins and tell him which sites are ready to bring to debrief so he can populate the schedule. Amazon is loading the new pins into Lens/SHIELD and updating Workdocs folders — Dominic to confirm when done. Another check-in call expected early the week of 8/3, before the first debrief session.

## MSA Files (35 pins)

| MSA | Pins | New | Carried | 2028 | Priority |
|---|---|---|---|---|---|
| [[Cincinnati]] | 9 | 6 | 3 | 3 | ⭐ |
| [[Cleveland]] | 9 | 7 | 2 | 1 | ⭐ |
| [[Columbus]] | 7 | 3 | 4 | 1 | ⭐ |
| [[Toledo]] | 4 | 2 | 2 | 1 | ⭐ |
| [[Louisville]] | 2 | 1 | 1 | — | |
| [[Lexington]] | 1 | 0 | 1 | — | |
| [[Nashville]] | 1 | 0 | 1 | — | |
| [[Charleston, WV (new)]] | 1 | 0 | 1 | — | |
| [[Morgantown, PA (new)]] | 1 | 0 | 1 | — | |

**Launch-year mix:** 2028 → 6 · 2029 → 15 · 2030 → 4 · 2031 → 10. The whole book pulled left; the original dataset had nothing before 2029-03.

## What Changed in the 7.29 Recut

**25 pins deleted** — all removed from the dataset entirely (not reassigned to another broker):

| MSA (old naming) | Deleted pins |
|---|---|
| Cincinnati-Hamilton | Cincinnati41011, 41094, 45052, 45150, 45157, 45212 |
| Dayton-Springfield | Cincinnati45410, 45440 |
| Cleveland-Akron | Cleveland44054, 44074, 44086, 44092, 44139, 44233, 44276 |
| Youngstown-Warren | Cleveland44509 |
| Mansfield | Cleveland44905 |
| Columbus | Columbus43061, 43203, 43221 |
| Huntington-Ashland | Huntington-Ashland, WV (new)25703 |
| Lexington | Lexington40003 |
| Steubenville-Weirton | Pittsburgh43953 |
| Toledo | Toledo43566, 43606 |

**19 pins added** (by site_code; Amazon's own count says 18 new — the delta is likely `SOHA`, which carries a facility code rather than a metro+zip code): Cincinnati41018, 41059, 45002, 45174, 45430, 45449 · Cleveland44022, 44035, 44077, 44138, 44147, 44215, 44437 · Columbus43026, 43054, 43240 · Louisville40026 · SOHA (Waterville, OH) · Toledo43613.

**16 pins carried over**, all with identical coordinates but **every one had its launch date changed** — mostly pulled left (e.g. Cleveland44243 2031-06 → 2029-01, Cincinnati45011 2030-03 → 2029-01). Per-pin detail is in each MSA file.

**MSA naming collapsed.** Amazon dropped the long CMSA/MSA labels for plain metro names, and seven of Jason's former MSAs are gone from his book entirely: Dayton-Springfield (folded into Cincinnati), Canton-Massillon and Youngstown-Warren (folded into Cleveland), Lima (folded into Toledo), and Mansfield, Steubenville-Weirton, Huntington-Ashland (all pins deleted). Pre-recut MSA files are preserved in `x_Archive/Project Mercury (pre-7.29 recut)/`.

## Survey Impact

The CoStar saved searches were built one per pin against the **old** centroids. Of the 38 saved searches, roughly 25 are now dead and 19 new pins have no search. Carried-over pins keep the same coordinates, so those searches remain valid — but the launch-date pull-left changes the urgency ranking on all of them.

## Search Criteria

- **Search radius:** 3 miles from pin (lat/long given per pin). Up to 5 miles considered as backup if nothing viable within 3.
- **Size:**
   - Building: 120,000 – 145,000 SF
   - Land: 7 – 30 acres
- **Clear height:** 32' — can go lower if the building is on the large end of the range, but that rules out orbital.
- **Dock doors:** 11–12
- **Associate parking:** 180–220 spots
- **DP (flex) parking:** 40–53 spots
- **Preferred IB/OB location:** Adjacent
- **Min building short-side dimension:** 244'
- **Power:** 1,200 KW or 1,600 Amps at 480V (does not include added cooling for heat rejection, ~350kW additional)
- **Slab on grade:** 6" minimum thickness, 4,000 PSI, unreinforced
- **Design type:** Orbital
- **Daily volume (Orbital):** GM (sort + non-sort) 49,000 · Injection capacity 37,000 · Perishable 25,000 · Hazmat 1,000 · Total window-solve volume 112,000
- **Total building size needed (Orbital + process + perishable):** 115,287 SF
- **Hazmat capacity:** 1,000 SF · **Pharmacy:** 1,800 SF · **Prime Air:** 1,913 SF


## Search Methodology

One CoStar saved search per pin. For each pin:

1. Building search — radius 3 miles from pin lat/long. If nothing viable, expand to 5 miles.
2. Land search — same radius approach (3 miles, expand to 5 if nothing viable).

## Key Contacts

- **Dominic Nicholas** (Amazon SSD) — kickoff/debrief lead, (510) 435-5154, hnidomin@amazon.com
- **Ashleigh Sundet** (Amazon SSD) — backup for KMZ/Lens/survey questions

## Source Files

`C:\Users\kirkham\Documents\Amazon\Project Mercury\`:

**Current (7.29 recut):**
- `Project Mercury 2026 7.29 Update - KBC Brokers.xlsx` — all 726 pins by KBC broker, plus a Change Analysis tab
- `Project Mercury 2026 7.29 Update.xlsx` — same data, Amazon-wide view
- `Project Mercury 2026 - MSA Level.kmz` — all pins organized by MSA folder
- `Project Mercury 2026 - by MSA.zip` — one KMZ per MSA

**Superseded (original dataset):**
- `Project Mercury 2026.xlsx` — original 758 pins
- `Project Mercury.kmz` — original pin map
- `Mercury_Search_Plan.csv` — per-pin CoStar search plan, built against old centroids

## Tasks

## Notes

2026-08-27 - Added full RE BRS Summary (Orbital design type) to search criteria: dock doors corrected to 11-12 (was 11), DP/flex parking corrected to 40-53 (was 40-55), plus preferred IB/OB adjacent, 244' min short-side dimension, power (1,200 KW/1,600A @ 480V), slab-on-grade spec, and daily volume/capacity figures.

2026-08-27 - Updated building program requirements: 120K-145K SF (replaces old 75K-450K screening range), 40-55 flex spots, 180-220 parking spots, 32" clear height (can go lower if building is on the large end, but that rules out orbital), 11 dock doors.

2026-08-11 - Built /survey-intake skill: feed it a flyer PDF, broker .msg, CoStar export, image, or pasted listing + MSA → extracts fields, geocodes, assigns to nearest pin, screens criteria, inserts/updates the row in the MSA survey workbook. Tested end-to-end (insert, dedupe-update, placeholder replacement, criteria flags).

2026-08-11 - Built survey infrastructure. Assessed intern first pass (Joe outsourced initial surveys): Cincinnati land coverage salvageable, building coverage thin (4 of 9 pins zero candidates), wrong format, no distances/economics/retail-box search. Created 9 per-MSA survey workbooks in Amazon's SSD Multi Pin format at `Documents\Amazon\Project Mercury\Surveys\`, seeded with the intern's usable candidates (auto-flagged for distance/size violations). Wrote [[_Survey Playbook]] — sourcing checklist, population workflow, priority order, proposed /survey-intake flyer skill.

2026-07-31 - Processed Dominic Nicholas's 7.29 pin recut email (sent 2026-07-30). Jason drops from 41 pins to 35: 25 old centroids deleted outright, 19 added, 16 carried (all with shifted launch dates, coordinates unchanged). MSA count falls 16 → 9 as Amazon collapsed the CMSA labels and folded Dayton, Canton, Youngstown and Lima into their parent metros. Six pins now carry 2028 launches. Cincinnati, Cleveland, Columbus and Toledo are on Amazon's 58-MSA priority list; debriefs begin week of 8/3. Rebuilt all MSA files from the new dataset; archived the pre-recut files. Attachments saved to the Project Mercury docs folder.

2026-06-23 - Kickoff email received from Dominic Nicholas. 41 pins assigned across 16 MSAs, launch years 2029-2031. Loaded into per-MSA files. Strategy shifting to MSA-level solve (80% PDC target) vs. per-pin debriefs; TMs not yet assigned.
