# Design critique — ART-014 · Luma Batch 3 competitor coverage board (v2)

**Verdict: the gap is the headline for the first screen and stops being the headline below the fold — three consecutive mid-page objects are complete, resolved, six-competitor studies, and on the two most likely export paths (a mid-page screenshot; a PDF) the eight disappear entirely.**

**Reviewer:** design-critic (adversarial, clean context — did not build this, did not read the producing brief's rationale)
**Target:** `/Users/raquelpalis/Projects/coforge/artifacts/luma-travel/2026-09-03__dashboard__batch-3-competitor-coverage__v2/`
**Compared against:** `…__v1/` (ART-013, superseded)
**Gate:** B for this audit · **Gate A on any change this triggers.** Advisory only — I hold no Edit and no Bash. Nothing here is a fix and nothing here is approval.

---

## The one question

**Has the redesign made the coverage gap the headline, or a beautiful object that reads as a finished study?**

Answer: **both, in sequence.** The board splits cleanly at the fold.

*Above the fold it holds, and holds well.* The hero is a fraction (`6/14`), so the denominator travels with the numerator and a crop of the hero alone still carries the gap. The five secondary KPIs are all gap-flavoured (`12.7%`, `24.5%`, `33%`, `2/5`, `0`). The fourteen-row table is genuinely the loudest object on the page: eight near-black rows at `9.79:1` against the ground, full footprint, unbroken. v1's downplay problem is solved *there*. Song & Szafir's applicable finding — visual weight, not hue — was applied correctly, and the validation file's own correction of the brief's overreach on that paper is the best work in this artifact.

*Below the fold it inverts.* The load-bearing spotlight (6 cells), the cluster gap chart (denominated on 330 = 55 × 6), and the journey VSUP grid (48 cells = 8 × 6) are three consecutive sections in which the eight unprofiled competitors are not drawn, not reserved, and not counted. Each is internally complete and self-consistent about six competitors. Each looks finished. Together they occupy the majority of the board's data area. This is the failure mode the artifact exists to prevent, and the redesign did not reach it — it reached the table.

**Screenshot test.** The region most likely to enter a deck is *not* the hero. It is the journey grid: a 6 × 8 colour matrix of named competitors with a capability rating in every cell — precisely the object a stakeholder wants. Cropped to the table plus its legend, the only surviving statement of scope is the `<h2>` ("across the six profiled"), which says *six* and never says *of fourteen*. The section's opening caption and closing caption both say "six" and neither says "fourteen." That fragment does not carry the gap; it loses it. The cluster chart is the second most screenshottable region and loses it harder (DC-01).

---

## Findings

Root cause behind DC-02, DC-03 and DC-21: **every colour ramp on this board was validated in isolation** — `--ordinal`, monotone-within-ramp, one hue at a time — and **no check was ever run across the ramps that share a single viewport.** That is structurally the C-021 / C-024 pattern this repository already tracks: a check that passes on the object it was pointed at and is blind to the composition.

### BLOCKER

**DC-01 — The three mid-page objects silently re-base the study on 6 of 14, and the numbers prove it.**

- The board's own third KPI counts journey cells as **37 / 112** (112 = 8 stages × 14 competitors). The journey grid draws **48** of those 112 cells. **57% of the grid's own denominator is not rendered.** The eight unprofiled competitors are not eight dark rows in that matrix; they are *not rows at all* — the information-removal condition, applied to the exact fact the board exists to make loud.
- The cluster chart is worse because it produces a reassuring *ordering*. Its bars are shares of the six-competitor subtotal (330). Recomputed against the full 770-cell scope (`Unknown_all = Unknown_6 + rows × 8`, rows derived from each cluster total ÷ 6, summing to 55 ✓):

  | Cluster | Chart says | Against all 14 |
  |---|---|---|
  | Loyalty | 16.7% | **64.3%** (18/28) |
  | Vertical coverage | 23.8% | **67.3%** (66/98) |
  | Reassurance & trust | 31.3% | **70.5%** (79/112) |
  | Decision support | 31.7% | **70.7%** (99/140) |
  | Conversational & AI | 44.4% | **76.2%** (32/42) |
  | Personalisation & a11y | 53.3% | **80.0%** (56/70) |
  | Prepare & itinerary | 54.8% | **80.6%** (79/98) |
  | In destination | 56.7% | **81.4%** (57/70) |
  | Travel day | 63.3% | **84.3%** (59/70) |
  | After the trip | 66.7% | **85.7%** (36/42) |

  Total 581/770 = **75.5% unknown**, which is exactly the complement of the board's own `24.5%` KPI. So the board states 75.5% four inches above a chart whose *worst* bar is 66.7% and whose *best* bar is 16.7%. Read alone — and it will be — the chart says "coverage is fine except at the end of the journey."
- The captions are not lying (`"six profiled competitors"` is present in both sections), but the denominator is carried at 12px caption ink while the encoding carries the opposite impression at full size and full page width. Where the copy and the encoding disagree, the encoding wins.

**Suggested fix (advisory).** Give the eight structural presence in both objects. In the journey grid, render all fourteen rows and fill the eight with the same full-footprint absence block already used in the fourteen-row table — the grid becomes 14 × 8 with 64 blocked cells, which is the true picture and costs nothing but height. In the cluster chart, stack each bar: measured-Unknown segment + structurally-unknown segment, denominated on 770, with the 6-competitor figure retained as a secondary label. If the all-14 rebase is judged out of scope, then at minimum put "6 of 14" inside the `<h2>` of both sections and inside a real `<caption>` element so it survives a crop.

---

**DC-02 — In the journey grid the "Unknown" fill falls *inside* the value ramp, between Strong and Adequate. Absence is camouflaged at the good end.**

Computed by hand from the payload's own `color(srgb …)` declarations (WCAG relative luminance):

| Mark | Meaning | Y | Contrast vs `--gap-80` |
|---|---|---|---|
| `--teal-90` `#022b30` | Strong · High confidence | 0.0195 | **1.31 : 1** |
| `--gap-80` `#3c3838` | **Unknown — not reached** | 0.0408 | — |
| `--teal-70` `#005d5d` | Adequate · High | 0.0861 | **1.50 : 1** |

At the rendered size (`.vsup` = 1.5rem / 24px) and in the 12px legend swatches, `1.31:1` is not a distinction. **19 of the 48 cells** — 8 Strong·High plus 11 Unknown — are mutually indistinguishable near-black squares. The pre-attentive read of the grid is "a lot of dark," and dark means *both* the best possible rating and no data. That is the downplay condition returning through the back door, in the one object where it does the most damage.

Second collision in the same grid: `S·M` `#3e575e` (Y = 0.0866) and `A·H` `#005d5d` (Y = 0.0861) are luminance-identical at **1.003 : 1**, separated only by chroma at 24px. "Strong but we are not sure" and "Adequate and we are sure" are the same mark to a glancing reader. This is not the VSUP mechanism working; the mechanism is convergence *within* the uncertain band. The cause is that value here is encoded almost entirely in **lightness** (three steps of one hue), and the blend target `--tier-mix` (coolGray.50, Y = 0.264) happens to sit at the same luminance as `--teal-50` (Weak·High, Y = 0.2644) — so suppressing for uncertainty moves a cell *down the value scale*, confounding "we are unsure" with "it is weaker." That is exactly the misreading the brief worried about, and the legend does not defend against it: the legend explains the six value×confidence swatches but never states *"grey means we are less sure, not that the product is weaker."*

The `S·H` / `unk` text labels are the only thing keeping this legible, and validation.md §2.5 is right that they are mandatory — but a direct label rescues a cell you have already decided to read closely. It does not rescue the impression the grid makes in two seconds, which is the whole purpose of a matrix.

**Suggested fix (advisory).** Move the Unknown mark out of the value ramp's luminance range: give absence a non-fill treatment in this grid (an empty cell with a heavy border and a centred glyph, or a hatch on the ground colour) so it is separated by *form*, not by a 1.31:1 lightness step. If the fill must stay, invert the value ramp so Strong is the *lightest* teal and the ramp never approaches `--gap-80`. Add one sentence to the legend: "Greyed cells mean lower confidence in the rating, not lower capability." Then re-run the palette validator **on the union of marks that appear in this grid**, not ramp by ramp.

---

**DC-03 — Printed or exported to PDF, the eight competitors render as white text on a blank row. The design's central mechanism inverts on the one path validation.md singles out as safe.**

`tr.gap td` sets `background: var(--gap-80)` and `color: var(--raised)` — white text. The stylesheet nowhere sets `print-color-adjust: exact` (nor `-webkit-print-color-adjust`). Chrome, Safari and Firefox all default to *not* printing background colours and background images ("Background graphics" is off by default in the print dialog and in Save-as-PDF). Consequence in a default print or PDF export:

- the eight gap rows lose their fill and keep their white text → **white on white, i.e. blank**;
- `tr.gap.priorart`'s `repeating-linear-gradient` (a background-image) drops too, so the prior-art/never-evaluated distinction goes with it;
- the cluster chart's bars and track are backgrounds → the chart prints as ten empty rows plus percentage labels;
- the journey grid's `.vsup` divs are pure background with no content → 48 empty boxes, surviving only via their `S·H` / `unk` labels.

validation.md §5 states: *"a printed or PDF-exported copy of this page carries everything, including the Meta appendix, with zero clicks — checked by reading the CSS rules directly."* The `<details>` half of that claim is true. The half that matters — that the absence encoding survives — is false, and §9 concedes no print render was captured. The audit reasoned about the two rules it wrote and not about the rule it did not write.

**Suggested fix (advisory).** Add `print-color-adjust: exact; -webkit-print-color-adjust: exact;` to the `@media print` block, **and** make the gap rows legible without any fill at all: set `tr.gap td { color: var(--ink) }` under `@media print`, plus a heavy left border or a bold `▮` glyph in the state cell, so the encoding degrades to something rather than to nothing. Then capture an actual print-to-PDF and record it, because this class of defect is invisible to a screen render.

### ERROR

**DC-04 — The two caveats that would lower the confidence of the board's two most confident marks are behind a click, while the marks themselves are rendered at full assertiveness.**

- **Google Travel** is the board's single verified **Yes** in the load-bearing row — the one positive finding on the entire page. Its `[+ evidence]` note, in a different section, reads: *"Every other profile was walked signed out; ranking and personalisation cells are not comparable like-for-like."* The visible text says only "Walkthrough only, **signed in**." The consequence of that fact is disclosed; the fact alone is not self-interpreting, and it does not appear anywhere near the spotlight cell or the journey row it qualifies.
- **Tripadvisor** carries **three `S·H` cells** — more Strong·High ratings than any other competitor, i.e. the most confident row in the grid. Its hidden note reads: *"The originating prompt was not typed; every claim resting on it carries that caveat."* A High-confidence encoding whose originating interaction the researcher did not perform is a direct conflict between the visible encoding and the hidden text.

This is not two slips; it is the disclosure rule applied with the wrong test. `manifest.json → notes.interaction_boundary_held` claims every disclosure holds "EVIDENCE OR ELABORATION only… None hides or reveals a DATA VALUE." But this board *elevates confidence to an encoded data dimension* — that is what the VSUP grid is for. On the board's own terms, a caveat that would move a cell from High to Medium **is** a data value. The boundary is violated by the board's own definition.

**Suggested fix (advisory).** Promote both caveats to the static flow at the point of the mark they qualify: a visible asterisked line under the spotlight ("the one Yes was observed signed in; not like-for-like with the other five") and under the journey grid ("Tripadvisor's Discover/Compare ratings rest on a prompt the researcher did not type"). Retest every remaining disclosure against "would this change a confidence tag?", not against "is this a number?".

---

**DC-05 — Two denominators (770, 112) appear on the board, neither is defined, and the disclaimer flatly contradicts them ten lines below.**

The KPI band reads `98/770` and `189/770` and `37/112`. Neither 770 (= 55 rows × 14 competitors) nor 112 (= 8 stages × 14) is explained anywhere on the page or in `validation.md`. Immediately below, the disclaimer says: *"This board uses 330 throughout."* A reader who does the disclaimer's own arithmetic (99+55+35+141 = 330 ✓) and then looks up at `/770` has been told something false by the one panel on the board whose entire purpose is to establish that the study's arithmetic cannot be trusted. The panel that polices the numbers is the panel that misstates one.

Worse, `189 = 330 − 141` exactly — the strongest gap statement on the board (`24.5%` of full scope has any evidence at all) is fully derivable and completely unexplained, so it is the easiest figure to dismiss as an error.

**Suggested fix (advisory).** Define both denominators inline in the KPI floor labels (`770 = 55 feature rows × 14 in scope`; `112 = 8 stages × 14 in scope`) and restate the disclaimer as "this board uses the recount — 330 for the six profiled, 770 for the full fourteen — never the stated 275."

---

**DC-06 — Assumption A-4 is factually false as of the day before this board was dated, and it is hidden inside the collapsed Meta.**

The board asserts: *"A-4. Colour values are read from token release 0.2.0, whose bone/ink/coral primitives carry a Gate A a human has not yet cleared."* `design-system/tokens/tokens.json` records:

```
"gate": "Gate A — APPROVED by Agentic Designer - RP, 2026-09-02"
```

The board is dated 2026-09-03. The approval is a day old and is recorded in the exact file the board says it read. This is the C-021 shape: a status inherited from a sibling artifact rather than re-read at the source, and parked behind a disclosure where nobody will check it.

**Suggested fix (advisory).** Delete A-4 or restate it as cleared, citing the tokens.json gate string and date.

---

**DC-07 — `validation.md`'s primary palette evidence is a verbatim terminal transcript from a script that is not in this repository.**

§2.4 and §2.5 print six command transcripts as the load-bearing proof for the whole palette section. §2.4 invokes `scripts/validate_palette.js`; §2.5 invokes `validate_palette.js` — two different paths for one tool. Neither exists: I checked `scripts/validate_palette.js`, `validation/validate_palette.js` and `.claude/skills/dataviz/scripts/validate_palette.js`. All absent. By contrast v1 (`…__v1/validation.md` §2) is scrupulous about this — it names a *method* (`references/color-formula.md` § The six checks) and records the exact ephemeral path the skill was loaded from. v2 presents repo-relative paths, which read as committed files.

**To be fair and precise: the numbers are correct.** I independently recomputed `#8f8b8b` at **2.854:1** vs `#eeece6` (stated 2.85), `--gap-80` at **9.79:1** (stated 9.79), white on `--gap-80` at **11.57:1** (stated 11.57), `warmGray.70` at **6.61:1** (stated 6.60), `gray.70` at **6.61:1** (stated 6.61), and the Medium-confidence hexes `#3d9698` / `#3d7377` / `#3e575e` reproduce exactly. This is a **reproducibility** defect, not a truthfulness one — but a transcript nobody can re-run is not evidence, and this repository's standing rule is that the author is the one person who cannot clear their own check.

**Suggested fix (advisory).** Commit the script, or replace the transcripts with the formula and the inputs so a reviewer can recompute. Fix the two conflicting paths either way.

---

**DC-08 — `validation.md` §7.1 says "the four pre-existing warnings" and then enumerates six.**

> "The four pre-existing **warnings** (2 corrections with no check, C-031/C-033; 2 unverified load-bearing claims, V-015/V-020; 2 stale-surface warnings)"

2 + 2 + 2 = 6, against a JSON count of `"warning": 4`. One of the three pairs is miscounted or misattributed, and the section's purpose is to prove this artifact introduced nothing.

**Suggested fix (advisory).** Re-read the audit JSON and enumerate the four actual warnings by id.

---

**DC-09 — `validation.md` §4 misprints one of the ten figures it exists to make re-runnable, and it is one of the figures the file makes a point of having recomputed.**

The traceability row reads: `23.8, 31.7, 31.3, 16.7, 54.8, 63.3, 56.7, 66.7, 44.4, 23.8→ see note`. The tenth value is `16/30 = 53.3%`, not 23.8 (23.8 is the first entry, `10/42`, duplicated). The payload renders **53.3% correctly**, so the board is right and the validation file is wrong — which is the more dangerous direction, because §4 is the artifact someone would re-run against. The dangling `→ see note` points at a note that does not exist in the file.

Everything else in §4 checks out: the ten Unknown counts sum to **141** ✓, the ten cluster totals sum to **330** ✓, all ten rendered percentages match their fractions ✓, and both F-01 rows sum correctly (275 ✓, 330 ✓, and 275 = 55 × 5 ✓).

**Suggested fix (advisory).** Correct to 53.3 and either write the note or drop the pointer.

### WARNING

**DC-10 — The hero states the numerator, and the sentence that stops D-001 from being violated appears once, at 12px, outside the table it protects.**

The display figure is `6` at 3.875rem; `8 never reached this run` is at 0.875rem — a **4.4×** size ratio in favour of the reassuring number. The fraction rescues this (the `/14` denominator does the work), so I do not think the hero fails — but it is worth naming that the largest number on a board about a gap is the count of what *was* done.

The sharper problem is the exculpation. *"Never evaluated — a scope decision, not a finding about the competitor"* appears exactly once, in `<p class="legend14">` at `--fz-cap`, **above** the table and outside it. Crop the fourteen-row table — the second most screenshottable region — and what remains is eight named companies blacked out with no statement that the blackness is about the researchers. Meanwhile `tr.gap .gapword` renders the **competitor's name** in bold white at the highest contrast on the page: the alarm is attached to the entity, not to the process. That is the precise reading D-001 exists to prevent, and it is mitigated only by text that does not travel.

**Suggested fix (advisory).** Move the exculpatory clause into a real `<caption>` element on the table (captions travel with the table in a copy, a crop is more likely to include them, and AT gets it for free), and drop the gap rows' competitor names back to regular weight so the block reads as a state of the *row*, not a verdict on the *name*.

---

**DC-11 — Coral is the only saturated hue on the board and it is spent on F-01, not on the coverage gap.**

On a warm-grey ground with an achromatic absence palette, the `--coral` left border on the disclaimer is the single chromatic attractor on the page, sitting directly under the KPI band and above the fourteen. Its heading is a full declarative sentence ("this board's own denominator was itself wrong at source"). A reader with one unit of alarm to spend will spend it there, and walk away with "the study's arithmetic was wrong" rather than "the study covered less than half its scope."

I accept the counter-argument (Bach et al.: a disclaimer belongs next to the number it taints, and the numbers it taints are directly above). This is a judgment call, not an error — but it is a real second headline competing with the declared one, and it should be a conscious choice rather than a by-product of coral being the only accent in the token set.

**Suggested fix (advisory).** Either demote the disclaimer below the fourteen, or reduce it to a rule + label without the chromatic bar, or accept it and say in the artifact notes that the board deliberately carries two headlines.

---

**DC-12 — The class collision reported as fixed in §8 was patched on one property; two others still leak.**

`.val` is bound twice: `.kpi .val` (KPI numerals) and `.val` (cluster-chart percentage labels). §8 records the render-caught `text-align` bug and its explicit override. But `.val { font-family: var(--mono); font-variant-numeric: tabular-nums; }` has specificity 0-1-0 and `.kpi .val` declares neither, so the five secondary KPI values still take their typeface from a rule written for a chart in a different section. The rendering is benign (arguably good), which is why it went unnoticed — but any future edit to the chart's `.val` silently restyles the KPI band. A symptom was fixed; the collision was not.

**Suggested fix (advisory).** Rename the chart rule to `.pct` and remove the compensating `text-align: left` from `.kpi .val`.

---

**DC-13 — `✓` means "capability present" in the spotlight and "prior claim falsified" in the scoreboard, twenty lines apart.**

The board establishes a clean completeness vocabulary in `legend14`: `●` full, `◐` partial, `○` none. The scoreboard uses `◐` and `○` from that vocabulary for tests 3–5 and then breaks it with `✓` for tests 1–2, where `✓ Falsified` marks a *negative* result. In the spotlight, `✓ Yes` marks a *positive* one. Same glyph, opposite valence, same page, no legend for either set.

**Suggested fix (advisory).** Use `●` for the two settled tests, keeping the scoreboard inside the vocabulary the board already declared, and legend the spotlight's `✓ / ✗ / ○` explicitly.

---

**DC-14 — An off-token `font-size: 0.5em` on the hero produces a fifth rendered type size, and the audit method could not have caught it.**

`<span style="font-size:0.5em">/14</span>` computes to **1.9375rem** — not one of the four declared sizes, not a token, and *larger* than `--fz-h2` (1.75rem). validation.md §6 claims "Four sizes and two weights" and describes the check as "every `rem` literal in the file was extracted and checked against tokens.json." The value is an `em` literal, so the stated method was structurally blind to it. Five sizes render, and the off-token one is on the single most important element on the board.

**Suggested fix (advisory).** Replace with a token size (`--fz-h2` reads well as the denominator) and extend the extraction to `em`, `%` and `px` literals, not just `rem`.

---

**DC-15 — "Prior-art only" and "never evaluated" collapse at a glance; they separate only on close reading.**

The stripe is `repeating-linear-gradient(135deg, --gap-80 … --gap-60 …)` — Y 0.0408 vs 0.0447, a very small step on an already-dark field. At normal reading distance both states read as one thing: a black row. They separate on the 12px bold word (`◐ Prior-art only` vs `○ Never evaluated`) and the differing glyphs, both of which are correct and legible when you look. So the answer to "do the first two collapse into *dark = bad competitor*?" is: **partly**. They collapse into *dark = something is missing here*, which is the honest reading and is acceptable; the D-001 risk comes not from the collapse but from DC-10's missing exculpation.

**Suggested fix (advisory).** If the two states must be distinguishable pre-attentively, differentiate by *footprint* rather than by a 1.1:1 fill step — e.g. block only the State-through-What-exists columns for prior-art and the whole row for never-evaluated. If not, say so and leave it; the words carry it.

---

**DC-16 — The word-count claim is the only measurement in `validation.md` with no reproducible command, and it is the one under dispute.**

I cannot adjudicate 1,156 vs 1,234 — I hold no Bash and will not guess a token count. What I can establish:

- Both pairs are **internally consistent**: 1,234 + 894 = 2,128, and 1,156 + 867 = 2,023. So this is a tokenizer/scope difference, not an arithmetic slip. The two totals differ by 105 words.
- Every other figure in `validation.md` is presented as a transcript or a hand-computation with its inputs. §5's is presented as *"measured by stripping tags and counting tokens"* — no command, no script, no definition of what counts. That alone justifies restating it.
- There is at least one identifiable **undercount mechanism on the visible side**: the `[+ evidence]` / `[– evidence]` strings are injected by `details.note summary::before` as CSS `content`. They are rendered visible text (6 instances, 2 words each) that exists nowhere in the HTML, so a tag-stripping counter over the source misses them entirely. Whether `<code>ART-011 § Coverage</code>` citation strings, `&mdash;`/`&middot;` entities and table cell text were counted is also undefined.
- The claim's direction matters: **−56% is computed from the lower of the two candidate counts.** If 1,234 is right the true figure is **−53.4%**. Either way the reduction is large and real and the redesign's clutter goal was met — which is exactly why rounding it in the file's own favour is unnecessary and costly.

**Suggested fix (advisory).** Publish the command, or state the figure as "≈1,150–1,250 visible (−53% to −56%)". Do not restate a precise number without a re-runnable method.

### INFO

**DC-17 — Document structure (route to a11y-checker; not adjudicated here).** No `<h1>` anywhere — the outline starts at `<h2>`. No table uses a `<caption>` element (the CSS styles `caption` but every explanatory block is a sibling `<p class="cap">`). No `scope` attributes on any `th`. The journey grid's corner header is `<th></th>`. For a 6 × 8 matrix this materially affects AT traversal, and `<caption>` would also fix DC-10's crop problem for free.

**DC-18 — `validation.md` §2.5 states the wrong mixing space.** It says the Medium swatches were computed as a *"linear sRGB weighted average, matching `color-mix(in srgb, …)` semantics."* CSS `in srgb` interpolates in **gamma-encoded** sRGB (`srgb-linear` is the linear space). The published hexes match the gamma-encoded component-wise mix exactly (`0.55 × 0.007843 + 0.45 × 0.529412 = 0.2425 → 62 → 0x3E` ✓), so the browser behaviour and the numbers are correct — but a reviewer following the stated method would compute `r = 93` instead of `62` and conclude the file was wrong. Restate as "component-wise weighted average in gamma-encoded sRGB, per CSS Color 4 `in srgb`."

**DC-19 — §2.4's rhetorical flourish is true by noise.** *"the fill that means 'we did not look here' is more visually assertive than the fill that means 'Tier 1, verified'"* — `warmGray.80` is **9.79:1** on bone and `coolGray.80` is **9.75:1**. A 0.4% difference is not a design achievement. The assertiveness of the gap rows comes from **footprint**, which §3 correctly identifies as the paper's actual mechanism. Delete the fill comparison; keep the footprint argument, which is the strong one.

**DC-20 — One of the six `<h2>` elements renders at body size.** `.disclaimer h2 { font-size: var(--fz-sm) }`, so §6's claim that "section headers and the five secondary KPI values share `--fz-h2`" is false for the disclaimer. The 8-reading-block count in §5 is correct (6 `<h2>` + hero/KPI + Meta ✓); only the size claim is loose.

**DC-21 — The absence fill and the "Tier 1, verified live" dot are luminance-identical.** `--gap-80` (Y = 0.0408) and `--tier-1` coolGray.80 (Y = 0.0412) sit at **1.004:1** and appear in the same table five columns apart. §2.2's taxonomy claims the ABSENCE hue is "never used for value or tier" — true of *hue*, but hue is barely perceptible on a 12px dot, and what a reader actually resolves is lightness. In practice the size difference (full row vs dot) keeps this legible; it is recorded because it is the same isolated-validation blind spot as DC-02, in a place where it happens not to hurt.

---

## What holds, and should not be revised away

Stated so a revision does not sand off the good parts:

- **The fourteen-row table is right.** Full-opacity, full-footprint, achromatic, rows in ART-011's own order so the gaps sit where they fall rather than grouped into a ghetto. This is the redesign working.
- **The Song & Szafir correction is the best work in the artifact.** The producing agent fetched the paper, found three of the brief's claims overstated, and recorded that on the board itself instead of silently complying. That is the behaviour this repository is trying to buy.
- **The refusal to build a 10 × 6 matrix** because 54 of 60 cells would have to be invented, and the explicit relabelling of the cluster chart as univariate rather than dressing it up as bivariate — correct, and correctly disclosed.
- **The load-bearing spotlight caption** ("the entire evidence base, out of six of fourteen") is the one mid-page object that states its scope in the body text. It is the model the journey and cluster sections should copy.
- **The type discipline, the one-hero rule, the disclosure hygiene on data values, and 0 `<script>` tags** all hold as claimed.
- **All arithmetic on the board itself checks out** — 6+2+6 = 14, 275 = 86+48+28+113 = 55×5, 330 = 99+55+35+141, 141 across ten clusters, 189 = 330−141, 37 = 48−11, all ten cluster percentages. The defects found in §4 and §7.1 are in the validation file, not the payload.

## What I could not check

- **Word counts.** No Bash. See DC-16 — reported as unadjudicated, with the reasons the claim should be restated regardless.
- **The rendered page.** I read the source and computed luminances by hand; I did not open a browser. DC-02 and DC-03 are derived from the declared token values and from documented print-engine defaults, and both should be confirmed with a render before anyone acts on them.
- **Whether ART-011/ART-012's own figures are correct.** Same scope limit the artifact declares (A-1). I checked internal consistency only.
- **The all-14 cluster recomputation in DC-01** assumes each cluster's row count is `total ÷ 6`. That is consistent (the ten row counts sum to 55 ✓) but it is an inference from the board, not a reading of ART-012.

**Skipped is not passed.**

---

*Advisory. This critique changes nothing on its own; it is input to a human decision. Any revision it triggers is Gate A. A confident wrong critique steers bad revisions, so DC-02 and DC-03 in particular should be reproduced in a browser before they are acted on.*
