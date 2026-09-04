# Hands-on capture round — running learnings
Updated 2026-09-04 after Booking.com (complete for stays) and Expedia (complete for stays).
11 capture files. Executes ART-024. **Nothing here is a market claim yet — 15 competitors remain.**

## Method decision recorded, not drifted into

**Breadth-first on ONE vertical, not depth-first per competitor.** ART-024 §2.3 orders competitors
for a full per-competitor pass. In execution the accommodation journey was captured end to end on
Booking.com and Expedia before either product's other verticals.

That is deliberate and it is the stronger design: holding the vertical, the city, the dates and
the party fixed makes any difference between two products a **product** difference. Sweeping one
competitor's six verticals first would have produced six incomparable captures.

**Cost, stated plainly:** Expedia is complete for stays and untouched for flights, cars, packages,
activities and cruises. Booking.com likewise for flights, cars, attractions and airport transfers.
Neither competitor is "done". The second pass per competitor is owed and is NOT optional.

## Findings that survive across both competitors

**Ranking axes — 17 enumerated, zero about effort.**
Booking.com 11, Expedia 6. Every one is price, a quality proxy, distance, property type or an
opaque default. Both enumerated POSITIVELY by opening the control — not inferred from absence.
Two of two. This is the claim Luma's whole differentiation rests on, and it is holding so far.

**Commitment terms are filterable, never sortable.**
Both expose cancellation and payment terms as filter facets. Neither lets a traveller rank by
them. "Least committing first" is an unoccupied axis in both products.

**Loyalty gates the best rate behind accumulated bookings, and neither programme mentions a
first-time traveller.** Genius: 5 then 15 bookings in 2 years. One Key: Blue 0-4, Silver 5-14,
Gold 15-29, Platinum 30+ trip elements. Both explainer pages searched in full; no match for
first-time / new member / beginner.
**Nuance that matters:** the entry tier in both is non-empty. What is gated is the BEST rate —
and in Booking.com's case priority support, the only benefit that is help rather than price.

**Both reward booking COUNT.** Neither rewards trip completion, confidence gained, or a
disruption handled well. The open question for Luma is whether a retention unit exists that is
not transaction volume.

## Where the two diverge — these are the decisions, not the descriptions

| | Booking.com | Expedia |
|---|---|---|
| Checkout shape | staged — identity, then payment | single page — everything at once |
| Asked before payment | full postal address | first name, last name, phone |
| Tax disclosure | "Includes taxes and fees" | city tax stated per person, per night |
| Inventory, same query | 4,194 properties | 499 |
| Homepage surface | 300 links, index-like | 39 links, funnel-like |
| Insurance decline | not reached this pass | **confirmshaming** |

## The single sharpest finding

**F-22.** Expedia's insurance decline reads *"I'm willing to risk my $358.59 stay in Lisbon"*.
The market leader manufactures anxiety at the moment of payment and monetises the relief, while
Luma's stated objective is to reduce travel stress. Same economics will reach Luma. It is a
decision, not an observation.

## Findings about the METHOD, learned the hard way

1. **Two browsers, and they disagree by construction** (ART-024 §4.1b, CLAUDE.md). The client's
   Chrome is authenticated but carries extensions that inject page UI a page-context selector
   **cannot detect** — found only by looking at a screenshot. The inspector instance is signed
   out but clean and has network inspection. Every screenshot-derived claim comes from the clean
   one; every session-gated surface from the authenticated one.
2. **An empty result list is not a negative finding.** A sort-option query returned `[]` and
   `anyEffortAxis: false`. That `false` meant nothing — the selector had missed. Only opening the
   control and enumerating gave a real answer. **Absence must be positively enumerated.**
3. **The extension blocks keys it reads as session-related and redacts query strings.** Response:
   collect LESS — pathname only, which is all a site tree needs. Never work around a safety layer.
4. **Marketing copy is `Likely`, never `Verified`.** One Key was recorded from the homepage as
   earn-and-burn in contrast to Genius. The programme page showed it is BOTH a currency and a
   tenure ladder. The `Likely` label is what made that correctable instead of inherited.

## Standing constraints honoured
No account created. No credential entered. No card, billing or personal data entered — the
Expedia payment screen was recorded as page structure only. No transaction attempted.

## Owed
- Second pass per competitor for the five non-stays verticals
- Logged-out control capture on Expedia (Booking.com has one; Expedia does not)
- Empty, error, no-results and offline states on both — **none captured yet on either**
- Post-purchase and trip management on both — unreachable without a completed booking

---

# UPDATE — 2026-09-04, after 11 competitors
41 captures · 93 findings · **11 of 17 competitors touched, 0 complete.**

## The five findings that would change a design decision

**F-90 · Trainline notifies you when you QUALIFY FOR COMPENSATION.** Not when a delay happens —
when a right you already hold has been triggered. No inventory, no balance sheet, no insurance
licence; only the itinerary and the rules. Luma's scenario already assumes it holds the itinerary.
Unoccupied in air, proven in rail. **The cheapest high-value disruption feature in the round.**

**F-93 · Effort-first ranking is buildable and explicable in 26 words.** Trainline: *"We show
tickets for the fastest available journeys with the smallest number of changes, highlighting the
cheapest within these results."* Effort is the primary filter, price the tiebreaker — the inverse
of every accommodation product. The objection to "easiest first" was that effort cannot be
computed. In rail it is computed, ranked first, and explained.

**F-66/F-72 · The dark pattern is a choice, and two competitors prove it at the same moment.**
Expedia's insurance decline reads *"I'm willing to risk my $358.59 stay"*. Airbnb's reads *"¿Quieres
añadir un seguro de viaje? Sí, quiero añadirlo por 9,32 €"*. Same product category, same point in
the funnel, comparable money. One manufactures guilt; one asks.

**F-78 · Business goal 2 is unsolved, not merely unclaimed.** Airbnb holds stays, experiences and
services under one account and still presents three separate searches — moving from a dated stay
search to experiences drops the dates entirely. The barrier is not inventory or accounts. Nobody
has modelled the trip as the object the traveller actually has.

**F-88 · Three of seventeen roster entries are one company.** Booking.com, Kayak and Rentalcars are
all Booking Holdings, verified from first-party statements on two. Every "N of N competitors" claim
must state this or it overstates independence.

## Corrections made to my own earlier findings — all by capturing more, not by reasoning
- **F-25** "zero effort axes across 20" was measured on ACCOMMODATION and stated as a market claim.
  Flights rank on duration and emissions. Corrected to: *effort is ranked where it is measured and
  ignored where it is not* — which is sharper and points at Luma's real opening.
- **F-57** "nobody owns the disruption chain" — Hopper sells exactly that, as a paid app-only
  add-on. Corrected to: *ownership is sold as a product rather than being a property of the journey.*
- **F-28** "auth unlocks Track prices on Google" — it is gated per VERTICAL, not per account.
- **F-75** "control and explanation are traded off" — Kayak offers three sort tabs AND the round's
  most detailed ranking document. The trade-off framing does not survive.
- **F-71** AirCover "shown before booking" — searched results, listing and checkout: footer links
  only. A prior-round claim that did not survive contact with the product.

## Method findings, all learned the hard way
1. **An empty result is a prompt to look, never a finding.** Five occurrences: Booking.com sort
   options, Google decision panels, Kayak account UI, Airbnb listing (251 chars), Trainline
   fulfilment. Every one would have produced a false negative.
2. **Prohibition 2 nearly breached on Tripadvisor.** Two sweeps returned traveller review text.
   On a page that is 55,000 characters of user-generated content, ANY broad regex leaks quotes.
   Targeted selectors only, on that competitor and any like it.
3. **Locale drifts and must be recorded per capture** (D-004). Google served pt-BR, Trainline
   redirected /es to /en-us, Kayak served es-es. Cross-locale comparisons carry a live confound.
4. **Three products asserted three different countries** for one traveller in one afternoon —
   Toronto, Madrid, Marseille. None asked.

## Standing constraints honoured throughout
No account created. No credential entered. No card, billing or personal data entered. No
transaction attempted. Ad-tracking parameters stripped from a client-supplied URL. Consent: no
accept ever clicked on the client's behalf; where no reject affordance existed, the state was
recorded rather than resolved.

## Owed — and none of it is optional
- **No competitor is complete.** Not one of eleven.
- Trainline ticket fulfilment — the tier-3 justification, still unverified after three attempts
- Every state except one: empty, error, no-results, offline. Only one empty state captured
  anywhere in the round (F-39, Kayak's AI planner).
- Post-purchase and trip management on all eleven — unreachable without a completed booking
- Six competitors untouched: Omio, Rome2Rio, Citymapper, TripIt, American Airlines, Qatar Airways
- Roster audit: four items pending (F-45, F-54, F-85/F-88, and the airport-services comparator gap)
