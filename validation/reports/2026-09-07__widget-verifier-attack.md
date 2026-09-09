# Attack report — verify-widgets.mjs (new) and verify-charts.mjs (re-audit)

Target artifact: `artifacts/luma-hands-on/2026-09-07__dashboard__hands-on-findings-and-recommendations__v2/`
Attacker: system-keeper (did not author either checker). All work done in a copy at
`/private/tmp/claude-501/.../scratchpad/attack2/` — the real artifact directory was
never written to (confirmed by `git status`/`git diff --stat` before and after: the
only changes present are the ones already uncommitted by the main session before this
attack began).

## Headline count

**9 executable defects planted against real, rendered behaviour.**
- **6 CAUGHT** — verdict correctly flipped to FAIL: empty-pip fill, low-contrast row
  title, live border-left restore (substituted target, see below), forced page
  overflow, meter-only-carrier (number removed), and overflow verdict itself when
  triggered through the `.tablewrap` exemption.
- **3 MISSED outright** — a real, user-visible defect left the verdict at PASS:
  colour-alone filter-chip pressed state, and two exemption-loophole plants
  (`c-struct`, `c-cellbg`) in verify-charts.mjs.
- **1 target inapplicable** — `.card--evidence` is dead CSS with zero live matches in
  the current build; substituted a live selector to prove the underlying mechanism
  still works (it does).
- **1 diagnostic-only defect** — the overflow verdict fired correctly, but the
  exemption hid the true culprit from the reported element list and named the wrong
  element instead.
- **Backslash hunt: nothing found broken.** Every remaining `\\` in both files is
  correctly double-escaped for the one level of re-parsing they need (outer JS
  template literal → CDP `Runtime.evaluate` on the browser). Proved by execution, not
  by reading, including reproducing the historical bug pattern in a throwaway copy to
  confirm what it would look like if it came back.
- **All 5 claimed counts (57 rows, 8 chips, 0 thick borders, 183 panel entries, 121
  index rows) independently verified against the raw HTML by grep / JSON-parse — not
  by trusting the verifier's own report.** All 5 confirmed accurate.

I could not defeat every exemption I tried (the `.tablewrap` overflow gate itself held
even under an active CSS-neutralising attack), and I list every attempt below,
including the ones that produced nothing, per the standing instruction that "I read it
and it looks correct" is a failed attestation.

---

## BLOCKER

### F1 — `c-struct` exemption in verify-charts.mjs hides a real, already-shipped, unlabeled data mark

**Reproduction:**
```
cd <copy>/2026-09-07__dashboard__.../
# in charts.py, chart_quadrant(), before the real PTS loop:
python3 - <<'EOF'
path = "charts.py"
s = open(path).read()
old = '''    for name, ax, lvl in PTS:
        x, y = L0 + axw * ax / mx, B0 - axh * lvl / 4
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{L.gray("100")}"/>')'''
new = '''    o.append(f'<circle cx="{L0+axw*9/mx:.1f}" cy="{B0-axh*3.5/4:.1f}" r="6" '
             f'class="c-struct" fill="{L.gray("20")}"/>')
    for name, ax, lvl in PTS:
        x, y = L0 + axw * ax / mx, B0 - axh * lvl / 4
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{L.gray("100")}"/>')'''
open(path, "w").write(s.replace(old, new))
EOF
python3 build-dashboard.py
node verify-charts.mjs
```
**Observed:** `verdict: "PASS"`, `failures: []`, `declaredExemptions.structural: 192`
(up from the baseline 191 — my circle was silently absorbed). `marks.checked` stayed
at 485 (unchanged) — my circle was never evaluated as a real mark at all.

A completely fabricated 6th competitor data point, unlabeled, plotted at a genuinely
invisible contrast against the page ground, is fully exempted from the 3:1 mark floor
by adding one class attribute. There is no check that the element is actually axis
geometry (a thin line/rect repeated N times to match N axis levels) versus an
arbitrary shape; the exemption trusts the class name alone.

**This is not hypothetical — the same pattern already exists in the shipped chart.**
Without any plant, `chart_effort`/`chart_axes` (the "ways to reorder results" bar
chart, figure `ch-axes`) draws its **total-count bar** — the bar whose length is the
primary magnitude encoding for "how many sort options exist" — with `class="c-struct"`
(charts.py ~line 916: `o.append(f'<rect class="c-struct" ... fill="{other}"/>')`).
Measured on the real render:
```
node probe.mjs "(() => {
  const px = s => { const m=(s||'').match(/[\d.]+/g); if(!m||m.length<3) return null; const n=m.slice(0,3).map(Number); return s.startsWith('color(')||s.startsWith('rgb(')===false?n:n.map(v=>v/255); };
  const lin=v=>v<=0.04045?v/12.92:Math.pow((v+0.055)/1.055,2.4);
  const Y=c=>0.2126*lin(c[0])+0.7152*lin(c[1])+0.0722*lin(c[2]);
  const cr=(a,b)=>{const x=Y(a),y=Y(b),hi=Math.max(x,y),lo=Math.min(x,y);return (hi+0.05)/(lo+0.05);};
  const ground = px(getComputedStyle(document.body).backgroundColor);
  const els=[...document.querySelectorAll('figure.chart svg .c-struct')].filter(e=>e.getAttribute('h')||e.getAttribute('height')==='16');
  return els.map(e=>({w:e.getAttribute('width'), ratio: +cr(px(getComputedStyle(e).fill), ground).toFixed(2)}));
})()"
```
Result: bars 372.0 / 202.9 / 101.5 / 202.9 / 101.5 wide, all at **1.45:1** against the
page ground — a bar chart whose bars are, for practical purposes, invisible. It is
partially mitigated by a redundant printed "`{effort} of {total}`" label beside each
row, but the visual bar itself — the thing a bar chart exists to let you compare by
eye — carries no readable contrast, and `verify-charts.mjs` reports this as `PASS`
inside `declaredExemptions` with `worstStructuralRatio: 1.12` for the whole file
(driven by legitimate axis tracks, masking this bar's near-identical near-invisibility
in the aggregate number).

**Fix direction (not implemented — reporting only):** the exemption should require
either (a) the element repeats exactly once per declared axis/tick (countable and
checkable against a known N), or (b) a naming convention that separates "track"
elements from "value" elements, so a bar whose width is computed from a data value
(`bw = axw * total / mx`) cannot carry the same class as a fixed axis line.

---

### F2 — `c-cellbg` exemption is exploitable and is *not even reachable* by the one check meant to backstop it

**Reproduction:**
```
python3 - <<'EOF'
path = "charts.py"
s = open(path).read()
old = '''    for name, ax, lvl in PTS:'''
new = '''    o.append(f'<rect x="{L0+axw*7/mx:.1f}" y="{B0-axh*2.5/4-30:.1f}" width="20" height="20" '
             f'class="c-cellbg" fill="{L.gray("20")}"/>')
    for name, ax, lvl in PTS:'''
open(path,"w").write(s.replace(old,new,1))
EOF
python3 build-dashboard.py
node verify-charts.mjs   # x3, all identical
```
**Observed (3/3 runs):** `verdict: "PASS"`, `failures: []`,
`declaredExemptions.matrixCellFills: 60` (up from baseline 59),
`redundantEncoding: {shadedCells: 59, numbersPrinted: 59, ok: true}` — **unchanged**.

The comment in verify-charts.mjs justifies exempting `.c-cellbg` from the 3:1 floor
because "the number's own contrast is checked separately above," and a *separate*
check (#5, "colour is never the sole channel") verifies `shadedCells === numbersPrinted`
— but that check is hard-scoped to `#ch-matrix rect` only. A `.c-cellbg` element placed
**anywhere else in any chart** (as I did, inside `ch-quadrant`) is exempted from the
contrast floor by the mark-contrast loop (which scans `figure.chart svg` broadly) but
invisible to the redundancy loop (which only looks inside `#ch-matrix`). The two
checks that are supposed to compose into one guarantee ("exempt from contrast, but
provably redundant") do not actually share scope — `c-cellbg` outside the matrix gets
the exemption with none of the backstop.

---

## ERROR

### F3 — verify-widgets.mjs never simulates interaction; the exact defect its own comment describes as guarded-against ships undetected

**Reproduction:**
```
python3 - <<'EOF'
path = "build-dashboard.py"
s = open(path).read()
old = '''.fchip[aria-pressed="true"] {{ background: var(--ink); color: var(--raised);
  border-color: var(--ink); }}
.fchip[aria-pressed="true"]::before {{ content: ""; display: inline-block;
  width: var(--s03); height: var(--s03); background: var(--coral);
  margin-right: var(--s02); vertical-align: baseline; }}'''
new = '''.fchip[aria-pressed="true"] {{ color: var(--coral-text); }}'''
open(path,"w").write(s.replace(old,new))
EOF
python3 build-dashboard.py
node verify-widgets.mjs
```
**Observed:** `verdict: "PASS"`, `worstChipContrast: 18.84` (unchanged from baseline).

Section 3 of the PROBE says in its own comment: "the pressed state must not be
colour-alone (it also inverts ground and gains a leading block)." The code beneath it
implements none of that claim — it only computes `Math.min` contrast across
`document.querySelectorAll('.fchip')` as rendered at page load. Confirmed by direct
probe that **every chip is `aria-pressed="false"` on load** — no filter is
pre-selected — so the pressed branch of the CSS is never even read, let alone checked
for a structural (non-colour) differentiator:
```
node probe-async.mjs "(async () => { const c=document.querySelector('.fchip');
  c.click(); await new Promise(r=>setTimeout(r,200));
  return {pressed:c.getAttribute('aria-pressed'),
          bg:getComputedStyle(c).backgroundColor,
          color:getComputedStyle(c).color,
          before:getComputedStyle(c,'::before').content}; })()"
# -> {"pressed":"true","bg":"color(srgb 1 1 1)","color":"...coral...","before":"none"}
```
After the click, background is unchanged white, `::before` content is `none` — under
the plant, the pressed chip differs from the unpressed one **only by text colour**,
which is exactly the WCAG 1.4.1 "use of colour" failure the code comment claims to
defend against, and `verify-widgets.mjs` never observes it because it never clicks
anything. This is a structural gap, not a threshold-tuning issue: no row-expand state,
no chip-pressed state, no meter/board post-filter state is ever exercised by this
verifier — it checks the page exactly as it loads, twice (two viewports), and nothing
else.

---

## WARNING

### F4 — verify-charts.mjs is flaky: one observed false FAIL on an unmodified, previously-passing build

Mid-session, immediately after restoring `charts.py`/`build-dashboard.py` to their
exact originals (byte-for-byte, confirmed via `cp` from a preserved `.orig`), a single
run of `node verify-charts.mjs` reported:
```
"clippedTexts": 1,
"failures": ["clipped text in ch-effort: \"findings indexed · 0–18\""],
"verdict": "FAIL"
```
on a file that had passed cleanly at the top of this session and passed cleanly
**5/5 times** immediately afterward with zero code changes in between. This is
consistent with a render-timing race against the fixed `setTimeout(r, 2500)` wait
before `evaluate()` reads `getBoundingClientRect()` on SVG text — a font/layout settle
that occasionally isn't done at 2.5s. Not reliably reproducible (1 failure in 9 total
runs across this session), but real: it fired against known-good input. **A gate that
can flip red on unchanged input cannot be trusted from a single run** — if this is used
as a CI gate, either raise the wait, poll for layout stability, or run it N times and
require unanimous PASS before trusting a red result as real.

### F5 — the `.tablewrap`/`.chart-body` overflow exemption can hide the true culprit even when the verdict itself stays correct

**Reproduction:**
```
# inject inside <main>, a real defect that survives the .tablewrap CSS containment:
<div class="tablewrap" style="overflow-x: visible;">
  <div style="width:2200px;height:10px;background:red;"></div>
</div>
```
**Observed:** `overflowsX: true`, `verdict: "FAIL"` (correct — the boolean check is not
gated by the exemption) but `overflowingElements: []` on desktop and
`overflowingElements: ["CODE"]` on narrow — the actual offending `<div>` is filtered
out of the report by `closest('.tablewrap, .chart-body')`, and an unrelated `<code>`
element is named instead. **The gate does not produce a false PASS here**, but the
diagnostic list a human would use to find and fix the defect points at the wrong
element or nothing at all. Rated WARNING, not ERROR, because the fail-safe property
(never silently PASS a real page-level overflow) held in every variant I tried.

**Two other overflow-exemption attempts produced no defect at all (reported honestly,
not as findings):**
1. A 2000px child placed directly inside a real `.tablewrap` (no CSS override) does
   not overflow the page — Chrome genuinely contains it via the class's own
   `overflow-x: auto`, so there was nothing to hide. Correct behaviour, not a loophole.
2. A 2000px-wide `position: fixed` child inside `.tablewrap` does not contribute to
   `document.documentElement.scrollWidth` in Chromium regardless of ancestor overflow
   — not a property of this exemption, a general browser behaviour. No defect existed
   to be hidden.

I did **not** find a way to defeat the `.tablewrap`/`.chart-body` overflow exemption
into a false PASS. Listed per the instruction that a failed attack must be reported as
failed, not omitted.

I also did not attempt to defeat the **rotated-text exemption** in verify-charts.mjs
(clip/overlap checks) — ran out of scope in this pass. This is an **untested**
exemption, not a cleared one; flagging explicitly rather than letting silence read as
"checked."

---

## INFO

### F6 — planted defect (c) targets dead code; substituted a live target to prove the mechanism itself is sound

`.card--evidence` (and `.card`, `.card--pain`) exist only in the CSS
(`build-dashboard.py:1193`, `1186`) and in two Python render functions
(`render_finding_card`, `render_pain_card`, lines 696–730) that are **defined but
never called** anywhere in `build-dashboard.py`. Confirmed by grep on the rendered
HTML: `class="card"` (bare or with any modifier) appears **zero times**; the findings
and pain-point sections are rendered through the newer `.row`-based `render_row()`
path instead. Restoring a 3px coloured border-left on `.card--evidence` therefore
changes a CSS rule with **no matching element in the DOM** — `thickBorderCount`
correctly stayed at 0, not because the checker missed it, but because there was
nothing on the page to catch.

To confirm the border-left check itself is not the thing that's broken, I planted the
same defect against a live selector instead:
```
# build-dashboard.py: .row rule
- background: transparent; border-left: 0; border-right: 0; border-top: 0;
+ background: transparent; border-left: 3px solid var(--coral); border-right: 0; border-top: 0;
```
`node verify-widgets.mjs` → `thickBorderCount: 57`, `sel: "row"`, `verdict: "FAIL"` —
correctly caught. The check works; the target named in the task no longer exists in
the shipped markup. Recommend either removing the dead `.card*` CSS and render
functions, or noting in a comment that they're retained for a future card-mode.

### F7 — backslash-consumption hunt: nothing found broken in either file

Every backslash in both PROBE template literals is doubled (`\\d`, `\\s+`, `\\n`),
found by exhaustive scan:
```
python3 -c "
import re
for f in ['verify-widgets.mjs','verify-charts.mjs']:
    for i,l in enumerate(open(f),1):
        for m in re.finditer(r'\\\\+', l): print(f, i, repr(m.group()))
"
# -> verify-widgets.mjs:35, verify-charts.mjs:42,60,181 — all '\\\\' (double), none single
```
This is the **correct** escaping for a JS template literal whose contents are later
re-parsed as JS by the browser (one level of literal processing at file-parse time,
one level at `Runtime.evaluate` time — hence exactly two backslashes needed to deliver
one to the regex/string engine that actually uses it). Proved by execution, not
inspection:
```
node probe.mjs "(() => { const t='the quick brown  fox\njumped over';
  return {correct: t.split(/\s+/).length, broken: t.split(/s+/).length}; })()"
# -> {"correct":6,"broken":1}
node probe.mjs "(() => { const c='rgb(12, 34, 56)';
  return {correct: c.match(/[\d.]+/g), broken: c.match(/[d.]+/g)}; })()"
# -> {"correct":["12","34","56"],"broken":null}
```
confirming what a single-consumed backslash would actually produce (a regex matching
almost nothing, or `null`), and it is not what these files' real output looks like
(`descWords: 149`, `matrixCells.worstRatio: 5.02`, `csvRows: [121,18,5]` — all sane,
non-degenerate numbers).

To prove the danger is real (not just theoretical), I reproduced the historical bug in
a **disposable copy** (`verify-charts-brokenbug.mjs`, never touching the real file) by
de-doubling one backslash:
```
- descWords: desc ? desc.textContent.trim().split(/\\s+/).length : 0,
+ descWords: desc ? desc.textContent.trim().split(/\s+/).length : 0,
```
Result: `descWords: 47` instead of the true `149` — **silently wrong, no exception
thrown**, and because `descWords` is reported but not gated by any threshold in
`out.failures`, this would never surface as a FAIL even though the number is
meaningless. This confirms C-side of the historical bug class (silent corruption, not
a crash) without finding any live instance of it in the current files.

### F8 — count claims independently verified against the built HTML, not against the verifier's own report

```
H=luma-competitor-research-findings.html
grep -o 'class="row"' "$H" | wc -l        # -> 57   (claim: 57 rows)
grep -o 'class="fchip"' "$H" | wc -l      # -> 8    (claim: 8 filter chips)
grep -oE 'border-(left|right)-width:\s*[0-9]+px' "$H"
grep -oE 'border-(left|right):\s*[0-9]+px' "$H"      # -> all "1px", none higher
                                                       # (claim: 0 borders above 1px)
python3 -c "
import re,json
html=open('$H').read()
m=re.search(r'<script type=\"application/json\" id=\"panel-data\">(.*?)</script>', html, re.S)
print(len(json.loads(m.group(1))))"        # -> 183  (claim: 183 panel entries)
python3 -c "
import re
html=open('$H').read()
b=re.findall(r'<pre class=\"csv\"[^>]*>(.*?)</pre>', html, re.S)[0]
print(len(b.strip().split(chr(10)))-1)"    # -> 121  (claim: 121 index rows)
```
One non-finding worth recording: a naive grep for `border:\s*3px` also matches
`*::-webkit-scrollbar-thumb { ...; border: 3px solid var(--ground); }` in
build-dashboard.py:1148. This is **not** a violation of the "0 borders above 1px"
claim — `::-webkit-scrollbar-thumb` is a UA-shadow pseudo-element, not selectable via
`document.querySelectorAll('*')`, and correctly outside both the checker's and this
grep-based independent check's real scope. Flagging only so the false lead doesn't get
rediscovered and mis-reported as a miss by a future audit.

**All five claimed counts (57, 8, 0, 183, 121) are independently confirmed accurate.**

---

## What I did not manage to break, stated plainly

- The `.tablewrap`/`.chart-body` overflow **verdict** (the FAIL/PASS boolean) held under
  every attack I tried, including an active CSS-neutralising one (F5). Only the
  diagnostic culprit list was misled, not the gate itself.
- Could not find any live (currently-shipping) instance of the double-backslash bug
  class in either file — both are correctly escaped everywhere, confirmed by
  execution against real page content and by a reconstructed control case.
- Did not attempt to defeat the rotated-text clip/overlap exemption in
  verify-charts.mjs — out of scope for this pass, reported as untested rather than
  silently passed over.

## Files touched (attacker's scratch copy only — never the artifact directory)

- `/private/tmp/claude-501/-Users-raquelpalis-Projects-coforge/a9b9d131-97fa-4873-9b40-2f9c05bad2bf/scratchpad/attack2/2026-09-07__dashboard__hands-on-findings-and-recommendations__v2/` — full working copy, all plants applied and reverted here
- `verify-charts-brokenbug.mjs` and `probe-async.mjs` inside that copy — throwaway control-test scripts, not part of the real artifact

No file under `/Users/raquelpalis/Projects/coforge/artifacts/...` was modified by this
attack; `git status`/`git diff --stat` on the real directory before and after show only
the pre-existing uncommitted changes that were already there when this task started.
