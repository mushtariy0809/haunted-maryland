# 👻 Haunted Maryland

An interactive map of 170 reported haunted places in Maryland, built on **Amazon Location Service** + **MapLibre GL JS**.
Click a glow to read the story, hit **Summon a ghost** for a random haunting, or search ("cemetery", "Fells Point").

## How it works

```
Haunted Places CSV ──► scripts/build_geojson.py ──► maryland-haunted.geojson (S3)
                                                        │
Amazon Location (Maps API key) ──► MapLibre GL JS ◄─────┘   index.html, hosted on Amplify
```

- **Data:** Haunted Places dataset (Tim Renner, via TidyTuesday 2023-10-10), filtered to Maryland. Rows without exact coordinates fall back to town coordinates and are tagged "approximate location".
- **Map:** Amazon Location Service `Monochrome` style in dark mode, rendered with MapLibre. Clustering, popups, and search all run client-side.
- **Hosting:** AWS Amplify Hosting (or S3 + CloudFront).

## Setup (~20 min)

1. **Get an Amazon Location API key**
   AWS Console → Amazon Location Service → **API keys** → Create.
   Allow **Maps** actions (GetStyleDescriptor, GetTile, etc.), and under referrers add your Amplify URL and `http://localhost:*` for testing.
2. **Paste it in** `index.html`:
   ```js
   const AWS_API_KEY = "v1.public....";
   const AWS_REGION  = "us-east-1"; // the region you made the key in
   ```
   With no key, the page falls back to a free OpenFreeMap basemap so you can still preview it.
3. **(Optional) put the data in S3:** upload `data/maryland-haunted.geojson` to a bucket, enable CORS, and set `DATA_URL` to the object URL.
4. **Deploy:** zip `index.html` + the `data/` folder → AWS Amplify → **Deploy without Git** → drag in the zip. You get a live `amplifyapp.com` URL.

Test locally: `python3 -m http.server` in this folder, then open http://localhost:8000.

## Rebuild the data / try another state

```bash
python3 scripts/build_geojson.py haunted_places.csv data/maryland-haunted.geojson MD
```
Swap `MD` for any state abbreviation (then update the map center and the "near campus" coordinates).

## 15-minute class demo script

| Time | What to do |
|---|---|
| 0–2 | Hook: "There are **32 haunted spots within 10 miles of this room**." Open the map. |
| 2–5 | Hit **Near campus**, let the class pick glows to open. Hit **Summon a ghost** a couple of times. Search "cemetery". |
| 5–10 | Show the stack: one HTML file, a GeoJSON file, an Amazon Location API key. Open the code and point to the 3 config lines. |
| 10–13 | Live deploy: drag the zip into Amplify and open the real URL on your phone. |
| 13–15 | Plug the AWS Builder Center **Map It** weekend challenge (closes Mon, Nov 2, 4 PM ET, 18+). |

**Backup plan:** have the live URL already open in a second tab in case Wi-Fi or Amplify is slow.
