# Phase 3 — Feature Inventory (four threads)

**Method:** luma-competitor-analysis-pro, Phase 3, restricted to Threads A–D per the task brief. Phases 1–2
(desk research, capture planning) already complete and not re-run. No web browsing performed. Every fact in
`phase3-feature-inventory.json` was re-read from its underlying capture file under
`artifacts/luma-hands-on/2026-09-04__competitive-benchmark__hands-on-capture-round-1__v1/captures/` — not taken
on trust from `CAPTURE-INDEX.json`'s one-line claim text. `WORLD.json` was not used, per the brief (it is short
by 4 rows, correction C-043). 35 capture files were read in full; 31 distinct capture-file paths are cited as
evidence in the dataset, and all 31 resolve to real files on disk (verified programmatically).

## What this is NOT

No comparison, ranking, or recommendation is made anywhere in the dataset. Where a chart could not be honestly
supported by what the captures contain, that is stated in `gaps` rather than smoothed over.

## Thread A — Ranking axes & effort

10 product/vertical rows built (7 accommodation+activities+2 flights rows, plus rail as a qualitative-only
row), 7 ranking-basis disclosure statements, 8 anchor checks.

**All eight anchors given in the task brief were checked against the capture files and CONFIRMED, exact match,
no discrepancies:** Booking.com 11 signed-in / 10 signed-out; Expedia 6; Google hotels 3; Airbnb 0; Tripadvisor
activities 0; Google Flights 6 of which 4 effort/convenience; Kayak flights 3 of which 2 concern duration;
Trainline states its basis (confirmed as a qualitative fact — no enumerable axis list exists for Trainline, so
no number can be checked against it).

Two axis-breakdown cells required a judgment call beyond pure transcription, both flagged explicitly in the
JSON's `normalisations` and inline `axis_breakdown_source_note` fields:
- Booking.com's **signed-out** breakdown (price:3/quality:4/distance:1/property_type:1/opaque:1) is *derived*
  by subtracting the one axis (a price axis, per the source's own F-11) that differs from the signed-in
  11-axis breakdown — not independently re-enumerated. Marked Inferred, not Verified, for that split.
- Google Flights' "Emissions" axis is filed under effort-convenience because the correction capture's own
  `effort_or_convenience_axes` count includes it — but an earlier finding in the same round (F-34) describes
  emissions as "neither price, quality proxy, nor distance" without independently asserting it measures
  effort. Both readings are recorded; the file follows the source's own later, more considered classification.

Trainline has **no enumerable sort-axis count at all** — its results surface has no sort control (only a
"Direct only" filter), only a stated three-part ranking policy (fastest → fewest changes → cheapest). Reporting
a number for Trainline alongside Booking.com's 11 or Google Flights' 6 would misrepresent a policy statement as
a set of selectable options. This is called out as a gap, not resolved by inventing a number.

Ranking-basis character counts: computed directly from verbatim strings already in the capture files (not
estimated) for Booking.com (159 chars), Google Flights (38 chars, core sentence only), Airbnb (424-char
headline / 10,860-char full document), Trainline (166 chars, complete sentence). Kayak's (18,759-char document)
and Tripadvisor's sample sentences are both quoted **truncated mid-word** in their own capture files — their
true sentence-level length is NOT VERIFIED and is reported as such rather than estimated from the surrounding
document's total length.

## Thread B — Loyalty & the first-time traveller

5 programmes: Booking.com Genius, Expedia One Key, Iberia Club, Qatar Airways Privilege Club, American
Airlines AAdvantage (included as a heavily NOT-VERIFIED entry, not omitted, per the counter-case instruction).

All four numeric anchors given in the brief were confirmed exact: One Key Blue 0–4 / Silver 5–14 / Gold 15–29 /
Platinum 30+; Genius L1 grants 10% immediately (non-empty entry tier); Genius priority support requires 15
completed bookings in 2 years.

**Iberia Club has no numeric tier ladder on disk at all** — the page that would carry tier names and
thresholds was never opened in the round. Recorded as NOT VERIFIED per the brief's explicit instruction
("an unstated threshold is absent, not zero"), not interpolated from the other three ladders. Only the
currency mechanics (Avios spendable/earnable off-platform; Puntos Elite status/flight-gated) are Verified.

**American Airlines AAdvantage** has almost no data — one reward-unlock figure (15,000 Loyalty Points, from
the Spanish-locale site) and no tier names/thresholds (two 404s on URL guesses). It is not charted as a fourth
or fifth tier ladder.

First-time-traveller text search: zero matches on **four** programmes that were actually swept (Genius, One
Key, Iberia Club, Privilege Club) — different term lists, different locales, same null. AAdvantage was **never
swept** for this term set; the file is explicit that this is an untested cell, not a fifth confirmed null, so a
"5 of 5" claim would overstate the tested sample.

Qatar's Silver tier is the only tier across all programmes with a purchasable status currency (Qpoints, USD
25/point) — but purchase caps and minimum-earned-balance thresholds are unextracted (source page returned only
1,069 characters; constraint tables did not render). Per the source's own explicit warning, no "price of
Silver" figure is computed or reported here, since the cap means the naive $3,750 arithmetic is not a real
purchasable price.

## Thread C — The disruption gap

7 company-level entries (Booking.com; Iberia; American Airlines on two different locale-served sites, kept
as two separate rows because they returned two different results; Qatar Airways; Hopper; Trainline).

Findings, not verdicts: Iberia — zero matches across a three-surface, eleven-term, es-locale sweep (237 + 130
homepage/FAQ link labels plus the changes-and-refunds page), other than one sentence that names a different
regime and does not link to it. Qatar — zero matches across a 289-link, seven-term, en-gb homepage sweep.
American Airlines (US, en) — a four-section Customer Service Plan exists but was reached by URL guess after a
404, not navigation; its findability is untested. American Airlines (Spanish-locale site) — after a first,
wrong-language sweep produced a false null (English terms against a Spanish-served page), a corrected sweep
found "Actualizaciones de viaje" as a homepage **heading**, but on a materially thinner, different site (43
links) whose relationship to the US Customer Service Plan is unknown. Booking.com — no formal search-term
sweep exists in these captures at all, only a site-tree category read with no disruption-labelled destination
among ~26 named items; contractually, it disclaims flight liability outright and signposts EU 261 only inside
its Terms.

Two counter-cases, included per the brief: **Hopper** sells "Premium Disruption Assistance" — rebooking on
any airline or a full refund — as a named, paid, app-only product (price not captured). **Trainline** does
something different again: it proactively notifies travellers when they qualify for delay compensation,
rather than requiring them to find a rights page at all.

**Method-asymmetry flag:** the five "does a route exist" results were produced by five different methods (a
category read, two sweeps of different scope, a URL-guess-then-read, and a direct navigation to a named
product). They are not safely plotted on one uniform axis; the JSON records this explicitly rather than letting
a chart imply comparability the underlying tests don't have.

## Thread D — Business goal 2 (the trip as a single object)

Known instance confirmed as stated: Airbnb drops trip dates crossing from Stays to Experiences within one
account. Searching the rest of the capture set for another instance of the same pattern (trip state crossing a
product boundary and arriving dropped or wrong) found **exactly one other instance**: Trainline's pre-checked
Booking.com cross-sell fires a same-tab popunder carrying **today/tomorrow's dates, not the travel dates
searched** — a cross-company boundary this time, and the state isn't merely absent, it's wrong.

Two adjacent-but-distinct observations were found and kept separate rather than folded in as more instances,
because the underlying trip data actually survives intact in both: the Kayak→Iberia handoff carries the full
itinerary correctly (only branding/consent context is dropped), and Iberia's fare-selection page attributes a
Kayak-selected Basic Economy fare to the traveller as "your choice" (the fare code is carried correctly; the
decision-agency framing is what's misrepresented). Neither is counted toward the instance total.

One counter-case: TripIt models the trip as one object by refusing to sell anything — it ingests forwarded
confirmation emails from any source and never initiates a cross-sell or vertical switch that could drop state.

This was not a systematic sweep of all 17 competitors with one fixed method — no such sweep exists on disk.
It is a review of every capture that explicitly tests a handoff or discusses itinerary state surviving (or not)
a boundary. The gaps section states this limitation directly rather than implying a denominator of 17.

## Gaps (11 recorded)

Chart-relevant gaps recorded in the JSON's `gaps` array include: accommodation axis counts exist for only 4 of
9+ accommodation-capable competitors; flights axis counts exist for only 2 competitors (Google, Kayak); rail
has no enumerable axis count to chart at all; two ranking-statement lengths are unrecoverable (truncated
quotes); Iberia Club and AAdvantage cannot support a numeric tier-ladder chart; the first-time-traveller null
is a 4-programme finding, not 5; Qatar's Qpoint purchase caps are unextracted; Thread C's five "route exists"
results are not method-matched and should not be charted on one uniform axis without flagging that; and Thread
D's "2 instances found" should not be read as "2 of 17 competitors," since only a handful of boundary crossings
were ever actually walked.

## Files

- Dataset: `artifacts/luma-hands-on/2026-09-07__dashboard__hands-on-findings-and-recommendations__v2/phase3-feature-inventory.json`
- This summary: `artifacts/luma-hands-on/2026-09-07__dashboard__hands-on-findings-and-recommendations__v2/phase3-feature-inventory.md`
