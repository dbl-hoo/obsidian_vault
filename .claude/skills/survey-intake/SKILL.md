---
name: survey-intake
description: Take a listing flyer (PDF), broker email (.msg), CoStar export (.xlsx), image, or pasted listing text and populate/update the matching Project Mercury MSA survey workbook — extracts fields, geocodes, assigns to the nearest pin, screens against SSD criteria, and inserts or updates the row. Use when Jason sends listing material for a Mercury pin/MSA ("add this to the Cincinnati survey", "flyer for 41018", "intake this listing").
---

# Survey Intake Skill

Triggered by `/survey-intake` or by Jason sending listing material for a Project Mercury market. Feeds one or more candidates into the per-MSA survey workbooks at `C:\Users\kirkham\Documents\Amazon\Project Mercury\Surveys\{MSA} - SSD Survey.xlsx`.

**Windows work machine only** — the Surveys folder doesn't exist on Dathomir/macOS. If not on Windows, say so and stop.

Survey format, criteria, and conventions live in `Amazon/SSD/Project Mercury/_Survey Playbook.md`. Pin lists live in the per-MSA files in `Amazon/SSD/Project Mercury/`.

---

## Step 1 — Identify the source and MSA

Source material can be:

| Input | Extract with |
|---|---|
| PDF flyer | pymupdf skill (`fitz`) |
| .msg broker email | extract-msg skill (body + attachments — process attached flyers too) |
| .xlsx (CoStar export, broker list) | openpyxl skill (`data_only=True`) |
| Image / screenshot | image-digest skill (Read the image directly) |
| Pasted text | just read it |

**MSA determination:** from Jason's message, the property's location, or ask. If the property's city/state doesn't obviously belong to one of the nine Mercury MSAs (Cincinnati, Cleveland, Columbus, Toledo, Louisville, Lexington, Nashville, Charleston WV, Morgantown PA), **ask — don't guess.** A single source may contain multiple candidates (CoStar exports usually do); process each.

## Step 2 — Extract fields

Pull everything available into one JSON object per candidate. Decide **building vs. land** from the listing (a land listing has acreage and no building SF; if a listing offers both, ask). Field keys:

Common: `name, address, city, state, zip, lat, lon, owner, flyer, comments, sale_lease, sale_price, power`
Building: `total_sf, avail_sf, office_sf, land_ac, year_built, building_status, building_type, occupancy, tenancy, current_tenant, prior_use, prior_tenant, date_available, sprinkler, zoning, clear_min, clear_max, load_type, docks, grade_doors, col_w, col_d, auto_parking, trailer_parking, rate_psf, opex_psf`
Land: `acreage, zoning, constr_status, price_per_acre`

Conventions:
- Listing broker/company goes in `comments` ("Listed by Colliers (John Gartner)") — the template has no broker column.
- Clear height "32'" → `clear_min: 32, clear_max: 32`; a range "28-32" → 28/32.
- Column spacing "54x50" → `col_w: 54, col_d: 50`.
- `flyer` = the source filename or listing name.
- Numbers as numbers, not strings. Don't invent values — omit what the source doesn't state.
- If the flyer quotes only a total price and acreage, compute `price_per_acre`.

## Step 3 — Geocode if needed

If the source has no lat/long, geocode via Nominatim (no key; sleep 1.1s between calls):

```python
import requests, time
r = requests.get("https://nominatim.openstreetmap.org/search",
    params={"q": f"{address}, {city}, {state} {zip}, USA", "format": "json", "limit": 1},
    headers={"User-Agent": "KBC-Advisors-Mercury/1.0"})
res = r.json()
lat, lon = (float(res[0]["lat"]), float(res[0]["lon"])) if res else (None, None)
```

If geocoding fails (intersection addresses, "SEC of X & Y"), try the cross-street or the city centroid **only to sanity-check the MSA** — then either ask Jason for coordinates or pass `--pin` explicitly and note the missing coords.

## Step 4 — Insert via the helper script

Write the candidate JSON to the scratchpad, then run:

```
python "<skill dir>/scripts/add_candidate.py" --msa Cincinnati --type building --json cand.json [--pin Cincinnati41018] [--overwrite]
```

The script handles the rest: finds the workbook (partial MSA name ok), assigns to the **nearest pin** by haversine (or `--pin` to force), computes distance, appends criteria flags to Comments (>5 mi, 3–5 mi backup ring, SF outside 75k–450k, acreage outside 7–30), **dedupes by address/name within the pin group** (fills blanks on match; reports conflicts unless `--overwrite`), replaces `None` placeholder rows, keeps the group distance-sorted, and renumbers. It prints a JSON report.

Handle these outcomes:
- **Candidate >5 mi from every pin in the MSA** — the row still lands on the nearest pin with a flag, but tell Jason explicitly; it may belong in a different MSA or nowhere.
- **Conflicts reported on a dedupe match** — show Jason old vs. new; re-run with `--overwrite` only if he says the new data wins.
- **Workbook open in Excel** — the script errors; tell Jason to close it.

## Step 5 — Report back

Bullets, terse:
- What was added/updated: property → workbook / tab / pin, distance, row action
- Criteria flags raised
- Anything skipped, ambiguous, or needing his call (coords not found, conflicts, >5 mi)

Do **not** log vault notes for routine one-flyer intakes. If a batch materially changes a pin's picture (e.g., first real candidates for an empty 2028 pin), offer to update the MSA file's Notes/status — don't do it unprompted.

## Rules

- Never guess the MSA or fabricate field values.
- Never create a new workbook — if the MSA workbook is missing, stop and flag it.
- Multiple candidates in one source: one JSON + one script run each; summarize in a single report.
- Out-of-criteria sites still go in **with flags** — Jason cuts, not intake.
