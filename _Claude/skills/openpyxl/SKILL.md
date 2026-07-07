---
name: openpyxl
description: Read and edit Excel .xlsx files using openpyxl. Use when the user provides a .xlsx file path to read, review, or modify — spreadsheets, trackers, commission models, rent rolls, financial models.
---

# openpyxl

Read and write Excel `.xlsx` files.

## Read a workbook

```python
from openpyxl import load_workbook

path = r'C:\path\to\file.xlsx'
wb = load_workbook(path)
print(wb.sheetnames)

ws = wb.active  # or wb['Sheet Name']
for row in ws.iter_rows(values_only=True):
    print(row)
```

## Read specific range

```python
ws = wb['Summary']
for row in ws.iter_rows(min_row=2, max_row=50, min_col=1, max_col=5, values_only=True):
    print(row)
```

## Read a single cell

```python
val = ws['B4'].value
val = ws.cell(row=4, column=2).value
```

## Write values

```python
from openpyxl import load_workbook

wb = load_workbook(path)
ws = wb.active
ws['A1'] = 'Updated'
ws.cell(row=2, column=3).value = 42
wb.save(path)
```

## Key notes

- Use `load_workbook(path, data_only=True)` to read cached formula results instead of formula strings
- File must be closed in Excel before saving (same locking issue as Word — use `data_only=True` for read-only work)
- `values_only=True` in `iter_rows` returns plain Python values, not Cell objects
- Dates come back as Python `datetime` objects
