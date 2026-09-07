# Turning the prose into a dashboard — plan

**Date:** 2026-09-07. Nothing built. `dataviz` skill loaded and governing every form choice.

## The board today, measured

**15,680 visible words. 47 prose cards. 121 index rows. 11 charts.**

| section | words |
|---|---|
| Full evidence index | 3,942 |
| Findings | 3,390 |
| Shape of the evidence | 2,482 |
| Recommendations | 2,043 |
| Insights | 1,199 |
| Method & corrections | 732 |
| Pain points | 681 |
| Coverage | 573 |
| Next steps | 380 |

## The tension, named before anything is built

"All text digested into widgets" cannot mean *delete the claims*. Each card is a claim, its
citation and its scope limit — that traceability is the only reason this board is worth
anything, and it is what four rounds of corrections have been protecting.

So the operative reading, which is also what a real dashboard actually does:

> **Extract the countable spine into widgets. Move the prose behind the detail panel that
> already exists and already works.** Nothing is deleted; the default view stops being an essay.

## What is countable on every card — verified, not assumed

| group | on every card | evidence count |
|---|---|---|
| Findings (15) | competitor · confidence · scope_limit · sources | 0–5 |
| Pain points (10) | confidence · scope_limit · sources | 1–4 |
| Insights (7) | weakest_confidence · confidence_note · sources | 3–10 |
| Recommendations (9) | weakest_confidence · rests_on · sources | 1–8 |
| Next steps (6) | sources | 0–1 |

> **No card in any group carries impact, effort, severity, priority or a score.** So no widget
> may rank by importance. Anything that looks like a priority ordering would be my judgement
> wearing the authority of a measurement — the exact defect logged as C-052 today.

## The widgets, chosen by the skill's own form heuristic

`choosing-a-form.md`: *a handful of headline numbers → a KPI row of stat tiles, not a grouped bar.
More than ~7 classes that all carry meaning → a table, not more colours.*

| # | Replaces | Form | Encodes (all existing fields) |
|---|---|---|---|
| 1 | the coverage prose | **KPI row + hero** | the five ratios as meters against their target |
| 2 | 15 findings cards | **scannable rows** | competitor · theme · confidence · evidence count; title one line; body in the panel |
| 3 | 10 pain-point cards | **rows** | confidence · evidence count. **No severity — we have none** |
| 4 | 7 insight cards | **rows + breadth meter** | how many distinct competitors each cites |
| 5 | 9 recommendation cards | **ranked rows + evidence meter** | `len(sources)` 1–8, and a marker on the 4 that remain evidentially alone |
| 6 | 6 next-step cards | **the ranked backlog** | tier 1–5 and effort, from `round2-capture-ranked.json` — 206 rows already ranked |
| 7 | the 121-row index | **stays a table**, filterable | the skill is explicit: >7 meaningful classes is a table |

## What must not become a widget
The claims themselves. *"Priority support unlocks at 15 completed bookings"* is a sentence, not a
number, and a widget that reduces it to a bar has thrown away the only thing that makes it
checkable. Every card keeps its full text one click away.

## Colour: our constraint is stricter than the skill's

The skill's palette validator governs **categorical** palettes. This board deliberately has none —
`cf-chart-palette` is deprecated (C-036) and the dataviz token group ADR-021 owes does not exist,
so everything encodes by position, length and step on one gray ladder.

That is not a limitation here. The skill names our situation directly: *"Emphasis = the most
underused form. One series in the accent hue, the rest in the de-emphasis gray. Often the honest
answer to 'make this chart clearer.'"* **Emphasis is our native mode.** The validator will still be
run against the gray ramp to confirm the steps clear their floors.

## Skills and agents

| | | |
|---|---|---|
| **`dataviz`** | loaded | governs every form choice, the mark specs, the hover layer, and the anti-pattern check |
| **`impeccable`** | to load | the layout and information-architecture pass — this is a UI redesign, not only a chart job |
| **dashboard-analyst** | builds | owns the dataviz layer in the routing table |
| **design-critic** | attacks | ADR-021 item 4; may not review what it built |
| **a11y-checker** | attacks | 47 cards becoming rows changes the whole heading and focus structure |

**Constraint:** subagent dispatches hit an account spend limit earlier; it resets 18:20
Europe/Madrid. Until then this runs in the main session, which is slower but not blocked.

## The test it has to pass
Your own standard, from earlier: **a junior VC who knows nothing about the research can scan it in
sixty seconds and know what to ask.** Not "it has more widgets."

## The risk, stated plainly
This is the third redesign of this board and you have twice said it is cluttered. The failure mode
is replacing readable prose with unreadable widgets and calling it progress. The mitigation is the
detail panel — it already exists, already manages focus, and already passes its checks, so every
widget has somewhere to put the words rather than losing them.

## Order
1. Load `impeccable`; decide the layout before any widget is written
2. Widgets 1, 5, 6 first — coverage, recommendations, next steps. Highest text-to-signal ratio
3. Then 2, 3, 4 — the three card groups
4. Render, screenshot, run all three verifiers, check against `anti-patterns.md`
5. design-critic and a11y-checker attack it

---

# Build plan, after loading `impeccable`, `dataviz`, `create-viz` and `brand.md`

## One instrument is wrong for this job, and I am not using it

`/data:create-viz` generates **matplotlib PNGs**. This board is a single self-contained HTML
file whose charts are inline SVG carrying `aria-describedby` text alternatives, a working
detail panel, keyboard focus management and a live-region readout. Raster images would delete
all of it and fail every accessibility check we just passed.

**Taken from it (its principles are sound):** a title states the insight, not the metric; grey
the reference data and highlight the one that matters; sort by value not alphabet; zero
baseline on bars. **Rejected: its toolchain.** Said plainly rather than quietly ignored.

*(One documented exception to "sort by value": `ch-effort` is deliberately alphabetical, because
sorted by count it reads as a league table of competitors when it measures our own effort.)*

## Mode: Operate. The brand and the mode agree on three things

| | brand.md | operate.md | ruling |
|---|---|---|---|
| Hierarchy | "Weight carries hierarchy before size does… the scale can stay short and dense" | "Tighter scale ratio, 1.125–1.2. Exaggerated contrast creates noise" | **Weight does the work. Short scale.** |
| Accent | "Exactly one hot accent… its power comes entirely from scarcity" | "Accent for primary actions, current selection and state indicators only, not decoration" | **Coral marks state and the one number that matters. Nothing else.** |
| Display face | Anek Latin 700, negative tracking, **headings only** | Constraint: "display fonts in UI labels, buttons, data" | **Anek for section headings. Never on a value, label or chip.** |

**The binding brand rule, unchanged:** coral never carries body text, small labels, captions,
legends, table values or form hints, on any ground. It fills, rules and marks. Where coral must
be text, `coral.text` is a different role. Coral on bone is 2.82:1 — it fails AA as text and the
brand says breaking this is breaking the brand.

## The widget vocabulary — one row shape, reused

`operate.md`: *"Consistent affordances across the surface. Same button shape. Same form-control
vocabulary."* So groups 2–6 share **one row**, not five bespoke layouts:

`[ title — one line, weight for rank ] [ facts — mono ] [ evidence meter ] [ state chip ]`

| # | Replaces | Encodes | Accent earns its place by |
|---|---|---|---|
| 1 | coverage prose | five meters against target | the worst ratio; the target rule |
| 2 | 15 finding cards | competitor · theme · confidence · evidence | a corrected finding |
| 3 | 10 pain cards | confidence · evidence. **no severity** | — |
| 4 | 7 insight cards | breadth: distinct competitors cited | — |
| 5 | 9 rec cards | evidence base 1–8 | the 4 that remain evidentially alone |
| 6 | 6 next-step cards | tier 1–5 · effort, from the 206 ranked rows | tier 1 |
| 7 | 121-row index | **stays a table**, gains a filter row | the active filter |

Prose is not deleted. Every row opens the detail panel that already exists, already manages
focus and already passes its checks.

## States, because Operate demands the full set
Every row: default · hover · focus-visible · active · selected. Every meter: a zero case.
The filter row: an empty-result state that teaches, not "nothing here". Motion 150–200ms,
state only, and `prefers-reduced-motion` already zeroes it.

## Verification, in one batched pass
Build fully → screenshot desktop and narrow together → fix everything in one batch → confirm
once → stop. Then `detect.mjs`, the three existing verifiers, `anti-patterns.md`, and only then
design-critic and a11y-checker.

**Not doing:** a palette validator run. It checks categorical palettes; this board has none by
necessity (C-036) and the gray ramp's steps are already contrast-verified by
`verify-charts.mjs` on the rendered DOM.
