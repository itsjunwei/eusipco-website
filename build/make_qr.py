#!/usr/bin/env python3
"""make_qr.py — generate a high-error-correction QR code for the tutorial site.

Produces an SVG (crisp at any size, for the closing slide and the site) and a PNG
(handy for quick checks). Error correction is level H (~30%), so the code still
scans with a logo overlaid or in a low-quality projection.

Usage:
    python build/make_qr.py https://USERNAME.github.io/REPO/
    python build/make_qr.py https://USERNAME.github.io/REPO/ --out site/assets/img/qr

Writes <out>.svg and <out>.png (default out: site/assets/img/qr). Colors follow the
site palette (navy on transparent). Also updates content/meta.json → contact.qr with
the SVG path if that file is present, so the site shows the code automatically after
you re-run build/sync_content.py.

Requires segno (`pip install segno`).
"""
import argparse
import json
import sys
from pathlib import Path

try:
    import segno
except ImportError:
    sys.exit("segno is required:  pip install segno")

ROOT = Path(__file__).resolve().parent.parent
NAVY = "#17364F"


def main():
    ap = argparse.ArgumentParser(description="Generate the tutorial site QR code.")
    ap.add_argument("url", help="the full site URL to encode, e.g. https://user.github.io/repo/")
    ap.add_argument("--out", type=Path, default=ROOT / "site" / "assets" / "img" / "qr",
                    help="output path stem (no extension); .svg and .png are written")
    ap.add_argument("--dark", default=NAVY, help="module color (default site navy)")
    args = ap.parse_args()

    out = args.out
    out.parent.mkdir(parents=True, exist_ok=True)

    qr = segno.make(args.url, error="h")   # level H = ~30% error correction
    svg_path = out.with_suffix(".svg")
    png_path = out.with_suffix(".png")
    # SVG: transparent background so it sits on any slide/section color.
    qr.save(str(svg_path), kind="svg", scale=10, border=2, dark=args.dark, light=None)
    # PNG: white background for reliable scanning in previews.
    qr.save(str(png_path), kind="png", scale=10, border=2, dark=args.dark, light="#ffffff")

    print(f"Encoded: {args.url}")
    print(f"  wrote {svg_path.relative_to(ROOT)}  (version {qr.version}, ECC {qr.error.upper()})")
    print(f"  wrote {png_path.relative_to(ROOT)}")

    # Wire the SVG into meta.json so the site renders it (path relative to site/).
    meta_path = ROOT / "content" / "meta.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        rel = str(svg_path.relative_to(ROOT / "site")).replace("\\", "/")
        meta.setdefault("contact", {})["qr"] = rel
        meta["contact"]["url"] = args.url
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  updated content/meta.json → contact.qr = {rel}")
        print("  next: python build/sync_content.py  (then redeploy)")


if __name__ == "__main__":
    main()
