---
name: pymupdf
description: Read and extract text from PDF files using PyMuPDF. Use when the user provides a .pdf file path to read, review, or search — contracts, LLC agreements, closing documents, reports. Prefer over Word COM for PDFs. Import name is `fitz`, not `pymupdf`.
---

# PyMuPDF

Read and extract text from PDF files. Import as `fitz`.

```python
import fitz  # PyMuPDF
```

## Read all text

```python
import fitz

path = r'C:\path\to\file.pdf'
doc = fitz.open(path)
print(f'Pages: {len(doc)}')
for page in doc:
    print(f'--- Page {page.number + 1} ---')
    print(page.get_text())
doc.close()
```

## Read specific pages

```python
doc = fitz.open(path)
for i in range(4, 9):  # pages 5-9 (0-indexed)
    print(doc[i].get_text())
doc.close()
```

## Search for text (find a section)

```python
doc = fitz.open(path)
for page in doc:
    hits = page.search_for('Section 7.2')
    if hits:
        print(f'Found on page {page.number + 1}')
        print(page.get_text())
doc.close()
```

## Extract a text window around a keyword

```python
doc = fitz.open(path)
full_text = '\n'.join(page.get_text() for page in doc)
doc.close()

idx = full_text.find('Section 7.2')
print(full_text[max(0, idx-200) : idx+3000])
```

## Key notes

- Import is `fitz`, not `pymupdf` or `PyMuPDF`
- Pages are 0-indexed in code (`doc[0]` = page 1)
- `get_text()` returns plain text; `get_text('dict')` returns structured blocks with coordinates
- Much faster and more reliable than Word COM or pdftotext for text extraction
