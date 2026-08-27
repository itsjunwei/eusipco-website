# Content Inventory — EUSIPCO 2026 Tutorial Website

**Tutorial:** Environmental Acoustic Intelligence: From Acoustic Perception towards Context-Aware Sound Intervention
**Venue:** EUSIPCO 2026, Tutorial #2 · 31 August 2026
**Presenters:** Prof. Woon-Seng Gan · Dr. Ee-Leng Tan (Joseph) · Mr. Jun-Wei Yeow (all NTU)

This is the scope-lock table for the companion site. Every candidate content block is
listed with a **Ship / Cut / Defer** decision, its source, and the phase that produces it.
"Ship" = in the first live version. "Defer" = build only if time permits (Tier 2).
"Cut" = explicitly out of scope. Decisions here follow `pretext.md`; where `pretext.md`
was silent, the default chosen is noted in the Notes column and logged in `PROGRESS.md`.

---

## Tier 1 — Must ship

| # | Content block | Source | Decision | Produced in | Notes |
|---|---|---|---|---|---|
| 1 | Hero — title, subtitle, date, room, presenters | pretext.md, deck slides 1–2 | **Ship** | P3–P4 | Room/track number TBD — placeholder until confirmed |
| 2 | Abstract | deck slides 1–11, tutorial-outline-flow.md §0 | **Ship** | P1→P4 | Draft from opening framing (Hear→Understand→Reason→Act) |
| 3 | Learning outcomes | derived from outline arc | **Ship** | P1→P4 | 4–6 bullet outcomes across perception→action |
| 4 | Presenter bios (×3) | user-supplied / public pages | **Ship** | P1→P4 | Bios to be confirmed by Gan & Tan in Phase 6 |
| 5 | Presenter headshots (×3) | user-supplied | **Ship** | P4 | Placeholder initials-avatar until images provided |
| 6 | Tutorial outline — 5 sections, presenter-attributed, timings | tutorial-outline-flow.md | **Ship** | P1→P4 | outline.json is source of truth; timings TBD, flag |
| 7 | Slide downloads — full deck PDF | approved full-deck PDF | **Ship (released)** | P4–P5 | Single 186-slide full-deck download |
| 8 | Slide downloads — 3 per-presenter PDFs | split via build/split_deck.py | **Cut** | P4 | Removed by presenter request |
| 9 | References — grouped by section, IEEE format, DOI/arXiv links | reference_lists/ + in-deck citations | **Ship** | P1→P2 | Primary literature only; verified flag per entry |
| 10 | Contact + QR code | user + build/make_qr.py | **Ship** | P4–P5 | High error-correction SVG for closing slide |
| 11 | Footer — affiliation, copyright, last-updated | standard | **Ship** | P4 | Smart Nation TRANS Lab @ NTU |

## Tier 2 — Add if time permits

| # | Content block | Source | Decision | Produced in | Notes |
|---|---|---|---|---|---|
| 12 | Demos / media — SELD, ANC, soundscape audio clips | user-supplied | **Defer** | P4+ | Placeholder-safe; no clips yet |
| 13 | Supplementary resources — DCASE, datasets, toolkits | curated | **Defer** | P4+ | STARSS, DCASE Task 1/3, ARAUS, etc. |
| 14 | Cite-this-tutorial BibTeX block | generated | **Defer** | P4+ | Needs final citation metadata |
| 15 | Feedback form link | user-supplied | **Defer** | P4+ | External form URL from user |

## Cut — explicitly out of scope (never deployed)

| # | Content block | Reason |
|---|---|---|
| C1 | Speaker notes | Private; excluded per pretext.md |
| C2 | Spoken script (Tutorial_Script.md, Speaker-Notes-Script.md) | Private; excluded |
| C3 | PPTX source file (Tutorial Template.pptx, 327 MB) | Source-only; never deployed |
| C4 | Unpublished / preliminary results | Not for public release |
| C5 | Anything under source_materials/ referenced from site/ | Hard constraint: site/ links only to site/ |

---

## Hard constraints (carried from pretext.md)

- `site/` may reference **only** other files under `site/`. Never link or embed
  anything from `source_materials/`.
- Static single-page site, mobile-first, plain HTML/CSS/JS. No framework, no bundler.
- Deploy from `site/` only, GitHub Pages, on the **lab/org** GitHub account
  (not personal — flag if the org does not exist yet).
- IEEE citations, primary literature only, no invented citations, DOI/arXiv where available.
- Design anchor: navy `#17364F → #0E2842` + teal `#0F6E56`, Calibri or nearest web-safe.

## Open items to surface (batched, not blocking)

- **GitHub org/account** to deploy under — required before Phase 5.
- **Room / track detail** for the hero — placeholder until confirmed.
- **Section timings** — not present in the flow notes; needs presenter confirmation (Phase 6).
- **Headshots, demo clips, lab logo** — placeholder-safe; swap in when provided.
