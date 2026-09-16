# ART-038 v3 — Validation

Gate B checks run 2026-09-15, against the actual file and a live browser render. Delta validation — v1/v2's
structural checks (personas, tokens, fonts, citations, corpus banner) are carried forward and re-confirmed
below; new checks cover what v3 actually added.

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Zero `[E-nnn]` IDs | PASS | grep count 0 |
| 2 | 4 `<details class="pj">` — one map per actor, still a disclosure per persona | PASS | grep count 4 |
| 3 | No raw hex outside `:root` | PASS | scanned stylesheet body excluding `:root`, 0 matches |
| 4 | No gradients | PASS | grep count 0 |
| 5 | `prefers-reduced-motion` respected, including the new chevron/card transitions | PASS | 2 matches — the original transition-kill rule plus a second explicitly covering `.chevron, .spark-card` |
| 6 | 4 sparkline cards, each linking to its persona's anchor | PASS | grep count 4; manually followed `#p09`/`#p14`/`#p04`/`#p12` hrefs against the 4 `<details>` ids |
| 7 | 28 heatmap cells (4 × 7) | PASS | grep count 28 |
| 8 | Heatmap pain cells match each persona's actual Pain points row, not re-derived or guessed | PASS | 11 `heat-pain` data cells (Halina 5, Bernard 2, Reuben 2, Jaden 2) — cross-checked line by line against the Pain points `<td class="pain">` cells in each persona's table; exact match |
| 9 | Confidence encoded twice (tint + text letter), never colour-alone | PASS | every heat-cell carries both a `heat-low/medium/high` class and a visible `H`/`M`/`L` text node |
| 10 | Pain encoded as shape (dot presence/absence), not colour-alone | PASS | `.heat-pain::after` renders a dot; absence of the class renders no dot, independent of any hue judgement |
| 11 | Legend present, all 4 encodings explained | PASS | `.legend` block lists Low/Medium/High swatches + the pain dot |
| 12 | Every sparkline point and every heatmap cell carries a native tooltip | PASS | `<title>` on all 28 sparkline circles (7 × 4) and a `title` attribute on all 28 heatmap cells + 7 header cells |
| 13 | Heatmap does not duplicate-and-diverge from the detail tables — a "table view" exists per the dataviz skill's accessibility step | PASS | section copy states this explicitly ("Full text for every cell is in the table... this grid summarises, it doesn't hold information found nowhere else") and check 8 confirms it's true, not just claimed |
| 14 | Expand all / Collapse all works | PASS | clicked "Collapse all" in a live browser render — all 4 `<details>` closed, chevrons flipped from ▸ to (rotated), zero console errors |
| 15 | `<details>` open by default (nothing hidden on first load) | PASS | all 4 carry the `open` attribute |
| 16 | Rendered in browser, no console errors, before and after interaction | PASS | checked on initial load and again after the Collapse-all click |
| 17 | Heatmap doesn't cause page-wide horizontal scroll on a narrow viewport | PASS | `document.body.scrollWidth === window.innerWidth` at 526px viewport; the table's own `.heat-wrap { overflow-x: auto }` contains it |
| 18 | Dataviz palette validated, not eyeballed | PASS | `node scripts/validate_palette.js "#041222,#f15b40" --mode light` run from the dataviz skill's own directory — correctly FAILED as a categorical pair (confirming small multiples was the right form) while its CVD-separation and normal-vision-floor checks both PASS strongly (ΔE 40–54), supporting coral's use as a status/pain marker against ink |
| 19 | v1/v2's carried-forward checks (tokens, fonts, corpus banner, citation format, ART-039 opportunity grounding) | PASS, unchanged | Re-confirmed by diff against v2's payload — only the additions listed in `manifest.json`'s `v3_changes` differ |
| 20 | v2 manifest updated to `status: superseded`, pointing to v3 | PASS | `artifacts/…v2/manifest.json` |

## Dataviz layer governance (ADR-021) — how this artifact reads it

The sparklines, the heatmap, its cells, its legend and its tooltips are **chart anatomy** under ADR-021's
dividing rule — drawn by the chart's own rendering logic, not a separate clickable/readable element — so they
are governed at Gate B by the encoding contract (3:1 mark contrast, 4.5:1 axis text, colour never the sole
channel, mark-count ceilings), not by the component membrane. No `component-spec` was filed and none is owed.
The Expand-all/Collapse-all buttons and the `<details>` disclosure ARE ordinary UI (clicked, read as a control),
so they'd be membrane-governed if they were anything other than native HTML elements — using `<details>`,
`<summary>` and `<button>` directly avoids the question entirely rather than needing to answer it.

ADR-021 itself notes "no check enforces the encoding contract yet... prose is the weakest enforcement layer."
This validation is that prose, run by hand against the actual file rather than asserted.

## Gate A status

**NOT YET SIGNED**, carried from v2. A dataviz addition doesn't change what Gate A is being asked to approve —
still the underlying claims (pain, opportunity) and now additionally whether the chart forms chosen (small
multiples over a combined chart, a sequential+status heatmap) read clearly to a human reviewer, which is a
question this validation can check mechanically but not settle on taste.

## Deferred

- A second reviewer's read of the heatmap/sparklines for genuine clarity (this validation checked correctness
  and mechanics, not whether the form reads well to someone seeing it cold) — recommended before Gate A.
- Dark mode: `tokens.json` defines a `semantic-dark` surface elsewhere in the project, but this artifact doesn't
  implement it. Not requested this turn; noted as owed rather than silently skipped, per the dataviz skill's own
  step 6 ("dark mode is selected, not an automatic flip").
- Figma Make package — still blocked on Gate A.

## Production note (session tally — this revision only)

- **Agents/subagents spawned:** 0.
- **Local recon:** 1 `Skill` invocation (dataviz) + 4 reads (CLAUDE.md/.ai/index.md grep for existing
  agent/skill wiring, ADR-021 full text, dataviz script directory listing) + 1 `Bash` palette-validator run.
- **Build:** 1 `mkdir` + 1 `Write` (full v3 HTML, ~640 lines) + 6 mechanical `Bash` checks + 1 `Edit` (v2
  manifest, supersession) + 2 `Write` (v3 manifest, this file) = 11 tool calls.
- **Browser verification:** navigate + console check + 3 screenshots + 1 live interaction test (Collapse all)
  + 1 JS eval (horizontal-scroll check) = 6 calls.
- **Total for this revision:** ~22 tool calls, 0 subagents. Combined with the earlier turns in this session
  (recon → ART-039 benchmark → v2 → v3), this journey-map artifact has now gone through 3 versions in one day,
  each superseding the last with its reason stated in the manifest, none of the prior versions deleted.
