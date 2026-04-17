---
name: intake
description: Create a new KBC or Kirkham Law matter file from a saved email or pasted text. No substantive legal review.
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
- **Matter name** — derive from subject line or content (e.g. "Ferguson MSA", "Smith v. Jones", "Action Logistics Commission Agreement")
- **Area** — KBC or Kirkham Law
- **KBC office** — infer from context (which KBC broker is involved, where meeting occurred, etc.)
- **Counterparty** — company or person name
- **Key contacts** — names, emails, roles on both sides
- **What's being asked** — log it as a note entry; do NOT act on any legal request

If any of the above can't be determined, ask before creating the file.

### Step 3 — Create the matter file
- **KBC matters:** flat file at `KBC/{Matter Name}.md` — no subfolder in the vault
- **Kirkham Law matters:** flat file at `Kirkham Law/{Matter Name}.md` — no subfolder in the vault
- Create the matching docs folder at `KBC_DOCS\{Matter Name}\` or equivalent (docs folder still exists, vault file does not)

### Step 3b — Extract and save attachments
After the docs folder exists, extract attachments from the source file using Python:

**.msg files** — use `extract-msg`:
```python
import extract_msg
msg = extract_msg.Message('C:/Users/kirkham/Documents/Vault/Inputs/filename.msg')
for att in msg.attachments:
    att.save(customPath='C:/Users/kirkham/Documents/KBC Legal/{Matter Name}/')
```

**.pdf files** — use `pymupdf` to extract embedded attachments (if any); the PDF itself is the document, copy it to the docs folder directly.

**.eml files** — use `extract-msg` or Python's `email` stdlib to extract attachments.

**After extraction:**
- Note all saved filenames in the intake note (e.g. "Attachments saved: redlined_amendment.docx")
- If an attachment filename reveals the property name or matter name more precisely than the email subject, use that — update the matter name before creating the vault file if needed
- Skip image attachments (inline logos, signatures) — only save substantive documents
- If no attachments, note that explicitly

**KBC YAML:**
```yaml
project:
status: Ongoing
area: KBC
office:          # Atlanta | Austin | Chicago | Columbus | Dallas | Houston
                 # Los Angeles | Manhattan Beach | Nashville | New Jersey | New York
                 # Newport Beach | Oakland | On Location | Philadelphia | Phoenix
                 # Seattle 238 | Seattle 290 | West Texas
tags: [kbc]
last_updated:    # today's date
```

**Kirkham Law YAML:**
```yaml
project:
status: Ongoing
area: Kirkham Law
tags: [kirkham-law]
last_updated:    # today's date
```

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
- Matter created
- What arrived (document type, from whom)
- Attachments saved (filenames) or "no attachments"
- What's being asked of Jason
- Any open questions or ambiguities to flag
- Do NOT offer to do the legal work

---

## Rules

- **No substantive review** — do not analyze, summarize, redline, or opine on any legal document. Jason does that himself.
- **Log and flag** — describe what arrived and what's being asked; leave the legal judgment to Jason
- **Don't create files speculatively** — if the matter name or area is ambiguous, ask first
- **One task per matter** — enough to surface it, not a full breakdown of legal to-dos
- If a matter file already exists for the same counterparty/project, update it rather than creating a duplicate

---

## Example

**Input:** Email saved to `Inputs/FW KBC Ferguson MSA comments.msg`

**Jack does:**
1. Extracts: matter = "Ferguson MSA", area = KBC, office = Atlanta, contacts = Randy Hogan (Ferguson) + Todd Steffen (KBC)
2. Creates `KBC/Ferguson MSA.md` and `KBC Legal\Ferguson MSA\`
3. Logs note: email from Randy Hogan with clean + redlined MSA; Todd asking Jason to review and return critical redlines; two open questions on rebate language
4. Adds task: `- [ ] Review Ferguson MSA redlines and respond with critical comments 📅 2026-04-23`

**Jack reports:**
> Matter created: Ferguson MSA (KBC / Atlanta).
> - Randy Hogan (Ferguson) sent clean + redlined MSA to Todd Steffen; forwarded for Jason's review
> - Todd flagging two rebate language questions before reaching out to Ferguson
> - Task added due 4/23
> - Docs folder created at KBC Legal\Ferguson MSA\
