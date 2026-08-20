---
name: intake
description: Create a new Amazon, KBC, or Kirkham Law matter file from a saved email or pasted text. No substantive legal review.
---

# Intake Skill

Triggered by `/intake`. Creates a new matter file from an email saved to `Inputs/` or text pasted directly into the chat.

**Jason handles all substantive legal work himself. This skill handles file creation and logging only.**

---

## Workflow

### Step 1 — Find the source
- If invoked with no argument: check `Inputs/` for any new `.msg`, `.eml`, `.txt`, or `.pdf` files not yet processed
- If invoked with a filename argument (e.g. `/intake FW KBC Ferguson MSA comments.msg`): use that file
- If text is pasted directly into chat: use that as the source

### Step 2 — Extract matter details
Parse the source for:
- **Area** — Amazon | KBC | Kirkham Law
- **Matter name / site code** — derive from subject line or content
- **Counterparty** — company or person name
- **Key contacts** — names, emails, roles on both sides
- **What's being asked** — log it as a note entry; do NOT act on any legal request

**Amazon-specific fields to extract:**
- **Program type** — AMZL | GCF | Middle Mile | Quick Commerce | Project A | Renewals | SSD
- **Site code** — e.g. CVG47, DOM8 (use `TBD_{City}` if not yet assigned)
- **Deal type** — Purchase | Lease | BTS | etc.
- **Business unit** — SORT | GCF | IXD | etc.
- **TM** — Amazon Transaction Manager name
- **Local broker** — if any

**KBC-specific fields to extract:**
- **KBC office** — infer from which KBC broker is involved or where the deal is located
- **Property address** — extract from the document body or attachment content; this drives the matter name and folder name. Look for patterns like `123 Main St`, `456 Oak Ave, Atlanta, GA`, or a property name tied to a known address. If not findable, fall back to the counterparty name (see naming rules below).

If any required fields can't be determined, ask before creating the file.

### Step 3 — Create the matter file

**Amazon matters:**
- File at `Amazon/{program_type}/{site_code}.md` — use the correct subfolder per program:

| Program | Subfolder |
|---|---|
| AMZL | `Amazon/AMZL/` |
| GCF | `Amazon/GCF/` |
| Middle Mile | `Amazon/Middle Mile/` |
| Quick Commerce | `Amazon/Quick Commerce/` |
| Project A | `Amazon/Project A/` |
| Renewals | `Amazon/Renewals/` |
| SSD | `Amazon/SSD/` |

- Create the matching docs folder:
  - Standard programs: `AMAZON_DOCS\{site_code}\`
  - Quick Commerce: `AMAZON_QC_DOCS\{site_code}\`
  - Project A: `AMAZON_PA_DOCS\{site_code}\`

**KBC matters:** flat file at `KBC/{name} - {matter_type}.md`, docs folder at `KBC_DOCS\{name} - {matter_type}\`
- `{name}` = street address if one can be found (e.g., `312 Clay St Columbus OH`); otherwise the counterparty company name (e.g., `Interchange Co`)
- `{matter_type}` = most specific type that fits (same list used for attachment stems)
- If neither an address nor a counterparty name can be determined, ask Jason before creating the file

**Kirkham Law matters:** flat file at `Kirkham Law/{Matter Name}.md`, docs folder at equivalent path

### Step 3b — Extract and save attachments
After the docs folder exists, extract attachments from the source file using Python.

**Filename convention for saved attachments:**

The `{stem}` differs by area:

| Area | Stem format | Example |
|---|---|---|
| Amazon | `{site_code} - {address}` (address if available) | `DOM9 - 1234 Morse Rd Columbus OH` |
| KBC / Kirkham Law | `{matter_type} - {name}` (address if available, otherwise counterparty name) | `Listing Agreement - 456 Oak Ave Atlanta GA` or `Exclusive Services Agreement - Interchange Co` |

Full filename: `{stem} - {YYYY.MM.DD}.{ext}`

- `YYYY.MM.DD` = today's date (from the system), dots as separators
- Omit the address segment (and its ` - ` separator) only if it truly cannot be found
- Sanitize all parts: replace `\ / * ? : " < > |` with `_` and strip leading/trailing spaces

**KBC/Kirkham Law matter types** — use the most specific type that fits:
`Lease` | `Lease Renewal` | `Listing Agreement` | `Purchase Agreement` | `PSA` | `MSA` | `NDA` | `Amendment` | `Assignment` | `Sublease` | `Engagement Agreement` | `Other`

**Name extraction for KBC/Kirkham Law matters** — scan the email body and attachment filenames (and attachment content if a .docx or .pdf is already extracted) for a street address. Look for patterns like `123 Main St`, `456 Oak Ave, Atlanta, GA`, property names tied to a known address, or any explicit address reference. If found, use the shortest unambiguous form (street + city, no zip needed). If no address is findable, use the counterparty company name instead. Only ask Jason if neither can be determined.

**.msg files** — use `extract-msg`:
```python
import extract_msg, os, re

def sanitize(s):
    return re.sub(r'[\\/*?:"<>|]', '_', s).strip()

msg = extract_msg.Message('C:/Users/kirkham/Documents/Vault/Inputs/filename.msg')
date_str = '2026.05.26'         # today's date from system, dots as separators

# Amazon:  stem = sanitize('DOM9 - 1234 Morse Rd Columbus OH')
# KBC:     stem = sanitize('Listing Agreement - 456 Oak Ave Atlanta GA')
stem = sanitize('<stem>')

SKIP_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.tiff'}

for att in msg.attachments:
    orig = att.longFilename or att.shortFilename or 'attachment'
    _, ext = os.path.splitext(orig)
    if ext.lower() in SKIP_EXTS:
        continue
    new_name = f'{stem} - {date_str}{ext}'
    with open(os.path.join('<docs_folder_path>', new_name), 'wb') as f:
        f.write(att.data)
```

**.pdf files** — use `pymupdf` to extract embedded attachments (if any); the PDF itself is the document, copy it to the docs folder using the same naming convention.

**.eml files** — use Python's `email` stdlib to extract attachments; apply the same renaming logic.

**After extraction:**
- Note all saved filenames in the intake note (e.g. "Attachments saved: Listing Agreement - 456 Oak Ave Atlanta GA - 2026.05.26.docx")
- If an attachment filename reveals the property address or matter type more precisely than the email subject, update the stem before saving
- Skip image attachments (inline logos, signatures) — only save substantive documents
- If no attachments, note that explicitly

---

## YAML Templates

**Amazon deal files:**
```yaml
site_code:
deal_type:       # Purchase | Lease | BTS | etc.
business_unit:   # SORT | GCF | IXD | etc.
status: Surveying
tm:
pcm:
launch_date:
start_date:     # today's date (date file is created)
end_date:
local_broker:
area: Amazon
tags: [deal, amazon]
last_updated:    # today's date
last_note:       # one-line summary of intake note
next_due:        # ISO date of first task, or blank
```

**KBC matters:**
```yaml
project:
status: Ongoing
area: KBC
office:          # Atlanta | Austin | Chicago | Columbus | Dallas | Houston
                 # Los Angeles | Manhattan Beach | Nashville | New Jersey | New York
                 # Newport Beach | Oakland | On Location | Philadelphia | Phoenix
                 # Seattle | West Texas
tags: [kbc]
last_updated:    # today's date
```

**Kirkham Law matters:**
```yaml
project:
status: Ongoing
area: Kirkham Law
tags: [kirkham-law]
last_updated:    # today's date
```

---

### Step 4 — Log the intake note
Prepend a dated entry to `## Notes` with:
- Who sent what to whom
- What's being asked of Jason (describe it — do NOT do it)
- Key contacts with email addresses
- Any deadlines mentioned

Format:
```
YYYY-MM-DD - [Source: email / pasted] Matter opened. {Summary of what arrived and what's being asked.}

**Key contacts:** Name, Role — email
```

### Step 5 — Add a task
Add a single placeholder task so the matter appears in Open Tasks:
```
- [ ] {Brief description of what Jason needs to do} 📅 {due date if stated, otherwise 1 week out}
```

Do NOT add tasks for substantive legal work beyond what Jason explicitly requests. One task is enough to surface the matter.

### Step 6 — Commission Tracker: DEPRECATED

Do not touch `Commission Tracker.xlsx` as part of intake. The tracker's structure changed (no more "Commission Tracker" sheet/TOTALS row — now a single `_Inputs` sheet with fixed formula ranges) and this step is on hold until Jason asks for it to be rebuilt against the new layout.

---

### Step 7 — Delete the input file
Delete the source file from `Inputs/` after all vault files and attachments have been saved:
```python
import os
os.remove('C:/Users/kirkham/Documents/Vault/Inputs/filename.msg')
```
Confirm deletion in the report.

### Step 8 — Report back
Summarize in 3–5 bullet points:
- Matter created (area, program if Amazon, office if KBC)
- What arrived (document type, from whom)
- Attachments saved (filenames) or "no attachments"
- What's being asked of Jason
- Input file deleted
- Any open questions or ambiguities to flag
- Do NOT offer to do the legal work

---

## Rules

- **No substantive review** — do not analyze, summarize, redline, or opine on any legal document. Jason does that himself.
- **Log and flag** — describe what arrived and what's being asked; leave the legal judgment to Jason
- **Don't create files speculatively** — if the matter name, area, or site code is ambiguous, ask first
- **One task per matter** — enough to surface it, not a full breakdown of legal to-dos
- **Amazon: site code required** — if no site code is assigned yet, use `TBD_{City}` and flag it
- If a matter file already exists for the same counterparty/project, update it rather than creating a duplicate

---

## Examples

**KBC input:** Email saved to `Inputs/FW KBC Ferguson MSA comments.msg`

**Jack does:**
1. Extracts: area = KBC, office = Atlanta, contacts = Randy Hogan (Ferguson) + Todd Steffen (KBC); reads attachment to find property address → `456 Peachtree St NE Atlanta GA`
2. Creates `KBC/456 Peachtree St NE Atlanta GA - MSA.md` and `KBC Legal\456 Peachtree St NE Atlanta GA - MSA\`
3. Logs note: email from Randy Hogan with clean + redlined MSA; Todd asking Jason to review and return critical redlines
4. Adds task: `- [ ] Review MSA redlines and respond with critical comments 📅 2026-04-23`

**Jack reports:**
> Matter created: 456 Peachtree St NE Atlanta GA - MSA (KBC / Atlanta).
> - Randy Hogan (Ferguson) sent clean + redlined MSA; forwarded by Todd Steffen for Jason's review
> - Task added due 4/23
> - Docs folder created at KBC Legal\456 Peachtree St NE Atlanta GA - MSA\

---

**Amazon input:** Email with a new AMZL LOI for a site in Columbus, OH — site code DOM9, TM is Rachel Elliott

**Jack does:**
1. Extracts: area = Amazon, program = AMZL, site code = DOM9, deal type = Lease, TM = Rachel Elliott
2. Creates `Amazon/AMZL/DOM9.md` and `Amazon\DOM9\` docs folder
3. Logs intake note with summary of what arrived
4. Adds task: `- [ ] Review LOI and respond 📅 {1 week out}`

**Jack reports:**
> Matter created: DOM9 (Amazon / AMZL).
> - LOI received from Rachel Elliott (TM)
> - Task added due {date}
> - Docs folder created at Amazon\DOM9\
