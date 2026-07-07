---
name: weekly-review
description: Interactive weekly review of all active Amazon and KBC deals — flags overdue/stale items, works through deals one at a time, updates in real time, and wraps up with portfolio overview rebuild, vault lint, and calendar prep.
---

# Weekly Review Skill

Triggered by `/weekly-review` or "weekly review" or similar.

This is interactive — work through deals one at a time, wait for Jason's input before moving to the next.

## Step 1 — Load the queue

Read all deal files with `status: Surveying` or `status: Selected` across `Amazon/`, `Amazon/Quick Commerce/`, `Amazon/Project A/`, and `KBC/`. **Exclude any file with `review: skip` in its YAML** — passive engagements Jason doesn't want re-litigated weekly. Build two lists:
- **Needs attention:** overdue tasks (due date < today) OR no update in >14 days
- **Everything else:** active deals, sorted by `last_updated` ascending (stalest first)

**Checkpoint file:** Write the full queue to `.claude/weekly-review-checkpoint.md` (one line per deal: `- [ ] {site_code}`). Check each off as its deal is completed. If the file already exists when the review starts, a prior review was interrupted — offer to resume from the first unchecked deal instead of starting over. Delete the file at wrap-up.

Present the counts upfront:
> Weekly review — X Amazon deals, Y KBC matters. Z flagged for attention.

## Step 2 — Flagged items first

For each flagged deal, surface:
- Deal name + last updated date
- Most recent `## Notes` entry
- All open tasks with due dates

Ask Jason: *Any updates? Status change? Tasks to close?*
Apply any changes before moving to the next item. Do NOT create new tasks unless Jason explicitly dictates one.

## Step 3 — Remaining deals

Work through the rest in stalest-first order. Same format: last note, open tasks, prompt for input.
If Jason says "skip" or "nothing" — move on, no changes.

## Step 4 — Calendar

1. Prompt Jason to review his Outlook calendar for the week and identify any tasks from it.
2. Go through open tasks for the coming week — flag anything that needs prep or has likely changed.

## Step 5 — Wrap-up

After all deals:
1. Report what was updated (deal name + what changed)
2. Flag any deals Jason skipped that are >30 days stale — surface them so he can decide if they're dead or just quiet
3. **Delete completed tasks** — scan all deal files for `- [x]` tasks and remove them. Report count deleted.
4. Run Vault Lint (`/lint` skill — `_Claude/skills/lint/SKILL.md`) and report results
5. Suggest any `CLAUDE.md` improvements if the review surfaced gaps

## Rules
- Apply updates in real time — don't batch at the end
- **Prefix every write confirmation with the site code** (e.g. "DOH3 — logged PSA update, status → Selected"), so misattributed updates are caught immediately
- **If Jason's answer names a different deal than the one on deck, treat it as a redirect** — apply it to the named deal, confirm, then return to the deal in progress. Never apply it positionally to the current deal.
- If Jason says a deal is passive / "stop asking about this one," set `review: skip` in its YAML so it drops out of future reviews
- Re-read each deal file immediately before presenting it and before writing
- If Jason says a deal is closed/dead, update `status:` immediately
- **Never create tasks proactively** — only add a task if Jason explicitly dictates one during the session
