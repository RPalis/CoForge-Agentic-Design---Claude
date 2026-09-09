# Luma Competitor Benchmark · Phase 3: Feature Inventory

**Status:** Data structuring only. Profiles merged, not interpreted. No ranking, no scoring, no recommendations.
**Date:** 21 July 2026
**Phase:** 3 of 9
**Competitors merged:** 6 of 14 researched so far. Expedia, Booking.com, TripIt, Hopper, Google Travel, Tripadvisor. The remaining eight (Kayak, Skyscanner, Airbnb, Rentalcars.com, Trainline, Omio, Citymapper, Rome2Rio) are not yet profiled and appear nowhere below.
**Companion file:** `luma-feature-inventory.xlsx` holds the same three artefacts as colour-coded grids, plus a source register. The spreadsheet is the primary format for the matrix.

**Luma column, everywhere:** `Not built (ideation), decision required.` No current Luma behaviour is asserted.

**Cell values:** exactly one of `Yes` / `No` / `Partial` / `Unknown`. `No` means absence was verified. Where absence was not verified, the cell is `Unknown`. Every `Yes` and `Partial` carries a confidence tag: High (H, live product), Medium (M, docs or help centre), Low (L, marketing or inference). `Partial` names any paid tier.

---

## 1. Feature matrix

Read left to right per row. Confidence in brackets. Notes in parentheses.

### Cluster 1 · Vertical coverage

| Feature | Expedia | Booking.com | TripIt | Hopper | Google Travel | Tripadvisor |
|---|---|---|---|---|---|---|
| Flight search and compare | Yes (H) | Yes (H) | No (M) ingests only | Partial (H) results not reached | Yes (H) | Unknown |
| Accommodation search | Yes (H) | Yes (H) | No (M) | Partial (H) not walked | Yes (H) | Partial (H) not walked |
| Car rental | Yes (H) | Yes (H) | No (M) | Yes (H) | Unknown (no Cars tab in scope) | Unknown |
| Activities and experiences | Yes (H) | Yes (H) | No (M) | Unknown | Unknown (not reachable) | Yes (H) via Viator |
| Public transport tickets | Unknown | Unknown | No (M) ingests, sells nothing | Unknown | Unknown | Unknown |
| Shows multiple sellers per item | No (M) OTA | No (M) agency | No (M) | No (M) | Yes (H) 18 sellers | Partial (H) |
| Completes booking in-product | Yes (H) | Yes (H) | No (H) | Yes (M) | No (H) hands off | Partial (H) Viator |

Note on the public-transport-tickets row: every cell is `Unknown` or a documented `No`. The question the benchmark plan flagged as load-bearing stays open across the six profiled competitors and will only be resolved when Trainline, Omio, Citymapper and Rome2Rio are run.

### Cluster 2 · Decision support

| Feature | Expedia | Booking.com | TripIt | Hopper | Google Travel | Tripadvisor |
|---|---|---|---|---|---|---|
| Sort controls offered | Yes (H) 9 flight, 6 hotel | Yes (H) 11 hotel | No (M) | Unknown | Yes (H) 6 | Partial (M) |
| Filter set | Yes (H) | Yes (H) ~22 groups | No (M) | Unknown | Yes (H) | Yes (H) |
| Priced filters | Yes (H) | Unknown | No (M) | Unknown | Unknown | Unknown |
| Natural-language search input | Unknown | Yes (H) to chips | No (M) | Unknown | Partial (H) deep link | Unknown |
| Emissions shown per result | Unknown | Unknown | No (M) | Unknown | Yes (H) | No (M) |
| **Sortable non-price/non-time/non-rating axis** | **No (H)** | **No (M)** | Unknown | Unknown | **Yes (H)** emissions | Unknown |
| Ranking transparency disclosure | Yes (H) | Yes (H) | No (M) | Unknown | Yes (H) | Yes (H) |
| Price prediction (book now or wait) | Unknown | No (M) | No (M) | Partial (M) app-only | Unknown | No (M) |
| Price history / price insights | Yes (H) | Unknown | No (M) | Partial (M) in-app | Yes (H) | No (M) |
| Fare/seat/price-drop trackers | Yes (H) | Partial (M) Genius L1 | Partial (M) Pro | Partial (M) app | Yes (H) | No (M) |

The bold row is the one the benchmark plan singled out. Only Google Travel offers a sort on an axis that is neither price, time, nor rating (emissions). Expedia and Booking.com were verified not to, within the sorts observed. The other three are Unknown.

### Cluster 3 · Reassurance and trust

| Feature | Expedia | Booking.com | TripIt | Hopper | Google Travel | Tripadvisor |
|---|---|---|---|---|---|---|
| User reviews with counts | Yes (H) | Yes (H) | No (M) | Unknown | Yes (H) | Yes (H) core |
| Category sub-scores | Yes (H) | Yes (H) 7 | No (M) | Unknown | Unknown | Unknown |
| Sample size shown with score | Yes (H) | Yes (H) | No (M) | Unknown | Yes (H) | Yes (H) |
| Segment-specific review evidence | Yes (H) solo | Yes (H) solo | No (M) | Unknown | Unknown | Yes (H) party tags |
| Named human expert curation | Unknown | Unknown | No (M) | Unknown | Unknown | Yes (H) |
| Named protection/guarantee product | Partial (H) add-on | No (M) | No (M) | Partial (M) paid | No (M) | No (M) |
| All-in pricing | Yes (H) | Yes (H) | No (M) | Unknown | Yes (H) | Unknown |
| Cancellation terms before selection | Yes (H) | Yes (H) | No (M) | Partial (M) add-on | Unknown | Unknown |

### Cluster 4 · Loyalty

| Feature | Expedia | Booking.com | TripIt | Hopper | Google Travel | Tripadvisor |
|---|---|---|---|---|---|---|
| Loyalty programme | Yes (H) One Key | Yes (H) Genius | No (M) | Partial (M) Savings Club | No (H) | Yes (H) Rewards |
| Gated by tenure / accumulated bookings | Yes (M) tier | Yes (H) 5 and 15 bookings | No (M) | Unknown | No (M) | Unknown |

### Cluster 5 · Prepare and itinerary

| Feature | Expedia | Booking.com | TripIt | Hopper | Google Travel | Tripadvisor |
|---|---|---|---|---|---|---|
| Auto itinerary capture from email/inbox | No (M) | No (M) | Yes (M) | No (M) | No (M) | No (M) |
| Trips / saved surface | Yes (H) walled | Yes (H) walled | Yes (M) | Yes (H) | Partial (H) | Partial (H) |
| Calendar sync | Unknown | Unknown | Yes (M) | Unknown | Unknown | Unknown |
| Sharing / group coordination | Unknown | Unknown | Yes (M) | Unknown | Yes (H) | Yes (H) |
| Document storage | Unknown | Unknown | Partial (M) 3 free / 25 Pro | Unknown | Unknown | Unknown |
| Entry requirements / visa guidance | Unknown | Unknown | Partial (M) Pro | Unknown | Unknown | Unknown |
| Passport renewal reminder | Unknown | Unknown | Yes (M) Pro | Unknown | Unknown | Unknown |

### Cluster 6 · Travel day

| Feature | Expedia | Booking.com | TripIt | Hopper | Google Travel | Tripadvisor |
|---|---|---|---|---|---|---|
| Live flight status / alerts | Unknown | Unknown | Yes (M) Pro | Partial (M) | No (M) | No (M) |
| Departure timing (go now) | Unknown | Unknown | Yes (M) Pro | Unknown | Unknown | Unknown |
| **Interactive airport indoor maps / wayfinding** | Unknown | Unknown | **Yes (M)** ~110 airports, Pro | Unknown | Unknown | Unknown |
| Disruption risk alerts | Unknown | Partial (M) overbooking | Yes (M) Pro | Partial (M) paid | No (M) | Unknown |
| Terminal/gate, connection, baggage reminders | Unknown | Unknown | Yes (M) Pro | Unknown | Unknown | Unknown |

The airport-wayfinding row is the one that falsified a prior-run claim. TripIt ships it (documented, Pro, app). The others are `Unknown` because their travel-day surfaces were not reached, not verified absent.

### Cluster 7 · In destination

| Feature | Expedia | Booking.com | TripIt | Hopper | Google Travel | Tripadvisor |
|---|---|---|---|---|---|---|
| Things to do / activities discovery | Partial (H) | Yes (H) | No (M) | No (M) | Unknown | Yes (H) |
| Public transit info (stops / distances) | Yes (H) | Yes (H) | Partial (M) | Unknown | Unknown | Partial (H) |
| Street-level navigation / wayfinding | Unknown | Unknown | Yes (M) app | Unknown | Unknown | Partial (H) AI plan (caveat) |
| Neighbourhood safety scores | Unknown | Unknown | Yes (M) GeoSure | Unknown | Unknown | Unknown |
| Declared-tolerance personalisation | Unknown | Unknown | Yes (M) Risk Level | Unknown | Unknown | Unknown |

### Cluster 8 · After the trip

| Feature | Expedia | Booking.com | TripIt | Hopper | Google Travel | Tripadvisor |
|---|---|---|---|---|---|---|
| Review writing | Yes (H) | Yes (H) | Partial (M) ratings | Unknown | Unknown | Yes (H) |
| Flight-delay compensation eligibility | Unknown | Unknown | Yes (M) AirHelp | Unknown | Unknown | Unknown |
| Personal carbon tracking / offset | Unknown | Unknown | Yes (M) | Unknown | Unknown (per-result only) | Unknown |

### Cluster 9 · Conversational and AI

| Feature | Expedia | Booking.com | TripIt | Hopper | Google Travel | Tripadvisor |
|---|---|---|---|---|---|---|
| Conversational AI trip planner | Partial (L) vendor claim, alpha | Unknown | Unknown | No (M) | No (M) not in scope | Yes (H) observed, caveat |
| AI review/property Q&A | Yes (H) | Partial (H) form only | No (M) | Unknown | Unknown | Unknown |
| AI disclosure / labelling present | Yes (H) | Partial (H) | Unknown | Unknown | Unknown | Yes (H) |

### Cluster 10 · Personalisation and accessibility

| Feature | Expedia | Booking.com | TripIt | Hopper | Google Travel | Tripadvisor |
|---|---|---|---|---|---|---|
| Behavioural personalisation | Yes (M) | Yes (M) | No (M) | Unknown | Partial (M) signed-in | Unknown |
| Declared/profile personalisation | Unknown | Partial (H) occupancy | Yes (M) risk, passport | Unknown | Unknown | Unknown |
| Accessibility as filterable inventory | Partial (H) anchor | Yes (H) 18 filters | Unknown | Unknown | Partial (H) tokens | Unknown |
| Published accessibility statement | Unknown | Yes (M) EAA scope | Unknown | Unknown | Unknown | Unknown |
| Consent: decline with equal prominence | Partial (M) | Yes (H) | Yes (H) | Yes (H) | Unknown | Unknown |

---

## 2. Capability map

Depth is one of shallow, standard, deep, or none, with a one-line justification drawn from the profiles. Full grid in the xlsx.

| Cluster | Expedia | Booking.com | TripIt | Hopper | Google Travel | Tripadvisor |
|---|---|---|---|---|---|---|
| Vertical coverage | deep, OTA across flights/stays/cars/activities | deep, six verticals | shallow, sells nothing | standard, four verticals | standard, flights/hotels walked | standard, experiences and hotels via Viator |
| Decision support | deep, priced filters, price history, disclosure | deep, 22 filter groups, NL, ranking banner | shallow, no compare surface | shallow, results not reachable | deep, emissions sort, inline rule | standard, ranked lists with printed basis |
| Reassurance and trust | standard, reviews, sub-scores, add-on protection | deep, sub-scores with sample size, segment evidence | shallow, no reviews | standard, named paid protection | standard, review counts, discloses own gaps | deep, layered social proof plus human expert |
| Loyalty | standard, tier-gated savings | deep, tenure thresholds published | shallow, subscription not loyalty | shallow, Savings Club documented | none, aggregator | standard, Rewards |
| Prepare and itinerary | standard, Trips walled | standard, Trips walled | deep, capture, calendar, sharing, docs, visa | shallow, lookup only | shallow, bookmark and share | shallow, saved list and share |
| Travel day | shallow, not reachable signed out | shallow, overbooking remedy documented | deep, status, maps, risk alerts, gate/baggage (Pro) | standard, paid day-of assistance | none, aggregator | none, not evidenced |
| In destination | shallow, distances on property pages | standard, named transit stops | deep, navigation, safety, declared tolerance | none, not evidenced | shallow, not reachable in scope | deep, things to do, distances, AI logistics |
| After the trip | standard, verified reviews | standard, review collection | standard, ratings, compensation, carbon | shallow, referral only | shallow, emissions not tracking | deep, reviews feed rankings and awards |
| Conversational and AI | standard, shipped Q&A, assistant is vendor claim | standard, Q&A form | shallow, capture-assist article only | none, none observed | none, not in scope | deep, running planner asks pace first (caveat) |
| Personalisation and accessibility | standard, algorithmic; accessibility anchor not opened | deep, 18 filters plus statement | standard, declared risk and passport | shallow, little evidence | standard, tokens and signed-in personalisation | shallow, not sought |

---

## 3. Journey coverage table

Each cell under 12 words, with confidence. Full grid in the xlsx.

| Stage | Expedia | Booking.com | TripIt | Hopper | Google Travel | Tripadvisor |
|---|---|---|---|---|---|---|
| 1. Dream and discover | Deal-led homepage modules (H) | Theme planner, trending destinations (H) | Not evidenced (Unknown) | Deals and featured destinations (H) | Explore present, not walked (Unknown) | Interest browsing, editorial, awards (H) |
| 2. Plan and compare | Search, priced filters, price history (H) | Deep filters, NL, ranking banner (H) | None, no compare surface (M) | Search built, results not reached (Unknown) | Emissions sort, ranking rule, sellers (H) | Reviews, ranked lists, human expert (H) |
| 3. Book | Transactional OTA, checkout not walked (H) | Transactional, rate terms upfront (H) | Sells nothing (H) | OTA plus paid flexible add-ons (M) | Hands off to third-party sellers (H) | Experiences via Viator, hotels off (H) |
| 4. Prepare | Trips behind auth wall (H) | Trips behind auth wall (H) | Email capture, calendar, visa guidance (M) | My Trips lookup (H) | Saved bookmark and share (H) | Saved list, AI-plan share (H) |
| 5. Travel day | Not reachable signed out (Unknown) | Overbooking remedy documented only (M) | Status, go-now, maps, alerts, Pro (M) | Paid day-of disruption assistance (M) | None, aggregator (M) | Not evidenced (Unknown) |
| 6. In destination | Landmark and transit distances (H) | Named transit stops with distances (H) | Navigation, safety, risk tolerance (M) | Not evidenced (Unknown) | Things To Do not reachable (Unknown) | Things to do, distances, AI logistics (H) |
| 7. Return | Not separately evidenced (Unknown) | Not separately evidenced (Unknown) | Return legs tracked, implied (M) | Not evidenced (Unknown) | Not evidenced (Unknown) | Not evidenced (Unknown) |
| 8. After the trip | Verified reviews (H) | Review collection (H) | Ratings, compensation, carbon (M) | Referral program (H) | Emissions, no personal tracking (Unknown) | Reviews feed rankings and awards (H) |

---

## 4. Synonyms list

Where competitors used different names for one capability, the matrix uses a single unified name. Originals recorded here.

| Unified name in matrix | Original names in the profiles |
|---|---|
| Fare/seat/price-drop trackers | Expedia "Get notified when prices change"; Booking.com "flight price alerts" (Genius); TripIt "Fare Tracker", "Seat Tracker"; Hopper "Fare Tracker", "Seat Tracker"; Google "Track prices" |
| Price prediction (book now or wait) | Hopper "Price Prediction" |
| Named protection/guarantee product | Expedia "trip protection"; Hopper "Flexible Travel Services", "Cancel for Any Reason", "Change for Any Reason", "Premium Disruption Assistance" |
| Disruption risk alerts | TripIt "Risk Alerts"; Hopper "Premium Disruption Assistance"; Booking.com "overbooking" remedy |
| Auto itinerary capture from email/inbox | TripIt "forward to plans@tripit.com", "Inbox Sync" |
| Trips / saved surface | Expedia "Trips"; Booking.com "Trips" / "Manage your trips"; TripIt "trip" / "itinerary"; Hopper "My Trips" / "Find Booking"; Google "saved" bookmark; Tripadvisor "saved" heart |
| Loyalty programme | Expedia "One Key" / "OneKeyCash"; Booking.com "Genius"; Hopper "Savings Club"; Tripadvisor "Tripadvisor Rewards" |
| Ranking transparency disclosure | Expedia "How our sort order and personalized savings work"; Booking.com "How we work" / ranking banner; Google "How 'Top flights' are ranked" / "How options are ranked"; Tripadvisor "These rankings are informed by Tripadvisor data" |
| Sortable non-price/non-time/non-rating axis | Google "Emissions" sort |
| Emissions shown per result | Google "kg CO2e" with "Avg emissions" / relative labels; TripIt "Carbon Footprint" (trip-level, listed separately) |
| Declared-tolerance personalisation | TripIt "Personal Risk Level" |
| Neighbourhood safety scores | TripIt "Neighborhood Safety Scores" (GeoSure) |
| Interactive airport indoor maps / wayfinding | TripIt "Interactive Airport Maps" |
| Departure timing (go now) | TripIt "Go Now" |
| Entry requirements / visa guidance | TripIt "Travel Guidance" (Riskline, Basetrip) |
| AI review/property Q&A | Expedia property "Have a question?" (Beta); Booking.com property "Ask a question" |
| Conversational AI trip planner | Expedia "Romie"; Tripadvisor "Plan with AI" / "AI Assistant" |
| Accessibility as filterable inventory | Booking.com "Property Accessibility" / "Room Accessibility" filters; Google amenity tokens "Accessible" / "Wheelchair accessible"; Expedia property "Accessibility" anchor |
| Street-level navigation / wayfinding | TripIt "Navigator"; Tripadvisor AI-plan walking logistics |
| Flight-delay compensation eligibility | TripIt "AirHelp Partnership" |

### Features merged with a recorded caution

Two merges were judgement calls, recorded per the normalisation rule:

- **"Disruption risk alerts"** combines three mechanisms that are not identical. TripIt Risk Alerts are push notifications about weather, strikes and outages. Hopper Premium Disruption Assistance is a paid same-day rebooking remedy. Booking.com's is a documented overbooking policy. They share the job of handling disruption but differ in kind, so the cells carry different values and notes rather than a flat Yes across the row.
- **"Price prediction"** is kept separate from **"Price history / price insights"**. Only Hopper markets a book-or-wait prediction. Expedia and Google show price context and history, which is a weaker claim, so those sit in the insights row, not the prediction row.

---

## Gaps

What could not be verified for this inventory, and why.

| Gap | Why |
|---|---|
| Eight competitors absent | Kayak, Skyscanner, Airbnb, Rentalcars.com, Trainline, Omio, Citymapper, Rome2Rio are not yet profiled. The matrix is 6 of 14 and will shift when they are added, especially the public-transport-tickets and in-destination rows |
| Public transport tickets, whole row | No profiled competitor was verified to sell them; several are Unknown. The rail and transit specialists that would resolve this are among the eight not yet run |
| Hopper decision-support rows | Flight results were not reachable in the Hopper session, so sorts, filters and any non-price axis are Unknown rather than No |
| Google Travel signed-in | Google was walked signed in while the others were signed out. Its personalisation and ranking cells may not be comparable like for like. Flagged in the source register |
| Tripadvisor AI planner | Observed live but the chat was pre-populated on load, not driven from a clean start. The conversational-planner cell carries that caveat |
| TripIt travel-day and in-destination rows | Documented from the help centre (Medium), not seen in operation, because the product is app-first and account-walled |
| Expedia assistant (Romie) | Recorded as a vendor claim (Low), alpha and app-only. Not counted as shipped |
| Auth-walled surfaces across all OTAs | Trips, saved lists, signed-in personalisation and loyalty state sit behind sign-in and were not entered |
| Absent rows are not proof of absence | A feature with no row does not mean no competitor has it. Rows were only created where at least one profile had evidence, per the no-symmetry rule |

---

## Confidence summary

Counts are of populated competitor cells across the 55 feature rows (6 competitors, Luma excluded). A cell can hold Yes, No, Partial or Unknown; Yes and Partial carry H/M/L.

| Rating | Count | What they are |
|---|---|---|
| High (live product) | 86 | Cells observed directly in a live product this run |
| Medium (docs / help centre) | Included in the Yes/No/Partial counts below where tagged M | First-party documentation, principally TripIt, Hopper and Booking.com help pages |
| Low (marketing / inference) | 1 | The Expedia conversational-assistant cell, a vendor claim |
| Unknown | 113 | Not verified, listed structurally in Gaps |

Cell values across the six competitor columns: **Yes 86, No 48, Partial 28, Unknown 113.** The high Unknown count is deliberate. It reflects auth walls, app-only surfaces, out-of-scope areas and the eight competitors not yet run, rather than gaps filled with guesses.

No ranking, score, or recommendation appears in this document. That is Phase 4 and later.
