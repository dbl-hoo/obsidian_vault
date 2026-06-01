---
name: nda
description: Review an NDA against KBC Advisors' standing playbook — produces a written review memo and redlined .docx with tracked changes and Word comments. Invokes /intake to open the KBC matter first.
---

# NDA Review Skill

Triggered by `/nda` or `/nda {filename}`. Reviews an NDA against KBC Advisors' standing playbook. Always produces a Review Memo. Produces a Redlined DOCX when the NDA is a `.docx` file.

**Never do substantive legal drafting beyond the playbook-driven redlines documented here. Flag and recommend; Jason decides what to accept.**

---

## Workflow

### Step 0 — Locate the NDA file

- If invoked with a filename argument (e.g. `/nda "Acme NDA.docx"`): look for that file in `Inputs/` first, then try the path as given.
- If invoked with no argument: check `Inputs/` for `.docx`, `.pdf`, or `.txt` files not yet processed. If multiple candidates, ask Jason which one.
- If no file found anywhere, ask Jason to drop the file into `Inputs/`.

Confirm the file path before proceeding. Note the file format — redlines are only possible for `.docx`.

### Step 1 — Run Intake

Follow the intake skill workflow (`see .claude/skills/intake/SKILL.md`) to:
1. Extract the counterparty name from the document (sender, file name, or document parties)
2. Create `KBC/{Counterparty} NDA.md` (or ask Jason for the matter name if ambiguous)
3. Create `KBC_DOCS\{Counterparty} NDA\` docs folder (Windows only)
4. Save the NDA file to the docs folder with the standard naming convention:
   `NDA - {address if available} - {YYYY.MM.DD}.docx`
   (skip the address segment for NDAs — just `NDA - {YYYY.MM.DD}.docx`)
5. Log the intake note
6. Add a placeholder task: `- [ ] Review and respond to NDA 📅 {1 week out}`
7. Delete the source file from `Inputs/`

**Stop and confirm the matter name with Jason before proceeding if ambiguous.**

### Step 2 — Extract NDA text

**For .docx:**
```python
from docx import Document

doc = Document(r'C:\path\to\file.docx')
paragraphs = []
for para in doc.paragraphs:
    if para.text.strip():
        paragraphs.append(para.text.strip())

# Also get table text
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for para in cell.paragraphs:
                if para.text.strip():
                    paragraphs.append(para.text.strip())

full_text = '\n'.join(paragraphs)
print(full_text)
```

**For .pdf:** Use the `pymupdf` skill.
**For .txt:** Read directly.

### Step 3 — Analyze against the Playbook

Work through every section of the Playbook below. For each issue found:
- Note which paragraph or section of the NDA triggers it
- Classify as: 🔴 Flag (change needed) | 🟡 Note (flag only) | ✅ OK
- Draft the recommended replacement language where the Playbook provides it

### Step 4 — Produce the Review Memo

Output to chat AND save as `{Counterparty} NDA - Review Memo - {YYYY.MM.DD}.md` in the docs folder.

Format:
```
### {Counterparty} NDA — Review Against KBC Playbook

**✅ No Issues**
| Section | Notes |
|---|---|
| ... | ... |

**🔴 Flags & Recommended Changes**

1. **[Section name]** — {Plain-language explanation of the problem.}
   - *Recommended action:* Delete / Revise / Flag only
   - *Suggested language:* "{replacement text}"

2. ...
```

List flags in priority order — most critical first.

### Step 5 — Produce the Redlined DOCX (if .docx)

Use the XML editing workflow below to insert tracked changes and Word comments into a copy of the original. Save the output to the docs folder as:
`{Counterparty} NDA - Redlined - {YYYY.MM.DD}.docx`

See **Redline Workflow** section below for the full procedure.

### Step 6 — Update the matter file

Prepend a note to `## Notes` in the KBC matter file:
```
YYYY-MM-DD - NDA review complete against KBC playbook. {N} flags identified. Review memo and redlined DOCX saved to docs folder.
```

Update `last_updated:` to today's date.

### Step 7 — Report back

```
NDA Review — {Counterparty}

Matter: KBC/{Counterparty} NDA.md
Docs: KBC_DOCS\{Counterparty} NDA\

{N} flags found — see Review Memo for full breakdown.
Top issues:
- [Flag 1 one-liner]
- [Flag 2 one-liner]
- ...

Review Memo saved: {filename}
Redlined DOCX saved: {filename}  ← (or "Redline not produced — source was not a .docx")
```

---

## The KBC Advisors NDA Playbook

### A. Structure

| Issue | Position |
|---|---|
| **Mutual vs. one-way** | One-way (KBC as Receiving Party) preferred. Flag mutual NDAs — if KBC is not disclosing its own confidential information, push to convert to unilateral. |
| **Signatory authority** | Officer/executive only. Flag if agreement contemplates a broker or agent signing. |

---

### B. Definition of Confidential Information

**Must-have exclusions (all five required):**
1. Information already publicly known (not through breach)
2. Information known to KBC prior to disclosure
3. Information independently developed by KBC without use of CI
4. Information received from a third party without restriction
5. Disclosures required by law or court order

**Flag and delete:**
- Marking requirements (information only protected if stamped/labeled at time of disclosure)
- Oral confirmation requirements (oral disclosures only protected if confirmed in writing within X days)
- "As evidenced by written records / documentation" qualifiers on exclusions (b) and (c) — standard practice allows exclusions to be proven by any reasonable means
- "Burden of proof" sentences placing the burden on KBC to prove any exclusion

**Preferred standard:** Reasonable-person test — *"information that a reasonable person would understand to be confidential given the nature of the information and the circumstances of disclosure."*

**Preferred exclusion language:**
> "(a) is or becomes generally available to the public other than as a result of disclosure by the Receiving Party or its Authorized Personnel in breach of this Agreement; (b) was known to the Receiving Party prior to disclosure by the Disclosing Party; (c) was independently developed by the Receiving Party without reference to or use of the Confidential Information; (d) was received by the Receiving Party from a third party who had the right to disclose it without restriction; or (e) is required to be disclosed by law, regulation, or court order, provided that the Receiving Party gives prompt written notice to the Disclosing Party to the extent legally permitted."

---

### C. Permitted Disclosures / Authorized Recipients

**KBC's standard permitted recipient list (all of these must be covered):**
- Employees and staff (need-to-know basis)
- Affiliated entities (parent companies and subsidiaries)
- Outside legal counsel
- Financial advisors and lenders
- Potential co-investors and joint venture partners
- Any other person with a legitimate business need who is subject to comparable confidentiality obligations

**Flag and revise:**
- Definitions that limit recipients to employees/agents of the named entity only (excludes affiliates, counsel, advisors)
- Definitions requiring a pre-existing "contractual relationship" with KBC before a person qualifies as an authorized recipient
- Asymmetric carve-outs that benefit the counterparty only (e.g., "and, in the case of [Counterparty] only, utility providers...")
- Blanket prohibitions on discussing CI with "third parties" without a carve-out for Authorized Personnel — these directly conflict with permitted disclosure provisions

**Preferred Authorized Personnel language:**
> "employees, officers, directors, affiliated entities (including parent companies and subsidiaries), outside legal counsel, financial advisors, lenders, and potential co-investors or joint venture partners, and any other person with a legitimate business need in connection with the Purpose who is subject to confidentiality obligations no less protective than those set forth in this Agreement (collectively, 'Authorized Personnel')."

---

### D. Term and Survival

| Item | Position |
|---|---|
| **Agreement term** | Flag anything exceeding **2 years** |
| **Post-termination survival** | Flag anything exceeding **2 years** |
| **Perpetual survival** | Always flag — "for as long as the information remains confidential" or "for as long as retained" is effectively perpetual |
| **Rolling survival** | Flag survival running "from the date of each disclosure" rather than from Effective Date or termination — each disclosure resets the clock independently |
| **Trade secret carve-out** | Acceptable for trade secrets to survive indefinitely — industry standard |

**Preferred survival language:**
> "for a period of two (2) years following the date of termination of this Agreement; provided, however, that obligations with respect to information constituting a trade secret shall continue for as long as such information remains a trade secret under applicable law."

---

### E. Return / Destruction of Information

Acceptable — either return or destruction (with or without certification). No strong preference.

---

### F. Standard of Care / Efforts

| Language | Position |
|---|---|
| **"Best efforts"** | Always revise to "commercially reasonable efforts" |
| **"Commercially reasonable efforts"** | Acceptable |
| **"Reasonable care"** | Acceptable |

---

### G. Remedies and Liability

| Item | Position |
|---|---|
| **Injunctive relief clause** | Acceptable — standard and expected |
| **Liability cap** | Acceptable if reasonable (e.g., capped at deal value or fees paid) |
| **No-consequential-damages clause** | Flag if it eliminates KBC's ability to recover; acceptable if mutual and reasonable |
| **Indemnification** | Flag — unusual in NDAs; creates open-ended financial exposure. Recommend deleting and relying on direct liability + injunctive relief |
| **Prevailing party attorneys' fees** | Flag — creates leverage for the party more willing to initiate a dispute; recommend deleting |

---

### H. Non-Solicitation

**Position:** KBC generally will not agree to non-solicitation in an NDA. Delete.

**Fallback if counterparty insists — accept only if:**
- Limited to employees *directly involved in the transaction* (not all employees)
- Term capped at **6 months**
- General solicitations / job postings explicitly carved out
- Mutual (both parties bound equally)

---

### I. Non-Circumvention

**Position:** Flag and delete. As a brokerage operating across overlapping deal networks, a non-circumvention clause creates unacceptable risk that routine deal activity is characterized as a breach.

**Particular red flags:**
- Applies only to KBC (one-sided)
- Covers anyone "introduced or made known" by counterparty (very broad)
- No clear identification requirement, or identification satisfied by a single email
- Term exceeding 1 year

---

### J. Data Security Provisions

Flag any data security section that:
- Applies only to KBC and not the counterparty (asymmetric)
- Requires "best efforts" (revise to "commercially reasonable efforts")
- Imposes a breach notification window shorter than **5 business days**
- Requires KBC to reimburse counterparty's costs of responding to a Security Breach (delete)

---

### K. Governing Law and Jurisdiction

| Issue | Position |
|---|---|
| **Preferred states** | NY, DE, CA, TX, OH, IL, GA — accepted without comment |
| **Unusual jurisdictions** | Flag any non-US jurisdiction — note enforcement complexity |
| **Arbitration clauses** | Flag mandatory binding arbitration — no right to jury trial, limited appeal rights, potential travel burden. Note whether permissive or mandatory. Recommend permissive at most, or KBC's home jurisdiction. |

---

### L. Miscellaneous Provisions

| Clause | Position |
|---|---|
| **Email notice exclusion** | Flag and delete — declaring email invalid as notice is outdated and impractical. Replace with email-valid notice provision. |
| **Nuclear / export control provisions** | Flag — confirm whether KBC will receive any technical information subject to export controls before signing. Request deletion or limitation to expressly marked technical disclosures. |
| **Bribery Act / SFO carve-outs** | Flag as UK-specific — confirm relevance to the deal before accepting. |
| **Third-party rights (UK)** | Flag as UK-specific (Contracts (Rights of Third Parties) Act 1999). |
| **Residuals clauses** | Flag (not a dealbreaker) — note that they allow counterparty to use information retained in unaided memory without restriction. |

---

## Redline Workflow

Produces a `.docx` with Word-native tracked changes (`<w:del>`, `<w:ins>`) and comments (`<w:comment>`).

### Tools

```
python scripts/office/unpack.py input.docx unpacked/
# ... edit unpacked/word/document.xml ...
python scripts/office/pack.py unpacked/ output.docx --original input.docx
```

The comment helper is inline Python — see below.

### Step-by-step

**1. Unpack**
```bash
python scripts/office/unpack.py "C:/path/to/original.docx" "C:/path/to/unpacked/"
```

**2. Read document.xml**
```python
with open('unpacked/word/document.xml', encoding='utf-8') as f:
    xml = f.read()
```

**3. Apply tracked deletions**

Replace the old text in `document.xml` using `<w:del>`. The deletion must be a sibling of `<w:r>`, never inside it.

Pattern — deleting a run of text:
```xml
<!-- BEFORE (inside a <w:p>) -->
<w:r><w:t>best efforts</w:t></w:r>

<!-- AFTER -->
<w:del w:id="1" w:author="KBC Advisors" w:date="2026-06-01T00:00:00Z">
  <w:r><w:delText>best efforts</w:delText></w:r>
</w:del>
<w:ins w:id="2" w:author="KBC Advisors" w:date="2026-06-01T00:00:00Z">
  <w:r><w:t>commercially reasonable efforts</w:t></w:r>
</w:ins>
```

Use string replacement on the XML — find the run containing the target text and wrap it. Increment `w:id` for each change (IDs must be unique across the document). Use today's date from the system for `w:date`.

**4. Add Word comments**

Comments require entries in two places: `unpacked/word/comments.xml` and `unpacked/word/document.xml`.

**comments.xml** — add inside `<w:comments>`:
```xml
<w:comment w:id="1" w:author="KBC Advisors" w:date="2026-06-01T00:00:00Z">
  <w:p>
    <w:r><w:t>KBC COMMENT: {comment text here}</w:t></w:r>
  </w:p>
</w:comment>
```

**document.xml** — wrap the target run:
```xml
<!-- commentRangeStart and commentRangeEnd are direct children of <w:p>, not inside <w:r> -->
<w:commentRangeStart w:id="1"/>
<w:r><w:t>text being commented on</w:t></w:r>
<w:commentRangeEnd w:id="1"/>
<w:r>
  <w:rPr><w:rStyle w:val="CommentReference"/></w:rPr>
  <w:commentReference w:id="1"/>
</w:r>
```

**Critical XML rules:**
- `<w:commentRangeStart>` and `<w:commentRangeEnd>` must be **direct children of `<w:p>`** — never inside `<w:r>` or `<w:t>`
- `<w:del>` and `<w:ins>` must be **siblings of `<w:r>`** — never inside `<w:r>` or `<w:t>`
- Text inside `<w:del>` uses `<w:delText>`, not `<w:t>`
- IDs must be unique integers across all changes and comments
- Close any open `<w:r>` before inserting comment markers or del/ins tags

**5. Ensure comments.xml exists**

If `unpacked/word/comments.xml` doesn't exist, create it:
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:comments xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas"
  xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
</w:comments>
```

And add the relationship to `unpacked/word/_rels/document.xml.rels`:
```xml
<Relationship Id="rIdComments" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments" Target="comments.xml"/>
```

And add the content type to `unpacked/[Content_Types].xml`:
```xml
<Override PartName="/word/comments.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"/>
```

**6. Write back and validate**
```python
with open('unpacked/word/document.xml', 'w', encoding='utf-8') as f:
    f.write(xml)
```

Quick validation — check no forbidden nesting:
```python
import re
# w:del or w:ins inside w:r (bad)
bad = re.findall(r'<w:r[^>]*>.*?<w:(?:del|ins)\b', xml, re.DOTALL)
if bad:
    print("ERROR: del/ins nested inside w:r — fix before packing")
```

**7. Pack**
```bash
python scripts/office/pack.py "C:/path/to/unpacked/" "C:/path/to/output.docx" --original "C:/path/to/original.docx"
```

**8. Test**
Open the output in Word and verify tracked changes and comments appear correctly. If Word reports corruption, re-check IDs for uniqueness and XML nesting.

---

## NDA Log

After completing the review, add a row to `KBC/NDA Log.md` (newest at top):

| Date Received | Counterparty | Type | Status | Date Reviewed | Notes |
|---|---|---|---|---|---|
| YYYY-MM-DD | {Counterparty} | Mutual / One-Way | Reviewed | YYYY-MM-DD | {N flags: top issues summary} |

---

## Rules

- **Never assume one-way vs. mutual without reading the document** — check the opening recitals or party definitions
- **Flag every playbook item** — do not silently pass something because it might be acceptable; flag it and note if it's acceptable fallback
- **Redline only what the playbook authorizes** — don't editorialize beyond the playbook
- **Save everything to the docs folder** — Review Memo + Redlined DOCX both go to `KBC_DOCS\{matter}\`
- **Log to NDA Log** — every NDA reviewed gets a row, even if no flags
- **Ask before proceeding** if the counterparty name, matter name, or file is ambiguous
