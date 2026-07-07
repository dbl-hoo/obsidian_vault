# _Claude — Synced Claude Code Configuration

Obsidian Sync does **not** sync dot-folders, so `.claude/` is machine-local. This folder is the canonical, synced home for skills. Each machine links `.claude/skills` to `_Claude/skills` so every machine runs the same skills.

## Machine setup

**Linux / macOS (done on Dathomir 2026-07-07):**

```
cd <vault root>
mv .claude/skills/* _Claude/skills/   # migrate any machine-local skills first
rmdir .claude/skills
ln -s ../_Claude/skills .claude/skills
```

**Windows (work machine) — run in an elevated cmd prompt:**

```
cd /d "<vault root>"
:: 1. Migrate the machine-local skills (weekly-review, eod) into the synced folder:
robocopy .claude\skills _Claude\skills /E
rmdir /s /q .claude\skills
:: 2. Create the junction:
mklink /J .claude\skills _Claude\skills
```

After step 1 syncs, all machines get weekly-review and eod automatically.

## Notes

- `settings.local.json` stays machine-local by design (permissions differ per machine). Don't move it here.
- Claude memory (`~/.claude/projects/.../memory/`) is also machine-local. Anything both machines must know goes in `CLAUDE.md`, not memory.
- New skills go in `_Claude/skills/<name>/SKILL.md` with `name:` and `description:` frontmatter.
