"""
Shrink PDFs and PNGs in assets/ and files/ in place.

PDFs: Ghostscript /ebook (images downsampled to 150 dpi, JPEG), CMYK -> RGB.
      Text and vector graphics are untouched.
PNGs: stripped and quantised to 256-colour PNG8 (thumbnails).

A file is only replaced when the result is at least MIN_SAVING smaller, so
already-optimised files are left alone.

Usage:
    python compress_assets.py              # dry run: report sizes, no changes
    python compress_assets.py --apply
    python compress_assets.py --apply assets/2023.Niue.pdf   # specific files
"""
import argparse
import os
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
DIRS = [HERE / "assets", HERE / "files"]
MIN_SAVING = 0.10

GS = ["gs", "-q", "-dNOPAUSE", "-dBATCH", "-dSAFER", "-sDEVICE=pdfwrite",
      "-dCompatibilityLevel=1.5", "-dPDFSETTINGS=/ebook",
      "-sColorConversionStrategy=RGB", "-dDetectDuplicateImages=true"]


def compress(src: Path, apply: bool):
    fd, tmp = tempfile.mkstemp(suffix=src.suffix, dir=src.parent)
    os.close(fd)
    try:
        if src.suffix.lower() == ".pdf":
            cmd = GS + [f"-sOutputFile={tmp}", str(src)]
        else:
            cmd = ["magick", str(src), "-strip", "-dither", "FloydSteinberg",
                   "-colors", "256", f"PNG8:{tmp}"]
        r = subprocess.run(cmd, capture_output=True, text=True)
        before, after = src.stat().st_size, os.path.getsize(tmp)
        if r.returncode != 0 or after == 0:
            return src, before, before, f"FAILED {r.stderr.strip()[:80]}"
        if after > before * (1 - MIN_SAVING):
            return src, before, before, "skipped (little gain)"
        if apply:
            os.replace(tmp, src)
        return src, before, after, "compressed" if apply else "would compress"
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("paths", nargs="*")
    args = ap.parse_args()

    if args.paths:
        files = [Path(p).resolve() for p in args.paths]
    else:
        files = sorted(p for d in DIRS for p in d.iterdir()
                       if p.suffix.lower() in (".pdf", ".png"))

    mb = lambda n: n / 1048576
    total_before = total_after = 0
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as pool:
        for src, before, after, status in pool.map(lambda f: compress(f, args.apply), files):
            total_before += before
            total_after += after
            print(f"{mb(before):8.1f}M -> {mb(after):7.1f}M  {status:<22} {src.relative_to(HERE)}")

    print(f"\nTotal: {mb(total_before):.0f}M -> {mb(total_after):.0f}M "
          f"({100 * (1 - total_after / max(total_before, 1)):.0f}% smaller)")
    if not args.apply:
        print("Dry run. Pass --apply to replace files.")


if __name__ == "__main__":
    main()
