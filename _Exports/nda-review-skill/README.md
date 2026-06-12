# NDA Review Skill (for Claude Code)

A Claude Code skill that reviews an NDA against a standing confidentiality
playbook and produces:

- A written **Review Memo** (flags issues, classifies them, suggests fixes)
- For `.docx` inputs, a **Redlined DOCX** with Word-native tracked changes and comments

## Install

1. Copy this whole `nda-review-skill/` folder into your project's
   `.claude/skills/` directory and rename it to `nda` (folder name doesn't
   strictly matter, but `nda` matches the `/nda` trigger below):

   ```
   your-project/
     .claude/
       skills/
         nda/
           SKILL.md
           scripts/
             pack.py
             unpack.py
   ```

2. Make sure Python 3 is available, with these packages:
   ```
   pip install python-docx
   pip install pymupdf   # only needed if you want to review PDF NDAs
   ```

3. Restart Claude Code (or start a new session) so it picks up the skill.

## Use

```
/nda                  # looks for an NDA file in the current directory
/nda "Acme NDA.docx"  # reviews a specific file
```

## Customize the playbook

The playbook (Sections A–L in `SKILL.md`) encodes one firm's standard NDA
positions — mutual vs. one-way, term limits, non-solicitation, governing law,
etc. Before relying on this for real review work, edit those sections to
reflect your own firm's positions. Everything else (workflow, redline XML
mechanics) is generic and shouldn't need changes.
