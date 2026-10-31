"""Turn the Haunted Places CSV into a Maryland-only GeoJSON file for the map.

Usage:
    python build_geojson.py <haunted_places.csv> <output.geojson> [STATE_ABBREV]

Source data: TidyTuesday 2023-10-10 "Haunted Places" (originally from Tim Renner / data.world).
"""
import csv
import json
import sys


def clean(text, limit=None):
    text = " ".join((text or "").split())
    if limit and len(text) > limit:
        text = text[:limit].rsplit(" ", 1)[0] + "…"
    return text


def main(src, dst, state="MD"):
    features = []
    with open(src, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["state_abbrev"] != state:
                continue
            lat, lon = row["latitude"], row["longitude"]
            approx = False
            # Some rows only have city coordinates: fall back to those and flag it
            if not lat or not lon or lat == "NA" or lon == "NA":
                lat, lon, approx = row["city_latitude"], row["city_longitude"], True
            try:
                lat, lon = float(lat), float(lon)
            except ValueError:
                continue
            features.append({
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [round(lon, 5), round(lat, 5)]},
                "properties": {
                    "name": clean(row["location"]),
                    "city": clean(row["city"]),
                    "story": clean(row["description"], 600),
                    "approx": approx,
                },
            })
    with open(dst, "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "features": features}, f, ensure_ascii=False)
    print(f"{len(features)} haunted places written to {dst}")


if __name__ == "__main__":
    main(*sys.argv[1:])
