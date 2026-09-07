# ART-026 v2 — iteration plan: data visualisation and interaction

**Status:** DRAFT. No manifest, no validation.md, not registered. This directory is not an
artifact until the payload passes validation. This file is the build record for it.
**Date:** 2026-09-07
**Supersedes nothing.** v1 stays immutable and becomes `superseded` only when v2 validates.

## Standing constraints for every phase below

1. **Nothing is invented.** Every number drawn resolves to a field in `CAPTURE-INDEX.json`,
   `WORLD.json`, or a named capture file. A number that is not already written down is not
   drawn — it is listed in §6 as owed.
2. **Nothing is skipped.** No chart replaces prose. Charts are an overview layer placed above
   content that already exists; all 121 findings, 8 sections and 188 disclosure panels survive
   intact.
3. **Progressive disclosure is preserved and extended**, in Shneiderman's order — overview
   first, zoom and filter, details on demand. The chart is the overview; the existing cards
   are the details. The 188 `aria-expanded` panels and 2 `<details>` blocks stay.
4. **Affordances stay visible.** Anything interactive announces itself before it is touched:
   a cursor change is not an affordance, a visible control is.

---

## Phase 0 — Reconcile the confidence field. ✅ CLOSED 2026-09-07.

> **Result.** 0a reconciled by set arithmetic; 0b classified all 121 rows mechanically;
> all 8 pointer rows resolved against their capture files. Reproducible via
> `phase0-reconcile.py` → `confidence-reconciliation.json`. Two defects logged, **C-043**
> and **C-044**. Detail in *Phase 0 — what closed* below; the original statement of the
> problem is kept intact underneath it.


**A defect was found while planning this, and it is larger than C-042.**

C-042 recorded that ART-024 mandates a Verified / Likely / Not-Verified tri-state and that the
data holds 169 / 1 / 0. Counting the actual capture data shows the field is not a tri-state at
all. Across the 117 `WORLD.json` chunks there are **14 distinct confidence strings**:

| Shape | Count | What it is |
|---|---|---|
| exactly `"Verified"` | 100 | a clean rating |
| a sentence that qualifies what is verified | 13 | e.g. *"Verified for the mechanism and the unit price. UNKNOWN for the caps."* — each unique, each one-off |
| `"see source"` | 4 | **not a confidence at all — a pointer where a rating should be** |

`CAPTURE-INDEX.json` holds 121 findings and 7 of the same dangling pointers, under the string
`"see capture file"`. `WORLD.json` holds 117 chunks and 4. The dashboard's `FULL_INDEX` is
121 = 117 chunks + 4 stub resolutions.

Two things must close before anything is drawn:

- **0a — Reconcile 121 vs 117 vs the pointer counts (7 vs 4).** Establish whether the 4 stub
  resolutions are the same 4 pointers, and what the other 3 are. Record the answer.
- **0b — Classify every confidence string by transcription, never by inference.** The rule is
  mechanical and inspectable: *does the string equal `"Verified"` exactly · does it carry
  additional qualifying text · is it a pointer to somewhere else.* Nothing is read for meaning
  and nothing is promoted or demoted. Each qualified row keeps its full original sentence,
  displayed in the panel, never truncated (C-039).

**Why this is not optional.** A confidence chart built before this runs would render 14 strings
as 3 buckets by guessing, which is inference on evidence — the exact failure this repository
exists to prevent. And a dangling pointer drawn as a confidence tier is a record present,
believed, and load-bearing on nothing.

**Output:** a `confidence_class` field on every row, plus a correction logged as C-043.

---

### Phase 0 — what closed

**0a — reconciled.** `CAPTURE-INDEX.json` (121) is a strict superset of `WORLD.json` (117);
zero rows go the other way. The gap is exactly 4, and v1's `STUB_RESOLUTIONS` restored exactly
those 4. Cross-checked: **v1's hand-written stubs invented nothing** — every claim and every
evidence string in them was located verbatim in the capture files, including the two that were
not in the correction block itself (Expedia's tier ladder, Kayak's avatar/heart/`Madrid (MAD)`).

**The 4 omitted rows are, without exception, the round's own corrections** — Expedia's One Key
mis-framing, the Google Track-prices over-reach, Kayak's empty-sweep method correction, and the
AirCover refutation. `WORLD.json` calls itself generated and regenerable and says nowhere that
it is a subset. An agent retrieving from the corpus cannot see where the round corrected
itself. **→ C-043.**

Also found: the index id `CORRECTION_to_F28` does not match its capture key
`CORRECTION_to_finding_F28`. A naive resolver reports the content missing when it is present —
the ninth "result that looked like data and wasn't" this round. It is resolved in the script by
dropping the `finding` infix on both sides, and the disagreement is **recorded** in the output
rather than normalised away.

**0b — classified, mechanically, on 121 of 121 rows.**

| class | n | what it is |
|---|---|---|
| `verified-exact` | **101** | the string is exactly `Verified` |
| `verified-qualified` | **13** | starts with `Verified` and carries a one-off sentence saying what was *not* verified — each kept in full, never truncated (C-039) |
| `pointer` | **7** | the literal string `see capture file` — a pointer where a rating belongs |
| `other-shape` / `absent` | **0** | the script exits non-zero if either is non-empty, so nothing is guessed |

14 distinct raw strings. **→ C-044.**

**All 8 rows needing resolution** (7 with a pointer confidence, 4 with a pointer claim, 3 with
both) resolve to real content in their capture files — 8 of 8. But **7 of the 8 blocks state no
confidence of their own**, so the only value available is the capture file's *file-level*
confidence, which rates the capture and not the finding. Only `F71` carries a block-level
`"confidence": "Verified"`. v1 assigned `Verified` to all four of its stubs without recording
that distinction. The output now carries an explicit `confidence_provenance` on every resolved
row.

**What Phase 0 does NOT do.** It does not overwrite the 7 pointers with `Verified` in
`CAPTURE-INDEX.json`, and it does not hand-edit `WORLD.json`. Promoting a pointer to a rating
is exactly the move C-044 exists to catch, and hand-editing a file whose header says it is
never hand-written makes the record worse, not better. Both are source fixes owed to round 2.

**Consequence for chart 2.4.** It is now specifiable: the three classes are real, mechanically
derived, and mutually exclusive. But it plots **101 / 13 / 7**, and the 7 are *not a confidence
level* — they are a missing rating. The chart must show them as a distinct absence, not as a
third tier of certainty, or it repeats the defect in ink.

---

## Phase 1 — Type the 71 prose-buried relations. Transcription only.

Unchanged from the standing plan and still required. 36 capture files reference another finding
by ID inside `why_it_matters`, `comparison` and `why_the_correction_matters`; only 3 relations
sit in a named relational field. Typing them into `supersedes` / `refines` / `corroborates`,
each citing the source sentence it came from, is transcription — the sentences already exist.

Four independent sources now agree this must precede any relational chart: harvest plots,
effect-direction plots, ACH and Toulmin maps all require a pre-existing relation (round 3);
datavizcatalogue's entire Connections family presupposes an edge list, and the sole chart it
lists under Text is the word cloud (round 4, R4-06); Flourish's network templates likewise
(round 5).

**This phase unblocks the relation graph. It does not gate Phases 2 and 3**, which draw counts
that already exist.

---

## Phase 2 — The six charts that are drawable from data already written down ✅ BUILT 2026-09-07

> **Result.** All six built in `charts.py`, wired through `build-dashboard.py`, and verified on
> the **rendered** page by `verify-charts.mjs` — PASS, no failures. 59 matrix numbers at worst
> 5.02:1 against a 4.5 floor; 839 marks at worst 4.25:1 against a 3:1 floor; 0 clipped labels.
> v1's own `verify-encoding.py` and `verify-interaction.mjs` both still PASS, so nothing
> regressed: 121 index rows, 183 panels, focus and Escape behaviour intact. Content grew
> 9,591 → 12,053 visible words; nothing was removed.
>
> **Three defects found by looking rather than by reading**, and all three are the same shape —
> a check that passed while the artefact was wrong:
>
> 1. **Dark text on dark cells, in all 59 shaded matrix cells.** `charts.py` computed the right
>    per-cell colour and set it as an SVG presentation attribute; the CSS rule
>    `.c-cell { fill: var(--ink) }` outranks a presentation attribute and silently overrode
>    every one. The build-time contrast check passed because it verified the arithmetic, not
>    the artefact. Fixed with an inline style, which nothing can outrank.
> 2. **The confidence chart's legend was entirely clipped** — text began at x=334 inside a
>    360-wide viewBox — and the whole chart rendered at roughly 3× because a 360-unit viewBox
>    was stretched to the full column. Fixed by sizing the viewBox to contain the legend and
>    capping the rendered width.
> 3. **`ch-nulls` scrolled sideways at print width**, because an inner SVG carried the 30rem
>    minimum meant for full-width charts. Fixed with an explicit fluid class.
>
> And a fourth in the verifier itself: it first excluded structural fills *by inference*
> (anything lighter than the ground), which silently exempted all 59 matrix cell fills.
> Exemptions are now **declared in the markup** (`.c-struct`, `.c-cellbg`), counted, and
> reported in the output — 26 structural and 59 cell fills — so an exemption can be seen
> rather than assumed.

Each names its source field and the benchmark ruling that selected the chart type. No chart
here needs a number that does not already exist.

### 2.1 Coverage against plan — five bullet graphs ✅
- **Data:** `COVERAGE_ROWS` — 25/136 journey stages · 47/68 booking types · 8/119 states ·
  6/17 walked to a payment gate · 4/17 captured on both browser surfaces.
- **Chart:** bullet graph. Feature measure = reached, comparative measure = what ART-024
  specified, at most five qualitative bands.
- **Selected by:** R4-05 (Stephen Few via datavizcatalogue) and R5-03 (Flourish ships
  *Performance vs target bars*). Two unrelated sources, same answer.
- **Why here:** this is the first thing on the board and stays first. The headline is that no
  competitor is complete.

### 2.2 How much we looked, per competitor — Cleveland dot plot ✅
- **Data:** `per_competitor` — captures and findings per competitor, 18 rows.
  Kayak 18 · Booking.com 15 · Airbnb 14 · Iberia 10 · Expedia 8 · Google Flights 8 ·
  Qatar 8 · Google Travel 7 · Tripadvisor 6 · Trainline 4 · Omio 4 · American 4 ·
  Skyscanner 3 · Rentalcars 3 · TripIt 3 · Hopper 2 · Rome2Rio 2 · Citymapper 2.
- **Chart:** Cleveland dot plot, two dots per row (captures, findings), sorted by findings.
- **Selected by:** R5-04 — three shipped forms exist; the two-value form is the reason to
  prefer the dot plot over a bar.
- **Mandatory label, non-negotiable:** *this measures our effort, not the competitor.* Kayak
  at 18 and Citymapper at 2 says where we looked, nothing about either product. Drawn without
  that label this chart lies, and it lies in the direction a reader will find plausible.

### 2.3 Where the findings landed — sorted horizontal bar ✅
- **Data:** chunk `theme` counts — ranking-and-comparison 35 · price-honesty 28 ·
  loyalty-and-retention 15 · other 12 · disruption-and-protection 8 · decision-support 8 ·
  user-types 3 · trip-as-an-object 3 · method 2 · dark-patterns-and-trust 2 ·
  market-structure 1.
- **Chart:** sorted horizontal bar. Ranking is a purpose Flourish names and datavizcatalogue
  does not (R5-01); the encoding is still an ordinary bar.
- **A finding in its own right:** `other` at 12 is the fourth largest theme, and
  `market-structure` — the theme carrying the board's headline claim — holds exactly 1 chunk.
  Both go in the caption. Neither is flattering and neither is hidden.

### 2.4 Confidence composition — an 11×11 dot matrix ✅
- **Data:** the Phase 0 output. Provisionally 100 / 13 / 4.
- **Chart:** single stacked bar, or dot matrix if the individual rows should stay clickable.
- Phase 0 closed, so this is drawn: **101 / 13 / 7**, exactly 121 marks in an 11×11 grid, three distinct shapes as well as three steps. The 7 are drawn as struck-through open circles — an absence, not a third tier.

### 2.5 Competitor × theme — the Framework Analysis matrix, seriated ✅
- **Data:** 18 competitors × 11 themes, cell = count of findings. Computed exactly from
  existing fields; nothing estimated.
- **Chart:** a **table** with numeric shading and row highlight — not a heatmap.
  R5-05: Flourish files Table as its own family (*Table with charts · Numeric shading ·
  Row highlight · Searchable*), which keeps the text cells Framework Analysis requires.
  R4-03 rejected the Marimekko alternative on the source's own caveat: 187 segments, no common
  baseline, and per-cell comparison is the whole job.
- **Row and column order is computed, never alphabetical** — seriation, per Behrisch et al.
  Alphabetical order is a decision to show no structure.
- **Governance:** under ADR-021 this table is read as values, so it is an ordinary component
  and the membrane applies to it. It is not chart anatomy and does not get the dataviz
  exemption.

### 2.6 The null results — negative space, drawn at true scale ✅
- **Data, all transcribed exactly:**
  - Iberia — 367+ link labels across three surfaces swept for *261 / derechos / compensación /
    reclamación*: **zero matches** (F-56). The `+` is preserved; it is a floor, not a count.
  - Qatar Airways — 289 homepage link labels swept for
    *disrupt / delay / cancel / irregular / compensat / rights / refund*: **zero matches** (F-107).
  - Four loyalty programmes, four full-text searches, **zero** mentions of a first-time
    traveller — Genius (F-02), One Key (F-18), Iberia Club (F-60), Qatar Privilege Club (F-110).
  - Booking.com — an 8,125-character accessibility statement searched for six standards names,
    **one** match, and that match is a statement of alignment rather than a conformance claim (F-06).
  - Airbnb — **zero** sort controls, the only competitor observed with none; Booking.com offers
    **11** ways to reorder (F-69).
- **Chart:** the searched population drawn at full scale with the matches drawn on it, so the
  emptiness occupies real area instead of being asserted in a sentence. Unit encoding, per
  R4-02 — **dot matrix, not pictogram**, and **no partial marks ever**, because 0/367 and 0/289
  do not reduce to whole icons.

### What is deliberately NOT drawn, and why

- **Loyalty tier ladders.** Booking.com's threshold is stated exactly (priority support at 15
  completed bookings in 2 years, F-01). I have **not** verified that a numeric threshold is
  stated for every programme in the set. Where a threshold is not stated, the rung is *absent*,
  not zero, and drawing it as zero would invent a fact. Listed as owed in §6.
- **The ranking-axes comparison.** Booking.com 11 and Airbnb 0 are verified today. The other
  figures I previously cited from memory are **not** re-verified against the captures and are
  not drawn until they are. Listed as owed in §6.
- **The relation graph.** Blocked on Phase 1. No exception.
- **Anything with a time axis.** There is no time dimension in this data. Flourish's time
  slider is the one interaction primitive of the seven with nothing here to drive it, and it
  is not adopted.

---

## Phase 3 — Interaction, from the seven primitives observed in round 5

Flourish's public template catalogue carries essentially seven interaction primitives. Six
apply; the seventh has no data. Each is mapped onto an affordance that is already visible.

| Primitive | Applied to | Affordance |
|---|---|---|
| **Filter** | theme · competitor · confidence class, applied across every section at once | visible chip row, `cf-chip` (promoted L1, ADR-022), selected state announced |
| **Highlight** | hovering or focusing a matrix cell highlights the matching finding cards; hovering a bar highlights its rows | outline plus label, never colour alone (WCAG 1.4.1) |
| **Search** | the 121-row evidence index | a real input with a visible label |
| **Hover / popup** | existing detail panels, unchanged | unchanged |
| **Side panel** | the R5-06 pattern: prose is annotated in place rather than converted to a chart | existing panel mechanism |
| **Reveal** | the 188 `aria-expanded` panels, unchanged | unchanged |
| ~~Time slider~~ | — | **not adopted; no time dimension exists** |

**Governance note that must not be skipped.** ADR-021 exempts chart marks and chart anatomy
from the membrane. It explicitly does **not** exempt *"a bespoke cross-filtering brush"* — that
is product UI and returns to the membrane. So the filter controls in row 1 either reuse
promoted L1 primitives or need a spec, human approval and an ADR before they are built. This
is a real gate, it applies to this phase, and it is not routed around.

**Colour constraint, from a defect we already own.** `cf-chart-palette` is deprecated (C-036) —
four hues at one step on Carbon's universal lightness ladder, under 0.4% luminance apart,
worst-case 1.055:1 against a 3:1 floor. ADR-021 item 1 owes a dataviz token group and it does
not exist yet. Rather than wait or improvise a palette, **v2 is designed to need no categorical
hue**: encode by position, length, and step on the lightness ladder — the escape hatch is step,
not hue. This turns a blocker into a discipline and leaves the owed token group genuinely owed.

---

## Phase 4 — Accessibility, from R5-08

Flourish declines a blanket WCAG AA certification, on the stated grounds that final
accessibility is decided per artifact by palette, titles and annotations. That is a vendor
claim recorded as a vendor claim — and it is the commercial form of ADR-021's open item, which
says no check enforces the encoding contract yet. It argues for the per-artifact adversarial
pass ADR-021 item 4 already requires.

Measured against v1 on 2026-09-07 by grep:

| Feature | v1 | v2 |
|---|---|---|
| reduced-motion | present | keep |
| keyboard / ARIA | 193 `aria-label`, 183 `role=`, 185 `tabindex` | keep, extend to chart marks |
| screen-reader chart description | 0 `aria-describedby` — and 0 `<svg>`, so not yet applicable | **required on every chart**: type, purpose, and the finding |
| **data download** | **0 — nothing, in any form** | **add CSV** |
| auto-contrast labels | — | text-stroke fallback on any label over a mark |

Data download is the only gap on that list, the cheapest to close, and the only item that
helps a reader who cannot use the visual encoding at all.

---

## Phase 5 — Verification, adversarial

- `verify-encoding.py` extended: every chart's drawn number must resolve to a source field, and
  the check fails on any number in the SVG that is not traceable. Charts do not get to be an
  exception to the citation check.
- `verify-interaction.mjs` extended to the six adopted primitives, keyboard path included.
- **`design-critic` and `a11y-checker` have never attacked ART-026.** They attack v2 before it
  is published, not after. ADR-021 item 4 requires exactly this and it has not been done once.
- **Whoever builds the checks does not clear them.** Standing rule; twice on 2026-09-01 a check
  was declared working by its author and was not.
- Print path re-verified (C-039 was a truncation nobody saw across 730 read lines).

---

## §6 — Owed, and named rather than quietly dropped

1. ~~Reconcile 121 vs 117, and 7 pointers vs 4 (Phase 0a).~~ **Closed 2026-09-07.** Remaining
   at source, for round 2, not for v2: regenerate `WORLD.json` to carry all 121 rows and a
   subset warning (C-043); replace the 7 pointers in `CAPTURE-INDEX.json` with real ratings,
   and amend ART-024 §5.2 to a scale that varies (C-044).
2. Loyalty tier thresholds — **partially discharged in passing.** Two complete ladders are
   captured with exact numbers: Expedia One Key (Blue 0–4 → Silver 5–14 → Gold 15–29 →
   Platinum 30+ trip elements, with Member Prices applying independent of tier) and
   Booking.com Genius (priority support at 15 completed bookings in 2 years). Still owed: the
   same confirmation for every other programme in the set. An unstated threshold is absent,
   not zero.
3. Ranking-axis counts beyond Booking.com's 11 and Airbnb's 0, re-verified against captures.
   Only those two are drawn in 2.6; nothing else is.
7. **One capture file of 50 is cited by no finding** — `captures/01-booking-com/01-site-tree-L1.json`,
   a site-tree inventory carrying no finding blocks. Omio's equivalent site-tree capture *did*
   produce findings, so this is listed as owed for a round-2 review rather than closed. Found
   while deriving per-competitor capture counts; `charts.assert_sourced()` now asserts the
   count is exactly one and names it, so a second uncited capture fails the build.
8. **`design-critic` and `a11y-checker` still have not attacked ART-026** — Phase 5, and ADR-021
   item 4 requires it. Self-verification is not that check.
4. The dataviz token group owed by ADR-021 item 1. v2 is built so as not to need it; that does
   not discharge it.
5. Gate A on ART-011, ART-012, ART-016, ART-021, ART-023, ART-025 and ART-026 v1.
6. Re-attestation on the machinery hash — audit check 5g is the standing error.

## Sequence

Phase 0 → Phase 2 (2.1, 2.2, 2.3, 2.5, 2.6) and Phase 3 in parallel → Phase 2.4 once 0 closes
→ Phase 4 → Phase 1 → the relation graph as v2.1. Phase 1 is placed last among the build phases
because it gates only the relation graph, and nothing else waits on it.
