# Validation — ART-005 · Coforge web, measured visual foundations

Checked 2026-08-27 against `validation/checklists/brand-extraction.md`.

## Provenance

- [x] Subject confirmed **first-party** — Agentic Designer - RP, 2026-08-27. Recorded in
      `manifest.subject`. Had it not been ours, `competitive-benchmark` was the
      correct type and `brand.md` could not have been written from it at all.
- [x] Five of six raw captures carry a resolvable URL **and** a sha256
      (`manifest.inputs.sources` S-01…S-05). Re-fetch and hash to verify.
- [x] Capture method stated and re-runnable — `manifest.capture.method`.
- [x] Capture date recorded: 2026-08-27.

**Exception, stated not hidden:** S-06, the rendered screenshot, has a sha256 but no URL.
A screenshot is not re-fetchable — a live site changes. It is a dated snapshot, currently
in `scratch/brand-extraction/raw/`. It cannot be moved into `research/sources/` by any
agent: `.claude/settings.json` denies `Write`/`Edit` on `research/sources/**`. **Placing it
is a human action and is outstanding.** Until then the claims resting on it — the wordmark
description and the illustration hues — are verifiable only by re-capture, not by hash.

## Gate B — automatic

- [x] Directory name matches `YYYY-MM-DD__brand-extraction__<slug>__v<N>`
- [x] `manifest.json` present, valid JSON, type registered in `artifacts/_types.json`
- [x] `validation.md` present (this file)
- [x] No `[E-nnn]` citations to resolve — no user is quoted; no ledger entry was faked
- [x] No `[ART-nnn § …]` citations outbound from this artifact
- [x] Raw hex exemption applies and is bounded: every hex here is a **reported finding**
      about the source. The artifact has no styling of its own.

## Measurement quality

- [x] Values read from the source's **declared** layer, not sampled from pixels. This is
      the finding that made the extraction worth doing — the token layer loads after first
      paint and is invisible to a computed-style read.
- [x] Defects demonstrated numerically: hue spread in degrees, luminance order, contrast
      ratios, method named.
- [x] Contrast reported against the grounds each colour actually appears on — bone and
      white — not white by default.
- [x] Coherent and defective ramps separated into two sections. Two of five ramps are
      usable; three are not. An undifferentiated value list would have invited the
      wholesale import this type exists to prevent.

## Gate A — human review

- [x] Claims are values, defects, or labelled assumptions
- [x] Assumptions block present and visible — A-1 to A-4
- [x] No brand judgment. The "Brand signal worth carrying" section is marked observed,
      not judged, and defers the decision to `brand-director`.
- [ ] Reviewed by: ______  Date: ______

## Known limits

- Homepage only. Inner templates may declare values not seen here (A-3).
- No motion captured — a single still frame (A-4). Anything about transition or easing
  is outside this artifact's evidence.
- `template_buttons.min.css` and `template_utilities.min.css` (S-03, S-04) were captured
  and hashed but not exhaustively parsed. They are listed so a later pass has them
  under a verified hash rather than re-fetching a changed file.
