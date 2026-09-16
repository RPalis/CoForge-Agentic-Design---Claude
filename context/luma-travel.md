# Luma Travel — Project Context (RAG)

> Rolling workstream context. Updated at the end of each define-phase run.
> Load this file to get the full picture without reading individual artifact directories.
> Last updated: 2026-09-15

---

## Workstream state

| Item | Status |
|---|---|
| Build stage | Stage 0–2 complete — L1 foundations unblocked |
| Design Loop phase | Phase 2 Define (in progress) |
| Corpus | SYNTHETIC — desk research + 40 synthetic interviews, no primary research |
| Gate A | Not yet signed on any define-phase artifact |
| Evidence ledger | Zero entries — ADR-024 in force |
| Journey maps | **Done — ART-038 v3**, 4 of 14 personas (P09 Halina, P14 Bernard, P04 Reuben, P12 Jaden), interactive, dataviz overview. v1 (14-persona draft, trimmed) and v2 (opportunities unbenchmarked) both superseded — see Artifact index. |
| Opportunity benchmark | ART-039 — market precedent check on ART-038's opportunity cells, one honest non-finding (Bernard's exact failure mode uncorroborated) |
| Figma Make package | ART-040 — journey-map package, same pattern as ART-036 |

---

## Corpus summary

**ART-029** — 40 synthetic interviews, rotation lattice, 14 personas × 6 themes, 0 coverage gaps.
**ART-030** — 14 desk-research archetypes across 5 segments. Built from open sources: forums, regulators, trade bodies, peer-reviewed work. Not recruited participants.
**ART-031** — Shareable ZIP package of the synthetic interview corpus.

---

## The 6 overturned findings (ART-030 §1)

Every problem statement, journey map, and HMW must check against these before framing.

| # | Finding | Anti-framing |
|---|---|---|
| 1 | Planning is the pleasure — multi-leg ground transport is the pain | Don't frame as "removing planning stress" |
| 2 | The dreaded moment is the return home airport, not destination arrival | Don't optimise arrival experience as the primary concern |
| 3 | The "needs help booking" persona is 18–34, not old | Don't frame help-seeking as an accessibility or age issue |
| 4 | The failure mode is near-miss completion, not digital exclusion | Don't simplify for "less digitally confident" — design against the almost-right action |
| 5 | For disabled travellers, research is a gate before booking | Don't improve the booking flow — improve what comes before it |
| 6 | Nobody is asking for one app — tool plurality is deliberate | Don't frame as "one place for everything" |

---

## Segment map (ART-030)

| Segment | Personas | Defining characteristic |
|---|---|---|
| Premise-rejectors | P01 P02 P03 | Planning is a pleasure, or a package, or deliberately multi-tool. The product premise conflicts with their mode. |
| Designated planners | P04 P05 | Organises for others. Pain is being the single point of knowledge, not interface friction. |
| Families | P06 P07 P08 | Budget stated as a trip total. Return leg is the dreaded moment. |
| Disabled / assisted | P09 P10 P11 | Research is a gate before booking. Published info is distrusted. Abandonment fires before the funnel. **Highest-stakes segment.** |
| First-timers / near-miss | P12 P13 P14 | First-timers: opacity of physical process, not digital. Near-miss: almost-successful, not excluded. |

---

## Full persona index (ART-030)

| ID | Name | Age | Role | Location | Segment | Pain count |
|---|---|---|---|---|---|---|
| P01 | Marianne | 67 | Retired solicitor | Yorkshire | Premise-rejector | 1 |
| P02 | Tomas | 45 | Structural engineer | Manchester | Premise-rejector | 0 |
| P03 | Aisling | 34 | Hospital pharmacist | Dublin | Premise-rejector | 1 |
| P04 | Reuben | 52 | Quantity surveyor | Cardiff | Designated planner | 3 |
| P05 | Nkechi | 38 | Teacher | Birmingham | Designated planner | 2 |
| P06 | Siân | 41 | Part-time nurse | Swansea | Family | 2 |
| P07 | Deniz | 31 | Warehouse supervisor | Leicester | Family | 2 |
| P08 | Fabio | 27 | Chef | Naples | Family | 2 |
| P09 | Halina | 58 | Wheelchair user | Kraków | Disabled / assisted | 4 |
| P10 | Oskar | 24 | Autistic | Gothenburg | Disabled / assisted | 3 |
| P11 | Ruth | 74 | Low vision | Leeds | Disabled / assisted | 3 |
| P12 | Jaden | 19 | Apprentice | Plymouth | First-timer | 2 |
| P13 | Priya | 22 | Student | London | First-timer | 2 |
| P14 | Bernard | 81 | Retired | Ealing | Near-miss | 3 |

---

## Problem statements — 4 priority personas (ART-034)

Selection criteria: highest design-risk or highest unmet need per ART-030 §1.5 and overturned findings.

### P09 Halina — Disabled / Assisted
**AS-IS:** Three in five disabled travellers avoid venues without published access info. Halina verifies by telephone. Abandonment fires before the funnel.
**HMW:** How might we make access verification instant and trustworthy so Halina can commit to a venue with the same confidence as a non-disabled traveller?
**Anti-HMW:** NOT "how might we make booking easier" — she never reaches booking.
**Design implication:** Accessibility info must surface in search results, before intent is declared.
**Overturned finding:** #5 `[ART-030 § Overturned findings]`

### P14 Bernard — Near-miss
**AS-IS:** Printed return boarding passes instead of outbound; charged £55 each. Digitally almost successful, not excluded.
**HMW:** How might we design commitment moments so the wrong action is visually impossible to mistake for the right one under time pressure?
**Anti-HMW:** NOT "how might we simplify for elderly users" — Bernard is digitally capable.
**Design implication:** Error prevention before error recovery. Wrong and right actions must be perceptually distinct at the moment of commitment.
**Overturned finding:** #4 `[ART-030 § Overturned findings]`

### P04 Reuben — Designated Planner
**AS-IS:** Organises travel for a group; becomes the single point of knowledge. Post-trip resentment follows.
**HMW:** How might we distribute itinerary ownership across a group so the designated planner is not the single point of failure?
**Anti-HMW:** NOT "how might we make planning faster" — speed is not the pain; sole knowledge-holding is.
**Design implication:** The itinerary has an audience beyond the planner. Output must be shareable and actionable by people who did not plan the trip.
**Source:** `[ART-030 § Designated Planner]`

### P12 Jaden — First-timer
**AS-IS:** Books via a travel professional not because of digital friction but because the physical airport process is opaque.
**HMW:** How might we surface the airport sequence as primary content before Jaden arrives?
**Anti-HMW:** NOT "how might we simplify for less digitally confident users" — the opacity is physical, not digital.
**Design implication:** Pre-trip process explainers are not onboarding — they are the product for this persona.
**Overturned finding:** #3 `[ART-030 § Overturned findings]`

---

## Artifact index — luma-travel workstream

| ART | Type | Title | Status |
|---|---|---|---|
| ART-029 | interview-analysis | Synthetic corpus pipeline run — 40 interviews, 6 themes, rotation lattice | validated |
| ART-030 | persona | Research-grounded persona set — 14 archetypes, 5 segments | validated |
| ART-031 | interview-analysis | Luma interviews shareable package (ZIP) | validated |
| ART-032 | insight-report | Luma synthetic research report | draft |
| ART-033 | dashboard | Persona set dashboard — 14 archetypes visualised | draft |
| ART-034 | dashboard | Problem statements — P09 P14 P04 P12 | draft |
| ART-035 | persona | Priority-four persona set (P09/P14/P04/P12), selection criteria stated | draft |
| ART-036 | handoff-spec | Figma Make package for ART-035 — README/manifest cite a `04-figma-make-prompt.md` that isn't actually in the zip (defect found 2026-09-15, not yet fixed) | draft |
| ART-037 | insight-report | User-research governance report, Phase 5 | draft |
| ART-038 v3 | journey-map | Priority-four journey maps, 7 stages, interactive (sparklines + heatmap). v1→v2→v3, each superseded-with-reason in its own manifest, none deleted | draft |
| ART-039 | competitive-benchmark | Opportunity-cell market-precedent check for ART-038 | draft |
| ART-040 | handoff-spec | Figma Make package for ART-038 v3 | draft |
| ART-041 | insight-report | Journey-map task governance — 85 tool calls, 0 subagents, 1 defect found (ART-036), 0 Gate A signatures | draft |

---

## Design decision worth preserving — two-tier journey-map citation

Introduced in ART-038 v2, carry forward to every future journey map in this workstream: **pain** and
**opportunity** are different evidentiary claims and get different citations. Pain cites `[ART-030 §
persona]` — evidence about the persona. Opportunity cites the relevant competitive-benchmark artifact
(`[ART-039 § persona]` here) — evidence about the market. A pain being real does not make a proposed fix
precedented; stating them with one shared, uncited "Opportunities" column (as ART-038 v1 did) hides that gap.
Where no market precedent exists (ART-038's Bernard cell), say so — an evidenced absence, not a filled-in
guess.

---

## Next-run priming — options, not a decision

Journey maps are done for the priority four. `.ai/index.md`'s Define-stage type list still has unused types
for this persona set: `empathy-map`, `service-blueprint`, `jtbd`, `opportunity-map`, `prioritization`. Phase 3
Ideation (IA/site map, then sketches) is also open once Define is judged sufficient. No orchestrator run has
chosen between these yet — recorded as open, not defaulted:

- **Service blueprint** for P09 Halina — the highest-stakes, most cross-touchpoint persona (venue, hotel,
  airline, aggregator all appear in her journey) would show the backstage handoffs a journey map can't.
- **Opportunity map** — ART-038/ART-039 together already have 4 evidenced opportunities; a map would force
  relative prioritisation, which neither artifact currently does.
- **Phase 3 IA/site map** — if Define is judged sufficient without the remaining define-stage types, this is
  the next phase per the routing table.

Whichever is chosen: load this file first, then ART-038 v3 + ART-039 for the priority-four persona detail, not
ART-030 directly — the two-tier citation above depends on reading opportunity claims from ART-039, not
re-deriving them from ART-030.

---

## Claim format reminder (ADR-017)

- `Evidenced [ART-030 § Section]` — measurement form, resolves to ART-030 and a real section heading
- `Evidenced [ART-nnn § Section]` — measurement form for any registered artifact
- `Evidenced [E-nnn]` — testimony form, resolves to `research/evidence-ledger.json` — **currently zero entries; do not mint**
- `Inferred` — must name what it is inferred from
- `Assumption` — collected in a visible Assumptions block
