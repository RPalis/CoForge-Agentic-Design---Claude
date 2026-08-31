# Validation — ART-007 · Monospace face benchmark

Checked 2026-08-28 against `validation/checklists/competitive-benchmark.md`.

## Gate B — automatic

- [x] Directory name matches `YYYY-MM-DD__competitive-benchmark__<slug>__v<N>`
- [x] `manifest.json` present, valid, type registered in `artifacts/_types.json`
- [x] `validation.md` present (this file)
- [x] No `[E-nnn]` citations to resolve — no user is quoted; no ledger entry was faked
- [x] Raw hex: none. This artifact reports type metrics, not colour.

## Gate A — human review

- [x] Claims labelled `Evidenced` / `Inferred` / `Assumption`
- [x] Assumptions block present and visible — A-1 to A-4
- [x] Reviewed by: **Agentic Designer - RP** · Date: **2026-08-28**

## How this one was found

Not by inspection. `validation/audit-contracts.py` flagged that
`typography.scale.code` resolved to exactly the same four aliases as
`typography.scale.caption` — a proportional sans behind a level whose entire purpose is
fixed-width alignment. The contract audit was written to catch redundancy between token
names; it caught a semantic defect instead, which is worth recording because it is the
first time a check in this repo surfaced something nobody had gone looking for.

## Measurement quality

- [x] Method stated and re-runnable — `manifest.capture.method`
- [x] Every family confirmed loaded before measuring, so no figure is a fallback
- [x] The reference face (Anek Latin) measured in the **same pass** as the candidates,
      not quoted from ART-006 — same engine, same rasterisation, so the deltas are
      comparable rather than assembled from two sessions
- [x] The non-discriminating criteria are reported as non-discriminating (licence,
      availability, weight range, monospace-ness) rather than padded into a scorecard
      to make the comparison look broader than it was

## Known limits

- **Ambiguous glyphs were not measured** (A-3). `0`/`O` and `1`/`l`/`I` legibility is a
  real criterion for a code face and this pass did not test it. Source Code Pro is
  believed to ship a dotted zero; that was **not** verified programmatically and should
  not be treated as established by this artifact.
- **Single engine, no hinting model** (A-2). Chrome only; small-size rasterisation
  differs across platforms.
- **Optical pairing is assessed by proxy** (A-4). x-height and cap-height ratios predict
  how two faces sit together; they do not measure it. No human read the pairing.
- The decision rests on one criterion. That is defensible here because the other five
  genuinely did not separate the field — but it does mean a single measurement error
  would change the outcome, and the x-height figures are the thing to re-check if the
  choice is ever questioned.
