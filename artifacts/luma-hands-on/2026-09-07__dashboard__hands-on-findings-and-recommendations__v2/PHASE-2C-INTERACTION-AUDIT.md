# Audit — Pain points onward, and what interactive data design the data actually supports

**Date:** 2026-09-07 · **Scope:** `#painpoints` · `#insights` · `#recommendations` · `#nextsteps`
**Status:** audit + plan. Nothing built.

## 1 · What these four sections are today

32 prose cards, **zero charts**, and one interaction — the shared detail panel every card on the
board already opens. Everything below the Findings section is currently read-only text.

| Section | Items | Source refs | Distinct findings cited | Confidence field |
|---|---|---|---|---|
| Pain points | 10 | 17 | 17 | `confidence_raw` |
| Insights | 7 | 28 | 27 | `weakest_confidence` |
| Recommendations | 9 | 19 | 17 | `weakest_confidence` |
| Next steps | 6 | 10 | 1 | — none |

## 2 · The finding this audit turned on

**The citation graph is already typed, already complete, and resolves at 100%.**

68 of 68 references from these sections to a finding resolve to a real indexed finding. Every
insight, every pain point and every recommendation names the evidence it stands on, in a
structured `sources` field — not in prose.

This corrects something I said earlier in this project. When I concluded the relation graph was
blocked because 71 relations sat buried in prose, that was true of **finding-to-finding**
relations and I generalised it to all relations. **Synthesis-to-evidence relations were typed all
along.** Linked highlighting is buildable today and needs no transcription phase first.

Two measurements fall straight out of that graph, and both are findings in their own right:

- **41 of the 113 findings carry a conclusion; 72 carry none.** (42 and 71 if Next steps are counted, but those describe owed work rather than conclusions resting on evidence, and they are excluded from the chart.) The round
  captured 121 findings and the argument uses just over a third of them.
- **18 findings carry more than one downstream item.** *Corrected after building the chart:* an
  earlier draft of this audit said F-57 carries four conclusions. It carries **three**. Four
  references to it exist, but one conclusion cites it twice, and counting references rather than
  conclusions inflated it. **Four findings tie at three** — F-22, F-57, F-67 and F-78. If any one
  of them is wrong, three conclusions move, and nothing on the board currently says so.

## 3 · What the data does NOT carry, so what must not be built

There is **no `impact` field, no `effort` field, no severity, no RICE, no priority**, anywhere in
these 32 items. So:

- **The impact-against-effort 2×2 cannot be drawn.** The `luma-competitor-analysis-pro` skill
  asks for one at Phase 7 and it is the conventional output of this kind of work. Building it
  would mean scoring nine recommendations myself and rendering my judgement with the visual
  authority of measurement. That is the failure this whole board exists to prevent, and it is
  refused here rather than quietly approximated.
- The honest substitute is **evidential base size**, which IS recorded: `len(sources)` per item,
  exact and mechanical, 1 to 6. It ranks recommendations by *how well supported* they are, never
  by how good they are. Those are different questions and the chart must say which one it answers.

`rests_on`, present on all nine recommendations, states the base in prose — *"one Verified
capture"*, *"four Verified findings"*, *"three findings of mixed confidence"*. Six of nine name a
number; three describe the base without one. Counting only where a number is written, and reading
`len(sources)` for the rest, keeps this transcription.

## 4 · The interactions the data supports, in order of what they are worth

### 4a. Linked highlighting — the evidence chain. **Build this first.**
Click or focus a recommendation, and every finding it rests on highlights. Click a finding, and
every downstream item that depends on it highlights. The relation is `sources`, it already
exists, and it resolves 100%.

This answers the only question a sceptical reader actually has — *why should I believe this?* —
without them having to hold 121 rows in their head. It is Flourish's **highlight** primitive,
observed across nine template families in round 5, and it is the one interaction on that list
this board has never used.

**It also makes the fragility visible.** Highlighting a recommendation that rests on one capture
lights one row; one that rests on four lights four. The difference is the finding.

### 4b. Evidential base per recommendation — a small chart, nine rows.
`len(sources)` per recommendation, 1 to 4, with `weakest_confidence` shown as a second channel
(6 verified, 3 qualified). Sorted by base size, it says plainly which recommendations are
well-founded and which rest on a single capture — three of the nine do.

The caption has to carry the disclaimer in bold: **this ranks evidence, not value.** A
recommendation resting on one capture may be the most valuable one on the board.

### 4c. Filter across every section at once.
Theme, competitor, or confidence class — applied to findings, pain points, insights and
recommendations simultaneously, so a reader can ask *"show me everything about Booking.com"* and
see the evidence and the conclusions together.

**Governance, and it is not routed around:** ADR-021 exempts chart marks from the membrane and
explicitly does **not** exempt *"a bespoke cross-filtering brush"*, which is product UI. So this
either reuses `cf-chip` (promoted L1, ADR-022) as its control vocabulary, or it needs a spec,
human approval and an ADR before it is built. Reusing `cf-chip` is the cheaper and more honest
path and is what I would do.

### 4d. Not adopted, and why
- **Search** — the index already has 121 rows and no search. Worth having, but it finds rows; it
  does not explain anything. Lower value than 4a.
- **Time slider** — no time dimension exists in this data. Named here only so its absence is a
  decision rather than an oversight.
- **The 2×2** — see §3. Refused.

## 5 · What I would build, in order

1. **4a linked highlighting**, driven by the existing `sources` graph. No new data, no scoring,
   and it turns 32 static cards into a navigable argument.
2. **A "what this rests on" chart** in Recommendations (4b), with the ranks-evidence-not-value
   caption.
3. **4c filtering**, only after settling the `cf-chip` reuse question, because the membrane
   applies to it.

## 6 · Two things the audit found that belong on the board regardless

- **71 of 113 findings support nothing downstream.** Either the argument is under-using its own
  evidence, or those findings are context rather than support. Both readings matter and neither
  is currently visible.
- **Four findings each carry three conclusions** — F-22, F-57, F-67, F-78. The board has four
  load-bearing points and names none of them. Linked highlighting makes each one visible on
  contact.
