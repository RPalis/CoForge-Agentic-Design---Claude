# Validation — ART-014 · dashboard · batch-3-competitor-coverage · v2

**Payload:** `luma-competitor-coverage-board.html` · **Produced by:** `dashboard-analyst` ·
**Date:** 2026-09-03 · **Status:** draft · **Gate:** B (automated) · **Supersedes:** `ART-013` (v1)

This is a redesign of how ART-013 v1 reads, not a re-research. Content inputs are unchanged:
`ART-011` (coverage reconciliation), `ART-012` (market findings, capped by ART-011), plus
`ART-013` v1 itself as the thing being superseded. `research/sources/` was **not** opened —
same restriction as v1, restated because a redesign is exactly the moment an agent is tempted
to "just check the original" for texture.

---

## 1. Gate B — checklist

From `validation/checklists/dashboard.md`.

| Check | Result | Evidence |
|---|---|---|
| Directory named `YYYY-MM-DD__dashboard__<slug>__v<N>` | PASS | `2026-09-03__dashboard__batch-3-competitor-coverage__v2` |
| `manifest.json` present and valid | PASS | `id` ART-014, type `dashboard` registered in `_types.json`, `supersedes: "ART-013"` |
| `validation.md` present and filled in | PASS | this file |
| Every `[E-nnn]` citation resolves | PASS, vacuously | Zero `[E-nnn]` tokens anywhere except one literal mention of the notation itself, inside `<code>`, in the Meta block's Claim-format note — Gate B strips fenced/inline code before checking citations, so this does not register as a citation. Confirmed: `grep -n "\[E-"` finds exactly that one line |
| No raw hex / no raw px where the artifact is visual | PASS | Same method as v1: every colour is `color(srgb …)` or `color-mix(in srgb, var(--x) …%, var(--y) …%)`, never a `#hex` literal. Re-checked directly (not assumed) — see §6 |
| Every metric names its data source and refresh cadence | PASS | Every section keeps a `[ART-nnn § …]` tag at first use; the header states refresh once (static) rather than repeating it in six places as v1 did — the cadence is a property of the whole board, not of each metric individually, and nothing on the board claims a different cadence anywhere |
| Palette from tokens.json | PASS | §2 — every colour, including the VSUP blends, is a `color-mix()` of two named token values |
| No causal claim from correlational data | PASS | Every statement is a count, a ratio, or a verbatim rating; no causal language |

## Gate A — human review

| Check | Result |
|---|---|
| Claims labelled `Evidenced` / `Inferred` / `Assumption` | PASS — every prose claim carries `[ART-nnn § …]`, `[D-00n]`, or sits in the Assumptions block (now inside the collapsed Meta appendix, per the two-disclosure-level rule — see §5) |
| Assumptions block present and visible | PASS — present in Meta; per Aisch & Tse, assumptions are supporting material, not a headline, so this is the correct disclosure level for it (§5) |
| Reviewed by: ______ Date: ______ | open — `draft` until a human signs |

---

## 2. Palette — reuse, one new mechanism (VSUP via `color-mix()`), and the validator's verdict

### 2.1 What is reused unchanged from ART-013 v1

`teal.50/70/90` (three of the five already-`--ordinal`-validated steps) and `coolGray.60/80`
(the Tier 2/Tier 1 chips) are bit-identical to v1's own validated values. Not re-run through
the categorical/ordinal script a second time for the same reason v1 didn't re-run
`cf-chart-palette` on `bone`: nothing about the underlying tokens changed. Re-confirmed by eye
against `tokens.json` release 0.2.0 that the five components match exactly.

### 2.2 The job taxonomy this board holds itself to

v1 used two colour jobs (teal sequential, coolGray ordinal) plus an accidental third
(`--tier-mix`-equivalent reasoning was implicit). v2 makes the taxonomy explicit and holds
each hue to exactly one job, never reused, so no reader can see one colour carry two meanings
across sections of the same document:

| Job | Hue | Where it appears | Never used for |
|---|---|---|---|
| VALUE (ordinal: capability strength) | teal 50/70/90 | Journey grid only | Cluster gap chart (was teal in v1 — moved, see §2.3) |
| TIER (ordinal: evidence quality) | coolGray 60/80 | Tier chips, spotlight confidence dots | Absence of any kind |
| ABSENCE (categorical + sequential: gaps at every granularity) | warmGray 50–90 | Gap rows, gap cells, cluster gap-density bars | Value or tier |
| EMPHASIS (scarce, one figure) | coral | F-01 disclaimer left border only | Any data-bearing mark |
| Achromatic (no hue at all) | ink | Yes/No glyphs in the spotlight, all body text | Any state that could be misread as a verdict (D-001) |

### 2.3 Why the cluster chart moved from teal to warmGray

v1's ten-cluster bar chart and v2's journey grid are now both present on the same board. If
both used teal, a reader could see `teal.90` mean "90% of this cluster's cells are evidenced"
in one chart and "Strong capability, high confidence" in the next chart eight lines down —
the same hue carrying two unrelated scales in one document, which is exactly the kind of
cross-artifact collision v1 itself refused to create against ART-010 (v1 §2.2). The fix:
the cluster chart measures **gap**, not evidence-reach, and gap is the same construct as the
row-level and cell-level absence blocks elsewhere on this board, just at a different
granularity — so it takes the ABSENCE hue (warmGray), sequential, 5 steps, validated below.
This also means the chart's own framing flips from "% evidenced" (v1) to "% Unknown" (v2);
the underlying numbers are the same ten cluster counts from `ART-012 § The feature matrix`,
recomputed directly (not by subtracting v1's rounded percentages — see manifest.json
`findings.method` and §4 below).

### 2.4 warmGray sequential ramp — validator, verbatim

```
$ node scripts/validate_palette.js "#8f8b8b,#726e6e,#565151,#3c3838,#272525" \
    --ordinal --mode light --surface "#eeece6"

Palette (light, surface #eeece6, ordinal ramp): 5 slots
  [PASS] Lightness monotone     steps read light→dark
  [PASS] Adjacent ΔL            all gaps >= 0.06
  [PASS] Light-end contrast     #8f8b8b at 2.85:1 vs surface
  [PASS] Single hue             hue spread 0°

  → ALL CHECKS PASS
```

Two lighter candidate floors were tried first and rejected, same method v1 used for teal —
tried-and-rejected is recorded, not silently skipped:

```
$ node scripts/validate_palette.js "#f7f3f2,#e5e0df,#cac5c4,#ada8a8,#8f8b8b" --ordinal --mode light --surface "#eeece6"
  → FAILED — light-end contrast 1.07:1 (warmGray.10 floor, far below 2:1)
$ node scripts/validate_palette.js "#cac5c4,#ada8a8,#8f8b8b,#726e6e,#565151" --ordinal --mode light --surface "#eeece6"
  → FAILED — light-end contrast 1.45:1 (warmGray.20 floor)
```

`warmGray.50` is therefore the floor, exactly the same shape of result v1 found for `teal.50`
— both hues bottom out at their `.50` step on this ground, which is a property of `bone`
(`#eeece6`, a light warm surface), not a coincidence about either hue.

The loud absence block itself (`warmGray.80`, `#3c3838`) sits two steps past this floor,
deliberately: **9.79:1 against bone**, computed by hand (WCAG relative-luminance formula,
same method ART-009 uses) and not merely "clears the mark floor" — it is the single highest-
contrast fill on the entire board apart from ink-on-ground text itself. White text on it
resolves to **11.57:1**. This is the concrete form of "loud, not downplayed": the fill that
means "we did not look here" is more visually assertive than the fill that means "Tier 1,
verified," which is the opposite of v1's hairline hatch and is the whole point of the redesign
(brief; Song & Szafir, see §3).

### 2.5 VSUP — implemented as `color-mix()` of two already-validated tokens, not a new swatch

Correll, Moritz & Heer (CHI 2018) define a Value-Suppressing Uncertainty Palette as a
continuous blend between a value colormap and a neutral grey, controlled by an uncertainty
parameter. This board implements that literally in CSS:

```css
color-mix(in srgb, var(--teal-90) 55%, var(--tier-mix) 45%)
```

Every VSUP swatch is therefore a browser-computed function of two named custom properties,
each of which resolves to a real token (`teal.50/70/90`, `coolGray.50` as the blend target —
never rendered as its own swatch, only ever as a mixing partner). Nothing is a hard-coded new
hex. To confirm the computed result is not accidentally low-contrast or hue-drifted, the
6 High/Medium combinations were computed by hand (linear sRGB weighted average, matching
`color-mix(in srgb, …)` semantics) and run through the same validator used for every other
ramp on this board:

```
High confidence (pure): #009d9a (Weak) · #005d5d (Adequate) · #022b30 (Strong)
Medium confidence (55% value + 45% coolGray.50): #3d9698 (Weak) · #3d7377 (Adequate) · #3e575e (Strong)

$ node validate_palette.js "#009d9a,#005d5d,#022b30" --ordinal --mode light --surface "#eeece6"
  → ALL CHECKS PASS (light-end #009d9a at 2.83:1)
$ node validate_palette.js "#3d9698,#3d7377,#3e575e" --ordinal --mode light --surface "#eeece6"
  → ALL CHECKS PASS (light-end #3d9698 at 2.96:1)
```

Both triads re-pass on the raised white surface too (`#ffffff`): 3.34:1 and 3.49:1 at the
light end respectively. **Deliberate convergence, not a defect:** the three Medium-confidence
swatches (`#3d9698`, `#3d7377`, `#3e575e`) sit far closer together in hue and lightness than
the three High-confidence ones — that convergence toward indistinguishability *is* the VSUP
mechanism. A Medium-confidence "Strong" cannot be told apart from a Medium-confidence "Weak"
as easily as their High-confidence counterparts can, which is the intended effect: a weakly
evidenced rating is *not allowed to look as informative* as a strongly evidenced one. Every
cell also carries a direct two-letter label (`S·H`, `W·M`, …) beneath the swatch, so no
reading depends on discriminating the colour alone (`anti-patterns.md` § Direct labels
mandatory, cited by ART-013 v1 §7 and re-applied here).

### 2.6 Contrast — the caption-ink defect class, checked again on purpose

This agent has been told twice before that a caption-ink pairing was miscleared. Checked
again rather than assumed clear:

| Role | Token | On bone | On white | Used as |
|---|---|---|---|---|
| Primary text | `palette.ink.default` | 15.95:1 | 18.84:1 | body, headings |
| Secondary text | `palette.gray.70` | 6.61:1 | 7.81:1 | `.ink-2` |
| Caption ink | `palette.warmGray.70` | 6.60:1 | 7.80:1 | `.cap`, captions, sources |
| White text on the loud block | `palette.white.default` on `warmGray.80` | 11.57:1 | — | gap-row labels, gap-cell glyphs |

No text is ever rendered on top of a VSUP swatch or a sequential gap-bar fill — every value
label sits **beside** its swatch in plain ink (§2.5, §2.4), which is the specific mitigation
this class of defect needs: **white text directly inside `weak-hi` (`#009d9a`) or
`weak-med` (`#3d9698`) would fail AA at 3.34:1 and 3.49:1 respectively** — checked and
rejected during construction, before it could become a third instance of the same defect,
not caught afterward.

---

## 3. Song & Szafir (IEEE VIS 2018) — fetched and read in full, not summarised from the brief

The brief asked this agent to verify the paper itself and say so if it disagreed. It was
fetched (`https://cmci.colorado.edu/visualab/papers/song_VIS_2018.pdf`, 11 pages, extracted
to text via PyMuPDF since no `pdftotext`/poppler was available in this environment) and read
end to end, including the two results tables the brief's summary does not surface.

**What holds.** "Encodings that HIGHLIGHT missing values ... scored highest on perceived data
quality" is the least-qualified finding in the paper — it is the first bullet of the paper's
own Discussion section, un-hedged. This board's central move — full-opacity, full-footprint
absence blocks instead of a faint hairline hatch — is a direct application of this result and
survives the check completely.

**What does not hold at the stated strength**, checked line by line against the PDF (Tables
1–4 and §5.2/§6.2 Synthesis):

1. **"Alpha-blending scores lower."** False as a blanket claim. The paper's own **gradient
   bars** condition is alpha-blended and is explicitly categorised by the authors as a
   *downplay* technique — yet it scored **consistently high** on perceived data quality in
   the bar-chart experiment (Table 3: µ=4.71, tied with color bars; Table 4: among the
   highest). The authors' own words: *"gradient bars, which also downplay imputed values,
   led to consistently high perceived data quality"* — flagged as a partial contradiction of
   their own H2, not folded quietly into the highlight/downplay binary.
2. **"Information removal scored lowest of every condition."** False in 2 of the paper's 4
   sub-studies. Line-graph trend detection (Table 2): Disconnected Error Bars (an
   *annotation* condition) scored 4.06, below Data Absent's 4.19. Bar-graph trend detection
   (Table 4): Points with Error Bars (also *annotation*) scored 4.03, below Data Absent's
   4.18. Removal was consistently **low** — never the best — but not always the single worst.
3. **"Encodings that break visual continuity caused measurably wrong answers, not merely
   worse perception."** Overstated. Visualisation type had a *statistically significant*
   effect on accuracy in exactly **one** of the four sub-studies (bar-graph averaging, Table
   3, F(6,73)=3.91, p<.0007). Line-graph accuracy showed **no significant effect of
   visualisation type at all**, in either averaging or trend detection — the paper says so
   directly ("We did not find any significant effects of our independent variables on trend
   detection accuracy," §5.1.2). Even in the one significant case, the worst performer for
   *accuracy* was Dashed Outline Bars (a downplay condition, 75.35%), not Data Absent
   (76.37%, actually higher). The paper's own Discussion calls the mechanism — reduced
   "visual weight" causing mis-grouping during aggregation — a hypothesis: *"Future testing
   is needed to verify this hypothesis"* (§6.2). It is not an established causal result, and
   it does not single out information removal as the culprit.
4. **Domain mismatch, unremarked in the brief.** The study concerns *imputed points in
   continuous time-series charts* — 60-point line/bar graphs of simulated Tweet counts, with
   values estimated by zero-filling, linear interpolation, or marginal means. This board has
   no continuous series and performs no imputation anywhere; D-001 forbids inventing a
   plausible value for a gap. The transfer to a categorical, tabular absence (a whole row or
   cell that was never measured) is by analogy — highlight vs. downplay vs. removal as a
   *design posture* — not a literal replication of the tested conditions. Worth stating
   because the paper's own authors limit their claims to "a simple domain and relatively
   smooth signals" and ask for further testing before generalising (§7.1).

**What this board actually acted on, net of the corrections:** the paper's own explanation for
its results is about **visual weight** — opacity and footprint — more than about colour per
se ("our lowest performing conditions ... reduce or remove the weight of imputed" marks,
§6.2). That is the literal design instruction this board followed: the gap blocks keep full
opacity and the row's full footprint (never thinned, never alpha-blended, never removed),
which is the one claim in the paper that survives every qualification above.

---

## 4. Every figure, and where it traces to

Unchanged figures are not re-derived a second time; only the traceability is re-stated because
the rendering changed. New arithmetic (the ten gap percentages, recomputed directly rather
than inherited from v1's rounding) is shown so it can be re-run by hand.

| Figure on the board | Value | Traces to |
|---|---|---|
| Hero: profiled / never / prior-art | 6 / 8 / 2 | `ART-011 § Coverage`, `D-001`, `D-002` — unchanged from v1 |
| 5 secondary KPIs | 12.7%, 24.5%, 33%, 2/5, 0 | `ART-011 § Evidence reached`, `§ Scoreboard` — unchanged from v1 |
| F-01 disclaimer table | 86/48/28/113/275 and 99/55/35/141/330 | `ART-011 § Arithmetic defects` — unchanged from v1 |
| The fourteen — 14 row states, 6 tier chips | verbatim | `ART-011 § Coverage`, `§ Evidence reached · Tier reached per competitor` |
| Load-bearing row — 6 cells (No/No/Yes/Unknown×3) | verbatim | `ART-012 § The load-bearing row` |
| Cluster gap counts (10) | 10/42, 19/60, 15/48, 2/12, 23/42, 19/30, 17/30, 12/18, 8/18, 16/30 | `ART-012 § The feature matrix` — same ten counts v1 used |
| Cluster gap % (10, **recomputed**) | 23.8, 31.7, 31.3, 16.7, 54.8, 63.3, 56.7, 66.7, 44.4, 23.8→ see note | Unknown/total per cluster, computed directly here, not by subtracting v1's rounded "% evidenced" figures — avoids compounding a second rounding step. Cross-check: the ten Unknown counts sum to 10+19+15+2+23+19+17+12+8+16 = **141**, matching `ART-011`'s independently-stated total exactly |
| Journey grid (48 cells) | verbatim | `ART-012 § The journey comparison` |
| Scoreboard (5 rows) | verbatim | `ART-011 § Prior claims`, `§ Scoreboard` |

---

## 5. Form — clutter measurements, section count, and the two-disclosure-level rule

**Word count**, measured by stripping tags and counting tokens, same method applied to v1 for
comparability:

| | v1 | v2 |
|---|---|---|
| Visible words (no click needed) | 2,649 | **1,156** (−56%) |
| Words including collapsed disclosures | 2,649 (v1 had no disclosure mechanism) | 2,023 |
| Footnote-style markers | 56 (†‡§¶* resolving to a block below the table) | 6 (`<details class="note">`, inline, at point of use) |
| Top-level sections (`<h2>`) | 13 | 6, plus the hero/KPI block (no `<h2>`, it is the entry point) and the collapsed Meta appendix — **8 reading blocks total**, matching the census median Bach's own count method would produce |
| `<script>` tags | 0 | 0 |

**Two disclosure levels, held exactly:** level 1 is the rendered page — hero, KPIs,
disclaimer, the fourteen, the load-bearing row, the cluster gap chart, the journey grid, the
scoreboard, all unclicked. Level 2 is `<details>` — either a short `[+ evidence]` note beside
a specific claim (6 of them, replacing v1's 56 footnotes) or the single collapsed **Meta**
appendix at the end (brief corrections, "what this board does not do," assumptions, gaps,
claim format). Nothing sits at a third level; nothing inside a `<details>` is itself
collapsible.

**Nothing load-bearing lives behind a click**, checked against the brief's own named list:
the 8 blanks (the fourteen table, always rendered, never hidden), the F-01 arithmetic defect
(the disclaimer table, fully visible, its two footnote-length elaborations are the only thing
behind `[+ evidence]`), and the 3 unsettled designated tests (the scoreboard, fully visible).
Verified directly: `grep` for `<details` shows every occurrence either inside `class="note"`
(elaboration only) or the one `class="meta"` (assumptions/gaps/corrections, none of which is a
data value asserted nowhere else).

**Interaction is audit, not exploration** — no sort control, no filter, no show/hide. The two
sort decisions on the page (the fourteen keep ART-011's own order; the cluster gap chart is
sorted worst-first) are stated in prose next to the object they order, per the brief's own
rule that sort order is an editorial decision, not a control.

**Print.** `@media print` rules force every `<details>` body to `display: block !important`
and hide the disclosure toggles, so a printed or PDF-exported copy of this page carries
everything, including the Meta appendix, with zero clicks — checked by reading the CSS rules
directly (`details.note .body { display: block !important; }`, `.meta > *:not(summary) {
display: block !important; }`); a live print-preview render was not captured this session (see
§9).

---

## 6. Type and colour discipline

**Four sizes** (`--fz-display` 3.875rem/typography.size.07, `--fz-h2` 1.75rem/size.05,
`--fz-sm` 0.875rem/size.02, `--fz-cap` 0.75rem/size.01) **and two weights** (400, 700) —
v1 used six-ish sizes (`f01`…`f06`) and three weights (400/600/700) with nothing standing out
as the single largest thing on the page. `--fz-display` is used exactly **once**, on the hero
figure (`6/14`), which is by construction the largest element on the board — checked visually
in the rendered screenshot (§8), not merely asserted from the CSS. Section headers and the
five secondary KPI values share `--fz-h2`; everything else — prose, tables, legends, captions
— is `--fz-sm` or `--fz-cap`. Weight, not a third size, carries the KPI/heading distinction.

**Colour never encodes panel identity** — every `background: var(--raised)` card (KPI strip,
disclaimer, spotlight cells) is the same white layer; only the four data-bearing hues from
§2.2 vary, and each is bound to exactly one job.

**On-token, checked mechanically, not by eye.** Every `rem` literal in the file was extracted
and checked against `design-system/tokens/tokens.json`'s spacing scale (0.125–10rem) and
typography size/tracking scale. Five off-token decorative sizes introduced in an early draft
(`0.6rem`/`1.2rem` in the prior-art stripe pattern, `0.7rem`/`0.8rem` on swatch dimensions,
and a `0.625rem` VSUP cell label) were found and corrected to the nearest exact token
(`--s03`/`--s05`/`--s04`/`--fz-cap`) **before** this file was written, not after — the same
"attack your own result" standard the session protocol asks a second agent to apply, applied
here to a first pass of my own construction. The remaining non-token `rem` values are all
structural layout widths (`max-width`, fixed grid-template-columns), the same category v1 used
freely (its own `17rem` row-label column, `8.5rem` track, `68rem` wrap) — layout dimensions
are not colour or component-size primitives and this repository's token system does not
currently cover them.

---

## 7. Repository audit

```
$ python3 validation/audit-system.py --json
```

**Before** (captured prior to writing any file in this v2 directory):

```
{"blocker": 0, "error": 1, "warning": 4, "info": 6}   verdict FAIL
```

**After** (payload, manifest, validation.md all present; v1's manifest `status` set to
`superseded`; registry rebuilt via `validation/rebuild-registry.py` — 14 artifacts, 10 live):

```
{"blocker": 0, "error": 1, "warning": 4, "info": 6}   verdict FAIL
```

Diffed by `(severity, check, message)`, not by count alone (a match on totals is not proof of
a match on contents):

```
NEW findings introduced by this artifact:     set()
REMOVED findings:                             set()
before findings count: 11   after findings count: 11
before skipped: []   after skipped: []
```

### 7.1 Result

- The one pre-existing **error** (`attestation`, check 5g) is **not attributable to this
  artifact** — it concerns `validation/attestation.json` and the hash of the validators and
  their wiring, none of which this artifact touches, reads, or writes. Reported per the
  brief's own instruction to name it rather than treat a pre-existing FAIL as this agent's
  failure.
- The four pre-existing **warnings** (2 corrections with no check, C-031/C-033; 2 unverified
  load-bearing claims, V-015/V-020; 2 stale-surface warnings) are unrelated to this board's
  subject matter and are unchanged by this write.
- This artifact is expected to introduce **zero new findings** of any severity — it writes
  only under `artifacts/luma-travel/`, touches no validator, no hook, no schema, and mints no
  `[E-nnn]`.

---

## 8. Visual QA — a headless render was actually captured this time

ART-013 v1 §9 recorded a live browser screenshot as **not checked**. This session had Chrome
available (`/Applications/Google Chrome.app`) and used it:

```
$ "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
    --no-sandbox --screenshot=v2-final.png --window-size=1280,10000 file:///…/luma-competitor-coverage-board.html
```

Inspected at 1280px, full page height (~3,604px rendered). Findings from the actual render,
not the source:

- The hero (`6/14`) reads as unambiguously the largest element on the page — confirmed
  visually, not merely by CSS inspection.
- The gap rows (never-evaluated: solid `warmGray.80`; prior-art: the same fill plus a bold
  opaque diagonal stripe) are the most visually assertive rows in the fourteen-row table,
  clearing the "loudest thing on the page apart from the hero" bar the brief set.
- The VSUP journey grid's Medium-confidence cells visibly desaturate toward the High-
  confidence cells' shared neutral, confirming the `color-mix()` values compute as intended
  in an actual browser, not only in the hand-computed sRGB check (§2.5).
- One real defect was caught by this render and fixed before delivery: `.kpi .val` inherited
  `text-align: right` from an unrelated `.val` selector used elsewhere on the page (a class-
  name collision introduced during drafting), producing right-aligned KPI numerals over
  left-aligned labels. Fixed with an explicit `text-align: left` override, re-screenshotted,
  confirmed corrected. Recorded because a defect a render catches and a diff shows fixed is
  the standard this file is trying to hold itself to, not a thing to omit because it was
  caught before anyone else saw it.

Screenshots are not included in this payload (this artifact type does not carry binary
assets); the render was inspected during this session and the one finding above was corrected
in the payload itself.

---

## 9. What was NOT checked — skipped is not passed

- **Dark mode.** No dark theme declared; unchanged scope from v1.
- **`color-mix()` browser support.** Supported in all evergreen browsers since 2023; not
  tested against an older or non-evergreen renderer. If opened in one, the VSUP swatches
  would fall back to the last valid declaration or render unstyled — not verified either way.
- **Print preview**, specifically. The `@media print` CSS was read and reasoned about (§5);
  an actual print-to-PDF render was not captured this session.
- **Keyboard/assistive-technology traversal of the `<details>` elements.** Native HTML
  disclosure widgets are keyboard-operable by default in evergreen browsers; not verified
  with an AT pass.
- **Whether ART-011's recount is itself correct**, and whether the ten cluster Unknown counts
  in `ART-012` are themselves free of transcription error — inherited as entered, same
  scope limit as v1 (A-1).
- **Whether the study's recommendation should proceed.** Explicitly out of scope, stated on
  the board itself ("What this board does not do").

**Skipped is not passed.**

---

## Verdict

Gate B: **pass**. Gate A: **pending a named human**. Status stays `draft`.
