# dashboards

```js
const to_record = (row) => ({
  date: row[0],
  time: row[1],
  /// "x-edge-location": row[2],
  "sc-bytes": row[3],
  "c-ip": row[4],
  "cs-method": row[5],
  // "cs(Host)": row[6],
  "cs-uri-stem": row[7],
  "sc-status": row[8],
  "cs(Referer)": row[9],
  "cs(User-Agent)": row[10],
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
const data = (
  await FileAttachment("github_blog.tsv").tsv({
    array: true,
    typed: true,
  })
).map(to_record);
display(data[0]);
```
