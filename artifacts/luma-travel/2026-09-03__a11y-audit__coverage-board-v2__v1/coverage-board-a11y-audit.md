# Luma competitor coverage board (v2) — WCAG 2.2 AA audit

**Artifact:** ART-015 · **Type:** `a11y-audit` · **Version:** 1 · **Date:** 2026-09-03
**Subject:** ART-014 — `artifacts/luma-travel/2026-09-03__dashboard__batch-3-competitor-coverage__v2/luma-competitor-coverage-board.html`
**Produced by:** `a11y-checker` (`Write` for this directory only; no `Edit`, no `Bash`)
**Rulebook:** WCAG 2.2 AA (4.5:1 normal text, 3:1 large text and non-text UI components/graphical
objects). Every ratio below was computed **by hand** from the `color(srgb …)` values in the
payload's `<style>` block — no script was run; this agent holds no `Bash`.

> **First filter, not the verdict.** A human (Gate A) still reviews ART-014. Nothing here is a
> design decision and nothing in ART-014 was changed to produce this file.

**Headline:** 29 contrast pairs computed (12 text/background, 17 non-text) · **11 semantic
checks** · **4 use-of-colour checks** · **1 motion check** · **46 checks total** · **11
findings** (4 contrast, 7 semantic) · **7 items explicitly UNCHECKED** (zoom/reflow render,
forced-colors render, AT pass, CVD-simulated render, print render — no rendering tool in this
agent's tool set). **Skipped is not passed.**

---

## 0. Method — how every number below can be re-derived

**Relative luminance.** Each channel normalised to 0–1, linearised
(`c/12.92` where `c ≤ 0.03928`, else `((c+0.055)/1.055)^2.4`), combined as
`L = 0.2126R + 0.7152G + 0.0722B`.

**Contrast ratio.** `(L_lighter + 0.05) / (L_darker + 0.05)`.

**`color-mix()` resolution.** ART-014's VSUP ramps use `color-mix(in srgb, A P%, B Q%)`.
`in srgb` interpolates the two operands' **gamma-encoded (non-linear) sRGB channel values**
directly — `result = P·A + (1−P)·B` per channel, in 0–255 space — then that result is treated as
an ordinary colour for luminance purposes. Verified against the three blends the payload declares
(`teal-90/70/50` × `coolGray.50` at 55/45): my independent recomputation reproduces
`#3d9698`, `#3d7377`, `#3e575e` exactly, matching `validation.md` §2.5's own hand-computed hex.
The VSUP colour math in the payload is **correct**; my job below is whether the *resulting*
colours clear WCAG, which is a separate question from whether the blend was computed correctly.

**`opacity` resolution — a second colour-synthesis mechanism the brief named for `color-mix()`
but applies equally here.** `tr.gap .gapnote { opacity: 0.86 }` does not fade only the text —
`opacity` on a CSS box creates a stacking context and composites the **entire element** (its own
background paint *and* its content, already flattened together) against whatever is visually
behind that element, at the given alpha. Two of the fourteen rows (`tr.gap.priorart`) paint a
diagonal two-tone stripe as that element's own background, so the text and the stripe are
flattened together first, and *that* flattened image is then blended 86%/14% against the page
ground (`bone`, nothing else sits between the table and the page background). I got this wrong on
a first pass — my initial instinct was to treat the visible stripe colour as the thing the text
composites against, which is not how CSS `opacity` works — and redid it against the actual
compositing model before writing this file. Worked example, a text pixel (opaque white,
`(255,255,255)`) over the `gap-60` half of the stripe, in a `tr.gap.priorart .gapnote` cell:

```
text pixel, pre-opacity:  white occludes whatever is under it → (255,255,255)
element composite → ground: result = 0.86×255 + 0.14×238(ground R) = 252.6  (≈white, barely moves)
background stripe pixel, pre-opacity: gap-60 (114,110,110)
background → ground:      result = 0.86×114 + 0.14×238 = 131.4  (R); (127.6, 127.6) G,B
```

Both halves of the cell fade toward the page ground, but the **text** (already near-white) barely
moves while the **stripe** lightens substantially — so the ratio *between* them shifts a lot more
than either value shifts on its own. Full derivation and the two resulting ratios are in §1.4/F-01.

---

## 1. Text/background pairs (WCAG 1.4.3 / 1.4.6) — every pair rendered, including passes

No text on this board is large-text-eligible at a ratio anywhere near the 3:1 large-text floor
(the one `--fz-display`/`--fz-h2` use is `ink` at 15.95:1+), so the 4.5:1 normal-text threshold is
applied everywhere below without exception, as `validation.md` §2.6 also chose to do.

| # | Foreground | Background | Ratio | Threshold | Verdict | Where used |
|---|---|---|---|---|---|---|
| T1 | `ink` #041222 (`0.015686 0.070588 0.133333`) | `bone` #eeece6 | **15.95:1** | 4.5:1 | PASS | body text, headings, all default text |
| T2 | `ink` | `white` #ffffff | **18.84:1** | 4.5:1 | PASS | text inside `.card`/`.spot`/`.disclaimer` |
| T3 | `gray.70` (`ink-2`) #525252 | `bone` | **6.61:1** | 4.5:1 | PASS | `.flanking`, `.rowlab .task`, `.vlab`, note bodies |
| T4 | `gray.70` (`ink-2`) | `white` | **7.81:1** | 4.5:1 | PASS | note `.body` text (white background) |
| T5 | `warmGray.70` (`ink-3`, caption ink) #565151 | `bone` | **6.60:1** | 4.5:1 | PASS — confirms the payload's own claim, and clears the specific defect class this agent has shipped twice before (a `warmGray.60` caption at 4.26:1) |
| T6 | `warmGray.70` | `white` | **7.80:1** | 4.5:1 | PASS | `.disclaimer p.cap` |
| T7 | `coral.text` #b03822 | `bone` | **5.17:1** | 4.5:1 | PASS | `[+ evidence]` label colour (rows 3, 6, 9; F-01's rows do not have this element) |
| T8 | `coral.text` | `white` | **6.11:1** | 4.5:1 | PASS | F-01-disclaimer inline note |
| T9 | `white` (`raised`), full opacity | `warmGray.80` (`gap-80`) solid | **11.57:1** | 4.5:1 | PASS — matches the payload's own claimed value exactly | gap-row text, `.gapword`, `.spot.gap`, `tierchip` inside gap rows |
| T10 | `white`, full opacity (`.gapword`, no opacity rule) | `warmGray.60` (`gap-60`) stripe half, `tr.gap.priorart` | **5.03:1** | 4.5:1 | PASS (bold, but not large-text-eligible at 14px; passes on the normal-text floor regardless) | "Kayak" / "Prior-art only" labels |
| T11 | `white` at 86% opacity (`.gapnote`), composited onto `bone` | `warmGray.80` half of the stripe, also composited onto `bone` | **7.64:1** | 4.5:1 | PASS | `.gapnote` text over the darker half of the priorart stripe, and over the solid `gap-80` fill in the six non-priorart gap rows |
| T12 | `white` at 86% opacity (`.gapnote`), composited onto `bone` | `warmGray.60` half of the stripe, also composited onto `bone` | **3.85:1** | 4.5:1 | **FAIL — F-01** | `.gapnote` text, rows 4–5 (Kayak, Skyscanner) only, wherever a glyph falls on the lighter half of the diagonal stripe |
| T13 | `ink-2` at 86% opacity (inherited: a `<details class="note">` nested inside a `tr.gap .gapnote` cell is inside the opacity group too) | `white` at 86% opacity, both composited onto `bone` | **5.48:1** (down from the nominal 7.81:1 at T4) | 4.5:1 | PASS, but flagged — a second, benign instance of the same inherited-opacity mechanism as F-01, in rows 8 and 11 (Airbnb, Trainline), where it happens not to cross the line |
| — | `white` text, if ever placed **inside** a `teal-50`/Weak-High or Weak-Medium VSUP swatch | that swatch | 3.34:1 / 3.49:1 | 4.5:1 | **Confirmed would-FAIL** — independently recomputed and matches the payload's own worked numbers exactly. Correctly **never rendered**: every VSUP label sits beside its swatch in plain `ink-2`, not inside it (verified in the markup — no `<span>` with white text is ever a child of `.vsup`). Recorded because a claim of "checked and rejected during construction" deserves independent confirmation, not just trust. |

**12 rendered text/background pairs checked, 11 pass, 1 fails (F-01).**

---

## 2. Non-text contrast (WCAG 1.4.11) — chips, swatches, bars, matrix cells

| # | Element | Against | Ratio | Threshold | Verdict |
|---|---|---|---|---|---|
| N1 | `coolGray.80` (`tier-1`) chip dot | `bone` | **9.75:1** | 3:1 | PASS |
| N2 | `coolGray.80` chip dot | `white` | **11.52:1** | 3:1 | PASS |
| N3 | `coolGray.60` (`tier-2`) chip dot | `bone` | **4.25:1** | 3:1 | PASS |
| N4 | `teal-50`, pure (Weak, High confidence) | `bone` | **2.83:1** | 3:1 | **FAIL — F-02** |
| N5 | `color-mix(teal-50 55%, coolGray.50 45%)` = `#3d9698` (Weak, Medium) | `bone` | **2.96:1** | 3:1 | **FAIL — F-02** |
| N6 | `teal-70`, pure (Adequate, High) | `bone` | **6.53:1** | 3:1 | PASS |
| N7 | `#3d7377` (Adequate, Medium) | `bone` | **4.53:1** | 3:1 | PASS |
| N8 | `teal-90`, pure (Strong, High) | `bone` | **12.78:1** | 3:1 | PASS |
| N9 | `#3e575e` (Strong, Medium) | `bone` | **6.51:1** | 3:1 | PASS |
| N10 | `warmGray.80` (`gap-80`, the Unknown/absence VSUP swatch) | `bone` | **9.79:1** | 3:1 | PASS — matches the payload's own headline number exactly |
| N11 | `teal-90` (Strong, High) **vs an adjacent** `gap-80` (Unknown) cell in the same row | — | **1.30:1** | n/a (informational — see F-04) | **FLAGGED — F-04** |
| N12 | `teal-50` (Weak, High) **vs an adjacent** `gap-80` (Unknown) cell | — | **3.47:1** | n/a | for comparison — this pairing is fine |
| N13 | Cluster gap-chart bar, `warmGray.50` tone | its own track (`warmGray.20`, `hairline-soft`) | **2.58:1** | 3:1 | **FAIL — F-03** |
| N14 | Cluster gap-chart bar, `warmGray.60` tone | track | **3.85:1** | 3:1 | PASS |
| N15 | Cluster gap-chart bar, `warmGray.70` tone | track | **5.97:1** | 3:1 | PASS |
| N16 | Cluster gap-chart bar, `warmGray.80` tone | track | **8.85:1** | 3:1 | PASS |
| N17 | Cluster gap-chart bar, `warmGray.90` tone | track | **11.66:1** | 3:1 | PASS |

**17 non-text pairs checked, 15 pass, 2 fail outright (F-02, F-03), 1 flagged as a perceptual risk
without being a clean SC failure (F-04).**

Not counted as findings: `hairline` (#c4c4c4, 1.45:1 vs bone) and `hairline-soft` (#e5e0df,
~1.1:1 vs bone) — the row and card divider lines. These sit well under 3:1, but 1.4.11 exempts
"purely decorative" boundaries not required to understand content; every row/card here remains
identifiable by its content and whitespace without the divider line being visible at all, so this
is noted, not filed.

---

## 3. Colour is not the only channel (WCAG 1.4.1)

This is the section the brief flagged as critical, and it is the one place ART-014 is built
carefully. Verified directly against the markup, not assumed from the design's own framing:

- **The three absence states** ("The fourteen" table) — ● Profiled, ◐ Prior-art only,
  ○ Never evaluated — carry a **distinct Unicode glyph**, a **distinct word**
  ("Profiled"/"Prior-art only"/"Never evaluated"), and a **distinct row treatment** (plain
  row / diagonally-striped / solid block). Three independent non-colour channels for three
  states. **Confirmed, PASS.**
- **The load-bearing-row spotlight** (✕/✓/○ + "No"/"Yes"/"Unknown") — no colour differentiates
  Yes from No; both sit in plain `ink` on `white`. Only the Unknown cells get the absence
  treatment, and they get shape + word too. **Confirmed, PASS.**
- **The designated-tests scoreboard** (✓/○/◐ + "Falsified"/"Not tested"/"Not settled"/
  "Unresolved") — same pattern, no hue used for verdict. **Confirmed, PASS.**
- **The VSUP journey grid** — every one of the 48 journey cells and 6 load-bearing cells carries
  a plain-text `.vlab` label (`S·H`, `W·M`, `unk`, …) directly beneath the swatch, in `ink-2`,
  entirely independent of the swatch's own colour. Checked by grep-equivalent read of every
  `<tr>` in `.journey tbody`: **every single cell has one.** A reader who cannot perceive the
  swatch colour at all still gets the full bivariate reading from text alone. **Confirmed, PASS.**
- **Deuteranopia / greyscale, reasoned (not rendered — see §6).** The one place colour-only
  reliance comes closest to mattering is **not** a hue confusion but a **lightness** one: `teal-90`
  (Strong, High — a near-black blue-green) and `gap-80` (Unknown — a near-black neutral) sit only
  1.30:1 apart (N11) and, converted to greyscale, would be close to indistinguishable by shape
  alone. Because every cell also carries its text label, no *information* is lost — but the
  *visual pattern* the VSUP mechanism depends on (glancing at relative "loudness") degrades for
  a low-vision or greyscale-printed reader exactly at the pairing the design most wants to be
  legible (a verified Strong rating sitting next to a total unknown). Filed as **F-04**, severity
  `info`, precisely because the text label saves it — a human should decide whether that's enough.

---

## 4. Semantics — headers, `<details>`, headings, landmarks, lang

| # | Check | Result |
|---|---|---|
| S1 | `<html lang="en">` | **PASS** |
| S2 | Focus order (any `tabindex` overrides?) | **PASS** — none found; the only focusable elements are the 7 native `<details>/<summary>` pairs, in DOM order, matching visual order |
| S3 | Focus visibility (any `outline` removal?) | **PASS** — no `outline: none`/`outline: 0` anywhere in the stylesheet; default focus rings are intact on every `<summary>` |
| S4 | Images / alt text | **N/A** — zero `<img>` elements; all icons are inline Unicode glyphs (●, ◐, ○, ✕, ✓), always paired with a text word per §3 |
| S5 | `<caption>` on the 4 data tables | **FAIL — F-05.** CSS defines `caption { … }` styling (line 121) but no `<table>` in the document actually contains a `<caption>` element, and no `<table>` carries `aria-label`/`aria-labelledby` either. Every table is programmatically nameless. |
| S6 | Row headers (`<th scope="row">`) | **FAIL — F-06.** In all four tables (F-01 disclaimer, "the fourteen," journey grid, scoreboard) the row-identifying cell (competitor name, cluster label, row label) is a plain `<td>`. With no `colspan`/`rowspan` anywhere (confirmed — none used), the browser's implicit header-association algorithm *could* still work for column headers, but it never treats a `<td>` as a row header candidate — a screen-reader user moving cell-by-cell through, say, the journey grid gets no "Expedia:" context read before "Strong, High" the way a `<th scope="row">` would provide. |
| S7 | `scope="col"` on `<thead><th>` | **Minor — F-07.** Absent everywhere. Lower severity than F-06 because the implicit HTML association algorithm generally succeeds for simple column headers in a table with no merged cells, but explicit scope (WCAG technique H63) is the recommended, robust form and costs nothing to add. |
| S8 | `<details>/<summary>` accessible name | **FAIL — F-08.** All 6 `<details class="note">` elements (rows 3, 6, 8, 9, 11 of "the fourteen," plus the F-01 disclaimer note) use `<summary></summary>` — **literally empty**. The visible "[+ evidence]" / "[– evidence]" text exists **only** as CSS `::before` generated content (`details.note summary::before { content: '[+ evidence]'; }`). Current evergreen browsers largely do include generated content in accessible-name computation per the accname spec, but this is a documented fragile pattern (support has been inconsistent historically, and dynamic content changes on `::before` — e.g. the `[open]` state swap to "[– evidence]" — are not guaranteed to be re-announced by every AT). Six interactive controls with **zero real DOM text** is a real risk to 4.1.2 (Name, Role, Value), not merely a style choice. The `.meta` top-level `<details>` (line 509) does **not** have this problem — it has real, visible summary text. |
| S9 | `<h1>` | **FAIL — F-09.** No `<h1>` exists anywhere in the document. The largest visual element (`6/14`, `--fz-display`) is a `<span class="figure">`, not a heading of any level. |
| S10 | Heading order (no skipped levels) | **FAIL — F-10, minor.** Top-level flow is `<h2>` × 5 ("The fourteen" → … → "Designated tests"), then the collapsed `<details class="meta">` (whose `<summary>` is not a heading at all) contains `<h3>` elements directly ("Corrections made to the v2 brief," "What this board does not do," "Assumptions," …) with no `<h2>` wrapping the Meta section in between. This is a level skip (2→3 with no intervening 2), mitigated somewhat by the `<summary>` text itself acting as a de facto section title immediately before it. |
| S11 | Landmarks (`<main>`, `<header>`, `<footer>`) | **Partial — F-11.** `<header>` and `<footer>` are present and correctly placed as direct children of `<body>` (implicit `banner`/`contentinfo`). There is **no `<main>` element** — every substantive section (KPIs, disclaimer, the fourteen, spotlight, cluster chart, journey grid, scoreboard) sits in a bare `<div class="wrap">` with no landmark role at all. |

**11 semantic checks, 4 pass, 7 findings (one of them, S4, is N/A rather than pass/fail).**

---

## 5. Zoom / reflow (WCAG 1.4.10) — UNCHECKED, with a static-analysis risk note

**This agent has no `Bash` and no rendering tool.** 200% zoom, 400% zoom, and the 320×256px
viewport condition were **not rendered and are not claimed to pass.** `dashboard-analyst`'s own
`validation.md` §8 captured a real Chrome headless screenshot at 1280px; it did not test narrow
viewports either, and this agent cannot fill that gap without the same capability.

What a **static CSS read** supports, stated as reasoning, not as a verified result:

- `.kpis` (5 → 2 columns) and `.spotlight` (6 → 3 columns) both use `repeat(n, 1fr)` and have an
  explicit `@media (max-width: 60rem)` fallback. These are very likely to reflow cleanly; **not
  independently confirmed at 320px.**
- The four `<table>` elements have **no responsive treatment** beyond `.journey` shrinking its
  font under the same breakpoint — no card-transform pattern, no per-table horizontal-scroll
  wrapper (`overflow-x: auto` around just the `<table>`). Several columns force `white-space:
  nowrap` (`.n`, `.nw`, every `thead th`). WCAG 1.4.10 explicitly **exempts** "content that
  requires two-dimensional layout for usage or meaning" — a genuine data table is the textbook
  case — so a table needing its own horizontal scroll at 320px is likely **compliant by
  exception**, provided the scroll is local to the table. The risk is that **no local scroll
  wrapper exists**: without `overflow-x` scoped to the `<table>`, a table that overflows 320px
  would widen `.wrap`/`<body>` themselves (neither sets `overflow-x: hidden` nor wraps the table
  in a scrollable container), dragging the surrounding **prose** (which is not exempt) into a
  horizontal-scroll requirement it shouldn't need. **This is a plausible defect based on the CSS
  as written, not a confirmed one** — only a real 320px render settles it.

**Marked UNCHECKED:** 200% zoom, 400% zoom, 320px viewport reflow (3 items).

---

## 6. Motion / `prefers-reduced-motion`

Searched the entire `<style>` block for `transition`, `animation`, `@keyframes`, `transform`:
**none exist anywhere in this file.** The only interactive state change is the native
`<details>`/`<summary>` open/close toggle, which browsers render as an instant, non-animated
attribute flip with no author-supplied transition. **PASS by inapplicability** — there is no
motion for `prefers-reduced-motion` to gate, so its absence is correct, not an omission.

---

## Findings register

| ID | Severity | Section | Finding | Suggested direction (not a fix — that is a human/`dashboard-analyst` call) |
|---|---|---|---|---|
| F-01 | **error** | §1, T12 | `.gapnote` text in the two `tr.gap.priorart` rows (Kayak, Skyscanner) resolves to **3.85:1** against the lighter half of its own diagonal stripe once the element's 86% opacity is correctly composited against the page ground — below the 4.5:1 floor, for roughly half of every glyph in that line, unpredictably by stripe phase. Passes (7.64:1) over the darker half. | Either drop the opacity on this specific text (keep it at 100% like `.gapword` already is, which passes both stripe halves at 5.03/11.57:1) or move the note text off the striped surface. |
| F-02 | **warning** | §2, N4/N5 | The VSUP "Weak" swatches — `teal-50` pure (2.83:1) and its Medium blend `#3d9698` (2.96:1) — both sit under the 3:1 non-text floor against `bone`. Every other rung of the ramp (Adequate, Strong, both confidences) clears 3:1 comfortably; the failure is specific to the lightest step. Mitigated by the redundant `.vlab` text label on every cell. | A human/token-keeper call: raise the floor step, or accept the exemption on the basis that no information depends on the swatch boundary alone. |
| F-03 | **warning** | §2, N13 | The lowest two cluster gap-chart bars (`warmGray.50`, used at 23.8% and 16.7%) sit at 2.58:1 against their own track — under 3:1. Every darker bar tone in the same chart clears 3:1 by a wide margin. Mitigated by the adjacent `%` text label. | Same shape as F-02 — a floor-step decision, not a full-ramp defect. |
| F-04 | **info** | §2 N11, §3 | `teal-90` (Strong, High confidence) and `gap-80` (Unknown) differ by only 1.30:1 in lightness and appear adjacent in the journey grid (e.g. Tripadvisor's "In dest./Return" pair). Not a clean SC failure — every cell carries a redundant text label — but the *visual* legibility of "loud vs. quiet" the VSUP/loud-absence mechanism depends on is weakest exactly at this pairing, for greyscale or low-vision readers. |Recommend a rendered CVD/greyscale check before Gate A signs off on the journey grid specifically. |
| F-05 | **warning** | §4 S5 | No `<caption>` (or `aria-label`/`aria-labelledby`) on any of the 4 data tables; all four are programmatically nameless. | Add a one-line `<caption>` per table — several already have adjacent `<p class="cap">` prose that could be linked via `aria-describedby` instead if a visible caption is undesired. |
| F-06 | **warning** | §4 S6 | Row-identifying cells are `<td>`, not `<th scope="row">`, in all four tables. | Promote the competitor/cluster/row-label column to `<th scope="row">`. |
| F-07 | **info** | §4 S7 | No explicit `scope="col"` on any `<thead><th>`. | Low-cost addition; implicit association likely already works given no merged cells. |
| F-08 | **error** | §4 S8 | 6 of 7 `<details>` disclosure controls have an empty `<summary></summary>`; their entire visible/accessible label is CSS `::before` content, a documented-fragile accessible-naming pattern, especially across the `[open]` state change. | Put real (even visually-hidden-via-clip, not `display:none`) text inside `<summary>`; keep the `::before` glyph as decoration only. |
| F-09 | **warning** | §4 S9 | No `<h1>` anywhere in the document. | Give the page (or at minimum the hero "6/14 competitors profiled") a real `<h1>`. |
| F-10 | **info** | §4 S10 | Heading order skips from the last `<h2>` to `<h3>` with no intervening `<h2>` for the collapsed Meta section. | Either promote "Meta" itself to an `<h2>` (visually hidden if needed) or demote the interior headings to match the true nesting depth. |
| F-11 | **warning** | §4 S11 | No `<main>` landmark; all substantive content sits in an unlabelled `<div class="wrap">`. | Wrap the body content (between `<header>` and `<footer>`) in `<main>`. |

**11 findings: 2 error, 5 warning, 4 info.**

---

## What was NOT checked — skipped is not passed

1. **200% zoom render** — no rendering tool in this agent's tool set. UNCHECKED.
2. **400% zoom render** — same reason. UNCHECKED.
3. **320px viewport reflow** — same reason; §5 gives a reasoned, unverified risk note instead of a
   verdict. UNCHECKED.
4. **An actual assistive-technology pass** (VoiceOver, NVDA or JAWS reading the page, especially
   the 7 `<details>` controls and the 4 tables) — reasoned from spec/known browser behaviour in
   §4, never run against a live AT. UNCHECKED.
5. **Forced-colors / Windows High Contrast Mode render** — forced-colors mode typically strips
   `background-image` and custom `background-color`, which would remove the priorart diagonal
   stripe and the solid gap blocks entirely, leaving only glyph + word to carry the three absence
   states (which, per §3, is sufficient) — reasoned, not rendered. UNCHECKED.
6. **An actual CVD-simulated (deuteranopia/protanopia/tritanopia) render** — F-04 is reasoned from
   luminance-and-hue proximity math, not from a simulated filter. UNCHECKED.
7. **Print-to-PDF render** — `dashboard-analyst`'s own `validation.md` §5 already records this as
   not captured; independently confirmed still open, not re-attempted here (same tool gap).
   UNCHECKED.

**7 items explicitly unchecked.**

---

## Assumptions

- **A-1.** `color-mix(in srgb, …)` resolves as gamma-space linear interpolation of the two
  operands' sRGB channel values, per the CSS Color 4 `in srgb` interpolation-space definition.
  Cross-checked against the three hex values `validation.md` §2.5 hand-computed independently —
  all three matched exactly, which is the basis for trusting this model for the swatches that
  were *not* independently hex-checked in that file.
- **A-2.** CSS `opacity` composites the whole element (background + content, pre-flattened)
  against the nearest painted surface behind it in paint order, per the CSS Compositing and
  Blending spec's stacking-context behaviour for `opacity < 1`. No intervening element paints
  between the audited `<td>`s and the page `bone` background, so the ground for that composite is
  `bone` throughout.
- **A-3.** "Large text" thresholds (3:1) were not applied to any pairing in §1, because no
  borderline pairing in this document is close enough to either threshold for the distinction to
  matter — every text pair is either comfortably above 4.5:1 or, in the one case that fails
  (F-01), fails a threshold well below what large text would even require.
- **A-4.** Where `validation.md`'s own stated ratios could be independently reproduced (T1, T2,
  T3, T4 minus the exact caption pairing, T5, T6, T9, N10, and the three `color-mix()` hex
  outputs), they matched to the stated precision. This audit does not re-state those as new
  findings — it confirms them and moves on to the pairs the source file did not enumerate.

---

## Boundaries observed

- Nothing outside this artifact directory was written. ART-014's payload, `design-system/tokens/`,
  and `validation/` were only read.
- This is a **first filter in Phase 4, not a verdict.** F-02, F-03 and F-04 in particular are
  framed as decisions for a human (and, where a token value is implicated, `token-keeper`) —
  this agent names the measured gap and stops there.
- `validation/audit-system.py` was not run; that is the orchestrator's or Gate B's job, not this
  agent's.
