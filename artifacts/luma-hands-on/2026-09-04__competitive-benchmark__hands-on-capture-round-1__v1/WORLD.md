# Luma — world document
The retrieval corpus for the competitor round. **Generated from the capture files, not written over
them.** `WORLD.json` carries the same content as 117 self-contained chunks for retrieval; this file
is the human-readable companion. If either disagrees with a capture file, **the capture file wins**.

---

## 0. How to use this, and how it can mislead you

**This is an index of evidence, not synthesis.** No claim in it has passed Gate A.

Every chunk carries its own `confidence` and `scope_limit`. Those are not decoration. The failure
mode of a retrieval corpus is a true sentence arriving without the caveat that made it true — so a
chunk retrieved from `WORLD.json` should never be quoted without them.

**Coverage is uneven and the unevenness is not random.**

| | captured | of |
|---|---|---|
| journey stages | 25 | 136 (18%) |
| booking types | 47 | 68 (69%) |
| states | 8 | 119 (6%) |
| walked to payment gate | 6 | 17 |
| captured on both browser surfaces | 4 | 17 |

Findings about **discovery, comparison, ranking, loyalty and pricing** rest on broad coverage.
Findings about **post-purchase, disruption and failure states** rest on very little — and that is
precisely where Luma proposes to differentiate. Weight accordingly.

---

## 1. The product this is for

From `Luma test project scenario.pdf` — the only source for anything about Luma.

**Luma** is an AI travel companion at **ideation**. Nothing is built. Available on iOS, Android and
web. Its stated objective: *"Create the world's most intelligent travel companion by reducing travel
stress and helping users confidently navigate every stage of their journey."*

**Eight journey stages**: Dream & discover → Plan & compare → Book → Prepare → Travel day →
In destination → Return → After the trip. Stages 2 and 3 each cover four booking types: flights ·
on-site transport · on-site accommodation · on-site activities.

**Five primary users**: leisure · frequent business · families with children · international ·
first-time travellers.

**Eight business goals**, including +20% completed bookings, more multi-type trips, more on-site
experience and airport-service usage, and becoming the primary app before, during and after travel.

**Constraints**: mobile-first · native iOS and Android · WCAG 2.2 AA · multi-language · works
offline where possible · a design system already exists · 8-week discovery.

---

## 2. The finding that should govern the rest

> **The more a product can sell you, the less of the real answer it shows.**

This is not one observation; it is the shape of the whole market as captured.

| | shows | decision layer |
|---|---|---|
| **Transacts** — Booking.com, Expedia, Iberia | only what it sells | none |
| **Hands off** — Google, Kayak, Skyscanner | what it can refer | rich |
| **Sells nothing** — Rome2Rio, TripIt | what cannot be monetised at all | its entire product |

Rome2Rio shows you driving your own car and sharing someone else's. TripIt sees your whole trip
*because* it sells none of it. Booking.com has the widest inventory in the roster and no decision
layer at all.

**Luma proposes to do both halves. No observed competitor does.** Whether one product can hold both
is the central unanswered question of this round.

*Corroborating detail*: Booking.com and Kayak share a parent — Booking Holdings, with Rentalcars —
and run opposite models deliberately. That strengthens this as a business-model claim and weakens
any count that treats the three as independent firms.

---

## 3. Where the market is weak, with evidence

**Effort is ranked where it is measurable and ignored where it is not.**
Flights and rail rank on duration, changes, emissions. Accommodation: **20 enumerated ranking axes
across four products, zero about effort**. Activity duration exists only inside seller-written
titles. Luma's opening is not inventing an effort axis — three already exist in three units (time,
carbon, calories) — it is computing one where the data does not yet exist.

**Nobody addresses a first-time traveller.**
Four loyalty programmes, four full-text searches, zero mentions. Across 17 competitors and 121
findings, the roster addresses **families** (Iberia) and **international travellers** (TripIt Pro).
Luma's stated primary user is addressed by nothing. That is either the whole opportunity or a
warning that the segment does not sustain a product.

**The moment of most need is the hardest to navigate to.**
Iberia names the operational-disruption regime and provides no link. Qatar: 289 homepage links,
zero. Booking.com disclaims flight liability outright. Five findings from five angles converge here.

**Business goal 2 is unsolved, not unclaimed.**
Airbnb holds stays, experiences and services under one account and still drops your dates moving
between them. The barrier is not inventory or accounts — it is that nobody models the trip as the
object the traveller actually has.

---

## 4. Where the market is strong, and Luma starts behind

- **Live flight tracking** — Kayak gives it away free and unbundled.
- **Price tracking and history** — Google gives them away free.
- **Alerts, gate info, entry requirements** — TripIt Pro sells them as a subscription.
- **Disruption rebooking** — Hopper sells it per trip, app-only.
- **AI planning** — five of seventeen ship it. It is table stakes, not a differentiator.

Four items on Luma's Core Features list are already free or already sold by products that never
touch the booking. Luma proposes to bundle all of it with the booking, and **nobody does that** —
which may be a business-model constraint rather than an oversight.

---

## 5. The five most transferable things observed

1. **Trainline** — *"Get notified when you qualify for delay compensation."* Needs only the
   itinerary and the rules. No inventory, no balance sheet, no insurance licence.
2. **Kayak** — the sort control shows what each choice costs: `35 € / 7h 14m` against
   `47 € / 1h 25m`. The trade-off is visible before you choose.
3. **Airbnb** — total price only, never nightly, at comparison time. Deletes the arithmetic a
   first-timer cannot yet do.
4. **Google** — *"Prices are currently typical."* Tells you what normal looks like, before you search.
5. **Airbnb AirCover** — states what it does **not** cover, with examples, in the same document that
   promises the protection.

And the anti-pattern, because it is a choice: **Expedia** phrases declining insurance as
*"I'm willing to risk my $358.59 stay in Lisbon."* **Airbnb**, at the identical moment for
comparable money, asks a neutral priced question. One manufactures guilt; one asks.

---

## 6. Method rules this round paid for

1. **An empty result is a prompt to look, never a finding.** Eight instances of a result that looked
   like data and was not — five empty selector returns, two 404s that rendered with titles and
   headings, and one sweep run in the wrong language against a Spanish page.
2. **Two browsers, and they disagree by construction.** The authenticated browser carries extensions
   that inject page UI a selector cannot see. Screenshot-derived claims come from the clean
   inspector instance; session-gated surfaces from the authenticated one. Run as a matched pair and
   personalisation becomes measured rather than asserted.
3. **Sweep in the locale actually served**, not the one requested.
4. **Never transcribe a competitor review.** The evidence ledger holds zero records; a review in a
   capture file is an unresolvable user quote. Describe the mechanism, never the words.
5. **Marketing copy is `Likely`, never `Verified`.**

Six findings corrected their own earlier versions this round — every one by capturing more, not by
reasoning harder.

---

## 7. What this corpus cannot answer

Stages 4–8 · every error, no-results and offline state · post-purchase and trip management on all 17
· whether any transport competitor actually fulfils a ticket · lounge and Fast Track pricing for an
economy traveller · Omio and Tripadvisor results surfaces, both blocked at consent with no reject
affordance.

If a question falls in that list, the honest answer from this corpus is **"not captured"** — not an
inference.
