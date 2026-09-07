# Phase 1 — corroboration sweep

**2026-09-07 · research-synthesizer · Gate A, suggest-only.** Nothing here is applied to the
board. Every verdict below needs a human before it counts.

Nine conclusions on the v2 board cite exactly one finding. This is what an honest search of the
round found for each. Machine-readable detail, with per-candidate independence and confidence
judgements, is in `phase1-corroboration.json`.

## Verdicts

| | Conclusion | Verdict |
|---|---|---|
| rec-6 | Compute an ease/effort ranking axis | **now_corroborated** — and its scope is contradicted |
| pain-7 | The trip disappears when you switch booking type | **now_corroborated** |
| rec-2 | Show what each ranking choice costs, on the control | partially |
| rec-3 | Compare accommodation by one total price | partially |
| pain-8 | Three products, three guesses at where you are | partially — and one leg is misattributed |
| rec-1 | Notify a traveller when they qualify for a right | **still alone** |
| pain-2 | A button that looks live can silently do nothing | **still alone** |
| pain-3 | A sign-in prompt interrupts a signed-out search | **still alone** |
| pain-10 | A decline written back to you as a confession | **still alone** |

2 corroborated · 3 partial · 4 still alone.

## What I found

**pain-7 is genuinely corroborated.** F91 (Trainline) records a pre-checked cross-sell opening a
hotel search dated `checkin=2026-09-04, checkout=2026-09-05` — "today and tomorrow. The journey
searched was for a different date entirely." Different competitor, different capture, different
vertical pair, and it survives the test: if the Airbnb capture were withdrawn, this would still
evidence that a trip's dates do not cross a booking-type boundary. It crosses a *company*
boundary where F78 stays inside one account, so it corroborates at a structurally weaker
position — and F50 shows Kayak *does* carry a full itinerary across a handoff, so the technical
carry is possible and Airbnb chose not to do it inside its own account.

**rec-6's premise is corroborated and its scope is wrong.** F43 (Kayak) settles the one thing the
cited capture flagged about itself — "The flights picture rests on one product" — on a second
product. F69 (Airbnb, zero sort axes) extends the accommodation sample from three products to
four. F83 and the Airbnb `note_on_duration` block corroborate the activities exclusion on two
competitors. But F99/F100 (Citymapper, captured 16:06Z) contradict the capture rec-6 inherits its
scope from (12:40Z): on-site transport is the *richest* effort surface in the round — frequency,
calories, duration, cross-mode alternatives — and F100 restates the gap as "accommodation and
on-site **activities**". Two captures in one round disagree about which vertical the gap is in.
rec-6 should go to Gate A as a re-scope, not as a strengthening.

**pain-8's phenomenon holds; its headline does not.** F41 records "Estás en Toronto Todos los
aeropuertos" on `kayak.es/ai` — **Kayak's** AI planner. The cited F61 attributes that identical
string to the "Google Travel AI planner" while citing (F-41), and pain-8's body repeats it. No
Google capture in the round records a location assertion at all, and the Google captures were
taken on the inspector instance while Kayak and Skyscanner were on the client's authenticated
Chrome — two surfaces that disagree by construction (ART-024 §4.1b). On the evidence this is one
product disagreeing with itself on two of its own surfaces seven minutes apart, plus a second
product asserting a third city. Arguably sharper than what is on the board, and it does not need
the attribution the evidence cannot support.

**rec-2 and rec-3 are partial in the same way:** the *principle* is corroborated on independent
products, the *specific claim* is not. Rome2Rio and Citymapper both show an option's full cost on
the option — but in results lists, not on a ranking control, which is what rec-2 is about. Google
Flights, Iberia and Expedia's own price construction corroborate "one final figure at
comparison" — but in flights, and the second sentence of F70 only. Airbnb remains the only
product doing total-only in accommodation, and F79 shows it abandons the convention in its own
second vertical.

## What I did not find

Four conclusions survived the search and are still alone. Each is now a research question.

- **rec-1 — proactive entitlement notification.** Nothing in the round corroborates it. Google's
  price tracking (F28) and Kayak's Flight Tracker (F36) prove products already watch on the
  traveller's behalf, but the object is a price or a flight status, never a right. Iberia (F56),
  American Airlines (F104) and Qatar (F107) corroborate only the *absence*, which is a different
  claim. Decisive: the AA capture's own `not_observed` reads "whether AA offers proactive
  disruption notification of the kind Trainline does (F-90)". The round recorded the test as unrun.
- **pain-2 — the inert enabled control.** No second instance. Omio's consent modal is a *visible*
  obstruction and is pain-9's evidence. The round only walked two funnels to a payment gate, so a
  sample of two produced one defect — a design limit, not evidence of rarity.
- **pain-3 — the third-party sign-in prompt.** No second instance. Kayak's and Omio's are consent
  gates, not authentication. Only two matched-pair signed-out diffs exist in the whole round, and
  Expedia's is already recorded as OWED.
- **pain-10 — the shamed decline.** Observed once. F72 (Airbnb's neutral decline) is the
  counter-example and is logically incapable of corroborating it; F91's pre-checked opt-out never
  asks the traveller, so there is no decline to phrase. Worth flagging: rec-5 calls itself "the
  strongest-evidenced recommendation in this set" on the F22/F72 pairing — the pairing is strong,
  the prevalence is a sample of one.

## Reconciliation against the anchors

Four of five anchors reproduce exactly: **26** conclusions, **41** distinct findings cited,
**113** findings, **72** uncited. The 121 − 113 gap in `CAPTURE-INDEX.json` resolves cleanly to
seven non-finding entries plus the superseded `F108_LOUNGE_ACCESS_IS_INDIRECTLY_PURCHASABLE`.

Disagreements, reported rather than adopted:

1. **"single_capture: 9" is the wrong label.** Nine conclusions cite one *finding*; rec-3 and
   rec-6 each list two *capture files*. rec-6 draws its entire scope from the second one.
2. **pain-9 cites zero findings** (`cites: []`, `n: 0`) and is not on the fragile list. It is more
   fragile than the nine. It is also, incidentally, corroborated — `captures/11-omio/01` records
   "Tripadvisor presented the same shape … Two of eleven competitors have now blocked capture at
   consent with no compliant path forward."
3. **Theme count:** I derive 22 uncited findings on `price-honesty`, not 21. The other eight match.
4. **F61 misattributes the Toronto assertion to Google Travel.** The primary capture says Kayak.
   The index's own rule applies: if index and capture disagree, the capture wins.
5. **Three conclusions cite capture keys that are not finding IDs** and cannot resolve in
   `Evidenced [F-nnn]` form: rec-3 (`price_construction_at_checkout`), insight-5
   (`disclosure_spectrum_updated`), rec-6 and insight-4 (the MATERIAL_CORRECTION capture).
6. **Not verified:** WORLD.json's 117 vs 121 (C-043) — not opened, out of scope. Stated so its
   absence does not read as a clean result. 30 of 50 capture files were not opened.

Theme adjacency was a poor hint, as warned. Every corroboration that mattered crossed themes:
F91 (`loyalty-and-retention`) corroborated a `trip-as-an-object` pain; F43
(`ranking-and-comparison`) corroborated a recommendation cited from a `price-honesty` capture.

## Assumptions

- Independence is judged from capture metadata, not causal knowledge. The Skyscanner and Kayak
  location captures share one session, one afternoon and one IP — a shared cause I cannot exclude
  and which F61 itself flags as unestablished.
- Absence of a corroborating finding is absence of a corroborating *observation*, never evidence
  the phenomenon is rare. Coverage is skewed: Booking.com, Google Travel and Kayak have 7 captures
  each; Hopper, Skyscanner, Rome2Rio, Citymapper, TripIt and Omio have 1.
- Analyst prose inside capture files (`why_it_matters`, `pattern_family`) was read as
  interpretation, not observation. This is why F91 is only "partially" for pain-10 despite its own
  capture calling it the same family as F22.
- **One-sidedness, declared.** Every conclusion on this board rests on an analyst observing a
  product surface. `research/evidence-ledger.json` holds zero records. Not one of the ten pain
  points is a traveller reporting harm; each is an inference that a described surface *would* harm
  the stated primary user. The Tripadvisor capture shows the discipline held under pressure —
  review text was pulled twice by regex and discarded at write time. That was the right call, and
  it leaves the board without testimony. Corroborating a pain point across two products makes the
  observation sturdier. It does not make it a user problem, and no amount of competitor capture
  can close that gap.
