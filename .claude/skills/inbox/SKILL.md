---
name: inbox
description: Process all entries in _Inbox.md, route them to the right place (Todoist, deal files, journal, food log, training log), then clear the file.
---

# /inbox Skill

Process all entries in `_Inbox.md`, route them to the right place, then clear the file.

## Steps

### 1. Read the inbox

Read `_Inbox.md` from the vault root. If it's empty or doesn't exist, report "Inbox is empty." and stop.

### 2. Parse entries

Each entry is a timestamped line followed by optional detail:
```
YYYY-MM-DD HH:MM - [content]
```

Split into individual entries. For each one, classify it:

**A — Personal task**
Something that has nothing to do with a deal. Examples: "clean the kitchen", "call the dentist", "order something". → Add to Todoist via `td task add "..."`.

**B — Deal-specific task or note**
Mentions a site code, deal name, TM name, or is clearly about a transaction. → File it:
- If it's an action item: add to that deal file's `## Tasks` section
- If it's a note/intel: prepend to that deal file's `## Notes` section using the standard note entry format
- Update `last_updated` and `last_note` YAML fields

**C — Journal entry**
A personal reflection, emotional observation, or introspective thought with no actionable component. → Prepend to `Personal/Health/Journal.md` under today's date header (`## YYYY.MM.DD`). If a header for today already exists, append the bullet under it.

**D — Food log entry**
A meal, snack, or ingredient capture — anything describing what Jason ate or is about to eat (e.g. "pre-workout 160g steel cut oats, peanut powder, honey, milk"). → File to `Personal/Health/Food Log.md` under the entry's date, following that file's existing format. Preserve quantities exactly as captured.

**E — Training/workout entry**
Sets, reps, weights, cardio results, or workout observations. → File into the matching session file in `Personal/Health/Training/Sessions/` (named `YYYY-MM-DD-*.md`) for the entry's date, following that file's existing format. If no session file exists for that date, ask Jason before creating one.

**F — Ambiguous**
No deal is identifiable but it could be either. → Treat as personal, add to Todoist.

**G — Not actionable**
A stray capture, test entry, or something Jason already handled. → Drop it silently.

### 3. Dedupe check — before filing anything

Obsidian Sync can resurrect already-processed entries: a device with a stale copy of `_Inbox.md` (e.g. the phone, backgrounded since capture) pushes its version and merges old entries back in after they've been filed. So **an entry sitting in the inbox is not proof it hasn't been processed.**

Before filing each entry, check the destination for an existing match:

- **Todoist**: `td task list` (or search) — skip if an open task with the same description already exists
- **Food Log / Journal / Training**: read the target section for the entry's date — skip if an entry covering the same content is already there (match on substance, not exact wording; the filed version may be reformatted)
- **Deal files**: check `## Notes` for a same-date entry covering the same call/intel, and `## Tasks` for the same task (open **or** checked off)

If a match exists, treat the entry as **already processed**: drop it from the inbox without filing, and count it in the report as a dedupe skip. Never file the same capture twice.

### 4. Routing rules

- **Todoist tasks**: use `td task add "..."` — keep the description clean, no timestamps
- **Vault tasks**: follow the task format from CLAUDE.md — `- [ ] Task description 📅 YYYY-MM-DD`. Use today's date if no due date is implied; infer a date if one is mentioned (e.g. "by Friday")
- **Vault notes**: follow the note entry format — `YYYY-MM-DD - Brief summary` prepended to `## Notes`
- Always re-read a deal file immediately before writing to it
- **Work machine (Windows) caveat**: `Personal/` does not sync to the work machine. If a personal entry (C, D, or E) can't be filed because its target doesn't exist, **leave that entry in `_Inbox.md`** — the homelab (Dathomir) will process it. Only file and clear what this machine can actually reach.

### 5. Clear the inbox

Once all entries are processed (including any ambiguous ones Jason has responded to), overwrite `_Inbox.md` with empty content — **except** entries deliberately left for another machine (see work machine caveat above), which stay in place. Do not leave processed entries behind.

### 6. Report back

Brief summary:
- X tasks added to Todoist
- X items filed to [deal codes / journal / food log / training]
- X items skipped as already processed (sync resurrection)
- X items dropped
- Any items still pending (ambiguous ones awaiting Jason, or personal entries left for the homelab)
