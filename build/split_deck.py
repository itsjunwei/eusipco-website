#!/usr/bin/env python3
"""split_deck.py — prepare the per-presenter and full-deck slide PDFs.

The tutorial deck is 189 slides across four contiguous presenter ranges. This
tool either splits a full-deck PDF into those ranges or merges approved section
PDFs into one deck.

Page ranges (1-based, inclusive) mirror content/meta.json → downloads:
    intro   1–10    (all presenters)
    yeow    11–54   (Spatial Perception — SELD)
    tan     55–81   (Contextual Understanding)
    gan     82–189  (remaining tutorial sections)

Output is written to a staging directory by default. Public download availability
is controlled by content/meta.json.

Examples:
    # Split a full-deck export into the four section PDFs
    python build/split_deck.py split \
        site/downloads/EUSIPCO2026_Tutorial2_Environmental_Acoustic_Intelligence.pdf \
        --out build/_slides

Requires pikepdf (`pip install pikepdf`).
"""
import argparse
import sys
from pathlib import Path

try:
    import pikepdf
except ImportError:
    sys.exit("pikepdf is required:  pip install pikepdf")

# id -> (first_page, last_page) inclusive, 1-based
RANGES = {
    "intro": (1, 10),
    "yeow": (11, 54),
    "tan": (55, 81),
    "gan": (82, 189),
}


def split(full_pdf: Path, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    src = pikepdf.open(full_pdf)
    n = len(src.pages)
    print(f"Opened {full_pdf.name}: {n} pages")
    expected_last = max(hi for _, hi in RANGES.values())
    if n != expected_last:
        print(f"  ! warning: expected {expected_last} pages, found {n} — check RANGES")
    for name, (lo, hi) in RANGES.items():
        if lo > n:
            print(f"  ! skip {name}: range {lo}-{hi} beyond document")
            continue
        dst = pikepdf.Pdf.new()
        for i in range(lo - 1, min(hi, n)):
            dst.pages.append(src.pages[i])
        out = out_dir / f"tutorial_{name}.pdf"
        dst.save(out)
        print(f"  wrote {out.name}: pages {lo}-{min(hi, n)} ({len(dst.pages)} pp)")
    src.close()


def merge(out_pdf: Path, inputs):
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    dst = pikepdf.Pdf.new()
    total = 0
    for p in inputs:
        src = pikepdf.open(p)
        dst.pages.extend(src.pages)
        total += len(src.pages)
        print(f"  + {Path(p).name}: {len(src.pages)} pp")
        src.close()
    dst.save(out_pdf)
    print(f"Wrote {out_pdf} — {total} pages total")


def main():
    ap = argparse.ArgumentParser(description="Split or merge the tutorial slide deck PDFs.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("split", help="split a full-deck PDF into per-presenter PDFs")
    sp.add_argument("full_pdf", type=Path)
    sp.add_argument("--out", type=Path, default=Path("build/_slides"))

    mg = sub.add_parser("merge", help="merge section PDFs (in order) into one full deck")
    mg.add_argument("--out", type=Path, required=True)
    mg.add_argument("inputs", nargs="+", type=Path)

    args = ap.parse_args()
    if args.cmd == "split":
        split(args.full_pdf, args.out)
    elif args.cmd == "merge":
        merge(args.out, args.inputs)


if __name__ == "__main__":
    main()
