# Lien Waiver Skill

Generate a conditional lien waiver `.docx` for KBC Advisors to sign at a real estate closing. Output saved to `Inputs\`.

---

## Trigger

User invokes `/lien-waiver` or asks to draft a conditional lien waiver, broker's lien waiver, or commission lien waiver.

---

## Workflow

### Step 1 — Gather inputs

Collect these from context, deal file, invoice, or PSA. Ask only for what you can't find:

| Field | Source |
|---|---|
| Property address (street, city, state, zip, county) | PSA or deal file |
| Seller — full legal name + entity type | PSA |
| Buyer — full legal name + entity type | PSA |
| Commission amount | Invoice |
| Invoice number | Invoice |
| Invoice date | Invoice |
| State governing the transaction | Property state |
| KBC entity signing the waiver | Jason or knowledgebase (see Step 2) |

### Step 2 — Resolve KBC entity

Look up `_Knowledgebase/KBC/KBC Legal Entities and Signatories.md` for the correct KBC entity, incorporation type, signatories, and office address for the property state.

### Step 3 — Load state requirements

Read `.claude/skills/lien-waiver/state-requirements.md`. Pull the section matching the property state. This gives you:
- **Lien statute citation** — cite in Section 1 of the waiver
- **Waiver language override** — replaces the standard Section 1 body if present
- **Notary form** — the full state-specific acknowledgment block
- **Special requirements** — any extra steps or language

If the state is not in the appendix, flag it: use `[STATE STATUTE — VERIFY]` as a placeholder in Section 1 and `[STATE NOTARY FORM — VERIFY]` in the notary block, and tell Jason to add the state to the appendix.

### Step 4 — Generate .docx

Use python-docx with the template helper below. Replicate the exact structure of the approved form.

**Document structure (match exactly):**

```
Para 0:   Normal, centered, bold                → "CONDITIONAL LIEN WAIVER"
Para 1:   List Paragraph                        → Background A (KBC entity, services, property, seller, buyer)
Para 2:   List Paragraph                        → Background B (commission amount, invoice #, date)
Para 3:   List Paragraph                        → Background C ("Broker delivers this waiver at closing...")
Para 4:   Heading 1, run0=bold "Conditional Waiver.  ", run1=body text (state lien statute)
Para 5:   Heading 1, run0=bold "Limitation.  ", run1=body text
Para 6:   Heading 1, run0=bold "Authority.  ", run1=body text
Para 7:   Heading 1, run0=bold "Governing Law.  ", run1="[State] law governs this waiver."
Para 8:   Heading 1, empty (spacer)
Para 9:   Heading 1, centered, bold             → "[Signatures on Following Page]"
Para 10:  Normal, page-break run (w:br type=page)
Para 11:  Normal, empty
Para 12:  Normal, empty
--- Signature table (1 col) ---
  Row 0: "BROKER:" (bold), entity name, entity type, blank line,
         "By: ________________________", "Name: ______________________",
         "Title: _______________________", "Date: _______________________"
Para 13: Normal, bold  → "STATE OF [STATE]"
Para 14: Normal, bold  → "COUNTY OF _______________"
Para 15: Normal        → notary body (from state-requirements.md)
Para 16: Normal        → witness clause (from state-requirements.md, or standard)
Para 17: Normal        → "________________________________"
Para 18: Normal        → "Notary Public"
Para 19: Normal        → "My Commission Expires: ___________"
```

**Standard body text for each section:**

*Section 1 — Conditional Waiver (substitute state statute from appendix):*
> Upon Broker's actual receipt of good funds in the amount of $[AMOUNT], Broker waives and releases any and all lien rights, claims, and encumbrances against the Property arising from or related to Broker's brokerage services in connection with the sale of the Property, including any broker's lien under [STATE STATUTE].

*Section 2 — Limitation:*
> This waiver is conditional on Broker's actual receipt and collection of the full Commission. It does not take effect, and Broker does not waive any rights, unless and until Broker has received good funds in the full amount stated in Section 1.

*Section 3 — Authority:*
> The person signing below is authorized to execute this waiver on behalf of Broker.

*Section 4 — Governing Law:*
> [State] law governs this waiver.

*Standard witness clause (override with state form if appendix provides one):*
> IN WITNESS WHEREOF, I have hereunto set my hand and official seal this _____ day of _______________, [YEAR].

**Template helper (use every time):**

```python
import shutil, os, zipfile, tempfile
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

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
for p in list(doc.paragraphs):
    p._element.getparent().remove(p._element)
```

**Page break helper:**

```python
def add_page_break(doc):
    p = doc.add_paragraph(style='Normal')
    run = p.add_run()
    br = OxmlElement('w:br')
    br.set(qn('w:type'), 'page')
    run._r.append(br)
```

**Signature table:**

```python
table = doc.add_table(rows=1, cols=1)
table.style = 'Normal Table'
cell = table.cell(0, 0)
lines = [
    ('BROKER:', True),
    (f'{kbc_entity_name},', False),
    (f'{kbc_entity_type}', False),
    ('', False),
    ('By: ________________________', False),
    ('Name: ______________________', False),
    ('Title: _______________________', False),
    ('Date: _______________________', False),
]
for i, (text, bold) in enumerate(lines):
    p = cell.paragraphs[0] if i == 0 else cell.add_paragraph()
    r = p.add_run(text)
    r.bold = bold
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
```

### Step 5 — Save and report

Save to:
```
C:\Users\kirkham\Documents\Vault\Inputs\Conditional Lien Waiver - {KBC short name} - {City or Property} - DRAFT.docx
```

Report filename and flag any `[VERIFY]` placeholders.

---

## Output filename convention

`Conditional Lien Waiver - KBC {State/City} - {Property identifier} - DRAFT.docx`

Examples:
- `Conditional Lien Waiver - KBC Ohio - 2177 Williams Rd - DRAFT.docx`
- `Conditional Lien Waiver - KBC Illinois - 123 Main St Chicago - DRAFT.docx`
