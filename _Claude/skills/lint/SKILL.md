---
name: lint
description: Non-interactive vault health check — stale deals, overdue tasks, YAML gaps, and orphan files. Report only, no fixes. Run on demand ("lint the vault", "health check") or as the wrap-up step of /weekly-review.
---

# Vault Lint Skill

Triggered by `/lint`, "lint the vault", "health check", or as Step 5 of `/weekly-review`.

**Report only — never auto-fix anything.** Jason decides what to act on.

## Scope

Scan active deal files: `Amazon/**` (including `Quick Commerce/` and `Project Mercury/`), `KBC/`, and `Kirkham Law/`. Skip `x_Archive/` entirely. Files with `status: Not Started` (e.g. unstarted Mercury MSAs) or `review: skip` are exempt from the staleness check but still count for YAML gaps.

Get today's date from the system before computing any staleness or overdue math.

## Checks

1. **Stale deals** — `status: Surveying` or `status: Selected` with `last_updated` >30 days ago
2. **Overdue tasks** — open `- [ ]` tasks with `📅` due dates in the past, across all active deal files
3. **YAML gaps** — required fields (per the conventions in `CLAUDE.md`) that are blank or missing
4. **Orphan files** — files in deal folders that don't match any naming convention

## Output

Bulleted report grouped by category, severity-flagged:

- `🔴` Action needed (overdue tasks, stale deals)
- `🟡` Worth checking (YAML gaps, orphans)
- `🟢` Clean (no issues in category)

Keep it terse — one line per finding, `file: issue` format. End with a one-line count summary (e.g. "3 🔴 / 5 🟡 / 4 categories clean").
