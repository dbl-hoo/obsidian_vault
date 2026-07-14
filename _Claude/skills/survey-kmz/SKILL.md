---
name: survey-kmz
description: Build a nested-folder KMZ of site-survey results — one folder per MSA/pin with radius rings and color-coded land vs. building candidate placemarks. Use when Jason asks to build/update the Project Mercury KMZ or any survey KMZ from a pin list + candidate property spreadsheet.
---

# Survey KMZ Skill

Builds a Google Earth KMZ that visualizes site-survey results: target pins with radius rings, and candidate properties color-coded by type (land vs. building), organized in collapsible folders per pin and per MSA.

Triggered by `/survey-kmz`, "build the Mercury KMZ", "update the KMZ", or similar.

## Inputs

Two data sources. Ask for whichever is missing — don't guess paths.

1. **Pin list** — one row per target pin: pin ID, MSA, lat/long, launch date (or other description text).
   - *Project Mercury default:* `C:\Users\kirkham\Documents\Amazon\Project Mercury\Project Mercury 2026.xlsx`, filtered to `Broker = "Jason Kirkham"` (41 rows).
2. **Candidate properties** — one row per candidate: address (or lat/long), source pin ID, type (Land | Building), plus any detail worth showing in the placemark balloon (SF/acreage, zoning, price, broker).
   - *Project Mercury default:* the merged master XLS of the intern's CoStar exports (land + building). If it doesn't exist yet, stop and say so.

If candidates have addresses but no coordinates, geocode via Nominatim (same approach as the `/comps` skill): 1 req/sec, descriptive User-Agent, cache results to a sidecar CSV next to the source file so re-runs don't re-geocode.

## KMZ Structure

```
{Project}.kmz
└── {Project} (root document)
    └── {MSA name}                      ← folder
        └── {Pin ID, e.g. Cincinnati41011}   ← folder
            ├── Pin placemark — target lat/long; description = launch date + any notes
            ├── 3-mile radius ring — unfilled polygon, thin solid border
            ├── 5-mile radius ring — unfilled polygon, dashed border
            ├── Building Options         ← folder, yellow placemarks
            └── Land Options             ← folder, green placemarks
```

Design intent: folder collapse in Google Earth toggles whole pins/MSAs on and off; color alone distinguishes land (green) from building (yellow).

## Build Rules

- **Build programmatically** — Python `simplekml`, output `.kmz` (it zips for you). Write the script to the scratchpad; the KMZ goes wherever Jason says (default: same folder as the pin-list spreadsheet).
- **Radius rings:** KML has no circle primitive. Generate each ring as a ~64-point polygon: for bearing θ in 0..360 step ~5.6°, project the radius from the pin using the haversine/spherical formula (or `geographiclib`). `outerboundaryis` only, `polystyle.fill = 0`.
  - 3-mile ring: solid line, width 2.
  - 5-mile ring: dashed look — KML lines can't truly dash; approximate with a thinner, semi-transparent line (e.g. width 1, ~50% alpha) and note the legend in the root document description.
- **Placemark styles:** shared styles defined once on the document, not per-placemark (keeps file size down). Yellow pushpin for building, green for land, a distinct icon (e.g. target/crosshair) for the pin itself.
- **Balloon content:** candidate placemark description = address, SF/acreage, zoning, and source-pin distance. Keep it plain HTML-free text unless Jason asks otherwise.
- **Skip, don't drop silently:** any candidate row that fails geocoding or has no parseable type goes in a "Skipped rows" list in the final report.

## Two-Pin Overlap Check

After placing candidates, for each candidate compute haversine distance to **every** pin in its MSA (not just its source pin). Flag any candidate within the 5-mile radius of 2+ pins:

- Add `⚠ Also within X mi of {other pin}` to its balloon description.
- List all flagged candidates in the final report — these are sites that might satisfy two PDC targets at once.

Pure geometry on data already in hand — no external API.

## Workflow

1. Confirm both input files exist and read them; report row counts before building.
2. **First run for a project: mock up ONE pin** (Mercury default: Cincinnati41011), deliver the KMZ, and get Jason's sign-off on styling before scaling to all pins.
3. Full build: all pins, all candidates, overlap check.
4. Report: output path, pin count, candidate counts (land/building), overlap flags, skipped rows.

## Sharing Note

This skill is self-contained except for the *Project Mercury default* paths above — anyone reusing it should swap those two inputs for their own pin list and candidate spreadsheet. Everything else (structure, ring generation, overlap check) is generic.
