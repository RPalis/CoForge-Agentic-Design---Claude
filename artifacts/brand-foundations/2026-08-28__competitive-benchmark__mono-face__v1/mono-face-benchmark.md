# Monospace face — six candidates against Anek Latin

**ART-007** · competitive-benchmark · v1 · measured 2026-08-28

Decision aid for the monospace family behind `typography.scale.code`. The gap was found
by `validation/audit-contracts.py`: `typography.scale.code` was byte-identical to
`caption` — Anek Latin, a proportional sans — while `component-index.json` declares
`code` as a real type level. Code set in a proportional face defeats the only reason a
code level exists.

Measurements are re-runnable: canvas `TextMetrics` at 200px, weight 400, in Chrome via
the DevTools MCP, with each family confirmed loaded via `document.fonts.check` before
measuring so no result is a silent fallback.

## Monospace is not the differentiator

All six candidates are true monospace. Advance spread across `i I l 1 O 0 m W x .`
measured **0.00px** for every one of them, against Anek Latin's 125.29px. That criterion
separates mono from non-mono and nothing else, so it cannot pick a winner.

## Optical pairing

Inline code sits *inside* body text. A mismatched x-height reads as a size change
mid-sentence, which invites a compensating font-size nudge on the code — and that nudge
then breaks the column alignment in tables that was the whole point of choosing a
monospace face. So the deciding measure is how closely a candidate's x-height tracks the
body face it will sit inside.

Anek Latin, the reference: **x-height ratio 0.488**, cap-height 0.639.

| Candidate | x-height | Δ vs Anek | cap-height | Δ vs Anek | advance ratio |
|---|---|---|---|---|---|
| **Source Code Pro** | 0.486 | **0.4%** | 0.656 | 2.7% | 0.600 |
| Space Mono | 0.496 | 1.6% | 0.700 | 9.5% | 0.612 |
| DM Mono | 0.496 | 1.6% | 0.700 | 9.5% | 0.600 |
| IBM Plex Mono | 0.516 | 5.7% | 0.698 | 9.2% | 0.600 |
| Roboto Mono | 0.528 | 8.2% | 0.711 | 11.3% | 0.600 |
| JetBrains Mono | 0.550 | 12.7% | 0.730 | 14.2% | 0.600 |

Source Code Pro is **14× closer** to Anek Latin than IBM Plex Mono and **30× closer**
than JetBrains Mono. It also has the smallest cap-height divergence, so capitalised
tokens and constants sit correctly against surrounding prose without adjustment.

## What did not separate them

- **Licence** — all six are SIL Open Font Licence. No constraint.
- **Headless availability** — all six are served by Google Fonts and confirmed loaded.
  Criterion 6 of brand.md §4 ("available to an agent, headless, at render time") is met
  by every candidate.
- **Weight range** — 400, 500 and 700 loaded for all six. Code needs emphasis, not a
  hierarchy ladder, so a wide range earns nothing here.

## Outcome

**Source Code Pro**, decided 2026-08-28.

Chosen on optical pairing alone, which is the only criterion that separated the field.
The choice also avoids setting a second element of CoForge's identity in IBM's type
after brand.md §6's "Not IBM" position — but that is a consequence, not the reason.
Had IBM Plex Mono won on measurement, the brand argument would have had to be made
explicitly rather than smuggled in behind a metric, as it was for OQ-2 in ART-006.

Recorded in `typography.family.mono` and consumed by `typography.scale.code`.

**One authored decision beyond the face itself:** `scale.code` uses tracking step 03
(the curve's zero-crossing) rather than caption's slightly-open step 01. A monospace
face already carries a fixed advance; adding letter-spacing widens an already-wide face
and degrades the column alignment that justifies using one.

## Assumptions

- **A-1** Measured as served by Google Fonts on 2026-08-28. Self-hosting or a foundry
  release could differ.
- **A-2** Single rendering engine (Chrome). Hinting at 12–14px differs across platforms
  and is not modelled here.
- **A-3** Ambiguous-glyph legibility — `0`/`O`, `1`/`l`/`I` — was **not** measured. It is
  a real criterion for a code face and needs visual review. Source Code Pro ships a
  dotted zero, but that was not verified programmatically in this pass.
- **A-4** No reading test with humans. Optical pairing is assessed from glyph metrics,
  which are a proxy for how the pairing actually reads.
