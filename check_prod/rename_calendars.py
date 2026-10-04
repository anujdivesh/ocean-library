"""
Rename tide calendar PDFs in assets/ to YEAR.Country.Station.pdf.

Station/year come from each PDF's own header ("TIDAL PREDICTIONS FOR VANUATU -
PORT VILA / JANUARY 2018", "Fiji - Suva / 2021 Tide Predictions Calendar"; 2024
covers were OCR'd/eyeballed). References in assets/documents.csv and
assets/documents.json are updated, and old -> new is written to rename_map.csv.

Usage:
    python rename_calendars.py            # dry run
    python rename_calendars.py --apply
    python rename_calendars.py --undo     # reverse using rename_map.csv
"""
import argparse
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
MAP_FILE = HERE / "rename_map.csv"

# header station -> canonical file stem (without year)
IDO_2018 = {
    "IDO60041": "Papua.New.Guinea.Port.Moresby",
    "IDO60042": "Papua.New.Guinea.Lombrum",
    "IDO60043": "Solomon.Islands.Honiara",
    "IDO60044": "Vanuatu.Port.Vila",
    "IDO60045": "Cook.Islands.Rarotonga",
    "IDO60046": "Niue",
    "IDO60047": "Tonga.Nukualofa",
    "IDO60048": "Samoa.Apia",
    "IDO60049": "Fiji.Suva",
    "IDO60050": "Fiji.Lautoka",
    "IDO60051": "Tuvalu.Funafuti",
    "IDO60052": "Kiribati.Betio",
    "IDO60053": "Nauru",
    "IDO60054": "Marshall.Islands.Majuro",
    "IDO60055": "FSM.Pohnpei.Harbour",
    "IDO60056": "Palau.Islands.Malakal",
    "IDO60057": "Vanuatu.Luganville",
    "IDO60058": "Solomon.Islands.Lata.Wharf",
    "IDO60059": "Solomon.Islands.Tarekukure",
    "IDO60060": "Tonga.Neiafu",
}

# 2019/2020 "Work Plan" files: old prefix -> canonical stem
WORK_PLAN = {
    "Cook.Islands.Rarotonga": "Cook.Islands.Rarotonga",
    "Fiji.Lautoka": "Fiji.Lautoka",
    "Fiji.Suva": "Fiji.Suva",
    "Kiribati.Betio": "Kiribati.Betio",
    "Kiribati.Kanton": "Kiribati.Kanton",
    "Kiritimati": "Kiribati.Kiritimati",
    "Marshall.Islands.Majuro": "Marshall.Islands.Majuro",
    "Nauru": "Nauru",
    "Niue": "Niue",
    "Palau": "Palau.Islands.Malakal",
    "Papua.New.Guinea.Lombrum": "Papua.New.Guinea.Lombrum",
    "Papua.New.Guinea.Port.Moresby": "Papua.New.Guinea.Port.Moresby",
    "Samoa.Apia": "Samoa.Apia",
    "Solomon.Islands.Honiara": "Solomon.Islands.Honiara",
    "Solomon.Islands.Lata.Wharf": "Solomon.Islands.Lata.Wharf",
    "Solomon.Islands.Tarekukure.Wharf": "Solomon.Islands.Tarekukure",
    "Tonga.Neiafu": "Tonga.Neiafu",
    "Tonga.Nukualofa": "Tonga.Nukualofa",
    "Tuvalu.Funafuti": "Tuvalu.Funafuti",
    "Tuvalu.Vaitupu": "Tuvalu.Vaitupu",
    "Vanuatu.Luganville.Wharf": "Vanuatu.Luganville",
    "Vanuatu.Port.Vila": "Vanuatu.Port.Vila",
}

# 2021-2024 files already start with the year; fix the station part only
YEAR_FIRST = {
    "Lautoka.Calendar": "Fiji.Lautoka",
    "Suva.Calendar": "Fiji.Suva",
    "Marshall.Island.Majuro": "Marshall.Islands.Majuro",
    "Marshall.Island.Ebeye": "Marshall.Islands.Ebeye",
    "Marshall Island.Majuro": "Marshall.Islands.Majuro",
    "Marshall Island.Ebeye": "Marshall.Islands.Ebeye",
    "Marshal.Islands.Majuro": "Marshall.Islands.Majuro",
    "Pohnpei.Harbour": "FSM.Pohnpei.Harbour",
    "Solomon.Islands.Terekukure.Wharf": "Solomon.Islands.Tarekukure",
    "Solomon.Islands.Tarekukure.Wharf": "Solomon.Islands.Tarekukure",
    "Tonga.Nuku'alofa": "Tonga.Nukualofa",
    "Tuvalu.Vaitupo": "Tuvalu.Vaitupu",
    "Vanuatu.Luganville.Wharf": "Vanuatu.Luganville",
    "PNG.Lombrum": "Papua.New.Guinea.Lombrum",
    "PNG.Port.Moresby": "Papua.New.Guinea.Port.Moresby",
}


def new_name(name):
    stem = name[:-4]
    if stem.startswith("IDO") and stem[:8] in IDO_2018:
        return f"2018.{IDO_2018[stem[:8]]}.pdf"
    if stem == "Tonga.Neiafu.2019.Tide.Calendar.Work.Plan.print.version":
        return "2019.Tonga.Neiafu.print.pdf"
    for suffix in (".Tide.Calendar.Work.Plan", ""):
        for year in ("2019", "2020"):
            tail = f".{year}{suffix}"
            if stem.endswith(tail) and stem[: -len(tail)] in WORK_PLAN:
                return f"{year}.{WORK_PLAN[stem[:-len(tail)]]}.pdf"
    if stem.startswith("Pohnpei.Harbour.FSM."):
        return f"{stem[-4:]}.FSM.Pohnpei.Harbour.pdf"
    if stem[:4].isdigit() and stem[4] == ".":
        year, rest = stem[:4], stem[5:]
        return f"{year}.{YEAR_FIRST.get(rest, rest)}.pdf"
    return name  # factsheets etc. left alone


def update_refs(mapping):
    csv_path = ASSETS / "documents.csv"
    with open(csv_path, newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["file"] = mapping.get(r["file"], r["file"])
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["title", "file", "category"])
        w.writeheader()
        w.writerows(rows)

    json_path = ASSETS / "documents.json"
    docs = json.loads(json_path.read_text())
    for d in docs:
        d["file"] = mapping.get(d["file"], d["file"])
    json_path.write_text(json.dumps(docs, indent=1, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--undo", action="store_true")
    args = ap.parse_args()

    if args.undo:
        with open(MAP_FILE, newline="") as f:
            mapping = {new: old for old, new in csv.reader(f)}
    else:
        mapping = {p.name: new_name(p.name) for p in sorted(ASSETS.glob("*.pdf"))}
        mapping = {o: n for o, n in mapping.items() if o != n}

    targets = list(mapping.values())
    dupes = {t for t in targets if targets.count(t) > 1}
    clash = {t for t in targets if (ASSETS / t).exists() and t not in mapping}
    for old, new in mapping.items():
        flag = "  <-- DUPLICATE" if new in dupes else "  <-- EXISTS" if new in clash else ""
        print(f"{old:<70} -> {new}{flag}")
    print(f"\n{len(mapping)} renames")
    if dupes or clash:
        raise SystemExit("Refusing: target name collisions")
    if not (args.apply or args.undo):
        print("Dry run. Pass --apply to rename.")
        return

    for old, new in mapping.items():
        (ASSETS / old).rename(ASSETS / new)
    update_refs(mapping)
    if args.undo:
        MAP_FILE.unlink()
    else:
        with open(MAP_FILE, "w", newline="") as f:
            csv.writer(f).writerows(mapping.items())
    print("Done.")


if __name__ == "__main__":
    main()
