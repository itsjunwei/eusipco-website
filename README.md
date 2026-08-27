# Environmental Acoustic Intelligence — EUSIPCO 2026 Tutorial site

Companion website for the EUSIPCO 2026 tutorial **"Environmental Acoustic Intelligence:
From Acoustic Perception towards Context-Aware Sound Intervention"** (Tutorial #2, 31 Aug 2026)
by Prof. Woon-Seng Gan, Dr. Ee-Leng Tan, and Mr. Jun-Wei Yeow (NTU Singapore).

Static, single-page, mobile-first. Plain HTML/CSS/JS — no framework, no build step.
Deployed to GitHub Pages from `site/` via GitHub Actions.

## Repository layout

```
content/            Source-of-truth JSON (meta, people, outline, references). EDIT HERE.
site/               The deployed site (this folder is what GitHub Pages serves).
  index.html          Data-driven shell.
  assets/css/         styles.css (design system).
  assets/js/          app.js (loads assets/data/*.json and renders).
  assets/data/        Deployed copy of content/*.json (produced by sync_content.py).
  assets/img/         qr.svg (generated), favicons, etc.
  downloads/          Public slide PDFs.
build/              Utility scripts (not deployed).
  sync_content.py     content/*.json  →  site/assets/data/*.json
  build_references.py Rebuilds content/references.json from the reference lists.
  split_deck.py       Merge/split the slide PDFs into per-presenter files.
  make_qr.py          Generate the site QR code.
docs/               CONTENT_INVENTORY.md, PROGRESS.md, DEPLOY.md.
source_materials/   PRIVATE inputs (deck, PDFs, scripts). Git-ignored, never deployed.
```

## Edit content

1. Edit the JSON in `content/` (or, for references, edit `build/build_references.py`
   and run `python build/build_references.py`).
2. Sync it into the deployed tree: `python build/sync_content.py`.
3. Commit and push — the site redeploys automatically.

## Preview locally

The page loads its data with `fetch()`, which needs HTTP (it will **not** work by
double-clicking `index.html`). Serve the folder:

```bash
cd site
python -m http.server 8000
# open http://localhost:8000
```

## Deploy

See **[docs/DEPLOY.md](docs/DEPLOY.md)** for the deployment and maintenance guide.

## Requirements for the build scripts

Python 3, plus: `pikepdf` (split_deck), `segno` (make_qr).
`pip install pikepdf segno`
