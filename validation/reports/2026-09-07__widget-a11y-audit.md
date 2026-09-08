# Accessibility audit — widget layer

**Artifact under audit:** `artifacts/luma-hands-on/2026-09-07__dashboard__hands-on-findings-and-recommendations__v2/luma-competitor-research-findings.html`
**Scope:** the interactive widget layer added today — `.row` buttons + evidence meter, `.fchip` filter row + evidence-index table, `.ledger` `<dl>`, and the global theming (`::selection`, `caret-color`, `accent-color`, `scrollbar-color`) and motion handling. Chart/SVG interaction (`.c-row`, `.chain-node`) is noted only where it shares code paths with the audited widgets.
**Standard:** WCAG 2.2 AA.
**Auditor tool boundary:** Read + Write only, no Bash, no browser. Every finding below comes from reading the rendered HTML/CSS/inline JS directly — none from the generator, except where explicitly marked. **No contrast ratio or pixel/target-size measurement is asserted here** — that is the rendered-DOM pass's job, and its numbers (worst row text 5.18:1, filter chip text 18.84:1, filled meter pip 15.95:1) are taken as given. Anything below that needs an actual browser render (forced-colors mode, computed geometry) is flagged as **NEEDS RENDER**, not asserted as pass or fail, per the scope limit given for this task.
**Gate:** B (automated first filter). This is not the verdict — Gate A (human) still reviews before this screen ships.

---

## Summary

| Severity | Count |
|---|---|
| Blocker | 0 |
| Error | 2 |
| Warning | 4 |
| Info | 3 |
| Needs render (deferred, closing condition below) | 2 |
| Confirmed pass (quoted evidence) | 7 |

---

## 1. `.row` buttons — accessible name, `aria-expanded`, focus management

### PASS — accessible name conveys count in words regardless of `.row__nu`'s `display:none`

The task's premise was: `.row__nu` (" finding"/" findings") is `display:none` above 40rem [actually stated as 60rem in the CSS — see note], which removes it from the accessibility tree, so does the bare digit read as meaningless at desktop width? **It doesn't, and not because of anything to do with `.row__nu`'s display state.** The entire row is a single `<button>` carrying an explicit `aria-label`, and per the accessible-name computation algorithm, a non-empty `aria-label` on an element **replaces** the "name from subtree content" step entirely — the browser never looks at `.row__n`/`.row__nu` to build the name. Evidence:

```html
<button type="button" class="row" data-detail="find-market-1"
    aria-haspopup="true" aria-controls="detail-panel" aria-expanded="false"
    aria-label="The more a product can sell you, the less of the real answer it shows.. 5 findings cited. Opens full text and sources.">
  ...
  <span class="row__n">5<span class="row__nu"> findings</span></span>
  ...
</button>
```

The name is `"...5 findings cited. Opens full text and sources."` — spelled out — irrespective of whether `.row__nu` is rendered. This holds at every breakpoint. **Correction to the CSS reference in the task brief:** the breakpoint is `@media (max-width: 60rem)`, not 40rem (`.row { grid-template-columns: 1fr auto; row-gap: var(--s02); } .row__nu { display: inline; }` at line ~195-199 of the stylesheet).

### PASS — state and count are both in the accessible name

```
aria-label="...20 axes total), zero concern effort.. 0 findings cited. corrected. Opens full text and sources."
aria-label="Notify a traveller...1 finding cited. alone. Opens full text and sources."
```
`.st--corrected` → "corrected." and `.st--alone` → "alone." both appear verbatim in `aria-label`, matching the visual chip text. Zero-evidence rows correctly say "0 findings cited" and use `.meter__z` ("no finding cited") instead of pips — also `aria-hidden="true"`, so it doesn't double up with the label.

### ERROR — `.row__who` is dropped from the accessible name whenever it isn't already repeated in the title (WCAG 1.3.1 Info and Relationships; WCAG 2.5.3 Label in Name)

`.row__who` is visible, un-hidden text inside the button. Where the competitor name is already present in `.row__t`'s title (the common case), nothing is lost. But at least three rows carry a `.row__who` attribution that is **not echoed anywhere in the title**, and it is silently dropped because `aria-label` overrides the whole subtree:

```html
<!-- find-market-1: sighted users see "Roster-wide"; aria-label never says so -->
aria-label="The more a product can sell you, the less of the real answer it shows.. 5 findings cited. Opens full text and sources."
<span class="row__who">Roster-wide</span>

<!-- find-loyalty-2: sighted users see all four named companies; aria-label says none of them -->
aria-label="Four loyalty programmes, four full-text searches, zero mentions of a first-time traveller.. 4 findings cited. Opens full text and sources."
<span class="row__who">Booking.com, Expedia, Iberia, Qatar Airways</span>

<!-- find-loyalty-3 -->
aria-label="In both examined programmes the entry tier is non-empty — what is gated is the BEST rate, not participation.. 1 finding cited. Opens full text and sources."
<span class="row__who">Booking.com &amp; Expedia</span>
```
This isn't a one-off (checked more than one instance per SR-7): it recurs at least three times in the `find-*` groups (pain points and insights are unaffected because their `.row__who` is always an empty span). On a board whose entire premise is evidence traceability to a named source, dropping *which competitor(s)* a claim covers for screen-reader users is a direct hit to the artifact's own stated purpose, not a cosmetic gap. **Fix:** fold `.row__who` into the generated `aria-label` string (e.g., append `"— {who}."`) whenever it is non-empty and not already a substring of the title.

### PASS — `aria-expanded` is set on open and correctly cleared on every other trigger

```js
document.querySelectorAll('[aria-expanded="true"]').forEach(function(el) {
  if (el !== trigger) el.setAttribute('aria-expanded', 'false');
});
if (trigger) trigger.setAttribute('aria-expanded', 'true');
```
Runs on every `openPanel()` call, so exactly one trigger (row, evidence-index `<tr>`, or chart `.c-row`) is ever marked `aria-expanded="true"` at a time, and `closePanel()` clears all of them. Verified against the initial static markup, which starts every trigger at `aria-expanded="false"`.

### PASS — `aria-labelledby` target is populated before focus lands on the panel

```js
panelTitle.textContent = d.title;   // line ~2555
...
panel.setAttribute('tabindex', '-1');
panel.focus({preventScroll: true}); // line ~2577
```
`panel-title`'s text is set several statements before `panel.focus()` runs, and the panel itself is `display:none` until `shellgrid.panel-open` is added (also before `.focus()`), so there is no frame where an empty-named, invisible element receives focus.

### PASS — Escape closes the panel from anywhere on the page

```js
if (e.key === 'Escape' && shellgrid.classList.contains('panel-open')) { closePanel(); }
```
Global `keydown` listener, not scoped to focus-within-panel — works regardless of where focus currently is, as long as the panel is open.

### PASS — focus returns to the invoking control on close (with one real exception, below)

```js
if (lastTrigger && document.contains(lastTrigger)) { lastTrigger.focus(); }
```
`document.contains()` guards against the trigger having been removed from the DOM entirely.

### ERROR — that guard checks DOM *presence*, not *visibility*, so filtering the evidence index while its detail panel is open can drop focus to nowhere (WCAG 2.4.3 Focus Order)

Every evidence-index `<tr>` is itself a `data-detail` trigger (`role="button" tabindex="0"`). The filter script hides non-matching rows using the `hidden` **property** (`tr.hidden = !hit`), which correctly removes them from the accessibility tree and from the tab order — but `document.contains(lastTrigger)` returns `true` for a `hidden` element (`hidden` doesn't remove a node from the DOM, only from rendering/focusability). Reproduction, traced directly from the code, not asserted from a render:

1. Open the panel from evidence-index row `idx-72` (competitor: Rentalcars.com).
2. Click the `Booking.com` filter chip. `idx-72`'s claim text happens to mention "Booking.com" too (see the next finding), but suppose instead the user filters by a competitor that does hide `idx-72` — the row becomes `tr[hidden]`, which the stylesheet renders as `display:none` (`.idx tr[hidden] { display: none; }`), i.e. unfocusable.
3. Press Escape (or click Close). `closePanel()` runs `lastTrigger.focus()` on the now-hidden `<tr>`. Calling `.focus()` on a `display:none` element is a documented no-op in every major browser — focus does not move, and because the panel itself is also being hidden at the same time, focus is left on nothing determinate (effectively reset to `<body>`), forcing the keyboard user to re-navigate from the top of the document.

**Fix:** in `closePanel()`, check visibility as well as DOM presence (e.g. `lastTrigger.offsetParent !== null` or `!lastTrigger.hidden`), and fall back to a stable landmark (e.g. the filter input, or `document.body` with an explicit heading focus) when the original trigger is no longer reachable.

### WARNING — programmatic focus order doesn't match DOM/tab order, so Shift+Tab from the panel is disorienting (WCAG 2.4.3 Focus Order)

DOM order is `.shellgrid > .content > .panel` (confirmed: `.content`'s closing `</div>` and `.shellgrid`'s closing `</div>` bracket the `<aside id="detail-panel">`, matching the CSS's `.shellgrid.panel-open { grid-template-columns: minmax(0,1fr) var(--panel-w); }` two-column grid expectation). `panel.focus()` moves focus there directly regardless of where the trigger sits in the document, which is fine going forward (Tab from the panel reaches the Close button, which is the panel's only other focusable descendant, then exits the page). But **Shift+Tab from the freshly-focused panel goes to whatever is *last* in DOM order inside `.content`** — e.g. a footer or Meta-details link — not back toward the row the user just activated, which could be anywhere on a very long page. This is not a hard trap (nothing loops forever), but it is a focus-order surprise for keyboard users who instinctively Shift+Tab to "go back". Comment in the CSS explicitly documents that this is deliberately *not* a modal and has *no* focus trap, so this isn't an oversight of that decision — it's a side effect of the panel's fixed DOM position that the decision doesn't address.

---

## 2. `.meter` — decorative pips, zero-evidence path

### PASS — nothing is conveyed by the meter alone

```html
<span class="meter " aria-hidden="true"><i class="on"></i>...</span>
<span class="meter meter--alone" aria-hidden="true">...</span>
<span class="meter__z" aria-hidden="true">no finding cited</span>
```
All three variants (filled pips, "alone" variant, zero-evidence text) are `aria-hidden="true"`, and — as established in §1 — even if they weren't, the parent button's `aria-label` would override them anyway. Belt-and-braces, correctly applied. (Minor code-hygiene note, not a compliance issue: since the parent `aria-label` already suppresses the whole subtree, `aria-hidden` here is redundant, whereas the `.st--corrected`/`.st--alone` state chips get the *same* protection with *no* `aria-hidden` at all — an inconsistent technique across two elements achieving the identical outcome. Worth normalising for the next author who copies one pattern and not the other, since the inconsistency only stays harmless as long as every row keeps an `aria-label`.)

---

## 3. `.fchip` filter row and the evidence index

### PASS — pressed state is exposed as a real toggle, not colour alone, in the accessibility tree

```html
<button type="button" class="fchip" data-f="Kayak" aria-pressed="false">Kayak</button>
```
`role=button` (implicit) + `aria-pressed` is the correct semantic toggle pattern; screen readers announce "pressed"/"not pressed" independent of any visual styling.

### PASS — JS re-syncs `aria-pressed` on every chip, on every change

```js
wrap.querySelectorAll('.fchip').forEach(function(b){
  b.setAttribute('aria-pressed', String(b.dataset.f === active));
});
```
Runs inside `apply()`, called on every click — so exactly one chip is ever `true` and all others are explicitly reset to `false` (never left stale).

### PASS — `.themegroup` separator rows are hidden with the `hidden` property, reinforced by CSS, not visual-only

```js
if (tr.classList.contains('themegroup')) { tr.hidden = !!active; return; }
```
```css
.idx tr[hidden] { display: none; }
```
The explicit CSS override matters because a bare `hidden` attribute on a `<tr>` can lose to the table's default `display: table-row` in some engines — the stylesheet closes that gap.

### WARNING — the filter match is a substring test against the *entire row's text*, not the competitor cell, so it can report false positives (functional bug with an accessibility consequence: WCAG 4.1.3 Status Messages — the announced count can be wrong)

```js
var hit = !active || (tr.textContent || '').indexOf(active) !== -1;
```
`tr.textContent` includes the claim cell, so filtering by "Booking.com" also matches any row whose *claim text* happens to mention Booking.com even when the row's own competitor is someone else — e.g. `idx-72` ("**Rentalcars.com** states on its own homepage that it is part of Booking Holdings — the same parent as **Booking.com**, competitor 1") would appear under a `Booking.com` filter alongside genuine Booking.com rows. This inflates both the visible row count and the number spoken by the live region (`#filter-status`, "N of 121 findings shown, filtered by Booking.com"). Sighted users can at least visually spot the wrong competitor name in the row; screen-reader users hear only a possibly-wrong count with no easy way to audit it row-by-row. **Fix:** match against the competitor `<th>` cell specifically, not `tr.textContent`.

### WARNING — the zero-results recovery instructions are not part of the announced status message (WCAG 4.1.3 Status Messages, partial)

```js
var none = document.createElement('p');
none.className = 'fnone'; none.hidden = true;
none.textContent = 'No finding matches this filter. Clear a filter to see the rest — every one of the 121 findings is still here.';
...
none.hidden = shown > 0;
```
`.fnone` has no `role="status"`/`aria-live` of its own; only `#filter-status` is a live region, and its message is the terser `"0 of 121 findings shown, filtered by X"`. The richer recovery guidance in `.fnone` ("Clear a filter to see the rest") is not proactively announced — a screen-reader user only encounters it by continuing to read linearly past the (now-empty) table, which is a reasonable but not guaranteed path. **Placement is fine** (`.fnone` is inserted immediately after `<table class="idx">`, i.e., exactly where the emptied table used to have content) — it's the *announcement*, not the position, that's incomplete. **Fix:** either merge the two messages into the one live-region update, or add `aria-live="polite"` to `.fnone` itself.

### Info — only 8 of the 17 roster competitors have a filter chip

`Kayak, Booking.com, Airbnb, Iberia, Expedia, Google Travel — Flights vertical, Qatar Airways, Google Travel` — the other named competitors in the evidence index (American Airlines, Citymapper, Hopper, Omio, Rentalcars.com, Rome2Rio, Skyscanner, Trainline, Tripadvisor, TripIt) have no corresponding chip. Not a WCAG issue on its own (a partial filter set is not inaccessible), but worth flagging since it bears on the correctness concern above — a user trying to isolate one of the un-chipped competitors has no way to do so via this control at all.

---

## 4. `.ledger` — the six-pair `<dl>`

### PASS — `dl > div > dt + dd` nesting is spec-legal

```html
<dl class="ledger">
  <div><dt>17<span class="of">/17</span></dt><dd>competitor products touched...</dd></div>
  ...
</dl>
```
The HTML Living Standard explicitly permits wrapping each name/value group of a `<dl>` in a `<div>` (added specifically to allow styling hooks like this one) — this is not a legacy `<dl><dt><dd>` structure retrofitted incorrectly, it is the currently-specified form. Browsers preserve the term/definition relationship through the wrapper.

### PASS — reading order pairs each number with its sentence correctly

DOM order inside each `<div>` is `<dt>` (the number) then `<dd>` (the sentence), matching the CSS grid's visual left-to-right layout (`grid-template-columns: 5.5rem 1fr`) — satisfies SC 1.3.2 Meaningful Sequence.

### Info — `17<span class="of">/17</span>` concatenates to "17/17" with no separation for assistive tech

```html
<dt>17<span class="of">/17</span></dt>
```
No `aria-label` override and no `aria-hidden` on `.of` — a screen reader reads the `<dt>`'s full text content, "17/17", exactly as written (synthesizer-dependent whether the `/` is spoken as "slash" or a pause). This is legible but not maximally clear; not a WCAG failure, just worth a designer's attention given how much this board cares about exact-figure precision — consider `aria-label="17 of 17"` on the `<dt>` if the intent is that this be *heard* the way the surrounding prose reads it ("17 of 17"), which is how sighted users are meant to parse the compact `17/17` glyph.

---

## 5. Global theming — `::selection`, `caret-color`, `accent-color`, `scrollbar-color`; and `prefers-reduced-motion`

### PASS — every new transition in the widget layer is wired through the reduced-motion-aware duration tokens

```css
@media (prefers-reduced-motion: reduce) {
  :root { --dur-fast: 0ms; --dur-reveal: 0ms; --dur-dismiss: 0ms; }
  html { scroll-behavior: auto !important; }
}
```
Checked every `transition:` declaration touching the audited widgets — `.row { transition: background var(--dur-fast) ...}`, `.fchip { transition: background var(--dur-fast) ...}`, `.panel { transition: transform var(--dur-reveal) ..., opacity var(--dur-reveal) ...}`, `.rail a`, `.skiplink` — all reference `--dur-fast`/`--dur-reveal`/`--dur-dismiss`, none hardcodes a duration. None of the audited widgets defines an independent, un-tokenised transition or CSS animation that would escape this override. The chain-diagram's dim/highlight effect (`#chain-svg.tracing .chain-node:not(.on) { opacity: 0.28; }`) has no `transition` property at all, so it's an instant state change with nothing to reduce. This is a genuine, verified pass — not merely "the variable exists somewhere," but confirmed to be the *only* mechanism driving every timed effect in scope.

### WARNING — NEEDS RENDER: filter-chip pressed state has no non-colour differentiator and is at risk under forced-colors / Windows High Contrast Mode (WCAG 1.4.1 Use of Color, forced-colors robustness)

```css
.fchip[aria-pressed="true"] { background: var(--ink); color: var(--raised); border-color: var(--ink); }
.fchip[aria-pressed="true"]::before { content: ""; ...; background: var(--coral); ... }
```
Under ordinary rendering this passes 1.4.1 in the everyday sense — the ink/raised fill inversion is a luminance change, not a hue-only change, so common colour-vision deficiencies still perceive it. The specific risk is **forced-colors mode**, a Windows accessibility feature that overrides author `background-color`/`color`/`border-color` on ordinary elements with a fixed system palette, regardless of the visiting user's own colour perception. Every property this pressed-state relies on — fill, text colour, border colour, plus the decorative `::before` square — is exactly the category forced-colors neutralises, and there is no accompanying difference in border **style** (solid vs. dashed), weight, icon, or shape that would survive that override. There is also no redundant text or `aria-live` channel a *sighted* forced-colors user could fall back on (unlike the meter, below, which is backed by the row's own spoken-out-loud count). **I cannot render this** to confirm the actual collapse — no browser tool is available to this audit — so this is reported as a risk with a named closing condition, not an asserted failure: **someone with a Windows High Contrast Mode or `forced-colors: active` emulation pass needs to check whether pressed vs. unpressed chips remain visually distinguishable, and if not, add a `@media (forced-colors: active)` rule giving the pressed state a border-style or outline difference.** Owner: whoever runs the rendered-DOM verification pass already cited for contrast in this task (same pass, same tooling, one more check).

### Info — meter pips carry the same forced-colors risk but are self-mitigated

```css
.meter i { background: transparent; box-shadow: inset 0 0 0 1px var(--gray-60); }
.meter i.on { background: var(--ink); box-shadow: none; }
```
The "off" pip's only marker is an inset `box-shadow`, a property forced-colors mode commonly suppresses outright — but the meter is `aria-hidden="true"` and the count it visualises is *also* printed as ordinary text (`.row__n`, "5"), which forced-colors correctly remaps to system text colour. So even a total visual collapse of the pip on/off distinction loses no information for any user. No action needed; noted for completeness since the task asked the question directly.

### Info — `caret-color` and `accent-color` are currently inert

No `<input>`, `<textarea>`, `contenteditable`, checkbox, radio, range, or `<progress>` element exists anywhere in the audited page. `caret-color: var(--coral)` and `accent-color: var(--ink)` on `html` therefore have no observable effect today — dead styling, not a live risk. Worth knowing before any future form control is added to this artifact family, since neither has been forced-colors-tested.

### NEEDS RENDER — `::selection` and `scrollbar-color` theming, general check

Both are properties that Chromium-family browsers are documented to override under forced-colors (selection maps to system `Highlight`/`HighlightText`; scrollbars map to system scrollbar colours), so risk is low — but "documented to usually happen" is not the same as "verified on this page," and Firefox's forced-colors implementation differs in details from Chromium's. Folding into the same closing condition as the fchip finding above: one rendered pass under `forced-colors: active` (Windows High Contrast or the equivalent DevTools/Firefox emulation) covering all four themed properties (`::selection`, `caret-color`, `accent-color`, `scrollbar-color`) plus the fchip pressed state, owned by whoever runs the contrast verification pass this task was told to treat as already covered.

---

## Deferred items and their closing conditions (per standing rule SR-3)

| Deferral | What would close it | Owner |
|---|---|---|
| Forced-colors rendering of `.fchip[aria-pressed]`, `::selection`, `caret-color`, `accent-color`, `scrollbar-color` | One `forced-colors: active` render pass (Windows High Contrast Mode or browser emulation), screenshot or DOM snapshot confirming pressed/unpressed chips remain distinguishable | Whoever runs the existing rendered-DOM verification pass (same tooling already used for the contrast numbers cited in this task) |
| Whether the DETAIL panel-data JSON blob (embedded as a single very large `<script>`/data line before the behaviour script) contains any additional accessible-name or citation content not visible from the static row markup | A tool capable of reading or parsing that single oversized line — this audit's Read tool hit its per-call token ceiling on that exact line and could not open it | Whoever re-runs this audit with a tool not subject to a single-line size limit, or asks `build-dashboard.py`'s author to confirm the panel body/cite content matches what each row's `aria-label` already promises |

---

## Note on tool/scope limits actually hit

This audit could not open one line of the file (the embedded per-item detail-panel data, immediately before the behaviour `<script>`) because it exceeded this session's single-read token ceiling and the Read tool has no character-level offset within a line. Everything else audited above — every `.row` example, the full `.fchip`/filter script, the full evidence-index table, the `.ledger`, and the panel's open/close/focus logic — was read directly from the rendered HTML and its inline `<script>`, not inferred from `build-dashboard.py`. `build-dashboard.py` was not consulted for any finding in this report.
