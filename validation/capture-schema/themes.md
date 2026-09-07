# Theme taxonomy — hands-on competitor capture

**Status: PROPOSED. Gate A. Nothing here has been applied.**
Machine-readable form: `validation/capture-schema/themes.json` — that file is the
specification a validator is built against; this one is the same content with the
reasoning in front of it.

Derived from the 121 findings of round 1 (`CAPTURE-INDEX.json`) and the mechanical
audit (`theme-audit.json`), in response to **C-045**. No capture, no finding, no theme
value and no dashboard was modified in producing this.

---

## What I read, and what that limits

I read all 121 claim summaries from `CAPTURE-INDEX.json` and all 121 filed themes from
`theme-audit.json`. **I did not open the 50 capture files.** Four rows carry the claim
string `"see capture file"`; my judgement on those rests on the row id and on C-043's
description of them, and they are marked `low_confidence` in the JSON.

**42 of 121 rows (35%) keep their filed primary theme. 79 (65%) are proposed to move.**
The audit found 48% contradiction among the 29 rows it could speak about, and says of
itself that this is a lower bound — so 65% is compatible with it, but the gap is filled
by my judgement, not by the ledger. Ratify the *definitions* first. The per-row moves
are worked examples of the definitions, not a migration script.

### The audit has four false positives, and a validator must not trust it

`theme-audit.json` compares a finding's theme against its own id by substring match, and
never reads claim prose. It says so. Four of its fourteen `CONTRADICTS` verdicts are
matching artifacts:

| Row | Audit says | Actually |
|---|---|---|
| `F83_DURATION_IS_VISIBLE_BUT_NOT_STRUCTURED` | names `market-structure` | matched `STRUCTURED`. It is about a duration field not being structured for comparison. Its filed theme is **correct**. |
| `correction_to_own_earlier_claim` | names `method` | matched `correction`. Per C-043 it corrects a mis-framing of Expedia One Key — a competitor claim. Filed theme **correct**. |
| `CORRECTION_to_F28` | names `method` | matched `correction`. Corrects the scope of Google Track-prices — a competitor claim. |
| `MATERIAL_CORRECTION_to_F09_F20_F25` | names `method` | matched `correction`. Its claim text is about 20 enumerated ranking axes. Filed theme **correct**. |

Two conclusions follow. First, an id that contains `CORRECTION` is not a method record —
the test is *what does it correct*. Second, the audit's `agrees` verdicts are worth no
more than its `CONTRADICTS` ones: `F74_PRICE_CONTEXT_AT_COMMITMENT` is marked `agrees`
because its id contains `PRICE`, and I propose moving it.

---

## Ruling 1 — the field is MULTI-VALUED, ordered, primary first

```
"themes": ["disruption-and-protection", "loyalty-and-retention"]
```

1 to 3 items. `themes[0]` is the primary and **is the only value a chart may count.**
Secondaries exist for retrieval and coverage questions, never for counting. Round 1's
single string is equivalent to a one-element array and a validator must normalise it.

**Why.** Round 1 assumed single-valued and never said so, which turned every genuinely
two-subject finding into a coin flip nobody could audit. F-107 — *"No disruption, delay,
cancellation, compensation or passenger-rights destination appears in Qatar Airways' 289
homepage links"* — was captured during a loyalty sweep and is about disruption.
Single-valuedness made that either/or and the round chose the sweep, which is how the
matrix came to draw Qatar as empty under Disruption. As two values the record is simply
true.

**Why ordered.** An unordered set makes every count ambiguous: one finding would inflate
two bars and the totals would exceed the denominator. Ordering costs one decision per
finding and keeps every chart's denominator equal to the row count.

### Tie-break: the subject test, then precedence

**Subject test.** The primary is the theme of the mechanism, document or surface that was
**observed** — not of the consequence inferred from it.

- F-01 observed a gate (*"gated behind 15 completed bookings in 2 years"*) and inferred an
  effect on first-timers → `loyalty-and-retention`, secondary `user-types`.
- F-02 observed an absence of address (*"never addresses a first-time traveller anywhere on
  its own explainer page"*) → `user-types`, secondary `loyalty-and-retention`.

**Precedence.** When two themes both describe the observed artefact, the earlier one wins:

```
accessibility-and-inclusion → disruption-and-protection → dark-patterns-and-trust →
ai-assistants → trip-as-an-object → loyalty-and-retention → user-types →
market-structure → price-honesty → ranking-and-comparison → decision-support → other
```

Ordered most specific to most absorbent. The two themes that swallowed round 1 —
`price-honesty` (29 rows) and `ranking-and-comparison` (36) — sit near the bottom
deliberately, so they receive a finding only when nothing narrower fits.

**The side effect, stated rather than hidden.** A late theme is starved by construction.
Under this order `price-honesty` holds **6** rows, not 29. I believe that is the correct
semantics of the name — *is the price shown the price paid* — but it means the round has
materially less price-honesty evidence than its label implied, and any board conclusion
leaning on "price honesty" needs re-reading against 6 findings. That is open question Q3,
and I am the wrong person to settle it, having written the order.

---

## Ruling 2 — `method` is a DIFFERENT AXIS and must leave the vocabulary

`method` is not a theme. A theme answers *what is this finding about in the market*;
`method` answers *is this a finding at all*. Sharing one field caused 5 of round 1's 14
recorded contradictions, because a method row still had to pick a competitor theme and
every available choice was wrong — and it silently inflated whichever theme it landed in.
Two method rows are counted as `ranking-and-comparison` evidence on the current board.

**Proposal: a separate required field.**

```
"record_kind": "finding" | "method-note" | "capture-limit"
```

`themes` is required when `record_kind == "finding"` and **must be absent otherwise**.

Applying the *what does it correct* test, exactly **four** round-1 rows are not findings:

- `method_correction` — Kayak's empty text sweep was not absence → method-note
- `METHOD_CORRECTION_TO_MY_OWN_FINDABILITY_TEST` — English sweep terms against a Spanish
  page → method-note
- `PROHIBITION_2_NEAR_MISS_RECORDED` — two extraction sweeps returned traveller review
  text → method-note
- `CAPTURE_BLOCKED_BY_CONSENT` — *"A search for Madrid to Barcelona could not be
  completed"* → capture-limit

Three rows round 1 filed under `method` are findings and move out: `F16_vs_booking`
(six verticals to four → `market-structure`; being comparative is not being
methodological) and `F41_LOCATION_ASSERTION` (→ `ai-assistants`).

The slug `method` stays in the vocabulary so round-1 rows remain readable, and is
**deprecated**: a validator errors on it for any row generated after approval.

---

## Ruling 3 — `other` is BOTH, and the second half is the operative one

It gets a definition, so a validator can accept it. And its round-1 population is an
**admission the vocabulary was short**, not a residual tail.

The 12 rows are not a scatter. They are three clusters and four strays:

| Cluster | Rows | Where they belong |
|---|---|---|
| Accessibility | F-05, F-06, F-07 | **new theme** `accessibility-and-inclusion` |
| AI assistants | F-38, F-55, F-96 | **new theme** `ai-assistants` |
| Market composition | F-17, F-19 | `market-structure` |
| Strays | F-12, F-13 | `dark-patterns-and-trust` |
| | F-80 | `decision-support` |
| | F-95 | `ranking-and-comparison` |

The AI cluster is the strongest evidence in this file that a theme was missing: two of
the ids are literally `F55_FOURTH_AI_ASSISTANT` and `F96_FIFTH_AI_ASSISTANT`. **The round
was running a census against a category it had no label for.**

After reassignment `other` holds **one** row — F-21, the shape of Expedia's checkout,
proposed inbound from `disruption-and-protection`, where it does not belong either. One
quarantined row with a note is `other` working; twelve is `other` failing.

**Two enforcement requirements.** A row in `other` must carry a `theme_note` of at least
40 characters. And `other` above **5%** of a round is an error, above **3%** a warning.
Round 1 sat at 9.9%. The quota is the detector for exactly this defect — it fires when a
theme is missing, before anyone builds a chart on the gap.

---

## The eleven, one line each

| Theme | Definition | R1 → proposed |
|---|---|---|
| **market-structure** | What a product IS in the market: whether it sells, refers or only compares; whose inventory and how much; who owns it; and where contractual responsibility sits when it is not the traveller's. | 1 → 17 |
| **ranking-and-comparison** | How a product orders a set of bookable options and what a traveller can do to that order — sort axes, filters, per-result attributes, and any published explanation of the ordering. | 36 → 25 |
| **price-honesty** | Whether the price shown is the price paid: what the figure includes and excludes, the convention it uses, fees revealed later, and commitments or disclaimers about that composition. | 29 → 6 |
| **loyalty-and-retention** | The mechanics of membership: tiers, gates, currencies, benefits, what an account unlocks that a signed-out traveller does not get, and what it costs to reach. | 16 → 11 |
| **disruption-and-protection** | What happens when the trip goes wrong and who is answerable: delay, cancellation, compensation, passenger rights, protection and flexibility products — and whether any of it is findable at the point it matters. | 8 → 16 |
| **decision-support** | Information that reduces uncertainty, on surfaces that are not an ordered list of bookable options: price normality and buy timing, trackers, destination-less search, discovery, and context carried or dropped. | 8 → 9 |
| **trip-as-an-object** | Whether the product holds the whole journey as one persistent thing — across verticals, bookings, suppliers and time — or only as separate transactions. | 3 → 4 |
| **user-types** | How a product treats an identifiable class of traveller — first-timer, undecided, unregistered, cash-constrained, cross-border — by addressing, serving, excluding, or never mentioning them. | 3 → 8 |
| **dark-patterns-and-trust** | Interface behaviour that steers, deceives, defaults or obstructs — pre-checked options, confirmshaming, inert controls, unrequested prompts, consent gates — and the inverse, where a product words a choice neutrally. | 2 → 8 |
| **method** | *Deprecated as a theme.* Records about how the round was run. Not a subject a competitor can have. Moves to `record_kind`. | 3 → 0 |
| **other** | The finding is about a competitor and no theme describes it. A quarantine slot for a single row, with a mandatory note and a 5% quota — not a category. | 12 → 1 |

Plus two proposed: **ai-assistants** (0 → 6) and **accessibility-and-inclusion** (0 → 3).

---

## The boundary rules that do the work

Only the tests that separate genuinely confusable pairs are listed here; the full set is
in the JSON, per theme.

**disruption-and-protection vs loyalty-and-retention** — the known confusion, and the one
that produced C-045. *Being found during a loyalty sweep does not make a finding a loyalty
finding.* Test: does the claim mention delay, cancellation, disruption, compensation,
passenger rights, refund or a protection product? Then disruption is at least the primary
candidate, whatever surface it was found on. F-56, F-107 and F-113 mention no tier, no
currency and no benefit between them.

**price-honesty vs ranking-and-comparison** — the removal test. Delete the price: if the
finding survives, it is ranking. Delete the ordering: if it survives, it is price-honesty.
F-09 survives with no price; F-70 (*"total price for the stay and never a nightly rate"*)
survives with no ordering.

**price-honesty vs decision-support** — could the claim be checked by comparing the
displayed price against the final charged total? Then price-honesty. Does checking it
require *other* prices, in time or across the market? Then decision-support. This is why
F-27, F-33 and F-74 leave price-honesty despite being entirely about price.

**price-honesty vs loyalty-and-retention** — is the money the price of a **trip** or the
price of a **programme benefit**? *"USD 25 per Qpoint"* is the price of status. This moves
the whole Qatar cluster (F-105, F-108, F-109, F-108_SETTLED, F-111).

**market-structure vs disruption-and-protection** — the pair I came closest to declaring
unseparable. Test: is there a traveller-facing mechanism — a page, a route, a product, a
notification? Then disruption. Is it only an allocation of responsibility with no mechanism
offered? Then market-structure. F-03 disclaims and offers no route; F-04 operates a
mechanism conditionally. Without this test the two are indistinguishable on every liability
finding in the round and merging would have been the honest answer.

**price-honesty vs dark-patterns-and-trust** — number or control. A misleading *figure* is
price-honesty; a misleading *control, default, wording or modal* is dark-patterns.

**loyalty-and-retention vs user-types** — mechanism or address. See the subject test above.

**"the ranking does not show X"** — always filed under **X**, never under ranking. F-49
(*"the protection a traveller ends up with varies enormously — and nothing in the ranking,
sorting or price display reflects that"*) is about protection; the ranking is where the gap
was noticed, not what it is about.

**decision-support is not a residual bucket.** Almost anything can be called informational.
If the finding names no surface a traveller could use to decide, it is `other`.

---

## Merges considered and rejected

| Pair | Verdict | The test that saved it |
|---|---|---|
| market-structure / disruption-and-protection | separable | traveller-facing mechanism, or only an allocation of responsibility |
| price-honesty / dark-patterns-and-trust | separable | number, or control |
| decision-support / ranking-and-comparison | separable | presence of an ordered list of bookable options — and F-26 is the round's own evidence it treated these as two layers |

## A theme I considered and did not propose

**funnel-and-checkout-shape.** Only one finding survives precedence with this as its only
home: F-21. The other candidates each have a stronger one — F-13 is an inert control
(dark-patterns), F-14 and F-73 are the treatment of a class of traveller (user-types),
F-50 is journey continuity (trip-as-an-object). *A theme with one anchor is not decidable:
nobody can tell from one example where its edges are.* If round 2 produces three or more
findings whose only subject is funnel shape, propose it then, from those three.

---

## What is owed at Gate A

Six open questions, in full in the JSON. The three that matter most:

**Q1 — the four "first-timer" sweep findings (F-02, F-18, F-60, F-110).** `user-types` or
`loyalty-and-retention`? This is the biggest judgement in the file. It is the round's most
repeated pattern (*"four loyalty programmes, four full-text searches, zero mentions of a
first-time traveller"*) and it decides whether the round's central negative result is filed
under the surface it was found on or the subject it measured. I recommend `user-types`
primary on the subject test; the alternative preserves the round's own reading and keeps
the loyalty sweep legible as one block. Multi-valuedness means nothing is lost either way.

**Q3 — price-honesty at 6.** Correct measurement, or starvation artifact of a precedence
order I wrote myself? This repository's own record (C-021, C-024) is that an author
checking their own check is the weakest link. Someone who has not read the precedence order
should re-derive the price-honesty population from the definition alone and compare.

**Q6 — what happens to round 1's existing values.** C-045 was closed by demoting what the
charts may claim, *not* by re-labelling, because hand re-theming 121 findings is the
inference that record exists to prevent. This file does not change that. Approve the
definitions and the field shape first; then re-theme round 1 as a fresh pass, by an agent
that has not read my per-row list, and treat agreement with my list as corroboration rather
than as the method.
