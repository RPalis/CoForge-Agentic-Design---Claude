# Closing the gap — a plan to make this analysis decision-useful

**Date:** 2026-09-07 · **Status:** plan, nothing started.

## The diagnosis: three gaps, not one, and they do not have the same fix

| Gap | Measured | What it actually is |
|---|---|---|
| **A · Corroboration** | 9 of 25 conclusions rest on a single capture | A synthesis gap. The evidence may already exist |
| **B · Unused evidence** | 72 of 113 findings carry no conclusion | The same gap from the other end |
| **C · Coverage** | 25/136 stages · 8/119 states · 6/17 payment gate · 4/17 both browsers | The only one that genuinely needs new capture |

**The measurement that decides the order.** Every one of the 9 fragile conclusions has uncited
findings *on its own theme* already in the round — 22, 22, 22, 21, 6, 6, 6, 4 and 1 of them.

> **CALL 1 — Synthesis before capture.** Running round 2 first would add evidence to a pile we are
> already not using. A and B are cheap, fast, need no browser, and may strengthen a third of the
> board for nothing. C follows, aimed by what A and B expose.

## The reframe on coverage

136 is 8 stages × 17 competitors. Reaching 100% means roughly **111 more stage-captures** — two to
three times round 1, which produced 50 captures across three logged runs and about 560,000 tokens.

> **CALL 2 — The target is decision-sufficiency, not 100%.** "Complete coverage" is not a goal, it
> is an alibi for never shipping. The testable bar instead:
> **every recommendation rests on ≥2 independent captures, on ≥2 competitors, and every journey
> stage a recommendation touches is captured on the competitors that recommendation names.**
> That is checkable by script, and it is what "useful for decisions" actually means.

> **CALL 3 — States before stages.** Coverage is 18% on stages and **6% on states**. Zero error,
> no-results and offline states were captured anywhere in the entire round, and failure states are
> precisely where Luma proposes to differentiate. A stage captured in its happy path tells us
> little about a product built for people whose trip goes wrong. States are the higher-value buy.

## The bottleneck that governs the whole schedule

> **CALL 4 — Capture is serial and cannot be delegated.** No agent in this repository holds browser
> tools; only the main session can drive one (CLAUDE.md). Agents can plan, triage, synthesise,
> verify and critique **in parallel**; they cannot capture. Any plan that assumes fan-out capture
> is wrong. Everything else is parallelisable and should be.

## Phases

### Phase 1 — Corroboration sweep · no capture · **research-synthesizer**
For each of the 9 single-capture conclusions, search all 121 findings for corroborating evidence
and either cite it or record that none exists. Skill: `luma-competitor-analysis-pro`.
**Output:** updated `sources`, and a named list of conclusions that remain on one capture *after*
an honest search — those are the real research questions.
**Gate A.** research-synthesizer conclusions never graduate to auto (CLAUDE.md).

### Phase 2 — Triage the 72 · no capture · **research-synthesizer**, second pass
Classify every uncited finding as exactly one of: *supports an existing conclusion that failed to
cite it* · *supports a conclusion nobody drew* · *context, correctly uncited* · *method record*.
**Output:** the answer to whether the argument is under-using its evidence, with a count per class.
The second class is the interesting one — conclusions we have the evidence for and never wrote.

### Phase 3 — Aim the capture · **research-ops** + `ux-personas` + `ux-research-methods`
Turn Phases 1 and 2 into a prioritised capture list: exact competitor × stage × state, each row
naming **which decision it unblocks**. Nothing gets captured because it is missing; it gets
captured because a decision needs it.
`ux-personas` sets which stages carry the most anxiety for a first-time traveller — that is the
ranking key. `ux-research-methods` checks the prior question nobody has asked: whether competitor
capture can answer these questions at all, or whether some need real users.

### Phase 4 — Round 2 capture · **main session only, serial**
Standing rules, all already earned the hard way: dual browser as a matched pair (4/17 today,
CLAUDE.md); sweep vocabulary in the locale actually served (D-004, and the AA false zero);
consent walls recorded as blocked, never accepted; no payment, no account creation; never
transcribe review text (prohibition 2 — the ledger holds zero records).

### Phase 5 — Re-synthesis and rebuild · **research-synthesizer → dashboard-analyst**
Then **design-critic** and **a11y-checker** attack the result, and neither may be the agent that
built it.

### Phase 6 — The prioritised opportunity table · **`feature-prioritization`**
> **CALL 5 — This is how the impact/effort 2×2 gets built legitimately.** I refused to draw one
> because no `impact` or `effort` field exists and scoring nine recommendations myself would render
> my judgement with the authority of measurement. `feature-prioritization` applies a structured
> rubric with two weighted criteria instead of intuition. The scores then exist as data, produced
> by a stated method, and the chart becomes drawable. The refusal stands; the skill removes the
> reason for it.

## Two things that must happen BEFORE Phase 4, or round 2 repeats round 1's defects

> **CALL 6 — Write the theme taxonomy first.** C-045: 48% of the rows the audit can speak about are
> filed under a theme their own id contradicts, because themes were assigned ad hoc with no written
> definition. Capturing 111 more findings against the same undefined taxonomy reproduces the defect
> at three times the scale. **system-keeper** writes the definitions and a validator; the taxonomy
> is agreed before a single new capture is filed.

> **CALL 7 — Fix the capture schema's confidence field.** C-042 and C-044: the mandated
> Verified/Likely/Not-Verified tri-state never varied and never held, and 7 rows carry a pointer
> where a rating belongs. ART-024 §5.2 is amended before round 2 — to corroboration count and reach,
> per C-042's own conclusion — or round 2 produces another 100 rows of a field that says nothing.

## Skills, and what each is actually for

| Skill | Phase | Why |
|---|---|---|
| `luma-competitor-analysis-pro` | spine | Nine gated phases; carries the evidence ladder and the walkthrough limits |
| `ux-personas` | 3 | Which journey stages carry the most anxiety — the ranking key for capture |
| `ux-research-methods` | 3 | Whether competitor capture answers these questions at all |
| `customer-journey-mapping` | 5 | The pro skill's Phase 5 is journey comparison and it is the thinnest part of the round at 18% |
| `feature-prioritization` | 6 | Generates impact/effort by rubric so the 2×2 stops being my opinion |
| `ux-heuristics-review` | 5 | Gives pattern analysis a defensible frame rather than impressions |
| `persuasive-ux` | 5 | White space in *behaviour*: where do competitors fail to move a low-confidence user |
| `accessibility` | 4–5 | European Accessibility Act is a named Luma risk; incumbent weakness is strategic, not hygiene |

Not used: `empathy-mapping` (no user research exists to synthesise), `ux-benchmark` (a scored
rubric is a different instrument from this qualitative round), `ux-competitor-analysis` (the
vendor-neutral version of a skill we already have in its Luma form).

## Agents

| Agent | Job | Constraint |
|---|---|---|
| **research-synthesizer** | Phases 1, 2, 5 | Never graduates to auto; every conclusion is Gate A |
| **research-ops** | Phase 3 capture plan | Does not make design changes |
| **main session** | Phase 4 capture | The only holder of browser tools; serial |
| **dashboard-analyst** | Phase 5 rebuild | Owns the dataviz layer |
| **design-critic** | Phase 5 attack | Advisory; may not review what it built |
| **a11y-checker** | Phase 5 attack | Holds Write but no Edit and no Bash |
| **system-keeper** | Calls 6 and 7 | Owns validators and schemas; must not be the agent that clears its own check |
| **evidence-clerk** | standby | Only if a real user quote ever enters. The ledger holds zero records and prohibition 2 is absolute |

> **CALL 8 — I would not route this through the orchestrator.** It is built to dispatch one agent
> per turn against a routing table. This plan is one serial bottleneck with parallel work either
> side of it, and the sequencing depends on findings that do not exist until Phase 2 returns.
> Dispatch stays in the main session.

## What "done" looks like, and it is checkable

1. Every recommendation cites ≥2 independent captures on ≥2 competitors — **script-checkable**
2. Every journey stage a recommendation names is captured on the competitors it names — checkable
3. Error, no-results and offline states captured on at least the 6 competitors that carry a
   recommendation — checkable
4. The theme taxonomy is written, and a validator rejects a finding filed against no definition
5. Confidence is a field that varies
6. Gate A granted on the round, by a person

> **CALL 9 — Nobody quotes this round externally until item 6.** Both ART-026 versions are `draft`
> and neither has been approved. The board is honest about its limits on its face, which makes it
> safe to reason with internally and not yet safe to present as a finding about the market.
