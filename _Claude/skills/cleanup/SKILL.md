---
name: cleanup
description: Clean up a deal file (or all deal files) to enforce vault conventions — ISO dates, newest-first notes, single Notes section, remove completed tasks, strip orphaned content.
---

# Cleanup Skill

Triggered by `/cleanup`. Cleans one file if a deal name or path is given (e.g. `/cleanup DOH3`), or spawns subagents to clean all active deal files if no argument is provided.

## Conventions This Skill Enforces

### 1. ISO Dates Everywhere
All dates — in YAML frontmatter and note entry headers — must be `YYYY-MM-DD`.

**YAML fields to fix:**
- `launch_date`, `start_date`, `end_date`, `last_updated`
- Common bad formats: `January 1, 2028` → `2028-01-01` | `July 31, 2025 9:34 AM` → `2025-07-31` | `04-03-2026` → `2026-04-03`

**Note entry headers to fix:**
- Format: `YYYY-MM-DD - Summary text`
- Bad examples: `April 1, 2026 -` | `March 31, 2026 -` | `04-03-2026 -`

### 2. Notes: Newest Entry at Top
The `## Notes` section must be in reverse chronological order (most recent first). After converting all dates to ISO, sort entries descending.

### 3. Single `## Notes` Section
Files sometimes have duplicate `## Notes` headers from copy-paste or import artifacts. Merge all note content into one `## Notes` section. Preserve all unique entries; deduplicate exact duplicates.

### 4. No Orphaned Content
Note entries, contact info, or other content that appears outside of `## Tasks` or `## Notes` must be moved to the correct section or removed. Specifically:
- Note-style entries sitting between `## Tasks` and `## Notes` → move into `## Notes`
- Stray headings inside `## Notes` (e.g. `# DOH3 - Notes`) → remove
- Floating contact info blocks not tied to a note entry → remove unless clearly meaningful; if unclear, ask
- Broken image embeds (`![image.png](image%206.png)`) → remove unless Jason confirms they're needed

### 5. Remove Completed Tasks
Tasks marked `[x]` are deleted per vault convention. Do not move them to Notes. Just delete.

### 6. Deal Sheet Table
If a deal sheet table exists (repeating YAML fields like Deal Type, Business Unit, TM, etc.), remove it entirely. All that data lives in frontmatter.

---

## Workflow — Git Checkpoint (always, before any writes)
Before touching any files, commit and push the current vault state as a restore point:
```
cd VAULT_ROOT
git add -A
git commit -m "checkpoint: pre-cleanup YYYY-MM-DD"
git push origin main
```
If the working tree is clean, skip silently. If the push fails, warn Jason but proceed.

## Workflow — Single File

1. **Read** the file immediately before making any changes
2. **Identify** all issues against the conventions above
3. **Report** what you found before writing — list issues, ask if anything is ambiguous (e.g. orphaned content that might matter)
4. **Write** the cleaned file in one pass
5. **Update** `last_updated:` to today's date
6. **Report** what changed

## Workflow — Bulk (no argument)

1. Spawn one subagent per deal file across `Amazon/`, `Amazon/Quick Commerce/`, `Amazon/Project A/`, and `KBC/` with `status: Ongoing`
2. Each subagent reads its file and returns a list of issues found
3. Consolidate the report — present to Jason before making any writes
4. On confirmation, clean each file

---

## What NOT to Touch
- Content of note entries (don't rewrite prose, fix typos, or summarize)
- YAML fields other than date formatting and `last_updated`
- `x_Archive/` — never
- Tasks that are open `[ ]` — leave as-is unless they're malformed

---

## Example: Before / After

**Before (YAML):**
```yaml
launch_date: January 1, 2028
start_date: July 31, 2025 9:34 AM
```
**After:**
```yaml
launch_date: 2028-01-01
start_date: 2025-07-31
```

**Before (Notes — oldest first, bad dates):**
```
April 1, 2026 - Call with Jeff.
March 31, 2026 - LOIs sent.
```
**After (newest first, ISO):**
```
2026-04-01 - Call with Jeff.
2026-03-31 - LOIs sent.
```
