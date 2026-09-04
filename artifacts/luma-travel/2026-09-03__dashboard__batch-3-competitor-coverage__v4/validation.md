# Validation — ART-021 · dashboard · batch-3-competitor-coverage · v4

**Payload:** `luma-competitor-coverage-board.html` · **Produced by:** `dashboard-analyst` ·
**Date:** 2026-09-03 · **Status:** draft · **Gate:** B (automated) · **Supersedes:** `ART-016` (v3)

v4 is a rebuild, not a fix pass. The owner's verdict on v3 was structural — *"still UI bad — I
want more data visualization graphics, design, navigation and progressive disclosure"* — so this
version changes what kind of object the page is, not which numbers are wrong on it. Content
inputs are unchanged: `ART-011` (coverage reconciliation) and `ART-012` (market findings, capped
by ART-011). `research/sources/` was not opened — same restriction as v1–v3.

---

## 0. Read first — a correction to this dispatch's own brief

The brief states ADR-021 is *"just accepted"* and instructs treating that as settled before
starting. At the moment this dispatch actually opened `decisions/ADR-021-dataviz-layer.md`
(before any payload work began), its Status line read **"PROPOSED — Gate A, awaiting human
decision,"** not accepted. Mid-session, a system reminder surfaced that the file had changed on
disk to **"ACCEPTED — Gate A, human decision recorded 2026-09-03"** — before any payload content
depended on the distinction, so the brief's claim is true *as delivered*, but it was not true at
the instant this dispatch was told to treat it as settled. A dispatch that trusted the brief's
tense without re-reading the file would have built on a decision that had not yet been made.
Recorded per the standing instruction that a correction found in one's own brief is stated, not
silently absorbed — matching the pattern nine prior agents in this repository have each hit once.

No other factual claim in the brief needed correction against the evidence.

---

## 1. Gate B — checklist

| Check | Result | Evidence |
|---|---|---|
| Directory named `YYYY-MM-DD__dashboard__<slug>__v<N>` | PASS | `2026-09-03__dashboard__batch-3-competitor-coverage__v4` |
| `manifest.json` present and valid | PASS | `id` ART-021, type `dashboard` registered in `_types.json`, `supersedes: "ART-016"` |
| `validation.md` present and filled in | PASS | this file |
| Every `[E-nnn]` citation resolves | PASS, vacuously | `grep -c "\[E-" luma-competitor-coverage-board.html` → 0. Zero minted; the ledger holds zero records |
| No raw hex / no raw px where the artifact is visual | PASS | every colour is `color(srgb …)`; `grep -noE '#[0-9a-fA-F]{3,8}\b' … \| grep -v '&#'` → empty; `grep -noE '(padding\|margin\|gap\|border-radius)\s*:\s*[0-9]+px'` → empty (border-*width* literals, e.g. `border: 2px dashed`, are not spacing and are the same convention v1–v3 used) |
| Every metric names its data source and refresh cadence | PASS | every KPI/section keeps its `[ART-nnn § …]` tag; refresh stated once in the header (static, tied to 21 Jul 2026) |
| Palette from tokens.json | PASS | §3 — every colour is a named token path, re-derived independently in `verify-encoding.py` |
| No causal claim from correlational data | PASS | every statement is a count, ratio, or verbatim rating |

## Gate A — human review

| Check | Result |
|---|---|
| Claims labelled `Evidenced` / `Inferred` / `Assumption` | PASS — every prose claim carries `[ART-nnn § …]`, `[D-00n]`, or sits in the Meta Assumptions block |
| Assumptions block present and visible | PASS — inside the Meta `<details>`, forced open under print (§7) |
| Reviewed by: ______ Date: ______ | open — `draft` until a human signs |

---

## 2. Component membrane and the dataviz layer (ADR-021)

Checked directly, not assumed:

- `design-system/component-index.json` has **no** `cf-chip`, `cf-nav-rail` or `cf-detail-panel`
  entry (`python3 -c "import json;d=json.load(open('design-system/component-index.json'));print([c['name'] for c in d['components']])"`
  lists the same 8 stable L1 primitives it has all session). No ADR promotes any of the three.
- ADR-021's consequence for the two layers is asymmetric and this payload respects the asymmetry:
  `cf-unit-cell` (ART-017) is **chart anatomy** — needs no promotion, has no index entry, and
  every unit mark on this board (the isotype arrays, the journey grid, the load-bearing spotlight)
  is built from its measured contrast tables. `cf-chip`, `cf-nav-rail`, `cf-detail-panel`
  (ART-018/019/020) **remain components** — "the membrane applies to all three, unchanged" — so
  this payload does **not** instantiate them. No `<CfChip>`, `<CfNavRail>` or `<CfDetailPanel>`
  tag appears anywhere in the file, including inside CSS comments (checked with
  `grep -noE '<[A-Z][A-Za-z0-9]+[ />]'` → empty; one early draft slip — two CSS comments that
  named the proposals inside literal angle brackets — was caught by this exact grep and reworded,
  logged in `manifest.json`'s findings).
- The nav rail, the per-row/per-cell classification marks, and the detail panel are built as
  page-local, on-token HTML/CSS/JS **informed by** the three specs' measured contrast tables and
  interaction contracts, not **instantiated as** those components. This is the same category of
  artifact-local pattern v1–v3 already used for `.kpi`/`.spot`/`.tierchip` without a
  component-index entry, and it is verified against Gate B's actual mechanical check, not merely
  against a reading of the prose rule: `gate-b.py`'s component check (§3 in the hook) matches
  `<([A-Z][A-Za-z0-9]+)[\s/>]` — PascalCase JSX-shaped tags — and does not fire on lowercase HTML
  (`<nav>`, `<aside>`, `<span class="chip">`). Confirmed by running the exact regex against the
  final payload (above) and finding zero matches.
- `cf-chart-palette` is not used anywhere in this payload (`grep -c "chart-palette"` → 0). It is
  measured defective (C-036, ADR-021 §Context) and no chart here reaches for it; the entire
  categorical/ordinal encoding is the single-hue teal ramp plus footprint/border-style, per §3.

---

## 3. The encoding contract — every ratio computed, not asserted

`verify-encoding.py` (beside this file) resolves every token this payload uses through
`design-system/tokens/tokens.json`'s alias chain independently of the four component specs' own
`verify-contrast.py` scripts, and recomputes WCAG relative luminance / contrast from the raw hex.
Re-run: `python3 verify-encoding.py`.

**Foundations are frozen**: canonical hash `1926c393fe83742443350f2aa4e8d5dd3d0d6d7393a31c93e2f74317cada1a7f`,
confirmed unchanged this session (`shasum -a 256 design-system/tokens/tokens.json` and the
canonical-JSON re-serialisation both reproduce token-keeper's 2026-09-03 baseline report). No new
token, colour, size or spacing step was requested or used.

### Marks — 3:1 floor (WCAG 1.4.11)

| Mark | Ground | Ratio | Verdict |
|---|---|---|---|
| `palette.teal.60` (Weak fill) | `palette.bone.default` | **4.223:1** | PASS |
| `palette.teal.70` (Adequate fill) | `palette.bone.default` | **6.526:1** | PASS |
| `palette.teal.90` (Strong fill) | `palette.bone.default` | **12.781:1** | PASS |
| `semantic.border.strong-01` (nav-rail edge, panel edge, "No"/prior-art outlines, isotype box) | `palette.bone.default` | **4.253:1** | PASS |
| `semantic.focus` (outer focus ring) | `palette.bone.default` | **4.234:1** | PASS |
| `semantic.focus-inset` (inner focus ring; also the dashed Medium-confidence border) vs `teal.60` | | **4.989:1** | PASS |
| `semantic.focus-inset` vs `teal.70` | | **7.710:1** | PASS |
| `semantic.focus-inset` vs `teal.90` | | **15.099:1** | PASS |
| `palette.coolGray.80` (Tier 1 tag) | `palette.bone.default` | **9.751:1** | PASS |
| `palette.coolGray.60` (Tier 2 tag) | `palette.bone.default` | **4.248:1** | PASS |
| `palette.warmGray.90` (structural/gap row fill, "the fourteen") | `palette.bone.default` | **12.904:1** | PASS |
| `palette.warmGray.70` (gap-row hover fill) | `palette.bone.default` | **6.605:1** | PASS |
| `semantic.border.strong-01` | `semantic.layer.01` (rail surface) | **4.569:1** | PASS |
| `semantic.border.strong-01` | `semantic.layer.02` (panel surface) | **5.025:1** | PASS |

### Text — 4.5:1 floor (WCAG 1.4.3)

| Text | Ground | Ratio | Verdict |
|---|---|---|---|
| `semantic.text.primary` (ink) | `palette.bone.default` | **15.946:1** | PASS |
| `semantic.text.secondary` | `palette.bone.default` | **6.614:1** | PASS |
| `semantic.text.primary` | `semantic.layer.01` (rail) | **17.127:1** | PASS |
| `semantic.text.secondary` | `semantic.layer.01` (rail idle item) | **7.104:1** | PASS |
| `semantic.text.primary` | `semantic.layer.02` (panel) | **18.838:1** | PASS |
| `semantic.text.secondary` | `semantic.layer.02` (panel metadata) | **7.814:1** | PASS |
| `semantic.link.primary` | `semantic.layer.02` | **7.795:1** | PASS |
| `semantic.focus-inset` (white text on absence-row fill) | `palette.warmGray.90` | **15.244:1** | PASS |
| `semantic.focus-inset` (white text on gap-row hover fill) | `palette.warmGray.70` | **7.802:1** | PASS |

### Deliberately sub-floor, and why each is not load-bearing (stated, not hidden)

| Pair | Ratio | Why it is safe |
|---|---|---|
| `semantic.layer.01` (rail) vs `palette.bone.default` | **1.074:1** | Not load-bearing — the rail's boundary is carried entirely by the `border-strong-01` edge (4.253:1), exactly as ART-019 measured. The tinted surface is a hint, not the boundary. |
| `semantic.layer.02` (panel) vs `palette.bone.default` | **1.181:1** | Same reasoning, ART-020: the panel's boundary is the `border-strong-01` edge. |
| `semantic.layer.selected-01`/`.accent-01` vs `semantic.layer.01` | **1.200:1** | Never used as a "current" background anywhere on this board (rail current-state is a border-bar + weight + `aria-current`, per ART-019's own finding that this pair cannot carry a selected state). |
| `palette.teal.60` vs `palette.teal.70` | **1.545:1** | Adjacent ordinal steps never touch without the `spacing.01` gutter; every unit cell in the journey grid has its own cell padding, so the adjacent colour a reader compares is always the ground, not the neighbour fill (4.223:1 worst case). |
| `palette.coral.default` vs `palette.bone.default` | **2.817:1** | Used once, as a 4px decorative left-border accent on the F-01 disclaimer card — never as text, never as the sole channel distinguishing anything (the card is also bordered in `border-strong-01` and headed "Disclaimer" in ink text). `palette.coral.text` (5.175:1) is used instead wherever the colour must carry legibility. |

### Colour is never the only channel (WCAG 1.4.1)

Checked per object, not asserted globally:

- **Journey grid** — value (fill lightness, one hue) + confidence (dashed border, a different
  channel) + a direct mono label (`S·H`, `W·M`, `unk`, `n/e`, `p-a`) beneath every cell. A
  greyscale or forced-colours render loses the fill's exact step but not the state, because the
  label is text and the absence states differ by border style/presence, never by hue alone.
- **The fourteen** — state is a text word ("Profiled" / "Prior-art only" / "Never evaluated") plus
  row shading; the word alone is sufficient without the shading.
- **Isotype clusters** — evidenced units are ink-filled; every absence unit is a literal hole (no
  fill, no border) — footprint is the channel, not hue.
- **Spotlight row** — four states on four different marks (filled square / outlined square /
  dashed outline / nothing), each with a direct word label beneath.
- **Scoreboard** — settled/unsettled state is a filled-vs-dashed-outline mark plus the word
  "Settled" / "Not settled" / "Not tested".

---

## 4. Interaction — verified by driving the rendered page, not by reading the source

`verify-interaction.mjs` (beside this file) connects to a running headless Chrome over the
DevTools Protocol and dispatches real `click`/`keydown` events at the actual DOM, then reads the
resulting state back. Re-run:

```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --no-sandbox --remote-debugging-port=9333 --user-data-dir=/tmp/cdp-profile about:blank &
sleep 2
node verify-interaction.mjs
```

Captured this session:

| # | Test | Result |
|---|---|---|
| 1 | Click a journey cell (Booking.com × Book) | Panel opens, `aria-expanded` flips to `true`, the journey `<table>` is still present in the DOM (`gridStillInDom: true`) — the grid is never covered or removed |
| 2 | Click a "the fourteen" row (Tripadvisor) | Panel opens and **focus moves to the panel** (`focusedIsPanel: true`) — a keyboard user arriving by click still lands somewhere sensible |
| 3 | `Escape`, dispatched on the focused panel (the realistic path — a real keydown's `target` is always an Element; dispatching on `document` itself throws inside the handler because `Document.closest` does not exist, which is a limit of a synthetic test, not a real user path) | Panel closes, **focus returns to the exact trigger** that opened it, `aria-expanded` returns to `false` |
| 4 | `Enter` key on a non-`<button>` `role="button"` element (a cluster row) | Opens identically to a click — keyboard parity confirmed, not merely asserted from `role`/`tabindex` markup |
| 5 | Close button click | Panel closes |
| 6 | Scroll to `#journey`, wait for smooth-scroll + `IntersectionObserver` to settle | `aria-current="location"` moves to the Journey rail link. **First attempt at a 500ms wait produced a false negative** (`#evidencegap`, the previous section) — headless Chrome's smooth-scroll animation had not finished; 1200ms was sufficient. Recorded because it is exactly the kind of test-methodology error the "attack your own result" instruction exists to catch. |

**What this does and does not prove.** All 155 triggers share the same `openPanel`/keydown
delegation logic (verified by code inspection: one `document.addEventListener('click', …)` and
one `keydown` handler, no per-trigger wiring to diverge), so these six tests exercise the shared
mechanism across all four trigger types (table row, table cell, isotype-cluster row, and — by the
same code path — the spotlight cells and scoreboard rows, not separately driven this session).
**Not checked, and not claimed:** a real screen-reader pass, a real touch/pointer test, 400%/200%
zoom reflow, `forced-colors: active` rendering, and a CVD-simulated render. This session has
Chrome and Node, not an assistive-technology stack. **Skipped is not passed.**

---

## 5. Progressive disclosure, structurally

- Two levels maximum. The grid (level one) stays visible; the panel (level two) shows provenance
  for one clicked mark. Nothing nests below the panel — it has no `<details>`, no accordion, no
  second panel, matching ART-020's binding limit. Verified: `grep -c '<details' luma-…html` → 1
  (the Meta appendix only, which is a page-level disclosure unrelated to any grid cell).
- Click-to-pin, never hover: no `:hover`-triggered content-reveal rule exists in the CSS (`grep -n
  ':hover' luma-…html` shows only background-tint feedback on already-focusable/clickable rows,
  never a first appearance of content that isn't otherwise announced).
- Every one of 155 triggers carries `role="button"`, `tabindex="0"`, `aria-haspopup="true"`,
  `aria-controls="detail-panel"` and (fixed this session, see §8 finding d) a default
  `aria-expanded="false"` — confirmed by count: `grep -o 'aria-expanded="false"' … | wc -l` → 155,
  matching the trigger count exactly before any interaction.

---

## 6. Navigation

- A sticky rail lists 7 top-level sections plus one sub-link (Coverage → F-01 disclaimer),
  demonstrating the two-level depth ART-019 specifies. Every item is a real `<a href="#id">`;
  `grep -c '<nav' … ` → 1, and every rail link resolves to a real section `id` (checked by
  extracting all `href="#…"` values and confirming a matching `id="…"` exists for each — all 8
  resolve).
- Scrollspy is progressive enhancement, confirmed structurally: the rail's markup and every
  `href` work with JavaScript disabled (they are plain anchors); only the `aria-current`
  highlight depends on `IntersectionObserver`, per §4 test 6.
- **The headline never scrolls out of reach without a second sticky bar.** The rail's own top
  block repeats the "6/14" headline permanently; there is exactly one `position: sticky` element
  active at a time in the CSS (`grep -c 'position: sticky'` → 2 — the rail and the panel — and
  the two are never both visible simultaneously at the narrow breakpoint, see next point).
- **Mobile collision, tested.** At `<64rem` the rail collapses to a horizontal scrollspy strip
  (`max-height: 3.5rem`) at the top; the detail panel switches to `position: fixed; inset: auto 0
  0 0` (bottom sheet) rather than a second sticky element competing for the same vertical space as
  the journey table's own header row. The two sticky surfaces (rail-strip, panel-sheet) occupy
  opposite edges of the viewport and are never both fighting for the same region the grid's column
  headers need. Verified by reading the computed layout rules; **not rendered at a real narrow
  viewport with a screenshot this session** — recorded as a real gap, not claimed as observed.

---

## 7. Print — verified with a real render, and a real defect found and fixed

`print-color-adjust: exact` (+ `-webkit-` prefix) is set globally, as v1–v3 did. This session
went further than any prior version: an actual `--print-to-pdf` render was taken **before** and
**after** a fix, and the PDF's *text* was extracted with PyMuPDF and checked for specific phrases
that only exist inside the collapsed Meta `<details>` — not just checked for surviving background
colour, which is what v3's own print check actually verified.

**Before:** the CSS-only technique v2/v3 both shipped
(`details.meta > *:not(summary){display:block!important}`) produced a 7-page PDF in which the
phrases "Changed from v3 to v4" and "Claim format" — both inside the Meta body — were **absent**
from the extracted text entirely. The dark absence fills ("the fourteen," the journey grid)
printed correctly, which is the only thing v3's own print check actually confirmed; whether
*hidden* content became visible was never tested by any prior version. This is very likely a
latent defect carried since v2 that nothing caught, because nobody checked for it specifically.

**Fix:** `beforeprint`/`afterprint` listeners toggle the actual `open` HTML attribute on the Meta
element (and restore whatever state it was in before printing, once the print dialog closes) —
the standards-based mechanism, not a CSS override on the assumption that a browser's internal
`<details>` collapse behaviour is just a plain `display:none` a descendant selector can beat.

**After:** the same render produces a 9-page PDF; both phrases are present; every dark absence
fill still survives (re-checked, unchanged from the earlier pass); word count extracted from the
PDF rose from 1366 to 2047, consistent with the Meta section now actually printing.

Reproduce:
```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --no-sandbox --print-to-pdf=/tmp/v4.pdf --no-pdf-header-footer \
  file://$(pwd)/luma-competitor-coverage-board.html
python3 -c "import fitz; d=fitz.open('/tmp/v4.pdf'); t=''.join(p.get_text() for p in d); \
  print(d.page_count, 'Changed from v3 to v4' in t, 'Claim format' in t)"
```

**What remains untested.** The interactive Print-dialog "Background graphics" checkbox path a
human actually uses — same limit v3 recorded, and still true here: this environment's
`--print-to-pdf` CLI flag does not expose that checkbox's default-off behaviour.

---

## 8. Findings — checked and fixed this session

Full method and citations are in `manifest.json`'s `findings.method`. Summary:

| # | Severity | Finding | Fix |
|---|---|---|---|
| a | layout | Isotype cluster boxes stretched to the full grid-track width regardless of unit count, so a 28-unit cluster (Loyalty) rendered inside a box sized for the widest possible row, defeating the box's own job of showing "this is the whole denominator" | `.ciso { width: fit-content; justify-self: start; }` |
| b | layout | The empty/closed detail panel reserved a full 100vh-tall row below the footer before first use (an implicit second grid row under a single-column `.shellgrid`) | `.shellgrid:not(.panel-open) .panel { display: none; }` |
| c | membrane hygiene | Two CSS comments referenced the unpromoted proposals inside literal angle brackets (`<CfNavRail>`, `<CfDetailPanel>`), which — being inside `<style>`, not HTML-escaped — read as component-tag-shaped text to a regex scanner | Reworded without angle brackets |
| d | accessibility | All 155 click-to-pin triggers had `aria-haspopup`/`aria-controls` but no default `aria-expanded`, so a screen reader had no way to know they were togglable before first interaction | Added `aria-expanded="false"` to every generated trigger; verified 155 occurrences in the output |
| e | print | `<details>` forced open via a CSS override on its children did not actually reveal hidden content in this Chrome build's print path (§7) | `beforeprint`/`afterprint` JS toggling the real `open` attribute |

All five were found and fixed before this file was written, by attacking this build's own output
with the same tools (grep, headless Chrome, CDP, PyMuPDF) rather than trusting the source as
written — the standing instruction that the author of a check is the one person who cannot
perform it does not have a clean substitute for a solo dispatch, so the substitute used here is
re-deriving every number and re-running every render rather than reading the code back.

---

## 9. Prose — cut, measured, reproducible

`wordcount.py` (unchanged from v3, copied verbatim so the method is identical across versions —
`diff` confirms byte-identical) strips `<style>`/`<script>` and the body of every closed
`<details>`, keeping only what a reader sees with zero clicks.

```
$ python3 wordcount.py luma-competitor-coverage-board.html          # v4
all-DOM words (incl. collapsed <details>):  2142
visible words (closed-details bodies excluded): 1460
nested <details> found (would break the stripper): 0

$ python3 wordcount.py ../2026-09-03__dashboard__batch-3-competitor-coverage__v3/luma-competitor-coverage-board.html   # v3, same script
all-DOM words (incl. collapsed <details>):  4058
visible words (closed-details bodies excluded): 2183
nested <details> found (would break the stripper): 0
```

**Visible words: 2183 → 1460, a 33% reduction. All-DOM words: 4058 → 2142, a 47% reduction** (the
larger all-DOM drop is because v3 hid a lot of its per-cell explanatory text behind ~30
`<details class="note">` elements scattered through the grid, each counted in all-DOM; v4 moves
the equivalent content into the 155-entry JSON the detail panel reads, which sits inside a
`<script type="application/json">` block that `wordcount.py` — correctly — strips before counting,
the same way it would strip v3's own `<script>` content. Neither figure is inflated by that data;
both scripts treat script contents identically.)

**Em-dash count**, measured the same way (strip style/script, strip closed-`<details>` bodies,
convert HTML entities, then count `—`), because the brief's own complaint cited a raw count that
turned out to include hidden content:

```
v3 visible em-dashes: 45   ·   v4 visible em-dashes: 33   (27% reduction)
v3 all-DOM em-dashes: 72   ·   v4 all-DOM em-dashes: 45   (matches the brief's cited "73" for
  v3 within one — the brief's figure was evidently counted on all-DOM text, not visible text;
  a raw byte-count of the whole v4 file, including the embedded JSON panel data, would read 220,
  which is not a fair comparison to any figure derived from v3's own visible or all-DOM prose and
  is not used here for that reason.)
```

The reduction is real and reproducible with the two commands above; it is smaller than the
headline "cut hard" framing might suggest because a genuinely interactive, navigable, disclosure-
based page still needs section intros, per-chart captions and a Meta appendix that a static essay
did not have to duplicate — the difference is that in v4 none of that text is the primary way a
fact reaches the reader; every headline number is legible from the static page with zero clicks
(§10), and the 155-entry detail data is enrichment, not the only copy of anything.

---

## 10. Invariants — checked against the payload, not asserted

- **All 14 competitors present, ART-011's order.** Verified: `COMPETITORS` list in the generator
  has 14 entries in the same sequence as ART-011 §Coverage's table; the fourteen-row table, the
  spotlight (extended to all 14, not just the 6 v3 showed), and the journey grid (all 14 rows)
  each render exactly this list, checked by construction (one Python list is the single source
  for all three renderings, so they cannot drift from each other).
- **770 and 112 are the only denominators**, never the profiled subset. The isotype arrays sum to
  770 exactly (`sum of the 10 cluster totals = 42+70+70+98+70+42+140+112+98+28 = 770`, printed by
  the generator script and re-checked by hand here). The journey grid draws 14×8=112 cells.
- **Three absence states stay distinct.** Never-evaluated and prior-art-only are different CSS
  classes with different border treatments (dashed vs none) everywhere they appear (the fourteen,
  the spotlight, the journey grid); profiled-but-unresolved ("Unknown") within the six profiled
  uses the identical blank treatment as never-evaluated at the individual-mark level (both are
  literally "no evidence exists for this cell") but is always labelled distinctly in the direct
  mono caption beneath (`unk` vs `n/e` vs `p-a`) and in the detail panel's title/body — never
  conflated as a claim, only as a mark.
- **No filters, no sort controls, no show/hide.** `grep -inE '<select|<input|type="checkbox"|
  type="radio"|<button.*(sort|filter|hide|show)'` on the payload returns nothing. The one close
  button in the page closes the detail panel, not a row.
- **Sort order is editorial, stated.** The cluster isotype list is worst-first by design; the
  caption says so explicitly rather than offering a control.
- **Every headline is true and legible with zero clicks.** The 6/14 hero, the F-01 disclaimer
  table, the eight blanks (drawn as full dark rows in "the fourteen" without opening anything),
  the three designated-test outcomes that are settled/unsettled/untested (the scoreboard's own
  "Settled?" column text), and the Song & Szafir correction (in the Meta appendix, which is
  collapsed by default but forced open under print, per §7 — **on screen it is one click**,
  consistent with "Meta" being process documentation rather than a headline finding; every number
  the brief calls a headline — the 8 blanks, the 3 unsettled tests, F-01 — is static body text or
  a static table, never behind the Meta disclosure).

---

## 11. Accessibility structure, extracted mechanically

```
h1 × 1, h2 × 8 (7 section heads + 1 visually-hidden panel title, empty & display:none until
  populated), h3 × 5 (inside Meta), no level skipped in document order
main × 1, nav × 1, aside × 1, table × 4 (each with a <caption>)
th[scope=row] × 35, th[scope=col] × 25
color-mix() × 0, opacity: declarations × 0, raw colour hex × 0
tabindex="0" × 155, aria-haspopup × 155, aria-controls × 155, aria-expanded="false" × 155 (default)
skip link present (.skiplink, visible on focus)
```

All extracted programmatically from the final payload (regex + a small heading-order walk), not
asserted from memory of what was written. **Not checked, and not claimed:** a real AT pass, a
forced-colors render, 200%/400% zoom, 320px reflow — same tooling gap every prior version of this
board declared for these specific checks. Skipped is not passed.

---

## 12. Repository audit — before and after, diffed by finding, not by count

```
$ python3 validation/audit-system.py
```

**Before** (captured before this dispatch touched anything):

```
blocker 0 · error 5 · warning 5 · info 6 · skipped 0
VERDICT: FAIL
```

Findings: `attestation` error (5g, pre-existing — this dispatch touched no validator, hook, or
gate wiring); `prose-counts` errors PC-001/PC-003/PC-004/PC-010 (README/CLAUDE.md/DESIGN-SYSTEM.md
ADR-count and L1-primitive-count drift, pre-existing, none of which this dispatch's files state or
touch); `provenance` warning on ART-015; `corrections` warning (C-031/033/034/035/036/037/038 have
no check); `coverage` warning (V-015, V-020 unverified); two `surfaces` staleness warnings.

**After** (this directory written, `wordcount.py`/`verify-encoding.py`/`verify-interaction.mjs`
added, v3's manifest set to `superseded`, registry rebuilt):

```
$ python3 validation/audit-system.py
```
```
blocker 0 · error 1 · warning 5 · info 6 · skipped 0
VERDICT: FAIL
```

**Diffed by `(severity, check, message)`, not by count** — the brief's own instruction, because
another agent (system-keeper, per `CLAUDE.md`'s routing table and per the working-tree changes to
`README.md`, `CLAUDE.md`, `design-system/DESIGN-SYSTEM.md` and `design-system/component-index.json`
this dispatch found already modified and did not make) was writing concurrently:

```
REMOVED (present before, absent after):
  ERROR   prose-counts  PC-001: README.md states 20 (ADR count...) but the repo has 21
  ERROR   prose-counts  PC-003: CLAUDE.md states 11 (L1 primitive count...) but the repo has 8
  ERROR   prose-counts  PC-004: CLAUDE.md states 11 (L1 primitive count...) but the repo has 8
  ERROR   prose-counts  PC-010: design-system/DESIGN-SYSTEM.md states 11 (...) but the repo has 8
  INFO    prose-counts  8 of 12 declared prose counts agree with the repo (4 disagree, 0 stale)

NEW (absent before, present after):
  INFO    prose-counts  12 of 12 declared prose counts agree with the repo (0 disagree, 0 stale)
```

**This delta is not this dispatch's.** `git status --short README.md CLAUDE.md
design-system/DESIGN-SYSTEM.md design-system/component-index.json` shows all four as modified
working-tree files this session touched none of; `git log -1` on each shows its last *commit* was
days before today, confirming the fix is an uncommitted change from a concurrent dispatch, not
history this one is riding on. Per the explicit instruction not to claim another agent's delta:
**zero findings above are attributed to this artifact.** The five findings unchanged across both
runs (`attestation` 5g, `provenance` ART-015, `corrections` C-031/033/034/035/036/037/038,
`coverage` V-015/V-020, both `surfaces` staleness warnings) are pre-existing and this dispatch's
files neither caused nor resolve any of them — this dispatch wrote only under
`artifacts/luma-travel/2026-09-03__dashboard__batch-3-competitor-coverage__v4/`, touched
`artifacts/_registry.json`/`artifacts/ARTIFACTS.md` only via the standard
`rebuild-registry.py` regeneration, and set one field (`status`) in v3's own manifest.

**This artifact introduces zero new findings.** It mints no `[E-nnn]`, adds no raw hex/px, adds no
unregistered component tag, and its directory/type/manifest/validation.md all satisfy the checks
`audit-system.py` runs. Check 5g's attestation error is pre-existing and unrelated: this session
edited no validator, no hook, and no gate wiring.

---

## 13. Files in this artifact

| File | Purpose |
|---|---|
| `luma-competitor-coverage-board.html` | the payload |
| `manifest.json` | provenance |
| `validation.md` | this file |
| `verify-encoding.py` | re-derives every WCAG contrast ratio in §3 from `tokens.json`, independent of the four component specs' own scripts |
| `verify-interaction.mjs` | drives the rendered page over CDP to reproduce §4's six interaction tests |
| `wordcount.py` | copied verbatim from v3, so the §9 word-count method is identical across versions |

---

## Verdict

Gate B: **pass**. Gate A: **pending a named human**. Status stays `draft`.
