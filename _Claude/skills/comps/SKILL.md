---
name: comps
description: Fill the Comps tab in an Amazon CAR Page 0 .xlsx file from a broker/local comps .xlsx source. Geocodes missing lat/long via Nominatim and looks up missing zoning via web search. Use when Jason provides a CAR file and a comps spreadsheet and asks to fill in the comps tab.
---

# Comps Skill

Triggered by `/comps`. Reads lease comps from a source spreadsheet and writes them into the Comps tab of an Amazon CAR Page 0 file. Fills in missing lat/long (via Nominatim geocoding) and missing zoning (via web search) automatically.

---

## Step 1 — Identify files

Look in `Inputs/` for:
- **CAR file** (destination): matches `CAR Page 0*.xlsx` — this is the Amazon template
- **Comps source** (source): any other `.xlsx` in `Inputs/` that is NOT the CAR file and appears to contain comp data (e.g., "Comps", "Local Broker", "comp" in the filename)

If invoked with arguments (e.g., `/comps CAR Page 0 ZDT6.xlsx`), use the named file as the CAR file and auto-detect the comps source from the remaining `.xlsx` files in `Inputs/`.

If either file can't be determined unambiguously, **ask before proceeding**.

---

## Step 2 — Read the source comps

Load the source file with `openpyxl` (`data_only=True`). Find the `Comps` sheet (exact name).

The source sheet structure has **two leading `None` columns** before the data starts. The header row identifies the columns; find it by scanning for the row that contains `'#'` in it. Data rows follow immediately after the Example row.

Extract all comps (numbered rows where `#` is an integer). Collect these fields for each comp (column order matches both source and destination):

| Field | Notes |
|---|---|
| # | Integer comp number |
| Property Name | May be blank |
| Address | Street address |
| City | |
| State | |
| Zip Code | |
| Market | May be blank |
| Zoning | May be blank — **enrich if missing** |
| Latitude | May be blank — **geocode if missing** |
| Longitude | May be blank — **geocode if missing** |
| Year Built | |
| Building Class | |
| Total Building SF | |
| Building Status | |
| Occupancy Status | |
| Landlord | |
| Current Tenant | |
| Lease Transaction Type | New Lease / Sublease / Renewal |
| Leased SF | |
| Annual Base Rent (PSF) | |
| Lease Structure | NNN / MG / Plus Utilities / etc. |
| Term (mo) | |
| Free Rent (mo) | |
| Lease Execution | datetime |
| Lease Commencement Date | datetime |
| Tenant Improvement (PSF) | |
| Annual Escalations | |
| Comments | |

---

## Step 3 — Enrich missing lat/long

For any comp where Latitude or Longitude is `None`, geocode using the **Nominatim** API (no key required):

```python
import requests, time

def geocode(address, city, state, zip_code):
    query = f"{address}, {city}, {state} {zip_code}, USA"
    r = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={"q": query, "format": "json", "limit": 1},
        headers={"User-Agent": "KBC-Advisors-CAR/1.0"}
    )
    results = r.json()
    if results:
        return float(results[0]["lat"]), float(results[0]["lon"])
    return None, None

for comp in comps:
    if comp["Latitude"] is None or comp["Longitude"] is None:
        lat, lon = geocode(comp["Address"], comp["City"], comp["State"], comp["Zip Code"])
        comp["Latitude"] = lat
        comp["Longitude"] = lon
    time.sleep(1.1)  # Nominatim rate limit: 1 req/sec
```

If geocoding fails for a comp, leave the fields blank and flag it in the report.

---

## Step 4 — Enrich missing zoning

For any comp where Zoning is `None` or blank, attempt a **web search** using the WebSearch tool:

- Query: `"{address} {city} {state}" zoning`
- Look for the current zoning designation in municipal GIS sites, permit records, or real estate listings
- If a confident zoning code can be extracted (e.g., `I-1`, `M-2`, `General Industrial`), fill it in
- If the result is ambiguous or not found, leave blank and flag in the report

Don't spend more than one search per comp. If the first result doesn't yield a clear answer, note it as "manual lookup needed."

---

## Step 5 — Read the CAR destination file

Load `CAR Page 0 *.xlsx` with `openpyxl` (NOT `data_only=True` — preserve formulas on other sheets).

Find the `Comps` sheet. The structure:
- **Row 1**: Header row (cols A–AB, 28 columns)
- **Row 2**: Subject property row (leave untouched)
- **Row 3**: Example row (leave untouched)  
- **Rows 4–13**: Comp slots 1–10 (write comps here)
- **Rows 16–17**: Median/Average formula rows (leave untouched)

Column order in the destination (A=1 through AB=28) matches the source field order exactly.

---

## Step 6 — Write comps to destination

Write each enriched comp to its corresponding row (comp 1 → row 4, comp 2 → row 5, etc.):

```python
from openpyxl import load_workbook

wb_dst = load_workbook(dst_path)  # NOT data_only — preserve formulas
ws_dst = wb_dst['Comps']

fields = [
    "#", "Property Name", "Address", "City", "State", "Zip Code",
    "Market", "Zoning", "Latitude", "Longitude", "Year Built", "Building Class",
    "Total Building SF", "Building Status", "Occupancy Status", "Landlord",
    "Current Tenant", "Lease Transaction Type", "Leased SF", "Annual Base Rent (PSF)",
    "Lease Structure", "Term (mo)", "Free Rent (mo)", "Lease Execution",
    "Lease Commencement Date", "Tenant Improvement (PSF)", "Annual Escalations", "Comments"
]

for i, comp in enumerate(comps):
    dst_row = 4 + i
    for col_idx, field in enumerate(fields, start=1):
        ws_dst.cell(row=dst_row, column=col_idx, value=comp.get(field))

wb_dst.save(dst_path)
```

---

## Step 7 — Report back

Summarize in bullets:
- CAR file updated: filename, site code if visible
- Number of comps written
- Any lat/long geocoded (address → coords)
- Any zoning filled in or flagged for manual lookup
- Any comps where enrichment failed

Example:
> Comps tab updated — `CAR Page 0 ZDT6.xlsx`.
> - 4 comps written (rows 4–7)
> - Lat/long already present on all 4
> - Zoning: all 4 had values from source
> - Average rent PSF from formula row: $11.87

---

## Rules

- Never overwrite the Subject row (row 2) or Example row (row 3)
- Never touch the Median/Average formula rows (rows 16–17)
- Never overwrite non-Comps sheets — load without `data_only=True` to preserve formulas
- If more than 10 comps are found in the source, warn Jason — the template only has 10 slots; ask which to include
- If the CAR file is open in Excel, the save will fail — tell Jason to close it first
- Nominatim rate limit is 1 request/second — always sleep 1.1s between geocoding calls
