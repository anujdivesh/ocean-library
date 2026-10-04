"""
Tide calendar coverage table: station x year, local vs production.

Cell legend:
    ✓   in both
    L   local only  -> MISSING IN PROD
    P   prod only
    .   in neither

Titles differ between uploads ("Fiji - Suva", "Tide Calendar - Suva 2020",
"Fiji - Suva 2021"), so each title is normalised to a station name first.

Usage:
    python tide_calendar_table.py            # prints table, writes tide_calendar_table.csv
"""
import argparse
import csv
import re
from collections import defaultdict
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent

# normalised title fragment -> canonical station name
ALIASES = {
    "port villa": "Port Vila",
    "vaitupo": "Vaitupu",
    "nukualofa": "Nuku'alofa",
    "luganville wharf": "Luganville",
    "tarekukure wharf": "Tarekukure",
    "pohnpei harbour": "Pohnpei",
    "palau": "Malakal",
    "lata whart": "Lata Wharf",
}
# countries with a single station: use the country name regardless of title
SINGLE_STATION = {"NRU": "Nauru", "NIU": "Niue", "ASM": "Pago Pago"}


def station(doc):
    country = doc["country"]["value"]
    if country in SINGLE_STATION:
        return SINGLE_STATION[country]
    name = doc["title"].split(" - ")[-1]
    name = re.sub(r"\b(19|20)\d{2}\b", "", name).strip(" -")
    return ALIASES.get(name.lower(), name)


def fetch(base):
    r = requests.get(f"{base.rstrip('/')}/library/documents/", timeout=120)
    r.raise_for_status()
    out = defaultdict(list)
    for d in r.json():
        if d["document_type"]["value"] == "tidecalendar":
            out[(d["country"]["value"], station(d), d["year"]["value"])].append(d)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--local", default="http://localhost:8000")
    ap.add_argument("--prod", default="https://ocean-library.spc.int")
    args = ap.parse_args()

    local, prod = fetch(args.local), fetch(args.prod)
    keys = set(local) | set(prod)
    years = sorted({k[2] for k in keys})
    stations = sorted({(k[0], k[1]) for k in keys})

    def cell(k):
        return {(True, True): "✓", (True, False): "L", (False, True): "P"}.get(
            (k in local, k in prod), ".")

    rows = [[c, s] + [cell((c, s, y)) for y in years] for c, s in stations]

    header = ["Country", "Station"] + [str(y) for y in years]
    widths = [max(len(str(r[i])) for r in rows + [header]) for i in range(len(header))]
    line = lambda r: "  ".join(str(v).ljust(w) for v, w in zip(r, widths))
    print(line(header))
    print("  ".join("-" * w for w in widths))
    for r in rows:
        print(line(r))
    print("\n✓ both   L local only (MISSING IN PROD)   P prod only   . neither")

    missing = sorted(k for k in local if k not in prod)
    print(f"\nMissing in prod: {len(missing)}")
    for c, s, y in missing:
        print(f"  {y}  {c}  {s:<14} local id {local[(c, s, y)][0]['id']}  '{local[(c, s, y)][0]['title']}'")

    with open(HERE / "tide_calendar_table.csv", "w", newline="") as f:
        csv.writer(f).writerows([header] + rows)
    print("\nWrote tide_calendar_table.csv")


if __name__ == "__main__":
    main()
