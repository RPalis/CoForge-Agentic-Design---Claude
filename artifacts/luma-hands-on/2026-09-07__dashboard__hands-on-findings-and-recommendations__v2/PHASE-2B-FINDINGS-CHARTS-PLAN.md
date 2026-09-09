# Phase 2b — data visualisation for the four findings threads

**Status:** DRAFT plan, 2026-09-07. Nothing built yet.
**Scope:** Ranking axes & effort · Loyalty & the first-time traveller · The disruption gap ·
Business goal 2. These are the four `#findings` subsections that currently carry prose cards
and no chart.

## The rules this plan inherits, and one it adds

Learned building Phase 2 and rebuilding `ch-nulls` three times:

1. **Encode the answer, not the method.** `ch-nulls` failed twice because it drew how many
   links we checked — a fact about us — instead of whether a route exists.
2. **Never unit-chart a zero — but a zero inside a visible whole is fine.** Zero has no area,
   so 367 dots could never show it. *0 of 20 sort axes* is different: the 20 has area, and the
   empty part of it is legible. This is the distinction that decides three of the charts below.
3. **The reader's question is the chart's own title**, drawn inside the SVG.
4. **Label the unit inside the drawing**, on a leader, where the eye already is.
5. **Draw the counter-case.** Omitting American Airlines made an absence look universal. Every
   chart below must include the products that do the opposite.
6. **No categorical hue** — position, length, and step on the single gray ladder (C-036,
   ADR-021 item 1 still owed).
7. **Colour is never the sole channel** (WCAG 1.4.1 Level A).
8. **Verify on the rendered DOM, and declare structural elements in the markup.** Build-time
   arithmetic passed while all 59 matrix cells were dark-on-dark.

---

## 1 · Ranking axes & effort — the richest of the four, three charts

### 1a. The vertical split — where effort is ranked and where it is not
The round's most important correction (M1), currently carried only in prose.

| vertical | product | axes | of which effort/convenience |
|---|---|---|---|
| Accommodation | Booking.com | 11 | **0** |
| | Expedia | 6 | **0** |
| | Google hotels | 3 | **0** |
| | Airbnb | 0 | — no sort control at all |
| Activities | Tripadvisor | 0 | — no sort control at all |
| Flights | Google Flights | 6 | **4** (Departure time, Arrival time, Duration, Emissions) |
| | Kayak | 3 | **2** (Shortest duration; Best = composite) |
| Rail | Trainline | — | leads with 2 effort criteria *before* price |

**Encoding:** segmented horizontal bars, grouped by vertical, dark segment = effort axes.
The top group has no dark anywhere; the bottom group does. Rule 2 applies and permits it: the
zero sits inside a bar that has length.
**Source:** F-09 · F-20 · F-25 · F-35 · F-43 · F-69 · F-92 · MATERIAL_CORRECTION_to_F09_F20_F25.

### 1b. Control against explanation — the empty quadrant
F-75's inversion, and the strongest single chart available anywhere on this board, because it
draws an **unoccupied position** rather than a ranking.

| product | sort axes | what it publishes about its ranking |
|---|---|---|
| Booking.com | 11 | commission influences ranking; criteria not named |
| Google Flights | 6 | one line — "ranked based on price and convenience" |
| Expedia | 6 | nothing observed |
| Kayak | 3 | each paid placement marked, advertiser named |
| Tripadvisor | 0 | criteria named inline on the results surface |
| Airbnb | 0 | ~10,800 characters, five weighted factors, linked from results |

Points fall on a descending diagonal. **The corner that is few-axes-AND-fully-explained is
empty** — and F-75 says so in words: *control and explanation are being treated as
alternatives, and nobody offers both.*

**The honesty risk, named:** the vertical axis is ordinal and partly a judgement. Mitigation —
it is **not** scored. It is an ordered categorical with six levels, each level being the
verbatim description already in the capture, ordered by a rule stated on the chart
(nothing < one line < criteria named < paid placement marked < criteria named inline <
weighted factors published). One measured anchor exists (Airbnb ~10,800 chars) and is labelled
as the only measured point. If dashboard-analyst cannot defend the ordering from the captures
alone, **this chart is not drawn.**
**Source:** F-75 · F-84 · F-30 · F-46.

### 1c. The three units of effort
F-100: effort is measured in **time** (flights, rail), **carbon** (Google Flights, sortable),
and **calories** (Citymapper) — and in **no unit at all** in accommodation and activities.
**Encoding:** a small typology strip, three occupied cells and two empty ones. Rule 2 permits
it — the row exists, the cell is empty.

---

## 2 · Loyalty & the first-time traveller — one ladder chart

Two complete ladders are captured with exact thresholds. This is the chart I rejected a span
chart for in round 4 (R4-01: span charts "give no information on the data points between the
minimum and maximum" — and here the middle rungs are the entire finding).

- **Expedia One Key:** Blue 0–4 trip elements (1% OneKeyCash) → Silver 5–14 (2%) →
  Gold 15–29 (3%) → Platinum 30+ (4%). Member Prices apply independent of tier.
- **Booking.com Genius:** Level 1 grants 10% immediately; **priority support at 15 completed
  bookings in 2 years.**

**Encoding:** one shared horizontal axis, *bookings or trip elements completed*, 0 → 30+.
One row per programme, tier boundaries as marks, each rung labelled with what it grants. A
heavy rule at **0**, labelled *"the traveller this product is designed for is standing here."*
The finding is the **distance** from that rule to the rung that grants help.

**What the chart must not overstate:** the entry tier is not empty. At zero you get 10%
(Booking) and 1% (Expedia). The chart must show that you are given the floor and not nothing —
what is gated is the *best rate* and the *help*, not participation. Drawing zero as "nothing"
would misrepresent the third card in this thread.
**Source:** F-01 · F-18 · Expedia One Key tier_structure · the 4-of-4 first-timer null.

---

## 3 · The disruption gap — relocate, then extend

The route diagram already built (`ch-nulls`) **belongs in this thread** and currently sits in
the Findings section intro, disconnected from the four cards it explains. Move it.

**Then add one small second route, same encoding, so it reads instantly:** Booking.com holds
the disruption relationship in one place and disclaims it in another —
*flights sold via a third-party aggregator → no liability*; *airport transfers, where it holds
the supplier relationship → compensation and assistance*. Two lines, one dead end, one arrival,
inside the same product. That is the sharpest available statement of the round's market-structure
finding, and it needs no new data.
**Source:** F-56 · F-107 · F-113 · Booking.com Terms A19 / transfers.

---

## 4 · Business goal 2 — one strip, and an explicit n=1

One card, and it is the strongest evidence business goal 2 is unsolved rather than unclaimed:
Airbnb holds stays, experiences and services under one account, and **moving from an
accommodation search to Experiences drops the trip's dates entirely.**

**Encoding:** a "what survives the handoff" strip. What the traveller is holding on the left
(destination · dates · guests), the boundary in the middle, what is still held on the right
(destination) — with *dates* visibly dropped at the crossing.

**Mandatory caveat drawn on the chart:** this is **one observation on one product**. The chart
must not read as a survey. A single-case chart carrying a survey's visual authority is the
failure mode here, and it is the same failure as omitting American Airlines from `ch-nulls`.
**Source:** the Airbnb trip-as-an-object capture.

---

## Who does what

**CORRECTED 2026-09-07 — I was wrong about this, and the client caught it.** I checked
`.claude/skills/` in the project directory, found it empty, and concluded no skills existed.
Skills are installed at **account level**, not in the repo. Four are enabled and relevant:

| Skill | Use |
|---|---|
| **`luma-competitor-analysis-pro`** | **The one being run.** Nine gated phases; phase six is white-space analysis, which is exactly what chart 1b draws |
| `luma-competitor-analysis` | The earlier, single-pass version of the same method |
| `ux-competitor-analysis` | Vendor-neutral equivalent |
| `ux-benchmark` | Scored rubric — a different instrument, not this job |

Checking one directory and declaring a capability absent is the same error this whole board is
about: **absence of evidence reported as a finding.** Logged here rather than quietly fixed.

### How the four charts map onto the skill's phases

The skill reframes the work, and the mapping is close enough that it should govern the build:

| Chart | Skill phase | Why it lands there |
|---|---|---|
| 1a vertical split | **Phase 3 — Feature inventory** | It *is* a feature matrix: axes per product, normalised across competitors |
| 1b empty quadrant | **Phase 4 — Pattern analysis**, feeding **Phase 6** | The skill: *"Contradiction usually means the problem is genuinely unsolved."* Control and explanation are treated as alternatives and nobody offers both — that is a Phase 4 contradiction and a Phase 6 category-2 white space (poorly served, demand already demonstrated) |
| 1c three units of effort | Phase 4 — convergent/emerging | Every vertical that can quantify effort does; the ones that cannot ignore it |
| 2 loyalty ladder | **Phase 6 — category 3, structurally excluded** | The skill names this exact case as the template for good white space: the model itself prevents serving a first-timer, so an incumbent cannot follow without breaking it |
| 3 disruption routes | **Phase 5 — journey comparison, seams** | The skill: seams between stages are where confidence collapses and are systematically under-designed |
| 4 business goal 2 | **Phase 5 — a broken handoff** | Literally a seam: state dropped crossing a product boundary |

### Gate check performed before entering Phase 3

| Phase | Required artefact | Status |
|---|---|---|
| 1 | Benchmark Plan | ✅ ART-024 |
| 2 | Verified Competitor Profiles | ⚠️ **ART-025 exists at the highest tier and the lowest breadth.** All 50 captures are Tier 1 (hands-on) or Tier 2 (first-party documentation) on the skill's ladder — no third-party, no vendor-marketing source anywhere in the round. But journey coverage is 25 of 136 stages, so no profile is complete |
| 3–9 | — | not started |

**Consequences of that gate reading, stated rather than skipped:**
- Phases 3, 4 and 6 are runnable on what exists, with holes marked.
- **Phase 5 (journey comparison) is thin.** 18% stage coverage means most of the eight stages
  carry no evidence at all. It will be reported as thin, not filled in.
- **7 of 50 captures record no `surface`**, which CLAUDE.md requires for every capture. A gap in
  the method record; owed.
- **One quarantined prior claim is refuted by round 1:** *"no competitor consistently explains its
  recommendations."* Airbnb publishes ~10,800 characters naming five weighted factors and links to
  it from the results page; Tripadvisor names its criteria inline. The claim does not survive, and
  its refutation is the substance of chart 1b.

| # | Agent | Tools | Job | Why this one |
|---|---|---|---|---|
| 1 | **dashboard-analyst** | Read, Write, Bash | Specify and build 1a, 1b, 1c, 2, 4 in `charts.py`; extend the CSV tables | The routing table's owner for data visualisation. Best track record on this artifact: it found C-042 and it corrected three of my overstated Song & Szafir claims by fetching the paper |
| 2 | **main session (me)** | browser | Wire into `build-dashboard.py`, render, screenshot, verify on the DOM | **No agent holds browser tools** (CLAUDE.md). Every one of the four defects today was found by looking at the rendered page. This step cannot be delegated |
| 3 | **design-critic** | Read, Write | Adversarial pass on the assembled board | **ADR-021 item 4 requires it and it has never run on ART-026.** Advisory, not auto — a confident wrong critique steers bad revisions |
| 4 | **a11y-checker** | Read, Write | WCAG pass on the chart layer | Also never run on ART-026. Auto from day one; small blast radius; holds no Edit and no Bash so it cannot alter what it audits |
| 5 | **system-keeper** | Read, Write, Bash, Grep | Extend `verify-charts.mjs` for the new mark types | Owns `validation/` and the checks. **Must not be the same agent that built the charts** — the author is the one party who cannot attack their own check (C-021, C-024) |

**Not used, and why:** *research-synthesizer* — these charts encode findings that already exist;
drawing a new conclusion is not in scope. *token-keeper* — the dataviz token group (ADR-021
item 1) stays owed, because none of these five charts needs categorical hue. *brand-director*,
*screen-producer*, *diagram-cartographer* — no brand, product-UI or IA work here.

### Sequence
3 and 4 run **in parallel** after 2, and neither may be run by whoever built the thing it
checks. 5 runs last, so it can cover mark types that actually exist rather than predicted ones.

### The limit on delegation, stated plainly
An agent can read the captures, write `charts.py`, and reason about encoding. It **cannot see
the page.** Dark-on-dark cells, a clipped legend, a chart at 3× scale, and a sideways scroll at
print width were all invisible to source-reading and all found by a screenshot. Any plan that
delegates the looking is a plan that ships those four defects.
