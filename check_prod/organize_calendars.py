"""
Gather all tide calendars into assets/ as YEAR.Country.Station.pdf/.png.

- 2025: copied from files/ (hash names) using missing_documents.json.
- 2026: the "2026_tide_predictions_calendar_..." files are renamed in place.
Every move/copy is appended to rename_map.csv (old,new).

Usage:
    python organize_calendars.py            # dry run
    python organize_calendars.py --apply
"""
import argparse
import csv
import json
import shutil
from pathlib import Path

from build_batch import STATIONS, station_from_file

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
MAP_FILE = HERE / "rename_map.csv"

# station key -> file stem (without year), matching the existing assets/ names
STEM = {
    "pago pago": "American.Samoa.Pago.Pago",
    "penrhyn": "Cook.Islands.Penrhyn",
    "rarotonga": "Cook.Islands.Rarotonga",
    "lautoka": "Fiji.Lautoka",
    "port denarau": "Fiji.Port.Denarau",
    "suva": "Fiji.Suva",
    "vatia": "Fiji.Vatia",
    "pohnpei": "FSM.Pohnpei.Harbour",
    "betio": "Kiribati.Betio",
    "kanton": "Kiribati.Kanton",
    "kiritimati": "Kiribati.Kiritimati",
    "ebeye": "Marshall.Islands.Ebeye",
    "majuro": "Marshall.Islands.Majuro",
    "nauru": "Nauru",
    "niue": "Niue",
    "malakal": "Palau.Islands.Malakal",
    "lombrum": "Papua.New.Guinea.Lombrum",
    "port moresby": "Papua.New.Guinea.Port.Moresby",
    "apia": "Samoa.Apia",
    "honiara": "Solomon.Islands.Honiara",
    "lata wharf": "Solomon.Islands.Lata.Wharf",
    "tarekukure": "Solomon.Islands.Tarekukure",
    "atafu": "Tokelau.Atafu",
    "fakaofo": "Tokelau.Fakaofo",
    "nukunonu": "Tokelau.Nukunonu",
    "neiafu": "Tonga.Neiafu",
    "nukualofa": "Tonga.Nukualofa",
    "funafuti": "Tuvalu.Funafuti",
    "nanumaga": "Tuvalu.Nanumaga",
    "nanumea": "Tuvalu.Nanumea",
    "niulakita": "Tuvalu.Niulakita",
    "niutao": "Tuvalu.Niutao",
    "nui": "Tuvalu.Nui",
    "nukufetau": "Tuvalu.Nukufetau",
    "nukulaelae": "Tuvalu.Nukulaelae",
    "vaitupu": "Tuvalu.Vaitupu",
    "lenakel": "Vanuatu.Lenakel",
    "luganville": "Vanuatu.Luganville",
    "malekula": "Vanuatu.Malekula",
    "port vila": "Vanuatu.Port.Vila",
}
assert set(STEM) == set(STATIONS)
TITLE_TO_KEY = {title: key for key, (_, title) in STATIONS.items()}
TITLE_TO_KEY.update({"Niue - Niue": "niue", "Vanuatu - Port Villa": "port vila"})


def plan():
    ops = []  # (action, src, dst)
    for d in json.loads((HERE / "missing_documents.json").read_text())["documents"]:
        stem = f"{d['year_value']}.{STEM[TITLE_TO_KEY[d['title']]]}"
        ops.append(("copy", HERE / d["pdf"], ASSETS / f"{stem}.pdf"))
        ops.append(("copy", HERE / d["image"], ASSETS / f"{stem}.png"))
    for p in sorted(ASSETS.glob("2026_*")):
        key = station_from_file(p.stem)
        if key is None:
            raise SystemExit(f"Cannot identify station for {p.name}")
        ops.append(("move", p, ASSETS / f"2026.{STEM[key]}{p.suffix.lower()}"))
    return ops


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    ops = plan()
    dsts = [dst for _, _, dst in ops]
    dupes = {d for d in dsts if dsts.count(d) > 1}
    exists = {d for d in dsts if d.exists()}
    for action, src, dst in ops:
        flag = "  <-- DUPLICATE" if dst in dupes else "  <-- EXISTS" if dst in exists else ""
        print(f"{action}  {str(src.relative_to(HERE)):<75} -> {dst.name}{flag}")
    print(f"\n{sum(a == 'copy' for a, _, _ in ops)} copies, {sum(a == 'move' for a, _, _ in ops)} renames")
    if dupes or exists:
        raise SystemExit("Refusing: target name collisions")
    if not args.apply:
        print("Dry run. Pass --apply to copy/rename.")
        return

    with open(MAP_FILE, "a", newline="") as f:
        w = csv.writer(f)
        for action, src, dst in ops:
            if action == "copy":
                shutil.copy2(src, dst)
            else:
                src.rename(dst)
            w.writerow([str(src.relative_to(HERE)) if action == "copy" else src.name, dst.name])
    print("Done.")


if __name__ == "__main__":
    main()
