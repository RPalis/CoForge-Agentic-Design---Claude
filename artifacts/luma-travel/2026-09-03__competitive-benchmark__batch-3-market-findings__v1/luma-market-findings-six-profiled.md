# Luma competitor benchmark (Batch 3) — what the study found, across the six profiled

**Type:** competitive-benchmark · **Stage:** discover · **Status:** draft, awaiting Gate A
**Produced by:** research-synthesizer · **Date:** 2026-09-03
**Companion:** `ART-011` — read it first. This document is not readable without it.

---

## Coverage ceiling — read before any finding below

Everything in this document describes **six of fourteen** confirmed competitors.

- 14 confirmed in scope, **6 profiled**, **8 never profiled**, and 2 of those 8 (Kayak,
  Skyscanner) carry evidence only in an earlier, superseded framing that may be cited as
  prior art and may **never** be presented as current coverage.
  `Evidenced [ART-011 § Coverage]`, `Evidenced [D-001]`, `Evidenced [D-002]`.
- **98 of 770** planned feature cells (12.7%) rest on Tier 1 observation. 141 of the 330
  cells that exist are Unknown. `Evidenced [ART-011 § Evidence reached]`.
- **37 of 112** planned journey stage-cells (33%) carry any rating.
  `Evidenced [ART-011 § Evidence reached]`.
- One of the five designated tests — the one the plan flags as supporting a headline
  opportunity — **did not run**. `Evidenced [ART-011 § The untested claim]`.
- The Phase 3 and Phase 9 cell totals **do not reconcile with the grid they describe**.
  This document uses the recounted figures, not the stated ones.
  `Evidenced [ART-011 § Arithmetic defects]`.

The word "everyone" below never means the market. It means six competitors, and often four
or three, because two of the six have no compare surface to compare.
`Evidenced [S-09 § A note on the word "everyone"]`.

**No claim about what a user wants, needs or feels appears in this document as a finding.**
The study holds no user research; the evidence ledger holds zero records; none may be
minted. Where the source reasons about the first-time traveller it labels the reasoning
`Interpretation:` and rates it Low, and it is carried here at that rating or not at all.
`Evidenced [S-11 § Read this before the findings: what counts as evidence here]`.

Source register, claim labels and the reason citations read `[S-nn]` rather than `[ART-nnn]`
are all defined in `Evidenced [ART-011 § How to read a claim here]` and
`Evidenced [ART-011 § Source register]`.

---

## The feature matrix, across the six profiled

**Ten capability clusters, not seven.** 55 feature rows across ten clusters: vertical
coverage (7 rows), decision support (10), reassurance and trust (8), loyalty (2), prepare
and itinerary (7), travel day (5), in destination (5), after the trip (3), conversational
and AI (3), personalisation and accessibility (5). 7+10+8+2+7+5+5+3+3+5 = 55.
`Evidenced [S-08 §1 Feature matrix]`, `Derived` for the row arithmetic.

Cell values are exactly one of Yes / No / Partial / Unknown. **`No` means absence was
verified; where absence was not verified the cell is `Unknown`.** Every Yes and Partial
carries a confidence tag: High (live product), Medium (docs), Low (marketing or inference).
`Evidenced [S-08 header]`, `Evidenced [S-14 GUARDRAIL]`. The Luma column reads "Not built
(ideation), decision required" on all 55 rows and asserts no current behaviour.

**Where the Unknowns sit.** `Derived`, counting Unknown cells per cluster out of that
cluster's rows × 6: vertical coverage 10/42, decision support 19/60, reassurance and trust
15/48, loyalty 2/12, prepare and itinerary 23/42, travel day 19/30, in destination 17/30,
after the trip 12/18, conversational and AI 8/18, personalisation and accessibility 16/30.
Sum 141 of 330. **Prepare carries the largest number of Unknowns (23); after the trip
carries the largest proportion (12 of 18, 67%), with travel day next (19 of 30, 63%).** The
three thinnest clusters by proportion are the three stages the plan designated for the
deepest effort. `Evidenced [S-01 §3 Depth priority]`.

### The load-bearing row

The plan names one dimension as "the load-bearing dimension of the whole study": whether any
sort or filter ranks on ease, effort, reliability or stress rather than cost or time.
`Evidenced [S-01 §4 B. Decision support]`.

| Competitor | Sortable non-price / non-time / non-rating axis |
|---|---|
| Expedia | **No (High)** — all nine flight sorts and all six hotel sorts resolve to price, time, distance, rating or star |
| Booking.com | **No (Medium)** — sorts are price, rating, distance, review |
| Google Travel | **Yes (High)** — emissions is a sort option, and the whole result set can be reordered by it |
| TripIt | Unknown — no compare surface exists to carry a sort |
| Hopper | Unknown — flight results were never reachable this run |
| Tripadvisor | Unknown |

`Evidenced [S-08 §1 Cluster 2]`, `Evidenced [S-03 §4 Notable design decisions, item 2]`,
`Evidenced [S-04 §3 A non-price, non-time axis is a first-class control]`.

**One verified Yes, two verified Nos, three Unknowns, out of six of fourteen.** That is the
entire evidence base for the claim on which the recommendation rests. `Derived`.

`Inferred`: the two verified Nos are the strongest cells in the study — both transactional
incumbents, both walked hands-on, both with their full sort lists enumerated. The claim is
not weak because those cells are weak. It is weak because of what was never opened:
Trainline, Omio, Citymapper and Rome2Rio compare non-equivalent transport modes as their
core surface, and whether they rank on effort was never looked at.
`Evidenced [S-01 §2]`, `Evidenced [ART-011 § The untested claim]`.

### The rest of the matrix, cluster by cluster

Stated at the level the evidence supports. Every "no competitor" formulation is refused.

- **Vertical coverage.** Expedia and Booking.com sell across four or more verticals from one
  interface, both transactional, both High. Google Travel is the only metasearch surface in
  the profiled set, showing 18 sellers for one itinerary at prices differing by more than a
  factor of two, and hands off to buy. TripIt sells nothing at all, verified High.
  **Public transport ticketing is Unknown or a documented No in every cell** — the row is
  open and the four competitors that would close it were never run.
  `Evidenced [S-08 §1 Cluster 1]`, `Evidenced [S-04 §2 Stage 3]`,
  `Evidenced [ART-011 § The untested claim]`.
- **Decision support.** Deep on the two OTAs: Booking.com carries about 22 filter groups with
  a live result count on every option and a free-text "Smart filters" control that converts
  a typed request into removable, editable chips; Expedia annotates each flight filter with
  the price of the cheapest option meeting that constraint, so the cost of a refundable fare
  is legible before the filter is applied. Google Travel explains its own ranking inline in
  two sentences and states what happens to the results outside the top group.
  `Evidenced [S-02 §2 Stage 2]`, `Evidenced [S-03 §2 Stage 2]`, `Evidenced [S-04 §2 Stage 2]`.
- **Reassurance and trust.** Delivered as counted evidence and plain rate terms, not as a
  named guarantee. Sub-scores are published with the sample size behind them; review
  evidence is segmented by traveller type; one product carries a named human expert.
  Only two of six carry a named protection product, and both are paid: Expedia's
  checkout add-on and Hopper's "Flexible Travel Services", which its own help centre states
  plainly are **not insurance** and do not replace it.
  `Evidenced [S-08 §1 Cluster 3]`, `Evidenced [S-05 §2 Stage 3]`, `Evidenced [S-06 §3]`.
- **Loyalty.** Two of six publish numeric tenure thresholds. Booking.com's Genius reaches
  Level 2 at 5 bookings in 2 years and Level 3 at 15 bookings in 2 years, and **priority
  support sits at Level 3**. Tier 2, Medium. Google Travel has no programme at all.
  `Evidenced [S-02 §5 Evidence log, entry 32]`, `Evidenced [S-08 §1 Cluster 4]`.
- **Prepare and itinerary.** The cluster with the most Unknown cells in the matrix, 23 of 42.
  `Derived`. What is known: TripIt captures confirmations from any supplier by forwarded
  email or inbox sync and is the only product in the set that does; the two OTAs put the
  stage behind an auth wall that was never entered.
  `Evidenced [S-07 §2 Stage 4]`, `Evidenced [S-08 §1 Cluster 5]`.
- **Travel day.** Zero High cells in the entire cluster. `Derived` — every populated cell is
  Medium documentation or Unknown. TripIt documents the deepest support (computed departure
  timing, indoor airport maps across roughly 110 airports, terminal, gate and baggage
  reminders, disruption alerts), all on the Pro tier and none observed in operation. Hopper
  documents a paid same-day rebooking remedy with a stated $2,000 cap, a same-cabin rule and
  one use per booking. `Evidenced [S-07 §2 Stage 5]`, `Evidenced [S-05 §2 Stage 5]`.
- **In destination.** TripIt is the only product carrying a neighbourhood safety signal:
  1-to-100 scores with separate day and night values across six named sub-categories
  including women's safety and LGBTQ safety, sourced from a named third party, plus a
  user-declared risk threshold. Documented, app-gated, not observed.
  `Evidenced [S-07 §2 Stage 6]`.
- **After the trip.** Mostly review collection, and the thinnest cluster in the matrix by
  proportion of Unknown (12 of 18). One product surfaces flight-delay compensation
  eligibility through a third-party partnership.
  `Evidenced [S-08 §1 Cluster 8]`, `Derived`.
- **Conversational and AI.** One planner observed running (Tripadvisor, with a caveat), one
  narrow labelled question box shipped by two of the largest players, and one assistant that
  is a vendor claim only. This is the single Low-confidence cell in all 330.
  `Evidenced [S-08 §1 Cluster 9]`, `Evidenced [ART-011 § Prior claims]`.
- **Personalisation and accessibility.** Booking.com exposes 18 accessibility attributes as
  ordinary filters with result counts, split 7 property and 11 room, and publishes an
  accessibility statement citing European Accessibility Act scope. It is the only published
  statement found; **two of the five other competitors were never searched for one**.
  `Evidenced [S-02 §3 Accessibility as filterable inventory]`,
  `Evidenced [ART-011 § Prior claims]`.

---

## The journey comparison, across the six profiled

Eight stages, from the plan's own framing. The user held constant is the first-time
traveller, and every "best" call is a reasoned judgement against that person's job, not a
measurement. `Evidenced [S-10 header]`.

| Competitor | 1 Discover | 2 Compare | 3 Book | 4 Prepare | 5 Travel day | 6 In destination | 7 Return | 8 After |
|---|---|---|---|---|---|---|---|---|
| Expedia | Adequate (H) | Strong (H) | Strong (H) | Weak (H) | Unknown | Weak (H) | Unknown | Adequate (H) |
| Booking.com | Adequate (H) | Strong (H) | Strong (H) | Weak (H) | Weak (M) | Adequate (H) | Unknown | Adequate (H) |
| TripIt | Weak (M) | Weak (M) | Weak (H) | Strong (M) | Strong (M) | Adequate (M) | Adequate (M) | Adequate (M) |
| Hopper | Adequate (H) | Unknown | Adequate (M) | Weak (H) | Adequate (M) | Unknown | Unknown | Weak (H) |
| Google Travel | Unknown | Strong (H) | Adequate (H) | Weak (H) | Weak (M) | Unknown | Unknown | Weak (M) |
| Tripadvisor | Strong (H) | Strong (H) | Adequate (H) | Weak (H) | Unknown | Strong (H) | Unknown | Adequate (H) |

`Evidenced [S-10 § Stage strength table]`. Unknown means not reached this run, **not**
verified absence.

**What the table says, read carefully:**

- **No competitor in the profiled six is strong across the journey.** Strengths cluster:
  Expedia and Booking.com at compare and book; TripIt at prepare and travel day; Tripadvisor
  at discover, compare and in-destination. `Evidenced [S-10 § Stage strength table]`.
- **Prepare is Weak for four of six**, because it is auth-walled or shallow. The single
  Strong is TripIt, and it is Medium documentation of a Pro tier, not an observation.
  `Evidenced [S-10 § Stage strength table]`.
- **Travel day and return are the emptiest columns.** Return is Unknown for five of six, and
  the sixth is "implied" from travel-day evidence. **No product was walked through a return
  scenario at all**, so this column is absence of observation, not evidence about the
  market. `Evidenced [S-10 § Stage 7]`, `Evidenced [S-11 §3.4]`.
- **A Weak cell is not always a failing.** TripIt is Weak at book because it sells nothing,
  which is a product decision, not a gap. `Evidenced [S-10 § Stage strength table]`.
- **Three of eight stages have no leader.** Book (Expedia and Booking.com tie, and the
  evidence does not separate them), in-destination (Tripadvisor owns what-to-do and how-to-
  move, TripIt owns is-it-safe, and no product does both), and return.
  `Evidenced [S-10 § Stage 3]`, `[S-10 § Stage 6]`, `[S-10 § Stage 7]`.

`Inferred`, and named as inference: the leader calls are the softest evidenced material in
the study. They are judgements about a user nobody interviewed, made by a researcher the
study itself notes "is not the target user" and for whom "fluency hides friction".
`Evidenced [S-01 §7 Risk 3]`.

---

## The patterns, across the six profiled

### Conventions — present, with their denominator stated

| Convention | Who, and the denominator |
|---|---|
| Rating shown with its review count | 4 of the 4 competitors with a review surface (H) |
| Sort control and filter rail on results | 3 of the 3 transactional or aggregating compare surfaces (H) |
| Printed ranking-basis disclosure | **4 of 4 ranked surfaces** (H) |
| A saved or trips surface, usually behind sign-in | 6 of 6, in some form |
| All-in pricing labelled as such | 3 of 3 transactional players (H); two market it as positioning |
| Consent with a genuine decline path | 3 of 3 where a modal was seen (H); one dismissed, two not observed |

`Evidenced [S-09 §1]`. Note that no row's denominator is six. The convention claims are
strong within a small, explicitly stated set and say nothing about the eight unprofiled.

### Emerging, and how thin the evidence for "emerging" is

Conversational planning: one shipped and observed, one marketed and unshipped — two of six.
Narrow labelled AI question-answering: two of six, both badged Beta. Natural-language input
converted to editable controls: two of six, and not the same mechanism. **A non-price
decision axis on results: one of six.** Accessibility as filterable inventory: three of six,
one deep and two shallow. Named paid flexibility products: two of six. Declared-tolerance
personalisation: one of six. `Evidenced [S-09 §2]`.

The source rates its own trend confidence Low or Low-to-Medium on four of these seven, and
Low on the non-price axis specifically, with the note that whether it generalises beyond
emissions to ease or effort "is not evidenced anywhere". `Evidenced [S-09 §2.4]`.

### Where the market has not converged

Nine unsettled questions, each with incompatible live answers: the business model itself;
what ranking discloses about commission and in which vertical; whether to advise the user
when to buy; **whether a user can rank on anything but price, time or rating**; what
personalisation is based on, watched or declared; whether loyalty includes a zero-booking
user; how disruption is handled — monetised, notified, or handled as policy; what the word
"AI" refers to; and how an itinerary gets filled. `Evidenced [S-09 §4]`.

`Inferred`: an unsettled question is a genuinely open design question, which is a different
and more useful object than a gap. It is also where a small entrant can take a position
without being wrong by consensus.

### What "works" — and the bar the study refused to lower

The study admits only two kinds of evidence for "this works": adoption across competitors,
and a step it demonstrably removes. It looked for user reviews referencing an interface
pattern and found none — the reviews it read were about tour guides and venues.
`Evidenced [S-09 §3]`. Two on-thesis patterns (Tripadvisor's layered social proof plus human
expert; Hopper's onboarding psychology) were **explicitly refused** as "works well", because
each is a single instance with no adoption evidence and no groundable step-removal claim:
"Any statement that they 'work' would be taste." `Evidenced [S-09 §3]`.

That refusal is the strongest methodological moment in the study and it is worth preserving
downstream, because both patterns are the ones a reader most wants to copy.

---

## The white space, across the six profiled

Four kinds, kept separate. The separation is the finding.

**Unsolved (3).** No sort or filter on ease, effort or stress anywhere in the profiled set.
Street-level safety never in the same place as what-to-do and how-to-get-there. Travel-day
help absent on the open web unless paid or in an app. `Evidenced [S-11 §1]`.

**Badly solved, so demand is proven by everyone building it (4).** Reassurance at the moment
of paying is present but buried in rate rows. Prepare is an auth-walled list, and the entry-
requirements answer is paywalled. The homepage assumes the user knows their destination.
The ranking disclosure is written for a regulator. `Evidenced [S-11 §2]`.

**Deliberately unsolved — walls, not doors (5).** Selling transport tickets (low margin,
fragmented supply — **and explicitly caveated as untested**). Priority support for a
zero-booking user (unit economics; a structural exclusion, not an oversight). Aggregators
owning the failure experience (outside the model). The return leg as its own moment (no
second transaction). Deep travel-day help on the open web (a platform constraint).
`Evidenced [S-11 §3]`.

**Cross-stage seams nobody owns (4).** Book to prepare, "I have paid, now what". Compare to
book across four separate vertical searches. Confidence rebuilt from zero at every stage —
the softest item in the study, labelled `Interpretation:` at Low throughout. Where you
booked versus where you manage the trip. `Evidenced [S-11 §4]`.

**Naming the wall is the point.** A gap with a reason is not an opportunity. The study wrote
a "why nobody has solved this" line for every item and dropped or reclassified the ones where
it could not write one honestly. `Evidenced [S-11 header]`.

---

## The opportunity scoring, across the six profiled

**The model is an unweighted sum, not a weighted score.** Five criteria — user impact,
evidence strength, differentiation, feasibility, strategic fit — each scored 1 to 5, totalled
out of 25 with no weights applied. `Evidenced [S-12 header]`. All fourteen totals were
re-added here and **all fourteen agree** with the stated total. `Derived`.

| ID | Opportunity | Imp | Ev | Diff | Feas | Fit | Total | Flag |
|---|---|---|---|---|---|---|---|---|
| O3 | Inverted priority: most help at zero bookings | 4 | 3 | 5 | 3 | 5 | **20** | |
| O1 | Least-stress ranking axis | 4 | 3 | 4 | 2 | 5 | **18** | RISK feasibility |
| O2 | Per-option confidence label | 4 | 3 | 3 | 2 | 5 | **17** | RISK feasibility |
| O4 | Free upfront entry-readiness check | 4 | 3 | 3 | 3 | 4 | **17** | |
| O5 | One in-destination surface: safe, do, move | 4 | 3 | 4 | 2 | 4 | **17** | RISK feasibility |
| O9 | Post-booking "now what" guide | 3 | 3 | 3 | 3 | 4 | **16** | |
| O6 | Proactive travel-day companion | 4 | 3 | 2 | 2 | 4 | **15** | RISK feasibility |
| O7 | Plain-language reassurance at the decision point | 3 | 3 | 1 | 4 | 4 | **15** | low differentiation |
| O8 | "Where should I go" discovery | 3 | 3 | 2 | 3 | 4 | **15** | |
| O10 | One trip object across verticals | 4 | 3 | 3 | 1 | 3 | **14** | RISK feasibility (fatal 1) |
| O13 | Persistent confidence state | 3 | 2 | 3 | 2 | 4 | **14** | RISK evidence + feasibility |
| O14 | Named pre-purchase safety net | 3 | 3 | 2 | 2 | 4 | **14** | RISK feasibility |
| O11 | Supplier-agnostic trip manager | 3 | 3 | 1 | 3 | 3 | **13** | low differentiation |
| O12 | Reassurance-first ranking copy | 2 | 3 | 1 | 4 | 3 | **13** | low differentiation |

`Evidenced [S-12 §2 Scores at a glance]`, `Derived` for the re-addition.

**Read the columns, not the totals.**

- **Every one of the fourteen scores exactly 3 on evidence strength — except O13, which
  scores 2.** `Derived`. That is not a coincidence and the source says why: with no user
  research held, evidence strength reflects how solid the *market* evidence for the problem
  is, never proof that a user feels the pain, so the whole column is capped in the middle.
  `Evidenced [S-12 header]`. The ranking therefore discriminates on impact,
  differentiation, feasibility and fit — and not at all on evidence.
- **A fatal 1 was never averaged away.** O10 carries feasibility 1 and stays visible at
  total 14 rather than being deleted; O7, O11 and O12 carry differentiation 1 and are
  flagged in place. `Evidenced [S-12 §1]`, `Evidenced [S-17.5 §7]`.
- **Feasibility is scored against a blank.** Team size, technology, data access and
  distribution "arrived blank" and were not guessed. Every feasibility number means
  "feasible at ideation, with no supplier deals and an unknown team", and the source states
  that real facts would move the column. `Evidenced [S-12 § Product context]`.
- **Three of the top five carry a feasibility RISK, and all five share the same evidence
  ceiling.** `Evidenced [S-12 §3 Ranked shortlist]`.
- **The shortlist is four bets, not five.** O2 made the cut on total but is "the display
  layer of the same bet" as O1 and would merge with it; the source says so and asks that it
  not be treated as a separate fifth of the roadmap. `Evidenced [S-12 §3]`.
- **The rejects list is load-bearing.** Nine ideas were generated and discarded with a
  reason each, including a conventional loyalty programme (it reproduces the exact exclusion
  the thesis attacks) and "most intelligent AI assistant" positioning (commoditising, not
  differentiating). `Evidenced [S-12 §4 Rejects]`.

---

## The strategy, and what it rests on

`Evidenced [S-13]`, corroborated by `Evidenced [S-17.6 §8]`.

**Where to play.** The plan-and-compare decision (stage 2), reframed around stress rather
than price, extended into the moments where a first-timer's confidence collapses. Four
alternatives are rejected with a traced reason each: discover (partly occupied),
in-destination (data-heavy, feasibility risk), prepare (TripIt occupies it), travel day
(platform wall), full breadth (feasibility 1).

**Three bets.** A: make "easiest for someone like me" a first-class sort. B: front the
confidence a newcomer would otherwise have to earn, tapering as they gain experience. C:
answer "am I allowed in and what do I need" free and without an account, as the acquisition
wedge.

**Model conditionality.** Enter as a referral layer, which needs no supplier deals and ships
bets A and C now; move to a subscription companion once B's retention is demonstrated; do
not become an OTA at ideation.

**The strongest evidenced part is a structural exclusion, not a feature gap.** Priority
support is gated at Genius Level 3, which requires 15 bookings in two years. A booking-count
loyalty model cannot front support to a zero-booking user without contradicting itself, so
this is a wall for incumbents rather than a race. Tier 2, Medium.
`Evidenced [S-02 §5 Evidence log, entry 32]`, `Evidenced [S-11 §3.2]`.

### What the strategy itself says would prove it wrong

Reproduced because it is the most useful paragraph in the study and because every one of its
four kill signals is currently open. `Evidenced [S-13 § What would prove this strategy
wrong]`.

1. First-time travellers choose primarily on price and do not value a stress axis. **Not
   tested — no user research exists.**
2. First-timers want less friction, not more guidance. **Not tested.**
3. A specialist among the eight unprofiled competitors already owns an effort or stress
   axis. **Not tested — and this is the same gap that leaves designated test 3 unrun.**
   `Evidenced [ART-011 § The untested claim]`.
4. The stress signal cannot be built from available data. **Not tested — data-source
   availability and cost were never checked.** `Evidenced [S-12 Gaps]`.

`Inferred`: all four kill signals are open, and the study is explicit that the first is the
deepest, which is why research is the first item in its own sequencing and not the last.
`Evidenced [S-13 §4 Sequencing]`.

---

## Carried with a reduction

Twelve places where a source claim could not be carried at the strength its own summary
gives it. This list is the reason the artifact exists rather than a link to the folder.

1. **The feature-matrix cell totals.** Stated 86/48/28/113 (sum 275) against a 330-cell
   grid. Replaced by the recount. `Evidenced [ART-011 § Arithmetic defects]`.
2. **"High 86" and "Yes 86".** One integer used for two different populations; not carried
   in either direction. `Evidenced [ART-011 § Arithmetic defects]`.
3. **Hopper's compare stage.** Unknown, never `No`. Results were unreachable, so Hopper
   cannot be ranked at compare and its absence from the non-price-axis finding is a gap, not
   a data point. `Evidenced [S-05 § Evidence note]`.
4. **Google Travel's cells.** Walked signed in while the other five were walked signed out.
   Its ranking and personalisation observations are not comparable like-for-like and must
   not be presented as equivalent in kind. `Evidenced [S-04 § Two conditions]`.
5. **Tripadvisor's AI planner.** Observed live but pre-populated on load; the originating
   prompt was not typed. Every claim resting on it carries the caveat, and the source itself
   asks for a clean re-run before it is quoted as a capability.
   `Evidenced [S-06 § Scope note]`.
6. **Expedia's Romie.** Vendor claim, alpha, app-only, not seen shipped. Treated as
   unshipped and never counted toward any capability. `Evidenced [S-03 §5, entries 26–28]`.
7. **TripIt's travel-day, prepare and in-destination depth.** Documentation of intended
   behaviour, Pro-gated, never seen in operation: 12 High claims against 49 Medium.
   `Evidenced [S-07 § Confidence summary]`.
8. **Every stage "leader" call.** A reasoned judgement against an unresearched user, not a
   measurement. Carried as `Inferred`, never as evidence. `Evidenced [S-10 header]`.
9. **The word "everyone".** Six, and often four or three. Every convergence claim in the
   pattern analysis carries its own denominator here. `Evidenced [S-09 § A note on the word
   "everyone"]`.
10. **White-space item 3.1, transport ticketing.** Cannot be read as white space; the
    competitors that would settle it were never profiled, and the source prints that caveat
    in place. `Evidenced [S-11 §3.1]`.
11. **Bet A's vacancy claim.** Verified across six of fourteen, with three of the six
    Unknown on the load-bearing row. Carried as an open question, not as a finding.
    `Evidenced [ART-011 § The untested claim]`.
12. **Every claim about what the first-time traveller wants or feels.** Carried only as the
    source's own `Interpretation:` at Low, never as a finding, and never in a form that
    would require a ledger record this repository cannot supply.
    `Evidenced [S-11 § Read this before the findings: what counts as evidence here]`.

---

## Assumptions

- **A-1.** That the six profiles are a faithful record of what was on screen on 21 July 2026.
  Not independently reproduced. Two competitors state in their own documentation that they
  run display tests and may order results differently across app and web, so any single
  observation may be one variant. `Evidenced [S-02 Gaps]`, `Evidenced [S-03 Gaps]`.
- **A-2.** That findings recorded from one region (a browser located in Spain) and one
  account state generalise well enough to be worth comparing. The plan flags region and
  account state as a named risk and the study records both per walkthrough, which is the
  mitigation, not a solution. `Evidenced [S-01 §7 Risk 4]`.
- **A-3.** That the ten-cluster grouping is a sound comparison frame. It was built by
  merging six profiles under a rule that forbids inventing a row for symmetry, so a
  capability only one competitor has still gets a row. This makes the Unknown count high by
  construction, which is honest and also means cluster-level comparisons are not like-for-
  like. `Evidenced [S-08 § Gaps, last row]`.
- **A-4.** That the first-time traveller is the right user to judge against. This is the
  study's own sharpened purpose statement, which the plan rates Low and asks the client to
  accept, amend or reject before Phase 2. **No acceptance is recorded anywhere in the
  sources**, and Phases 7 and 8 hold it constant as "the business goal".
  `Evidenced [S-01 §1]`, `Evidenced [S-12 § Product context]`.
- **A-5.** That the executive report read here from its eight page images is the same
  document as the PDF and DOCX in the folder. `Evidenced [ART-011 § Source register]`.

---

## Gaps

The full register is in `Evidenced [ART-011 § Gaps]` — 26 entries. The ones that bear
directly on the findings above, restated so this document is not readable without them:

| # | Gap | What it would change |
|---|---|---|
| 1 | Eight competitors unprofiled | Every convergence claim, every vacancy claim, the transport row, and the in-destination combination gap |
| 2 | No user research, anywhere | Every impact and desire judgement, and the whole evidence column of the scoring model |
| 3 | Stage 7, return, never walked for any product | The emptiest column in the journey table is absence of observation, not a market finding |
| 4 | Travel day has zero High cells | The stage the study calls peak-anxiety rests entirely on documentation and paid tiers |
| 5 | Auth walls across every OTA | Trips, saved lists, signed-in personalisation and loyalty state were never entered |
| 6 | Checkout and post-payment excluded by design | The book stage stops before the moment it describes as highest-anxiety |
| 7 | Product context blank | Every feasibility score, and therefore the order of the shortlist |
| 8 | Data-source availability never checked | Bets A and C both assume data is licensable or public |
| 9 | Target markets never supplied | Which competitors are even available, and European Accessibility Act exposure |
| 10 | The Phase 3 and Phase 9 cell totals do not reconcile | Any figure quoted from either document about matrix coverage |

**Unknown is a valid answer and nothing above has been filled with a plausible guess.**
`Evidenced [S-01 §5 Rules that hold for the whole study]`.

---

## What a human is being asked to decide (Gate A)

1. Whether these findings may be quoted at all, given they describe six of fourteen.
2. Whether the recounted cell figures replace the stated ones downstream, or sit beside them.
3. Whether the three "no clear leader" stages stay unresolved or get a named tiebreaker.
4. Whether the shortlist is read as four bets or five, given O2 merges into O1.
5. Whether anything proceeds before the study's own first sequenced action — first-time-
   traveller research — has run.

Nothing here graduates to automatic. research-synthesizer conclusions never do.
