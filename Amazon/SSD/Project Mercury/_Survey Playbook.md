---
program: Project Mercury
business_unit: SSD
area: Amazon
tags: [project-mercury, amazon, playbook]
last_updated: 2026-08-11
last_note: "Created survey playbook + 9 MSA workbooks seeded from intern data"
---

# Project Mercury — Survey Playbook

How surveys get built, maintained, and brought to debrief. One workbook per MSA, Amazon's SSD Multi Pin format, living documents until the MSA is solved.

## The Deliverable

**One workbook per MSA** at `C:\Users\kirkham\Documents\Amazon\Project Mercury\Surveys\{MSA} - SSD Survey.xlsx`, with two tabs in Amazon's exact SSD Multi Pin column format (copied from the Kansas City examples):

- **Building Survey** — full Amazon column set: location, site details (SF, clear height, load type, docks, parking, power), economics (sale/lease, rate, price, OpEx), comments
- **Land Survey** — owner, acreage, zoning, construction status, power, distance, economics

Within each tab, candidates are grouped **per pin** under a grey band row showing the pin ID, city/zip, launch date, and pin coordinates. Pins with no candidates carry a `None` row (Amazon's own convention — shows the pin was surveyed, not skipped). Candidates are sorted by distance from pin.

> Deviation from Amazon's vanilla template: the KC examples separate pin groups with unlabeled blank rows. Band rows were added because 9 unlabeled groups is unusable. If Amazon wants the vanilla layout for submission, delete the band rows — columns are untouched.

## Survey Criteria (from Amazon)

| Test | Pass | Backup | Fail |
|---|---|---|---|
| Distance from pin | ≤ 3 mi | 3–5 mi | > 5 mi (only if truly nothing else — flag it) |
| Building | 75k–450k SF available | Larger if divisible | — |
| Land | 7–30 ac | > 30 ac if divisible (note it) | < 7 ac |
| Zoning | Industrial | Retail box convertible to storage/distribution | — |

Plus: don't over-index on launch year — Amazon wants pull-left options. A 2031 pin with a great 2028-ready site is worth surfacing.

## Per-Pin Sourcing Checklist

For every pin, in order:

1. **CoStar building search** — 3 mi radius from pin lat/long, industrial + flex, 75k–450k SF available. Expand to 5 mi if under ~3 viable results.
2. **CoStar land search** — same radius approach, 7–30 ac, industrial/commercial zoning. Include larger divisible tracts.
3. **CoStar retail box search** — freestanding retail ≥ 75k SF (dead big boxes, former Kmart/Sears/grocery DCs). Criteria item 3 explicitly puts these in scope; the intern pass had zero.
4. **Planned/proposed inventory** — spec pipelines, BTS parks, developer land positions (NorthPoint, VanTrust, Core5, Scannell, etc.). The KC example surveys lean heavily on planned product; a "Planned/Proposed" row with TBD specs is a valid entry.
5. **Off-market / municipal** — city- and county-owned industrial parks, port authority land, economic development inventory. KC survey includes city-owned sites with incentive notes.
6. **Local broker call** — one call per market once the CoStar pass is done. Off-market and quiet-marketed sites won't be in CoStar.

**Minimum bar per pin:** 3+ candidates across building + land combined, or a documented statement of why the market is empty. A pin with one candidate isn't surveyed — it's a coin flip.

## Population Workflow (per MSA)

1. **Rebuild CoStar saved searches** against 7.29 pin coordinates (≈25 of the old searches are dead; carried pins' searches remain valid).
2. Run the per-pin sourcing checklist above.
3. **Screen** every candidate: compute straight-line distance from pin, check size/zoning against criteria. Out-of-criteria sites may stay **with a flag in Comments** (e.g., "outside 5-mi backup radius", "check divisibility") — Jason cuts, not the sourcing pass.
4. **Populate** the MSA workbook. Every row gets: coordinates, distance, owner, size, zoning, status, sale/lease + pricing where known, listing broker in Comments, flyer link when available.
5. **QA pass:** dedupe, fix CoStar name garbage ("Hwyive", trailing spaces), verify coordinates land where the address says, confirm distances.
6. **Rank within pin** by distance and fit; add a one-line rationale in Comments for the top candidates.
7. **Mark survey-ready** — update the pin's Status in the MSA vault file, then tell Dominic which sites are ready so he can slot the debrief.

## Priority Order

2028 launches first, then debrief-priority MSAs, then the rest:

1. **Cincinnati** — 3× 2028-09 pins (41018, 45002, 45174) ⭐
2. **Toledo** — SOHA 2028-09 ⭐
3. **Cleveland** — 44215 2028-10 ⭐
4. **Columbus** — 43054 2028-10 ⭐
5. Remaining 2029 pins in the four priority MSAs
6. Louisville / Lexington / Nashville / Charleston WV / Morgantown PA (2029–2031, no debrief priority)

## Maintaining the Surveys

- The workbook is the single source of truth per MSA. New flyers, broker responses, and CoStar updates get merged into the existing row (or added as a new row) — never a parallel list.
- When a candidate advances (tour, LOI, debrief selection), fill the Survey Review columns (WHS Risk, Approved HC, Selection Status) as Amazon supplies them.
- Mirror only the headline into the vault: the pin's `Status` and `Candidate Site` columns in the MSA file. Detail lives in the workbook.

## Roles

- **Jason** — final screen, ranking, broker calls, debrief presentation.
- **Intern/support** — CoStar pulls and initial population **into the MSA workbook directly, in Amazon's format**. No side spreadsheets. Every row must have coordinates, distance, and size or it doesn't go in.
- **Jack** — distance/criteria screening, QA, flyer intake (see below), workbook maintenance, vault sync.

## Flyer Intake (proposed skill)

`/survey-intake` — feed it a flyer PDF, broker email (.msg), CoStar export, or pasted listing text + the MSA (pin optional):

1. Extract property fields (name, address, SF/acreage, clear height, docks, pricing, broker).
2. Geocode if no coordinates; compute distance to the nearest pin(s) in that MSA.
3. Screen against criteria; build the Comments flags.
4. Append to (or update the matching row in) the MSA workbook, correct tab, correct pin group.
5. Report back: what was added, where it landed, any criteria flags.

Status: **built 2026-08-11** — `_Claude/skills/survey-intake/`. Handles PDF flyers, .msg emails, CoStar exports, images, and pasted text; geocodes via Nominatim, assigns to nearest pin, dedupes, flags criteria violations. Windows work machine only.

## Source Files

- Templates: `Inputs\SSD Multi Pin Building Survey.xlsx`, `Inputs\SSD Multi Pin Land Survey.xlsx` (KC market examples)
- Intern first pass (superseded, data absorbed into Cincinnati/Cleveland workbooks): `Inputs\Project Mercury 7.29 Update.xlsx`
- Pin data: `[[_Overview]]` and per-MSA files in this folder
