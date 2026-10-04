"""
Compare the local library API against production and export every document
that exists locally but is missing in production.

Output (inside this folder):
    missing_documents.json   - one entry per missing document, ready for post_to_prod.py
    files/                   - the .png/.jpg image and .pdf for each missing document

Documents are matched by (title, country value, document type value, year value)
because database IDs differ between servers (e.g. year 2025 is id 1 locally, id 16 in prod).

Usage:
    python compare.py
    python compare.py --local http://localhost:8000 --prod https://ocean-library.spc.int
"""
import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
LOCAL_UPLOAD_DIR = HERE.parent / "app" / "uploads" / "documents"
FILES_DIR = HERE / "files"
OUTPUT_JSON = HERE / "missing_documents.json"

# Countries excluded entirely: Nauru was renamed "Naoero" in prod and its
# documents re-uploaded under different titles, so title matching doesn't apply.
SKIP_COUNTRIES = {"NRU"}


def fetch(base, endpoint):
    r = requests.get(f"{base.rstrip('/')}/library/{endpoint}/", timeout=120)
    r.raise_for_status()
    return r.json()


def doc_key(d):
    return (
        d["title"].strip(),
        d["country"]["value"],
        d["document_type"]["value"],
        d["year"]["value"],
    )


def get_file(local_base, media_url, dest):
    """Copy the file from local disk, or download it from the local server if not on disk."""
    filename = media_url.rsplit("/", 1)[-1]
    src = LOCAL_UPLOAD_DIR / filename
    if src.exists():
        shutil.copy2(src, dest)
        return "disk"
    r = requests.get(f"{local_base.rstrip('/')}{media_url}", timeout=120)
    r.raise_for_status()
    dest.write_bytes(r.content)
    return "http"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--local", default="http://localhost:8000")
    ap.add_argument("--prod", default="https://ocean-library.spc.int")
    args = ap.parse_args()

    print(f"Fetching local: {args.local}")
    local_docs = fetch(args.local, "documents")
    print(f"Fetching prod:  {args.prod}")
    prod_docs = fetch(args.prod, "documents")
    print(f"local={len(local_docs)} documents, prod={len(prod_docs)} documents")

    prod_keys = {doc_key(d) for d in prod_docs}
    missing = [d for d in local_docs
               if doc_key(d) not in prod_keys and d["country"]["value"] not in SKIP_COUNTRIES]
    missing.sort(key=lambda d: (d["year"]["value"], d["country"]["value"], d["title"]))

    if FILES_DIR.exists():
        shutil.rmtree(FILES_DIR)
    FILES_DIR.mkdir()

    entries = []
    errors = 0
    for d in missing:
        entry = {
            "local_id": d["id"],
            "title": d["title"],
            "country_value": d["country"]["value"],
            "country_name": d["country"]["name"],
            "document_type_value": d["document_type"]["value"],
            "year_value": d["year"]["value"],
            # local IDs for reference only - post_to_prod.py resolves prod IDs by value
            "local_country_id": d["country"]["id"],
            "local_document_type_id": d["document_type"]["id"],
            "local_year_id": d["year"]["id"],
            "image": f"files/{d['image'].rsplit('/', 1)[-1]}",
            "pdf": f"files/{d['pdf'].rsplit('/', 1)[-1]}",
            "skip": False,  # set true by hand to hold an entry back
        }

        for field in ("image", "pdf"):
            dest = HERE / entry[field]
            try:
                get_file(args.local, d[field], dest)
            except Exception as e:
                errors += 1
                entry.setdefault("file_errors", []).append(f"{field}: {e}")
                print(f"  !! could not get {field} for local id {d['id']}: {e}")
        entries.append(entry)

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "local_base": args.local,
        "prod_base": args.prod,
        "count": len(entries),
        "count_to_post": sum(1 for e in entries if not e["skip"]),
        "documents": entries,
    }
    OUTPUT_JSON.write_text(json.dumps(out, indent=2, ensure_ascii=False))

    print(f"\nMissing in prod: {len(entries)} (excluding countries {sorted(SKIP_COUNTRIES)})")
    for e in entries:
        print(f"  {e['year_value']}  {e['country_value']}  {e['document_type_value']:<12} {e['title']}")
    print(f"\nWrote {OUTPUT_JSON.name} and {len(list(FILES_DIR.iterdir()))} files in {FILES_DIR.name}/")
    if errors:
        print(f"{errors} file errors - see 'file_errors' in the JSON")
        sys.exit(1)


if __name__ == "__main__":
    main()
