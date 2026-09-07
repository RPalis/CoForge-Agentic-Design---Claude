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
