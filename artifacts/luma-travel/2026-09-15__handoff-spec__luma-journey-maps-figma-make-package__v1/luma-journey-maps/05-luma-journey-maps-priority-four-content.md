# Luma Travel — Priority-Four Journey Maps (content reference)
**ART-038 v3 · Define Phase · Synthetic Corpus · 2026-09-15**

> SYNTHETIC CORPUS — DESK RESEARCH ONLY — NO LINE BELOW IS A USER QUOTE — ART-038

One map per priority persona (same four as ART-035: P09, P14, P04, P12), 7 stages each. Pain cites
`[ART-030 § persona]`; Opportunity cites `[ART-039 § persona]` — deliberately different citations, because a
pain being real does not make a proposed fix precedented. Evidence ledger holds zero entries; ADR-024 in force.

Stages, fixed order: **1 Inspiration & Dreaming · 2 Research & Compare · 3 Book · 4 Pre-departure ·
5 Airport (outbound) · 6 At Destination · 7 Return & Post-trip**

---

## P09 · Halina — Highest-stakes segment, 4 pains
58 · Powered wheelchair user · Kraków · Segment: **Disabled / Assisted** (coral marker)

Research is a gate before booking, not a funnel step. ~3 in 5 abandon a venue with no published access info.
*Evidenced [ART-030 § Disabled and assisted travellers]*

Emotion curve: ↓ ↓ → ↓ ↓ → ↓ — critical at stage 1, low at 2/4/5/7.

| | 1. Inspiration & Dreaming | 2. Research & Compare | 3. Book | 4. Pre-departure | 5. Airport (outbound) | 6. At Destination | 7. Return & Post-trip |
|---|---|---|---|---|---|---|---|
| **Goal** | Decide whether a destination is even reachable | Confirm the room and route will actually work | Commit only once the gate is cleared | Confirm the assistance request survived the booking | Get through with the chair intact | Confirm assistance arrives as promised | Get home with the chair undamaged |
| **Actions** | Screens out venues with no published access info | Requests photos of room, bathroom, entrance; verifies by phone | Books only after under-bed clearance confirmed in cm | Rings the airline 48 hours out to re-confirm assistance | Photographs chair from every angle at handover | Checks assistance shows up as booked | Re-verifies assistance for the return leg |
| **Thoughts** | No published info means assume inaccessible | The website can't be trusted — she has to hear it from someone | The hoist has to fit, no exceptions | Did the request actually stick to the booking | Documenting the chair now, in case of damage later | Watching for whether the promise holds | Doing the whole check again for the way home |
| **Emotion** | ↓ | ↓ | → | ↓ | ↓ | → | ↓ |
| **Pain points** | Unpublished access information | Venue websites misleading; verification burden | — | Assistance request not confirmed to have survived booking | Equipment damage risk | — | Assistance ending before the journey does |
| **Opportunities** | Structured, verified access info at the point venues are shortlisted — built on the protocol accessibility guides already publish (door widths, hoist clearance, room photos), not invented from nothing. *[ART-039 § Halina]* | One verified-access source that merges mainstream filterable breadth with specialist verified depth — today a traveller gets Booking.com's 18 filterable accessibility attributes (self-reported) or a specialist's measured, photographed rooms (narrow inventory), never both. *[ART-039 § Halina]* | — | Visible confirmation that an assistance request is attached and live | Damage-claim path built around her own handover photos | — | Assistance confirmation that covers the return leg by default |
| **Evidence** | Evidenced [ART-030 § What the research overturned] | Evidenced [ART-030 § Halina] | Evidenced [ART-030 § Halina] | Evidenced [ART-030 § Halina] | Evidenced [ART-030 § Halina] | Inferred [ART-030 § Halina] | Inferred [ART-030 § Halina] |
| **Confidence** | High | High | Medium | High | High | Medium | Medium |

**Design note:** The abandonment this describes fires before any funnel a product team would instrument. Fix
the gate at Inspiration & Research, not the booking flow. *Evidenced [ART-030 § Disabled and assisted
travellers]*

**Grounding caveat:** Least grounded register in ART-030. Regulator and market evidence, thin first-person
voice; Reddit blocked by policy throughout. Treat as directional until primary research is run.
*[ART-030 § Bias controls]*

---

## P14 · Bernard — Near-miss, overturned finding #4
81 · Retired · Ealing · Segment: **Near-miss** (ink marker)

Printed the return boarding passes instead of the outbound pair, charged £110 at the desk. Digitally almost
successful, not excluded. *Evidenced [ART-030 § First-timers and the near-miss]*

Emotion curve: ↑ ↑ → → ↓ → → — critical (!) at stage 5, positive (★) at stage 1.

| | 1. Inspiration & Dreaming | 2. Research & Compare | 3. Book | 4. Pre-departure | 5. Airport (outbound) | 6. At Destination | 7. Return & Post-trip |
|---|---|---|---|---|---|---|---|
| **Goal** | Plan the next trip in detail, as always | Rule out connections — nonstop only | Book independently online, as he's done for years | Build his usual paper and digital trip books | Check in and print the right documents | Keep up his usual pace — 15k steps a day | Get home without a repeat of the misread |
| **Actions** | Fifty years of travel experience — starts planning as usual | Filters out any route with a connection | Books all flights online independently | Builds detailed paper and electronic trip books | Checks in online, prints boarding passes | Walks extensively, self-guided | Rechecks documents more carefully after last time |
| **Thoughts** | Still does this the way he always has | Connection anxiety — nonstop only, no exceptions | Confident using digital tools he's used for years | Detail is what keeps a trip under control | Printed the return pair instead of outbound — didn't notice | Not digitally excluded, still capable and active | One misread cost £110 — won't let it happen again |
| **Emotion** | ↑ | ↑ | → | → | ↓ | → | → |
| **Pain points** | — | — | — | — | Near-miss completion — printed wrong document pair, charged £110 | — | Interfaces that punish a single misread |
| **Opportunities** | — | — | — | — | Make right vs. wrong document pair perceptually impossible to confuse — an open problem: wallet-pass adoption fixes scanning failures but not a confidently-wrong document choice, and no competitor solves it either (zero High-confidence travel-day cells market-wide). *[ART-039 § Bernard]* | — | Post-error recovery path that doesn't default to a full-price charge — return is the least-built stage in the market, Unknown for 5 of 6 competitors studied, so this is a confirmed vacancy, not an adaptation of an existing pattern. *[ART-039 § Bernard]* |
| **Evidence** | Inferred [ART-030 § Bernard] | Evidenced [ART-030 § Bernard] | Evidenced [ART-030 § Bernard] | Evidenced [ART-030 § Bernard] | Evidenced [ART-030 § Bernard] | Evidenced [ART-030 § Bernard] | Evidenced [ART-030 § Bernard] |
| **Confidence** | Low | High | High | High | High | Medium | Medium |

**Design note:** Bernard is not the person who can't start — he is the person who almost finished. At
commitment moments (print, confirm, submit) wrong and right must be perceptually impossible to confuse.
*Overturned finding #4 [ART-030 § What the research overturned]*

---

## P04 · Reuben — 3 pains, highest outside disabled segment
52 · Quantity surveyor · Cardiff · Segment: **Designated planner** (ink marker)

Organised 12 nights for 8 people across 3 generations. Was the single point of knowledge; blamed after.
*Evidenced [ART-030 § Designated planners]*

Emotion curve: → → ↓ ↓ → → ↓ — low at stage 3/4, critical (!) at stage 7.

| | 1. Inspiration & Dreaming | 2. Research & Compare | 3. Book | 4. Pre-departure | 5. Airport (outbound) | 6. At Destination | 7. Return & Post-trip |
|---|---|---|---|---|---|---|---|
| **Goal** | Find something that works for 3 generations | Research options across 8 people's needs | Book for the whole group | Get everyone aligned before departure | Shepherd the group through the airport | Keep the group's plan running | Come home without being blamed |
| **Actions** | Starts researching for the whole group | Cross-checks options against 8 people's constraints | Books accommodation and transport for the group | Circulates a detailed itinerary; fields "what's the plan?" for weeks | Coordinates 8 people through check-in | Remains the group's single point of contact on-site | Absorbs blame for pace and cost after the fact |
| **Thoughts** | Someone has to plan this properly | Weighing what will actually work for everyone | Committing on behalf of people who haven't decided | He sent the document — why is he still fielding questions | Responsible for more than just himself | Still the one who knows the plan | Did the work, got the blame |
| **Emotion** | → | → | ↓ | ↓ | → | → | ↓ |
| **Pain points** | — | — | — | Single point of knowledge; group coordination | — | — | Post-trip resentment for pace and cost |
| **Opportunities** | — | — | — | A shareable, read-only plan the group can act on without adopting a new app — every named group-planning competitor builds for collaborative editors (live sync, voting, shared editing), not passive recipients; the gap isn't a shareable plan, it's one requiring zero adoption from the other 7 people. *[ART-039 § Reuben]* | — | — | Attribute decisions to the group's own choices, not just his |
| **Evidence** | Inferred [ART-030 § Reuben] | Inferred [ART-030 § Reuben] | Inferred [ART-030 § Reuben] | Evidenced [ART-030 § Reuben] | Inferred [ART-030 § Designated planners] | Inferred [ART-030 § Reuben] | Evidenced [ART-030 § Reuben] |
| **Confidence** | Low | Medium | Medium | High | Low | Medium | High |

**Design note:** Speed is not Reuben's pain — he does the planning willingly. The pain is that the knowledge
stays in his head. Output format must be actionable by people who did not plan the trip.
*Evidenced [ART-030 § Designated planners]*

---

## P12 · Jaden — Overturned finding #3
19 · Apprentice · Plymouth · Segment: **First-timer** (ink marker)

First flight. Questions were mechanical, not emotional. Booked through an agency on college recommendation.
*Evidenced [ART-030 § First-timers and the near-miss]*

Emotion curve: → ↓ → → ↓ → → — low at stage 2 and stage 5.

| | 1. Inspiration & Dreaming | 2. Research & Compare | 3. Book | 4. Pre-departure | 5. Airport (outbound) | 6. At Destination | 7. Return & Post-trip |
|---|---|---|---|---|---|---|---|
| **Goal** | First flight — excited but unsure what's involved | Understand the physical process before booking | Book with someone accountable if it goes wrong | Know what documents he actually needs | Reach the gate without uncertainty | Enjoy the trip he's never done before | Get home the same way he came |
| **Actions** | Excited about the idea of flying for the first time | Asks mechanical questions — bag, gate, passport control | Books through the agency his college recommended | Checks what documents and process apply to him | Works through security, gate-finding, boarding for the first time | First-time traveller experiencing the destination | Repeats the airport process, now once familiar |
| **Thoughts** | Never done this before | Does my bag go through, where do I find the gate | Wants someone accountable, not just a better interface | Is passport control the same as immigration | Working out the physical sequence as he goes | Made it — first flight done | Knows the process now, less uncertain |
| **Emotion** | → | ↓ | → | → | ↓ | → | → |
| **Pain points** | — | Document uncertainty | — | — | Airport process opacity | — | — |
| **Opportunities** | — | A plain end-to-end explainer covering the seam TSA's own free MyTSA app leaves open — it already covers checkpoint prep, wait times and what's allowed, so duplicating that would be wasted; passport control/immigration and post-security wayfinding aren't covered by it at all. *[ART-039 § Jaden]* | — | — | Step-by-step guidance for the specific seam a first flight exposes — security to passport control to gate, as one sequence instead of three separately-owned pieces. *[ART-039 § Jaden]* | — | — |
| **Evidence** | Inferred [ART-030 § Jaden] | Evidenced [ART-030 § Jaden] | Evidenced [ART-030 § Jaden] | Evidenced [ART-030 § Jaden] | Evidenced [ART-030 § Jaden] | Inferred [ART-030 § Jaden] | Inferred [ART-030 § First-timers and the near-miss] |
| **Confidence** | Low | High | High | High | High | Low | Low |

**Design note:** The opacity is physical and procedural, not digital. Jaden is 19 and digitally capable —
pre-trip process explainers are the primary product for this persona, not onboarding content.
*Overturned finding #3 [ART-030 § What the research overturned]*

---

## Overview data (for the dataviz section)

### Pain × confidence, all 4 personas × 7 stages

| Persona | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| P09 Halina | H ● | H ● | M | H ● | H ● | M | M ● |
| P14 Bernard | L | H | H | H | H ● | M | M ● |
| P04 Reuben | L | M | M | H ● | L | M | H ● |
| P12 Jaden | L | H ● | H | H | H ● | L | L |

`●` = evidenced pain point at that stage. Letter = confidence (H/M/L).

---

> SYNTHETIC CORPUS — desk research only, no primary research conducted — no line above is a user quote —
> ART-038 v3 · sources: ART-030 · ART-029 · ART-035 · ART-039 · ADR-024 · ADR-021 (dataviz layer) · Gate A not
> yet signed · produced 2026-09-15
