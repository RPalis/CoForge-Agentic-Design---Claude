# Luma Competitor Benchmark · Phase 5: Journey Comparison

**Status:** Comparing experiences, not feature counts. A leader is named for who serves the job best at a stage, which is not always who has the most features. No proposals for what to build. Friction is noted, not solved.
**Date:** 21 July 2026
**Phase:** 5 of 9
**Dataset:** the six profiled competitors. Expedia, Booking.com, TripIt, Hopper, Google Travel, Tripadvisor. The other eight are not yet researched and are absent here, which matters most at stages where a rail, transit or accommodation specialist would likely lead (2, 6, 7).
**User held constant throughout:** the first-time traveller from Phase 1. Low confidence, needs reassurance at every step, does not yet know what "good" looks like, and cannot always name their own criteria. Every "best" call is made against that person's job, not against a feature list.

Confidence tags: High (H, live product), Medium (M, docs or help centre), Low (L, marketing or inference).

---

## Stage 1 · Dream and discover

**What the user is trying to do.** Turn a vague urge to travel into a chosen destination and rough dates, starting from nothing. For a first-timer this is hard because they have no frame of reference: they do not know what is realistic, what a place is like, or how to choose. Most discovery surfaces sort by price or popularity, which quietly assume the user already knows where they are going.

**How each competitor supports it.**
- **Expedia.** Discovery is deal-led: homepage modules and themed collections framed around price, for example "last-minute deals" and "$X off" (High). This helps someone deciding between known options, but it assumes a destination and does not answer "where should I go."
- **Booking.com.** A "Quick and easy trip planner" asks the user to pick a theme or vibe, then returns destinations by distance, alongside trending destinations and explore-country tiles (High). This is a genuine non-price entry point that needs little prior knowledge.
- **TripIt.** Nothing. The product is documented to begin only after a booking exists (Medium). A first-timer with no destination gets no help.
- **Hopper.** A Deals tab, sponsored featured destinations, and a popular-destinations list, all US cities in this session (High). Discovery is deal-and-destination led and assumes some existing interest.
- **Google Travel.** An Explore tab exists but was not walked (Unknown); a hotel "When to visit" guidance entry was seen (High). The discovery surface itself cannot be assessed.
- **Tripadvisor.** Interest-led browsing (Outdoors, Food, Culture, Water), editorial inspiration articles, Travelers' Choice "best of" lists (High), plus the AI planner that turned "3 days in Lisbon for a first-time visitor" into a structured plan (High, with the caveat that the chat was pre-populated on load).

**Who serves the first-timer best here.** **Tripadvisor.** It is the only product that offers a non-price way in (browse by interest, read editorial framing) and follows it with an AI planner that speaks to someone with no frame of reference. That maps to the first-timer's real job, "I do not know where or what," better than price-led modules. Booking.com's theme planner is a close second and is the strongest non-price entry among the transactional players.

**What is weak across the board.** Discovery is mostly price-led or assumes a destination is already chosen. Only two of six offer a "where should I go" entry that does not start from price, and one of the six (TripIt) has no discovery stage at all.

---

## Stage 2 · Plan and compare

**What the user is trying to do.** Evaluate options in each vertical and form a preference without paying. This is hard for a first-timer because comparison surfaces sort on price and time, and a newcomer cannot yet judge whether a two-hour layover is fine, which neighbourhood is central or safe, or what a fair price is. They often cannot even name the criteria to filter on.

**How each competitor supports it.**
- **Expedia.** Full search across verticals, nine flight and six hotel sorts, filters that show the price consequence of applying them, price history, a "prices typical" statement, and a ranking disclosure (High). Rich and self-explaining, but every sort resolves to price, time, distance, rating or star, so the user must still know what to filter on.
- **Booking.com.** Deep filters across about 22 groups, natural-language "Smart filters" that convert a typed request into removable chips, a ranking banner naming commission, a solo-specific review score, 18 accessibility filters, and named transit stops with distances (High). The natural-language input lowers the "know what to ask" barrier more than any other compare surface in the set.
- **TripIt.** No compare surface (Medium). It is not a plan-and-compare product.
- **Hopper.** A search form was built but results were not reachable this run (Unknown), so its comparison experience cannot be assessed.
- **Google Travel.** An emissions sort, the only non-price/time/rating axis in the set, an inline two-sentence ranking rule, a price judged against its usual range, a list of 18 sellers showing price dispersion, and a printed statement of where its own data stops (High). It explains its own reasoning better than anyone.
- **Tripadvisor.** Reviews with counts and sample size, ranked lists with a printed basis, travel-party tags on reviews, and a named human expert mini-guide that answers first-timer questions like terrain, footwear and weekday-versus-weekend timing, plus the AI planner (High).

**Who serves the first-timer best here.** **Tripadvisor**, narrowly, for this specific user. Google Travel is the strongest at decision transparency and would lead for a confident comparison shopper, but the first-timer's problem is not transparency, it is not knowing what good looks like. Tripadvisor's layered reviews and its human expert answer questions a price-sort cannot, which is closer to the newcomer's actual job. What would settle it is a usability test with first-timers on whether they felt able to choose confidently, which no desk research can supply.

**What is weak across the board.** Only one product (Google Travel) lets a user rank on anything but price, time or rating, and none lets a user sort on ease, effort or stress. Comparison still assumes the user can name their own criteria.

---

## Stage 3 · Book

**What the user is trying to do.** Commit to one option and pay without fear of making a mistake. For a first-timer the anxiety is concrete: hidden fees, non-refundable traps, and "have I done this right."

**How each competitor supports it.**
- **Expedia.** A priced refundable-versus-non-refundable choice per room, "Reserve now, pay later," a "You won't be charged yet" caption, all-in pricing, and rate-restriction disclosure (High). Reassurance is delivered as terms the user can see before committing. The checkout itself was not walked.
- **Booking.com.** A free-cancellation date and "pay nothing until" line per rate, cumulative quantity pricing, "You won't be charged yet," all-in "includes taxes and fees," and a documented overbooking remedy (High). The same reassurance-as-visible-terms pattern, executed well.
- **TripIt.** Sells nothing (High). There is no booking stage.
- **Hopper.** An OTA flow plus named paid flexibility products (Cancel for Any Reason, Change for Any Reason, Premium Disruption Assistance), stated not to be insurance (Medium). Reassurance is monetised as add-ons. The base booking flow was not reachable, so its clarity is Unknown.
- **Google Travel.** Hands off to third-party sellers, showing a "Lowest total price" label and disclosing which sellers lack bag-fee data (High). It reduces uncertainty before the handoff but does not own the checkout, so the fear-reducing part of booking happens on someone else's site.
- **Tripadvisor.** Experiences book via Viator, hotels hand off to sellers, and scarcity cues are attributed to Viator's data (High). As with Google, the actual commitment is a handoff.

**Who serves the first-timer best here.** **No clear leader between Expedia and Booking.com.** Both make the two things a first-timer fears, the cancellation cost and whether they are being charged now, visible before selection, and they use the same pattern to the same standard. The evidence does not separate them. What it does separate is model: the two transactional players own the reassuring moment, while the aggregators (Google, Tripadvisor) hand the user off at the point of highest anxiety.

**What is weak across the board.** The products that own checkout bury the reassurance inside rate rows the user has to read carefully. The aggregators hand off at the moment of commitment, so the failure experience lands on a third party the user did not choose.

---

## Stage 4 · Prepare

**What the user is trying to do.** Get everything in order before leaving: confirmations in one place, entry requirements understood, nothing forgotten. A first-timer does not know what they are allowed to bring or whether they need a visa, and fears forgetting something they did not know to remember.

**How each competitor supports it.**
- **Expedia.** A Trips surface behind an auth wall (High). Contents unknown; a first-timer must create an account to reach any prepare surface.
- **Booking.com.** A Trips surface behind an auth wall (High). The same.
- **TripIt.** This is its home stage. Forward-an-email or inbox-sync capture builds one itinerary from any supplier, plus calendar sync, sharing, document storage, entry-requirements and visa guidance, and a passport-renewal reminder (Medium, much of it Pro and app). It is supplier-agnostic and answers "what do I need and am I allowed in."
- **Hopper.** A My Trips lookup (High). Shallow.
- **Google Travel.** A saved bookmark and a Share control (Partial High). Shallow.
- **Tripadvisor.** A saved list and the ability to share an AI plan (Partial High). Shallow.

**Who serves the first-timer best here.** **TripIt**, and this is the clearest "fewer features, better at the stage" case in the whole comparison. It has none of the OTAs' booking depth, but it captures confirmations from anywhere, tells the user their visa, health and entry requirements before they travel, and reminds them about their passport. That maps directly to the newcomer's "am I forgetting something, am I allowed in" anxiety. The caveat is that most of this is documented and Pro-gated, not seen in operation.

**What is weak across the board.** For the transactional players, prepare is an auth-walled trips list with unknown contents. Entry-requirement guidance, the thing a first-timer most needs here, exists in only one product and is behind a paid tier.

---

## Stage 5 · Travel day

**What the user is trying to do.** Get from home to the destination without missing anything: know when to leave, find the gate, handle a delay, and know what to do if something breaks. For a first-timer this is the peak-anxiety stage.

**How each competitor supports it.**
- **Expedia.** Not reachable signed out (Unknown); trip management is positioned in the app.
- **Booking.com.** A documented overbooking remedy only (Medium); no day-of surface was observed.
- **TripIt.** Deep, if you pay. Flight status, Go Now (computed departure timing from traffic and flight status), interactive indoor airport maps with walking directions across roughly 110 airports, terminal, gate and baggage reminders, and Risk Alerts for disruption (Medium, Pro, app). It is the most complete travel-day support in the set, though documented rather than observed and Pro-gated.
- **Hopper.** Paid Premium Disruption Assistance, a same-day rebook or refund (Medium). Narrow to disruption, and paid.
- **Google Travel.** None; it is an aggregator (Medium).
- **Tripadvisor.** Not evidenced (Unknown).

**Who serves the first-timer best here.** **TripIt**, on the documented evidence. Go Now, indoor wayfinding and gate and baggage reminders address the exact moments a first-timer panics: when do I leave, where is my gate, where are my bags. The strong caveat is that this is Medium-confidence documentation of an app, Pro-gated, and not seen in operation. If the bar is restricted to what is free and verified, then **No clear leader**, because the free tiers and the transactional players show almost nothing here.

**What is weak across the board.** Travel-day support is thin unless you pay: TripIt Pro or a Hopper add-on. The transactional players put it in the app behind sign-in, so it could not be reached on the open web. For the first-timer this is the highest-anxiety stage and the least served.

---

## Stage 6 · In destination

**What the user is trying to do.** Get around an unfamiliar city and do things, at street level, with confidence: navigate, judge which areas are safe, use the transit system, and find what is worth doing.

**How each competitor supports it.**
- **Expedia.** Landmark and transit distances on property pages (High). Static context, not active in-destination help.
- **Booking.com.** Named transit stops with distances on property pages, an Attractions vertical, and a Things to do module (High). Useful reference rather than navigation.
- **TripIt.** Navigator (options between two points), Neighborhood Safety Scores (1 to 100, separate day and night, six sub-categories including women's and LGBTQ safety), and declared Personal Risk Level flagging (Medium, app). The safety layer is the only street-level reassurance signal in the set.
- **Hopper.** Not evidenced (Unknown).
- **Google Travel.** Things To Do was not reachable in scope (Unknown).
- **Tripadvisor.** Deep things-to-do with ratings and distances, and an AI plan that gave concrete street-level logistics, naming the local transit card and how to avoid ticket friction (High, planner caveat).

**Who serves the first-timer best here.** **No clear leader**, because the two strongest split cleanly. Tripadvisor owns "what to do and how to move around," with rated things-to-do and an AI plan that gave a newcomer real transit logistics. TripIt owns "is this area safe," with the only neighbourhood-safety signal in the set. No single product does both, and which one leads depends on which anxiety dominates for the first-timer in the destination, which is testable with users and was not settled here.

**What is weak across the board.** Nobody combines what-to-do, how-to-get-there-at-street-level, and is-it-safe in one place. Safety scoring exists in only one product and is app-gated. Two of six could not be assessed at this stage at all.

---

## Stage 7 · Return

**What the user is trying to do.** Get home. The job resembles travel day but with trip fatigue: manage the return leg, re-check bags, catch the flight back.

**How each competitor supports it.**
- **Expedia, Booking.com, Hopper, Google Travel, Tripadvisor.** Not separately evidenced (Unknown). None was walked through a return-day scenario.
- **TripIt.** Return legs are tracked as part of the itinerary, and the travel-day Pro features apply to the return as well (Medium, implied from the travel-day evidence).

**Who serves the first-timer best here.** **No clear leader.** Only TripIt plausibly covers the return, and only as an extension of its travel-day features, which are themselves documented rather than observed. What would settle it is a walked return-day session for each product, which this run did not include.

**What is weak across the board.** The return leg is essentially undesigned across the set. At best it inherits whatever travel-day support exists. No product treats "getting home" as its own moment with its own reassurance.

---

## Stage 8 · After the trip

**What the user is trying to do.** Close the loop: leave reviews, settle expenses, claim anything owed, keep the memories. A first-timer usually does not know they might be owed compensation for a delay, or that reviewing has any point.

**How each competitor supports it.**
- **Expedia.** Verified reviews (High). Standard review collection.
- **Booking.com.** Review collection within a stated window (High). Standard.
- **TripIt.** Flight ratings, AirHelp compensation-eligibility alerts, carbon tracking, and travel stats (Medium). The compensation eligibility is distinctive and squarely pro-user.
- **Hopper.** A referral program (High). Thin at this stage.
- **Google Travel.** Emissions are shown at compare time but there is no personal after-trip tracking (Unknown for this stage).
- **Tripadvisor.** Reviews are the core and feed rankings and Travelers' Choice awards, closing a loop from reviewing to influence, and Rewards ties reviewing to a balance (High).

**Who serves the first-timer best here.** **TripIt**, for this user specifically. Being told "you may be owed compensation for that delay" is concrete money and reassurance a newcomer would not discover on their own. Tripadvisor's review loop is genuinely strong, but it serves the platform and the community more than it serves the individual first-time traveller, whereas TripIt's compensation alert serves the traveller directly.

**What is weak across the board.** After-trip is mostly review collection. Only one product surfaces compensation rights, and it is a third-party partnership feature rather than a core capability.

---

## Stage strength table

Cells: Strong / Adequate / Weak / Unknown, with confidence. Strong means the stage's job is served well for the first-time traveller. Weak includes "serves this stage poorly" and "not designed for this stage." Unknown means not reachable or not evidenced this run, not verified absence.

| Competitor | 1 Discover | 2 Compare | 3 Book | 4 Prepare | 5 Travel day | 6 In destination | 7 Return | 8 After |
|---|---|---|---|---|---|---|---|---|
| Expedia | Adequate (H) | Strong (H) | Strong (H) | Weak (H) | Unknown | Weak (H) | Unknown | Adequate (H) |
| Booking.com | Adequate (H) | Strong (H) | Strong (H) | Weak (H) | Weak (M) | Adequate (H) | Unknown | Adequate (H) |
| TripIt | Weak (M) | Weak (M) | Weak (H) | Strong (M) | Strong (M) | Adequate (M) | Adequate (M) | Adequate (M) |
| Hopper | Adequate (H) | Unknown | Adequate (M) | Weak (H) | Adequate (M) | Unknown | Unknown | Weak (H) |
| Google Travel | Unknown | Strong (H) | Adequate (H) | Weak (H) | Weak (M) | Unknown | Unknown | Weak (M) |
| Tripadvisor | Strong (H) | Strong (H) | Adequate (H) | Weak (H) | Unknown | Strong (H) | Unknown | Adequate (H) |

Reading notes, not conclusions:
- The three "Strong" clusters sit at different stages for different products: Expedia and Booking.com at compare and book, TripIt at prepare and travel day, Tripadvisor at discover, compare and in-destination.
- Prepare is Weak for four of six because it is auth-walled or shallow. The one Strong (TripIt) is Medium-confidence documentation.
- Travel day and return are the emptiest columns: mostly Unknown or Weak, and the one Strong (TripIt, travel day) is paid and documented.
- TripIt's "Weak" at book is by design, it sells nothing, which is the clearest illustration that a Weak cell is not always a failing, just a product that does not play that stage.

---

## Gaps

| Gap | Why |
|---|---|
| Eight competitors absent | The rail, transit and accommodation specialists are not profiled. They would most likely change the leader at stages 2, 6 and 7 |
| Hopper compare stage | Flight results were not reachable, so Hopper is Unknown at compare and cannot be ranked there |
| Google Travel discover and in-destination | Explore and Things To Do were not reachable in scope, so both cells are Unknown |
| Google Travel signed-in | Walked signed in while others were signed out; its compare and after-trip cells are not strictly comparable |
| Tripadvisor travel day and return | Not evidenced; the planner caveat also applies to its in-destination and discover strengths |
| TripIt and Hopper depth | Their strongest stages (prepare, travel day, disruption) are Medium documentation or paid tiers, not seen in operation |
| No return-day sessions | No product was walked through a return scenario, so stage 7 is Unknown almost everywhere |
| No user evidence | Every "best" call is a reasoned judgement against the first-timer's job from desk research, not from testing with first-time travellers |

---

## Confidence summary

Counts are of the distinct evidenced support-claims across the eight stages (leader calls and interpretations excluded from the count).

| Rating | Count | What they are |
|---|---|---|
| High | 30 | Stage support observed directly in a live product |
| Medium | 11 | Stage support resting on first-party documentation, principally TripIt and Hopper help pages and Booking.com's overbooking policy |
| Low | 0 | No stage-support claim rests on marketing or inference; the one prior vendor claim (Expedia Romie) was not used to credit any stage |

Leader calls are judgements against the user's job, stated as such, and three of the eight stages are recorded as "No clear leader" where the evidence did not support naming one. No proposal for what to build appears above.
