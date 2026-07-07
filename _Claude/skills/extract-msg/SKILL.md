---
name: extract-msg
description: Read Outlook .msg email files using extract-msg. Use when the user provides a .msg file path — saved emails from counterparties, Amazon TMs, brokers, or counsel. Extracts sender, recipients, subject, body, and attachments.
---

# extract-msg

Read Outlook `.msg` email files.

```python
import extract_msg  # underscore, not hyphen
```

## Read an email

```python
import extract_msg

path = r'C:\path\to\email.msg'
msg = extract_msg.Message(path)

print(f'From:    {msg.sender}')
print(f'To:      {msg.to}')
print(f'CC:      {msg.cc}')
print(f'Date:    {msg.date}')
print(f'Subject: {msg.subject}')
print()
print(msg.body)

msg.close()
```

## Check attachments

```python
msg = extract_msg.Message(path)
for att in msg.attachments:
    print(f'Attachment: {att.longFilename or att.shortFilename}')
msg.close()
```

## Save attachments to disk

```python
import os, extract_msg

msg = extract_msg.Message(path)
out_dir = r'C:\path\to\output'
for att in msg.attachments:
    name = att.longFilename or att.shortFilename or 'attachment'
    with open(os.path.join(out_dir, name), 'wb') as f:
        f.write(att.data)
msg.close()
```

## HTML body (if plain text body is empty)

```python
msg = extract_msg.Message(path)
body = msg.body or msg.htmlBody
msg.close()
```

## Key notes

- Import is `extract_msg` (underscore)
- Always call `msg.close()` when done
- `msg.date` returns a `datetime` object
- Nested `.msg` attachments (email-within-email) can be opened recursively as `extract_msg.Message`
- If body is blank, try `msg.htmlBody` — some emails are HTML-only
