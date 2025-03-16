---
sql:
  github_blog: ./github_blog.tsv
---

# dashboards

```js
import { UAParser } from "ua-parser-js";
const to_record = (row) => ({
  // date: row[0],
  // time: row[1],
  datetime: (() => {
    const [hours, minutes, seconds] = row[1].split(":");
    row[0].setHours(Number(hours));
    row[0].setMinutes(Number(minutes));
    row[0].setSeconds(Number(seconds));
    return row[0];
  })(),
  /// "x-edge-location": row[2],
  "sc-bytes": row[3],
  "c-ip": row[4],
  "cs-method": row[5],
  // "cs(Host)": row[6],
  "cs-uri-stem": row[7],
  "sc-status": row[8],
  "cs(Referer)": row[9],
  // "cs(User-Agent)": row[10],
  userAgent: UAParser(row[10]),
  "cs-uri-query": row[11],
  // "cs(Cookie)": row[12],
  "x-edge-result-type": row[13],
  // "x-edge-request-id": row[14],
  "x-host-header": row[15],
  "cs-protocol": row[16],
  "cs-bytes": row[17],
  "time-taken": row[18],
  "x-forwarded-for": row[19],
  // "ssl-protocol": row[20],
  // "ssl-cipher": row[21],
  // "x-edge-response-result-type": row[22],
  "cs-protocol-version": row[23],
  // "fle-status": row[24],
  // "fle-encrypted-fields": row[25],
  // "c-port": row[26],
  "time-to-first-byte": row[27],
  // "x-edge-detailed-result-type": row[28],
  "sc-content-type": row[29],
  "sc-content-len": row[30],
  // "sc-range-start": row[31],
  // "sc-range-end": row[32],
});
/*
const data = (
  await FileAttachment("github_blog.tsv").tsv({
    array: true,
    typed: true,
  })
).map(to_record);
display(data[0]);
*/
```

```js
const hits_per_day = [
  ...(await sql`
SELECT date, COUNT() as hits
FROM github_blog
GROUP BY date
`),
].map(({ date, hits }) => ({
  date: new Date(date),
  hits,
}));
display(
  Plot.plot({
    marks: [
      Plot.rectY(hits_per_day, {
        x: "date",
        y: "hits",
        interval: Plot.utcInterval("day"),
      }),
    ],
  }),
);
```

```js
const hits_per_uri = await sql`
SELECT "cs-uri-stem", COUNT() as hits
FROM github_blog
GROUP BY "cs-uri-stem"
ORDER BY hits DESC
LIMIT 10
`;

display(
  Plot.barY(hits_per_uri, {
    x: "cs-uri-stem",
    y: "hits",
    sort: { x: "y", order: "descending" },
  }).plot(),
);
```

```js
const hits_per_referrer = await sql`
SELECT "cs(Referer)", COUNT() as hits
FROM github_blog
WHERE "cs(Referer)" != '-'
GROUP BY "cs(Referer)"
ORDER BY hits DESC
LIMIT 10
`;

display(
  Plot.barY(hits_per_referrer, {
    x: "cs(Referer)",
    y: "hits",
    sort: { x: "y", order: "descending" },
  }).plot(),
);
```
