---
name: image-digest
description: Analyze and extract content from images — screenshots, handwritten notes, scanned docs, pasted images from Obsidian. Use when the user provides an image file path (.png, .jpg, .jpeg, .webp, .gif) or an Obsidian embed (![[...]]), or says "digest/read/transcribe this image."
---

# image-digest

Read and extract content from image files using Claude's native vision. No Python needed — the Read tool handles images directly.

## Trigger conditions
- User provides a file path ending in `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`
- User provides an Obsidian embed like `![[Pasted image 20260513.png]]`
- User says "digest/read/transcribe this image"

## Workflow

### 1. Resolve the path

If given an Obsidian `![[filename]]` embed, extract the filename and locate the file. Common attachment folders (check in order):
- `{VAULT_ROOT}/Attachments/{filename}`
- `{VAULT_ROOT}/{filename}`
- Same folder as the active note
- Use Glob `**/{filename}` as a fallback

If given a full path, use it directly.

### 2. Read the image

Use the Read tool — Claude is multimodal and reads PNG/JPG/etc. natively:

```
Read(file_path="C:\...\image.png")
```

### 3. Identify content type and extract

| Content type | Extraction approach |
|---|---|
| Email / message screenshot | Sender, recipient, date, subject, full body |
| Handwritten notes | Verbatim transcription, preserve structure |
| Typed document / contract page | Full text, preserve section headers |
| Table / spreadsheet | Reconstruct as markdown table |
| Whiteboard / diagram | Describe structure, extract all visible text |
| Property / site photo | Describe key features relevant to the deal |
| Mixed / unclear | Extract all readable text, then describe visuals |

### 4. Present the extracted content

Output clean markdown. For emails:

```
**From:** ...
**To:** ...
**Date:** ...
**Subject:** ...

{body}
```

For notes/documents, preserve structure as closely as possible. For tables, use GFM table syntax.

If anything is illegible, say so explicitly — don't invent content.

### 5. Ask what to do

After presenting:

> Want me to log this to a deal file, daily note, or somewhere else?

If yes, follow standard note entry format (YYYY-MM-DD prepended to `## Notes`).

## Key notes

- If the image path can't be found, ask the user to confirm the location or drag the file in
- Don't write SSNs, passwords, or other sensitive credentials to deal files without confirming
- If the image is a multi-page doc scan, note that only the visible page is captured
