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
  marks: [
    Plot.rectY(hits_per_day, {
      x: "date",
      y: "hits",
      interval: Plot.utcInterval("day"),
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
SELECT "cs-uri-stem", COUNT() as hits
FROM github_blog
GROUP BY "cs-uri-stem"
ORDER BY hits DESC
LIMIT ${uriPageLimit}
OFFSET ${uriPageLimit * uriPage}
`;

const uriPlot = Plot.plot({
  marks: [
    Plot.ruleY([0]),
    Plot.barY(hits_per_uri, {
      x: "cs-uri-stem",
      y: "hits",
      sort: { x: "y", order: "descending" },
    }),
  ],
});
```

</div><div class="card">${referrerPlot}

```js
const totalReferrers = [
  ...(await sql`
SELECT COUNT(DISTINCT RTRIM("cs(Referer)", '/')) as count
FROM github_blog
WHERE "cs(Referer)" != '-'
`),
][0].count;
const referrerPageLimit = 10;
const totalReferrerPages = Math.ceil(totalReferrers / referrerPageLimit);
const referrerPage = view(PageButtons("referrer", totalReferrerPages));
```

<span>Page ${referrerPage + 1} of ${totalReferrerPages}</span>

```js
const hits_per_referrer = await sql`
SELECT RTRIM("cs(Referer)", '/') as "cs(Referer)", COUNT() as hits
FROM github_blog
WHERE "cs(Referer)" != '-'
GROUP BY RTRIM("cs(Referer)", '/')
ORDER BY hits DESC
LIMIT ${referrerPageLimit}
OFFSET ${referrerPageLimit * referrerPage}
`;

const referrerPlot = Plot.plot({
  marks: [
    Plot.ruleY([0]),
    Plot.barY(hits_per_referrer, {
      x: "cs(Referer)",
      y: "hits",
      sort: { x: "y", order: "descending" },
    }),
  ],
});
```

</div>
</div>
