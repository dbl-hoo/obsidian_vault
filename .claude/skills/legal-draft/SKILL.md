# Legal Draft Skill

Draft a legal document for Jason. Output is a `.docx` file saved to `Inputs\`.

---

## Trigger

User invokes `/legal-draft` or explicitly asks to draft a legal document (PSA, lease, assignment, bill of sale, amendment, promissory note, NDA, engagement letter, or similar).

---

## Style Rules — Non-Negotiable

Apply these to every document, every time.

- **Plain English. Active voice. No exceptions.** Rewrite any passive construction before saving.
- **Ohio law** governs unless Jason specifies otherwise.
- **Structure:** Document Title → `Background` section → numbered `Agreement` sections. No "Whereas." No "NOW, THEREFORE." No "WITNESSETH."
- **No boilerplate consideration recital.** Do not write "for good and valuable consideration, the receipt and sufficiency of which are hereby acknowledged." State actual consideration or omit entirely.
- **Signature blocks in a two-column table.** Include notice addresses in the same table below the signature lines. See signature table format below.
- **Adams on Contract Drafting style:**
  - `shall` = party obligation. `may` = discretionary. Present tense = condition.
  - No `hereof`, `herein`, `hereto`, `hereunder` — use specific cross-references ("Section 3," "this Agreement," "Schedule A").
  - Defined terms in quotes on first use: the "Agreement" — not (the "Agreement").
  - `including` — never "including without limitation" or "including but not limited to."
  - `void` — not "null and void." `cease` — not "cease and desist."
  - Do not pair "representations and warranties" by default — choose one based on context.
  - Sections numbered at top level (1, 2, 3). Subsections lettered (a, b, c). Sub-subsections roman (i, ii, iii).

---

## Workflow

### Step 1 — Identify document type and deal file

Determine what type of document is needed. If Jason named a deal or site code, locate and read the deal file now. Pull:
- Party names (Assignor/Assignee, Buyer/Seller, Landlord/Tenant, etc.)
- Property description
- TM, local broker, counterparty names
- Any deal terms already captured in Notes

### Step 2 — Interview for missing information

Ask only for what you cannot get from the deal file. Group questions by topic. Do not ask for information you already have.

**Universal questions (if not in deal file):**
- Property address / legal description (if applicable)
- Counterparty full legal name and entity type
- Effective / execution date
- Governing law deviation (if any from Ohio)
- Any special provisions or carve-outs Jason wants included

**Document-type-specific questions — ask only the relevant set:**

| Doc Type | Key questions |
|---|---|
| **PSA / Purchase Agreement** | Purchase price; earnest money amount + holder; due diligence period (length or dates); closing date / outside date; title company; financing contingency (yes/no); conditions to closing; proration methodology |
| **Lease / Sublease** | Term (start/end); base rent + escalation schedule; gross or NNN (if NNN, which expenses); TI allowance; options (renewal, ROFO, ROFR, termination); permitted use; assignment/subletting rights |
| **Assignment & Assumption** | Contract or lease being assigned (attach as exhibit?); consent of counterparty required?; release of assignor from future obligations? |
| **Bill of Sale** | What is being sold (list or reference schedule); warranty of title (full / limited / as-is); consideration amount |
| **Amendment / Side Letter** | Document being amended (date + parties); specific provisions being changed; effective date of amendment |
| **Promissory Note** | Principal amount; interest rate (fixed/variable); maturity date; payment schedule (interest only, amortizing, balloon); secured or unsecured; prepayment permitted?; default / cure period |
| **NDA** | Mutual or one-way; purpose / transaction context; term; key exclusions beyond standard |
| **Engagement Letter** | Services (scope); fee structure (flat, hourly, contingent); payment timing; term and termination; conflict waiver needed? |

### Step 3 — Draft

Draft the document using the style rules above and the structure below. Do not add sections that are not needed for this document type. Do not pad with boilerplate that serves no function.

### Step 4 — Generate .docx and save

Use `python-docx` to generate a `.docx` file. Save to:
```
C:\Users\kirkham\Documents\Vault\Inputs\{Document Title} - DRAFT.docx
```

Report the filename and flag any blanks left for Jason to fill in.

---

## Document Structure

### Title
Centered, bold, all caps. One line if possible.

### Background
Numbered sentences (A., B., C.) stating the facts that explain why the document exists. Active voice. No "whereas." End the last sentence with a period — do not lead into the Agreement with a transition clause.

### Agreement
Numbered sections. Lead directly into the substantive provisions — no "the parties agree as follows" bridge.

Standard closing sections (include only what applies):
- Governing Law
- Entire Agreement
- Amendments
- Counterparts; Electronic Signatures
- Severability (only if genuine risk of partial invalidity)
- Further Assurances (only if ongoing cooperation is needed)
- Notices (if notice mechanics are needed — otherwise handle in signature table)

Omit boilerplate sections that add no value for the transaction at hand.

### Signature Table Format

Two-column table. One party per column. Include notice address below sig lines in the same table.

```
| PARTY A NAME:                    | PARTY B NAME:                    |
| [Full Legal Entity Name],        | [Full Legal Entity Name],        |
| [entity type]                    | [entity type]                    |
|                                  |                                  |
| By: ________________________     | By: ________________________     |
| Name: ______________________     | Name: ______________________     |
| Title: _____________________     | Title: _____________________     |
| Date: ______________________     | Date: ______________________     |
|                                  |                                  |
| Notice Address:                  | Notice Address:                  |
| [address]                        | [address]                        |
| Attn: ______________________     | Attn: ______________________     |
| Email: _____________________     | Email: _____________________     |
```

---

## Python-docx Output Notes

**Template:** `.dotx` files require a content-type patch before python-docx will accept them. Always open with this helper:

```python
import shutil, os, zipfile, tempfile
from docx import Document

def doc_from_dotx(template_path):
    with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp:
        tmp_path = tmp.name
    shutil.copy(template_path, tmp_path)
    with zipfile.ZipFile(tmp_path, 'r') as z:
        files = {name: z.read(name) for name in z.namelist()}
    ct = files['[Content_Types].xml'].decode('utf-8')
    ct = ct.replace(
        'application/vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml'
    )
    files['[Content_Types].xml'] = ct.encode('utf-8')
    with zipfile.ZipFile(tmp_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in files.items():
            z.writestr(name, data)
    doc = Document(tmp_path)
    os.unlink(tmp_path)
    return doc

TEMPLATE = r'C:\Users\kirkham\Documents\Vault\Templates\legal-template.dotx'
doc = doc_from_dotx(TEMPLATE)
```

**Available styles in the template** (use these names exactly — do not hardcode fonts or sizes):

| Use | Style name |
|---|---|
| Body text, recitals, agreement paragraphs | `Normal` |
| Document title, schedule titles | `Title` / `Heading 1` |
| Section headings (1., 2., etc.) | `Heading 2` |
| Sub-headings | `Heading 3` |
| Bulleted lists | `List Paragraph` |
| Tables | `Normal Table` |

- Signature table: equal column widths; no shading; `Normal Table` style
- Schedules: page break before each; title in `Heading 1`, centered

---

## Entity Quick Reference

- **KBC broker entity (typical):** KBC Illinois Investment, LLC (confirm — "Development" also exists; they are different entities)
- **Kirkham Law:** Kirkham Law LLC, an Illinois limited liability company
- Jason's default signing authority: Member / Manager (confirm per entity)
