#!/usr/bin/env python3
"""split_deck.py — prepare the per-presenter and full-deck slide PDFs.

The tutorial deck is 191 slides across four contiguous sections. This tool either
SPLITS a full-deck PDF into the per-presenter ranges, or MERGES the four section
PDFs into a single full-deck PDF — whichever the available source calls for.

Page ranges (1-based, inclusive) mirror content/meta.json → downloads:
    intro   1–11    (all presenters)
    yeow    12–55   (Spatial Perception — SELD)
    tan     56–79   (Contextual Understanding)
    gan     80–191  (Context-Aware Action & Intelligent Sound Management)

Slides are gated until after the session (see pretext.md), so this script writes
its output to a staging dir by default — NOT into site/downloads/. Move/rename the
approved PDFs into site/downloads/ and set their `status`/`file` in meta.json when
the presenters choose to release them.

Examples:
    # Split a full-deck export into the four section PDFs
    python build/split_deck.py split source_materials/full_deck.pdf --out build/_slides

    # Merge the four section PDFs (in slide order) into one full deck
    python build/split_deck.py merge --out build/_slides/full_deck.pdf \
        source_materials/Tutorial_Intro_1-to-11.pdf \
        source_materials/Tutorial_JW_12-to-55.pdf \
        source_materials/Tutorial_Joseph_56-to-79.pdf \
        source_materials/Tutorial_ProfGan_80-to-191.pdf

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
    "intro": (1, 11),
    "yeow": (12, 55),
    "tan": (56, 79),
    "gan": (80, 191),
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
