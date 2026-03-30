---
tags: [dashboard, moc]
---

# Deal Dashboard

## Amazon — Active Deals

```dataview
TABLE WITHOUT ID
  link(file.path, site_code) AS "Site Code",
  deal_type AS "Type",
  business_unit AS "BU",
  tm AS "TM",
  status AS "Status",
  last_updated AS "Last Updated"
FROM "Amazon"
WHERE contains(tags, "amazon") AND status = "Ongoing" AND !contains(file.folder, "Quick Commerce") AND !contains(file.folder, "Project A")
SORT last_updated DESC
```

## Amazon — Quick Commerce

```dataview
TABLE WITHOUT ID
  link(file.path, file.name) AS "Site",
  status AS "Status",
  last_updated AS "Last Updated"
FROM "Amazon/Quick Commerce"
WHERE contains(tags, "amazon")
SORT last_updated DESC
```

## Amazon — Project A

```dataview
TABLE WITHOUT ID
  link(file.path, file.name) AS "Project",
  status AS "Status",
  last_updated AS "Last Updated"
FROM "Amazon/Project A"
WHERE contains(tags, "amazon")
SORT last_updated DESC
```

## KBC — Active

```dataview
TABLE WITHOUT ID
  link(file.path, file.name) AS "Matter",
  status AS "Status",
  last_updated AS "Last Updated"
FROM "KBC"
WHERE contains(tags, "kbc") AND status = "Ongoing"
SORT last_updated DESC
```

## Kirkham Law — Active

```dataview
TABLE WITHOUT ID
  link(file.path, file.name) AS "Matter",
  status AS "Status",
  last_updated AS "Last Updated"
FROM "Kirkham Law"
WHERE contains(tags, "kirkham-law")
SORT last_updated DESC
```

## Personal — Active

```dataview
TABLE WITHOUT ID
  link(file.path, file.name) AS "Project",
  status AS "Status"
FROM "Personal"
WHERE contains(tags, "personal") AND status = "Ongoing"
SORT file.name ASC
```

## Quick Links

- [[Open Tasks]]
- [[Call Log]]
- [[Templates/new-deal|New Deal Template]]
- [[Templates/call-notes|Call Notes Template]]
- [[Templates/daily-note|Daily Note Template]]
