---
name: email
description: Pull emails directly from Outlook, match them to existing deal files, log as Notes entries, extract tasks, save attachments to the deal's docs folder, and mark read. Replaces the manual .msg-save → /extract-msg workflow for incoming emails.
---

# Email Skill

Triggered by `/email` (triage mode) or `/email {query}` (targeted mode, e.g. `/email ZDT6` or `/email royal oak`).

**This skill updates EXISTING deal files only.** For creating a new deal file from an email, use `/intake` instead.

---

## Mode Detection

- **No argument** → **Triage mode**: fetch unread emails, match to deal files, process interactively
- **Argument provided** → **Targeted mode**: search inbox for the query, show results, process selected

---

## Workflow

### Step 0 — Git checkpoint

```
git add -A
git commit -m "checkpoint: pre-email YYYY-MM-DD"
git push origin main
```

If working tree is clean, skip silently. If push fails, warn Jason but proceed.

---

### TARGETED MODE (`/email {query}`)

#### Step T1 — Search inbox

Call `mcp__outlook__search_inbox(query="{query}", count=20)`.

Present results as a numbered list:

```
1. [UNREAD] ZDT6 - 313 E. Hudson LOI — Tony Schmitt <tschmitt@midamericagrp.com> — May 24
2. [READ]   RE: ZDT6 electrical clearance — Himanshu Sharma — May 22 [2 attachments]
```

Include `[UNREAD]` / `[READ]` status and `[N attachments]` if present. If no results, say so and stop.

#### Step T2 — Select email

Ask Jason which number to process. If he says "all unread" or "all", process each in sequence (Step T3 → Common processing, then repeat). If he names a number, process that one.

#### Step T3 — Fetch and display

Call `mcp__outlook__get_email(entry_id="{id}", include_body=True)`.

Display a compact summary:

```
From: Tony Schmitt <tschmitt@midamericagrp.com>
Subject: ZDT6 - 313 E. Hudson LOI — Landlord Counter
Date: 2026-05-24
Attachments: ZDT6_LL_Counter_LOI.pdf (244 KB)

Body excerpt:
Jason — LL came back at $9.25/SF NNN, holding firm on 10-year term. Attached is their redline...
```

Then proceed to **Common Processing (Step C1)**.

---

### TRIAGE MODE (`/email`)

#### Step R1 — Fetch unread

Call `mcp__outlook__list_inbox(count=50, unread_only=True)`.

If zero unread: report "Inbox clear." and stop.

#### Step R2 — Match and group

For each unread email, run **Deal Matching Logic** (see below). Present results grouped:

```
MATCHED TO DEALS:

ZDT6 (Royal Oak LOI): 2 emails
  1. [UNREAD] ZDT6 - LL Counter LOI — Tony Schmitt — May 24 [1 attachment]
  2. [UNREAD] RE: ZDT6 electrical clearance — Bryan Matthews — May 22

ZIN3 (Carmel Tech): 1 email
  3. [UNREAD] Permit approval update — Shannon Hunt — May 23

UNMATCHED / NEEDS ROUTING:
  4. [UNREAD] RE: Ferguson MSA redlines — Randy Hogan — May 21 [1 attachment]
  5. [UNREAD] New industrial site Dayton OH — Coldwell Banker — May 20
```

Ask Jason: "Process all matched ones? Or pick specific numbers? What about the unmatched ones?"

#### Step R3 — Process selected

For each email Jason selects: call `mcp__outlook__get_email(entry_id="{id}", include_body=True)` then proceed to **Common Processing (Step C1)**.

For unmatched emails: ask Jason which deal file they belong to, or whether to skip or run `/intake`. Never route silently.

---

### COMMON PROCESSING (per email)

#### Step C1 — Confirm deal match

State the matched deal file path (e.g., `Amazon/Quick Commerce/Cleveland_University Heights_ZCL2.md`). If the match was exact (site code in subject), proceed. If it was fuzzy (keyword or sender-based), ask Jason to confirm before writing.

If no deal can be matched and Jason can't identify one:
- Looks like a new deal → suggest `/intake`
- Truly unroutable → skip and note it in the final report

#### Step C2 — Re-read the deal file

Read the deal file immediately before writing. Never work from cached content.

#### Step C3 — Compose the note entry

Date = today's system date (never the email's received date — that's the capture date, not the event date).

```
YYYY-MM-DD - Email from {Sender Name} ({role if known, e.g. "local broker", "TM", "LL counsel"}). {One-line summary.}
{Key details — what was communicated, what's being asked, any deadlines or numbers.}
Attachments: filename1.pdf, filename2.docx   ← omit this line if no real attachments
```

Capture the substance faithfully. Don't rewrite or editorialize beyond what the email says.

#### Step C4 — Extract tasks

**Only create a task if the email explicitly requires Jason to take an action** — a deadline stated, a response requested, a document to send.

Status updates ("LL signed", "permit submitted", "site approved") are NOT tasks. Implied follow-ups ("let me know what you think") are NOT tasks.

If a task is warranted and no due date is given, default to 1 week from today.

```
- [ ] Task description 📅 YYYY-MM-DD
- [ ] 🔺 High priority task 📅 YYYY-MM-DD
```

#### Step C5 — Handle attachments

If the email has attachments:

1. Determine the docs folder using **Attachment Routing** below.
2. If routing is uncertain, confirm with Jason before saving.
3. Call `mcp__outlook__save_all_attachments(entry_id="{id}", destination_folder="{path}")`.
   - The server automatically skips embedded images (logos, signatures) — only real file attachments are saved.
4. If the docs folder doesn't exist, the server creates it. Note the creation in the report.

If no attachments (or all are embedded images): note "No attachments." in the report.

**macOS check:** if running on macOS (not the Windows work computer), skip all attachment steps and note "Attachment saving skipped — docs folders are Windows-only."

#### Step C6 — Write to deal file

1. Prepend the note entry to the top of `## Notes` (newest first)
2. Add any tasks to `## Tasks`
3. Update YAML:
   - `last_updated:` → today's date
   - `last_note:` → one-line summary matching the note's first line

#### Step C7 — Mark email read

Call `mcp__outlook__mark_email_read(entry_id="{id}")`.

**Only after the vault write succeeds.** If the write failed, don't mark read.

#### Step C8 — Loop or finish

In triage mode: move to the next email in the queue. In targeted mode: if Jason selected multiple, continue; otherwise finish.

---

### Final Report

After all emails are processed:

```
- ZDT6 updated — LL counter at $9.25/SF NNN; redline received from Tony Schmitt
- ZIN3 updated — permit approval pushed to June 9 per Shannon Hunt
- Attachments saved → Amazon\ZDT6\: ZDT6_LL_Counter_LOI.pdf
- Tasks created: "Respond to ZDT6 LL counter" due 2026-05-31
- 2 emails marked read
- #4 (Ferguson MSA / KBC) — skipped; Randy Hogan email, no KBC deal file found. Run /intake or tell me the file name.
- #5 (Coldwell Banker / Dayton) — skipped per Jason
```

---

## Deal Matching Logic

Run these checks in order. Stop at the first confident match.

1. **Exact site code in subject** — scan for patterns like `ZDT6`, `CVG47`, `ZIN3` (2–5 uppercase alphanumeric characters, typically 3–4 letters + 1–2 digits). Match against `site_code:` fields across vault deal files.

2. **Site code in body (first 300 chars)** — same pattern scan applied to the email body excerpt.

3. **Keyword vault search** — strip `RE:`, `FW:`, `[EXTERNAL]`, and brackets from the subject. Extract 2–3 meaningful terms. Run vault search. If exactly one deal file matches, use it.

4. **Sender match** — check sender name/email against `tm:`, `local_broker:` YAML fields in active deal files, or against People/ pages.

5. **Ambiguous or no match** → ask Jason. Never guess silently. Never write to a deal file without confirmation.

---

## Attachment Routing

| Deal program | Docs folder path |
|---|---|
| AMZL | `C:\Users\kirkham\Documents\Amazon\{site_code}\` |
| GCF | `C:\Users\kirkham\Documents\Amazon\{site_code}\` |
| Middle Mile | `C:\Users\kirkham\Documents\Amazon\{site_code}\` |
| Renewals | `C:\Users\kirkham\Documents\Amazon\{site_code}\` |
| SSD | `C:\Users\kirkham\Documents\Amazon\{site_code}\` |
| Quick Commerce | `C:\Users\kirkham\Documents\Amazon\Quick Commerce\{site_code}\` |
| KBC matters | `C:\Users\kirkham\Documents\KBC Legal\{project_folder}\` |
| Kirkham Law matters | Ask Jason — no standard path |

For pre-code deals (working name, no `site_code:` assigned yet), use the working name as the folder name — same convention as `/intake`.

---

## Out of Scope

- **New deal files** → say so, suggest `/intake`, stop
- **Legal drafting or review** → log that it was requested, then ask Jason what he needs; do not produce any legal work
- **Emails with no deal connection** → ask Jason how to route; never skip silently

---

## Rules

- **Re-read each deal file immediately before writing** — never work from cached content
- **Today's system date for note headers** — not the email's received date
- **Tasks only when email explicitly requires Jason to act** — status updates and implied follow-ups are not tasks
- **Mark email read only after the vault write succeeds**
- **Never create new deal files** — update existing ones only
- **Confirm routing if uncertain** — especially KBC matters where the project folder name may not be obvious
- **Inbox reads from Outlook's default account** — if Jason needs a specific non-default account, this skill can't reach it without server changes

---

## Note Entry Format

```
YYYY-MM-DD - Email from {Sender Name} ({role}). {One-line summary.}
{Supporting detail — what was communicated, numbers, deadlines, what's being asked.}
Attachments: filename1.pdf, filename2.docx
```

## Task Format

```
- [ ] Task description 📅 YYYY-MM-DD
- [ ] 🔺 High priority task 📅 YYYY-MM-DD
```

---

## Example 1 — Targeted Mode with Attachment

**Invocation:** `/email ZDT6`

**Step T1:** Searches "ZDT6". Returns:
```
1. [UNREAD] ZDT6 - 313 E. Hudson — LL Counter LOI — Tony Schmitt — May 24 [1 attachment]
2. [READ]   RE: ZDT6 - ADA survey schedule — Bryan Matthews — May 22
```

**Step T2:** Jason says "1".

**Step T3:** Fetches email 1:
```
From: Tony Schmitt <tschmitt@midamericagrp.com>
Subject: ZDT6 - 313 E. Hudson — LL Counter LOI
Date: 2026-05-24
Attachments: ZDT6_LL_Counter_LOI.pdf (244 KB)

Body excerpt:
Jason — LL came back at $9.25/SF NNN, 10-year term, holding on TI. Attached is their redline of our LOI. Let me know how you want to respond.
```

**Step C1:** "Matched to ZDT6 → `Amazon/Quick Commerce/Detroit_Royal Oak_ZDT6.md`."

**Step C2:** Re-reads deal file.

**Step C3:** Composes note:
```
2026-05-25 - Email from Tony Schmitt (local broker). LL counter at $9.25/SF NNN, 10-year term, holding on TI — redline attached.
Attachments: ZDT6_LL_Counter_LOI.pdf
```

**Step C4:** "Let me know how you want to respond" = implicit ask, but no explicit deadline or action stated → no task by default. (If Jason wants a task, he can say so.)

**Step C5:** Routes to `C:\Users\kirkham\Documents\Amazon\Quick Commerce\ZDT6\`. Saves `ZDT6_LL_Counter_LOI.pdf`.

**Step C6:** Prepends note to `## Notes`. Updates `last_updated: 2026-05-25`, `last_note: LL counter $9.25 NNN, 10-yr, holding TI — redline received`.

**Step C7:** Marks email read.

**Report:**
```
- ZDT6 updated — LL counter $9.25/SF NNN, 10-year, holding TI; redline from Tony Schmitt
- Attachment saved → Amazon\Quick Commerce\ZDT6\: ZDT6_LL_Counter_LOI.pdf
- No tasks created (no explicit deadline or action in email)
- 1 email marked read
```

---

## Example 2 — Triage Mode (3 unread emails)

**Invocation:** `/email`

**Step R1:** Fetches 50 unread → returns 3.

**Step R2:** Groups:
```
MATCHED:
ZIN3 (Carmel Tech Center): 1 email
  1. Permit approval update — Shannon Hunt — May 25

Ferguson MSA (KBC): 1 email
  2. RE: Ferguson MSA redlines — Randy Hogan — May 24 [1 attachment]

UNMATCHED:
  3. New industrial site Dayton OH — Coldwell Banker — May 23
```

Asks: "Process 1 and 2? What about #3?"

Jason: "Do 1 and 2. Skip 3."

**Email 1 — ZIN3:**
Permit approval pushed to June 9 (was June 2). Status update only — no action required.

Note:
```
2026-05-25 - Email from Shannon Hunt (local broker). Permit approval pushed to June 9 (was June 2).
```
No task. Prepends to ZIN3. Updates YAML. Marks read.

**Email 2 — Ferguson MSA (KBC):**
Randy Hogan sends revised MSA v3 with two remaining redlines. "Please review by end of week."

Note:
```
2026-05-25 - Email from Randy Hogan (Ferguson). MSA v3 with 2 remaining redlines attached — review requested by end of week.
Attachments: Ferguson_MSA_v3_redlined.docx
```
Task: "review by end of week" = explicit action + deadline.
```
- [ ] 🔺 Review Ferguson MSA v3 redlines and respond 📅 2026-05-29
```
Routes attachment to `C:\Users\kirkham\Documents\KBC Legal\Ferguson MSA\`. Marks read.

**Final Report:**
```
- ZIN3 updated — permit approval pushed to June 9 per Shannon Hunt
- Ferguson MSA updated — MSA v3 with 2 redlines received from Randy Hogan
- Attachment saved → KBC Legal\Ferguson MSA\: Ferguson_MSA_v3_redlined.docx
- Task created: "Review Ferguson MSA v3 redlines and respond" due 2026-05-29
- 2 emails marked read
- #3 (Coldwell Banker / Dayton) skipped per Jason
```
