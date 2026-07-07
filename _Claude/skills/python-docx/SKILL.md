---
name: python-docx
description: Read and edit Word .docx files using python-docx. Use when the user provides a .docx file path to read, review, or modify — especially legal documents, promissory notes, agreements, and other Word files. Handles run-level formatting preservation and file-locking conflicts when the file is open in Word.
---

# python-docx

Use `python-docx` to read and edit `.docx` files. Already installed at `C:\Users\kirkham\AppData\Local\Python\pythoncore-3.14-64`.

Python binary: `python` (via `python -c "..."` or a script)

## Reading a .docx

```python
from docx import Document

path = r'C:\path\to\file.docx'
doc = Document(path)
for para in doc.paragraphs:
    print(para.text)
```

To inspect run-level formatting before editing:

```python
for i, para in enumerate(doc.paragraphs):
    for j, run in enumerate(para.runs):
        print(f'Para {i} Run {j}: bold={run.bold} italic={run.italic} text={repr(run.text[:60])}')
```

## Editing a .docx

Always inspect runs first — editing `para.text` directly destroys formatting. Edit `run.text` instead:

```python
for para in doc.paragraphs:
    if para.text.startswith('Section Header'):
        para.runs[1].text = 'new body text here'  # run 0 may be bold label
doc.save(path)
```

## File locked by Word

When the file is open in Word, `doc.save(path)` raises `PermissionError`. Fix:

1. Close in Word via `win32com`, save to a temp file, replace, reopen:

```python
from docx import Document
import win32com.client
import os, time

path = r'C:\path\to\file.docx'
tmp = path.replace('.docx', '_tmp.docx')

# Close in Word
try:
    word = win32com.client.GetActiveObject('Word.Application')
    for doc in word.Documents:
        if doc.FullName == path:
            doc.Close(SaveChanges=False)
            break
except Exception as e:
    pass  # Word not running

time.sleep(1)

# Edit
doc = Document(path)
# ... make changes ...
doc.save(tmp)
os.replace(tmp, path)

# Reopen
word.Documents.Open(path)
```

`win32com` is available via `pywin32` (already installed).

## Word's Find & Replace limit

Word's COM Find & Replace caps replacement text at ~255 characters. For longer replacements, use Range.Find then set `range.Text` directly — or use python-docx (no limit).

## Key gotchas

- `para.text` is read-only (reconstructed from runs) — always edit `run.text`
- Run 0 is often the bold/italic label (e.g. `"Repayment"`), Run 1 is the body
- `os.replace()` is atomic on Windows; prefer over `shutil.move`
- If Word isn't running, skip the `win32com` close step and edit directly
