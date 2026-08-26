#!/usr/bin/env python3
"""Copy the structured data from /content into the deployed tree at
site/assets/data/, so the site's JS loader can fetch it.

Why: the deploy is `site/` only, and files under site/ may reference only other
files under site/. `content/` is the editable source of truth; this script mirrors
it into `site/assets/data/`. Run it after any change to content/*.json, before deploy.

Usage:  python build/sync_content.py
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "content"
DST = ROOT / "site" / "assets" / "data"
FILES = ["meta.json", "people.json", "outline.json", "references.json"]

def main():
    DST.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        src = SRC / name
        if not src.exists():
            print(f"  ! missing {src} — skipped")
            continue
        shutil.copy2(src, DST / name)
        print(f"  synced {name}  ({src.stat().st_size:,} bytes)")
    print(f"Done → {DST}")

if __name__ == "__main__":
    main()
