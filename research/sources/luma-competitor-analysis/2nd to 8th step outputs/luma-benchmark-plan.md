# Luma Competitor Benchmark · Phase 1: Benchmark Plan

**Status:** Plan only. No competitor has been researched. No competitor feature is described in this document.
**Date:** 21 July 2026
**Phase:** 1 of 9
**Next gate:** This plan must be agreed before Phase 2 research begins.

---

## 1. Purpose statement

This analysis will inform one decision: **which stage of the traveller journey Luma builds first, and on what axis it differentiates.** Everything downstream, including scope, business model, and the first release, follows from that call.

### The stated goal, and a sharper version

The stated business objective is to create the world's most intelligent travel companion by reducing travel stress and helping users confidently navigate every stage of their journey.

**This is too vague to make a decision against, for three reasons.**

1. "Most intelligent" is not a testable position. Several better-resourced incumbents already ship conversational planning. Intelligence is becoming table stakes, not a differentiator.
2. "Every stage" is a breadth claim. Breadth is the most expensive possible position to hold from ideation, and it is where incumbents are strongest.
3. "Reducing travel stress" is the actual idea, but it is buried and unmeasured.

**Proposed sharper version:**

> Luma helps a first-time traveller act with confidence at the moments where confidence normally collapses, by making the least stressful option visible and choosable, not just the cheapest one.

This version is falsifiable. It names a user, a moment, and a decision axis. It also tells us what to look for in the benchmark: whether any competitor lets a user sort, filter, or choose on anything other than price and time.

**Interpretation:** the sharper version implies Luma should win a narrow set of high-anxiety moments rather than match incumbent breadth. This is an interpretation of the stated goal, not the stated goal itself. Confidence: **Low**. It should be confirmed or rejected by the user before Phase 2.

### What this analysis will not decide

It will not decide the business model. That has been confirmed as unsettled, so Phase 8 will present recommendations conditionally across referral, OTA, and subscription models rather than assuming one.

---

## 2. Competitor set

Fourteen confirmed, grouped by what we expect to learn. Categories are **direct** (competes for the same job), **adjacent** (owns one stage of the journey deeply), **analogous** (solves a comparable confidence problem in a different domain of travel), and **aspirational** (sets the bar for a pattern Luma wants).

### Confirmed set

| # | Competitor | Category | Why in scope | What we expect to learn |
|---|---|---|---|---|
| 1 | Booking.com | Direct | The broadest multi-vertical player in the set | Whether breadth actually produces a coherent journey, or a set of adjacent silos. Also the mechanics of tenure-based loyalty and who it excludes |
| 2 | Expedia | Direct | Multi-vertical, and ships a conversational assistant | **Top open question of this run.** How much of the assistant has actually shipped, and what it does at each stage |
| 3 | Google Travel | Direct | Default surface for a large share of trip planning | How a non-transactional aggregator handles the plan and compare stage, and where it hands off |
| 4 | Kayak | Direct | Metasearch across flights, stays, and cars | The metasearch comparison pattern, and what happens to the user after handoff to a supplier |
| 5 | Skyscanner | Direct | Flight-led metasearch with strong discovery entry points | Whether the dream and discover stage is served by anyone as a real product surface |
| 6 | Hopper | Adjacent | Narrow scope, strong behavioural onboarding | Onboarding psychology for a low-confidence first action. Applied to price here, but the pattern may transfer to confidence |
| 7 | TripIt | Adjacent | Itinerary management and alerting, sells no inventory | Low-friction itinerary capture, and the prepare and travel day stages when there is no booking incentive |
| 8 | Airbnb | Adjacent | Accommodation, with a named pre-purchase guarantee | Reassurance presented as visible product before booking rather than buried policy. The most transferable pattern identified so far |
| 9 | Tripadvisor | Adjacent | Reviews, activities, and conversational planning | Trust signals at the compare stage, and how social proof is presented to someone with no frame of reference |
| 10 | Rentalcars.com | Adjacent | Car rental as a distinct booking vertical | A vertical with notoriously high anxiety at pickup. Where does the product stop supporting the user |
| 11 | Trainline | Adjacent | Rail and coach ticketing | **Directly tests the weakest prior claim**, that no competitor sells public transport tickets |
| 12 | Omio | Adjacent | Multi-modal ground transport ticketing across Europe | Same test as Trainline, plus how mode comparison is presented when the modes are not equivalent |
| 13 | Citymapper | Analogous | In-destination transit navigation and ticketing | Closest analogue to Luma's in-destination stage. Confidence at street level rather than at booking |
| 14 | Rome2Rio | Analogous | Multi-modal A to B route planning | How the "can I even get there" question is answered before any booking intent exists |

### Competitors I think are weak choices, and why

**Rentalcars.com.** Car rental is a real vertical, but as a benchmark target it is narrow and the flow is largely a commodity funnel. I expect it to produce a thin profile with low transferable insight. **Recommendation:** keep it, but time-box it. If it produces little after one pass, do not force symmetry by padding the profile.

**Google Travel.** Scope is ambiguous. "Google Travel" spans Google Flights, Google Hotels, the Things To Do surface, and general search integration, and these behave differently. **Recommendation:** keep it, but scope it explicitly to Google Flights plus Google Hotels plus Things To Do, and record anything outside that as out of scope rather than guessing at the boundary.

**Airbnb.** In scope for one specific reason, the named pre-purchase guarantee pattern. It is not a Luma competitor in any broader sense. **Recommendation:** research it narrowly against that question rather than running a full eight-stage profile. Doing otherwise burns effort on accommodation supply mechanics that do not inform Luma's decision.

### Unresolved items in the supplied list

- **"Bookum experiences".** I cannot identify this product with confidence. It may be a typo for an activities marketplace such as GetYourGuide or Klook. **Not added to the set.** If activities booking should be represented by a specialist rather than by Tripadvisor alone, name the product and I will add it.
- **"Booking" listed separately from "Booking.com".** Treated as a duplicate. If a different product was meant, name it.
- **"Car Rental" as a generic entry.** Interpreted as Rentalcars.com, which is the Booking Holdings car rental brand. Confirm or substitute.

### Deliberate exclusions

- **Airline and hotel own-brand apps.** They own one supplier, not a journey. Different problem.
- **Traditional travel agents and concierge services.** Human-delivered, not comparable as a product experience.
- **Generative AI chat assistants used for trip planning.** Relevant to positioning, but they are not travel products with journey coverage, so they do not fit the matrix. Worth a note in Phase 8 as a commoditisation risk instead.

---

## 3. Journey stages in scope

Eight stages, using the client's framing. Each is defined so that two researchers scoping independently would draw the same boundary.

| # | Stage | Starts when | Ends when |
|---|---|---|---|
| 1 | Dream and discover | The user has intent to travel but no fixed destination or dates | A destination and rough dates are chosen |
| 2 | Plan and compare | A destination is chosen and the user begins evaluating options | The user has a preferred option in each vertical but has not paid |
| 3 | Book | The user commits to a specific option and enters a checkout flow | Payment is confirmed and a reservation exists |
| 4 | Prepare | A booking exists and the trip is in the future | The user leaves home for the trip |
| 5 | Travel day | The user leaves home | The user arrives at the destination accommodation or first fixed point |
| 6 | In destination | The user is at the destination and moving around it | The user begins the return journey |
| 7 | Return | The user begins travelling home | The user arrives home |
| 8 | After the trip | The user is home | Engagement with the product for this trip ends |

**Verticals assessed within stages 2 and 3, separately in each case:** flights, ground transport at destination, accommodation, activities and experiences.

This produces a 14 by 8 grid, with stages 2 and 3 subdivided four ways. That is why the feature matrix will be delivered as a spreadsheet rather than as a table in a document.

**Depth priority.** Not all stages get equal effort. Based on the first-time traveller lens, effort concentrates on stages 4, 5, and 6, where confidence is lowest and where the prior run suggests coverage is thinnest. Stages 1 and 8 get a lighter pass. This is a resourcing decision, not a claim that the other stages matter less. It is stated here so it is visible rather than accidental.

---

## 4. Comparison dimensions

Recorded per competitor, per stage. All of these are observable on screen or in first-party documentation. Nothing here requires inferring intent, strategy, or performance.

### A. Coverage

| Dimension | What we record |
|---|---|
| Stage present | Does the product do anything at this stage. Yes, partial, no |
| Vertical present | For stages 2 and 3, which of the four verticals are covered |
| Transactional or referral | Does the user complete the action in-product, or get handed to a third party |
| Entry point | How the user reaches this stage in the product. Navigation label, or entry surface |

### B. Decision support

| Dimension | What we record |
|---|---|
| Sort options offered | The literal list of sort controls presented |
| Filter options offered | The literal list of filters presented |
| Default sort | What is selected before the user changes anything |
| Non-price ranking axis | Whether any sort or filter ranks on ease, effort, reliability, or stress rather than cost or time. **This is the load-bearing dimension of the whole study** |
| Explanation of results | Whether the product states, on screen, why a specific item is shown or recommended |

### C. Reassurance and trust

| Dimension | What we record |
|---|---|
| Named guarantee or protection | Whether a protection scheme is named and where it appears in the flow |
| Position relative to purchase | Shown before commitment, or only after |
| Support access | How the user reaches help at this stage, and how many steps it takes |
| Support gating | Whether support quality depends on account tier, tenure, or spend |
| Cancellation and change clarity | Whether terms are visible at the decision point |

### D. Proactive help

| Dimension | What we record |
|---|---|
| Alerts offered | What the product offers to tell the user without being asked |
| Permission asked when | At what point in the flow notification or location permission is requested |
| Disruption handling | What the product presents when a booked item changes or fails |
| Live data shown | Which live data appears on screen at this stage |

### E. Onboarding and first run

| Dimension | What we record |
|---|---|
| First action requested | What the product asks a new user to do first |
| Commitment level of that action | Whether the first action requires account, payment, or nothing |
| Auth wall position | At what point sign-in becomes mandatory |
| Personalisation basis | What input the product uses to personalise, as stated on screen or in docs |

### F. Accessibility and resilience

| Dimension | What we record |
|---|---|
| Published accessibility statement | Present or not, with URL. **Absence of a statement is recorded as absence of a statement, never as absence of practice** |
| Observed WCAG 2.1 AA issues | Only issues directly observed during walkthrough. Contrast, focus visibility, labelling, target size |
| Empty and error states | What the screen shows when there are no results or the action fails |
| Offline and low connectivity | What is stated in first-party docs about offline access |

### Dimensions deliberately excluded

These cannot be observed and will not be recorded: conversion rates, revenue, user numbers, market share, internal roadmap, technology stack, effectiveness of any pattern, and user satisfaction with any feature. Where the study needs any of these, it becomes a research question in Phase 9, not a matrix cell.

---

## 5. Evidence rules

### Access method per competitor

**Confirmed for this run:** hands-on walkthrough via browser tools, plus first-party documentation. Platform coverage is both web and mobile on a best-effort basis. Web is reachable hands-on. Mobile-only behaviour will be covered through app store listings and first-party docs at a lower ceiling, and anything unreachable is recorded as unreachable.

| Competitor | Expected access | Expected walls |
|---|---|---|
| Booking.com, Expedia, Kayak, Skyscanner, Google Travel, Tripadvisor, Airbnb, Rentalcars.com, Trainline, Omio, Rome2Rio | Web, browse and search without account | Checkout beyond the point of payment. Some personalisation features may be account-gated |
| TripIt | Web, likely account-gated early | Sign-up wall. Paid tier features not reachable |
| Hopper | Predominantly mobile | App-only flows not reachable. Expect a low ceiling |
| Citymapper | Web and mobile, mobile-led | Ticketing flows may be app and region specific |

Region gating is expected on several of these. The walkthrough will be conducted from a single stated region and that region will be recorded, because pricing, inventory, and even feature availability vary by market. Anything visible only in another market is recorded as region-gated, not as absent.

### The evidence ladder

| Tier | Source | Ceiling |
|---|---|---|
| 1 | Hands-on walkthrough of the real flow | Verified |
| 2 | First-party documentation, help centre, accessibility statement, newsroom, engineering blog | Verified |
| 3 | Screenshots supplied by the user | Verified for what is visible, nothing beyond |
| 4 | Credible third party, design case study, reputable reporting, app store listing | Likely |
| 5 | Vendor marketing claim about the vendor's own product | Likely, and permanently labelled as a vendor claim |
| 6 | Nothing found | NOT VERIFIED |

**Overall confidence ceiling this run: Verified**, because hands-on access is available. This will not be uniform. Hopper and Citymapper are expected to sit lower because their primary surfaces are app-only.

### Rules that hold for the whole study

1. **Every finding records its tier.** A reader must be able to tell a walked-through screen from a marketing page at a glance.
2. **Absence of evidence is never a finding.** A search returning nothing produces `NOT VERIFIED · searched [where], no result found. This does not establish absence.` It never produces "no competitor does X".
3. **Vendor claims stay labelled as vendor claims permanently.** Reported as "Hopper states that", never as "Hopper's predictions are".
4. **Unknown is a valid answer** and goes into the Gaps section rather than being filled with a plausible guess.
5. **Luma's own column always reads** `Not built (ideation) · decision required.` No invented current behaviour, not even as illustration.
6. **Observation and interpretation stay separated.** Interpretation is labelled and rated Low.

### Walkthrough limits

- No payment. No card details entered. No booking completed.
- No account creation with real personal details. A flow requiring sign-up is recorded as `NOT VERIFIED · auth wall`.
- No scraping or automated bulk collection. Navigate as a user would.
- Geo-gated, app-only, or otherwise unreachable flows are recorded with the reason.

### Four prior claims to re-verify explicitly

These are the weakest and most load-bearing claims from the previous desk-research run. Each is a research question in Phase 2, not a starting assumption.

| Claim to test | Why it is weak |
|---|---|
| No competitor offers airport interior wayfinding | Absence of evidence, and it supports a headline opportunity |
| No competitor consistently explains its recommendations | Same weakness, same importance |
| No competitor sells public transport tickets | True only within the original ten. Trainline, Omio, and Citymapper were never tested. They are now in scope specifically for this |
| Accessibility statements exist only for Booking.com | Absence of a published statement is not absence of practice |

Plus the standing open question: **how much of Expedia's conversational assistant has actually shipped.** Hands-on access is available this run. This is the single highest-value unknown.

---

## 6. Out of scope

Stated so that nobody assumes it was covered and quietly missing.

| Out of scope | Reason |
|---|---|
| Pricing accuracy, fare competitiveness, inventory depth | Not a design question, and not stable enough to benchmark meaningfully |
| Business performance, revenue, market share, user numbers | Not observable, and not what this analysis decides |
| Backend architecture, data partnerships, supplier contracts | Inferable at best. Effort costs and supplier dependencies enter in Phase 7 as honest estimates, clearly labelled |
| Marketing, SEO, brand campaigns, acquisition channels | Different discipline. Use the marketing competitive-brief skills if this is needed |
| Airline, hotel, and rail operator own-brand apps | Single-supplier products, not journey products |
| Loyalty programme economics beyond the eligibility mechanics | We record who qualifies and when, not the commercial model behind it |
| Checkout completion and post-payment flows | Blocked by the no-payment walkthrough limit |
| Legal review of the European Accessibility Act or of price-guarantee mechanisms as financial products | Flagged as risks in Phase 8. Not assessed here. Needs qualified legal input |
| Luma's current product | It does not exist. Ideation stage |
| Any competitor not on the confirmed list of fourteen | Including the unresolved items in section 2 |

---

## 7. Risks

Where this benchmark could mislead us.

| # | Risk | How it misleads | Mitigation in the method |
|---|---|---|---|
| 1 | **Absence of evidence becomes a finding** | The most exciting output of a benchmark is "nobody does this", and it is also the easiest thing to get wrong. An unserved need is precisely the claim you will least want to interrogate | Rule 2 is enforced per claim. Phase 6 separates unserved from poorly served from structurally excluded, and NOT VERIFIED white space is a research question, not an opportunity |
| 2 | **Feature comparison flatters incumbents** | A matrix of features rewards the products with the most features. Luma will always lose that comparison, and the comparison is not the question | Phase 5 compares journeys and seams between stages, not feature counts. The seams are where the real answer sits |
| 3 | **A walkthrough is one session, in one region, by one person who is not the target user** | A researcher navigating Booking.com is not a first-time traveller navigating Booking.com. Fluency hides friction | Findings are recorded as observed behaviour of the interface, never as claims about how a user feels. Emotional claims in Phase 5 are labelled as hypotheses needing user research |
| 4 | **Region and account state change what is on screen** | A/B tests, market-specific inventory, and logged-out versus logged-in states can produce contradictory observations that look like findings | Region and account state recorded per walkthrough. Anything only visible in one state is labelled with that state |
| 5 | **Vendor marketing reads as capability** | Travel products are heavily marketed and roadmap language is often written in the present tense. This is a live problem with at least one product in the set | Tier 5 exists specifically for this and the label is permanent |
| 6 | **Profile quality decays across fourteen competitors** | The last profile written is reliably thinner than the first, and thin profiles are where invented detail enters | Parallel execution in Phase 2, one clean context per competitor, schema validation on every return |
| 7 | **The benchmark answers the wrong question** | Competitor analysis tells us what the market does. It cannot tell us what a first-time traveller needs. If the real question is the second one, this whole study is the wrong instrument | Stated here, at the start. Phase 9 lists what needs user research rather than pretending the benchmark covered it. **This is the most important risk in the table** |
| 8 | **Prior-run findings leak back in at inflated confidence** | Ten opportunities and a headline conclusion already exist from a desk-research run. They are memorable and they will feel established | Prior findings are quarantined as hypotheses. Phase 7 re-derives from this run's Phase 6 or drops them |
| 9 | **Confidence in evidence gets confused with likelihood of success** | A well-evidenced observation about a gap is not the same as a good bet. Conflating them turns a hypothesis into a roadmap item | Phase 7 defines confidence explicitly as evidence strength, scored separately from impact |

---

## 8. Deliverables

| Artefact | Format | When |
|---|---|---|
| Benchmark Plan | This document, plus a Phase 1 frame on the FigJam board | Phase 1, now |
| Verified Competitor Profiles | Working documents, one per competitor | Phase 2 |
| Feature matrix, capability map, journey coverage grid | .xlsx, confidence colour coded | Phase 3 |
| Pattern analysis, journey comparison, white-space map, scored opportunities | FigJam board, one section per journey stage, stickies colour coded by confidence | Phases 4 to 7 |
| Executive report | .docx, with the .xlsx matrix alongside | Phase 9 |

Confidence colour coding is consistent across every artefact: green `D6E9D6` Verified, amber `FCEFCC` Likely, red `F6D8D6` NOT VERIFIED.

The FigJam board is the working surface for the team. The document is the citable record. Neither drops the confidence ratings, the source register, or the manual-verification checklist.

Board: https://www.figma.com/board/ub26bTCPPUibiuDtBTSBn4/

---

## Gaps

What I could not verify or resolve at this stage.

| Gap | Why |
|---|---|
| "Bookum experiences" | Cannot identify this product. Not added to the set. Needs the user to name it |
| "Booking" as an entry separate from "Booking.com" | Treated as a duplicate. Needs confirmation |
| "Car Rental" as a generic entry | Interpreted as Rentalcars.com. Needs confirmation |
| Whether the sharper purpose statement in section 1 is accepted | It is my interpretation of the stated goal, not the stated goal. Needs the user to accept, amend, or reject before Phase 2 |
| Target markets | Not supplied. Determines European Accessibility Act exposure, region for the walkthrough, and which competitors are even available. **Needed before Phase 2 starts** |
| Business model | Confirmed as unsettled. Carried forward, not a blocker, handled conditionally in Phase 8 |
| Which competitors are reachable hands-on, and how deeply | Cannot be known until Phase 2 begins. The access table in section 5 is expectation, not observation |
| Whether any screenshots or recorded flows exist from prior work | Not supplied. Would raise the ceiling on app-only products, particularly Hopper and Citymapper |
| Existing Luma user research | Not supplied. If first-time traveller research exists, it should shape which stages get depth priority in section 3. Without it, the depth priority is my judgement |

---

## Confidence summary

This is a plan. It contains no factual claims about any competitor, which is the intended state at Phase 1.

| Rating | Count | What they are |
|---|---|---|
| Verified | 0 | No competitor research has been conducted |
| Likely | 0 | No competitor research has been conducted |
| NOT VERIFIED | 4 | The four prior-run claims listed in section 5, carried explicitly as research questions rather than as findings |
| Interpretation, rated Low | 2 | The sharper purpose statement in section 1, and the depth priority across journey stages in section 3 |
| Unresolved inputs | 9 | Listed in Gaps above |

**No competitor feature has been described in this document.** That is Phase 2's job and Phase 2 has not started.

---

## What I need from you before Phase 2

1. Accept, amend, or reject the sharper purpose statement in section 1
2. Confirm target markets
3. Resolve the three unclear list entries: "Bookum experiences", the duplicate "Booking", and generic "Car Rental"
4. Confirm the depth priority on stages 4, 5, and 6, or redirect it
5. Send any existing screenshots, recorded flows, or first-time traveller research
