# Luma Competitor Benchmark · Phase 7: Opportunity Generation and Scoring

**Status:** Converting Phase 6 problems into opportunities and scoring them honestly, including the ones that score badly. Every opportunity traces to a specific Phase 6 item. Scores are shown per criterion, a fatal 1 is never averaged away, and any opportunity scoring 1 or 2 on evidence or feasibility carries a `RISK:` line.
**Date:** 21 July 2026
**Phase:** 7 of 9

## Product context: what was supplied, and the assumption used

The product-context input (team size, technology, data access, distribution) arrived **blank**. This is a real gap and it is not filled with a guess. Feasibility is instead scored against the only product context that is on the record, from the benchmark plan:

- Luma is at **ideation**. No product is built.
- The **business model is unsettled** across referral, OTA and subscription.
- There are **no supplier agreements**, so any capability requiring inventory, live supplier feeds, or booking fulfilment is currently outside reach. The plan states plainly that without supplier agreements Luma is a referral layer.
- Team size, engineering capacity, and any owned data or distribution are **Unknown**.

Consequence: every feasibility score below is "feasibility at ideation, with no supplier deals and an unknown team." If concrete team, tech, data and distribution facts arrive, the feasibility column moves, and three of the RISK flags could clear. This is stated so the scores are read for what they are.

**Business goal held constant** (the sharper Phase 1 version): help a first-time traveller act with confidence at the moments where confidence normally collapses, by making the least stressful option visible and choosable, not just the cheapest one.

Confidence tags: High (H, live product), Medium (M, docs), Low (L, marketing or inference). Scoring criteria are each 1 to 5; total is out of 25.

A note the whole section depends on: with no user research held, the **evidence strength** score reflects how solid the *market* evidence for the problem is, not proof that users feel the pain. Where a problem's existence as a market gap is High but its user salience is only inferred, the evidence score sits in the middle and says so. This mirrors Phase 6.

---

## 1. Opportunities, with scores

Format per opportunity: the five description fields, then the five criterion scores each with a one-line justification, then the total.

### O1 · Least-stress ranking axis
- **Problem it solves:** Phase 6, item 1.1. The user can only choose on price and time, never on how easy or stressful an option is.
- **What it does:** adds a ranking and filtering axis that orders options by predicted effort and stress rather than price, using observable signals such as number of transfers, tightness of connection timing, total door-to-door time, and whether a step needs a language the user does not speak. The user can sort the whole result set by "easiest for me," the same way they can sort by price today.
- **Who it is for:** the first-time traveller at the plan-and-compare stage who cannot yet judge whether an option is manageable.
- **Why we are plausibly the ones to build it:** as an ideation product with no conversion-on-price economics to protect, Luma can make a non-price axis the primary sort. Every incumbent optimises order for conversion, which correlates with price, so the axis competes with their core metric and they are disincentivised to lead on it.
- **Scores:**
  - User impact **4**: removes the central first-timer pain at the highest-traffic stage, for a broad set of users.
  - Evidence strength **3**: the market absence is verified High (only Google offers any non-price/time/rating sort), but that users want a stress axis is inference, Low.
  - Differentiation **4**: incumbents are structurally tied to price-led order; copying a genuine stress model is more than a UI change.
  - Feasibility **2**: the stress signal must be constructed, and the inputs are not in supplier feeds Luma does not yet have. `RISK`.
  - Strategic fit **5**: this is the sharper business goal restated as a feature.
  - **Total: 18.**
- `RISK:` feasibility 2. For this to be buildable, at least one of the following must be true: Luma can source structured itinerary data (transfers, timings) without supplier agreements, or it can start with a narrow single-vertical dataset where the signals are already public. If neither holds, this is a research-and-data project before it is a product.

### O2 · Per-option confidence label
- **Problem it solves:** Phase 6, item 1.1 (display side of the same problem as O1).
- **What it does:** shows a plain "how easy is this for someone like you" label on each result, built from the same signals as O1 but presented as a single readable badge rather than a sort. It sits beside the price the way a review score does.
- **Who it is for:** the same first-timer at compare who reads a list faster than they configure a sort.
- **Why we are plausibly the ones to build it:** same reasoning as O1; a greenfield product can put a confidence label where incumbents put a price.
- **Scores:**
  - User impact **4**: same pain, same breadth as O1.
  - Evidence strength **3**: same basis as O1.
  - Differentiation **3**: a label is easier to fast-follow than a true ranking model.
  - Feasibility **2**: depends on the same unavailable signal as O1. `RISK`.
  - Strategic fit **5**: same goal alignment.
  - **Total: 17.**
- `RISK:` feasibility 2, same condition as O1. Note also that O2 overlaps O1 heavily and would merge with it in practice.

### O3 · Inverted priority: most help at zero bookings
- **Problem it solves:** Phase 6, item 3.2. Priority and human help are gated by tenure, so the first-timer who needs it most is excluded.
- **What it does:** gives the newcomer the most guidance and support at the start of their relationship with the product, before any booking history exists, and reduces the hand-holding as the user gains experience. It inverts the loyalty logic where support is earned by accumulated bookings.
- **Who it is for:** the first-time traveller across every stage, most acutely at book and travel day.
- **Why we are plausibly the ones to build it:** this is a structural position an incumbent cannot copy without breaking its own economics. Booking.com grants priority support only at Genius Level 3, which requires 15 bookings in two years (Medium). A model that fronts the support cost for a zero-booking user contradicts a booking-count loyalty model, so the incumbents are walled out of it, not merely slow.
- **Scores:**
  - User impact **4**: addresses the confidence deficit for the target user across the journey, not one stage.
  - Evidence strength **3**: the exclusion is grounded in an observed threshold (Genius L3, Medium); that it hurts the first-timer is inference, Low.
  - Differentiation **5**: structurally hard to copy, which is the strongest kind of differentiation and the one the benchmark plan singled out.
  - Feasibility **3**: feasible if "support" means guided automated flows and proactive reassurance rather than staffed human agents; expensive and model-dependent if it means people.
  - Strategic fit **5**: it is the confidence-at-collapse thesis expressed as a strategy, not just a feature.
  - **Total: 20.**

### O4 · Free upfront entry-readiness check
- **Problem it solves:** Phase 6, item 2.2. Prepare is an auth-walled list, and the thing the user most needs, whether they can even enter the country, is hidden or paid.
- **What it does:** tells a traveller, before they commit, what they need to enter the destination given their nationality: visa, health and documentation requirements, presented free and without an account. It answers "am I allowed in and what do I need" at the moment the question arises.
- **Who it is for:** the first-time international traveller at the prepare stage, and earlier for the anxious planner.
- **Why we are plausibly the ones to build it:** the data is licensable (TripIt cites Riskline and Basetrip, Medium) or available from official government sources, and an ideation product has no margin incentive to paywall it, so it can be an acquisition surface rather than a Pro feature.
- **Scores:**
  - User impact **4**: concrete, high-anxiety question removed for international first-timers.
  - Evidence strength **3**: the paywalling is observed (Medium); that the free version is wanted is inference, Low.
  - Differentiation **3**: the data is available to anyone, so it is copyable, but incumbents are disincentivised from making it free because it is a paid tier for them.
  - Feasibility **3**: needs a data licence or official-source integration, no supplier agreements required, moderate build.
  - Strategic fit **4**: strong confidence play, though at prepare rather than on the compare-axis spine.
  - **Total: 17.**

### O5 · One in-destination surface: safe, do, move
- **Problem it solves:** Phase 6, item 1.2. At street level the user cannot find whether an area is safe in the same place as what to do and how to get there.
- **What it does:** for a chosen area, combines a neighbourhood safety signal, things to do, and street-level navigation in one view, so the newcomer does not switch between three apps. It answers "is it safe here, what is worth doing, and how do I get around" together.
- **Who it is for:** the first-time traveller in the destination.
- **Why we are plausibly the ones to build it:** greenfield, so it can integrate safety, activity and transit data without a legacy that separates them; no product in the set combines the three (Medium).
- **Scores:**
  - User impact **4**: addresses a real multi-app burden at a high-anxiety stage.
  - Evidence strength **3**: the non-combination is observed across six (Medium); the safety pain is inference, Low.
  - Differentiation **4**: combining three third-party data sources is a genuine barrier, not a UI copy.
  - Feasibility **2**: needs safety data with its liability exposure, transit integration, and activity data at once. `RISK`.
  - Strategic fit **4**: on-thesis for in-destination confidence, off the compare-axis spine.
  - **Total: 17.**
- `RISK:` feasibility 2. For this to be buildable near-term, Luma would need access to a safety data source willing to carry the liability, plus transit and activity data, in at least one launch city. Without that, it is a multi-partner integration before it is a product.

### O6 · Proactive travel-day companion
- **Problem it solves:** Phase 6, items 1.3 and 3.5. Travel-day help is missing unless the user has paid or installed an app.
- **What it does:** tells the traveller when to leave, where the gate is, and what to do if a leg is delayed or missed, pushed proactively on the day rather than looked up. It targets the single highest-anxiety window for a first-timer.
- **Who it is for:** the first-time traveller on travel day and return.
- **Why we are plausibly the ones to build it:** an ideation product can be app-first from the start, which is where this value has to live.
- **Scores:**
  - User impact **4**: the peak-anxiety stage.
  - Evidence strength **3**: the web gap is High and the app-wall is documented; user salience inferred, Low.
  - Differentiation **2**: TripIt Pro and Hopper already ship versions of this, so it is copyable and partly occupied.
  - Feasibility **2**: needs an app, push notifications, and live status and traffic feeds. `RISK`.
  - Strategic fit **4**: strong confidence alignment.
  - **Total: 15.**
- `RISK:` feasibility 2. Requires a native app and live data feeds (flight status, traffic, airport data), none of which exist at ideation. For this to be near-term, Luma would need those feeds and app capacity, and would be building where two incumbents already operate.

### O7 · Plain-language reassurance summary at the decision point
- **Problem it solves:** Phase 6, item 2.1. The reassurance the user needs when paying is buried in rate rows.
- **What it does:** before commitment, shows a calm summary of the three things a nervous buyer needs: the cancellation cost, whether they are charged now, and the all-in total, separated from upsell. It lifts existing information out of the fine print.
- **Who it is for:** the first-time traveller at book.
- **Why we are plausibly the ones to build it:** a product not optimised for upsell revenue can give reassurance the prominent slot incumbents give to cross-sell.
- **Scores:**
  - User impact **3**: real but incremental; the information already exists, it is presentation.
  - Evidence strength **3**: the fine-print pattern is observed High; user impact inferred, Low.
  - Differentiation **1**: trivially copyable, a fast-follow within weeks.
  - Feasibility **4**: light, presentation-layer, no new data.
  - Strategic fit **4**: on-thesis for confidence at book.
  - **Total: 15.**
- Note: differentiation 1 is not a RISK per the rule (which flags evidence or feasibility), but it is a fast-follow exposure and is called out here.

### O8 · "Where should I go" discovery for the undecided
- **Problem it solves:** Phase 6, item 2.3. The homepage assumes the user already knows their destination.
- **What it does:** a discovery entry for someone with no destination, driven by interest and constraints (budget band, time available, appetite for effort) rather than by a destination search box or a deal grid. It returns candidate destinations with reasons.
- **Who it is for:** the first-time traveller at dream-and-discover.
- **Why we are plausibly the ones to build it:** greenfield, no obligation to convert existing search intent, so it can serve the undecided rather than the decided.
- **Scores:**
  - User impact **3**: helps a real subset, but only those with no destination yet.
  - Evidence strength **3**: the assume-destination pattern is observed High; desire inferred, Low.
  - Differentiation **2**: Booking.com's theme planner and Tripadvisor's interest browse already do versions of this (High).
  - Feasibility **3**: moderate, content and matching rather than supplier data.
  - Strategic fit **4**: on-thesis, early-journey confidence.
  - **Total: 15.**

### O9 · Post-booking "now what" next-steps guide
- **Problem it solves:** Phase 6, item 4.1. The seam between book and prepare, where the user is dropped from a polished checkout into an empty list.
- **What it does:** turns any booking confirmation into a plain checklist of what to do next before the trip, ordered by when it matters. It bridges the drop that nobody currently owns.
- **Who it is for:** the first-time traveller crossing from book to prepare.
- **Why we are plausibly the ones to build it:** a neutral product can accept a confirmation from any source and own the handoff that each incumbent leaves to its own retention surface.
- **Scores:**
  - User impact **3**: removes a real drop, though it depends on the user arriving with a booking.
  - Evidence strength **3**: the seam is observed High; user distress inferred, Low.
  - Differentiation **3**: nobody in the set owns this seam.
  - Feasibility **3**: capture-and-checklist, no supplier agreements needed.
  - Strategic fit **4**: on-thesis for continuity of confidence.
  - **Total: 16.**

### O10 · One trip object across verticals
- **Problem it solves:** Phase 6, item 4.2. A trip is one thing but must be assembled from separate vertical searches.
- **What it does:** carries a single coherent trip through compare and book across flights, stay, transport and activities, so the user does not reassemble it themselves.
- **Who it is for:** the first-time traveller across compare and book.
- **Why we are plausibly the ones to build it:** greenfield, not siloed by legacy entities the way the incumbents are (Booking.com books flights and cars under different legal entities, High).
- **Scores:**
  - User impact **4**: removes a large assembly burden.
  - Evidence strength **3**: the silo structure is observed High; user burden inferred, Low.
  - Differentiation **3**: hard, but the incumbents are moving toward connected trips.
  - Feasibility **1**: requires supplier agreements across four verticals from ideation, which the plan names as the breadth trap. `RISK`.
  - Strategic fit **3**: breadth is off the narrow-confidence thesis.
  - **Total: 14.**
- `RISK:` feasibility 1. This needs inventory and supplier relationships in four verticals at once, which Luma explicitly does not have and which the benchmark plan flags as the most expensive possible position from ideation. For this to be viable, Luma would need to be a funded OTA with supplier deals, which contradicts the current stage.

### O11 · Supplier-agnostic trip manager
- **Problem it solves:** Phase 6, item 4.4. The seam between where you booked and where you manage the trip.
- **What it does:** captures any booking from any source and manages the prepare-to-return arc in one place.
- **Who it is for:** the first-time traveller who booked across several sites.
- **Why we are plausibly the ones to build it:** a neutral manager has no incentive to trap the trip in one vendor's app.
- **Scores:**
  - User impact **3**: real, but the arc it serves is the less anxious middle.
  - Evidence strength **3**: fragmentation observed; user impact inferred, Low.
  - Differentiation **1**: TripIt already is precisely this (Medium), so it is an occupied position.
  - Feasibility **3**: capture-based, moderate.
  - Strategic fit **3**: useful but not the confidence-at-collapse spine.
  - **Total: 13.**

### O12 · Reassurance-first ranking explanation
- **Problem it solves:** Phase 6, item 2.4. Ranking disclosure is written for a regulator, not the user.
- **What it does:** explains result order in plain, reassuring language aimed at comprehension rather than compliance.
- **Who it is for:** the first-time traveller at compare.
- **Why we are plausibly the ones to build it:** a product not writing to satisfy a regulator can write to be understood.
- **Scores:**
  - User impact **2**: marginal, a wording change on an existing disclosure.
  - Evidence strength **3**: the compliance-flavoured text is observed High; benefit inferred, Low.
  - Differentiation **1**: copyable in an afternoon.
  - Feasibility **4**: pure copy and presentation.
  - Strategic fit **3**: weakly on-thesis.
  - **Total: 13.**

### O13 · Persistent confidence state across stages
- **Problem it solves:** Phase 6, item 4.3. Confidence is rebuilt from zero at every stage.
- **What it does:** carries the user's readiness and anxiety context across stages so reassurance is continuous rather than re-established each time.
- **Who it is for:** the first-time traveller across the whole journey.
- **Why we are plausibly the ones to build it:** a product organised around the user rather than around per-vertical transactions could hold this state.
- **Scores:**
  - User impact **3**: potentially broad, but diffuse and hard to feel as a single win.
  - Evidence strength **2**: rests on the softest Phase 6 item, an explicit Interpretation at Low. `RISK`.
  - Differentiation **3**: unusual, but hard to demonstrate.
  - Feasibility **2**: abstract; unclear what the minimum build even is. `RISK`.
  - Strategic fit **4**: it is almost a restatement of the thesis.
  - **Total: 14.**
- `RISK:` evidence 2 and feasibility 2. The underlying problem is the one Phase 6 flagged as its softest, resting on interpretation not observation, and the build is undefined. For this to be real, it would need user research confirming that confidence resets are a felt pain, and a concrete definition of what the persistent state contains.

### O14 · Named pre-purchase safety net
- **Problem it solves:** Phase 6, item 2.1 (reassurance at book), extending the transferable pattern noted in Phase 4.
- **What it does:** names and shows a protection or safety net before booking rather than after failure, so the newcomer sees the fallback while deciding.
- **Who it is for:** the first-time traveller at book.
- **Why we are plausibly the ones to build it:** a confidence-first product can foreground reassurance the incumbents bury in policy.
- **Scores:**
  - User impact **3**: real reassurance, but narrow to the booking moment.
  - Evidence strength **3**: the buried-reassurance pattern is observed High; user impact inferred, Low.
  - Differentiation **2**: the pattern exists in the market (Hopper's named products, Medium), so it is partly occupied.
  - Feasibility **2**: an actual guarantee is a financial product with regulatory and capital requirements the plan flags. `RISK`.
  - Strategic fit **4**: strongly on-thesis for confidence.
  - **Total: 14.**
- `RISK:` feasibility 2. A real guarantee is a regulated financial product needing capital and licensing. For this to be feasible without becoming an insurer, it would have to be a presentation of an existing third-party protection rather than a Luma-underwritten one.

---

## 2. Scores at a glance

| ID | Opportunity | Impact | Evidence | Diff | Feasibility | Fit | Total | Flag |
|---|---|---|---|---|---|---|---|---|
| O3 | Inverted priority support | 4 | 3 | 5 | 3 | 5 | **20** | |
| O1 | Least-stress ranking axis | 4 | 3 | 4 | 2 | 5 | **18** | RISK feas |
| O2 | Per-option confidence label | 4 | 3 | 3 | 2 | 5 | **17** | RISK feas |
| O4 | Entry-readiness check | 4 | 3 | 3 | 3 | 4 | **17** | |
| O5 | In-destination safe+do+move | 4 | 3 | 4 | 2 | 4 | **17** | RISK feas |
| O9 | Post-booking now-what guide | 3 | 3 | 3 | 3 | 4 | **16** | |
| O6 | Travel-day companion | 4 | 3 | 2 | 2 | 4 | **15** | RISK feas |
| O7 | Reassurance summary at book | 3 | 3 | 1 | 4 | 4 | **15** | low diff |
| O8 | Where-should-I-go discovery | 3 | 3 | 2 | 3 | 4 | **15** | |
| O10 | One trip object across verticals | 4 | 3 | 3 | 1 | 3 | **14** | RISK feas |
| O13 | Persistent confidence state | 3 | 2 | 3 | 2 | 4 | **14** | RISK ev+feas |
| O14 | Named pre-purchase safety net | 3 | 3 | 2 | 2 | 4 | **14** | RISK feas |
| O11 | Supplier-agnostic trip manager | 3 | 3 | 1 | 3 | 3 | **13** | low diff |
| O12 | Reassurance-first ranking copy | 2 | 3 | 1 | 4 | 3 | **13** | low diff |

---

## 3. Ranked shortlist, top five

Ranked strictly by total. Reason each made the cut, and the caveat each carries.

1. **O3 · Inverted priority support (20).** The only opportunity that scores 5 on both differentiation and strategic fit. It is a structural position incumbents cannot copy without breaking their booking-count loyalty economics, and it is the confidence thesis expressed as strategy rather than a single feature. Cut-caveat: evidence of user pain is inferred, and "support" must mean guided flows, not staffed agents, for feasibility to hold.

2. **O1 · Least-stress ranking axis (18).** This is the business goal restated as a feature, and it scores 5 on fit and 4 on differentiation. It carries a feasibility RISK because the stress signal must be built from data Luma does not yet have. Cut-caveat: it is a data-and-research project before it is a shippable sort.

3. **O2 · Per-option confidence label (17).** Made the cut on total, but it overlaps O1 so heavily that in practice it is the display layer of the same bet and would merge with O1. Listed for transparency because it scored here; it should not be treated as a separate fifth of the roadmap.

4. **O4 · Entry-readiness check (17).** The most feasible of the high scorers, with no supplier agreements required and a clear, concrete user question answered. It is off the compare-axis spine but strongly on the confidence thesis at the prepare stage. Cut-caveat: copyable, and its edge rests on incumbents being disincentivised rather than unable.

5. **O5 · In-destination safe, do, move (17).** Strong differentiation because combining three third-party data sources is a real barrier, and it addresses a genuine multi-app burden. Cut-caveat: a feasibility RISK, since it needs safety, transit and activity data at once in a launch city.

Reading note, not a recommendation: three of the top five carry a feasibility RISK, and all five carry the same evidence caveat, that user pain is inferred not researched. The shortlist is a ranking of opportunities against the stated goal, not a decision.

---

## 4. Rejects

Ideas generated and discarded, one line each. This section is what makes the shortlist mean something.

- **Sell public transport tickets ourselves.** Rejected: Phase 6 item 3.1 is a margin-and-integration wall for generalists, and the specialists that occupy it are not yet profiled.
- **Own the post-booking failure experience as an aggregator.** Rejected: Phase 6 item 3.3, this needs inventory and supplier contracts Luma does not have; it is a model boundary, not a gap.
- **A dedicated return-journey product.** Rejected: Phase 6 item 3.4, no second transaction funds it and the evidence is absence-of-observation, not verified demand.
- **Full multi-vertical OTA (O10 as a company, not a feature).** Rejected into the not-shortlisted set: feasibility 1, the breadth trap the plan names explicitly.
- **Persistent confidence state (O13).** Not shortlisted: rests on the softest Phase 6 item and an undefined build; needs research before it is an opportunity.
- **Reassurance-first ranking copy (O12).** Not shortlisted: differentiation 1, a wording change anyone copies in an afternoon.
- **Supplier-agnostic trip manager (O11).** Not shortlisted: TripIt already occupies this position, so differentiation is 1.
- **Loyalty programme of any conventional kind.** Rejected before scoring: a tenure or spend programme reproduces the exact exclusion Phase 6 item 3.2 identifies, so it works against the thesis.
- **"Most intelligent AI assistant" positioning.** Rejected before scoring: the pattern analysis shows conversational planning is already shipped by Tripadvisor and claimed by Expedia, so it is commoditising, not differentiating.

---

## Gaps

| Gap | Why |
|---|---|
| Product context blank | Team, tech, data and distribution were not supplied. Feasibility is scored against ideation-stage reality only. Real numbers would move the feasibility column and could clear the RISK flags on O1, O4-adjacent and O6 |
| No user research | Every evidence-strength score reflects market-gap evidence, not proof of user pain. This caps the top five at evidence 3 and is the single biggest thing that would change the ranking |
| Eight competitors absent | O5 (in-destination) and the transport reject could look different once the rail, transit and accommodation specialists are profiled |
| Business model unsettled | Opportunities that imply a model (O10 an OTA, O14 an insurer) are scored against the current no-model state; a settled model would change their feasibility |
| Data-source feasibility unverified | O1, O4 and O5 assume data is licensable or public; the actual availability and cost were not checked this phase |

---

## Confidence summary

Counts are of the distinct market-evidence claims underpinning the opportunities (competitor behaviour cited). Score justifications that rest on inference are labelled in place.

| Rating | Count | What they are |
|---|---|---|
| High | 8 | Competitor behaviour observed live and cited as problem evidence: price-led sorts, buried reassurance, auth walls, silos, the assume-destination homepage, the ranking-disclosure text |
| Medium | 5 | Documentation-based problem evidence: Genius support threshold, entry-data licensing, TripIt safety and capture, Hopper named products, cross-entity structure |
| Low (inference) | 14 | Every user-impact and user-desire judgement, and the strategic-fit reasoning, which rest on the first-timer thesis rather than on research |

The Low count is high for the same reason as Phase 6: with no research, user pain is inferred. No opportunity above should be read as a decision. Phase 8 sets strategy, and would test the top five against research before commitment.
