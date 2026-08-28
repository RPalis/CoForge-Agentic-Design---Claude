# Validation — ART-006 · Body face benchmark

Checked 2026-08-27 against `validation/checklists/competitive-benchmark.md`.

## Gate B — automatic

- [x] Directory name matches `YYYY-MM-DD__competitive-benchmark__<slug>__v<N>`
- [x] `manifest.json` present, valid, type registered in `artifacts/_types.json`
- [x] `validation.md` present (this file)
- [x] No `[E-nnn]` citations to resolve — no user is quoted; no ledger entry was faked
- [x] Raw hex: none present. The artifact reports type metrics, not colour.

## Gate A — human review

- [x] Claims labelled `Evidenced` / `Inferred` / `Assumption`
- [x] Assumptions block present and visible — A-1 to A-3
- [x] Reviewed by: **Raquel** · Date: **2026-08-27**

## Type fit, declared not hidden

`competitive-benchmark` is defined as "comparison against competitors on named dimensions."
The subject here is two typefaces competing for one role, not two companies. The structure
matches exactly — named dimensions, scored, with a verdict — and a bespoke type for a
one-off would inflate a controlled vocabulary for no gain. Recorded in `manifest.type_note`
so a reader meets the reasoning rather than guessing at it. Revisit if these recur.

## The recommendation was not the decision

This artifact recommends **IBM Plex Sans**. **Anek Latin was chosen.**

That divergence is deliberate and left standing. The benchmark measured what it measured;
the decision weighed a brand constraint the measurements cannot see — brand.md §6's
"Not IBM" position, on a question brand.md owns. Editing the artifact to agree with the
outcome would destroy its value as evidence: an assessment rewritten to match the decision
it informed records nothing.

The divergence is recorded in `manifest.decision_note` and in § Outcome of the payload.

## Measurement quality

- [x] Method stated and re-runnable — `manifest.capture.method`
- [x] Fonts confirmed loaded (`document.fonts.check`) before measuring, so no result is a
      silent fallback measurement
- [x] The deciding metric — default digit spacing — was measured two ways: with and
      without `tabular-nums`, establishing that Anek's proportional digits are a default
      and not a missing capability

## Known limits

- **Single rendering engine.** Chrome only. Hinting and rasterisation at 14px differ across
  platforms and this benchmark does not model that (A-2).
- **Criterion 1 is assessed by proxy.** x-height and advance width correlate with
  long-form legibility; they do not measure it. No human reading test was run (A-3).
  This is the weakest column in the comparison table and the one most worth revisiting if
  the choice is ever questioned.
- **`sha256` is null for both sources.** Google Fonts serves a per-user-agent subset, so a
  hash would fix this session's slice rather than the family. The method, not the binary,
  is what makes these numbers checkable.
