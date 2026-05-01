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

**KBC matters:** flat file at `KBC/{Matter Name}.md`, docs folder at `KBC_DOCS\{Matter Name}\`

**Kirkham Law matters:** flat file at `Kirkham Law/{Matter Name}.md`, docs folder at equivalent path

### Step 3b — Extract and save attachments
After the docs folder exists, extract attachments from the source file using Python:

**.msg files** — use `extract-msg`:
```python
import extract_msg
msg = extract_msg.Message('C:/Users/kirkham/Documents/Vault/Inputs/filename.msg')
for att in msg.attachments:
    att.save(customPath='<docs_folder_path>/')
```

**.pdf files** — use `pymupdf` to extract embedded attachments (if any); the PDF itself is the document, copy it to the docs folder directly.

**.eml files** — use `extract-msg` or Python's `email` stdlib to extract attachments.

**After extraction:**
- Note all saved filenames in the intake note (e.g. "Attachments saved: redlined_amendment.docx")
- If an attachment filename reveals the property name or matter name more precisely than the email subject, update the matter name before creating the vault file
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
start_date:
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

### Step 6 — Report back
Summarize in 3–5 bullet points:
- Matter created (area, program if Amazon, office if KBC)
- What arrived (document type, from whom)
- Attachments saved (filenames) or "no attachments"
- What's being asked of Jason
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
1. Extracts: matter = "Ferguson MSA", area = KBC, office = Atlanta, contacts = Randy Hogan (Ferguson) + Todd Steffen (KBC)
2. Creates `KBC/Ferguson MSA.md` and `KBC Legal\Ferguson MSA\`
3. Logs note: email from Randy Hogan with clean + redlined MSA; Todd asking Jason to review and return critical redlines
4. Adds task: `- [ ] Review Ferguson MSA redlines and respond with critical comments 📅 2026-04-23`

**Jack reports:**
> Matter created: Ferguson MSA (KBC / Atlanta).
> - Randy Hogan (Ferguson) sent clean + redlined MSA; forwarded by Todd Steffen for Jason's review
> - Task added due 4/23
> - Docs folder created at KBC Legal\Ferguson MSA\

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
