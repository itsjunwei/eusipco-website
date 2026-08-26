# pretext.md — EUSIPCO 2026 Tutorial Website Build

## Purpose of this document

This is the standing brief for building a companion website for the EUSIPCO 2026
tutorial "Environmental Acoustic Intelligence." The user is busy and wants to
delegate execution end-to-end. Read this file in full before doing anything.
Follow it phase by phase without re-asking questions this document already answers.

**Operating rule:** proceed autonomously through each phase. Only interrupt the
user for one of these three reasons:
1. A required file is missing (see File Inventory below) and no placeholder is acceptable.
2. A citation cannot be verified after a genuine search attempt.
3. A decision is needed that is genuinely not answered anywhere in this document.

Do not ask about design taste, wording, or anything with a reasonable default —
pick the default, note the choice in `docs/PROGRESS.md`, and move on. Batch all
open questions and surface them once at the end of a phase, not mid-task.

---

## Project identity

- **Tutorial:** Environmental Acoustic Intelligence: From Acoustic Perception
  towards Context-Aware Sound Intervention
- **Venue:** EUSIPCO 2026, Tutorial #2
- **Date:** 31 August 2026
- **Presenters:** Prof. Woon-Seng Gan, Dr. Ee-Leng Tan (Joseph), Mr. Jun-Wei Yeow — all NTU
- **Deck:** 183 slides total; Jun Wei's section is slides 9–54 (supervised SELD
  pipeline, label-efficient SELD, language-based SELD, context-aware SELD)

---

## Decisions already made (do not re-ask)

| Question | Decision |
|---|---|
| Site type | Static single-page site, mobile-first, no build framework |
| Hosting | GitHub Pages, deployed from `site/` only |
| Tech stack | Plain HTML/CSS/JS. No React, no bundler |
| Repo location | Lab/organisation GitHub account, not personal — flag if org doesn't exist yet |
| Slides release timing | Publish outline + references immediately; publish slide PDFs with a note "available after the session," then flip live post-talk. If user overrides this later, treat as a content update, not a redesign |
| Content excluded from site | Speaker notes, spoken script, PPTX source file, unpublished/preliminary results |
| Design anchor | Navy (#17364F → #0E2842) + teal (#0F6E56) from the deck's palette, Calibri or closest web-safe equivalent |
| Citation format | IEEE style, primary literature only, no invented citations, DOI/arXiv link where available |
| QR code | High error-correction SVG, placed in `site/assets/img/` and handed back for the closing slide |

---

## Folder structure to create

```
Claude-EUSIPCO-Website/
├── pretext.md                 ← this file
├── HANDOFF.md                 ← operating instructions (create alongside this)
├── source_materials/          ← PRIVATE, never deployed, user-provided
│   ├── [pptx, pdf, script, flow notes]
│   └── reference_lists/
├── content/                   ← generated structured data (site source of truth)
│   ├── meta.json
│   ├── people.json
│   ├── outline.json
│   └── references.json
├── site/                      ← DEPLOYED. Must never reference source_materials/
│   ├── index.html
│   ├── assets/ (css, js, img, headshots)
│   └── downloads/ (public PDFs only)
├── build/                     ← scripts, not deployed
│   ├── extract_outline.py
│   ├── split_deck.py
│   └── make_qr.py
└── docs/
    ├── CONTENT_INVENTORY.md
    └── PROGRESS.md            ← running log Claude updates after each phase
```

**Hard constraint:** files under `site/` may only reference other files under
`site/`. Never link or embed anything from `source_materials/` directly.

---

## File inventory — what must come from the user

Placeholder-safe (build with a stand-in, swap in later, do not block on these):
- Presenter headshots (use initials-avatar placeholder)
- Demo audio clips
- Any logo / lab branding

Cannot proceed without (stop and ask):
- The tutorial deck (PPTX or the subset PDF)
- The reference list(s)
- Confirmation of GitHub org/account to deploy under

---

## Site content scope

**Tier 1 — must ship:**
Hero (title/date/room/presenters) · Abstract + learning outcomes · Presenter
bios · Tutorial outline (5 sections, presenter-attributed, timings) · Slide
downloads (full deck + 3 per-presenter PDFs) · References (grouped by section,
IEEE format, DOI/arXiv links) · Contact + QR

**Tier 2 — add if time permits:**
Demos/media (SELD, ANC, soundscape audio) · Supplementary resources (DCASE,
datasets, toolkits) · Cite-this-tutorial BibTeX block · Feedback form link

---

## Phase plan

**Phase 0 — Scope lock.** Turn this document into `docs/CONTENT_INVENTORY.md`
with a ship/cut column. Confirm folder structure exists.

**Phase 1 — Extraction.** Read everything in `source_materials/`. Produce
`content/outline.json`, `content/people.json`, `content/references.json`
(merged from `reference_lists/` and in-deck citations, `verified: false` by
default). Log duplicates/conflicts to `docs/PROGRESS.md`.

**Phase 2 — Reference verification.** For each `verified: false` entry, search
IEEE Xplore / arXiv / publisher pages. Confirm authors, title, venue, volume,
pages, year, DOI. Never invent a field. Mark unresolved items and batch them
for the user rather than guessing.

**Phase 3 — Visual direction.** Produce one homepage layout using the design
anchor above, checked at 380px width first. No need to present options unless
genuinely torn — pick one, proceed.

**Phase 4 — Build.** Skeleton `index.html`, JS loader rendering from the JSON
files, `split_deck.py` to cut per-presenter PDFs, responsive + accessibility
pass (heading order, alt text, contrast, keyboard nav).

**Phase 5 — Deploy.** Push to repo, enable Pages on `site/`, confirm live URL,
generate QR, verify it scans.

**Phase 6 — Review.** Draft (don't send) a short review message for Prof. Gan
and Joseph covering: bio accuracy, section timings, slide-release timing.
Hand to user to send.

At the end of each phase, append a short entry to `docs/PROGRESS.md`: what was
done, what defaults were chosen, what (if anything) needs the user.
