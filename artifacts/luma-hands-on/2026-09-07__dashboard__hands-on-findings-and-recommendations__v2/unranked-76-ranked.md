# The 76 unranked blanks, ranked

**Gate A — every tier below is a proposal.** Severity and priority are the researcher's
call. Nothing here changes the board or round-2 scope until a person accepts it. No web
research was used; every judgement comes from files on disk.

**What this is.** Round 1 recorded 222 blanks about itself. A mechanical pass tiered 146
by category and left 76 UNRANKED — labelled tier 6 — because they name product surfaces
rather than journey stages. This ranks those 76 by which decision each one unblocks,
using the same five tiers as `round2-capture-ranked.json` so the two lists merge.

**Tiers, unchanged:**

| Tier | Meaning |
|---|---|
| 1 | Would corroborate a conclusion still alone after Phase 1 — rec-1, pain-2, pain-3, pain-10 |
| 2 | Falls in a category with zero observations anywhere: error, no-results, offline states |
| 3 | Would confirm or kill a class-B proposal |
| 4 | Deepens a conclusion the board already rests weight on |
| 5 | Real, and not currently load-bearing |

**The standard applied.** Tiers 1, 3 and 4 name the conclusion or proposal served. A row
with no named beneficiary is a 5, by rule. Tier 1 required the blank to BE the unrun
corroboration test — Phase 1 graded mechanism-only evidence (F28 price alerts, F36
tracker) as "partially, not corroboration", and that boundary is held here rather than
loosened to produce a longer tier 1.

---

## Tier 1 — five rows, seven source blanks

Each names the conclusion it serves. Four of the five are the round writing down its own
corroboration test and not running it.

### R09 · American Airlines · **rec-1**
> "whether AA offers proactive disruption notification of the kind Trainline does (F-90)"

- **Serves:** rec-1 — *Notify a traveller the moment they qualify for a right they already hold.*
- **Effort:** authenticated · **Source:** `captures/16-american-airlines/01-disruption-a-choice-not-a-statute.json`
- **Why:** rec-1 rests on F-90 alone, in rail, and this is its air equivalent, named as unrun in the capture itself.
- **Do it right:** Phase 1 names the cheapest form — aa.com manage-booking notification settings. A published plan is not a push; publication is the thing rec-1 argues is insufficient.

### R56 · Trainline · **rec-1**
> "what the delay-compensation notification does when triggered (F-90)"

- **Serves:** rec-1 — the load-bearing capture's own unrun half.
- **Effort:** authenticated · **Merged from 2 blanks** · **Sources:** `captures/10-trainline/01-fulfilment-compensation-and-a-popunder.json`, `captures/10-trainline/02-ranking-names-effort.json`
- **Why:** rec-1's single citation is an *offer* to notify. Nobody has seen what the notification contains.
- **Limit to record:** the trigger cannot be manufactured — a real delay is required. What is reachable is the opt-in screen and the published terms. Do not present a settings screen as the notification.

### R19 · Expedia (control missing for the Google Travel matched pair) · **pain-3**
> "logged-out comparison of the same query on this competitor"

- **Serves:** pain-3 — *Being signed out doesn't stop a sign-in prompt from interrupting your search.*
- **Effort:** flow walk · **Merged from 2 blanks** · **Sources:** `captures/02-expedia/03-stays-search-results.json`, `captures/03-google-travel/04-auth-gated-capability.json`
- **Why:** Phase 1's named cheapest next capture for pain-3, already recorded as OWED. The round holds only two matched-pair signed-out diffs in total.
- **Two payoffs in one capture:** it is also the missing third leg of F-29, which rec-8 rests on. Must run on the extension-clean inspector instance or it is not a control (ART-024 §4.1b).

### R46 · Rentalcars.com · **pain-10**
> "insurance, excess, deposit and fuel policy presentation"

- **Serves:** pain-10 — *Saying no to an add-on is written back to you as a confession.*
- **Effort:** flow walk · **Source:** `captures/09-rentalcars/01-ownership-and-hidden-costs.json`
- **Why:** pain-10 is one instance, one funnel, one competitor. Car hire is where the protection decline is most standard, and this is the decline wording on a fourth product.
- **Narrow it:** the blank says "presentation"; the pain-10 test is the accept AND decline strings, verbatim. The same walk also settles F-86, whose capture calls the funnel walk "the test that is owed".

### R32 · Kayak · **rec-1** (weakest of the five, flagged)
> "Flight Tracker opened"

- **Serves:** rec-1 — and B7 (Luma starts behind on its own Core Features list).
- **Effort:** single page · **Source:** `captures/04-kayak/01-site-tree-and-decision-layer.json`
- **Why:** Phase 1 grades F36 "partially" for one stated reason — *"the capture explicitly did not establish what it does on disruption, which is precisely the claim rec-1 rests on."*
- **Honest caveat:** it may resolve only to the mechanism half. A tracker reporting a delay notifies that something went wrong, not that an entitlement triggered — the distinction rec-1 turns on. If it resolves that way it is a tier 3 for B7. **A researcher could reasonably set this to 3 now.**

### Not found: anything that tests pain-2

No blank among the 76 tests **pain-2** (*a button that looks live can silently do nothing*).
The funnel blanks that would test it sit in the mechanical pass's tier 1, not in this set.
Stated rather than forced — inventing a pain-2 row here would have been the confident
guess this task warns against.

---

## Tier 2 — one row, one source blank

### R23 · Google Travel · the degraded-data state class
> "whether these surfaces exist for destinations with thinner data"

- **Serves:** the state class with zero observations round-wide; secondarily **B4** (telling a traveller whether the price is normal).
- **Effort:** single page · **Source:** `captures/03-google-travel/03-decision-surfaces-opened.json`
- **Why:** the round captured 8 of 119 states (6%) and not one degraded, empty or failed state of a decision surface. This is the only blank in the 76 that names one.
- **Reading stated so it can be overruled:** a thin-data destination is a *sparse-data* state, not literally an error, no-results or offline state. Read tier 2 strictly and this drops to tier 3 under B4 — where it still matters, because B4 calls price-normality "the round's cheapest observed answer" and a surface that only exists for Lisbon-scale cities is a much smaller answer. Either reading keeps it above tier 4.

---

## Counts

| Tier | Rows | Source blanks |
|---|---|---|
| 1 | 5 | 7 |
| 2 | 1 | 1 |
| 3 | 18 | 20 |
| 4 | 19 | 26 |
| 5 | 17 | 22 |
| **Total** | **60** | **76** |

60 rows carry 76 source blanks — 16 blanks were merged as duplicates in different words.
The heaviest merge is Airbnb's **Filtros panel**, which the round wrote down four times
across four captures (R03).

**By effort:** single page 35 · flow walk 19 · authenticated 3 · blocked 3.

**Blocked (needs a decision, not effort):**
- R42 Omio pre-checked toggle — CAPTURE_BLOCKED_BY_CONSENT, no compliant path recorded.
- R26 Hopper app-gated — outside the round's two-browser method.
- R11 Booking.com priority support — opening a support interaction as a non-customer is a research-ethics call.

**Ten source blanks across six rows are already closed** by a later capture in the same
round and are ranked 5 as stale entries, not gaps: R04, R05, R21, R33, R47, R59. Two more
rows are *partially* closed — R06 (Airbnb Experiencias closed, Servicios open) and R22
(Google flights closed, vacation rentals open) — and are ranked on the open half only.

**Where tier 3 concentrates (18 rows):** B5 (undecided traveller) 4 · B6 (transport half
solved) 3 · B1 (protection spectrum) 2 · B7 (behind on core features) 2 · B2, B4, B8, B9,
B11, B12, B14 one each. **Kayak alone carries 7 of the 18** — R34 through R40.

**Where tier 4 concentrates (19 rows):** pain-5 / insight-3 (disruption findability) 5 ·
rec-8 / pain-6 (loyalty) 5 · rec-6 / insight-5 (ranking) 3 · insight-2 / rec-9
(protection) 3 · the remaining 3 are pain-7/rec-7 (R06), insight-1 (R49) and
rec-7/insight-1 (R58).

**The tier 4 worth running first:** R03 (Filtros), R28 (Iberia EU 261 by search) and R07
(AA section bodies) can all *weaken* a load-bearing finding rather than deepen it. A clean
board is when to look hardest.

---

## What I could not judge

Six calls where the record does not settle the answer. Each is ranked, and each ranking is
the one I would defend — but the uncertainty is the point, not the ranking.

1. **R36 · Kayak "'Calculadora de precios' opened" — ranked 3 (B4).**
   The capture records the control's label and nothing about what it computes. I judged it
   from position: it sits in a price-construction capture beside price-tracking copy. If it
   is a baggage/fee calculator it belongs under B3, not B4.

2. **R21 · Google Travel "the four decision surfaces" — ranked 5 (superseded).**
   Capture 03 opened three and its own not_observed still reads *"'Track prices' surface —
   not opened this pass"*. I treated capture 04 (F28, persistent price monitoring) as the
   same surface. Split them and one quarter of this blank is open, at tier 4 under rec-8.

3. **R51 vs R14 · "step-by-step route detail" on Rome2Rio (5) and Citymapper (4).**
   Two identically-worded blanks, split on rec-6's wording alone — rec-6 names *on-site
   transport*, which is Citymapper, not Rome2Rio. Phase 1 records that rec-6's scope is
   contradicted within the round. If Gate A re-scopes rec-6, re-rank both together.

4. **R01 · Airbnb "AirCover for Hosts" — ranked 5.**
   Whether supply-side protection is in scope for Luma at all is not stated anywhere in the
   record. Ranked on the traveller-side reading of pain-4, rec-4 and insight-2. A reviewer
   building a two-sided marketplace would rank it higher and would not be wrong.

5. **R13 / R20 · "map view" on Booking.com and Expedia — both ranked 5.**
   Whether a map is a ranking or comparison surface for insight-4 and rec-2 is a scope
   decision. The round never opened one, so the record cannot say. They rise or fall together.

6. **R43 · Qatar "Transit Tours mechanics" — ranked 3 (B8).**
   Whether this is the airport product B8 turns on or a marketing page is unknown. Ranked 3
   because B8's own recorded unknown — "whether any of it is purchasable by an economy
   passenger" — is exactly what this surface would answer.

**One more, flagged separately because it is a rule outcome rather than an uncertainty:**
**R41 · Kayak "whether the roster's other entries disclose parentage" — ranked 5** and the
row most likely to be justly promoted by a human. Every claim of the form "N of 17
competitors do X" assumes independence, and F88 already shows 3 of 17 share a parent. It is
cheap and it changes how every count is read. It sits at 5 only because it repairs the
round's method rather than a named decision, and the named-beneficiary rule is what keeps
these tiers from being opinion.

---

## Carried forward from Phase 1, unchanged

`research/evidence-ledger.json` holds zero records. No amount of competitor capture makes
any of these pain points a traveller's report of being harmed. Every tier 1 here makes an
*observation* sturdier. Only Phase 1 fieldwork makes it a user problem.
