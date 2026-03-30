---
date: "{{date:MM-DD-YYYY}}"
tags: [daily]
---

> [!info] Daily Stoic
> <%* try {
    const res = await fetch("https://api.themotivate365.com/stoic-quote");
    const data = await res.json();
    tR += `"${data.quote}" \n> — ***${data.author}***`;
  } catch (err) {
    tR += "The impediment to action advances action. (ἐφ᾽ ἡμῖν)";
  }
%>

---

## Notes
<!-- Format: **DEAL** - note. e.g. **CVG47** - called Phil, IDI eval still pending -->

-

## EOD Processed
<!-- Charlie stamps this when done -->
