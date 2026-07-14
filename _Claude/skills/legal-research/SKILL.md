---
name: legal-research
description: Answer legal/regulatory research questions (licensing, commission sharing, brokerage law, statutes, state-specific rules) by checking the vault knowledgebase first, researching the web only if needed, and saving the answer back to the knowledgebase with citations. Use when Jason asks a "does state X allow...", "can a broker...", "what does the statute say..." style question.
---

# Legal Research Skill

Triggered by `/legal-research` or any legal/regulatory research question — licensing, commission sharing, referral fees, statutory questions, state-by-state rules.

**This is research, not legal work product.** Producing memos, redlines, or opinions is separate — see CLAUDE.md's legal-work rule.

---

## Workflow

### Step 1 — Check the knowledgebase FIRST

Before any web research:

1. Grep `_Knowledgebase/` (all subfolders) for the topic's key terms — statute numbers, state names, subject words ("commission", "referral", "licensing", etc.). Also Glob filenames — topics are often named by subject.
2. Read any matching file in full before deciding it does or doesn't answer the question.

Then branch:

- **KB answers the question and `last_verified` is within 12 months** → answer from the KB. Cite the KB file, repeat its citations, and state the last-verified date. **Do not re-research.** Done — skip to Step 4.
- **KB covers the topic but is stale (>12 months), incomplete, or the question extends it** → answer what the KB supports, then research the gap (Step 2) and update the existing file (Step 3).
- **No KB coverage** → research (Step 2) and create a new topic file (Step 3).

### Step 2 — Research

- Use WebSearch. **Prefer primary sources:** the statute itself (state legislature sites, official code), the state regulator (DOS, real estate commission), then Justia/FindLaw/Casetext as secondary confirmation.
- Pin down the actual statute/regulation cite (e.g., "N.Y. RPL § 442", "N.J.S.A. 45:15-3.1") — never cite only a blog post or law-firm marketing page.
- Note effective dates or recent amendments if they surfaced.
- If sources conflict or the rule is genuinely unsettled, say so — flag for local counsel rather than papering over it.

### Step 3 — Update the knowledgebase

**Location — route by subject area:**

| Subject | Folder |
|---|---|
| KBC brokerage/licensing/commission/legal | `_Knowledgebase/KBC/` |
| Amazon program/deal-structure reference | `_Knowledgebase/Amazon/` |
| Personal legal | `_Knowledgebase/Personal/` |

Default to `_Knowledgebase/KBC/` when unclear. Flat files, one topic per file, descriptive title-case filename (e.g., `NY-NJ Broker Commission Sharing.md`).

**Before creating a new file**, re-check for an existing file the answer belongs in — extending an existing topic beats creating a near-duplicate. (E.g., a question about a non-licensed state belongs in `Out-of-State Commission Paths.md`, not a new file.)

**File format** (match existing KB files):

```markdown
---
title: {Topic}
area: KBC            # or Amazon | Personal
tags: [kbc, reference, {subject tags}]
last_updated: YYYY-MM-DD    # today, from the system
last_verified: YYYY-MM-DD   # date the law was last confirmed current
---

# {Question or Topic as a heading}

**Short answer:** {one-line conclusion up front}

{Analysis — rule, caveats, how to structure around it. Bullets over prose.}

## Citations

- [Statute name § number (source)](url)
- {Every load-bearing source, primary first. Uncited assertions don't go in the KB.}

> Research summary, not a formal legal opinion. Verify current statutory text before structuring a specific deal.

See also: [[Related KB Topic]]
```

**When updating an existing file:**
- Refresh `last_updated` and `last_verified`
- Add the new material in place (new section or extended row), keeping the file organized by topic — not an append-only log
- **If new research contradicts a prior conclusion, don't silently overwrite** — state the change and date it (e.g., "*Updated 2026-07-11: WV dropped the in-state-office requirement (2025 SB 747); prior guidance superseded.*")
- Add `See also: [[...]]` cross-links between related topic files in both directions

### Step 4 — Report back

- Lead with the answer, then caveats.
- Include the citations inline (markdown links).
- Say where it lives: "Saved to `_Knowledgebase/KBC/{file}.md`" or "Answered from KB (`{file}.md`, verified {date})".

---

## Rules

- **KB first, always.** Web research when the KB already answers the question wastes time and risks inconsistent answers.
- **Citations are mandatory.** Every conclusion in a KB file traces to a named statute/regulation with a link. No cite → doesn't go in.
- **Primary sources over commentary.** Blogs and firm articles are leads, not authority.
- **One topic per file.** Extend existing files; don't create near-duplicates.
- **Flag unsettled law** — a 🚩 with "confirm with local counsel" beats a confident wrong answer (see `Out-of-State Commission Paths.md` for the pattern).
- **Research ≠ legal work.** If the question morphs into "draft/redline/opine for a client," stop and ask per CLAUDE.md.
