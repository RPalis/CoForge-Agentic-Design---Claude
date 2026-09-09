# Luma competitor benchmark (Batch 3) — coverage reconciliation

**Type:** competitive-benchmark · **Stage:** discover · **Status:** draft, awaiting Gate A
**Produced by:** research-synthesizer · **Date:** 2026-09-03
**Subject:** the Batch 3 nine-phase competitor study for Luma, a first-time-traveller travel
product at ideation. Not CoForge. The name collision with this repository's former project
name (ADR-009) is noted and is the reason the workstream is called `luma-travel`.

This artifact answers one question: **what did the Batch 3 study actually establish, and
over how much of what it set out to cover.** It carries no market findings. Those are in
the companion artifact, which cannot be read without this one.

---

## What this is not

- It is **not** a merge of the Batch 3 study with the earlier "Hermes and Claude" study.
  `Evidenced [D-002]` fixes those as two separate framings and forbids one matrix.
- It is **not** a competitor comparison. Six rows of comparison would misrepresent a
  fourteen-row scope. `Evidenced [D-001]`.
- It contains **no claim about what any user wants, needs or feels.** The evidence ledger
  holds zero records, none may be minted, and the study itself holds no user research.

---

## How to read a claim here

Every statement below carries one of these labels, per CLAUDE.md.

| Label | Means |
|---|---|
| `Evidenced [S-nn § …]` | Resolves to a sha256-baselined file in `research/sources-manifest.json` and to a real heading inside it. See **Source register**. |
| `Evidenced [D-00n]` | Resolves to a Gate A decision in `validation/decisions-log.json`. |
| `Derived` | Arithmetic performed here on the cited source, with the method stated so it can be re-run by hand. |
| `Inferred` | Reasoning. Names what it is inferred from. |
| `Assumption` | Neither. Collected in **Assumptions**. |

### Why not `[ART-nnn § …]` for the sources

ADR-017 defines `Evidenced [ART-nnn § Section]` as resolving against
`artifacts/_registry.json`. **None of the 48 Batch 3 source files is a registered
artifact**, and minting artifact IDs for raw sources would manufacture exactly the false
provenance ADR-017 refused when it declined to mint ledger IDs for measurements. The
`[S-nn]` register is local to this artifact, is declared in full below, and bottoms out in
the same place an `[ART-nnn]` citation does: bytes a reader can hash independently.

`[ART-nnn § …]` **is** used for the companion artifact, which is registered.

---

## Source register

All paths relative to `research/sources/luma-competitor-analysis/`. Hashes are copied from
`research/sources-manifest.json` as recorded on 2026-09-03. **They were not recomputed
here** — this agent holds `Read, Write` and no shell — so the register attests to what the
baseline says, not to a fresh hash. Recorded as gap G-06.

| ID | File | sha256 | Read? |
|---|---|---|---|
| S-01 | `2nd to 8th step outputs/luma-benchmark-plan.md` | `aa811e78329f0fb2cae41acc5e219c7c54ba04ca614b25b4e777e20d07ce6b98` | yes |
| S-02 | `2nd to 8th step outputs/booking-com-competitor-profile.md` | `07a91166d8754cc5bc29a5c3abe6861fabbfbe7dfb42facbaa8340caf8b5770b` | yes |
| S-03 | `2nd to 8th step outputs/expedia-competitor-profile.md` | `11b2e7afa459940077b0b63434bda494438af1b313524338cd190a0849ad7891` | yes |
| S-04 | `2nd to 8th step outputs/google-travel-competitor-profile.md` | `2c4c7d8c2d969c70c1e0ae43c5389712b4ffe5f621585375d6acd96b3aae1b0c` | yes |
| S-05 | `2nd to 8th step outputs/hopper-competitor-profile.md` | `ed9bf09b4d6543405dd51f4a2f480d3f2e2f8acdfa3b7cee7d3833c86bb7ee07` | yes |
| S-06 | `2nd to 8th step outputs/tripadvisor-competitor-profile.md` | `67dc93cdebfecb92e8f4c9ab1b2b4e5e9f930eaa835e2c5cc4ef5843b25d3231` | yes |
| S-07 | `2nd to 8th step outputs/tripit-competitor-profile.md` | `d339d88cce53bf44202ee246e2abaf20903277bdceab96bdf3e164fb65a8e121` | yes |
| S-08 | `2nd to 8th step outputs/luma-feature-inventory.md` | `2d9dc341fd9831006fde69307fa228a3868fa5be6056677373816edc1abd1590` | yes |
| S-09 | `2nd to 8th step outputs/luma-pattern-analysis.md` | `9508a80e0e0753b84eebb02dc00afce93844777d45e054c63d15f3811fa0c49f` | yes |
| S-10 | `2nd to 8th step outputs/luma-journey-comparison.md` | `f86d5d37b9daa51bf43078493845a859a7f11ceb983885894d3980d2b7d47446` | yes |
| S-11 | `2nd to 8th step outputs/luma-white-space-analysis.md` | `5271e8b37da305bdfe2180acec4986ac8e26057248a1c24bbb2bdf11c87afcfc` | yes |
| S-12 | `2nd to 8th step outputs/luma-opportunity-scoring.md` | `4e5aa43fc47e7762eae7a74a9e04bf5ce593b05f7f93f0e179d5ec5082dba470` | yes |
| S-13 | `2nd to 8th step outputs/luma-strategy-recommendation.md` | `c099f3dcc24da74793d76368d8fb6843b62d2a27386fde7bc065eb7c54fdd6fc` | yes |
| S-14 | `Prompts startegy/_guardrail.txt` | `b322467cbb2761004565ce74a5c9a63a96bedb021e0b011dbe2edfa03edd9441` | yes |
| S-15 | `Prompts startegy/00-README.md` | `eca44cae16f4cdfc2fd8109d400196f8c8df59f922f7a4edd64a3162d89fa33d` | yes |
| S-16 | `2nd to 8th step outputs/build_inventory.py` | `78cfb3a6907af6604ccfbdd3a881905bf028c66d304bb2f8a53a0ccf020f5b89` | yes |
| S-17 | `2nd to 8th step outputs/luma-executive-report.pdf` | `3558b5c5b48a3725f62c743f4dbb706039afe6328832bead72f700ffaac33d01` | **no** — read indirectly via S-17.1…S-17.8 |
| S-17.1…8 | `2nd to 8th step outputs/rp-1.jpg` … `rp-8.jpg` | `3192e16b…`, `25dee45a…`, `270fbc83…`, `862c7888…`, `2650c889…`, `491d6abc…`, `d946a3ee…`, `031ed840…` | yes — these are page images 1–8 of S-17 |
| S-18 | `2nd to 8th step outputs/luma-feature-inventory.xlsx` | `46e65d5e786424006fa080cac7bca9c72efae12239455f55b0bf9df40621e32e` | **no** — read indirectly via S-16, its generator |
| S-19 | `Luma-Competitor-Analysis - Hermes and Claude.docx` | `98b4fef7bc48bfd5a38c2cc529dc1188753e0f725cea58ff8793d25b7e5e3b32` | **no** — binary, unreadable with the tools held |
| S-20 | `2nd to 8th step outputs/luma-executive-report.docx` | `f5c7a93caa46100d3dedee5e592b951388250c1c8d874c3e1379a850ca02f0a8` | **no** |
| S-21 | `2nd to 8th step outputs/lu41h5dj8.tmp` | `3558b5c5b48a3725f62c743f4dbb706039afe6328832bead72f700ffaac33d01` | n/a — byte-identical to S-17 |
| S-22 | `2nd to 8th step outputs/AI Workflows for UX figma batch 3.png` | `c6e31e4bbf7814cf369e0d94abde7d2e489b0c9f83767ef73a1c9d6db6585ed2` | **no** — exceeds the 2000×2000 px read limit |
| S-23 | `2nd to 8th step outputs/build_report.js` | `5497ce5e83ea729f001985d57c1a81a1ac7c7f758402a8b3201d494863f31f4a` | not read |
| S-24 | `2nd to 8th step outputs/package.json` | `1ad896461fe8445ff4dd51ba2afbe8d116b1a46b8ca4aae721418b5150354e34` | not read |
| S-25 | `Prompts startegy/01-define-benchmark.md` … `08-strategy.md` | eight files, hashes in the baseline manifest | **all eight read** |

Not read: the eight `.head` partial duplicates of S-25, each roughly half the byte size of
its namesake. G-25.

**File count.** `research/sources-manifest.json` records **49 files across the whole of
`research/sources/`**, of which **48** are under `luma-competitor-analysis/` and one
(`coforge-home.png`) is not. `Derived` from the manifest's own file list.

---

## Coverage

### The fourteen

The benchmark plan confirms fourteen competitors in scope, grouped direct / adjacent /
analogous, each with a stated reason. `Evidenced [S-01 §2 Competitor set]`.

| # | Competitor | Category | Profiled? | Evidence that exists |
|---|---|---|---|---|
| 1 | Booking.com | direct | **yes** — competitor 2 of 14 | Tier 1 walkthrough + Tier 2 docs `[S-02]` |
| 2 | Expedia | direct | **yes** — competitor 1 of 14 | Tier 1 walkthrough + Tier 2 docs + Tier 5 vendor claim `[S-03]` |
| 3 | Google Travel | direct | **yes** — competitor 5 of 14 | Tier 1 walkthrough only, **signed in** `[S-04]` |
| 4 | Kayak | direct | **no** | **prior-art framing only** `Evidenced [D-002]` |
| 5 | Skyscanner | direct | **no** | **prior-art framing only** `Evidenced [D-002]` |
| 6 | Hopper | adjacent | **yes** — competitor 4 of 14 | Tier 1 partial + Tier 2 docs; results unreachable `[S-05]` |
| 7 | TripIt | adjacent | **yes** — competitor 3 of 14 | Tier 2 docs; product behind an auth wall `[S-07]` |
| 8 | Airbnb | adjacent | **no** | none in this study |
| 9 | Tripadvisor | adjacent | **yes** — competitor 6 of 14 | Tier 1 walkthrough + Tier 2 docs `[S-06]` |
| 10 | Rentalcars.com | adjacent | **no** | none in this study |
| 11 | Trainline | adjacent | **no** | none in this study |
| 12 | Omio | adjacent | **no** | none in this study |
| 13 | Citymapper | analogous | **no** | none in this study |
| 14 | Rome2Rio | analogous | **no** | none in this study |

`Evidenced [S-01 §2]` for scope and category. `Evidenced [S-02 … S-07]` for the "competitor
N of 14" line each profile carries in its own header. `Evidenced [S-08 header]`, which
states "6 of 14 researched so far" and names the eight absentees.

### The numbers

- **14** confirmed in scope. `Evidenced [S-01 §2]`
- **6** profiled. `Evidenced [S-08 header]`, corroborated by the six profile headers.
- **8** never profiled: Kayak, Skyscanner, Airbnb, Rentalcars.com, Trainline, Omio,
  Citymapper, Rome2Rio. `Evidenced [S-08 Gaps]`, `Evidenced [S-17.7 §10]`.
- **2 of those 8** — Kayak and Skyscanner — carry evidence, but only in the earlier
  framing, which may be cited as prior art and may never be presented as current coverage.
  `Evidenced [D-002]`.
- **6 of those 8** have **no evidence in either study**.
- The eight appear on the board as **empty rows**, not as scoped-out. `Evidenced [D-001]`.

**Empty is not the same state as checked-and-absent.** The encoding must distinguish them,
because the study's own rule 2 forbids reading a blank as an absence.
`Evidenced [S-01 §5 Rules that hold for the whole study]`.

### Two of the eight were pre-scoped, and are still unprofiled

The plan itself narrowed two of the eight before Phase 2 began: Airbnb was to be researched
narrowly against the pre-purchase-guarantee pattern rather than given a full eight-stage
profile, and Rentalcars.com was to be time-boxed to one pass.
`Evidenced [S-01 §2 Competitors I think are weak choices, and why]`. Neither narrowing was
executed, because neither competitor was researched at all. A narrowed profile and no
profile are different results and the board must not blur them. `Inferred` from the plan's
recommendation set against the absence of any Rentalcars.com or Airbnb output in the source
folder.

---

## Evidence reached

Coverage of *competitors* is one denominator. Coverage of *cells* is the other, and it is
worse.

### The feature grid, recounted

The study's matrix is 55 feature rows across 10 capability clusters, with six competitor
columns plus a fixed Luma column that always reads "Not built (ideation), decision
required." `Evidenced [S-08 §1 Feature matrix]`, `Evidenced [S-16 FEATURE MATRIX DATA]`.

`Derived`, by counting every cell in the row literals of `S-16` — the generator that
produces the companion spreadsheet `S-18`, which `S-08` names as "the primary format for
the matrix":

| Value | Count |
|---|---|
| Yes | 99 |
| No | 55 |
| Partial | 35 |
| Unknown | **141** |
| **Total** | **330** = 55 rows × 6 competitor columns |

A second, independent pass over the same literals counting **confidence tags** rather than
values reconciles to the same total, which is the check that the count is not drifting:

| Tier | Count | What it is |
|---|---|---|
| High (H) — Tier 1, live product | **98** | observed |
| Medium (M) — Tier 2, first-party docs | **90** | documented, not observed |
| Low (L) — Tier 5, vendor marketing | **1** | Expedia's Romie assistant |
| untagged (Unknown) | **141** | not verified |
| **Total** | **330** | |

98 + 90 + 1 = 189 evidenced cells; 189 + 141 = 330. `Derived`.

**The number that matters.** The plan's grid was fourteen competitors, so the full matrix
is 55 × 14 = **770 cells**. **98 of 770 — 12.7% — rest on Tier 1 observation.**
**189 of 770 — 24.5% — rest on any evidence at all.** `Derived` from `[S-01 §2]` and the
recount above.

### The journey grid

Eight stages × six profiled competitors = 48 stage-cells. Counting the Unknown cells in the
stage strength table: Expedia 2, Booking.com 1, TripIt 0, Hopper 3, Google Travel 3,
Tripadvisor 2 = **11 Unknown**, so **37 of 48** profiled stage-cells carry a rating.
`Derived` from `Evidenced [S-10 § Stage strength table]`.

Against the planned fourteen-competitor grid of 112 stage-cells, **37 (33%)** are rated.
`Derived`.

### Tier reached per competitor

`Evidenced [S-16 SOURCE REGISTER SHEET]`, reproduced verbatim in the executive report
`Evidenced [S-17.3 §2 Method and evidence standard]`:

| Competitor | Access this run | Highest tier reached | Session state |
|---|---|---|---|
| Expedia | live web walkthrough + docs | Tier 1 (Verified) | signed out, Spain, USD |
| Booking.com | live web walkthrough + docs | Tier 1 (Verified) | signed out, Spain, EUR |
| TripIt | public site + help centre | **Tier 2 (docs); app-walled** | signed out |
| Hopper | live web (partial) + help centre | **Tier 1 partial**; prediction app-exclusive | signed out, Spain, USD |
| Google Travel | live web walkthrough | Tier 1, **no docs swept** | **SIGNED IN**, Spain, EUR |
| Tripadvisor | live web + business docs | Tier 1 (Verified) | signed out; **AI chat pre-populated** |

Two of the six are not comparable like-for-like with the other four: Google Travel was
walked signed in while every other profile was walked signed out
`Evidenced [S-04 § Two conditions that change how this profile should be read]`, and
TripIt's product was never seen in operation at all — 12 High claims against 49 Medium,
which its own author flags as "a materially weaker evidence base"
`Evidenced [S-07 § Confidence summary]`.

**Tier 3 of the evidence ladder — screenshots supplied by the user — was never used.**
Every profile records "Evidence supplied by the user: none. Public sources only."
`Evidenced [S-02]`, `[S-03]`, `[S-04]`, `[S-05]`, `[S-06]`, `[S-07]` (session-conditions
block of each). The Phase 6 prompt's user-research input is likewise "none".
`Evidenced [S-25 06-white-space.md, Inputs]`. The eight `rp-*.jpg` files in the source
folder are page images of the Phase 9 executive report, not product screenshots.
`Evidenced [S-17.1 … S-17.8]`.

---

## The untested claim

### What it is

The benchmark plan lists four prior claims to re-verify. The third is:

> "No competitor sells public transport tickets" — "True only within the original ten.
> Trainline, Omio, and Citymapper were never tested. They are now in scope specifically for
> this." `Evidenced [S-01 §5 Four prior claims to re-verify explicitly]`

Trainline, Omio and Citymapper were **admitted to the set for this single purpose** and
**none of the three was profiled**. Rome2Rio, the fourth ground-transport competitor, was
not profiled either. `Evidenced [S-08 Gaps]`, `Evidenced [D-001]`.

### What the six profiled competitors show

The entire public-transport-tickets row is Unknown or a documented No. `Evidenced [S-08 §1
Cluster 1]`. Booking.com is the sharpest case: its first-party documentation carries a
section titled "Private and public transportation" describing comparison across "public and
private ground transportation providers", while the only ground-transport entry points
observed in the header were Car rental and Airport taxis. The profile records this as
"unresolved in both directions." `Evidenced [S-02 Gaps]`.

Under the study's own rule — "Absence of evidence is never a finding … It never produces
'no competitor does X'" `Evidenced [S-01 §5]` — that row cannot support the claim in
either direction. **The designated test did not run.**

### What rests on it

The dependency does not stop at ticketing. The same eight unprofiled competitors carry the
test for a second and much larger claim.

1. **White space item 3.1**, "Selling public transport tickets inside a journey product",
   is filed under *Deliberately unsolved* — a wall, not a door — with the caveat printed in
   place: "Do not treat the blank row as white space until they are run."
   `Evidenced [S-11 §3.1]`. The caveat is correct and it is load-bearing.
2. **The Phase 7 reject list** discards "Sell public transport tickets ourselves" citing
   3.1. `Evidenced [S-12 §4 Rejects]`.
3. **The strategy declines it outright**: "We will not sell public transport tickets
   ourselves." `Evidenced [S-13 §5]`.
4. **The central bet rests on the same gap.** Bet A (opportunity O1, the least-stress
   ranking axis, and the spine of the recommendation) rests on the claim that no competitor
   offers a choosing axis outside price, time and rating. That was verified across **six**
   competitors. `Evidenced [S-13 §1 Where we play]`. The strategy names the exposure
   itself: kill signal 3 is "A specialist among the eight unprofiled competitors already
   owns an effort or stress choosing axis." `Evidenced [S-13 § What would prove this
   strategy wrong]`.

`Inferred` from 1–4: **one unrun test carries both a rejection and the differentiator.**
Three of the four competitors that would settle it — Trainline, Omio, Citymapper, plus
Rome2Rio — are multi-modal ground-transport products whose core surface *is* comparison
across non-equivalent modes, which is the closest thing in the confirmed set to an
effort-based comparison. Whether they rank on effort is unknown and was never looked at.

**Consequence for Gate A.** The recommendation can be reviewed. It cannot be *closed*,
because the study's own stated kill signal for its primary bet is a test it did not run,
and the study says so. `Evidenced [S-13 § Evidence health check]`, which names the eight
unprofiled competitors as "the secondary evidence gap".

---

## Prior claims

Five designated tests: the four weakest prior claims, plus the standing open question the
plan calls "the single highest-value unknown".

### Claim 1 — "No competitor offers airport interior wayfinding"

**Falsified.** TripIt ships Interactive Airport Maps: searchable indoor maps with
step-by-step walking directions, walking-time estimates between any two points, searchable
interior points including gates, restrooms, ATMs and charging stations, stated to work
offline after first load, across roughly 110 named airports, on the Pro tier.
`Evidenced [S-07 §2 Stage 5 · Travel day]`, `Evidenced [S-08 §1 Cluster 6]`.

**At what tier:** Medium. Documentation of intended behaviour from the help centre, not
observed in operation, because the product is app-first and account-walled.
`Evidenced [S-07 § Evidence warning, read this first]`.

**What it does not establish:** the other five competitors are Unknown on this row, not
verified absent. `Evidenced [S-08 §1 Cluster 6]`. A single counter-example is logically
sufficient to falsify a universal negative, which is why this one test could complete on a
partial set. `Inferred`.

### Claim 2 — "No competitor consistently explains its recommendations"

**Falsified as stated.** Four of the four ranked surfaces print a ranking-basis disclosure:
Expedia links a ranking page and states compensation influences hotel ranking but not
flight ranking; Booking.com puts a banner naming commission directly above the first
result; Google Travel prints a two-sentence rule inline and says what happens to the
flights outside the top group; Tripadvisor prints the attractions ranking basis verbatim.
All four High. `Evidenced [S-09 §1.3]`, `Evidenced [S-03 §3 Ranking transparency]`,
`Evidenced [S-02 §3 Ranking transparency]`, `Evidenced [S-04 §3 Ranking is explained at the
point of ranking]`, `Evidenced [S-06 §3 Ranking is explained on the page]`.

**Watch the denominator.** Four of four *ranked surfaces*, not six of six competitors.
TripIt has no ranked surface by design and Hopper's results were never reached.
`Evidenced [S-09 § A note on the word "everyone"]`.

**What replaced it is not evidenced at the same strength.** The re-framed version — the
disclosure exists everywhere but reads as compliance text a first-timer will not parse — is
labelled `Interpretation:` and carried at Low by the source itself, and no user was asked.
`Evidenced [S-11 §2.4]`.

### Claim 3 — "No competitor sells public transport tickets"

**Not tested.** See **The untested claim** above.

### Claim 4 — "Accessibility statements exist only for Booking.com"

**Not re-verified.** Half the claim was confirmed; the other half was never tested.

- **Booking.com:** confirmed. A published accessibility statement citing European
  Accessibility Act scope, published Jun 2025, last updated Aug 2025, describing conformance
  work, training, an annotation kit, inclusive research, automated and manual testing, an
  assistive technology lab and third-party audits. Tier 2, Medium.
  `Evidenced [S-02 §5 Evidence log, entry 34]`.
- **Expedia:** Unknown. A footer link labelled "Accessibility" exists, but three guessed
  URLs returned the error page and the link was never resolved. `Evidenced [S-03 Gaps]`.
- **TripIt:** Unknown. "No accessibility statement was found on the public site or in the
  help centre this session." `Evidenced [S-07 §3 Accessibility]`.
- **Hopper:** Unknown. Not found this session; a help article on assistance for travellers
  with disabilities exists, "which is a different thing". `Evidenced [S-05 Gaps]`.
- **Google Travel:** **not sought** — outside the agreed scope. `Evidenced [S-04 Gaps]`.
- **Tripadvisor:** **not sought** this session. `Evidenced [S-06 Gaps]`.

`Derived`: of the five non-Booking.com competitors, three were searched and not found and
**two were never searched at all**. The plan's own dimension F requires that "Absence of a
statement is recorded as absence of a statement, never as absence of practice"
`Evidenced [S-01 §4 F. Accessibility and resilience]`, so even the three searched cases
cannot support "only". The word "only" remains untested.

### The standing open question — Expedia's conversational assistant

The plan calls this "the single highest-value unknown" and states that hands-on access is
available this run. `Evidenced [S-01 §5]`.

**Unresolved.** The only first-party source found is a 2024 newsroom release describing
Romie as an alpha on EG Labs — Tier 5, permanently labelled a vendor claim. Third-party
reporting that it remained in alpha is Tier 4. A guessed EG Labs URL returned the error
page, and no Romie entry point was found on any surface walked.
`Evidenced [S-03 §5 Evidence log, entries 26–28]`, `Evidenced [S-03 Gaps]`.

The profile records the correct conclusion: "This is absence of evidence from one desktop
web session, and does not establish that Romie is absent or discontinued."
`Evidenced [S-03 Gaps]`. It is treated as unshipped for pattern purposes and is the single
Low-confidence cell in the entire feature matrix.
`Evidenced [S-09 Gaps]`, `Derived` (L = 1 of 330).

`Inferred`: hands-on web access was available and did not raise the ceiling, because the
subject is app-only. The plan's access table predicted a low ceiling for app-first products
and this is the case it did not predict — an app-only feature inside a web-reachable
product. `Evidenced [S-01 §5 Access method per competitor]`.

### Scoreboard

| # | Designated test | Ran? | Settled? |
|---|---|---|---|
| 1 | Airport interior wayfinding | yes | **yes** — falsified, at Tier 2 |
| 2 | Explanation of recommendations | yes | **yes** — falsified, at Tier 1, on 4 of 4 ranked surfaces |
| 3 | Public transport tickets | **no** | no — the three competitors admitted to test it were never profiled |
| 4 | Accessibility statements "only Booking.com" | partial | no — 2 of 5 never searched |
| 5 | Expedia's assistant (standing question) | yes | no — ceiling stayed at Tier 5/4 |

**2 of 5.** `Derived`.

---

## Arithmetic defects

Ten findings. Each is a property of the source material, not a judgement about it. F-01 to
F-05 are checkable by anyone with the same files.

**F-01 — The stated cell totals do not describe the stated grid.** `S-08 § Confidence
summary` gives "Yes 86, No 48, Partial 28, Unknown 113". Those sum to **275**. The same
document states 55 feature rows and six competitor columns, which is **330** cells. 55 cells
are unaccounted for. `Derived` from `Evidenced [S-08 § Confidence summary]` and
`Evidenced [S-08 §1]`. Note that 275 = 55 × 5 exactly, which is one competitor column's
worth — a five-column total against a six-column grid. Whether that is the cause is not
stated anywhere and is not asserted here.

This is not a cosmetic slip. The prompt set requires a confidence summary counting High /
Medium / Low claims at the end of **every** output, in the guardrail block that appears
unchanged in all eight step prompts. `Evidenced [S-14 GUARDRAIL]`, `Evidenced [S-25]`. The
count is the contract, and at Phase 3 the contract is not met.

**F-02 — An independent recount disagrees with every stated figure.** Recounting the row
literals of the generator gives Yes 99, No 55, Partial 35, Unknown 141 = 330, reconciled by
a second pass on confidence tags (98 H + 90 M + 1 L + 141 untagged = 330). Every stated
figure is understated; Unknown is understated by 28. `Derived` from
`Evidenced [S-16 FEATURE MATRIX DATA]`. A hand-count can err by one or two; it cannot err
by 55, and two passes taken on different axes reconciling to the same total is not a failure
mode of this method.

**F-03 — One integer is doing two jobs.** `S-08 § Confidence summary` reports "High (live
product) 86" and, three lines later, "Yes 86". These are different populations: a `No` cell
can be tagged Medium and a `Partial` cell can be tagged High, so the count of `Yes` values
and the count of High tags have no reason to be equal. `Derived` from
`Evidenced [S-08 § Confidence summary]`. Flagged for a human rather than asserted as a
transcription error, because the cause is not visible in the file.

**F-04 — The citable document and the primary spreadsheet disagree on at least one cell.**
For Hopper × "Flight search and compare", `S-08 §1 Cluster 1` reads `Partial (H) results not
reached` while `S-16` encodes `Yes`, `H`, "search only; results not reached". Eight further
cells were spot-checked across five clusters and agreed. `Derived` from
`Evidenced [S-08 §1 Cluster 1]` and `Evidenced [S-16 FEATURE MATRIX DATA]`. The two files
also disagree about which is authoritative: `S-08` says "The spreadsheet is the primary
format for the matrix", while `S-01 §8` says "The document is the citable record."

**F-05 — The defect reached the stakeholder-facing report.** The Phase 9 executive report
reproduces the unreconciled distribution verbatim: "Full inventory: 55 features, cell
distribution Yes 86, No 48, Partial 28, Unknown 113."
`Evidenced [S-17.4 §4 Feature matrix and journey coverage]`. Phase 9 is the document
described as going to stakeholders, and it carries the figure that does not close.

**F-06 — The executive report's Contents page is empty.** Page 2 carries the heading
"Contents" and no entries. `Evidenced [S-17.2]`.

**F-07 — The designated test for a load-bearing claim did not run.** See **The untested
claim**. `Evidenced [S-01 §5]`, `Evidenced [S-08 Gaps]`.

**F-08 — The highest-value standing question was not resolved.** See prior claim 5.
`Evidenced [S-03 Gaps]`.

**F-09 — Two of five accessibility checks were never performed.** Google Travel and
Tripadvisor are recorded as "not sought", which is a different state from "searched, not
found", and the claim under test uses the word "only".
`Evidenced [S-04 Gaps]`, `Evidenced [S-06 Gaps]`.

**F-10 — The source folder holds material the study does not describe, and Phase 9 has no
prompt.** Beyond the 13 markdown deliverables, the report in two formats, the spreadsheet
and the page images, the folder holds `build_inventory.py`, `build_report.js`,
`package.json`, and `lu41h5dj8.tmp` — the last being **byte-identical to the PDF** (same
sha256, `3558b5c5…`, same 161,323 bytes). `Derived` from `research/sources-manifest.json`.
None is named as a deliverable in `S-01 §8`. All eight numbered prompts and the README were
read and **none corresponds to Phase 9**: the README's table runs steps 1 to 8, ending at
strategy. `Evidenced [S-15]`, `Evidenced [S-25]`. So the executive report — the document
that goes to stakeholders and that carries F-05 — is the one deliverable whose method is
undocumented in the sources. `build_report.js` is present and was not read.

### What the study got right, stated because a defect list without it is unbalanced

The study's structural discipline is stronger than its arithmetic. It states its own
coverage on the header of every deliverable; it files Unknown rather than guessing 141
times; it keeps a permanent Tier 5 label on the one vendor claim rather than counting it as
shipped; it records access failures as observations rather than absences; it prints its own
caveats on the last page of the stakeholder report as "Items to verify manually before
sharing" `Evidenced [S-17.7 §11]`; and it says plainly that its user premise is unresearched
and that research is the first move, not the last `Evidenced [S-13 §7 Evidence health
check]`. **The gaps found here were, almost without exception, gaps the study declared.**
This artifact counts them; it did not discover most of them.

---

## Assumptions

- **A-1.** That `research/sources-manifest.json` accurately records the sha256 of each file.
  Not re-verified here; this agent holds no shell. If the manifest is wrong, every citation
  in this artifact points at the wrong bytes.
- **A-2.** That `build_inventory.py` (S-16) is the generator that produced
  `luma-feature-inventory.xlsx` (S-18). The script's final line writes that filename, which
  is strong but is not proof that the shipped xlsx was produced by this version of it. The
  recount in **Evidence reached** rests on this assumption.
- **A-3.** That `rp-1.jpg` … `rp-8.jpg` are page images of `luma-executive-report.pdf`. Each
  carries a footer reading "Luma Competitor UX Benchmark · Executive Report · Page N" for
  N = 1…8 and the content matches the .md deliverables. The PDF itself was not opened.
- **A-4.** That the six competitor profiles are the complete set of Phase 2 output. No
  seventh profile is present in the folder and `S-08` names six, but a profile that was
  written and not supplied would be invisible here.
- **A-5.** That the earlier "Hermes and Claude" study contains evidence about Kayak and
  Skyscanner. This artifact could not open it (S-19 is binary). The claim rests entirely on
  `Evidenced [D-002]`, a Gate A decision, and is carried at that authority and no higher.
- **A-6.** That "Luma" in these sources denotes the travel product, not this repository's
  former name (ADR-009). Supported by the content of every source file; stated because the
  collision is real and a future reader will hit it.

---

## Gaps

Every unknown, carried rather than filled. Ordered by what would change most if closed.

| # | Gap | Why it is open |
|---|---|---|
| G-01 | Eight of fourteen competitors unprofiled | Phase 2 stopped at six. `[S-08 Gaps]` |
| G-02 | Public-transport ticketing, whole row | The four competitors that would settle it were never run. `[S-01 §5]`, `[S-08 Gaps]` |
| G-03 | Whether any specialist already owns an effort or stress axis | Same eight. This is the strategy's own kill signal 3. `[S-13 § What would prove this strategy wrong]` |
| G-04 | Every claim about what a first-time traveller wants or feels | No user research exists in the study; the Phase 6 prompt's research input is "none". The ledger holds 0 records and none may be minted. `[S-11 § Read this before the findings]`, `[S-25 06-white-space.md]` |
| G-05 | `luma-feature-inventory.xlsx` not opened | Binary; no spreadsheet reader available. Read indirectly through its generator (A-2) |
| G-06 | Source hashes not recomputed | No shell. The register attests to the baseline, not to a fresh hash |
| G-07 | The prior-art docx (S-19) not read | Binary. Its content is known here only through `[D-002]` |
| G-08 | The Figma board (S-22) not read | Exceeds the 2000×2000 px image read limit. `S-01 §8` names the board as a deliverable and gives a URL; neither was opened |
| G-09 | How the executive report was produced | No prompt for Phase 9 exists in the supplied set; `build_report.js` was not read. F-10 |
| G-10 | Product context: team, technology, data access, distribution | The Phase 7 prompt asks for it explicitly and it arrived blank. Every feasibility score is scored against ideation-stage reality only. `[S-12 § Product context]`, `[S-25 07-opportunities.md, Inputs]` |
| G-11 | Target markets | Never supplied. The plan flags this as needed before Phase 2 and Phase 2 ran anyway, from a browser in Spain. `[S-01 Gaps]` |
| G-12 | Whether the sharpened purpose statement was accepted | The plan asks for accept/amend/reject before Phase 2 and rates it Low. Phases 7 and 8 hold it constant as "the business goal". No acceptance is recorded. `[S-01 §1]`, `[S-12 § Product context]` |
| G-13 | Three unresolved entries in the supplied competitor list | "Bookum experiences", a duplicate "Booking", and a generic "Car Rental". Raised at Phase 1, never resolved in any later deliverable. `[S-01 Gaps]` |
| G-14 | Depth priority on stages 4, 5 and 6 | The plan asks for confirmation and records the priority as its own judgement. No confirmation appears. `[S-01 §3]` |
| G-15 | Stage 7, return, across the whole set | No product was walked through a return scenario. Absence of observation, not verified absence. `[S-10 Gaps]` |
| G-16 | Expedia's Romie: current status | See prior claim 5. `[S-03 Gaps]` |
| G-17 | Google Travel signed-out behaviour | Walked signed in. Its ranking and personalisation cells are not comparable like-for-like. `[S-04 Gaps]` |
| G-18 | Tripadvisor's planner from a clean start | Chat was pre-populated on load. Every claim resting on it carries the caveat. `[S-06 § Scope note]` |
| G-19 | Hopper's compare surface and onboarding psychology | Results were unreachable; the prediction feature is app-exclusive by the vendor's own statement. The question the plan set for Hopper is untouched. `[S-05 § Two cautions for Phase 3]` |
| G-20 | TripIt's product in operation | Auth wall plus app-first. 49 of its 75 claims are Medium documentation. `[S-07 § Confidence summary]` |
| G-21 | Accessibility statements for Google Travel and Tripadvisor | Not sought. `[S-04 Gaps]`, `[S-06 Gaps]` |
| G-22 | Checkout and post-payment behaviour, everywhere | Excluded by the no-payment walkthrough limit. `[S-01 §5 Walkthrough limits]` |
| G-23 | Auth-walled surfaces across every OTA | Trips, saved lists, signed-in personalisation and loyalty state. `[S-08 Gaps]` |
| G-24 | Whether observed states are stable | Expedia and Booking.com both document that they run tests affecting display and may order results differently across app and web. Any single observation may be one variant. `[S-03 Gaps]`, `[S-02 Gaps]` |
| G-25 | The eight `.head` partial duplicates of the numbered prompts | Not read. Each is roughly half the byte size of its namesake; whether they are truncations, earlier versions, or something else was not established |
| G-26 | The cause of F-01 and F-03 | The arithmetic does not close and the file does not say why |

**Unknown is a valid answer.** `Evidenced [S-01 §5 Rules that hold for the whole study]`.
Nothing above has been filled with a plausible guess.

---

## What a human is being asked to decide (Gate A)

1. Accept or reject the coverage numbers as derived: 14 confirmed, 6 profiled, 8 not, 2 of
   the 8 prior-art-only.
2. Accept or reject F-01 to F-05, and decide whether the Phase 3 and Phase 9 cell totals are
   corrected at source, annotated, or left with this artifact standing as the correction.
3. Decide whether the study's conclusions may be acted on while designated test 3 is unrun,
   given that the same gap carries the primary bet's stated kill signal.
4. Decide the disposition of the six competitors with no evidence in either study, and of
   the two with prior-art-only evidence.

Nothing in this artifact graduates to automatic. research-synthesizer conclusions never do.
