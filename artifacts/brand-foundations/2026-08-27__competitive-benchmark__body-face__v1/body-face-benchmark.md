# Body face — Anek Latin against IBM Plex Sans

**ART-006** · competitive-benchmark · v1 · measured 2026-08-27

Decision aid for **OQ-2**, the body face brand.md deliberately left unpicked. Six criteria
come from `design-system/foundations/brand.md` §4. Measurements are re-runnable: canvas
`TextMetrics` at 200px for glyph proportions, DOM width comparison at 64px for digit
spacing, in Chrome via the DevTools MCP.

This artifact records measurements and a recommendation. **The decision was made by a
human** — see § Outcome.

## The finding that decides it

Roughly all of CoForge's L1 output is documents — `dashboard`, `metrics-scorecard`,
`test-report`, tables of numbers. The question is therefore not which face is handsomer,
but which behaves when digits stack up.

| | `1111` vs `0000` at 64px | With `tabular-nums` |
|---|---|---|
| **Anek Latin** | **58.88px apart** — proportional | 0.00px |
| **IBM Plex Sans** | **0.00px** — tabular by default | 0.00px |

Anek Latin's digits are proportional by default: a `1` is **7.7% narrower** than a `0`.
Columns of figures do not align unless every numeric context opts in. Anek *has* tabular
figures — `font-variant-numeric: tabular-nums` flattens the delta to zero, verified — so the
risk is not capability, it is **default**. The failure is silent and reads as sloppiness
rather than as a bug.

IBM Plex Sans is tabular with nothing opted into.

## Measured glyph metrics

Canvas `TextMetrics`, weight 400, 200px.

| Metric | Anek Latin | IBM Plex Sans | Why it matters |
|---|---|---|---|
| x-height ratio | 0.488 | **0.516** | Larger x-height reads better at 14px |
| Cap-height ratio | 0.639 | 0.698 | Sets apparent size against the display face |
| Avg lowercase advance | **0.479** | 0.505 | Anek fits ~5% more text per line |
| Ascender / x-height | 1.357 | 1.434 | Higher is airier, needs more leading |
| Default digit spacing | proportional | **tabular** | The deciding criterion |
| Weight range served | **100–800** | 100–700 | Display sits at 700–800 |

## Against brand.md's six criteria

| # | Criterion | Anek Latin | IBM Plex Sans |
|---|---|---|---|
| 1 | Long-form legibility at 14–16px on warm ground | smaller x-height | **pass** |
| 2 | Weight range reaching the display face's heavy end | **to 800** | to 700 |
| 3 | Real numerics — tabular figures, currency, percent | opt-in only | **default** |
| 4 | Neutral under a characterful display face | is the display face | **pass** |
| 5 | Licence clean for embedding in PDFs and decks | OFL | OFL |
| 6 | Available to an agent, headless, at render time | Google Fonts | Google Fonts |

Criterion 4 cuts oddly. Anek-under-Anek cannot compete with the display face because it *is*
the display face — but that also spends the display face's distinctiveness on body copy,
the one place brand.md says character is not wanted.

## Recommendation, as measured

**IBM Plex Sans**, on criteria 1, 3 and 4, losing only 2.

**The argument against, stated at the time:** brand.md §6 says *"Not IBM"* — it answered
ADR-011's deferred question by ruling that CoForge's surface is its own. Setting every word
of body copy in IBM's typeface is in real tension with that. It is a brand argument, not a
technical one, so these measurements do not settle it.

## Outcome

**Agentic Designer - RP chose Anek Latin, 2026-08-27.** The brand argument outranked the metric, which is
the correct precedence for a question brand.md owns.

The choice is made safe by a condition, recorded as a brand rule in brand.md §4: tabular
figures are bound into the type tokens for every level that can carry a number, so
proportional figures become the exception a designer asks for rather than the default they
inherit. Without that rule this decision imports a quiet defect into every table CoForge
produces.

Criterion 2 resolves in Anek's favour, so CoForge is single-family — one variable family
across display and body, with hierarchy carried by weight as §4 requires.

## Assumptions

- **A-1** Both faces measured as served by Google Fonts on 2026-08-27. Self-hosting or a
  foundry release could differ in weight coverage or numeral defaults.
- **A-2** Glyph metrics measured in one engine (Chrome). Rasterisation at 14px differs
  across platforms; this benchmark does not model hinting.
- **A-3** No long-form reading test with human participants was run. Criterion 1 is
  assessed from x-height and advance width, which are proxies for legibility, not
  measurements of it.
