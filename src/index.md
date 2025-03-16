---
sql:
  github_blog: ./github_blog.parquet
---

# dashboards

```js
import { PageButtons } from "./PageButtons.js";
```

<div class="grid grid-cols-2">
  <div class="card">${dayPlot}

```js
const hits_per_day = [
  ...(await sql`
SELECT date, COUNT() as hits
FROM github_blog
GROUP BY date
ORDER BY date DESC
`),
].map(({ date, hits }) => ({
  date: new Date(date),
  hits,
}));
const dayPlot = Plot.plot({
  x: { label: "Day" },
  y: { label: "Hits" },
  marks: [
    Plot.rectY(hits_per_day, {
      x: "date",
      y: "hits",
      interval: Plot.utcInterval("day"),
      tip: true,
    }),
  ],
});
```

</div>
<div class="card">${uriPlot}

```js
const totalUris = [
  ...(await sql`
SELECT COUNT(DISTINCT "cs-uri-stem") as count
FROM github_blog
`),
][0].count;
const uriPageLimit = 10;
const totalUriPages = Math.ceil(totalUris / uriPageLimit);
const uriPage = view(PageButtons("uri", totalUriPages));
```

<span>Page ${uriPage + 1} of ${totalUriPages}</span>

```js
const hits_per_uri = await sql`
SELECT "cs-uri-stem" as uri, COUNT() as hits
FROM github_blog
GROUP BY uri
ORDER BY hits DESC
LIMIT ${uriPageLimit}
OFFSET ${uriPageLimit * uriPage}
`;

const uriPlot = Plot.plot({
  axis: null,
  marginRight: 130,
  y: { label: "URI" },
  x: { label: "Hits" },
  marks: [
    Plot.ruleX([0]),
    Plot.axisX({ anchor: "bottom", label: null }),
    Plot.axisX({ anchor: "top" }),
    Plot.axisY({ ticks: [] }),
    Plot.barX(hits_per_uri, {
      y: "uri",
      x: "hits",
      sort: { y: "x", order: "descending" },
      tip: true,
      fill: "lightblue",
    }),
    Plot.text(hits_per_uri, {
      y: "uri",
      x: "hits",
      text: "uri",
      textAnchor: "start",
      dx: 3,
    }),
  ],
});
```

</div><div class="card">${referrerPlot}

```js
const totalReferrers = [
  ...(await sql`
SELECT COUNT(DISTINCT SPLIT_PART("cs(Referer)", '/', 3)) as count
FROM github_blog
WHERE SPLIT_PART("cs(Referer)", '/', 3) != ''
`),
][0].count;
const referrerPageLimit = 10;
const totalReferrerPages = Math.ceil(totalReferrers / referrerPageLimit);
const referrerPage = view(PageButtons("referrer", totalReferrerPages));
```

<span>Page ${referrerPage + 1} of ${totalReferrerPages}</span>

```js
// TODO: add a toggle between partial (below) and full referrer values
const hits_per_referrer = await sql`
SELECT SPLIT_PART("cs(Referer)", '/', 3) as referrer, COUNT() as hits
FROM github_blog
WHERE referrer != ''
GROUP BY referrer
ORDER BY hits DESC
LIMIT ${referrerPageLimit}
OFFSET ${referrerPageLimit * referrerPage}
`;

const referrerPlot = Plot.plot({
  marginRight: 130,
  y: { label: "Referrer" },
  x: { label: "Hits" },
  marks: [
    Plot.ruleX([0]),
    Plot.axisX({ anchor: "bottom", label: null }),
    Plot.axisX({ anchor: "top" }),
    Plot.axisY({ ticks: [] }),
    Plot.barX(hits_per_referrer, {
      y: "referrer",
      x: "hits",
      sort: { y: "x", order: "descending" },
      tip: true,
      fill: "pink",
    }),
    Plot.text(hits_per_referrer, {
      y: "referrer",
      x: "hits",
      text: "referrer",
      textAnchor: "start",
      dx: 3,
    }),
  ],
});
```

</div>
<div class="card">
TODO: show all the filtered entries, once I have cross-chart filtering going on
</div>
</div>
