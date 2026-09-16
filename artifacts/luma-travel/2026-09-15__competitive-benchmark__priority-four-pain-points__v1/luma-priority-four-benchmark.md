# Priority-four pain-point benchmark — is each opportunity precedented, and by whom

**Type:** competitive-benchmark · **Stage:** discover · **Status:** draft, awaiting Gate A
**Produced by:** research-synthesizer · **Date:** 2026-09-15
**Scope:** the 4 priority personas (ART-035) and their journey maps (ART-038) — not a
market-wide study. Read `Evidenced [ART-012]` first for the broader Luma competitor
benchmark this one narrows from.

---

## Why this exists

[ART-038](../2026-09-15__journey-map__luma-priority-four__v1/luma-journey-maps-priority-four.html)'s
Opportunities column was flagged by Agentic Designer - RP as too thin — design reasoning
with no evidence behind it, the same defect the rest of this repository exists to prevent
on the Pain side. This artifact audits four specific opportunity cells against real,
named precedent (a live product, a published verification protocol, or an explicit gap
between them) so each can carry a citation, not just a sentence.

**What this is not.** Not a live-account walkthrough like ART-011/ART-012 (no product was
signed into, no transaction attempted). Every claim below is search-aggregated or
single-page-fetched on 2026-09-15, in one session, and is rated accordingly. Where a claim
could not be corroborated, that is stated as a finding, not smoothed over.

---

## Source register

| ID | Source | Fetched | Confidence basis |
|---|---|---|---|
| W-01 | Sociability.app, "How to Book an Accessible Hotel Room: UK Wheelchair User's Guide (2026)" | Full page fetched and quoted | Medium — named accessibility-travel publisher, specific and actionable, not independently corroborated against a second source |
| W-02 | Wheel the World, accessible-hotels listing; AccessibleGO (named in aggregated search results) | Search-aggregated only — direct fetch returned no extractable content (JS-rendered page) | Low-Medium — vendor's own marketing claim, not independently verified |
| W-03 | Islands.com, "The Common Boarding Pass Mistake That Could Ruin Your Airport Experience" | Full page fetched and quoted | Medium — consumer travel publisher, single source |
| W-04 | TSA.gov/mobile, official MyTSA app page | Full page fetched and quoted | High — primary source, the US federal aviation security authority describing its own product |
| W-05 | Wanderlog.com, product marketing page | Full page fetched and quoted | Medium — vendor's own marketing copy, not an independent review |
| W-06 | Aggregated search, "group trip itinerary sharing 2026" (whenavailable.com, tripsil.com, planharmony.com, familytrips.app) | Search-aggregated only, no page independently fetched | Low-Medium — multiple vendor blogs and marketing pages, mutually consistent on feature claims but not independently verified |
| W-07 | Aggregated search, "airline mobile boarding pass scan error 2026" (ironsoftware.com, ez-qr.com, haznos.org) | Search-aggregated only | Low-Medium — technical/vendor blogs, consistent on failure modes, not independently verified |

Cross-referenced against the existing Luma benchmark: `Evidenced [ART-012 § Personalisation
and accessibility]`, `Evidenced [ART-012 § Prepare and itinerary]`, `Evidenced [ART-012 §
Travel day]`, `Evidenced [ART-012 § The journey comparison]`.

---

## P09 Halina — access verification

**ART-030 pain, restated:** unpublished access information; venue websites misleading;
verification burden. `Evidenced [ART-030 § Halina]`.

**What ART-038 v1 said (too thin):** "Structured, verified access info at the point venues
are shortlisted" and "A single verified-access source instead of a phone call per venue" —
correct direction, no evidence it's buildable or that anyone has built pieces of it.

**What the benchmark found.** Halina's exact behaviour — requesting photos of the specific
room, confirming hoist clearance, ringing ahead — is not a personal idiosyncrasy; it is the
published best-practice protocol from a named accessible-travel guide, down to asking for
the "Access Lead," a "detailed access statement" with door-width/turning-circle
measurements, and re-confirming the booking with the hotel directly after paying.
`Evidenced [W-01]`. Two accessibility-specialist booking services (Wheel the World,
AccessibleGO) exist specifically to do this verification once, centrally, instead of per
traveller per booking — pre-visiting properties and publishing measured, photographed
rooms. `Evidenced [W-02]`. Separately, `Evidenced [ART-012 § Personalisation and
accessibility]` already found that Booking.com exposes 18 accessibility attributes as
ordinary, filterable inventory (7 property-level, 11 room-level) with live result counts —
proof that structured accessibility data *can* sit in a mainstream booking flow, not only
in a specialist product.

**Revised opportunity, evidenced:** the gap is not "build verified access info from
nothing" — it's that the specialist pattern (W-01, W-02) and the mainstream filterable
pattern (ART-012) have never been the same product. A traveller either gets Booking.com's
breadth with unverified self-reported attributes, or a specialist's verified depth with a
narrow inventory. Bridging that — surfacing W-01's protocol as structured, filterable data
rather than a phone-call checklist — is the opportunity, and it is now evidenced on both
sides of the gap, not asserted. `Evidenced [W-01]`, `Evidenced [W-02]`, `Evidenced [ART-012
§ Personalisation and accessibility]`.

---

## P14 Bernard — the near-miss

**ART-030 pain, restated:** printed the return boarding-pass pair instead of the outbound
pair, charged £110. `Evidenced [ART-030 § Bernard]`.

**What ART-038 v1 said (too thin):** "Make right vs. wrong document pair perceptually
impossible to confuse" — a correct design principle, unsupported by any market evidence
that the principle is achievable or already attempted elsewhere.

**What the benchmark found, including what it could NOT find.** Mobile boarding passes
are documented as fragile at the point of use for reasons *adjacent* to Bernard's — battery
death, screen cracks, lost connectivity, and airports (named: Morocco, Türkiye) that don't
accept them at all — which is why travel publishers recommend printing as the reliable
fallback. `Evidenced [W-03]`. Separately, digital-wallet passes (Apple Wallet / Google
Wallet) are documented as more failure-resistant than an airline's own app because they
use pre-validated, encrypted data rather than depending on the app staying in sync with a
changed itinerary. `Evidenced [W-07]`. **Neither source, nor any other consulted this
session, documents Bernard's specific failure mode — printing or presenting the wrong leg
of a multi-document pair.** That scenario's only source remains ART-030 itself. This is
recorded as a finding, not filled with a plausible-sounding match: the market conversation
about boarding-pass reliability is almost entirely about the pass failing to scan, not
about a traveller holding the *correct-format, wrong-content* document with total
confidence — which is precisely what makes Bernard's case a near-miss rather than an
obvious failure.

**Revised opportunity, evidenced, and honestly scoped:** two evidenced, narrower moves
replace the single unevidenced one. (1) Wallet-pass adoption as the default rather than
print-or-screenshot removes the *scanning* failure mode `Evidenced [W-03]`, `Evidenced
[W-07]`, but does nothing for Bernard's specific mistake, because a wallet pass can be the
wrong leg just as easily as a printed one — this must be stated, not implied away. (2) The
actual unevidenced-elsewhere gap — confusable multi-document pairs at the commitment
moment — is corroborated indirectly by `Evidenced [ART-012 § Travel day]` (zero High-
confidence cells across all six profiled competitors at this stage) and `Evidenced
[ART-012 § The journey comparison]` (return is Unknown for five of six, because no product
in the study was walked through a return scenario at all). Travel-day and return are where
the market has the least built anything, evidenced twice over now — which makes this a
genuinely open opportunity rather than a solved problem restated, but also means there is
no existing pattern to point to for *how* to solve the specific confusable-pair failure.
That gap is named as unowned, not quietly resolved.

---

## P04 Reuben — the single point of knowledge

**ART-030 pain, restated:** group coordination; single point of knowledge; post-trip
resentment, from organising 12 nights for 8 people across 3 generations. `Evidenced
[ART-030 § Reuben]`.

**What ART-038 v1 said (too thin):** "A shareable plan the group can act on without him" —
directionally right, no check on whether shareable group plans already exist and already
fail at this.

**What the benchmark found.** They exist, and the market's framing of them explains why
Reuben stays the single point of knowledge anyway. The named group-planning products
(Wanderlog, TripIt, Stippl, Travefy, Plan Harmony, Family Trips) all lead with
**collaborative editing** — "live syncing," "group voting," multiple people "contributing"
— not with a low-friction way to hand a finished plan to people who did not plan it and do
not want to plan it. `Evidenced [W-05]`, `Evidenced [W-06]`. Fetching Wanderlog's own
marketing copy directly found real-time collaborative editing and email-forward booking
capture clearly documented, and confirmed that **read-only, view-only sharing for
non-editing recipients is not clearly documented anywhere on the page** — the product's
own framing does not name that use case. `Evidenced [W-05]`. This matches `Evidenced
[ART-012 § Prepare and itinerary]`: TripIt's differentiator is capturing confirmations
from any supplier, which is a capture problem, not a distribution-to-a-passive-audience
problem.

**Revised opportunity, evidenced:** Reuben's 8 travelling companions are not going to
install a new collaborative app to read a plan someone else already built for them — that
is the actual mechanism behind "asked what's the plan for weeks after circulating a
detailed itinerary." The opportunity is not "a shareable plan" in the abstract; it is
specifically a plan that is legible and actionable *without* the recipient adopting any
tool, because every evidenced competitor in this category (W-05, W-06) is built for the
opposite audience — collaborators, not dependents. `Evidenced [W-05]`, `Evidenced [W-06]`,
`Evidenced [ART-012 § Prepare and itinerary]`.

---

## P12 Jaden — airport process opacity

**ART-030 pain, restated:** airport process opacity; document uncertainty, on a genuine
first flight. `Evidenced [ART-030 § Jaden]`.

**What ART-038 v1 said (too thin):** "Step-by-step in-airport guidance for a genuine first
flight" — plausible, unchecked against whether that already exists for free from an
authoritative source.

**What the benchmark found.** It exists, is free, and is government-authoritative — and it
does not cover what Jaden actually asked. TSA's own MyTSA app is documented, directly from
tsa.gov, as covering exactly the mechanical questions Jaden had about security: what can
go in a carry-on, live checkpoint wait times and crowding predictions, and how to prepare
for the checkpoint. `Evidenced [W-04]`. But Jaden's second question — "is passport control
the same as immigration" — sits outside TSA's remit entirely: TSA is a security-checkpoint
authority, not a border/immigration one, and nothing in the MyTSA feature set (checked
directly against the source) touches passport control, immigration, or gate-finding after
security. `Evidenced [W-04]`. This matches the wider pattern `Evidenced [ART-012 § Prepare
and itinerary]` already found: prepare is Weak for four of six competitors precisely
because it is auth-walled or shallow, and none of them own the full physical sequence
either.

**Revised opportunity, evidenced and narrowed:** building "airport guidance" from scratch
would duplicate a free, authoritative, government-run product on the one segment (security)
it already owns well. The evidenced gap is specifically the **seam MyTSA doesn't cover** —
security through to passport control/immigration through to gate-finding, as one continuous
explainer instead of three separately-owned pieces (an airline's own check-in help, TSA's
checkpoint app, and nothing at all for immigration or wayfinding) — which is a real product
angle at Book/Pre-departure stages, not a "point him at MyTSA" non-answer either, since
MyTSA alone leaves exactly the second half of his stated confusion unaddressed. `Evidenced
[W-04]`, `Evidenced [ART-012 § Prepare and itinerary]`.

---

## Assumptions

- **A-1.** That search-engine result aggregation (W-02, W-06, W-07) fairly represents its
  named sources' actual claims. Not independently verified page-by-page; rated Low-Medium
  throughout and never elevated to High regardless of how confident the aggregated summary
  reads.
- **A-2.** That a single fetched page per product (W-01, W-03, W-04, W-05) is representative
  of that product/publisher's position, not a stale or unusually-worded page. Not checked
  against a second page or a second date.
- **A-3.** That "no source found this session documents X" is honestly reported as absence
  of evidence, not evidence of absence — per the standing rule this repository already
  carries from `Evidenced [ART-012 § SR-2 equivalent]`. Bernard's exact failure mode is
  flagged exactly this way, not silently patched with an adjacent-sounding source.

## Gaps

| # | Gap | What it would change |
|---|---|---|
| 1 | No live product walkthrough — no account created, no booking attempted, on any of the six products named | Every W-0x claim stays Medium at best; a hands-on session (matching ART-012's own method) would let several move to High |
| 2 | Bernard's specific failure mode has no external corroboration | The opportunity for P14 is honestly narrower than the other three — flagged in place above, not hidden |
| 3 | AccessibleGO and Wheel the World's own accessibility-verification claims are vendor marketing, not independently audited | W-02 should not be read as proof the specialist model works at scale, only that it is offered |
| 4 | No pricing, availability-by-region, or API/licensing check on any named product | Feasibility of building against any of these findings is unassessed, same caveat ART-012 already carries for its own shortlist |

## What a human is being asked to decide (Gate A)

1. Whether Medium/Low-confidence, single-session web findings are sufficient grounding for
   journey-map opportunity cells, or whether a deeper walkthrough (ART-011/ART-012 style)
   is required before ART-038's Opportunities column is treated as more than directional.
2. Whether P14's narrower, honestly-gapped opportunity is acceptable as written, or whether
   that pain point should wait for further research before any opportunity is stated at all.
3. Whether this artifact's findings may be folded into ART-038 v2's Opportunities cells with
   inline citations (the intended next step), or should remain a separate reference document.
