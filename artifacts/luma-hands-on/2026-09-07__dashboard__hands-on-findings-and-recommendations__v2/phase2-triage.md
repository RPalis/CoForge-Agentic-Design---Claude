# Phase 2 — triage of the 72 uncited findings

**Date** 2026-09-07 · **Agent** research-synthesizer · **Gate A — every line below is a proposal.**
Nothing here is a fact about the board until a human accepts it. Machine-readable form:
`phase2-triage.json`.

All `F-nnn` identifiers are capture-round finding IDs from `CAPTURE-INDEX.json` / `WORLD.json`.
They are **not** `research/evidence-ledger.json` IDs, and no ledger ID was minted for any
measurement (ADR-017).

---

## The answer to the question that was asked

**Both, but mostly the first.** Of the 72 findings carrying no conclusion, **60 are load-bearing**
— 25 belong to a conclusion that already exists and failed to cite them, 35 belong to a conclusion
nobody wrote. Only 12 are genuinely context or method.

The board is not over-evidenced and under-argued. It is **under-argued against evidence it already
holds**, and every one of those 60 can be repaired today without a single new capture.

| class | count | what it means |
|---|---|---|
| **A** — supports an existing conclusion that failed to cite it | **25** | free strength; cite and move on |
| **B** — supports a conclusion nobody drew | **35** | 14 Gate A proposals |
| **C** — context, correctly uncited | **8** | leave alone |
| **D** — method or coverage record | **4** | belongs in the method section, not the board |
| | **72** | |

Certainty: **62 clear, 10 unsure** (5, 8, 34, 37, 39, 73, 85, 88, 99, 105). Where the choice was
between A and C I chose C — that is why F34, F39 and F73 sit in C with the reasoning recorded.

---

## Class A — 25 immediate free wins

Grouped by the conclusion they strengthen. Three of these gaps are **mechanical, not editorial**:
insight-6, rec-6, insight-2 and rec-9 each list a capture **file** as a source and cite no finding
ID from it, so the finding was in the author's hand and never got a number attached to it.

### insight-4 · "Effort is ranked exactly where it is already measured, and computed nowhere else" — cites 3, gains 5

| # | finding | why it is class A |
|---|---|---|
| **20** | Expedia offers no effort ranking axis | Two of the three accommodation products behind rec-6's own "measured on 3 products" claim. |
| **25** | Google Travel: three axes, none about effort | Enumerated positively — a positive null, not an absence of looking. |
| **11** | Booking loyalty adds one more **price** axis | States the proposition numerically: "zero of 11 axes concern how easy a trip will be." |
| **92** | Trainline: duration + change-count per result, "Direct only" | The "already measured" half, in rail. Same capture as F90, which rec-1 does cite. |
| **100** | Effort measured in a third unit (calories) | Says insight-4's mechanism outright: which unit is used "depends entirely on what the vertical can compute." |

### insight-3 · "The disruption chain degrades at every hop" — cites 7, gains 4 *(and they are the hops)*

insight-3 cites F57, the synthesis. It cites none of the links F57's own capture names.

| # | finding | why it is class A |
|---|---|---|
| **49** | Protection varies across one result set; nothing reflects it | Named in hop 1: "Kayak ranks on price and duration… but not protection (F-49)." |
| **47** | KAYAK Mix — no carrier owns the journey | Named in hop 2, verbatim. |
| **51** | Handoff pre-selects the least flexible fare | Named in hop 3, verbatim. |
| **8** | Booking deflects across three first-party documents | Its evidence list contains two of insight-3's own citations (F03, F04), generalised. *unsure* |

### rec-8 · "Design the retention mechanism for someone on their first trip" — cites 5, gains 3

| # | finding | why it is class A |
|---|---|---|
| **29** | Two matched-pair diffs, opposite kinds of unlock | Names rec-8's problem: "a directly usable answer to the retention problem F-18 left open" — and F-18 is one of rec-8's citations. |
| **28** | Auth unlocks a **capability**, not a discount | The only day-one mechanism for a user with no history to convert. |
| **58** | Iberia Club currency earnable without travelling | The nearest existing template. It also **qualifies pain-6** — the programme still never addresses a first-timer (F60) — and that tension must be stated where it is cited. |

### insight-1 · "Nobody does both halves" — cites 6, gains 3

| # | finding | why it is class A |
|---|---|---|
| **24** | Google hands off rather than sells | The verified basis of the "Hands off" row of insight-1's own governing table. |
| **23** | Four decision surfaces neither incumbent offers | The measurement under F26, which insight-1 does cite. |
| **88** | Three of seventeen share a parent | WORLD.md §2 — insight-1's cited source — closes with this as corroborating detail. *unsure: also a roster caveat* |

### rec-6 · the ease/effort axis — cites 1, gains 2

| # | finding | why it is class A |
|---|---|---|
| **35** | Emissions is a **selectable** sort axis | rec-6 already lists this finding's capture file as a source and cites nothing from it. It is the template rec-6 needs: computed per option, expressed relative to a baseline, explained. |
| **99** | Citymapper: frequency, calories, cross-mode alternatives | rec-6 names on-site transport as a target and cites nothing from the round's only on-site-transport product. *unsure — could read as narrowing rec-6 rather than supporting it* |

### The rest

| # | finding | conclusion | why |
|---|---|---|---|
| **94** | Omio: "our 164 partners process your personal data" | **pain-9** | pain-9 is the only conclusion on the board with **zero** citations, and its single source file is this capture. This repairs the weakest thing on the board at zero cost. |
| **64** | Hopper ships a *family* of flexibility products | **insight-2** | insight-2 and rec-9 both source the Hopper capture and cite no Hopper finding. This is the "sold as a product" pole, in its stronger form. |
| **55** | Iberia ships "Ibot" | **insight-6** | insight-6 counts five assistants and lists an Iberia capture while citing no Iberia finding. |
| **15** | Three opt-in checkboxes in the booking form | **rec-7** | Its own text states rec-7's dichotomy: "a checkbox at checkout, or a consequence of the trip being modelled as one object… These produce very different products." |
| **112** | AA serves a thinner site by locale | **pain-5** | The Customer Service Plan insight-3 cites (F104) is not on the site a Spanish session gets. Access to disruption help depends on which country you load the page from. |
| **87** | Rentalcars: "free cancellation on **most** bookings" | **rec-4** | rec-4 rests on two captures of one competitor and has only a positive example. This is the clean negative one, from a different competitor. |
| **79** | Airbnb uses two price conventions in two verticals | **rec-3** | rec-3 rests on one capture. This strengthens its scope — never a nightly rate **and** never a per-traveller rate — while being honest about the exemplar. |
| **41** | The planner asserts the traveller's location, wrongly | **pain-8** | One of pain-8's three legs, uncited. **Citing it exposes an error — see R-2 below.** |

---

## Class B — 35 findings, 14 conclusions nobody drew

Ranked by how much each would change the board. Every one is a **description of a claim**, not a
claim. None has passed Gate A.

**1 · Rank or flag by RECOURSE.** — *F48; also drawn from F47, F49, F51 (classified A)*
It would say that the protection a traveller ends up holding varies enormously inside one result
set — from a direct carrier booking carrying EU 261 duties to a self-assembled multi-carrier
itinerary no carrier owns — that nothing in ranking, sorting or price reflects it, and that the
referring product already holds the data to rank on it.
*Why it changes the board most:* the round's own capture rates this **above a recommendation that
is on the board**. F49: "this is the clearest evidence yet for a 'protected first' axis… Luma would
not need new data to rank on it" and, in F47, "a stronger differentiation candidate than 'easiest
first'" — which is rec-6. The board recommends the weaker of two candidates the same round produced.

**2 · Luma starts behind on its own Core Features list.** — *F36, F40 (+ F102, already cited)*
It would say flight tracking is given away free and unbundled by a product that never sells the
flight, document ingestion is already built as planning input, and the anxiety features are sold as
someone else's subscription — so the only unoccupied position is bundling them **with** the booking,
which nobody does and which may be a business-model constraint rather than an oversight.
*This is stated plainly in the round's own WORLD.md §4 and appears in none of the 26 conclusions.*

**3 · Stated price promises contradict each other.** — *F30, F46, F52, F86*
It would say most products publish a price-completeness promise and no two are compatible: an
explicit all-in commitment with a named exception, an explicit exclusion of baggage, a supplier
all-in total with a named exception, and an unqualified "no hidden charges" in the vertical where
post-headline charges are most classic. A first-time traveller cannot rank products on a promise.
*F52 also inverts an assumption the board never tests: the supplier was more honest than the
comparison layer that referred the traveller to it.*

**4 · Ranking disclosure is uneven, not absent.** — *F10, F44, F77, F84*
It would say four competitors disclose the basis of their ranking in four incompatible forms — a
page-level commercial-influence notice, per-placement advertiser labelling, plain-language criteria
on the results surface, and a full published document — so the problem is not that nobody explains,
it is that no two explain the same thing in the same place.
*This constrains pain-1, which currently reads as a blanket claim on two citations. F10 is literally
titled `REFUTES_PRIOR_HYPOTHESIS` and says a blanket claim "does not hold here."*

**5 · Business goal 5 rests on a false premise.** — *F53, F54, F106*
It would say airport services are a fare-class entitlement on one airline and a standalone product
line on another, so "sell airport services" is two businesses, and on the first supplier examined
the buyer is a Business-class passenger — not the stated primary user.
*A named business goal is challenged by two airlines and the board says nothing. F54 carries its own
"Goal 5 and the target user may be pulling in opposite directions, and that should be settled before
design." Its market inference is marked Inferred from a single capture; the proposal inherits that.*

**6 · Tell the traveller whether this price is normal.** — *F27, F33, F74*
It would say the round's cheapest observed answer to "am I being taken advantage of" is stating
whether the current price is typical, that it works at both ends of the journey — before the search
and at the moment of payment — and that only two products do it, neither of them a transactional
incumbent, at either point.

**7 · Cross-modal comparison is already solved for transport.** — *F45, F95, F97*
It would say the scenario's opening problem is already answered for the transport half by at least
three products — a cross-modal prompt out of a flight result set, a single origin field accepting
city/station/airport/port across four modes, and duration-and-price per mode in one view — and
remains open only where accommodation and activities join.
*F45's capture flags itself as "evidence AGAINST a position this plan already took." The board took
the position and dropped the counter-evidence.*

**8 · The undecided traveller is already served, by name.** — *F31, F62, F81*
It would say three products ship explicit stage-1 affordances — destination-less search, flexible-date
tooling addressed to the undecided in the product's own copy, discovery as a top-level destination —
while both transactional incumbents require a destination and dates before anything happens.
*insight-1 covers this as a business-model claim. Nothing covers what the affordances actually are.*

**9 · Every loyalty programme measures the same thing.** — *F105, F109, F111*
It would say every programme observed measures money spent with the operator, one sells status
outright at a published unit price (USD 25 per Qpoint), and none measures whether the traveller had
a good trip.
*rec-8 says design a retention mechanism without saying what it would measure. This names what every
incumbent measures and puts the operator's own price on the thing being given away.*

**10 · The handoff seam is a documented user problem.** — *F50, F63*
It would say crossing the handoff drops every trace of the referring product and imposes a second
cookie decision inside one journey — and that a meta-search answers that exact confusion in its own
top-level FAQ.
*A competitor documenting its own seam against its own interest is a rare evidential form, and it is
uncited.*

**11 · Two of five user types are addressed; the stated primary one is not.** — *F59, F103*
It would say the roster addresses families (one airline's programme) and international travellers
(one subscription's entry-requirement product), so the market does segment — it segments and skips
Luma's stated primary user. *This sharpens pain-6 instead of repeating it.*

**12 · Accessibility: no testable claim anywhere, and the experience is deflected.** — *F5, F6, F7*
It would say the market leader publishes a statement naming no standard and making no conformance
claim, treats accessibility as a contractual term, and routes accessibility of the actual travel
experience to the supplier — so a testable WCAG 2.2 AA claim, which Luma is bound to anyway, is
unoccupied positioning rather than compliance overhead.
**Scope warning: ONE competitor. The thinnest proposal here. Present it as a single-competitor
observation or not at all.**

**13 · Attachment is obtained by default, not consent.** — *F91*
It would say one competitor ships a pre-checked cross-brand cross-sell that, on search, navigates the
traveller's current tab to another company's hotel search with dates that are not the travel dates.
*Business goal 2 is attachment. The board recommends modelling the trip as one object without
recording how the market currently gets attachment — pre-checked here, opt-in at Booking (F15).*

**14 · Variety as a stated ranking objective.** — *F76*
It would say one product states that its algorithm deliberately favours variety over the single
best-scoring set, and that for a traveller who does not yet know what they want, a varied first page
may teach the shape of the market better than an optimal one.
*Single source. Present as one product's stated policy, not a market pattern.*

---

## Class C — 8, correctly uncited

**14** no account required to reach the booking form · **16** Expedia's six verticals on a smaller
link surface · **19** the 8× result-count difference *(its own scope limit forbids the interesting
reading)* · **21** one-page vs two-page checkout · **34** emissions as a displayed attribute
*(superseded by F35; unsure)* · **39** the round's first empty state *(the competitor fact is real;
its comparative force is a coverage artefact — 8 of 119 states captured; unsure between C and D)* ·
**73** pay-later at no cost *(interesting deferral-vs-credit distinction, one competitor, nothing
else in the round bears on it; unsure)* · **82** no flights vertical on Tripadvisor's homepage.

## Class D — 4, method or coverage

**37** the ad-landing null control *(establishes the capture is comparable; unsure)* · **65** the
Hopper browser limit *(records why the differentiating products could not be captured)* · **85** the
roster-independence problem *(a property of the round's design; unsure)* · **108** F-108 SETTLED
*(a record of the round closing its own flagged inference; the fact it settles is F111)*.

---

## Reconciliation against the anchors

**All five anchors reproduce exactly.** I recomputed the union of `cites` across all 26 conclusions
(41 distinct numbers), subtracted it from `finding_lookup` (113 keys), and compared the remainder to
`uncited_findings` — an exact match, member for member. 26 / 9 / 41 / 113 / 72 all confirmed.

Four disagreements or additions, none of which changes the counts:

**R-1 · The fragility anchor undercounts by one — material.**
`single_capture: 9` is correct for n=1, but **pain-9 carries n=0** and is absent from
`fragile_conclusions`, which filters on n=1. The board has **ten** conclusions resting on one finding
or fewer, and the weakest of the ten is the one the anchor omits. It is repairable today: F94, class
A above.

**R-2 · pain-8 contains a factual error — material.**
pain-8 attributes "Estás en Toronto" to **Google's** AI planner. The source does not support it.
`captures/04-kayak/03-ai-planner-and-first-empty-state.json` records it as **Kayak's** AI planner
(F41), and its own observation field reads: *"The session is a Spanish-locale browser whose flight
search pre-filled Madrid (MAD) as origin minutes earlier. The AI surface independently asserts
Toronto. Two surfaces of one product disagree about where the traveller is."* The misattribution
originates upstream in F61 ("Google Travel AI planner: 'Estás en Toronto' (F-41)").
As sourced, pain-8 is **two** products disagreeing (Kayak with itself, and Skyscanner), not three.
No Google location assertion appears anywhere in WORLD.json. WORLD's own rule is "if a chunk and its
source disagree, **THE SOURCE WINS**." pain-8 and insight-7 need correcting before either is defended
at Gate A. The pain point survives — two surfaces of *one* product disagreeing is arguably sharper —
but the sentence as written is wrong.

**R-3 · WORLD's 117 reconciles exactly, and F71 is the missing one — informational, bears on C-043.**
117 = **112** of the 113 numbered findings + **1 duplicate** (F-108 appears as both
`F108_LOUNGE_ACCESS_IS_INDIRECTLY_PURCHASABLE` and `F108_SETTLED`) + **4 unnumbered records**
(`MATERIAL_CORRECTION_to_F09_F20_F25`, `PROHIBITION_2_NEAR_MISS_RECORDED`,
`CAPTURE_BLOCKED_BY_CONSENT`, `METHOD_CORRECTION_TO_MY_OWN_FINDABILITY_TEST`).
The one numbered finding absent from WORLD is **F71** — already flagged `NOT-IN-WORLD` in the input —
and it is **load-bearing**: cited by both rec-4 and pain-4. Anything retrieving from WORLD rather
than from `captures/` cannot see it. The 121 → 117 gap is therefore two gaps, not one.

**R-4 · The theme field was ignored, and the warning was justified.**
Encountered: F82 "no flights vertical" filed under `loyalty-and-retention`; F85 ownership under
`loyalty-and-retention`; F107 "disruption absent from navigation" under `loyalty-and-retention`; F57
"the disruption chain" under `ranking-and-comparison`; F94 "consent modal" under `decision-support`;
F41 "location asserted incorrectly" under `method`. Consistent with C-045. No classification here
depends on a label.

**R-5 · Three conclusions cite a file where a finding ID exists.**
insight-6 sources an Iberia capture and cites no Iberia finding (F55 exists). rec-6 sources the
Google MATERIAL-CORRECTION capture and cites no finding from it (F35 exists). insight-2 and rec-9
both source the Hopper capture and cite no Hopper finding (F64 exists). This is a mechanical,
repeatable citation gap rather than a judgement gap, and it accounts for a meaningful share of the
class A list.

---

## Assumptions

- That `cites` in `phase12-input.json` faithfully transcribes the board. I did not open the board
  payload; I reconciled against the anchors and they matched.
- **Class A rests on a partial view of 17 of the 26 conclusions.** Only the 9 fragile ones expose a
  body; the rest expose title + cites + sources. Six A calls should be re-tested against the full
  body before they are accepted: **8, 23, 24, 79, 88, 99**.
- Class B items are descriptions of claims, not claims. Several inherit scope limits from their
  captures (single competitor, single market, single locale) and those limits are printed on the
  proposal rather than dropped — B12 in particular is one competitor.
- **The evidence base is one-sided in a way that matters here.** The round captured 25 of 136 journey
  stages (18%), 8 of 119 states (6%), and reached a payment gate on 6 of 17 competitors. Proposals
  about discovery, comparison, ranking, pricing and loyalty rest on broad coverage. **B1 and B10
  touch disruption and post-purchase and rest on very little — which is precisely where Luma proposes
  to differentiate.** Weight them accordingly.
- B3 carries a live locale confound (D-004, on F46). B5 carries an explicit unknown (whether any
  Qatar airport service is purchasable by an economy passenger was not determined, on F106). Stated,
  not smoothed.
- I read only the ledger-equivalent corpus for this round — `phase12-input.json`, `WORLD.json`,
  `WORLD.md` and four capture files. I did not open `research/sources/`, did not read or write
  `research/evidence-ledger.json`, and minted no ledger ID.
