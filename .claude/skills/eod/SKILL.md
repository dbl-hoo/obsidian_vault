---
name: eod
description: Process end-of-day notes from the daily note or pasted text — update deal files, extract tasks, stamp the daily note as processed, and suggest system improvements.
---

# EOD Skill

Triggered by `/eod`. Processes today's daily note (or a specific note file if passed as argument, e.g. `/eod 2026-04-07`).

## Workflow

### Step 0 — Git checkpoint
Before touching any files, commit and push the current vault state as a restore point:
```
cd VAULT_ROOT
git add -A
git commit -m "checkpoint: pre-EOD YYYY-MM-DD"
git push origin main
```
If the commit has nothing to stage (clean working tree), skip silently. If the push fails, warn Jason but proceed — don't block EOD over a push failure.

### Step 1 — Load the daily note
- Find today's daily note at `Daily Notes/YYYY-MM-DD.md` (use today's date)
- If an argument is passed, use that date instead: `/eod 2026-04-03` → `Daily Notes/2026-04-03.md`
- If the file doesn't exist or has no content, stop and tell Jason

### Step 2 — Check if already processed
- If the note contains `## EOD Processed` with a date line (e.g. `2026-04-22 — Updated: ...`), stop and say so — don't double-process
- A bare `<!-- EOD_PENDING -->` comment is the unprocessed template placeholder — proceed normally

### Step 3 — Parse the note
Read through the note and identify:
- **Deal references** — site codes (CVG47, DOH3, ZIN3, etc.) or deal names that map to vault files
- **Notes to log** — what happened, who was called, what was discussed
- **Tasks to extract** — action items, follow-ups, deadlines
- **Status changes** — if a deal closed, went on hold, etc.
- **Extra WikiLink Place Holders** - skip any empty wikilink lines; they are harmless

Group content by deal. If a chunk of content can't be matched to a deal, **stop and ask** — never skip silently.

### Step 4 — Update deal files
For each deal identified:
1. **Re-read the deal file immediately before writing**
2. **Prepend** a dated entry to `## Notes` (today's date, ISO format)
3. **Only create tasks if Jason expressly asks for one** — e.g., "send X by Friday", "need to do Y", "add a task to Z". Implied follow-ups do NOT become tasks (e.g., "follow up next week", "sent EAA to sellers", "waiting on LL" — none of these create tasks). If a task is warranted but no date is given, default to 1 week from today.
   - `- [ ] Task description 📅 YYYY-MM-DD`
   - `- [ ] 🔺 High priority task 📅 YYYY-MM-DD`
4. **Delete all completed tasks** — remove any `- [x]` lines from `## Tasks`. Completed tasks are deleted, not kept.
5. Update `last_updated:` to today's date
6. Update `status:` if it changed

### Step 5 — Stamp the daily note
Replace `<!-- EOD_PENDING -->` with:

```
## EOD Processed

YYYY-MM-DD — Updated: Deal1, Deal2, Deal3.
```

List every deal file that was modified. If the placeholder isn't present (older note format), append to the end of the file instead.

### Step 6 — Suggest improvements
After processing, suggest specific improvements to `CLAUDE.md` or other system files based on anything that was confusing, missing, or inefficient. Be concrete — not "consider adding more detail" but "add a YAML field for X because Y came up today."

---

## Rules

- **Never skip unmatched content** — if something can't be tied to a deal, stop and ask before continuing
- **Re-read each deal file immediately before writing** — never work from cached content
- **Don't create new deal files** during EOD — if a new deal is mentioned, flag it and ask Jason to open it explicitly
- **Preserve note prose exactly** — don't clean up, rewrite, or summarize what Jason wrote
- **Tasks go in ## Tasks, notes go in ## Notes** — don't mix them
- **Only create tasks when Jason expressly asks for one** — implied follow-ups, waiting-on notes, and status updates do NOT become tasks
- If a deal has `status: Closed` or `status: Dead`, flag it rather than updating silently

---

## Note Entry Format

```
YYYY-MM-DD - Summary of what happened
Supporting detail — bullets, prose, whatever fits.
```

## Task Format

```
- [ ] Task description 📅 YYYY-MM-DD
- [ ] 🔺 High priority task 📅 YYYY-MM-DD
```

---

## Example

**Daily note contains:**
```
CVG47 - called Sarah Chen. LL countered at $4.85 NNN, we were at $4.50. She's pushing back, needs internal approval. Phase II came back clean. Send estoppel to LL counsel by Friday.

DOH3 - Al confirmed he's good with the Franklin Vista LOI we sent.
```

**Jack does:**

1. Reads `Amazon/CVG47/CVG47.md`, prepends to Notes:
```
2026-04-07 - Call w/ Sarah Chen (TM). LL countered $4.85/SF NNN vs. our $4.50. Sarah pushing back, needs internal approval. Phase II enviro came back clean.
```
Adds to Tasks:
```
- [ ] 🔺 Send estoppel request to LL counsel 📅 2026-04-11
```

2. Reads `Amazon/DOH3/DOH3.md`, prepends to Notes:
```
2026-04-07 - Al Patel confirmed good with Franklin Vista LOI.
```

3. Stamps daily note:
```
## EOD Processed
2026-04-07 — Updated: CVG47, DOH3.
```
