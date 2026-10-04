"""
Post the documents in missing_documents.json to the production library API.

- Country / document type / year IDs are looked up in prod by *value*
  (local and prod IDs differ, e.g. year 2025 is id 1 locally, id 16 in prod).
- Prod is re-checked right before posting, so documents that already exist
  (same title + country + type + year) are skipped. Safe to re-run.
- Entries with "skip": true are left out unless --include-skipped is given.
- Dry run by default. Add --commit to actually POST.

Usage:
    export LIBRARY_API_TOKEN=...         # the x-token prod expects
    python post_to_prod.py               # dry run: shows what would be posted
    python post_to_prod.py --commit      # post for real
    python post_to_prod.py --commit --only 20 11   # only these local_ids
"""
import argparse
import json
import mimetypes
import os
import sys
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
INPUT_JSON = HERE / "missing_documents.json"
RESULT_JSON = HERE / "post_results.json"


def get(base, endpoint):
    r = requests.get(f"{base}/library/{endpoint}/", timeout=120)
    r.raise_for_status()
    return r.json()


def doc_key(title, country, doc_type, year):
    return (title.strip(), country, doc_type, year)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prod", default="https://ocean-library.spc.int")
    ap.add_argument("--token", default=os.environ.get("LIBRARY_API_TOKEN"))
    ap.add_argument("--commit", action="store_true", help="actually POST (default is dry run)")
    ap.add_argument("--include-skipped", action="store_true", help="also post entries flagged skip")
    ap.add_argument("--only", type=int, nargs="+", metavar="LOCAL_ID", help="only post these local_ids")
    ap.add_argument("--input", type=Path, default=INPUT_JSON, help="documents JSON to post")
    ap.add_argument("--results", type=Path, default=RESULT_JSON, help="where to write post results")
    args = ap.parse_args()
    prod = args.prod.rstrip("/")

    if args.commit and not args.token:
        sys.exit("No token: set LIBRARY_API_TOKEN or pass --token")

    data = json.loads(args.input.read_text())
    docs = data["documents"]
    if args.only:
        docs = [d for d in docs if d["local_id"] in set(args.only)]
    if not args.include_skipped:
        docs = [d for d in docs if not d["skip"]]

    # Resolve prod lookup IDs by value
    countries = {c["value"]: c["id"] for c in get(prod, "countries")}
    doc_types = {t["value"]: t["id"] for t in get(prod, "document-types")}
    years = {y["value"]: y["id"] for y in get(prod, "years")}
    existing = {
        doc_key(d["title"], d["country"]["value"], d["document_type"]["value"], d["year"]["value"])
        for d in get(prod, "documents")
    }

    print(f"{'COMMIT' if args.commit else 'DRY RUN'} -> {prod}  ({len(docs)} candidate documents)\n")
    results = []
    counts = {"posted": 0, "exists": 0, "error": 0, "would_post": 0}

    for d in docs:
        label = f"[local {d['local_id']}] {d['year_value']} {d['country_value']} {d['title']}"
        res = {"local_id": d["local_id"], "title": d["title"]}

        if doc_key(d["title"], d["country_value"], d["document_type_value"], d["year_value"]) in existing:
            print(f"  EXISTS   {label}")
            res["status"] = "exists"
            counts["exists"] += 1
            results.append(res)
            continue

        problems = []
        country_id = countries.get(d["country_value"])
        doc_type_id = doc_types.get(d["document_type_value"])
        year_id = years.get(d["year_value"])
        if country_id is None:
            problems.append(f"country '{d['country_value']}' not in prod")
        if doc_type_id is None:
            problems.append(f"document type '{d['document_type_value']}' not in prod")
        if year_id is None:
            problems.append(f"year {d['year_value']} not in prod")
        image_path, pdf_path = HERE / d["image"], HERE / d["pdf"]
        for p in (image_path, pdf_path):
            if not p.exists():
                problems.append(f"missing file {p.name}")
        if problems:
            print(f"  ERROR    {label}: {'; '.join(problems)}")
            res.update(status="error", error="; ".join(problems))
            counts["error"] += 1
            results.append(res)
            continue

        form = {
            "title": d["title"],
            "country_id": country_id,
            "document_type_id": doc_type_id,
            "year_id": year_id,
        }
        if not args.commit:
            print(f"  WOULD    {label}  (country={country_id} type={doc_type_id} year={year_id})")
            counts["would_post"] += 1
            continue

        try:
            with open(image_path, "rb") as img, open(pdf_path, "rb") as pdf:
                files = {
                    "image": (image_path.name, img, mimetypes.guess_type(image_path.name)[0] or "image/png"),
                    "pdf": (pdf_path.name, pdf, "application/pdf"),
                }
                r = requests.post(f"{prod}/library/documents/", data=form, files=files,
                                  headers={"x-token": args.token}, timeout=300)
            if r.ok:
                new = r.json()
                print(f"  POSTED   {label}  -> prod id {new['id']}")
                res.update(status="posted", prod_id=new["id"], image=new["image"], pdf=new["pdf"])
                counts["posted"] += 1
                existing.add(doc_key(d["title"], d["country_value"], d["document_type_value"], d["year_value"]))
            else:
                print(f"  ERROR    {label}: HTTP {r.status_code} {r.text[:200]}")
                res.update(status="error", error=f"HTTP {r.status_code}: {r.text[:500]}")
                counts["error"] += 1
                if r.status_code == 401:
                    results.append(res)
                    print("\nToken rejected - stopping.")
                    break
        except requests.RequestException as e:
            print(f"  ERROR    {label}: {e}")
            res.update(status="error", error=str(e))
            counts["error"] += 1
        results.append(res)

    print("\n" + ", ".join(f"{k}={v}" for k, v in counts.items() if v or k != "would_post"))
    if args.commit:
        args.results.write_text(json.dumps(results, indent=2, ensure_ascii=False))
        print(f"Results written to {args.results.name}")
    else:
        print("Dry run only. Re-run with --commit to post.")
    sys.exit(1 if counts["error"] else 0)


if __name__ == "__main__":
    main()
