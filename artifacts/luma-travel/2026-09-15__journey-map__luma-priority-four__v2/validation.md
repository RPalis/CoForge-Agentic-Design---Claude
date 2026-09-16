# ART-038 v2 — Validation

Gate B checks run 2026-09-15, against the actual file. This is a delta validation — checks already passing
unchanged from v1 are noted as carried forward; only what v2 actually touched is re-verified in full.

| # | Check | Result | Evidence |
|---|---|---|---|
| 1–20 | All v1 structural/token/font/motion/scope checks (see v1's `validation.md`) | PASS, carried forward | Only the Opportunities cells changed; grep-confirmed unchanged elsewhere (persona count 4, confidence cells 28, zero stray persona IDs, zero raw hex outside `:root`, zero gradients, zero `[E-nnn]`) |
| 21 | Every new opportunity citation resolves to `[ART-039 § persona]` | PASS | 7 citations: 2 Halina, 2 Bernard, 2 Jaden, 1 Reuben — all match real section headings in ART-039 |
| 22 | Opportunity citations use `[ART-039 § …]`, never conflated with the persona's `[ART-030 § …]` pain citation | PASS | Checked inline — each rewritten cell keeps its own distinct citation, Evidence row (pain) still cites ART-030 only |
| 23 | Cells that had no grounded opportunity in v1 remain `—`, not filled with invented content | PASS | Only 7 of the ~28 Opportunities cells carry a citation; the rest are unchanged `—` or the 2 previously-uncited cells (Halina pre-departure/airport, Bernard's — wait: Reuben's return cell) that ART-039 didn't reach |
| 24 | Honesty preserved — Bernard's uncorroborated claim stated as such, not silently resolved | PASS | Both Bernard opportunity cells state the absence/vacancy directly in their own text, matching ART-039's own finding |
| 25 | v1 manifest updated to `status: superseded`, pointing to v2 | PASS | `artifacts/…v1/manifest.json` — `status: "superseded"`, `superseded_by` set |
| 26 | v2 manifest declares `supersedes` and lists ART-039 as a new input | PASS | `manifest.json` — `version: 2`, `supersedes` set, `inputs.artifacts` includes `ART-039` |
| 27 | Footer/lede updated to reflect v2 and cite ART-039 | PASS | Lede carries a `<b>v2:</b>` callout; footer provenance list adds `ART-039 (opportunity benchmark, new in v2)` |
| 28 | Rendered, no console errors | SKIPPED | Not re-screenshotted after this edit — the CSS/markup pattern is identical to v1 (verified render-clean) plus 7 inline `<span class="cite">` additions with an added, minimal CSS rule; visual re-check recommended before Gate A, not assumed |

## Two-tier claim format, stated explicitly (this is the point of v2)

v1 conflated "this pain is real" and "this fix is worth building" under one column with no evidence for the
second half. v2 keeps them as two different evidentiary claims with two different citation targets:

- **Pain** → `Evidenced [ART-030 § persona]` — evidence about the persona (from the synthetic desk-research corpus).
- **Opportunity** → `Evidenced [ART-039 § persona]` — evidence about the market (from this session's competitive
  benchmark). A pain being real does not make a proposed fix precedented; those are different questions and now
  carry different citations, which is what makes checking one and not the other visible instead of hidden inside
  one merged claim.

## Gate A status

**NOT YET SIGNED**, same as v1 — this is a strengthening revision, not a new sign-off event. Human review still
required before design-brief use, Figma package production, or distribution. ART-039 (the benchmark this version
draws on) is also not yet signed and carries its own, lower-confidence Gate A question about whether
single-session web research is sufficient grounding at all — reviewing ART-038 v2 without also reading ART-039
would hide that ceiling.

## Deferred

- Fresh screenshot/console check on v2 specifically (check 28 above).
- Live-account competitive walkthrough (ART-039's own deferred item) — would let several opportunity citations
  move from "precedent exists, Medium confidence" toward something closer to ART-012's High-confidence tier.
- Figma Make package — still blocked on Gate A, unchanged from v1.

## Production note (session tally — this revision only; v1's own tally is in v1's validation.md)

- **Agents/subagents spawned:** 0.
- **New artifact produced first:** ART-039 (competitive-benchmark) — 9 web tool calls (4 WebSearch + 5 WebFetch,
  one WebFetch retried after an empty JS-rendered page) + 2 local recon reads + 3 Write calls (payload, manifest,
  validation). Full tally in ART-039's own `validation.md`.
- **This revision (ART-038 v2):** 1 `mkdir` + 1 `cp` (v1 → v2 starting point) + 1 partial `Read` (to satisfy the
  edit-after-read requirement) + 6 `Edit` calls (4 persona opportunity cells + 1 CSS rule + 2 header/footer text
  updates — 6 total, not 7, one Edit covered two personas' worth of a single contiguous CSS change) + 1 `Edit` on
  v1's manifest (supersession) + 2 `Write` calls (v2 manifest, this file) = 11 tool calls for the revision itself.
- **Full chain for this request, end to end:** local recon (2) → web research (9) → benchmark artifact (3 writes)
  → journey-map revision (11) = 25 tool calls, 0 subagents, 1 new artifact (ART-039) plus this revision of
  ART-038, from "opportunities are too blanked" to a grounded, honestly-gapped v2.
