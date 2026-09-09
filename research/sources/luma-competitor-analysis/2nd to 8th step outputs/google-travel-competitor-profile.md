# Verified Competitor Profile · Google Travel

**Phase:** 2 of 9, competitor 5 of 14
**Date researched:** 21 July 2026
**Researcher session conditions:** google.com/travel, desktop web, browser located in Spain, English interface requested, EUR.
**Platform covered:** desktop web only.
**Evidence supplied by the user:** none. Public sources only.

## Two conditions that change how this profile should be read

**The browser was signed in to a Google account.** Every previous profile in this run was walked signed out. This one was not, and a signed-in account may affect ranking, saved state and personalisation. This is a material difference and it is not comparable like for like with the other four. Nothing below is claimed to be the signed-out experience.

**Scope was fixed in advance by the benchmark plan.** Google Travel was scoped to Google Flights, Google Hotels and Things To Do, with anything outside that treated as out of scope. In this session the product surface exposed four tabs: Explore, Flights, Hotels and Vacation rentals. **No Things To Do tab was present, and /travel/things-to-do redirected to Flights.** Things To Do is therefore recorded as not reachable at that path in this session rather than as absent. Explore and Vacation rentals were not walked, being outside the agreed scope.

No comparison to any other product appears in this document. That is Phase 3's job.

---

## 1. Snapshot

Google Travel is a non-transactional aggregator. It searches, ranks and explains travel options, then hands the traveller to a third party to buy (High, live product). The flight flow ends on a "Booking options" page listing named sellers at different prices, with airline-operated options labelled "Airline" and online travel agencies unlabelled (High). The hotel flow ends on per-property "View prices" controls (High). Its own revenue surface is visible as clearly labelled Sponsored placements at the top of hotel results (High). Verticals present in this session were Explore, Flights, Hotels and Vacation rentals (High). Markets, currency handling and language coverage were partially observed: an English interface was requested and served, and a later navigation dropped the language parameter and returned Portuguese (High for the observation, Unknown for the rule).

---

## 2. Feature list by journey stage

Journey stages follow the benchmark plan.

### Stage 1 · Dream and discover

| Feature | What it does | Confidence | Source |
|---|---|---|---|
| Explore | A top-level tab alongside the booking verticals | High for presence, `Unknown` for contents. Out of agreed scope | Live product, header |
| Where to visit guidance | Hotel results carry a "When to visit" entry point beside the filters | High for the entry point, `Unknown` for contents | Live product, hotel results |
| Date flexibility shortcuts | Hotel results offer "This weekend", "Next weekend" and "Next work week" as one-click date changes | High | Live product, hotel results |

### Stage 2 · Plan and compare

**Flights**

| Feature | What it does | Confidence | Source |
|---|---|---|---|
| Result tabs | Two tabs above results, "Best" (default) and "Cheapest", with the cheapest price shown on the tab itself | High | Live product |
| Two ranked groups | Results split into "Top departing flights" and "Other departing flights", labelled as separate sections rather than one continuous list | High | Live product |
| Inline ranking explanation | Beneath the results heading: "Ranked based on price and convenience", with an info control | High | Live product |
| Ranking explanation, full text | The info control opens: "'Top flights' are ranked based on the best trade-off between price and convenience factors such as duration, number of stops, and airport changes during layovers. All other flights are ranked by price", with a Learn more link | High | Live product, verbatim |
| Sort control, 6 options | Top flights (default), Price, Departure time, Arrival time, Duration, Emissions | High | Live product |
| Filter chips | All filters, Stops, Airlines, Bags, Price, Times, Emissions, and at least one further chip cut off at the viewport edge | High for those listed, `Unknown` for the remainder | Live product |
| Emissions per result | Every result displays an absolute figure in kg CO2e plus a relative label against the route average, for example "Avg emissions", "-14% emissions", "+15% emissions", each with an info control | High | Live product |
| Price insights on results | A panel stating "Prices are currently typical", with View price history, Date grid and Price graph controls | High | Live product |
| Track prices, two scopes | Track prices for the specific dates, or "Any dates" for the route | High | Live product |
| Fee disclosure at results level | "Prices include required taxes + fees for 1 adult. Optional charges and bag fees may apply", with a bag fees link and a Passenger assistance link | High | Live product |

**Hotels**

| Feature | What it does | Confidence | Source |
|---|---|---|---|
| Filter chips | All filters, 4+ rating, Under a price threshold, Pool, 4- or 5-star, Spa, Price, Property type | High | Live product |
| Three guidance entry points | "Where to stay", "When to visit" and "What you'll pay" sit as a distinct row beside the filters | High for the entry points, `Unknown` for their contents | Live product, hotel results |
| Track prices | A toggle with an info control at the top of results | High | Live product |
| Result count and disclosure | "Lisbon · 15,000 results" with an "About these results" link | High | Live product |
| Sponsored carousel | A labelled "Sponsored · Lisbon hotels" carousel above organic results, with an options control. Some entries carry a seller attribution such as Booking.com | High | Live product |
| Qualitative badges on cards | Organic cards carry badges including "Excellent location", "Eco-certified" and "Popular with guests from Spain" | High | Live product |
| Rating and review count | Ratings out of 5 with review counts, alongside star class | High | Live product |
| Amenity tokens | Per-card amenity lists including "Accessible", "Wheelchair accessible", "Kid-friendly", "Airport shuttle", "Free breakfast", and paid variants marked with a currency symbol such as "Parking ($)" | High | Live product |
| Mixed inventory types | Hotels and vacation rentals appear in the same result list, distinguished by a "VACATION RENTAL" label and by different calls to action, "View prices" against "View details" | High | Live product |
| Date state disclosure | "Set your dates to update prices. Prices shown for [date range]", with a Change dates control | High | Live product |

**Things to do**

`Unknown - not reachable.` No Things To Do tab was present in the product header in this session, and /travel/things-to-do redirected to the Flights home page. Nothing is claimed about whether the surface exists elsewhere.

### Stage 3 · Book

| Feature | What it does | Confidence | Source |
|---|---|---|---|
| Two-step itinerary selection | Selecting an outbound advances to a "Choose return" screen with its own ranked groups, then to a booking page | High | Live product |
| Booking options list | A list of named sellers, each with a price, a Continue control and a "View options" control. Five were shown with "13 more booking options" beneath, so 18 in total for this itinerary | High | Live product |
| Seller type labelling | Options operated by the carrier are labelled "Airline". Others carry no such label | High | Live product |
| Price dispersion is visible | For one itinerary the same flights were offered at €99, €106, €107, €206 and €237 by different sellers | High | Live product |
| Ranking disclosure for sellers | The booking options block carries a "How options are ranked" link and a "Learn more about booking options" link | High for the presence of both links, `Unknown` for their contents |
| Lowest total price label | The headline price on the booking page is labelled "Lowest total price" | High | Live product |
| Baggage summary | "1 free carry-on" and "1st checked bag available for a fee", with links to each operating carrier's bag policy and the note that baggage conditions apply to the entire trip and fees may be higher at the airport | High | Live product |
| Explicit information-gap disclosure | A warning states that bag fee information is not available when booking with a named list of sellers, naming fifteen of them including the operating carrier itself | High | Live product, verbatim list captured |
| Price insights on the booking page | "€99 is low for Economy, €76 cheaper than usual", followed by "The least expensive flights for similar trips to London usually cost between €130 to €250", rendered with a visual range scale | High | Live product |
| Payment and checkout | `Unknown - by design.` Google hands off to a third party. No checkout exists inside the product to walk | Unknown | Product model plus walkthrough limit |

### Stage 4 · Prepare

| Feature | What it does | Confidence | Source |
|---|---|---|---|
| Track prices on the booking page | A toggle with an info control appears beside the selected flights | High | Live product |
| Share | A Share control on the booking page | High for the control, `Unknown` for behaviour | Live product |
| Saved items | A bookmark-style control appears at the top right of hotel results | High for the control, `Unknown` for behaviour | Live product |

### Stages 5 to 8 · Travel day, in destination, return, after the trip

`Unknown - not evidenced.` No day-of-travel, in-destination, return or post-trip surface was found within the agreed scope. Google operates other products that may serve these stages, and those are out of scope by the benchmark plan rather than absent.

---

## 3. UX patterns

**Navigation model.** A persistent header carries the product tabs, a theme control, an apps grid and the account avatar. Search state is encoded in long opaque URL parameters rather than readable query strings, so a search cannot be reconstructed or shared by editing the URL by hand. Flights supports a natural-language deep link of the form "Flights to LHR from BCN on [date] through [date]", which resolved correctly. (High.)

**Ranking is explained at the point of ranking.** The flight results page states the ranking basis in a line directly beneath the heading, and an adjacent info control opens the full rule in two sentences, including what happens to everything outside the top group. The booking options block carries its own separate ranking explanation link. Explanation is placed inline rather than in a footer policy page. (High.)

**Two ranked groups rather than one list.** Flights are split into "Top departing flights" and "Other departing flights". The first is ranked on a stated trade-off, the second on price alone. The split is visible, labelled, and explained. (High.)

**A non-price, non-time axis is a first-class control.** Emissions appear three times over: as a per-result figure, as a relative comparison against the route average, and as both a filter chip and a sort option. A traveller can order the entire result set by it. (High.)

**Price claims arrive with the comparison that produced them.** The results page says prices are "currently typical". The booking page says a price is low, states by how much, and then gives the reference range that makes it low. The judgement and its basis are shown together. (High.)

**The product discloses its own information gaps.** The booking page names fifteen sellers for which bag fee information is not available, including the operating carrier. Hotel results carry an "About these results" link and a visible statement of which dates the displayed prices apply to. (High.)

**Price dispersion between sellers is not hidden.** The booking options list shows the same itinerary at materially different prices across eighteen sellers, and labels which of them are the operating airline. (High.)

**Advertising is separated and labelled.** Hotel results place Sponsored inventory in a distinct carousel above the organic list, labelled "Sponsored" with its own options control, rather than interleaved into the result list. (High.)

**Hotel guidance is offered as three named questions.** "Where to stay", "When to visit" and "What you'll pay" sit together as a row of entry points, framing neighbourhood, timing and budget as three separate things a traveller might not know. (High for the framing, `Unknown` for what each opens.)

**Qualitative badges carry the recommendation.** Hotel cards carry short evaluative labels such as "Excellent location" and "Eco-certified" alongside the numeric rating, and one card carried an origin-specific label, "Popular with guests from Spain". (High.)

**Alerting is offered at three points in one flow.** Track prices appears on the results page with two scopes, on the booking page, and as a toggle on hotel results. (High.)

**Errors and empty states.** No zero-results state was reached. One redirect behaviour was observed: an unrecognised path under /travel resolved to the Flights home page rather than an error page, and the language parameter was not preserved through that redirect, producing a Portuguese interface after an English one. (High.)

**Accessibility.** Accessibility appears in hotel data as amenity tokens, "Accessible" and "Wheelchair accessible", and a "Passenger assistance" link sits in the flight results fee disclosure. No accessibility statement was sought or found within the agreed scope. `Unknown`. (High for the tokens and the link, Unknown for the statement.)

---

## 4. Notable design decisions

These look deliberate and are stated without evaluation.

1. **The ranking rule is written in the interface, not linked from a footer.** Two sentences, naming the trade-off and the factors, one click from the results.
2. **The rule states what happens to the flights that did not make the top group.** They are ranked by price, and this is said explicitly rather than left to inference.
3. **Results are split into two labelled groups with different ranking logic**, rather than presented as a single ordered list.
4. **Emissions is a sort option, not only a filter or a label.** The whole result set can be reordered by it.
5. **Emissions are shown as both an absolute and a relative figure.** A kg CO2e number and a percentage against the route average, on every row.
6. **Price judgements are always paired with their reference range.** "Low" is followed by the band that defines low for that route and cabin.
7. **Price tracking is offered date-agnostically as well as for the chosen dates.** "Any dates" tracks the route rather than the itinerary.
8. **The seller list names who is an airline and who is not.**
9. **Wide price dispersion between sellers is displayed rather than resolved.** Eighteen options at prices differing by more than a factor of two, presented as a list.
10. **The product publishes where its own data stops.** A named list of sellers for which bag fee information is unavailable, printed next to the baggage summary.
11. **Sponsored inventory is segregated into its own labelled carousel** rather than mixed into organic hotel results.
12. **Hotel guidance is framed as three questions a traveller may not know to ask**, rather than as filters.
13. **The current date assumption is stated on screen** when the user has not set dates, together with one-click alternatives.
14. **Hotels and vacation rentals share one result list** but are labelled and given different calls to action.

---

## 5. Evidence log

All URLs accessed 21 July 2026, signed in to a Google account, from Spain, English requested, EUR.

| # | Claim | Source | Tier | Confidence |
|---|---|---|---|---|
| 1 | Four product tabs: Explore, Flights, Hotels, Vacation rentals | google.com/travel/flights | 1, walkthrough | High |
| 2 | No Things To Do tab present; /travel/things-to-do redirects to Flights and does not preserve the language parameter | google.com/travel/things-to-do | 1, walkthrough | High |
| 3 | Best and Cheapest result tabs, with the cheapest price on the tab | Flights, BCN to LHR, 13 to 21 Aug 2026 | 1, walkthrough | High |
| 4 | Top departing flights and Other departing flights as two labelled groups | same | 1, walkthrough | High |
| 5 | "Ranked based on price and convenience" stated beneath the heading | same | 1, walkthrough | High |
| 6 | Full ranking explanation captured verbatim from the info control | same | 1, walkthrough | High |
| 7 | Six sort options including Emissions | same | 1, walkthrough | High |
| 8 | Filter chips including Bags and Emissions | same | 1, walkthrough | High |
| 9 | Per-result emissions in kg CO2e with relative comparison labels | same | 1, walkthrough | High |
| 10 | Price insights stating prices are currently typical, with price history, date grid and price graph | same | 1, walkthrough | High |
| 11 | Track prices offered for the chosen dates and for any dates | same | 1, walkthrough | High |
| 12 | Fee disclosure with bag fees and passenger assistance links | same | 1, walkthrough | High |
| 13 | Two-step outbound then return selection | same | 1, walkthrough | High |
| 14 | Booking options list, five shown plus thirteen more, with Continue and View options per seller | Flights booking page | 1, walkthrough | High |
| 15 | Airline label distinguishing carrier-operated options | same | 1, walkthrough | High |
| 16 | Price dispersion across sellers for one itinerary | same | 1, walkthrough | High |
| 17 | "How options are ranked" and "Learn more about booking options" links present | same | 1, walkthrough | High for presence only |
| 18 | Lowest total price label on the headline price | same | 1, walkthrough | High |
| 19 | Baggage summary plus per-carrier bag policy links | same | 1, walkthrough | High |
| 20 | Bag fee information gap disclosed, naming fifteen sellers | same | 1, walkthrough | High, verbatim captured |
| 21 | Booking-page price insight with the reference range | same | 1, walkthrough | High |
| 22 | Track prices and Share controls on the booking page | same | 1, walkthrough | High |
| 23 | Hotel filter chips | Hotels, Lisbon | 1, walkthrough | High |
| 24 | Where to stay, When to visit, What you'll pay entry points | same | 1, walkthrough | High |
| 25 | Track prices toggle on hotel results | same | 1, walkthrough | High |
| 26 | Result count with About these results link | same | 1, walkthrough | High |
| 27 | Labelled Sponsored carousel above organic results, with seller attribution on some entries | same | 1, walkthrough | High |
| 28 | Qualitative badges: Excellent location, Eco-certified, Popular with guests from Spain | same | 1, walkthrough | High |
| 29 | Amenity tokens including Accessible and Wheelchair accessible, and paid amenities marked | same | 1, walkthrough | High |
| 30 | Hotels and vacation rentals in one list with different labels and calls to action | same | 1, walkthrough | High |
| 31 | Date state disclosure and one-click date shortcuts | same | 1, walkthrough | High |
| 32 | Natural-language flight deep link resolves correctly | google.com/travel/flights?q=... | 1, walkthrough | High |

No Tier 2 documentation was consulted for this profile. The two ranking explanation links on the booking page and the "About these results" link on hotel results were observed but not opened, because model-backed browser tooling became unavailable partway through the session.

---

## Gaps

What could not be verified, and why.

| Gap | Why |
|---|---|
| Signed-out behaviour | The session ran signed in. Ranking, saved state and any personalisation may differ signed out. This profile is not comparable like for like with the four before it |
| Things To Do | No tab in the product header, and the expected path redirected to Flights. Not reachable in this session |
| Explore and Vacation rentals | Out of the scope agreed in the benchmark plan. Not walked |
| Contents of "How options are ranked" and "Learn more about booking options" | Links observed, not opened. Tooling for locating elements became unavailable |
| Contents of "About these results" on hotel results | Same reason |
| Contents of Where to stay, When to visit and What you'll pay | Entry points observed, not opened |
| The full flight filter set | At least one chip was cut off at the viewport edge, and the All filters panel was not successfully opened |
| Hotel sort options | No sort control was located on hotel results in this session. This does not establish that none exists |
| Flight detail expansion: aircraft, legroom, on-time performance, layover detail | Rows have expand controls that were not opened |
| First-party documentation on ranking, emissions methodology and price insights | Not swept. Every claim in this profile is Tier 1 observation, which is a strength for accuracy and a gap for stated methodology |
| Zero-results and error states | Not reached |
| Markets, currency and language rules | English was served on request and Portuguese after a redirect that dropped the parameter. The rule behind this was not established |
| Accessibility statement | Not sought within the agreed scope |
| What happens after Continue | The handoff destination was not followed, since it leads to a third-party booking flow |

---

## Confidence summary

Counts are of distinct claims recorded in this profile.

| Rating | Count | What they are |
|---|---|---|
| High | 32 | Observed directly in the live product, signed in, under the stated conditions. Two are captured verbatim |
| Medium | 0 | No first-party documentation was consulted this run |
| Low | 0 | No marketing or third-party source was relied on |
| Unknown | 14 | Listed in Gaps above |

**Total claims: 46.**

**Two notes for Phase 3.** First, this is the only profile in the run so far with no Medium and no Low claims, because everything recorded was seen rather than read. That is a strength, but it means nothing here is corroborated by stated methodology, and several explanation links were left unopened. Second, the signed-in condition must travel with these cells into the matrix. Do not present them as equivalent in kind to the signed-out observations from the other competitors.
