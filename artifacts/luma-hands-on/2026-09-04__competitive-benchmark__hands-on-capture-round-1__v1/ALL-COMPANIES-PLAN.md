# The 17 competitors — one plan
Generated 2026-09-04 from actual capture state, not asserted. Executes ART-024.
**3 of 17 started · 35 findings · 18 capture files.**

## The roster, and why each is on it

| # | Competitor | Tier | Why it is in scope | Status |
|---|---|---|---|---|
| 1 | **Booking.com** | 1 | named by the scenario · broadest capability · pilot | 7 captures |
| 2 | **Expedia** | 1 | named by the scenario · 6 verticals · Romie open question | 4 captures |
| 3 | **Google Travel** | 1 | named by the scenario · the only decision-layer product | 7 captures |
| 4 | **Kayak** | 1 | named by the scenario · meta-search, compare-then-leave | not started |
| 5 | **Skyscanner** | 1 | named by the scenario · second meta-search, pairs with Kayak | not started |
| 6 | **Hopper** | 1 | named by the scenario · price prediction · app-first, hardest browser test | not started |
| 7 | **Airbnb** | 2 | client's standing set · stays + activities under one account · AirCover | not started |
| 8 | **Tripadvisor** | 2 | client's standing set · leads with discovery, not a search box | not started |
| 9 | **Rentalcars.com** | 2 | client's standing set · single-vertical on-site transport | not started |
| 10 | **Trainline** | 3 | capability gap · first product that FULFILS an on-site transport ticket | not started |
| 11 | **Omio** | 3 | capability gap · multi-modal rail/coach/air | not started |
| 12 | **Rome2Rio** | 3 | capability gap · routes and compares without fulfilling | not started |
| 13 | **Citymapper** | 3 | capability gap · lives in stages 6-7, in-destination movement | not started |
| 14 | **TripIt** | 1 | named by the scenario · operates on OTHER products' confirmations · most account-dependent, so last | not started |
| 15 | **Iberia** | 4 | airline direct · European carrier on the fixed route · airline pilot | not started |
| 16 | **American Airlines** | 4 | airline direct · largest programme · different regulatory regime | not started |
| 17 | **Qatar Airways** | 4 | airline direct · only route to a business-goal-5 comparator (lounges, Fast Track) | not started |

**Tier 1** = named in `scenario.pdf`. **Tier 2** = client's own standing set in `SKILL.md`.
**Tier 3** = added because the scenario's *capability* list demands on-site transport that no
tier-1 or tier-2 product provides. **Tier 4** = added by the client (D-003) because all fourteen
prior entries are intermediaries; without a supplier in the sample, "the market disclaims the
failure moment" describes the sample rather than the market.

## What one competitor's complete pass means

**Eight journey stages**, per the scenario: Dream & discover · Plan & compare · Book · Prepare ·
Travel day · In destination · Return · After the trip.
**Stages 2 and 3 each cover four booking types**: flights · on-site transport · on-site
accommodation · on-site activities.
**Plus** a loyalty set (`L`) and a `loyalty_touch` flag wherever loyalty appears inside another
stage — loyalty is not a ninth stage.
**Plus** terms & conditions.
**Seven states** per surface: default · empty · loading · error · no-results · offline ·
signed-out vs signed-in.
**Both browser surfaces** — inspector instance for anything screenshot-derived, the client's
authenticated Chrome for anything session-gated (CLAUDE.md, ART-024 §4.1b).
**Six fields per observation**: Feature · Competitor · **Our Product** · Evidence · Confidence ·
Source. Confidence is `Verified` / `Likely` / `Not Verified`.

## Where the three started competitors actually stand

| | stays | flights | cars | activities | packages | loyalty | T&C | states |
|---|---|---|---|---|---|---|---|---|
| Booking.com | to card gate | — | — | — | n/a | done | done | none |
| Expedia | to card gate | — | — | — | — | done | — | none |
| Google Travel | tree + sort | deep | n/a | n/a | n/a | n/a | — | none |

**Owed on all three**: the non-stays verticals, every state (empty, error, no-results, offline),
post-purchase and trip management, and Expedia's logged-out control capture.
**No competitor is finished.** Breadth-first on one vertical was a deliberate method choice
(ROUND-LEARNINGS.md) — it makes differences product differences — and its cost is that second
passes are owed, not optional.

## Standing constraints, every competitor

No account created. No credential entered. No card, billing or personal data entered — payment
screens recorded as page structure only. No transaction attempted. Consent banners: decline
non-essential. The operator stops at any wall, names the exact surface, and the client
authenticates (ART-024 §4.1c). Locale is recorded per capture, never forced (D-004).

## Session estimate
~198k tokens per competitor at 40-70 screens. **19-23 sessions** for 17 competitors including
re-passes. Booking.com carries the protocol debugging as pilot.
