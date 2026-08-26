# PROGRESS.md — running build log

Newest entries at the bottom. One block per phase. Records what was done, what
defaults were chosen, and what (if anything) needs the user.

---

## Phase 0 — Scope lock  ·  2026-08-26

**Done**
- Created the folder skeleton: `content/`, `site/assets/{css,js,img,headshots}`,
  `site/downloads/`, `build/`, `docs/`. Empty dirs hold a `.gitkeep` so the tree
  survives version control.
- Wrote `HANDOFF.md` (operating companion to `pretext.md`).
- Wrote `docs/CONTENT_INVENTORY.md` with a Ship / Defer / Cut decision column,
  Tier 1 (11 blocks), Tier 2 (4 blocks), and explicit cuts (5 items).
- Started `docs/PROGRESS.md` (this file).
- Confirmed source inventory in `source_materials/`: Tutorial Template.pptx (327 MB,
  source-only), four section PDFs (Intro 1–11, JW 12–55, Joseph 56–79, ProfGan 80–191),
  Tutorial_Script.md, Speaker-Notes-Script.md (both CUT — private), and
  `reference_lists/` (Joseph refs .docx, ASI + AI-ANC selected-publications PDFs,
  Tutorial-JW-IEEE-References.md).

**Defaults chosen (no user input needed)**
- Empty-directory placeholders use `.gitkeep` rather than folder README stubs, to
  keep the deployed tree clean.
- Ship/Defer/Cut mapping follows `pretext.md` Tier 1 / Tier 2 / excluded lists verbatim;
  where `pretext.md` was silent (footer, learning-outcomes count), sensible defaults were
  taken and noted in the inventory.
- Environment: no local shell on this Windows device, so the build runs in the cloud
  workspace and commits files to `F:\Claude-EUSIPCO-Website`.

**Needs the user (batched — not blocking Phases 1–4)**
- GitHub org/account to deploy under (required before Phase 5). Flag if the lab org
  does not exist yet.
- Room / track detail for the hero.
- Section timings (absent from the flow notes) — for Phase 6 confirmation.
- Placeholder-safe assets: headshots, demo clips, lab logo — swap in when provided.

**Next:** Phase 1 — Extraction (outline.json, people.json, references.json).

---

## Phase 1 — Extraction  ·  2026-08-26

**Done**
- Read all four reference lists in `source_materials/reference_lists/` (JW IEEE .md,
  Joseph .docx, AI-ANC .pdf, ASI .pdf) and the `tutorial-outline-flow.md`.
- Produced `content/outline.json` — 7 blocks (opening §0, five core sections §1–§5,
  conclusions §6), presenter-attributed, with slide ranges and per-subsection topics.
- Produced `content/people.json` — three presenters with titles, affiliations, research
  areas, bios, and links. Titles/roles verified against NTU SNTL and DR-NTU pages.
- Produced `content/references.json` via a reproducible builder (`build/build_references.py`):
  **104 source citations → 103 unique** (one cross-list duplicate merged). All `verified:false`.
- Produced `content/meta.json` — abstract + 6 learning outcomes (both draft:true),
  event metadata, slide-release policy (`after_session`), and download manifest.
- Reference counts by section: §1 = 35, §2 = 14, §3 = 34, §4 = 17, §5 = 4 (the shared
  Hou 2023 paper is tagged both §3 and §4).

**Conflicts & duplicates logged**
- **Slide numbering conflict.** `pretext.md` states "183 slides total; Jun Wei's section
  is slides 9–54." The actual source PDFs and `tutorial-outline-flow.md` instead show
  **JW = slides 12–55** and a **191-slide deck** (Tutorial_ProfGan_80-to-191.pdf).
  Default chosen: adopt the source PDFs / flow file (JW 12–55, 191 total). **Needs user
  confirmation** — this changes the hero and download labels.
- **Section-numbering mismatch.** Joseph's reference `.docx` is titled "Section 3 (Joseph),"
  but the tutorial flow places his content as **Section 2 — Contextual Understanding**.
  Default: follow the flow's numbering (Joseph = §2). The `.docx` "Section 3" label refers
  to an older ordering.
- **Cross-list duplicate.** Hou et al., "AI-based soundscape analysis…" (JASA, 2023) appears
  in both the AI-ANC (authors) and ASI (others) lists. Merged into one entry (`s3a-20`),
  tagged sections §3 and §4.
- **ASI list spans two sections.** The ASI list mixes soundscape (→ §4) and hearables /
  intelligent sound management (→ §5). Split per-paper by topic: AR/MR hearables review,
  Sound Bubble, semantic hearing, and open-ear ANC glasses → §5; soundscape/annoyance
  work → §4.

**Defaults chosen (no user input needed)**
- **Integrity rule for identifiers:** only DOIs/arXiv ids/URLs present in the source lists
  were recorded. 36 entries (Xplore-only JW links and all of Joseph's list) have no DOI yet —
  left null for Phase 2 rather than invented.
- Per-section timings left null (absent from all source materials).
- Abstract and learning outcomes written from the outline arc, flagged draft:true.

**Found for Phase 2 (to apply during verification)**
- Tan et al. "Acoustic scene classification using CNN-GRU model without knowledge
  distillation" → arXiv:2509.09931 (surfaced while verifying bios).

**Needs the user (non-blocking)**
- Confirm the slide-numbering resolution above (12–55 / 191 total).
- Presenter bios/links confirmation is deferred to Phase 6 as planned.

**Next:** Phase 2 — Reference verification (fill DOIs, confirm authors/venue/pages/year).

---

## Phase 2 — Reference verification  ·  2026-08-26

**Done**
- Verified all 103 references and re-ran the builder. Each entry now carries a
  `verification` field:
  - **web (41)** — title/venue/year corroborated against arXiv / IEEE Xplore / publisher
    pages this phase. Covers every Section 1 entry that was searchable and all of Section 2.
  - **source-doi (60)** — DOI/arXiv taken from the presenters' own curated publication
    lists (Sections 3–5). Resolvable and treated as verified, but not independently
    re-checked (they are largely the presenters' own papers).
  - **unresolved (2)** — no stable identifier found; batched below.
- Added confirmed identifiers to ~30 entries (arXiv ids for the SELD/LALM papers, DOIs for
  the EURASIP/IEICE/Springer papers, and the Nature Electronics DOI for the Sound Bubble paper).
- **Corrected a Phase 1 integrity slip:** Section 2 (Joseph's `.docx`) listed authors only
  as "First-author et al." Phase 1 had over-expanded several into full author lists (inventing
  co-authors). Restored the source "et al." form for all 14 Section 2 entries.
- Applied the arXiv id found earlier for Tan's CNN-GRU paper (arXiv:2509.09931).

**Method note**
- The Crossref REST API returned HTTP 429 (rate-limited) from the shared egress IP, in
  parallel and sequentially, so DOI resolution was done via WebSearch against arXiv, IEEE
  Xplore, and publisher pages instead. This is why unchecked source-list DOIs are labelled
  `source-doi` rather than independently re-confirmed — exhaustive per-DOI resolution was
  not reliable in this environment.

**Unresolved — batched for the user**
- **s1-14** — Yeow, Tan, Bai, Peksi, Gan, "Enhancing 3D sound event localization and
  detection with distance estimation using reverberation and spatial coherence features,"
  *IEEE Sensors J.*, vol. 25, pp. 29221–29237, 2025. No DOI/Xplore link located — this is
  the presenter's own paper, so **Jun Wei can supply the DOI directly**.
- **s1-22** — Nozaki, Bando, Onishi, "Source-aware spatial self-supervision for SELD,"
  *ICASSP 2025*. The source-provided IEEE Xplore link (doc 10890626) is in place and the
  citation renders, but the DOI was not independently confirmed.

**Next:** Phase 3 — Visual direction (one homepage layout, navy + teal, checked at 380px first).

---

## Phase 3 — Visual direction  ·  2026-08-26

**Done**
- Built the design system (`site/assets/css/styles.css`) and one full homepage layout
  (`site/index.html`), mobile-first, verified at 380px, 1280px, and in dark mode via
  headless-Chromium screenshots.
- Content baked in from the JSON (hero, abstract + outcomes, presenter cards, the full
  7-block outline as native `<details>` accordions, gated download cards, a references
  sample, contact + QR placeholder, footer).

**Design decisions (one direction, chosen — not presented as options)**
- **Palette:** the deck anchor exactly — navy `#0E2842`/`#17364F` ground, teal `#0F6E56`
  accent (brightened to `#17A483` on dark). Cool neutrals biased toward teal, not flat grey.
- **Type:** `Calibri` first (the anchor), then **Carlito** — a metric-compatible Calibri
  substitute served from Google Fonts, so Windows viewers get real Calibri and everyone
  else an identical fallback. **IBM Plex Mono** for technical metadata (slide ranges, DOIs,
  section numbers, eyebrows) — apt for a signal-processing tutorial.
- **Motif:** faint concentric "sound-propagation / DOA" arcs in the navy hero. Subtle, on-theme.
- **Structure:** numbered section markers (0–6) are honest here — the outline is a real
  sequenced arc. Native `<details>` accordions → no JS needed for the outline/references.
- **Themes:** full light + dark via tokens (system-default + explicit `data-theme`).
  Accessibility: skip link, visible focus rings, semantic landmarks, reduced-motion honored.

**Notes / deferred to Phase 4**
- Content is currently baked into `index.html`; Phase 4 converts it to a JS loader reading
  `content/*.json`, and populates the full 103-reference list (only a sample is shown now).
- No mobile nav menu yet (links hide < 720px; page still scrolls) — Phase 4 polish.
- QR is a placeholder box; generated in Phase 5.

**Next:** Phase 4 — Build (JS loader from JSON, split_deck.py, accessibility pass).

---

## Phase 4 — Build  ·  2026-08-26

**Done**
- Converted `index.html` into a data-driven shell; new `site/assets/js/app.js` fetches
  `assets/data/*.json` and renders the abstract, learning outcomes, presenter cards, the
  7-section outline, the download manifest, and the full reference list. Verified via a
  local server + headless Chromium: 3 presenters, 7 outline sections, **104 reference
  entries** rendered (103 unique; the cross-listed Hou paper appears in both §3 and §4),
  5 downloads, 6 outcomes — all from JSON.
- `build/sync_content.py` — mirrors `content/*.json` → `site/assets/data/` so the deploy
  (site/ only) can load them without referencing outside `site/`.
- `build/split_deck.py` — merges the four section PDFs into a full deck, or splits a
  full deck into per-presenter PDFs. Round-trip validated on the real section PDFs.
- Added a mobile nav menu (accessible toggle: `aria-expanded` / `aria-controls`).
- **Accessibility pass:** heading order h1→h2→h3 with no skips, single h1, every image has
  alt (avatars are decorative `aria-hidden`), no empty links/buttons, `main`/`header`/`footer`
  landmarks, `lang="en"`, native `<details>` keyboard support, visible focus rings, skip
  link, and `prefers-reduced-motion` honored. Verified at 380 / 900 / 1280 px, light + dark.

**Data correction (measured from the actual PDFs — third slide-count value)**
- The provided section PDFs total **187 pages**, not 191: Intro 11, Yeow 44, Tan 24,
  **Gan 108**. The Gan file is named "…80-to-191" but contains 108 pages, so the deck ends
  at **slide 187**. Download labels updated to 1–187 (full) and 80–187 (Gan); a `deck_note`
  was added to `meta.json`. This now supersedes both `pretext.md`'s "183" and the filename's
  "191" — **please confirm the true deck length.** Outline section ranges still show the
  flow-file numbering (§6 conclusions "187–191"); the tail is uncertain by ~4 slides.

**Notes**
- The loader uses `fetch()`, which needs HTTP — it will not run from a `file://` URL. For
  local preview, run `python -m http.server` inside `site/`; GitHub Pages serves it directly.
- Fonts load from Google Fonts on the live site; in the sandboxed test browser that host is
  blocked, so the Calibri/system fallback renders (identical on the presenters' Windows machines).
- Slides remain gated: no PDFs are placed in `site/downloads/` yet. `split_deck.py` is ready
  to generate them when the presenters release the deck post-session.

**Next:** Phase 5 — Deploy (push to repo, enable Pages on site/, QR, verify).

---

## Phase 5 — Deploy (prepared; handed to user for the account-bound steps)  ·  2026-08-26

**Done (everything not requiring the user's GitHub account)**
- `.github/workflows/deploy.yml` — GitHub Pages via Actions, uploads `./site` only.
  This honours "deploy from site/ only" without moving files (branch-mode Pages can serve
  only root or /docs; the Actions flow serves any folder).
- `build/make_qr.py` — high-error-correction (level H) QR generator using segno; writes
  `site/assets/img/qr.svg` + `.png`, and points `content/meta.json → contact.qr` at it.
  Pipeline validated: an example URL encoded to a v6-H code and **decoded back correctly
  with OpenCV** (confirmed scannable).
- Wired the QR into the site: `app.js` renders `assets/img/qr.svg` when present, else a
  placeholder. Updated the placeholder copy.
- `site/.nojekyll` (safety for any future branch-deploy).
- `README.md` (repo overview, local preview, edit/deploy pointers) and
  `docs/DEPLOY.md` (full step-by-step deploy guide, Windows PowerShell).

**Blocked on the user (by design — the repo does not exist yet)**
- Creating the GitHub repo, pushing, enabling Pages, and getting the live URL — covered
  step-by-step in `docs/DEPLOY.md`.
- **The QR encodes the final URL**, so it is generated in step 4 of the guide once the URL
  exists (one command). Alternatively the user sends the URL and I produce `qr.svg`/`qr.png`.
- **`.github/workflows/deploy.yml` could not be committed to the device** — the remote bridge
  blocks writes under `.github/workflows/` (GitHub security). The file was delivered in chat
  and its full contents are inlined in `docs/DEPLOY.md` step 1b for the user to create by hand.

**Defaults chosen**
- Deploy mechanism: GitHub Actions upload of `site/` (not branch deploy).
- Suggested repo name in the guide: `eusipco2026-tutorial`; recommended a lab/org account
  (per the brief) with a personal-then-transfer fallback if the org doesn't exist yet.

**Next:** Phase 6 — Draft (don't send) a review message for Prof. Gan and Joseph
(bio accuracy, section timings, slide-release timing).

---

## Content update — post-deploy  ·  2026-08-26

Requested changes to the live site (repo `itsjunwei/eusipco-website`, Pages URL
`https://itsjunwei.github.io/eusipco-website/`). Scope limited to the three items below.

**Done**
1. **Jun-Wei Yeow — Scholar link.** Added `links.scholar`
   (`https://scholar.google.com/citations?user=iQpCWVYAAAAJ&hl=en`) to `content/people.json`,
   matching the existing `scholar` field used for Gan and Tan. Renders as a "Scholar ↗" chip.
2. **Downloads → single entry.** Removed the four subset items (intro / yeow / tan / gan) from
   `content/meta.json` → `downloads.items`; kept only the full-deck entry, labelled
   "Full tutorial deck · All · 183 slides · PDF" with the after-session placeholder (no dead
   link). Rendering is data-driven, so it now shows exactly one card. Updated `deck_note`.
3. **Presenter labels removed from refs & outline.**
   - References: stripped "(Presenter)" from all five `sections` titles in
     `content/references.json` **and** in `build/build_references.py` (so a rebuild stays
     name-free). Topic grouping unchanged.
   - Outline: removed the presenter label from the outline display in `site/assets/js/app.js`
     (`renderOutline`); section titles and slide ranges are kept.

**Verification (380px)**
- 1 download card; outline shows no presenter (`.who` absent); all 5 reference titles
  name-free; Jun-Wei's Scholar link present; no horizontal overflow; no JS page errors.

**Flags (not fixed — outside the three requested items)**
- **Slide count:** labelled **183** per instruction. Measured deck is **187 pages** (Phase 4).
  Left at 183 as requested; confirm the true length before release.
- **`content/outline.json` `presenter` field kept** as non-displayed metadata (only the display
  was removed). Say if you want it stripped from the data too.
- **Pre-existing cosmetic bug:** the downloads notice text renders twice ("Slides will be
  available for download after the session." doubled) because `renderDownloads` appends
  `release_note` to an already-complete sentence. Present before this update; flagged rather
  than silently fixed. One-line fix available on request.

**Not done by me (no git access to the machine):** the `git commit` + `git push`. Files are
written to the folder; the user pushes to publish, then Pages redeploys.
