<%*
  // 1. Rename the file to today's date (Month DD, YYYY)
  await tp.file.rename(`${tp.date.now("MMMM DD, YYYY")}`);
%>
---
date: <% tp.date.now("MMMM DD, YYYY") %>
tags: [daily]
---
**Weather:** <%* try {
  const res = await fetch("https://wttr.in/New+Albany+Ohio?format=%c+%t+%C");
  const weather = await res.text();
  tR += weather;
} catch (err) {
  tR += "Weather data unavailable";
}
%>

> [!info] Daily Stoic
> <%* try {
    const res = await fetch("https://api.themotivate365.com/stoic-quote");
    const data = await res.json();
    tR += `"${data.quote}" \n> — ***${data.author}***`;
  } catch (err) {
    tR += "The impediment to action advances action. (ἐφ᾽ ἡμῖν)";
  }
%>

## Today

> What happened. What you noticed. Whatever's on your mind.

---

## Mine / Not Mine

---

## Pattern Watch