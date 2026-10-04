"""
Build a batch JSON (same shape as missing_documents.json) for the tide
calendars in assets/<year>/, ready for `python post_to_prod.py --input <file>`.

- Titles follow the 2025 prod titles for each station (typos fixed).
- Anything whose (country, station, year) is already in prod is skipped.

Usage:
    python build_batch.py                                   # 2019 2022 2023 2026 -> batch_documents.json
    python build_batch.py --years 2018 --out batch_2018.json
"""
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
OUT = HERE / "batch_documents.json"
PROD = "https://ocean-library.spc.int"
YEARS = [2019, 2022, 2023, 2026]

# station key -> (country, title)
STATIONS = {
    "pago pago": ("ASM", "American Samoa - Pago Pago"),
    "penrhyn": ("COK", "COK - Penrhyn"),
    "rarotonga": ("COK", "COK - Rarotonga"),
    "lautoka": ("FJI", "Fiji - Lautoka"),
    "port denarau": ("FJI", "Fiji - Port Denarau"),
    "suva": ("FJI", "Fiji - Suva"),
    "vatia": ("FJI", "Fiji - Vatia"),
    "pohnpei": ("FSM", "FSM - Pohnpei"),
    "betio": ("KIR", "Kiribati - Betio"),
    "kanton": ("KIR", "Kiribati - Kanton"),
    "kiritimati": ("KIR", "Kiribati - Kiritimati"),
    "ebeye": ("MHL", "MHL - Ebeye"),
    "majuro": ("MHL", "MHL - Majuro"),
    "nauru": ("NRU", "Nauru"),
    "niue": ("NIU", "Niue"),
    "malakal": ("PLW", "Palau - Malakal"),
    "lombrum": ("PNG", "PNG - Lombrum"),
    "port moresby": ("PNG", "PNG - Port Moresby"),
    "apia": ("WSM", "Samoa - Apia"),
    "honiara": ("SLB", "SLB - Honiara"),
    "lata wharf": ("SLB", "SLB - Lata Wharf"),
    "tarekukure": ("SLB", "SLB - Tarekukure"),
    "atafu": ("TKL", "Tokelau - Atafu"),
    "fakaofo": ("TKL", "Tokelau - Fakaofo"),
    "nukunonu": ("TKL", "Tokelau - Nukunonu"),
    "neiafu": ("TON", "Tonga - Neiafu"),
    "nukualofa": ("TON", "Tonga - Nuku'alofa"),
    "funafuti": ("TUV", "Tuvalu - Funafuti"),
    "nanumaga": ("TUV", "Tuvalu - Nanumaga"),
    "nanumea": ("TUV", "Tuvalu - Nanumea"),
    "niulakita": ("TUV", "Tuvalu - Niulakita"),
    "niutao": ("TUV", "Tuvalu - Niutao"),
    "nui": ("TUV", "Tuvalu - Nui"),
    "nukufetau": ("TUV", "Tuvalu - Nukufetau"),
    "nukulaelae": ("TUV", "Tuvalu - Nukulaelae"),
    "vaitupu": ("TUV", "Tuvalu - Vaitupu"),
    "lenakel": ("VUT", "Vanuatu - Lenakel"),
    "luganville": ("VUT", "Vanuatu - Luganville"),
    "malekula": ("VUT", "Vanuatu - Malekula"),
    "port vila": ("VUT", "Vanuatu - Port Vila"),
}
# prod title fragments -> station key, for spotting what prod already has
PROD_ALIASES = {"port villa": "port vila", "luganville wharf": "luganville",
                "tarekukure wharf": "tarekukure", "lata whart": "lata wharf",
                "pohnpei harbour": "pohnpei", "nuku'alofa": "nukualofa", "palau": "malakal",
                "vaitupo": "vaitupu"}
SINGLE_STATION = {"NRU": "nauru", "NIU": "niue", "ASM": "pago pago"}


def station_from_file(stem):
    """'2019.Solomon.Islands.Lata.Wharf' / '2026_tide_..._fiji_-_port_denarau' -> station key."""
    s = stem.lower().replace("_", " ").replace(".", " ").replace("-", " ")
    s = re.sub(r"\s+", " ", s).replace("pagopago", "pago pago")
    # longest key first so "port moresby" beats "port", "lata wharf" beats "lata"
    for key in sorted(STATIONS, key=len, reverse=True):
        if re.search(rf"\b{key}\b", s):
            return key
    if "palau" in s:
        return "malakal"
    if re.search(r"\blata\b", s):
        return "lata wharf"
    return None


def prod_station(doc):
    country = doc["country"]["value"]
    if country in SINGLE_STATION:
        return SINGLE_STATION[country]
    name = re.sub(r"\b(19|20)\d{2}\b", "", doc["title"].split(" - ")[-1]).strip(" -").lower()
    return PROD_ALIASES.get(name, name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", type=int, nargs="+", default=YEARS)
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()

    docs = requests.get(f"{PROD}/library/documents/", timeout=120).json()
    in_prod = {(d["country"]["value"], prod_station(d), d["year"]["value"])
               for d in docs if d["document_type"]["value"] == "tidecalendar"}

    out, skipped = [], []
    for pdf in sorted(p for y in args.years for p in (ASSETS / str(y)).glob("*.pdf")):
        year = int(pdf.name[:4])
        if ".print" in pdf.name:
            skipped.append((pdf.name, "print duplicate"))
            continue
        png = pdf.with_suffix(".png")
        key = station_from_file(pdf.stem)
        if key is None:
            skipped.append((pdf.name, "unknown station"))
            continue
        country, title = STATIONS[key]
        if (country, key, year) in in_prod:
            skipped.append((pdf.name, "already in prod"))
            continue
        if not png.exists():
            skipped.append((pdf.name, "no thumbnail"))
            continue
        out.append({
            "local_id": len(out) + 1,
            "title": title,
            "country_value": country,
            "document_type_value": "tidecalendar",
            "year_value": year,
            "image": str(png.relative_to(HERE)),
            "pdf": str(pdf.relative_to(HERE)),
            "skip": False,
        })

    seen = {}
    for d in out:
        k = (d["country_value"], d["title"], d["year_value"])
        if k in seen:
            raise SystemExit(f"Duplicate {k}: {seen[k]} and {d['pdf']}")
        seen[k] = d["pdf"]

    args.out.write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "prod_base": PROD,
        "count": len(out),
        "documents": out,
    }, indent=2, ensure_ascii=False))

    for y in sorted(args.years):
        rows = [d for d in out if d["year_value"] == y]
        print(f"{y}: {len(rows)}")
        for d in rows:
            print(f"   {d['country_value']}  {d['title']:<28} {Path(d['pdf']).name}")
    print("\nSkipped:")
    for name, why in skipped:
        print(f"   {why:<18} {name}")
    print(f"\nWrote {args.out.name} ({len(out)} documents)")


if __name__ == "__main__":
    main()
