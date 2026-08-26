# HANDOFF.md — Operating instructions

This repo builds and hosts the companion website for the EUSIPCO 2026 tutorial
**"Environmental Acoustic Intelligence."** It is designed to be driven end-to-end
by Claude, phase by phase, with minimal interruptions to the user.

`pretext.md` is the standing brief — the authority on decisions, scope, and phase
plan. This file is the shorter operating companion: how the pieces fit and how to
resume work in a later session.

## How the folders relate

```
source_materials/   PRIVATE inputs (deck, PDFs, scripts, reference lists). Never deployed.
content/            Generated JSON — the site's source of truth (outline, people, references, meta).
site/               THE DEPLOYED SITE. Only references files under site/.
build/              Scripts (deck split, QR, extraction). Not deployed.
docs/               CONTENT_INVENTORY.md (scope), PROGRESS.md (running log).
```

**Data flow:** `source_materials/` → (build scripts + extraction) → `content/*.json`
→ (JS loader) → `site/index.html`. The site never reaches back into `source_materials/`.

## Resuming work

1. Read `pretext.md` in full, then `docs/PROGRESS.md` to see where the last session stopped.
2. Continue from the next unfinished phase. Do not redo completed phases.
3. Follow the Operating rule in `pretext.md`: proceed autonomously; interrupt the user
   only for a missing required file, an unverifiable citation, or a genuinely unanswered decision.
4. Append to `docs/PROGRESS.md` at the end of each phase.

## Environment notes (for the executing session)

- This device (`dsp-pc2736`, Windows) exposes the project folder `F:\Claude-EUSIPCO-Website`
  to the session as a connected folder, but **no local shell** is available.
- Files are built in the cloud workspace and written to the device with
  `device_commit_files` (via a `SendUserFile` file_uuid). Large source PDFs are staged
  into the cloud workspace with `device_stage_files` for reading/processing.
- The 327 MB PPTX is source-only and should not be staged unless a step genuinely needs it;
  the per-section PDFs cover extraction needs.

## Publishing rules (from pretext.md)

- Outline + references publish immediately.
- Slide PDFs publish with a note **"available after the session,"** then flip live post-talk.
- Excluded from the site entirely: speaker notes, spoken script, PPTX source, unpublished results.
