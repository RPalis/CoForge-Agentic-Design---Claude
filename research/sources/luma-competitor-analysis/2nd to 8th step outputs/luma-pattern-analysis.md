# Luma Competitor Benchmark · Phase 4: UX Pattern Analysis

**Status:** Interpretation permitted this phase, but every reading points back to a specific observation from Phase 2 or 3. No solutions, opportunities, or product recommendations. Ideas that occurred are parked, unelaborated, at the end.
**Date:** 21 July 2026
**Phase:** 4 of 9
**Dataset:** the six profiled competitors. Expedia, Booking.com, TripIt, Hopper, Google Travel, Tripadvisor. The other eight in the plan are not yet researched, so "everyone" below means "all or nearly all of these six," not the whole market. This matters most for the convergence claims in section 1.

A note on the word "everyone." Three of the six are transactional sellers or aggregators that run a compare surface (Expedia, Booking.com, Google Travel), and Tripadvisor runs a ranked review surface. TripIt sells nothing and has no compare surface, and Hopper's results were not reachable this run. So a convention can be near-universal among the four that have a compare surface while being absent-by-design or unverified in the other two. Each pattern states its denominator.

---

## 1. What does everyone do (table stakes)

### 1.1 User ratings shown with their review count
**Pattern:** every product that surfaces inventory shows a numeric rating and, beside it, the number of reviews behind that rating.
**Who:** Expedia (High), Booking.com (High), Google Travel (High), Tripadvisor (High). Four of the four with a review surface. TripIt has no reviews (documented, Medium). Hopper reviews not reached (Unknown).
**Expectation created:** a traveller expects to see how many people stand behind a score, not just the score. Booking.com and Tripadvisor go further and print the sample size behind sub-scores too (High).
**Cost of breaking it:** showing a bare score without its count would read as hiding something. On a compare surface it is the minimum credible unit.

### 1.2 Sort and filter on a results list
**Pattern:** results come with a sort control and a filter rail.
**Who:** Expedia (9 flight, 6 hotel sorts; High), Booking.com (11 hotel sorts, ~22 filter groups; High), Google Travel (6 sorts, filter chips; High). Three of the three transactional or aggregating compare surfaces. Tripadvisor shows ranked lists but an explicit user sort control was not confirmed (Partial, Medium).
**Expectation created:** the user expects to re-order and narrow a list themselves rather than accept the default order.
**Cost of breaking it:** a results page with no sort or filter would feel broken to anyone who has used a travel site.

### 1.3 A printed ranking-basis disclosure on ranked surfaces
**Pattern:** the product states, on or one click from the results, what determines the default order.
**Who:** Expedia (links a ranking page, states compensation influences hotel ranking; High), Booking.com (banner above the first result naming commission; High), Google Travel (inline two-sentence rule; High), Tripadvisor (attractions ranking basis printed; High). Four of four ranked surfaces.
**Expectation created:** on European-facing travel surfaces, a disclosure of ranking factors is now the norm rather than the exception.
**Interpretation:** this convergence is consistent with EU platform-transparency regulation rather than with independent design choices. Confidence Low.
**Cost of breaking it:** beyond user trust, likely a compliance exposure. Not a free choice.

### 1.4 A saved or trips surface, usually behind sign-in
**Pattern:** a place to hold saved items or booked trips, gated by an account.
**Who:** Expedia (Trips, auth-walled; High), Booking.com (Trips, auth-walled; High), Hopper (My Trips; High), Google Travel (saved bookmark; Partial High), Tripadvisor (saved heart; Partial High), TripIt (the whole product; Medium). Six of six in some form.
**Expectation created:** the user expects their selections and bookings to persist in one place tied to an account.
**Cost of breaking it:** losing selections between sessions is a basic failure. The auth wall is itself near-universal, which is worth noting for a first-time user who has no account yet.

### 1.5 All-in pricing among the transactional players
**Pattern:** prices shown inclusive of taxes and fees, and labelled as such.
**Who:** Expedia ("Total with taxes and fees"; High), Booking.com ("Includes taxes and fees"; High), Google Travel ("prices include required taxes + fees"; High). Three of three. Two of them (Expedia, Booking.com) actively market it as positioning (High).
**Expectation created:** the headline number should be close to the number paid.
**Cost of breaking it:** a price that balloons at checkout now reads as a dark pattern, and two competitors explicitly campaign against it.

### 1.6 Cookie consent with a decline path
**Pattern:** a first-run consent choice that offers refusal, not only acceptance.
**Who:** Booking.com (Decline as a primary control; High), Hopper (Deny with equal weight; High), TripIt (Reject All; High). Three of three where a modal was seen. Expedia banner dismissed (Partial Medium). Google and Tripadvisor no modal observed (Unknown).
**Expectation created:** a genuine refusal option, not a buried one.
**Cost of breaking it:** compliance exposure in the EU, plus the modal is the first interaction a first-time user has.

---

## 2. What is emerging (minority, recent)

### 2.1 Conversational AI trip planning as a distinct surface
**Who:** Tripadvisor ships one, observed live, "Plan with AI", which produced a first-timer itinerary and asked pace and scope follow-ups (High, with the caveat that the chat was pre-populated on load). Expedia markets one, "Romie", but it is alpha, app-only and reproduced from the newsroom, not seen shipped on web (Low, vendor claim).
**Maturity:** one looks shipped and interactive; one looks announced. Two of six.
**Trend confidence:** Medium. Two independent players plus a wider industry move make this more than a one-off, but only one was verified as a running product.

### 2.2 AI question-answering scoped to one task, and labelled
**Who:** Expedia property "Have a question?" returned a source-attributed answer with an AI disclaimer and feedback controls (High). Booking.com property "Ask a question" form observed, answer not submitted (Partial High). Both are Beta-badged.
**Maturity:** narrow, single-purpose, both explicitly Beta. Two of six.
**Trend confidence:** Medium. Two of the largest players ship the same narrow pattern, both labelled as experimental.

### 2.3 Natural-language input converted into structured, editable controls
**Who:** Booking.com Smart filters turned a free-text request into removable filter chips (High). Google Travel accepts a natural-language deep link that resolves to a structured search (Partial High).
**Maturity:** Booking.com's is a visible, reversible on-page feature; Google's is a URL behaviour. Two of six.
**Trend confidence:** Low to Medium. Two instances, and they are not quite the same mechanism.

### 2.4 A non-price, non-time decision axis surfaced on results
**Who:** Google Travel shows emissions per result and offers it as a sort (High). TripIt tracks carbon, but as a post-trip stat, not a compare axis (Medium). Booking.com and Expedia were verified to offer no such sort (High and Medium).
**Maturity:** one live sort, one adjacent stat. One of six as an actual compare axis.
**Trend confidence:** Low. A single verified instance. Whether it generalises beyond emissions to other axes such as ease or effort is not evidenced anywhere.

### 2.5 Accessibility exposed as filterable inventory
**Who:** Booking.com exposes 18 accessibility filters split across property and room (High). Google Travel shows "Accessible" and "Wheelchair accessible" amenity tokens (Partial High). Expedia has a property "Accessibility" anchor, not opened (Partial High). Three of six.
**Maturity:** one deep, two shallow. Booking.com also publishes an accessibility statement citing European Accessibility Act scope (Medium).
**Trend confidence:** Medium, and likely regulation-driven. Interpretation: the EAA timing lines up. Confidence Low.

### 2.6 Named, paid flexibility and disruption products
**Who:** Hopper sells a named family, "Flexible Travel Services" (Cancel for Any Reason, Change for Any Reason, Premium Disruption Assistance), documented and stated not to be insurance (Medium). Expedia offers a trip-protection add-on at checkout (Partial High). Two of six.
**Maturity:** Hopper's is a defined product line; Expedia's is a checkout add-on.
**Trend confidence:** Low to Medium. Two instances, and both are monetisation of reassurance rather than a shared UX pattern.

### 2.7 Declared-tolerance personalisation
**Who:** TripIt's Personal Risk Level lets the user set a risk threshold, then flags plans that exceed it (Medium). One of six.
**Maturity:** a single documented instance, app and account gated, not seen in operation.
**Trend confidence:** Low. One instance. Recorded here because it is the only personalisation mechanism in the set that is set by the user rather than inferred from behaviour, which makes it distinct even if it is not yet a trend.

---

## 3. What appears to work well (evidence beyond taste)

The bar here is evidence beyond design judgement: the pattern is widely copied, it removes a step, or user reviews reference it. I found no user reviews referencing a product-interface pattern. The Tripadvisor reviews I read reference tour guides and venues, not the interface (High that the reviews exist, and that they are about venues not UI). So the two admissible kinds of evidence below are adoption and step-removal.

### 3.1 Ranking-basis disclosure, on evidence of adoption
**Evidence:** copied by four of four ranked surfaces (section 1.3). Adoption is the evidence that it has become standard practice.
**What it does not tell us:** whether users read it or act on it. That would be Interpretation, Low.

### 3.2 Review count printed beside every score, on evidence of adoption
**Evidence:** universal on the four review surfaces, and extended to sub-score level by two of them (section 1.1).
**Interpretation:** pairing a score with its sample size lets a reader weight it. That it helps is design judgement. Confidence Low.

### 3.3 Price judgement paired with its reference range, on evidence of step-removal
**Evidence:** Google Travel states a price is "low" and prints the usual range that makes it low; Expedia states prices are "typical" (both High). This removes the separate step of the user working out whether a price is good.
**Adoption:** two of six show a version of it, so it is converging, not universal.
**Interpretation:** that it reduces decision effort is plausible but is judgement. Confidence Low.

### 3.4 Email-forward itinerary capture, on evidence of step-removal
**Evidence:** TripIt's forward-to-an-address and inbox-sync capture is documented to remove the copy-paste-and-retype step of building an itinerary (Medium, help centre). The step it removes is explicit in the mechanism.
**Caveat:** documented, not seen in operation. The claim is about the mechanism, not the polish.

### 3.5 Natural-language filters shown as removable chips, on evidence of step-removal plus reversibility
**Evidence:** Booking.com converted a typed request into two filter chips and moved the result count, and the chips were removable (High). It removes re-entry and keeps the interpretation reversible.
**Interpretation:** that visible, reversible interpretation is better for trust than an opaque result is judgement. Confidence Low.

**Not admissible as "works well":** Tripadvisor's layered social proof plus human expert, and Hopper's onboarding psychology. Both are on-thesis and interesting, but I have no adoption evidence (each is a single instance), no step-removal claim I can ground, and no user-review evidence. Any statement that they "work" would be taste. Recorded as Interpretation, Low, and nothing more.

---

## 4. Where the market is inconsistent (unsettled problems)

These are the places where the six solve the same problem in incompatible ways. Incompatibility means the market has not converged, which means the question is genuinely open.

### 4.1 The business model itself
**The split:** transactional sellers that own checkout (Expedia High, Booking.com High, Hopper Medium), a referral aggregator that hands off to third parties (Google Travel High), a review-and-experiences platform that books via a subsidiary (Tripadvisor via Viator High), and a product that sells nothing at all (TripIt High).
**Why it matters:** the model determines who owns the failure experience and whether the product can even show a price. Three incompatible answers, all live.

### 4.2 How honestly ranking discloses commission, and about which vertical
**The split:** Booking.com names commission in the banner itself and states it influences accommodation ranking (High). Expedia states compensation influences hotel ranking but not flight ranking (High). Google Travel states compensation does not influence flight ranking (High).
**Why it matters:** all three disclose, but they disclose different relationships between money and order, and they draw the line at different verticals. The convention to disclose has settled; what to disclose has not.

### 4.3 Whether to advise the user when to buy
**The split:** Hopper markets a book-or-wait prediction (Partial Medium, app-only). Google Travel shows price history and insight and leaves the decision to the user (High). Expedia states prices are "typical" without advising (High).
**Why it matters:** one product takes a position on the user's behalf, one informs and steps back, one only contextualises. Three different philosophies about how much the product should decide.

### 4.4 Whether a user can rank on anything but price, time, or rating
**The split:** Google Travel offers an emissions sort (High). Expedia and Booking.com were verified to offer no sort beyond price, time, distance, rating and star (High and Medium). TripIt lets a user flag plans against a declared risk threshold, which is not a sort and not on a compare surface (Medium).
**Why it matters:** this is the axis the benchmark plan singled out. Across the six, the market has not settled whether choosing on effort, ease, reliability, or any axis other than price and time and rating is even a thing a travel product does. One emissions sort is the whole of the evidence for "yes."

### 4.5 What personalisation is based on
**The split:** behavioural, inferred from history and loyalty status (Expedia Medium, Booking.com Medium, Google Travel signed-in Partial Medium), versus declared or profile-based, set by the user or read from a stored passport (TripIt Medium, Booking.com declared occupancy Partial High).
**Why it matters:** the same word, personalisation, covers two opposite mechanisms, one that watches the user and one that asks them. Booking.com does both.

### 4.6 Whether loyalty includes a first-time user
**The split:** tenure-gated, earned by accumulated bookings (Booking.com Genius, 5 and 15 bookings, High; Expedia tier-gated VIP savings, Medium) versus flat or absent (Google Travel none, High; TripIt none, Medium).
**Why it matters:** the two loyalty designs treat a zero-booking user in opposite ways. One structurally excludes them, one has no programme to exclude them from. Unsettled.

### 4.7 How disruption is handled
**The split:** a paid same-day rebooking product (Hopper Premium Disruption Assistance, Medium), free push alerts about disruption (TripIt Risk Alerts, Medium), and a documented operational overbooking remedy (Booking.com, Medium).
**Why it matters:** the same job, keeping the trip on track when something breaks, is monetised, notified, or handled as policy, depending on the product. No shared pattern.

### 4.8 What "AI" actually refers to
**The split:** a shipped, narrow, labelled Q&A box (Expedia High, Booking.com Partial High), a shipped conversational planner (Tripadvisor High, with caveat), and a marketed but unshipped assistant (Expedia Romie, Low).
**Why it matters:** the same "AI" banner spans a form that answers one question, a planner that holds a conversation, and a press release. For a benchmark, this is the field where the gap between claim and shipped reality is widest.

### 4.9 How an itinerary gets filled
**The split:** capture from anywhere by forwarding a confirmation (TripIt Medium) versus a trips surface that only holds what you booked on that platform (the OTAs, High).
**Why it matters:** one treats the itinerary as supplier-agnostic, the others treat it as a record of their own sales. Incompatible assumptions about what a trip is.

---

## Parked ideas

Recorded without elaboration, per the guardrail. Not proposals.

- A sort or filter axis for ease, effort, or stress, not only price and time.
- Declared-tolerance flagging applied beyond safety.
- A named safety net shown before booking rather than after failure.
- Supplier-agnostic itinerary capture as a confidence surface.
- Ranking disclosure reframed as reassurance rather than compliance.
- Price judgement always paired with its reference range.
- Loyalty or priority that does not require accumulated bookings.
- A conversational planner that asks about pace before committing.

---

## Gaps

| Gap | Why |
|---|---|
| "Everyone" is six, not fourteen | Kayak, Skyscanner, Airbnb, Rentalcars.com, Trainline, Omio, Citymapper, Rome2Rio are not profiled. Convergence claims in section 1 could weaken or strengthen when they are added |
| Hopper decision-support patterns | Flight results were not reachable, so Hopper is absent from the sort, filter, ranking and non-price-axis findings |
| Google Travel signed-in | Walked signed in while others were signed out. Its personalisation and ranking observations are not strictly comparable |
| Tripadvisor conversational planner | Observed live but pre-populated on load, not driven from a clean start. The section 2.1 and 4.8 claims carry that caveat |
| App-only and documented-only features | TripIt travel-day and in-destination patterns, and Hopper's flexibility products and price prediction, are Medium (docs), not seen in operation |
| No user-review evidence for interface patterns | The only user reviews read were about venues and guides, so section 3 rests on adoption and step-removal, not on users referencing a feature |
| Expedia Romie | Vendor claim, Low. Treated as unshipped for pattern purposes |

---

## Confidence summary

Counts are of the distinct evidenced claims in this analysis (interpretations counted separately).

| Rating | Count | What they are |
|---|---|---|
| High | 34 | Patterns observed directly in a live product across the six profiles |
| Medium | 12 | Patterns resting on first-party documentation, principally TripIt, Hopper and Booking.com help pages, plus trend-confidence judgements where two independent players were seen |
| Low | 8 | Labelled interpretations (four in the analysis), the Expedia Romie vendor claim, and the three regulation-attribution readings |

Every interpretation in the document is labelled `Interpretation:` and carried at Low. No opportunity, recommendation, or product direction appears above. Ideas that arose are parked, unelaborated.
