# a11y audit — ART-026 v2, chart layer (ADR-021 item 4)

**Artifact under audit:** `luma-competitor-research-findings.html` (2,228 lines)
**Generator:** `build-dashboard.py` + `charts.py` (same directory)
**Auditor:** a11y-checker · Gate B · first filter, not the verdict (Gate A / human review still required)
**Scope:** WCAG 2.2 AA, concentrating on the six chart figures added in v2 (`ch-coverage`,
`ch-effort`, `ch-themes`, `ch-confidence`, `ch-matrix`, `ch-nulls`), per ADR-021 item 4. Contrast
(marks ≥3:1, axis/cell text ≥4.5:1) is **not** re-checked here — `verify-encoding.py` and
`verify-charts.mjs` already pass it with exact figures (201 marks, worst 4.25:1; 59 matrix
numbers, worst 5.02:1; 0 clipped text; 203 declared structural exemptions). This audit reads code,
not a rendered browser — every item below is graded PASS / FAIL / **NOT TESTABLE WITHOUT A
BROWSER**, and NOT TESTABLE is reported explicitly rather than folded into a pass.

I hold Write only for this file. Nothing else was touched.

---

## Verdict by success criterion

| SC | Verdict | Basis |
|---|---|---|
| 1.1.1 Non-text Content | **PARTIAL FAIL** | 5 of 6 charts pass; `ch-matrix`'s alt text omits cell-level detail (W-1); `ch-nulls` buries real prose inside a pruned `role="img"` subtree (E-1) |
| 1.4.1 Use of Colour | **PASS** | Verified directly in the emitted SVG/CSS — see below |
| 1.3.1 Info and Relationships | **FAIL** | Heading-level skips, a mis-scoped `role="img"`, and a headingless top-level section — all quoted below |
| 1.4.10 Reflow | **PASS (static analysis only)** | rem-based layout, chart overflow correctly contained; not confirmed in a live viewport |
| 1.4.4 Resize Text | **PASS (static analysis only)** | rem/viewBox scaling throughout; not confirmed at 200%/400% zoom |
| 2.1.1 Keyboard | **PASS**, one INFO gap | Panel system verified correct from source; chart-body scroll region has no keyboard path (no information loss — see I-2) |
| 2.4.3 Focus Order | **PASS** | Verified from source: open moves focus in, Escape returns it, DOM order matches visual order |
| 2.4.6 Headings and Labels | **FAIL** | Four distinct, concrete defects (F-2 through F-5 below) |
| 1.4.12 Text Spacing | **NOT TESTABLE WITHOUT A BROWSER** | SVG chart text is arguably out of 1.4.12's scope (graphic text), but dense fixed-pixel layout is a real clipping risk under a forced spacing override — flagged, not resolved |

---

## Findings, ranked

### E-1 — error — `ch-nulls` — SC 1.3.1 Info and Relationships / 4.1.2 Name, Role, Value

`figure()` in `charts.py` wraps a `role="img"` div around `{svg}`, and `chart_nulls()` passes
`chart + side` as that `{svg}` argument — i.e. the `.nullwrap` block (two `.nullblock` divs
containing real prose, a bold lead-in, and a `<code>[F-69]</code>` citation) is rendered **inside**
the same `role="img"` container as the route-diagram SVG, not beside it. Confirmed in the rendered
HTML (`ch-nulls`, chart-body div):

```html
<div class="chart-body" role="img" aria-labelledby="ch-nulls-t" aria-describedby="ch-nulls-d">
  ...
  <svg ...>...</svg><div class="nullwrap"><div class="nullblock">...
    <span class="cap">— Booking.com Genius (F-02) · Expedia One Key (F-18) · ...</span>
  </div>...<code>[F-69]</code>...</div>
</div>
```

`role="img"` is a leaf role: assistive technology is expected to treat everything inside it as a
single image and expose only the label/description, pruning the actual descendant DOM. The
`.nullwrap` content is **not chart anatomy** by ADR-021's own dividing rule ("a separate element…
that reads as a number… is an ordinary component," not something "drawn by the chart's own
rendering logic") — it is KPI-tile-like text, indistinguishable in kind from other cards on this
board that are correctly left outside any `role="img"`. Placing it inside the image role hides
real, selectable prose from anyone using a screen reader, even though the board explicitly
advertises that its text is "selectable text… select, copy, paste into a spreadsheet." The
`ch-nulls-d` paraphrase does cover the same *numbers* (0/4 loyalty mentions, 11 vs 0 sort axes),
so no number is lost — but the framing prose and the `[F-69]` citation are.

**Fix:** move `.nullwrap` outside the `role="img"` div (e.g. as a sibling `<div>` between the
chart body and `chart-desc`, or fold into `chart-note`).

### F-2 — error — Document-wide (`ch-coverage`, `ch-effort`, `ch-nulls`) — SC 2.4.6 / 1.3.1

Every section that opens with a chart jumps from `<h2>` straight to the chart's `<h4>`
(`figure()` → `figcaption` → `<h4>{title}</h4>`), with no `<h3>` in between:

```html
<section id="coverage"><h2>Coverage — read this before anything else on this board</h2>
  ...
  <figure class="chart" id="ch-coverage"><figcaption class="chart-head"><h4>How much of the plan was actually captured</h4>
```

The same pattern repeats for `<h2>Shape of the evidence</h2>` → `<h4>Where we looked…</h4>`
(`ch-effort`) and `<h2>Findings</h2>` → `<h4>Looking for the help a stranded passenger needs</h4>`
(`ch-nulls`). A screen-reader user navigating by heading level (NVDA/JAWS "3", VoiceOver rotor)
will not find an `<h3>` for these charts and has no structural cue that a level was skipped rather
than that content is missing.

### F-3 — warning — `section#coverage` — SC 1.3.1

`.coveragewarn` nests a second `<h2>` inside the section that already has one:

```html
<section id="coverage"><h2>Coverage — read this before anything else on this board</h2>
  <div class="coveragewarn"><h2>No competitor is complete. All 17 touched; none exhausted.</h2>
```

This is a callout, not a new top-level section, but it reads as one in a heading-level list.

### F-4 — warning — Document-wide (~190 card titles) — SC 2.4.6 / 1.3.1

Every finding/pain-point/insight/recommendation/next-step/method-note **card title** is an
`<h3 class="card__title">`, and every **group heading** it sits under (`<h3 class="subhead"
id="find-market">`, `id="find-effort">`, etc.) is *also* an `<h3>`. Group and item are two
different conceptual levels rendered at one heading level, throughout the whole document — not a
skip, but a flattening that removes the main benefit of heading-based navigation on a
document this size (188 interactive detail panels' worth of headings, all at the same level).

### F-5 — warning — `<details id="meta">` — SC 2.4.6 / 1.3.1

The left-rail nav has one link per top-level section, and eight of nine resolve to a real
`<h2>` (`#coverage`, `#shape`, `#findings`, `#painpoints`, `#insights`, `#recommendations`,
`#nextsteps`, `#methodnotes` — note `#methodnotes` **is** a proper `<section><h2>`, distinct from
this item). The ninth, `<a href="#meta">Meta</a>`, resolves to `<details class="meta" id="meta">`,
whose only text at the top is a `<summary>` — not a heading element — and whose internal content
starts directly at `<h3>Sources</h3>`. A screen-reader user browsing by heading will find no "Meta"
entry at the same level as its eight siblings, and will find "Sources" etc. sitting at the same
`<h3>` level as ordinary card titles (F-4), one level too shallow for what is actually a top-level
section.

### W-1 — warning — `ch-matrix` — SC 1.1.1 Non-text Content

`ch-matrix-d` states row totals ("TripIt 3; American Airlines 4; … Kayak 18; … Skyscanner 3") and
the "59 of 198 cells" summary, but does not reproduce the 59 individual competitor×theme values a
sighted reader reads directly off the grid (e.g. Kayak / Ranking & comparison = 7). The full 18×11
grid does exist, verbatim, in the "Competitor × theme matrix — 18 rows, CSV" `<details
class="csvbox">` block later in the same section (`section#shape`) — but nothing connects the two:
no cross-reference in the alt text, no shared `aria-describedby`, not even a "full data below"
note. A screen-reader user has no way to discover, from the chart itself, that the complete data
exists a few elements later. **This is the one place in the six charts where "genuinely
equivalent" (item 1's test) does not hold** — the sighted reader gets 59 exact numbers, the
non-sighted reader gets 18 sums.

### I-2 — info — All 6 charts — SC 2.1.1 Keyboard

`.chart-body { overflow-x: auto }` plus `.c-svg { min-width: 30rem }` (26rem for
`.c-svg-narrow`) creates a horizontally-scrollable region with **no `tabindex`**, so a
keyboard-only user cannot scroll the SVG into view (no arrow-key/Page-key path, mouse or trackpad
drag only). The three `.csvbox` blocks got this right — `<pre class="csv" tabindex="0"
aria-label="…">` — the chart-body divs did not. Not a WCAG failure here specifically, because
every number is already present in the always-visible `aria-describedby` paragraph regardless of
scroll position (except the W-1 gap above), but it is an inconsistency in the same file worth
fixing the same way.

### I-3 — info — Coverage bullet chart bands — SC 1.4.1 (observation, not a fail)

The three "qualitative range" background bands (0–33% / 33–66% / 66–100%) in `ch-coverage` are
distinguished from each other only by a very close gray-shade step (`gray.10`/`gray.20`/`gray.30`
— visually subtle), with no border or tick mark at the 33%/66% boundaries. This is not a 1.4.1
failure because (a) the bands are decorative context, not data — the actual value is the dark bar
+ printed "`n` of `d`" + percentage, none of which depend on perceiving the bands — and (b)
`ch-coverage-d` explicitly states the band ranges in words ("The three background bands are
0–33%, 33–66% and 66–100%"). Recorded so a low-vision reader's likely difficulty telling the
bands apart isn't mistaken for an unreported gap.

### I-4 — info — All 6 `<svg>` elements — SC 1.3.1 / 4.1.2, NOT TESTABLE WITHOUT A BROWSER

No `<svg>` carries `aria-hidden="true"` or `focusable="false"`; the text-alternative pattern
relies entirely on the ancestor `<div role="img">` being treated as a leaf/pruned node by the
accessibility tree, which is the ARIA-spec-correct behaviour and passes in mainstream
browser/AT pairings — but it is genuinely unverified here. **Settle with:** NVDA+Chrome,
JAWS+Chrome, VoiceOver+Safari, each tabbing to a chart and confirming (a) only the label +
description are announced, and (b) none of the individual `<text>` marks inside the SVG (axis
labels, matrix cell numbers, dot-matrix legend) are separately exposed or separately focusable.

### NT-1 — NOT TESTABLE WITHOUT A BROWSER — 1.4.10 Reflow / 1.4.4 Resize

Static analysis supports a PASS: all typographic sizing is in `rem`/`ch`, the shell grid drops to
a single column with the rail collapsing to a horizontal strip at `max-width: 68rem` (well above
the 320 CSS px reflow target), and every chart's horizontal overflow is deliberately contained to
`.chart-body` (the WCAG-sanctioned exception for "content that requires two-dimensional layout for
usage or meaning," e.g. a data table or a matrix — same exception a data table gets). No fixed-px
containers were found outside the SVGs themselves. **Not confirmed:** actual rendering at a 320
CSS px viewport and at 400% zoom on a 1280px viewport, per the two equivalent 1.4.10 techniques.
Recommend a live check before Gate A sign-off, specifically of `ch-matrix` (the widest chart,
716px viewBox) and the `.panel`/`.rail` interaction at the 68rem breakpoint.

### NT-2 — NOT TESTABLE WITHOUT A BROWSER — 1.4.12 Text Spacing

Chart text is set as fixed-pixel SVG `<text>` (11–13px; matrix cell text specifically is 11px
inside a 40×23px cell) rather than reflowable HTML text — SVG text of this kind is generally
understood to sit outside 1.4.12's scope (the SC explicitly excludes captions and text that is
part of an image/graphic, and SVG chart marks are the closest analogue). Flagged anyway because a
user-stylesheet override that forces spacing indiscriminately (the standard 1.4.12 test technique)
could, in principle, push a two-digit matrix cell number past its 40×23px cell boundary and into a
neighbour, since the layout is fixed-position and does not reflow. Genuinely requires a browser
with a text-spacing bookmarklet/extension to settle — not resolved here.

---

## Confirmed PASSES (with the evidence, not just the claim)

**P-1 — `ch-nulls` route encoding — SC 1.4.1.** Dead-end vs. arriving routes are distinguished on
four independent channels, never colour: a solid line to the stop point (`.c-route`, gray.100) +
perpendicular stop-tick (`.c-stop`) + dashed continuation (`.c-nevert`, gray.60,
`stroke-dasharray:3 6`) + the word "DEAD END", versus one unbroken solid line + an arrowhead
polygon + the word "ARRIVES" — and both words are rendered in the identical `--ink` fill. Verified
directly in the generated SVG and the `chart_css()` source, not inferred from the description.

**P-2 — `ch-confidence` / `ch-matrix` — SC 1.4.1.** Three confidence classes render as three
distinct shapes (filled circle / filled square / struck-through open circle) plus a text legend;
every non-zero matrix cell prints its own count in text, contrast-checked per shade by
`Ladder.text_on()`. Exactly what ADR-021 item 2 requires, confirmed in the emitted markup.

**P-3 — Shared detail-panel keyboard/focus system (188 triggers + 3 CSV blocks) — SC 2.1.1 /
2.4.3.** Read directly from `build-dashboard.py`'s embedded script (not the rendered HTML, whose
data blob is too large for this tool to load): every `[data-detail]` trigger is
`tabindex="0" role="button"` and opens on `Enter`/`Space` as well as click; `openPanel()` sets
`aria-expanded="true"` on the active trigger and forces every other open trigger back to `false`;
focus moves into the panel (`panel.focus()`, panel has `tabindex="-1"`); `Escape` calls
`closePanel()`, which returns focus to the original trigger (`lastTrigger.focus()`). No focus trap
— consistent with the panel's own documented "not a modal" design. This is the correct
disclosure-widget pattern and it is what's actually shipped, not merely declared in a comment.

---

## What I could not test, and why (skipped ≠ passed)

- **Real AT behaviour** for all six `role="img"` charts (I-4) — needs NVDA/JAWS/VoiceOver, not
  code reading.
- **320 CSS px reflow and 200%/400% zoom** (NT-1) — needs a live viewport.
- **Text-spacing override rendering inside dense SVG cells** (NT-2) — needs a browser + a
  spacing-override tool.
- **The embedded `<script type="application/json" id="panel-data">` blob and the live rendered
  `<script>` block** in the HTML itself were not read from the rendered file — a single line
  ~40,000+ tokens long, past this tool's per-call limit. I instead read the equivalent,
  unminified source in `build-dashboard.py` (quoted under P-3), which the file's own footer states
  is the authoritative generator ("Regenerate this file with `build-dashboard.py` beside it").
  That covers the interaction logic; it does **not** let me confirm the *rendered* file's script
  matches the generator byte-for-byte — recommend re-running `build-dashboard.py` and diffing, or
  a live check, before treating P-3 as proven of the shipped artifact rather than of its source.
- **Print stylesheet behaviour** (`@media print`) was reviewed statically (min-widths cleared,
  `.chart-body{overflow-x:visible}`, `<details class="meta">` forced open via
  `beforeprint`/`afterprint`) and looks correct, but was not rendered to a printer/PDF to confirm.

---

## Summary for Gate A

Two governance-relevant defects (E-1, F-2 through F-5) are real and fixable without touching
contrast or the encoding contract, both already-passing per `verify-charts.mjs`. One genuine
content-equivalence gap (W-1) exists in `ch-matrix` between what a sighted reader sees and what a
screen-reader user is told. Everything ADR-021 specifically asked this audit to check beyond
contrast — colour-never-sole-channel (1.4.1), the route diagram's dual-encoding (1.4.1), and the
keyboard/focus system behind the 188 detail panels (2.1.1/2.4.3) — passed, with the source-level
evidence quoted above rather than asserted. This board should not be treated as fully cleared on
accessibility until a human confirms the items marked NOT TESTABLE WITHOUT A BROWSER; that
confirmation is Gate A's job, not mine.
