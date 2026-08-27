# Deploy guide — EUSIPCO 2026 Tutorial site

A start-to-finish walkthrough to publish this site on **GitHub Pages**. Everything that
does not need your GitHub account is already set up (the site, the Actions deploy workflow,
and the QR generator). This guide covers the parts only you can do.

Estimated time: ~15 minutes. Commands are shown for **Windows PowerShell** (your machine),
with notes where they differ elsewhere.

---

## 0. Before you start — two decisions

**A. Which account?** The brief recommends a **lab / organisation** account so the site
outlives any one person. If your lab GitHub org already exists, use it. If not, either
create one (GitHub → your avatar → *Your organizations* → *New organization*, the Free
plan is fine) or start under your **personal** account and transfer the repo to the org
later (*Settings → Danger Zone → Transfer ownership*). Pages works the same either way.

**B. Repo name.** This becomes part of the URL. Suggested: **`eusipco2026-tutorial`**.
Your site will then live at:

```
https://<OWNER>.github.io/<REPO>/
e.g.  https://your-lab.github.io/eusipco2026-tutorial/
```

> Note the trailing slash — it matters for the QR and for sharing.

Prerequisites: **Git** installed (`git --version`; if missing, https://git-scm.com/download/win).
A GitHub account you can push to. That's it — no Node, no build tools.

---

## 1. Create an empty repository on GitHub

1. GitHub → **New repository**.
2. **Owner:** your org (or personal). **Name:** `eusipco2026-tutorial` (or your choice).
3. Visibility: **Public** (required for free GitHub Pages).
4. **Do not** add a README, .gitignore, or license — the project already has them.
5. Click **Create repository**. Leave that page open; you'll need the URL it shows.

---

## 1b. Add the deploy workflow file (one file you create by hand)

Everything else is already in the project, but the GitHub Actions **workflow file could not
be placed automatically** — GitHub deliberately restricts writing files under
`.github/workflows/` through automated tools. Create it yourself (30 seconds):

1. In `F:\Claude-EUSIPCO-Website`, create the folders `.github\workflows\`.
2. Inside, create a file named **`deploy.yml`** with exactly this content:

```yaml
name: Deploy site to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Configure Pages
        uses: actions/configure-pages@v5
      - name: Upload site/ as the Pages artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./site
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

> The same `deploy.yml` was delivered to you as a file in the chat — you can save that copy
> to `.github\workflows\` instead of retyping. If Git later refuses to push it, your token
> needs the **`workflow`** scope (regenerate the PAT with that box checked), or add the file
> via GitHub's web UI: **Actions → set up a workflow yourself → paste → commit**.

---

## 2. Push the project

Open PowerShell in the project folder and run these once. Replace `<OWNER>` and `<REPO>`.

```powershell
cd F:\Claude-EUSIPCO-Website

git init
git branch -M main
git add .
git commit -m "EUSIPCO 2026 tutorial site"
git remote add origin https://github.com/<OWNER>/<REPO>.git
git push -u origin main
```

**What gets pushed:** the site, content, build scripts, and docs. The big private inputs
in `source_materials/` are excluded by `.gitignore` (so the 327 MB PPTX is **not** uploaded).
If Git ever asks you to sign in, use your GitHub username and a **Personal Access Token**
as the password (GitHub → *Settings → Developer settings → Personal access tokens*), or
install **GitHub Desktop** and push from there.

---

## 3. Turn on GitHub Pages (GitHub Actions)

1. In the repo: **Settings → Pages**.
2. Under **Build and deployment → Source**, choose **GitHub Actions**.
   (Do **not** pick "Deploy from a branch" — this project deploys the `site/` subfolder
   via the included workflow, which branch-mode can't do.)
3. That's all to configure. The workflow at `.github/workflows/deploy.yml` runs on every
   push to `main`.

Watch it run under the **Actions** tab. When the *Deploy site to GitHub Pages* job finishes
(green tick, ~1 min), the job summary and **Settings → Pages** both show your live URL.

Open the URL. You should see the full site — hero, abstract, presenters, the outline, the
released tutorial-deck download, and all 103 references.

---

## 4. Generate the QR code (needs the live URL)

Now that you know the real URL, generate the QR that goes on the closing slide and the
contact card. From the project folder:

```powershell
python -m pip install segno            # once, if not already installed
python build\make_qr.py https://<OWNER>.github.io/<REPO>/
python build\sync_content.py
```

This writes `site/assets/img/qr.svg` (+ a `.png`), points `content/meta.json` at it, and
syncs it into `site/`. Commit and push to publish it:

```powershell
git add site/assets/img/qr.svg site/assets/img/qr.png content/meta.json site/assets/data/meta.json
git commit -m "Add site QR code"
git push
```

After the redeploy, the contact card shows the QR, and `site/assets/img/qr.svg` is the file
to drop onto your closing slide. Scan it with a phone to confirm it opens the site.

> Prefer me to generate it for you? Send me the final URL and I'll produce `qr.svg`/`qr.png`
> ready to commit.

---

## 5. Update the released slides

The approved 186-slide full deck is published under `site/downloads/`. To replace it with
a newer approved export, keep the existing filename and verify the page count before syncing:

1. **Replace the approved PDF** in `site/downloads/`.
2. **Verify `content/meta.json`** still describes the downloadable file truthfully.
3. **Sync and publish:**
   ```powershell
   python build\sync_content.py
   git add site/downloads content/meta.json site/assets/data/meta.json
   git commit -m "Update tutorial slides"
   git push
   ```
   The download card continues to use structured metadata as its source of truth.

> GitHub caps individual files at 100 MB. The full deck is well under that; if any single
> PDF is larger, compress it (e.g. Ghostscript) before committing.

---

## 6. Optional — a custom domain

If the lab has a domain, add it under **Settings → Pages → Custom domain**, create the DNS
records GitHub shows, and add a `site/CNAME` file containing the domain. Regenerate the QR
(step 4) with the new URL afterward.

---

## Troubleshooting

- **Actions tab shows a red X.** Open the run for the error. Most often Pages source wasn't
  set to "GitHub Actions" (step 3) — set it and re-run the job.
- **Site is blank / sections say "could not be loaded."** The data files didn't deploy.
  Confirm `site/assets/data/*.json` exist in the repo; if not, run `python build\sync_content.py`,
  commit, and push.
- **404 at the URL.** Give it 1–2 minutes after the first successful deploy; confirm the repo
  is **public**; check the exact URL (including trailing slash) in Settings → Pages.
- **Fonts look slightly different locally.** The site pulls Carlito from Google Fonts online;
  offline it falls back to Calibri (identical on Windows). No action needed.
- **Changed content but the site didn't update.** Did you run `sync_content.py` and push?
  The site serves `site/assets/data/`, not `content/`.

---

## Quick reference

| Task | Command |
|---|---|
| Preview locally | `cd site` then `python -m http.server 8000` |
| Rebuild references | `python build\build_references.py` |
| Sync content → site | `python build\sync_content.py` |
| Generate QR | `python build\make_qr.py <URL>` |
| Split / merge deck | `python build\split_deck.py split|merge …` |
| Publish a change | `git add -A` · `git commit -m "…"` · `git push` |
