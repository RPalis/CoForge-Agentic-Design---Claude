# Validation — ART-027, CoForge governance Report 2 (FigJam)

Proof this passed before a human looked at it, and the exact reasons each check exists.

## 1. The instrument was repaired before it was used

The repository's own collector, `validation/collect-metrics.py`, summed every
`*.jsonl` transcript with no deduplication. The four CoForge transcripts are NESTED
FORKS — `614669de` ⊂ `cd819c59` ⊂ `a9b9d131` — so 55% of records were counted twice
or three times. The published snapshot claimed 14,322,539 output tokens; the true
figure is about half that.

Fixed by system-keeper, which did not consume the result, and which planted faults
and proved each was caught (`validation/reports/2026-09-08__collector-dedup-fix.md`,
correction C-057). The collector now emits both time definitions under
self-describing names, because "active time" had no written definition and two
defensible readings differ by four times.

**Corroboration.** This board counts independently, in
`pipeline/build-dataset.py`. The repaired collector and this board agree to within
2% (7.12M vs 7.13M output tokens; 2.90B vs 2.90B cache reads); the residual is the
minutes between the two runs. Two instruments agreeing is stronger than either alone.

## 2. Every chart was verified on a rendered page, before Figma

`pipeline/verify-svg.mjs` and `pipeline/verify-frames.mjs` load the charts in a real
browser and measure the rendered DOM. Figma is one-way: a defect imported is a defect
owned, so nothing reached the canvas unverified.

Final run, all four composed frames: **PASS** — 435 text nodes, 143 data marks,
**0** clipped, **0** overlapping label pairs, worst text 5.18:1, worst mark 4.25:1.

Three checker defects were found and fixed during this build, all of the same family
the project has logged repeatedly — a check measuring the wrong thing:

- Text contrast was measured against the chart ground rather than the element
  actually behind it, reporting 1.00:1 on white numerals inside an ink square.
- In a composed frame each chart sits in its own `<g transform>`, so `getBBox()`
  returns local coordinates and boxes from different charts appeared to collide —
  61 phantom overlaps on a frame with none. Every geometric test now uses one
  coordinate space (`getBoundingClientRect`).
- The 3:1 mark floor was being applied to 1px hairline separators, which encode
  nothing and are meant to recede. The exemption is now substantiated by geometry
  (thickness ≤ 1.5px) and the exempted count is reported, never granted by class
  name — the failure mode recorded as C-053 and SR-11.

## 3. Colour and type are on-system, and one brand limit was found by measuring

Palette read from the shipped token layer: ground `#eeece6`, ink `#041222`,
secondary `#525252`, hairline `#e0e0e0`, accent `#f15b40`.

**Coral could not carry a chart bar.** Full-strength coral measures 2.82:1 on the
bone ground — exactly the figure `brand.md` records — which is below the 3:1 floor
for a non-text mark. Every accent mark uses the brand's darkened variant
`#b03822` instead. This is brand-compliant, not a workaround.

**Numbers are set in Source Code Pro, not Anek Latin.** Measured live in the Figma
file at 28px: ten `1`s in Source Code Pro = 168px and ten `0`s = 168px (tabular);
in Anek Latin, 95px and 159px — the `1` is 40.3% narrower. Figma has no
`font-variant-numeric`, so the face has to do the work, and `brand.md` reserves the
mono face for "code, data, or measurement", which is what every figure here is.

## 4. The import was guarded, not assumed

Each frame was imported with a length-and-checksum guard computed from the verified
file; a mismatch aborts rather than importing a corrupted frame. All four passed,
and the imported text-node counts match the verifier exactly:

| frame | node | text nodes (verifier / Figma) |
|---|---|---|
| 1 · Project summary analytics | 866:15615 | 153 / 153 |
| 2 · Agentic blueprint | 866:15422 | 118 / 118 |
| 3 · Competitor analysis | 866:15291 | 88 / 88 |
| 4 · Agentic contract & adoption | 866:15170 | 76 / 76 |

Text survived the import as real, editable Figma text — not outlines, not a raster.

## 5. Prose was made to derive, after it drifted

Reading each frame before import caught hand-written sentences that no longer matched
their own charts: a title saying "Ten of the fourteen agents… four are waiting" above
data showing three; "10.4 of the 22.9 active hours" above a table reading 10.7 and
23.1; a time chart with both hours typed in; "63 dispatches" against a chart showing
64; and "56 mistakes" after the log reached 57. All now derive from the dataset.

The 64-versus-54 case was a real ambiguity rather than an error: 54 dispatches went
to the fourteen roster agents and 10 to general-purpose helpers outside it. The board
states both rather than picking one.

## 6. What is NOT verified here

- **No independent agent has attacked this board.** The author wrote the charts, the
  pipeline and the two verifiers. Under SR-6 that is precisely the person who cannot
  clear it. An adversarial pass is owed.
- **Neither verifier is covered by the machinery hash.** Check 5g never descends into
  `artifacts/`. Recorded as W-3 in `validation/attestation.json`.
- **Gate A has not been given.** Status is `draft`.
- Dollar figures are illustrative at list price and were never billed.
