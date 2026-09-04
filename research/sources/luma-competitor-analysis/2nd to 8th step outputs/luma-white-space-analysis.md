# Luma Competitor Benchmark · Phase 6: White-Space Analysis

**Status:** Looking for unsolved user problems, not gaps in a feature grid. Problems only. No product ideas; those are Phase 7. Every item carries a "Why nobody has solved this" line, and if one could not be written honestly the item was dropped or moved to the deliberately-unsolved section.
**Date:** 21 July 2026
**Phase:** 6 of 9
**Dataset:** the six profiled competitors, plus the Phase 3 to 5 outputs. The other eight are not yet researched, which matters most for the transport and in-destination items.

## Read this before the findings: what counts as evidence here

We hold **no user research**. That constrains the "evidence it is real" line for every problem below. Three kinds of evidence are admissible and are used:

1. **Observed friction** in a live product.
2. **Universal workaround**, where every competitor routes around the same thing the same way, which implies the underlying problem is real enough that none of them solves it head-on.
3. **Verified absence**, where a capability was checked for and not found.

What is **not** admissible without research is any claim that users *want* a thing or *feel* a pain. Wherever a finding rests on reasoning about the first-time traveller rather than on observed behaviour, it is labelled `Interpretation:` and carried at Low. This is the honest position: we can show what the market does and does not do with High confidence, and we can only infer the user's desire at Low confidence until Luma runs its own research.

Confidence tags: High (H, live product), Medium (M, docs or help centre), Low (L, marketing or inference).

---

## 1. Unsolved problems

Problems that no profiled competitor addresses well.

### 1.1 "I can only choose on price and time, never on how easy or stressful an option is"
- **Stage:** 2, plan and compare.
- **Evidence it is real:** universal workaround. Across the six, every sort resolves to price, time, distance, rating or star. Only Google Travel offers an axis outside that set, emissions, and it offers it as a genuine sort (High). Expedia and Booking.com were checked and verified to offer no sort on ease, effort, reliability or stress (High and Medium). The first-timer's actual question at this stage, "which of these will be least stressful for someone like me," has no control anywhere.
- **Evidence nobody solves it well:** verified absence of the axis across all six compare surfaces (Phase 3, load-bearing row).
- **Why nobody has solved this:** the data to rank on "ease" or "stress" is not in supplier feeds, which carry price, times, and cabin. It would have to be constructed. And the incumbents optimise result order for conversion, which correlates with price, so a stress axis competes with the metric their business runs on.
- **Confidence:** absence High. That users want it, `Interpretation:` Low.

### 1.2 "At street level in a strange city I do not know if where I am is safe, and the answer is never in the same place as what to do and how to get there"
- **Stage:** 6, in destination.
- **Evidence it is real:** universal workaround plus partial absence. Only TripIt carries a neighbourhood-safety signal, and it is app-gated and documented rather than observed (Medium). Tripadvisor carries what-to-do and street logistics (High, planner caveat). No profiled product combines safety, navigation and activities in one place; the first-timer assembles them across separate apps.
- **Evidence nobody solves it well:** across the six, no product was observed to combine the three, and safety exists in only one (Phase 5, stage 6 weak line).
- **Why nobody has solved this:** safety data is third-party and liability-sensitive (TripIt sources it from GeoSure), so a product that foregrounds it takes on reputational and legal exposure the OTAs avoid. And combining the three spans navigation, activities and safety, which are three different products with three different data sources.
- **Confidence:** absence of combination Medium (six checked, none combined). Safety-source claim Medium (docs). Users want it, `Interpretation:` Low.

### 1.3 "On the day I travel, the help I need most, when to leave and where to go, is missing unless I have paid or installed an app"
- **Stage:** 5, travel day.
- **Evidence it is real:** observed friction plus paywall. Travel-day support is mostly Unknown or Weak across the six on the open web. The one deep provider, TripIt, gates it behind Pro and the app (Medium). The transactional players position trip management in their apps behind sign-in, so it was not reachable in a signed-out web session (High that it was not reachable; the reason is stated by the products).
- **Evidence nobody solves it well:** stage 5 is the emptiest column in the Phase 5 table alongside return.
- **Why nobody has solved this:** the value of travel-day help is realised through push notifications and location, which need an app, so it is built where those live. On the web there is also no booking event on travel day, so there is no commercial pull to build it there. This item sits close to the deliberately-unsolved section and is cross-referenced in 3.5.
- **Confidence:** not-reachable-on-web High. Under-served overall Medium. Users want it, `Interpretation:` Low.

---

## 2. Badly solved problems

Solved by everyone, but poorly. Demand is proven by the fact that all of them build it.

### 2.1 "The reassurance I need at the moment of paying is buried in rate rows I have to read carefully"
- **Stage:** 3, book.
- **Evidence it is real:** observed friction. Expedia and Booking.com both deliver the two things a nervous buyer needs, the cancellation cost and "you won't be charged yet," as text inside rate rows the user must scan (High, both).
- **Evidence it is badly solved:** the reassurance exists but competes for attention with pricing, upsell and scarcity cues on the same row. It is present, not prominent.
- **Why nobody has solved it better:** the booking page is optimised for conversion and legal completeness, not for a first-timer's scan. Visible, calm reassurance competes with the same screen real estate as upsell, and upsell has a measurable revenue attached while reassurance does not.
- **Confidence:** presence-as-fine-print High. That it reads poorly for a first-timer, `Interpretation:` Low.

### 2.2 "Getting ready for the trip means signing in to a list, and the thing I actually need, whether I am even allowed into the country, is hidden or paid"
- **Stage:** 4, prepare.
- **Evidence it is real:** verified structure. For the transactional players, prepare is an auth-walled Trips surface (High, Expedia and Booking.com). Entry-requirement and visa guidance exists in only one product, TripIt, and is behind the Pro tier (Medium).
- **Evidence it is badly solved:** the trips surface is universal, so the stage is "solved," but for a first-timer with no account and no idea of entry rules it delivers little. The one product that answers the entry question paywalls it.
- **Why nobody has solved it better:** prepare has no transaction attached, so it is under-invested relative to compare and book. Entry-requirements data is licensed (TripIt cites Riskline and Basetrip), which carries a cost that pushes it behind a paid tier.
- **Confidence:** structure High, entry-data licensing Medium. User impact, `Interpretation:` Low.

### 2.3 "The homepage assumes I already know where I am going"
- **Stage:** 1, discover.
- **Evidence it is real:** universal workaround. Four of six discovery surfaces are price-led or assume a destination (Expedia deals, Hopper deals, and the search-first framing generally) (High). Only Booking.com's theme planner and Tripadvisor's interest browsing offer a non-price way in (High).
- **Evidence it is badly solved:** everyone has a discovery surface, so the stage is "solved," but most of them answer "which deal" rather than "where should I go," which is the first-timer's question.
- **Why nobody has solved it better:** the homepage's commercial job is to convert existing intent into a search as fast as possible. "Where should I go" is expensive to serve well and monetises weakly compared with a user who already has a destination.
- **Confidence:** surface behaviour High. That it underserves the first-timer, `Interpretation:` Low.

### 2.4 "The explanation of why these results are in this order is written for a regulator, not for me"
- **Stage:** 2, compare.
- **Evidence it is real:** observed. Four of the six ranked surfaces print a ranking-basis disclosure (High, Phase 4). The language names commission, sort factors and page views.
- **Evidence it is badly solved:** the disclosure is present everywhere but reads as compliance text. A first-timer is unlikely to parse "click-through rate, gross bookings and net bookings" into a reason to trust the order.
- **Why nobody has solved it better:** `Interpretation:` the disclosures appear to exist to satisfy platform-transparency regulation, so they are written for legal sufficiency, not comprehension. Low confidence, since the regulatory motive is inferred, not stated by the products.
- **Confidence:** presence High. Regulatory motive and poor comprehension, `Interpretation:` Low.

---

## 3. Deliberately unsolved

Gaps that are probably empty for a reason. Naming the reason stops us treating a wall as an open door.

### 3.1 Selling public transport tickets inside a journey product
- **Stages:** 2 and 6.
- **State:** Unknown or documented-No across the six. No profiled product was verified to sell rail, coach or transit tickets (Phase 3, whole row Unknown or No).
- **Likely reason:** low margin and fragmented supply. Ticketing integrations are per-operator, the margins are thin, and the inventory is not in the same feeds as flights and hotels. `Interpretation:` this is why the multi-vertical players stop at flights, stays, cars and attractions. Low.
- **Caveat:** the specialists that would resolve this (Trainline, Omio, Citymapper, Rome2Rio) are not yet profiled. This may be a wall for the generalists and an open, occupied market for the specialists. Do not treat the blank row as white space until they are run.
- **Confidence:** generalist absence Medium (Unknown, not verified). Reason, `Interpretation:` Low.

### 3.2 Priority or human support for a zero-booking first-timer
- **Stage:** cross-cutting, felt hardest at book and travel day.
- **State:** where priority support exists, it is gated by tenure. Booking.com's Genius grants priority support only at Level 3, which requires 15 bookings in two years (Medium).
- **Likely reason:** unit economics. Human support is expensive, and a first-timer is the most expensive user to serve and the least proven to monetise. Loyalty tenure is the mechanism the incumbents use to spend support money only on users who have already paid repeatedly. This is a structural exclusion, not an oversight.
- **Why it is a wall, not a door:** the exclusion is a direct consequence of a booking-count loyalty model. A competitor built on that model would have to break its own economics to serve the first-timer here.
- **Confidence:** Genius threshold Medium (docs). Structural-exclusion reading, `Interpretation:` Low but well-grounded in the observed threshold.

### 3.3 Owning the failure experience, for the aggregators
- **Stage:** 3 and 5.
- **State:** Google Travel and Tripadvisor hand off to third-party sellers at the point of booking (High). They deliberately do not own what happens after.
- **Likely reason:** business model. They are referral and review businesses without inventory or supplier contracts, so owning post-booking failure is outside what they are built to do. This is a deliberate boundary, not a gap.
- **Confidence:** handoff High. Reason Medium, since the model is documented.

### 3.4 The return journey as its own designed moment
- **Stage:** 7, return.
- **State:** not evidenced anywhere. Stage 7 is Unknown across all six (Phase 5). Note this is absence-of-observation, not verified absence; no product was walked through a return scenario.
- **Likely reason:** no booking event and low willingness to pay. The return leg was already sold as part of the outbound booking, so there is no second transaction to attach support to. `Interpretation:` this is why it inherits travel-day support at best and is designed for at worst. Low.
- **Confidence:** absence-of-observation High. Reason, `Interpretation:` Low.

### 3.5 Deep travel-day help delivered on the open web
- **Stage:** 5.
- **State:** cross-referenced from 1.3. On the web, travel-day help is thin; the depth lives in apps and paid tiers.
- **Likely reason:** the capabilities that make travel-day help valuable, push notifications and precise location, require an app. The web cannot deliver them, so building deep travel-day help on the web would be effort without the payload. This is a platform constraint, which is why 1.3 is recorded as underserved-on-the-surface-first-timers-use, while the "why" is a wall.
- **Confidence:** app-only positioning High (products state it). Constraint reasoning Medium.

---

## 4. Cross-stage problems

Friction that spans stages, so no single competitor owns it. Handoffs are where this lives.

### 4.1 The seam between book and prepare: "I have paid, now what"
- **Stages:** 3 to 4.
- **Evidence:** observed friction. The transactional players end the booking flow at a polished reserve step, then the next surface, prepare, is an auth-walled trips list with no guidance on what to do next (High). Nothing bridges the drop from a reassuring checkout to an empty list.
- **Why nobody owns it:** the two stages are owned by different internal goals. Book is a conversion surface; prepare is a retention surface with no transaction. The handoff between them is nobody's success metric.
- **Confidence:** structure High. "First-timer feels dropped," `Interpretation:` Low.

### 4.2 The seam between compare and book across verticals: "my trip is one thing, but I have to assemble it from four separate searches"
- **Stages:** 2 to 3, across flights, stay, transport and activities.
- **Evidence:** verified structure. Even the multi-vertical players present each vertical as a separate search and a separate booking (High, Expedia and Booking.com). A coherent trip object does not exist during compare and book; it only appears afterwards, and only TripIt assembles it, by capturing confirmations after the fact (Medium).
- **Why nobody owns it:** each vertical is a separate margin, a separate supplier relationship and often a separate corporate entity (Booking.com books flights and cars under different legal entities, High). A trip object that spans them is an integration and a commercial problem, not just a UX one.
- **Confidence:** silo structure High. Cross-entity point Medium (docs). User burden, `Interpretation:` Low.

### 4.3 Confidence as a through-line: "my nervousness is rebuilt from scratch at every stage"
- **Stages:** all.
- **Evidence:** `Interpretation:` this is a reading across the profiles, not a single observation. Reassurance is delivered per-surface, rate terms at book, reviews at compare, safety scores at destination, but never carried as a continuous state. Each stage re-establishes trust from zero.
- **Why nobody owns it:** no competitor is organised around the user's confidence as a persistent object. They are organised around transactions per vertical per stage, so confidence is a side effect of each surface rather than a thing that travels with the user.
- **Confidence:** `Interpretation:` Low throughout. This is the softest item and is labelled as such.

### 4.4 The seam between where you booked and where you manage the trip
- **Stages:** 4 to 7.
- **Evidence:** observed. The transactional players push trip management into their own apps (High). TripIt can hold the whole trip but only if the user forwards confirmations to it, a manual step (Medium). For anyone who booked on an OTA and did not adopt TripIt, the prepare-to-return arc is split across an app, an email inbox, and nothing.
- **Why nobody owns it:** each product wants the trip to live in its own surface, so there is no incentive to hand the itinerary cleanly to a neutral manager. The one neutral manager (TripIt) has to ask the user to do the stitching by forwarding emails.
- **Confidence:** app-push and manual-capture both High and Medium respectively. Fragmentation for the OTA booker, `Interpretation:` Low.

---

## Gaps

| Gap | Why |
|---|---|
| No user research | Every "this is a real user problem" claim is inference, carried at Low. Only the market's behaviour is High. Luma's own research would move these |
| Eight competitors absent | The transport ticketing wall (3.1) and the in-destination combination gap (1.2) could look different once Trainline, Omio, Citymapper and Rome2Rio are profiled |
| Return stage is absence-of-observation | No product was walked through a return scenario, so 3.4 rests on not-seen, not on verified-absent |
| Travel-day and prepare depth is documented or paid | TripIt's and Hopper's strongest relevant capabilities are Medium docs or paid tiers, not observed, so items touching stages 4 and 5 lean on documentation |
| Regulatory and unit-economics reasons are inferred | The "why nobody" lines in sections 2.4, 3.1 and 3.4 name likely reasons, labelled Interpretation, not reasons stated by the companies |
| Hopper compare stage | Results not reachable, so Hopper is absent from the stage-2 findings |

---

## Confidence summary

Counts are of the distinct evidenced claims about the market (the competitor behaviour behind each problem). The user-desire and reason claims are labelled Interpretation and counted separately.

| Rating | Count | What they are |
|---|---|---|
| High | 21 | Competitor behaviour observed directly in a live product: the sorts that exist, the auth walls, the handoffs, the fine-print reassurance, the silos |
| Medium | 9 | Behaviour resting on first-party documentation: Genius support threshold, entry-data licensing, cross-entity structure, TripIt safety and capture mechanics |
| Low (Interpretation) | 14 | Every claim that a problem is painful for the user, and every inferred "why nobody" reason. Labelled `Interpretation:` in place |

The Low count is high on purpose. With no user research, the honest state is that we can prove what the market does and cannot yet prove what the user feels. No product ideas appear above. Phase 7 converts these problems into scored opportunities.
