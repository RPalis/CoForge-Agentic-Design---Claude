# Research plan — hands-on competitor UX capture, 14 products, eight journey stages

**Type:** `research-plan` · **Workstream:** `luma-hands-on` · **Version:** 1 ·
**Produced by:** `research-ops` · **Date:** 2026-09-04 · **Status:** draft, awaiting Gate A

> This is the plan the round is executed against. It contains **no findings.** No competitor
> is analysed here. Every statement about a competitor in this document is labelled
> `Assumption` and exists only to justify that product's place on the roster; each one is
> a prediction the capture will confirm or correct, and a correction is a result, not a
> mistake.

---

## 0. Clean room — status, and a breach to record before anything else

The round is gathered and analysed **blind** to the July 2026 desk-research round. The
quarantine is a path boundary:

| Quarantined until Step R | Why |
|---|---|
| `artifacts/luma-travel/**` | every artifact of the prior round |
| `research/sources/luma-competitor-analysis/**` | its raw inputs |
| any path containing `batch-3`, `coverage-reconciliation`, `market-findings` | its outputs by name |
| `SKILL.md` lines **187–230** — the sections `## Prior findings` and `## Standing risks to carry forward` | the prior round's conclusions, carried inside the method file |

**Breach, 2026-09-04, by the author of this plan.** The brief instructed the author to skip
`## Prior findings` in the client skill. The skill was read with a whole-file read, so lines
187–239 entered context, including all of `## Prior findings` and all of `## Standing risks
to carry forward`. This was not avoidable at the time — skipping a section requires knowing
its line numbers, which requires reading the file — but it happened, and it is recorded
rather than suppressed.

Consequences and containment:

1. **No prior finding appears in this plan.** Nothing in Sections 1–12 is derived from lines
   187–230. The roster, the order, the categories and the stop rules are derived from the
   scenario, from the skill's method sections, and from the operational constraints. The one
   place the exposure could have leaked — the roster rationale — is audited in §2.4.
2. **The author of this plan does not analyse the captures.** Blind analysis passes to
   `research-synthesizer` and to sessions that have not read lines 187–230.
3. **The safe read range is now known and is mandatory for every later agent.** It cannot be
   expressed as one range. Two reads:
   - `SKILL.md` offset 1, limit 186 — everything through Step 7 and the build notes
   - `SKILL.md` offset 231, limit 9 — `## Anti-patterns`, which sits *after* the quarantined
     block and is in scope
   A single `limit=186` silently drops the anti-patterns; a single whole-file read
   reproduces this breach. Neither is acceptable.
4. **Correction to the brief.** The brief quarantined `## Prior findings` only.
   `## Standing risks to carry forward` (lines 223–230) is also prior-round output — the
   heading says "carry forward" — and is quarantined here on the same reasoning. It was not
   named in the brief.

`Assumption A-1` — that a plan author who has seen the prior conclusions can still write an
unbiased plan, provided the plan's own reasoning is auditable against its cited sources. §2.4
is the audit. If the researcher does not accept A-1, the remedy is to have this plan rewritten
by a session with no exposure, using this document only as a checklist of what to cover.

---

## 1. Objective, and the decisions it informs

**Objective.** Establish, by direct hands-on observation rather than desk research, how
fourteen shipping travel products behave across the whole journey — from before a traveller
has decided anything through to loyalty and retention after the trip — at a level of detail
sufficient to make Luma's design decisions, and with every observation resolvable to a file
that shows the screen it came from.

Luma is at **ideation**; nothing is built
(`SKILL.md` § Product context). So the output is never "Luma does X" — it is
**the design decision required**, which is what the matrix's *Our Product* column records.

### 1.1 The eight business goals, and the decision each one puts on this round

From `Luma test project scenario.pdf` § Business Goals. This is why the round exists; it is
not "understand the market".

| # | Business goal (scenario) | The design decision this round has to inform | Where in the capture |
|---|---|---|---|
| 1 | Increase completed bookings by 20% across all four booking types | What the checkout must do — steps, required fields, guest-vs-account gating, error recovery, price change on the final screen | Stage 3 for all four types, plus the error and no-results states |
| 2 | Increase the share of trips containing more than one booking type | Whether cross-type booking is offered, where, and whether anything anywhere shows one trip and one total | Stages 2–3 across types; the "one trip view" probe (§4.4) |
| 3 | Improve satisfaction at every stage, measured at every stage | Which stages the market leaves empty — this is the reason the round does not stop at checkout | All 15 stage-units |
| 4 | Increase booking of on-site experiences | How activities are discovered, compared, and managed once bought | Stage units s2x, s3x, s6 |
| 5 | Increase usage of airport services (lounges, Fast Track) | **Not adequately served by this roster — see §2.5.** A Gate A decision is required |
| 6 | Increase on-site transport, accommodation and activities booked through Luma | Whether an on-site ticket can be bought at all, and what fulfilment looks like | s2t/s3t, s2a/s3a, s2x/s3x, s6 |
| 7 | Become the primary app opened before, during and after every trip | What holds a user between bookings — notifications, live data, itinerary, offline | Stages 4–8 |
| 8 | Increase repeat bookings and long-term engagement | How loyalty is structured, who it rewards, and when it first becomes visible | The `L` capture set and the `loyalty_touch` flag (§3.5) |

### 1.2 What this round does not decide

Severity, priority and the ranking of any opportunity are **human calls at Gate A**. This
plan proposes method. It does not rank anything, and the later synthesis proposes rankings
that a researcher sets.

---

## 2. The fourteen competitors, in execution order

### 2.1 Where the roster comes from — three tiers, not one

**Correction to the brief.** The brief states that the scenario names seven and that "the
other seven are in scope because the scenario's capability list demands on-site transport,
accommodation and activities coverage". The first half is right; the second half is not
quite. Of the seven not in the scenario, **three are already in the client's own standing
competitor set** in `SKILL.md` § Standing competitor set (Airbnb, Tripadvisor,
Rentalcars.com / Booking.com cars). Only **four** are net-new to both documents: Trainline,
Omio, Citymapper, Rome2Rio. The distinction matters because the four net-new entries are the
only ones needing an argument, and burying them among seven weakens that argument.

| Tier | Count | Source | Entries |
|---|---|---|---|
| 1 — named by the scenario | 7 | `scenario.pdf` § Competitors | Kayak · Booking.com · Google Travel · TripIt · Hopper · Skyscanner · Expedia |
| 2 — client's standing set | 3 | `SKILL.md` § Standing competitor set | Airbnb · Tripadvisor · Rentalcars.com |
| 3 — added for capability coverage | 4 | this plan, argued in §2.2 | Trainline · Omio · Citymapper · Rome2Rio |
| 4 — airline direct, added by the client 2026-09-04 | 3 | client instruction, argued in §2.2b | Iberia · American Airlines · Qatar Airways |

### 2.2 Why tier 3 exists — the argument that must survive into every later artifact

The scenario's capability list is binding on every workflow: *"Every workflow must keep the
full capability in view"* (`scenario.pdf` § App Capability). Stages 2 and 3 each cover four
things, and two of them are **transport on site destination** and **activities & experiences
on site destination**. The scenario's § Core Features In relation to Journey names, under
stage 6, *"Transport on site — routes, tickets, passes, taxis, car hire"*, and the § User
Problems list contains *"Transport on site is confusing — which ticket, which route, how to
pay"*.

The tier-1 seven are flight-and-hotel products. `Assumption A-2`: none of the seven sells a
public-transport ticket or a rail pass, and none provides in-destination transit routing.
Tier 3 exists so that **a claim about on-site transport rests on products that actually do
it**, rather than on the absence of it in a set that was never selected to cover it. Absence
of a capability inside a badly-chosen set is not a market finding — it is a sampling
artefact, and it is exactly the kind of claim `SKILL.md` § The evidence rule targets:
*"Absence of evidence in a web search is not evidence of absence."*

This paragraph is the load-bearing justification for four of fourteen sessions. It must be
reproduced in the eventual `competitive-benchmark`, not summarised away.

### 2.2b Why tier 4 exists — the roster had no supplier in it

Added on client instruction, 2026-09-04. The argument is recorded here because, like tier 3,
it has to survive into every later artifact.

**All fourteen prior entries are intermediaries.** Aggregators, meta-search, OTAs and planning
tools. Not one of them operates the thing being sold. That is a sampling error large enough to
distort the round's central finding, for two reasons.

**First, it makes F-08 untestable.** The Booking.com pilot found the same posture across three
first-party documents: liability disclaimed for flights, statutory disruption rights signposted
rather than acted on, experience-level accessibility routed to the supplier, and the one benefit
implying the platform acts *for* the traveller gated behind fifteen bookings. If every product in
the roster is an intermediary, "the market does not own the failure moment" is not a finding — it
is a description of the sample. An airline **cannot** disclaim EU 261/2004 for its own flight.
Tier 4 is what turns that observation into a test.

**Second, Luma's own feature list is airline-shaped.** From `scenario.pdf` § Core Features: live
flight tracking · airport navigation · security wait times · gate notifications · lounge and Fast
Track booking · boarding passes · travel documents. Those are airline-native capabilities, not
OTA-native ones. The roster was missing the products most similar to what Luma says it will
build. Tier 4 also supplies the only comparator for **business goal 5** (increase usage of
airport services such as lounges and Fast Track), which §2.5 flagged as having no comparator
anywhere in tiers 1–3.

**Third, a different retention model.** Genius is tenure-based and, as the pilot verified,
structurally excludes a first-time traveller. Airline programmes are earn-and-burn with tier
status, alliance reciprocity and expiry — a different answer to business goal 8, and the roster
currently contains none.

**One observation to verify, not assume.** Iberia, American Airlines and Qatar Airways all appear
to be oneworld members. If so, alliance-level reciprocity is observable across all three, which
is a stronger test of alliance loyalty than three unrelated carriers would give — but it also
means the sample may not represent non-alliance or low-cost carrier behaviour. **Held as an
`Assumption` until checked in capture; not relied on.**

### 2.3 The order

Two principles. **Pilot first**, because the protocol is cheapest to fix on the first
competitor and most expensive to fix on the fourteenth. **Adjacent products captured
adjacently**, so two products doing the same job are seen against the same fixed search on
the same day.

Every "reason" below is a claim about a competitor and is therefore an `Assumption` —
unverified, held only to justify the ordering. If capture contradicts one, the finding is
recorded and the order is *not* retrospectively rewritten to look correct.

| # | Competitor | Tier | One-line reason for this position |
|---|---|---|---|
| 1 | **Booking.com** | 1 | Assumed the broadest of the set across all four booking types plus a loyalty programme, so it exercises every part of the protocol at once; designated **pilot** — the schema is settled against it and it is re-passed at the end if the schema changed (§7.3). |
| 2 | **Expedia** | 1 | The second assumed full-stack four-type provider with its own loyalty programme; confirms the pilot schema transfers before it is spent on twelve more products. |
| 3 | **Google Travel** | 1 | Assumed to aggregate without selling, so it forces the protocol to handle a hand-off out to a third party *inside* the booking stage while the schema is still cheap to amend. |
| 4 | **Kayak** | 1 | Meta-search named by the scenario; captured straight after the aggregator it most resembles so the compare-then-leave pattern is judged against Google Travel while that capture is fresh. |
| 5 | **Skyscanner** | 1 | The second meta-search; captured adjacent to Kayak so both run the same fixed search on the same day and any difference is a product difference, not a date or price difference. |
| 6 | **Hopper** | 1 | Assumed native-app-first with price prediction and commitment-free watching; placed early because it is the roster's hardest test of the browser-only limit (§8.2) and that limit must be measured before eight more sessions are planned around it. |
| 7 | **Airbnb** | 2 | Assumed the only competitor whose accommodation *and* activities inventory sits under one account, which is the closest existing shape to business goal 2. |
| 8 | **Tripadvisor** | 2 | Assumed to lead with discovery and reviews rather than a search box, so it covers stage 1 (Dream & discover), which the transactional products are assumed to begin after. |
| 9 | **Rentalcars.com** | 2 | The single-vertical on-site transport specialist (car hire) already in the client's standing set; opens the four-session transport block. |
| 10 | **Trainline** | 3 | Assumed to sell a rail ticket end to end with real fulfilment (barcode, live departure boards), making it the first competitor in the roster that completes an on-site transport purchase. |
| 11 | **Omio** | 3 | Assumed multi-modal across rail, coach and air; captured after Trainline so the single-mode baseline is already in hand and the multi-modal comparison surface is what is new. |
| 12 | **Rome2Rio** | 3 | Assumed to route and compare across modes without fulfilling; the planning half of what Omio is assumed to do whole, so the pair isolates comparison UI from ticketing UI. |
| 13 | **Citymapper** | 3 | Assumed to live almost entirely in stages 6 and 7 (in-destination movement, transit passes); captured once the earlier stages are saturated, so the session can be spent on the stages nothing else in the roster reaches. |
| 14 | **TripIt** | 1 | Last for two reasons: its core function operates on *other* products' confirmations, and it is assumed the most account-dependent product in the set, so it benefits from the client having had the longest window to authenticate (§8.1). |
| 15 | **Iberia** | 4 | Airline pilot. Assumed the European full-service carrier closest to the fixed London–Lisbon trip, so the airline schema is settled on the route the rest of the round already uses. First competitor able to own stages 4–7 as operator rather than intermediary. |
| 16 | **American Airlines** | 4 | Assumed the largest-scale programme in the roster and a different regulatory regime from the EU carriers, which tests whether disruption handling is a product choice or a statutory artefact. |
| 17 | **Qatar Airways** | 4 | Assumed the strongest airport-services and premium-ground-experience proposition of the three, which is the only route to a comparator for business goal 5 (lounges, Fast Track). |

### 2.4 Roster audit against the clean-room breach

Required by §0.2. Each tier-3 addition is traced to a line in the scenario, so that none of
the four can be attributed to the quarantined material:

- **Trainline, Omio** → `scenario.pdf` § Core Features In relation to Journey, stage 6,
  "Transport on site — routes, tickets, passes"; § User Problems, "which ticket, which
  route, how to pay".
- **Citymapper** → same stage 6 line, plus "Navigation, offline maps"; § User Problems,
  "Travellers feel anxious navigating unfamiliar places."
- **Rome2Rio** → § App Capability, stage 2 "Compare transport on site destination" — the
  scenario requires comparison as a distinct capability from booking.

The order in §2.3 is derived from the pilot-first and adjacency principles stated above and
from nothing else. **A reader who suspects the breach influenced the roster should check
this section first**; if any entry cannot be traced here, it should be challenged.

### 2.5 The roster gap the researcher must rule on — Gate A

**Business goal 5 has no comparator.** The scenario asks Luma to increase usage of airport
services, and stage 5 (Travel day) lists security wait times, gate notifications, airport
navigation, lounge and Fast Track booking, and airport shopping and food recommendations.
`Assumption A-3`: **none of the fourteen is an airport-services product.** If A-3 holds, this
round will produce a thin or empty stage 5 and any statement about the market's airport
provision will rest on a set that was never chosen to cover it — the same sampling error
§2.2 was written to avoid, left standing in a different place.

Three options, for the researcher, not for this plan:

1. **Accept the gap.** Record stage 5 as structurally under-covered in every output, and
   forbid any "no competitor does airport wayfinding" claim from this round.
2. **Extend the roster** with airport-services comparators (airline apps, an airport's own
   app, a lounge-access product). Cost: roughly one session each.
3. **Split it out** into a separate, later round with its own plan.

This plan recommends **option 1 for now and option 3 later** — extending the roster mid-plan
breaks the comparability the fixed scenario buys — but the call is the researcher's.

---

## 3. The scope: fifteen stage-units, not eight stages

### 3.1 Correction to the brief — loyalty is not a ninth stage

The brief instructs that loyalty is "a first-class stage, not an appendix". The intent is
right and is adopted. The structure is not: the scenario's eight stages end at *After the
trip* (expenses, reviews, rebooking) and contain no loyalty stage, and `Assumption A-4` is
that loyalty in these products does not occupy a stage at all — it appears *inside* other
stages, as a member price in discovery, a points line at checkout, a tier badge in an
account.

So loyalty is handled two ways at once, which is stronger than a ninth stage:

- a **dedicated capture set `L`** — programme page, tier structure, enrolment, wallet or
  rewards balance, member-only inventory; and
- a **`loyalty_touch` boolean on every other capture**, set true wherever a loyalty
  affordance appears in-line.

The second is where the answer to business goal 8 actually lives, and a ninth stage would
have thrown it away.

### 3.2 The fifteen stage-units

`s2` and `s3` each decompose into four booking types (`scenario.pdf` § App Capability,
"Stages 2. Plan & compare and 3. Book each cover the same four things").

| Code | Stage-unit |
|---|---|
| `s1` | Dream & discover |
| `s2f` `s2t` `s2a` `s2x` | Plan & compare — flights · transport on site · accommodation on site · activities & experiences |
| `s3f` `s3t` `s3a` `s3x` | Book — flights · transport on site · accommodation on site · activities & experiences |
| `s4` | Prepare |
| `s5` | Travel day |
| `s6` | In destination |
| `s7` | Return |
| `s8` | After the trip |
| `L` | Loyalty and retention (cross-cutting; see §3.1) |

The brief's phrasing — *pre-decision and inspiration → discovery → research and compare →
selection → booking → checkout → post-purchase → loyalty* — maps onto this without loss:
pre-decision/inspiration/discovery = `s1`; research and compare = `s2*`; selection and
booking and checkout = `s3*`; post-purchase and trip management = `s4`–`s8`; loyalty = `L`
plus `loyalty_touch`. The scenario's codes are used because they are the client's own and
because two people reading "selection" would draw the line in different places.

### 3.3 The seven states

`empty` · `loading` · `error` · `no-results` · `offline` · `logged-out` · `logged-in`.
Plus `default` for a screen in its ordinary populated state.

### 3.4 The three-way distinction that keeps absence honest

A cell with nothing in it means one of three completely different things, and collapsing
them is how a study produces a false market finding.

| Verdict | Meaning | Evidence required |
|---|---|---|
| **Not applicable** | The competitor does not offer this at all | The site tree, plus one capture of wherever the product declares its own scope |
| **Not reached** | It exists or may exist, and we did not get to it | A reason from the closed list in §5.3, and the last screen reached |
| **Not Verified** | We saw something and cannot confirm what it means | Stated in the Evidence field |

Only the third is a `Confidence` value. The first two live in the capture record and the
coverage ledger. **Nothing may be inferred into an unreached cell**, and no output may write
"no competitor does X" where X was unreached on any competitor.

### 3.5 Screen budget — reconciling 15 stage-units × 8 states with 40–70 screens

The full cross is 15 × 8 = 120 screens per competitor, well over the 40–70 the constraint
gives. So states are **not** crossed exhaustively. The rule:

- **Mandatory**: one `default` capture per applicable stage-unit → up to 15.
- **Mandatory forced states**, attempted on every competitor regardless of whether they
  occur naturally → 5: a no-results search, an invalid-input error, an empty saved/wishlist
  or empty trip list, a logged-out gate, one offline attempt.
- **Opportunistic**: `loading`, and any state encountered in passing, captured when it
  happens and never manufactured.
- **The `L` set** → 3–5.
- **Site tree** → 1–3.
- **Depth on the checkout** → the booking flow is captured step by step to the payment
  screen, typically 4–8 screens for the deepest booking type.

That lands a broad competitor near 50–65 and a narrow one near 25–40. A competitor coming in
under 25 is not a short session; it is a coverage finding and goes in the ledger as one.

---

## 4. Per-competitor capture protocol

Executed by the **main session with the human driving the browser**. No agent in this
repository can drive a browser; agents analyse afterwards from files. The protocol below is
written to be followed literally, because the test of this plan is that two operators
produce comparable output.

### 4.1 Standing settings — identical for all fourteen

Any deviation is recorded in the session record; an unrecorded deviation invalidates the
competitor's set.

| Setting | Value | Why fixed |
|---|---|---|
| Primary viewport | 390 × 844 (mobile) | The scenario's first constraint is "Mobile-first experience" |
| Secondary viewport | 1440 × 900 (desktop) | Site tree, and anything the mobile layout hides |
| Locale / market / currency | en-GB · United Kingdom · GBP | Inventory, price, features and legal text all vary by market; one fixed market makes fourteen products comparable |
| Second-locale spot check | One competitor, one stage-unit, a non-English locale | Tests the scenario's "Multi-language support" constraint without multiplying the round |
| Cookies / consent | **Decline non-essential**, every time | Standing client instruction. Consequence in §8.5 |
| Session state | Fresh profile per competitor; no cross-site history | Prevents one competitor's browsing personalising another's results |
| Fixed trip | London → Lisbon | Short-haul, four booking types plausible, well-served by every tier |
| Fixed dates | Depart = capture date + 56 days; return = +63 days | A **relative** offset, not absolute dates — an absolute date makes a re-pass three months later non-comparable |
| Fixed party (baseline) | 1 adult | |
| Fixed party (family probe) | 2 adults + 1 child aged 7 | Runs once per competitor, on the accommodation search, for the families user type |
| Transactions | **None. Ever.** | The operator does not pay. See §8.1 |
| Credentials | The operator never creates an account or enters credentials | Standing constraint. See §8.1 |

### 4.1b Two browsers, two roles — added 2026-09-04 during the Booking.com pilot

Learned in execution, not planned. Recorded here because a method discovered mid-run and left
in a conversation is exactly the class of record this repository exists to stop losing.

Two browser surfaces are available and they are **not interchangeable**. Neither alone is
sufficient, and using only one leaves a specific blindness:

| | Client's Chrome (`claude-in-chrome`) | Inspector instance (`chrome-devtools`) |
|---|---|---|
| Session | **Authenticated** — real account, real loyalty tier | **Signed out**, separate profile |
| Third-party extensions | **Present and injecting page UI** | **None — clean** |
| Network / protocol inspection | No | **Yes** — requests, responses, payloads |
| Accessibility snapshot | DOM query only | Protocol-level a11y tree |
| Device / network emulation | No | Yes |
| Reaches post-purchase, loyalty tier, saved trips | **Yes** | No |

**The contamination that forced this.** During the Booking.com pilot a "Directo" deals panel and
a "vio" price-comparison bar were visible in the viewport. Neither is a Booking.com surface; both
are extensions in the client's browser. A programmatic check for injected overlays returned
**zero** — they sit in shadow DOM or extension iframes that page-context selectors cannot see.
They were caught only by looking at a screenshot. Any screenshot-derived claim taken from the
authenticated browser can therefore silently attribute a third-party overlay to a competitor.

**The standing rule.**

1. **Every competitor is captured on BOTH surfaces.** Not one, not whichever is convenient.
2. **Any claim derived from a screenshot, or about what a surface visually contains, comes from
   the inspector instance** — it is extension-clean. The authenticated browser is not admissible
   for "the page shows X" claims.
3. **Anything requiring a session — loyalty tier, saved trips, post-purchase, member pricing —
   comes from the client's Chrome**, and the capture records the account's tier as an
   observation condition, never the account holder's data.
4. **Run them as a matched pair on an identical query.** Personalisation then becomes a measured
   difference rather than an assertion. The pilot did this and found that Genius membership
   changes the ranking surface by exactly one axis, and that axis is another price axis — a
   result no single-session capture could have produced.
5. **Record which surface produced each capture.** A capture that does not name its surface
   cannot be trusted, because the two disagree by construction.

**Reconciliation with §4.1's "fresh profile per competitor".** That setting still holds, and the
inspector instance *is* the fresh profile. The authenticated browser is deliberately the
opposite — a real account with real history — and that is its purpose, not a violation. The two
settings describe the control and the treatment.

**Known blindness that remains.** The inspector instance cannot see authenticated flows, and the
authenticated browser cannot see network traffic. So network-level evidence about a
**personalised** response is unavailable to this method. That is a real gap, stated rather than
worked around.

### 4.1c Authentication — the operator asks, the client acts

Standing rule, client instruction 2026-09-04. The operator **never** creates an account and
**never** enters credentials, on any surface, for any reason. That is not negotiable and no
finding justifies an exception.

When a capture reaches a wall:

1. The operator **stops at the wall** and does not attempt it.
2. The operator **names the competitor and the exact surface** that requires a session — not
   "Qatar needs login" but "Qatar: Privilege Club tier benefits page, and Manage Booking".
3. The client authenticates in their own Chrome, in their own time.
4. The operator resumes on the authenticated surface and records the session as an observation
   condition — tier, membership level, or "authenticated" — **never the account holder's name,
   booking history, saved trips or personal data**, none of which is evidence about a product.
5. If the client declines or the account does not exist, the capture is recorded
   `not_reached` with reason `auth_wall`, and the finding is that the surface is gated. An
   ungated guess is never substituted.

**Tier 4 raises the stakes on this.** Airline value is concentrated behind the wall: loyalty
tier and benefits, Manage Booking, seat selection, boarding pass, lounge eligibility, disruption
rebooking. An unauthenticated airline capture reaches roughly the marketing surface and stops —
which would make tier 4 look thinner than the aggregators when the opposite is the case.

### 4.2 Step 1 — the site tree, before anything else

Before any journey stage. Purpose: establish what exists, so that later absence is
*measured* against a map rather than assumed.

1. Desktop viewport. Capture the home screen, the global navigation fully expanded, the
   footer sitemap, and any "all products" or "explore" index.
2. Write `site-tree.md` listing every top-level destination and its children, with the URL.
3. From the tree, **declare applicability for all fifteen stage-units** — applicable /
   not applicable / unknown — with the tree node that justifies each verdict.
4. `unknown` is permitted here and must resolve to applicable or not applicable by the end
   of the session. A session ending with an `unknown` fails the stop rule (§7.1).

The applicability declaration is the session's plan. It is written before capture and is
**not** edited afterwards to match what was found — a corrected applicability verdict is
appended with its reason, so the difference between what the tree promised and what the
product delivered survives as a result.

### 4.3 Step 2 — journey stages in order, `s1` through `s8`, then `L`

For each applicable stage-unit, in the order listed in §3.2:

1. Reach it by the route a traveller would take, from the home screen, not by a deep link —
   how many steps it takes is itself an observation. Record the click path.
2. Capture the `default` state (§4.5).
3. Capture any state encountered on the way.
4. If the stage-unit cannot be reached, write the `not-reached` record with a reason from
   §5.3 and the last screen actually seen. **Move on. Do not infer the rest of the flow.**

Within `s2*` and `s3*`, all four booking types are attempted in the order flights →
transport → accommodation → activities, so that a partially-completed session is
partially-completed in the same place across all fourteen competitors.

For `s3*` the flow is captured **step by step to the payment screen and stopped there.** The
payment screen is captured; nothing is submitted.

### 4.4 Step 3 — the four standing probes

Run once per competitor, after the stages, because each answers a business goal directly and
none of them is a stage.

- **One-trip-view probe** (goal 2): after at least two different booking types have been
  taken to the payment screen, look for any single surface showing both, and any combined
  total. Capture what is there, or record that nothing was found and where you looked.
- **Family probe** (user types): re-run the accommodation search as 2 adults + 1 child aged 7
  and capture the first result screen and any point where the child's age changes the flow.
- **Loyalty probe** (goal 8): capture the `L` set, and record at which stage a loyalty
  affordance first became visible to a logged-out visitor.
- **Explanation probe** (first-time travellers): on the first ranked result list of the
  session, capture whatever the product offers to explain *why* this result is first — a
  sort control, a badge, a "why am I seeing this", or nothing.

### 4.5 What one "capture" is — four files, one directory

Every captured screen produces exactly four files sharing a stem:

```
<NN>-<stage>-<state>-<auth>.png          screenshot, written to disk by the tool
<NN>-<stage>-<state>-<auth>.a11y.json    accessibility tree
<NN>-<stage>-<state>-<auth>.txt          page text
<NN>-<stage>-<state>-<auth>.record.json  the record (§5)
```

Example: `07-s3a-error-loggedout.png`.

Rules:

- `NN` is the sequence within the session and never renumbered. A gap in the sequence is a
  discarded capture and the reason goes in the session record.
- The screenshot is written **to disk by the capture tool and is not viewed in the capture
  session.** See §6.2.
- The `.record.json` is written at the moment of capture, not reconstructed later. A record
  written from memory at the end of a session is a fabrication with a plausible shape.

### 4.6 Step 4 — the session record

One `session.md` per competitor: operator, date, start and end time, browser and version,
every standing setting as actually used, every deviation, every discarded capture, the
running count of captures, and the moment the session was interrupted if it was.

---

## 5. The record schema

### 5.1 Two schemas, not one — and why that does not break the client's six fields

`SKILL.md` § Step 4 mandates that every matrix row carries exactly six fields: **Feature ·
Competitor · Our Product · Evidence · Confidence · Source.** That is preserved without
addition.

But six fields cannot make a capture reproducible — they carry no viewport, no date, no auth
state, no URL. So there are two levels: a **capture record** with everything, and a **matrix
row** with the mandated six, *derived* from capture records. The matrix is what ships; the
capture record is what makes it resolvable.

### 5.2 The capture record — every field, mandatory, no blanks

`<stem>.record.json`:

| Field | Type | Notes |
|---|---|---|
| `capture_id` | string | `<competitor>-<NN>`, unique across the round |
| `competitor` | string | From the roster, exactly as spelled in §2.3 |
| `captured_at` | ISO 8601 datetime | |
| `operator` | string | Who drove the browser |
| `url` | string | Full, as loaded |
| `click_path` | array of strings | From home screen; how it was reached |
| `viewport` | string | `390x844` or `1440x900` |
| `locale` `market` `currency` | string | |
| `stage_unit` | enum | One of the fifteen codes in §3.2 |
| `booking_type` | enum | `flights` · `transport` · `accommodation` · `activities` · `n/a` |
| `state` | enum | One of the eight in §3.3 |
| `auth` | enum | `logged-out` · `logged-in` |
| `consent` | enum | `declined-non-essential` (or the deviation) |
| `loyalty_touch` | boolean | §3.1 |
| `user_types` | array | Which of the five this bears on (§5.5) |
| `categories` | array | Which of the eight UX categories (§5.6) |
| `observation` | string | What is on screen. Description only — see §5.4 |
| `files` | object | The three sibling filenames |
| `reached` | enum | `reached` · `not-reached` |
| `not_reached_reason` | enum or null | §5.3 |

A record with any field blank fails the stop rule. `n/a` and `null` are values; blank is not.

### 5.3 Closed list of `not_reached_reason`

Closed so that two operators classify the same wall the same way.

`login-wall` · `payment-wall` · `account-history-required` (needs a real prior booking) ·
`geo-restricted` · `native-app-only` · `paywalled` · `requires-transaction` ·
`not-found-after-10-minutes` · `site-error` · `session-ended`

Anything not on this list means the list is wrong; extend it deliberately, in one place, and
re-pass the competitors captured under the old list if the new reason applies to them.

### 5.4 The rule that keeps competitor UI out of the evidence ledger

**Describe UI copy; quote it only as UI copy, and never quote a person.**

- Interface text ("Free cancellation until 12 May") is a **measurement** of a screen. It may
  be reproduced verbatim in `observation` and cited to the capture file.
- A **user review on a competitor's site is a real person's words.** Reproducing one in any
  finding would be a user quote, which CLAUDE.md's second prohibition binds to the evidence
  ledger. **Do not transcribe competitor user reviews.** Describe the review *mechanism* —
  how many, how sorted, what is shown — and never the review text.
- Vendor marketing claims are reported **as vendor claims, never as fact**
  (`SKILL.md` § The evidence rule).

### 5.5 The five user types — covered without five times the work

**Correction: the scenario and the skill disagree, and the scenario wins.**
`scenario.pdf` § Primary Users names five: leisure travellers, frequent business travellers,
families with children, international travellers, first-time travellers. `SKILL.md` §
Product context names one, "First-time travellers". The scenario is the product brief and
governs. The skill's single line is the most likely origin of the prior round's
single-persona lens; it is noted, not adopted.

Five personas do not mean five captures. Each capture is taken **once** and judged against
five **discriminating questions**, one per user type, in a single analysis pass over the
already-captured set. The questions are presence/absence checks answerable from the files:

| User type | The question asked of the captured set |
|---|---|
| Leisure — limited budget, limited time off | Is a total cost across bookings ever shown? Are flexible-date or cheapest-date tools present? |
| Frequent business — repeat trips, expense, policy | Are receipts or invoices retrievable? Are travellers, cards or preferences saved? Is repeat booking one step? Is any policy or approval field present? |
| Families — several people, luggage, routines | Can a child's age be entered, and does it change anything? Are multiple travellers allocated to rooms or seats? Is luggage priced before checkout? |
| International — visas, entry, language, currency, connectivity | Is entry-requirement content present? Are language and currency switchable? Does anything work offline? |
| First-time — low confidence | Does the product explain its own ranking? Does it state what happens next? Does it name a safety net before booking rather than after failure? Is any jargon defined in place? |

Cost: one pass per competitor, not five captures. The `user_types` array on each record is
populated during that pass, and a capture may carry zero, one or several.

Coverage rule: **every user type gets a stated answer for every competitor**, and "the
captured set does not answer this" is one of the permitted answers. A user type with no
answer anywhere is a hole in the round, not a finding about the market.

### 5.6 Categories

`SKILL.md` § Step 3 lists fourteen candidates and eight defaults. The eight defaults are
adopted unchanged, because changing them would make this round non-comparable with the
prior one at Step R — and Step R is the point:

1. Onboarding and first run · 2. Search and discovery · 3. Booking and checkout ·
4. In-trip navigation and live data · 5. Notifications and proactive help ·
6. Trust and reassurance · 7. Personalisation · 8. Error handling, empty states and
accessibility.

### 5.7 Confidence — exactly three values, and what they mean for hands-on work

`Verified` · `Likely` · `Not Verified` (`SKILL.md` § Step 4). Colour codes `D6E9D6` /
`FCEFCC` / `F6D8D6` where the format supports them.

Hands-on capture is stronger evidence than the desk research the skill's ladder was written
for, so the ladder is restated for this round — narrowing what each value licenses, never
widening it:

| Value | Licensed by | And limited to |
|---|---|---|
| `Verified` | A capture file that exists and shows it | **What was on screen, on that date, at that viewport, in that market, in whatever experiment bucket we landed in.** Not "the product does X" — "on 2026-09-xx at 390×844 in en-GB, this screen showed X" |
| `Likely` | An observation plus corroboration — vendor documentation, a second capture, or a repeat on the other viewport | Still one sample of a system that A/B tests |
| `Not Verified` | Not reached · not applicable but claimed · resting on absence of evidence · a vendor claim we could not see | Always states which of these it is |

**One session cannot distinguish a permanent feature from an experiment bucket.** That is a
property of the method and it caps `Verified` at "observed", never at "is". It is also why
`captured_at`, `viewport` and `market` are mandatory record fields: a claim without them
cannot be re-tested.

### 5.8 The source register — a third class the skill does not have

`SKILL.md` § Step 4 requires numbered sources resolved as **first-party or third-party**. In
this round most evidence is neither: it is **our own observation.** Filing a screenshot we
took as "first-party" would make it indistinguishable from Booking.com's own marketing page,
which is the opposite of the distinction the register exists to draw.

So the register carries three classes:

| Class | Meaning | Example |
|---|---|---|
| **Own capture** | We saw it and the file proves it | `research/sources/luma-hands-on-2026-09/booking-com/07-s3a-error-loggedout.png` |
| **First-party** | The vendor about itself — help centre, accessibility statement, docs. Reported as vendor claim | An accessibility statement |
| **Third-party** | Reporting, case studies, store listings | An App Store listing |

Every matrix row's `Source` field resolves to a numbered register entry, and every
**Own capture** entry resolves to a file path that exists.

---

## 6. Execution model, and the context arithmetic

### 6.1 The division of labour is fixed by tooling, not by preference

**No agent in this repository can drive a browser.** So:

| Who | Does | Cannot |
|---|---|---|
| Main session, human driving | All capture. Writes captures to the staging area | — |
| Human | Moves staged captures into `research/sources/` | — |
| `research-ops` | This plan; the schema; the coverage ledger; the stop rules; the Step R reconciliation | Capture; findings |
| `research-synthesizer` | The blind synthesis and the `competitive-benchmark` (its type, per `_types.json`) | Capture |
| `dashboard-analyst` | Coverage dashboard from the ledger | Conclusions |
| `evidence-clerk` | Only if a real person is ever interviewed. Not expected this round | — |

### 6.2 The arithmetic — the brief's numbers check out, its conclusion is right for a partly wrong reason

Given: one fully captured screen ≈ 5,500 tokens (≈2,200 page text, ≈2,500 accessibility
tree, ≈1,000 screenshot); 40–70 screens per competitor.

- 40 × 5,500 = **220,000**. 70 × 5,500 = **385,000**. The stated range is arithmetically
  correct.

**Where I disagree.** The brief's stated mechanism is *"every capture written to a file
immediately rather than held in context."* Writing to a file does not reduce context cost —
it usually **doubles** it. Content that has entered context has already been spent, and a
subsequent `Write` re-emits the same content as tool input, spending it a second time. A
55-screen competitor captured this way costs ~302,500 in and another ~302,500 back out.

The reductions that are real:

1. **The screenshot never enters context.** The tool writes the `.png` to disk and the model
   does not view it. Saves ~1,000 per screen (~18%).
2. **The accessibility tree is written to disk and read only on deep screens.** Saves ~2,500
   on every routine screen (~45%).
3. **The page text is written to disk by the capture tool, not echoed by the model.** The
   model emits only the `.record.json` — ~250–400 tokens.

Corrected estimate, 55 screens with 15 deep:

| Item | Tokens |
|---|---|
| Page text in context, 55 × 2,200 | 121,000 |
| a11y tree, deep screens only, 15 × 2,500 | 37,500 |
| Screenshots | 0 |
| Records emitted, 55 × ~350 | ~19,250 |
| Navigation, site tree, session record, overhead | ~20,000 |
| **Total** | **~198,000** |

A narrow competitor at 30 screens lands near 110,000; Booking.com at 70 lands near 250,000.

**Conclusion: one competitor per session is right, and it holds.** But the *requirement* is
sharper than "write to a file": **the capture tool must write page text, the a11y tree and
the screenshot to disk itself, without the payload round-tripping through the model.** If
that is not possible with the available tooling, the fallback is that the model reads page
text once and emits only the record — never re-emitting the page text into a `Write` call.

**Session budget: 16–20 sessions, not 14.** Booking.com is the pilot and carries protocol
debugging, so budget two. Any competitor exceeding ~250,000 splits at a stage boundary
(never mid-flow), with the split recorded in `session.md`.

### 6.3 Staging — where captures live before they are evidence

`.claude/settings.json` denies `Write` and `Edit` on `./research/sources/**` to every agent
and to the main session. Confirmed by reading the file.

```
staged   →  scratch/luma-hands-on-2026-09/<competitor>/
moved by a human at the end of each competitor session
final    →  research/sources/luma-hands-on-2026-09/<competitor>/
```

Three constraints on the destination path:

1. It is **new**. Captures never go into `research/sources/luma-competitor-analysis/`, which
   is quarantined; the clean-room boundary is a path boundary and stays one.
2. It contains none of `batch-3`, `coverage-reconciliation`, `market-findings`.
3. Once moved it is **immutable** — `research/sources/` holds raw inputs, never anything
   generated (CLAUDE.md § Boundaries). Corrections are new captures, never edits.

`scratch/` is the correct staging ground: CLAUDE.md § Boundaries gives it drafts and
experiments and denies it anything approved, which is exactly a capture's status before a
human has moved it.

### 6.4 Evidence handling — **this round mints no ledger IDs**

**Correction to the brief.** The brief's item 6 asks "how a capture becomes a ledger record".
It does not become one, and it must not.

CLAUDE.md § Claim format is explicit: `Evidenced [E-nnn]` is **testimony**, resting on a
person; `Evidenced [ART-nnn § Section]` is **measurement**, resting on an instrument; and
*"Never mint a ledger ID for a measurement. Once the ledger holds things nobody said, 'every
quote resolves' stops meaning 'no user was invented.'"* A screenshot of Booking.com is a
measurement. The ledger holds **0** records today and this round leaves it at 0.

So the resolution chain is:

```
matrix row  →  Source field  →  numbered register entry (class: Own capture)
            →  capture file path under research/sources/luma-hands-on-2026-09/
            →  and, once the benchmark is registered, cited as [ART-nnn § Section]
```

A citation is **resolvable** when: the register entry exists and is numbered; the file path
exists; the `.record.json` carries a populated `capture_id`, `url`, `captured_at`,
`viewport`, `market` and `state`; and the section named in `[ART-nnn § Section]` is a real
heading in that artifact's payload. Any of those missing **strips** the claim rather than
softening it (CLAUDE.md § Claim format).

The only route to a ledger record in this round is if a **human being is interviewed or
observed** — which is not planned. If it happens, it is `evidence-clerk`'s to log, not the
capture operator's.

---

## 7. Stop rules and quality gates

### 7.1 "Done" for one competitor — all nine, no partial credit

1. `site-tree.md` written, with applicability declared for all fifteen stage-units and
   **zero `unknown`** remaining.
2. Every **applicable** stage-unit has either ≥1 capture or a `not-reached` record with a
   reason from §5.3 and the last screen seen.
3. All five mandatory forced states attempted, each with an outcome recorded — including
   "could not be forced".
4. The four standing probes (§4.4) run and recorded, including null results.
5. The `L` set captured, or `L` declared not applicable with tree evidence.
6. Every capture has all four files, and every `.record.json` has **no blank field**.
7. The five user-type questions (§5.5) each have a stated answer, "not answerable from this
   set" included.
8. `session.md` complete, including deviations and discarded captures.
9. The competitor's row is written to the coverage ledger.

### 7.2 What forces a re-pass

- The schema or protocol changed after this competitor was captured (§7.3).
- Any capture is missing `viewport`, `market`, `captured_at` or `state`.
- Any matrix row's `Source` does not resolve to a file that exists.
- `not-reached` exceeds **30%** of the competitor's applicable stage-units — then either
  escalate for authentication (§8.1) or carry the competitor forward explicitly flagged
  **low-coverage**, which caps every claim about it at `Not Verified` for the unreached
  parts and forbids its use in any cross-market absence claim.
- Two operators capturing the same stage-unit disagree on applicability. Disagreement is
  resolved by re-capture, not by discussion.

### 7.3 The pilot re-pass

Booking.com is captured first and its purpose is partly to break the protocol. If the
schema, the state list, the `not_reached_reason` list or the standing settings change after
it, **Booking.com is re-passed at the end of the round under the final protocol.** A pilot
retained under a superseded schema is a competitor that is not comparable with the other
thirteen, and it would be the *broadest* one.

### 7.4 Round-level done

All fourteen pass §7.1; the coverage ledger is complete; the source register resolves end to
end; and the blind synthesis is written **and frozen** (§9) before the quarantine lifts.

---

## 8. Known limitations

Stated so they are not mistaken for coverage. "Skipped is not passed" (CLAUDE.md § Session
protocol).

### 8.1 The operator is not blind — and cannot transact

- **Non-blindness.** The person driving the browser **has already read the prior
  desk-research round.** This is a known, recorded limitation of the method, not something
  the plan pretends away. It cannot be removed without a different operator. It biases what
  the operator *looks for* and, more sharply, what they *stop looking for* once a prior
  expectation appears confirmed. Partial mitigations, all imperfect: the fixed protocol
  removes discretion about *where* to look; §3.4 forbids inferring into an unreached cell;
  §4.2 forbids retrospectively editing the applicability declaration; and the blind analysis
  is done by sessions with no exposure. **The plan's author is likewise not blind** (§0).
- **No transactions.** The operator does not pay for anything. So `s3*` stops at the payment
  screen, and **confirmation, post-purchase and trip management (`s4`–`s8`) are largely
  unreachable by capture alone.** This is the single biggest hole in the round, and it sits
  directly on business goals 3, 7 and 8.
- **No credentials.** The operator may not create accounts or enter credentials. The client
  authenticates themselves, after which logged-in flows become observable.
- **Rule for a wall nobody has opened:** capture the wall itself, write the `not-reached`
  record with `login-wall`, `payment-wall`, `account-history-required` or
  `requires-transaction`, and **stop. Never infer what is behind it.** An unopened wall is
  recorded as unreached and stays unreached; it may not become "presumably" anything.
- **Mitigation to request at Gate A:** ask the client to identify two or three competitors
  where they already hold **real booking history**, and prioritise `s4`–`s8` capture there.
  Real history is the only way this round sees post-purchase at all. Everywhere else,
  `s4`–`s8` is `Not Verified — not reached`.

### 8.2 Browser-only, against a mobile-first product

The scenario's constraints are *"Mobile-first experience"* and *"Native iOS and Android
applications"*. Capture is **web only**. Native-app-only behaviour — push notifications,
location permissions, offline caches, widgets, wallet passes — is not reachable. Mobile
viewport emulation approximates the responsive web, not the native app.

Consequences: `s5` (Travel day) and `s6` (In destination) are the stages most likely to be
native-only and are therefore the most likely to be under-captured *for reasons of method,
not of market*. Any competitor assumed native-first — Hopper and Citymapper most obviously —
will be systematically under-observed. Every such gap is recorded `native-app-only`, and
**no absence claim may be made about a native-only surface.**

### 8.3 One sample, of systems that experiment continuously

Travel products A/B test, personalise by geography and cookie state, and change pricing UI
frequently. A single capture cannot tell a permanent feature from an experiment bucket. This
caps `Verified` at "observed on this date under these settings" (§5.7). Comparisons across
competitors captured on different days inherit any market change between those days.

### 8.4 The two-viewport, one-market design leaves real gaps

One market (en-GB / UK / GBP) makes fourteen products comparable and makes zero claim about
any other market. Feature availability, legal text, price presentation and inventory all
vary by market. One second-locale spot check is a smoke test, not coverage.

### 8.5 Declining non-essential cookies suppresses what we are trying to see

The standing instruction is followed. Its non-obvious consequence: **personalisation is
systematically under-observed**, because much of it is driven by exactly the tracking being
declined. Category 7 (Personalisation) is therefore the category with the weakest evidence
in this round, and every negative finding in it must say so in place. Optional mitigation,
requiring the researcher's approval: one recorded opt-in comparison pass on a single
competitor, on a disposable profile, with the deviation logged.

### 8.6 Accessibility observations are not a conformance verdict

Capturing an accessibility tree per screen is the largest single upgrade over desk research,
and it must not be overclaimed. A tree snapshot supports observations about names, roles,
labels and landmark structure. It does **not** support a WCAG 2.2 AA conformance claim,
which needs keyboard traversal, focus visibility, contrast measurement, 200% zoom, reflow,
target size and assistive-technology testing. This round records a11y **observations**
only. A conformance verdict is an `a11y-audit`, a different type and a different agent.

### 8.7 The plan's own foundational input is not immutable

The scenario lives at `/Users/raquelpalis/Desktop/Luma test project scenario.pdf` — outside
the repository, unversioned, on a Desktop. Every requirement in this plan traces to it. It
should be copied into `research/sources/` by a human (agents are denied that write) so the
round has a fixed, hashed input. Until then, the scenario could change without trace and
this plan would silently stop matching it.

### 8.8 What could not be verified while writing this plan

Listed in `validation.md` § 4. It includes the fact that this agent holds Read and Write
only and **cannot run `validation/audit-system.py`**, so no before/after audit delta exists
for this artifact.

---

## 9. Step R — prior-round reconciliation. Named, later, and not a merge

### 9.1 Preconditions — all four, in order

1. All fourteen competitors pass §7.1.
2. The blind synthesis is written from the captures alone.
3. It is **frozen**: committed to git, and its **commit SHA recorded** in the reconciliation
   artifact's manifest. A freeze that is asserted rather than hashed is not a freeze, and
   without it there is no way to prove the new findings were not adjusted after the prior
   round was opened.
4. Only then does the quarantine in §0 lift.

### 9.2 What Step R produces

For every load-bearing claim in the prior round, one of four verdicts:

| Verdict | Meaning |
|---|---|
| **Confirmed** | The hands-on round independently observed the same thing |
| **Contradicted** | The hands-on round observed something incompatible |
| **Not addressed** | This round did not reach it. **Stays unresolved** — it is not promoted by association and it is not demoted either |
| **Unfalsifiable as written** | The prior claim is not stated in a form any observation could confirm or refute — typically an absence claim over an unstated scope |

### 9.3 The three rules that keep it a diff and not a merge

1. **No prior claim is imported into the new findings.** The new findings are already frozen
   and are not edited at Step R.
2. **No new claim is softened, strengthened or reworded to agree with a prior one.**
3. **The output is a finding about the prior study's reliability**, expressed as counts and
   named examples per verdict — not a combined "what we know about the market" document. If
   a combined view is wanted later, it is a third artifact built from both, and it says so.

### 9.4 Type and ownership — a proposal for the researcher

Proposed type: **`test-report`** (`_types.json`: *"Results of a specific test with severity
set by a human"*, owner `research-ops`). The prior study is the thing under test; the
hands-on captures are the ground truth; and how serious each contradiction is, is precisely
the human call `test-report` is built around. `ux-benchmark` and `competitive-benchmark`
were both considered and both describe measuring *products*, not measuring a *prior study*.

**Severity is proposed, never set.** `research-ops` proposes a severity per contradiction;
the researcher sets it at Gate A. Every severity in the eventual report is marked as a
suggestion awaiting human confirmation.

---

## 10. Deliverables, and the client's Step 1 gate

`SKILL.md` § Step 1 requires up to five context questions before analysis, and § Anti-patterns
names *"Starting before the five-question gate"* first. The brief answered most of it. What
remains open, for Gate A:

| Open question | Why it matters | Status |
|---|---|---|
| Deliverable format — document, FigJam, presentation, or a pairing | `SKILL.md` § Choosing the format recommends FigJam + document at ideation. Also engages CLAUDE.md § Output surfaces: propose and confirm, never pick silently | **Open** |
| Target markets beyond UK | Determines accessibility obligations and price-guarantee viability | **Open** — one market fixed for comparability (§4.1) |
| Business model | Referral layer vs. inventory changes which findings are actionable | **Open** |
| Authenticated accounts, and which competitors hold real booking history | Determines whether `s4`–`s8` exists at all (§8.1) | **Open — blocking for post-purchase** |
| The airport-services roster gap (§2.5) | Business goal 5 has no comparator | **Open — blocking for stage 5 claims** |
| Screenshots available this time | Yes — that is the whole change from the prior round | Answered |
| Platform | Web capture only, against a mobile-first product (§8.2) | Answered, with a recorded limitation |

Planned artifacts downstream of this plan, each its own registered artifact:

- Per competitor: `site-tree.md`, `session.md`, and the capture set — **sources, not
  artifacts**, living under `research/sources/`.
- One **coverage ledger** across all fourteen — `research-ops`.
- One **`competitive-benchmark`** carrying the full six-field matrix — `research-synthesizer`,
  per `_types.json`. Not `research-ops`.
- One **`test-report`** for Step R — `research-ops` (§9.4).

`SKILL.md` § Step 7's section order and its rule that *"no format may drop the confidence
ratings, the sources, or the verification checklist"* bind every one of them.

---

## 11. Claim format used in this document

Neither evidenced form in CLAUDE.md § Claim format applies cleanly here. `[E-nnn]` is
testimony and the ledger holds **0** records; `[ART-nnn § Section]` resolves to a registered
artifact, and the scenario and the skill are neither. Following the precedent set by ART-010
(`validation.md` § 7), sources are therefore cited **by path and section** — resolvable and
honest, and deliberately not dressed as either evidenced form:

- `Luma test project scenario.pdf` § Business Goals
- `SKILL.md` § Step 4

`Inferred` names what it is inferred from. `Assumption` is collected below.

## 12. Assumptions

| # | Assumption | If it is wrong |
|---|---|---|
| **A-1** | A plan author exposed to the prior round's conclusions (§0) can still write an unbiased plan, because the plan's reasoning is auditable against its cited sources (§2.4) | The plan is rewritten by an unexposed session, using this one as a coverage checklist only |
| **A-2** | None of the seven scenario-named competitors sells a public-transport ticket or provides in-destination transit routing | Tier 3 is redundant; four sessions are freed and the roster shrinks |
| **A-3** | None of the fourteen is an airport-services product | Business goal 5 is covered after all and §2.5 dissolves |
| **A-4** | Loyalty appears inside other stages rather than occupying a stage of its own | The `loyalty_touch` flag returns nothing and the `L` set carries the whole answer |
| **A-5** | Every one-line roster reason in §2.3 | Each is a prediction the site tree will confirm or correct. A correction is recorded as a result and the order is not retrospectively rewritten |
| **A-6** | 40–70 screens per competitor is achievable under §3.5 without exhaustive state crossing | The screen budget is re-derived and every competitor already captured is re-checked against the new one |
| **A-7** | The capture tooling can write page text, a11y tree and screenshot to disk without the payload round-tripping through the model (§6.2) | Per-competitor context roughly doubles; sessions split at stage boundaries and the budget rises above 20 |
| **A-8** | A fresh browser profile per competitor prevents cross-competitor personalisation bleed | Ordering effects contaminate later competitors and the order in §2.3 becomes a confound |

---

**Gate A.** This plan is a proposal. The roster, the execution order, the fixed scenario and
market, the authenticated-account decision, the airport-services roster gap, the deliverable
format, and every severity and priority anywhere downstream are **human calls**. Nothing here
is approved by having been written.
