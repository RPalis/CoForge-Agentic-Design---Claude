# Validation — ART-026 · dashboard · hands-on-findings-and-recommendations · v1

**Payload:** `luma-competitor-research-findings.html` · **Produced by:** `dashboard-analyst` ·
**Date:** 2026-09-04 · **Status:** draft · **Gate:** B (automated, see §4) · **Supersedes:** none

Renders `ART-025` (hands-on competitor UX capture, round 1 — `WORLD.json`, `CAPTURE-INDEX.json`,
`ROUND-LEARNINGS.md`, `ALL-COMPANIES-PLAN.md`, and the 50 files under `captures/`, which are the
source of truth). No claim here has passed Gate A. `research/evidence-ledger.json` was not opened
and holds zero records — every citation on this board is a capture-file path, never `[E-nnn]`.

---

## 0. What this artifact is, and the structural problem it solves

Findings, pain points, insights, recommendations and next steps from the round, kept in two
registers that are never mistakable for each other: **Evidence** (Findings, Pain points — captured,
confidence-rated, traced to a named capture file) and **Synthesis** (Insights, Recommendations, Next
steps — reasoning on the evidence, unverified, not through Gate A). Every single card carries its
register as a one-word text chip (`Evidenced` / `Synthesis` / `Method`) **and** a distinct border
shape (plain / solid coral left accent / dashed on a shaded background) — never colour alone — so a
screenshot of one card cropped out of any context still states which kind of claim it is, per the
brief's own test.

`build-dashboard.py` (beside this file) is the generator. It is part of this artifact, not a
throwaway script: the prior dashboard family (ART-013..ART-023) had no generator anywhere in the
repository, which that family's own v5 `validation.md` names as the root cause of C-039 — a
hand-truncated cell going unpatched at the source because no source existed to patch. Re-running
`python3 build-dashboard.py` reproduces `luma-competitor-research-findings.html` directly from
`WORLD.json`, `CAPTURE-INDEX.json` and `design-system/tokens/tokens.json`; it asserts the 121-row
evidence-index count and the frozen tokens hash at build time and fails loudly if either drifts.

---

## 1. Corrections to the brief — checked against the data, not assumed

Per instruction: "Correct anything in this brief the evidence contradicts." Four corrections were
necessary; none is cosmetic.

**1.1 — The confidence tri-state the brief assumes is not what the data contains.**
The brief describes findings as "confidence-rated (`Verified` / `Likely` / `Not Verified`)". That
*was* the research plan's design — `ALL-COMPANIES-PLAN.md` states "Confidence is `Verified` /
`Likely` / `Not Verified`" outright. It is not what execution produced. Checked directly against
all 50 capture files:

```
$ grep -roh '"confidence": "[^"]*"' captures/ | sort | uniq -c | sort -rn
    169 "confidence": "Verified"
      2 "confidence": "Verified for the homepage surface"
      1 "confidence": "Verified — first-party statement on the product's own homepage."
      ... (≈20 distinct compound strings, each "Verified [that X]... Y is Inferred/UNKNOWN/NOT verified")
      1 "confidence": "Likely"
```

`"Not Verified"` appears **zero** times across all 50 files. `"Likely"` appears exactly **once**
(`captures/02-expedia/01-site-tree-L1.json`) and is corrected to a plain `Verified` finding within
the same round (`captures/02-expedia/02-loyalty-one-key.json`; see Method notes M5 on the board).
Rendering the brief's assumed tri-state would either invent a "Not Verified" tier that never occurs,
or collapse ~20 informative compound caveats into a bare "Verified" that discards the qualification
that made each one honest. This board renders three tiers that match what is actually there —
**Verified**, **Verified — qualified**, and **Method note** — and states this correction on the page
itself (Meta § "On confidence tiers"), not only here.

**1.2 — "The scenario's own problem list is in `WORLD.md` §1" does not hold.**
Read `WORLD.md` §1 in full: it contains the product framing (eight journey stages, five primary
users, eight business goals, constraints) and nothing enumerable as a "problem list." Pain points on
this board are derived directly from findings instead — which the brief itself names as the primary
method, so nothing is lost, but the board does not claim a quote from a document that does not
contain one.

**1.3 — `CAPTURE-INDEX.json` counts 121 findings; `WORLD.json` only fully carries 117.**
```
$ python3 -c "..."
117 chunks in WORLD.json; 121 findings in CAPTURE-INDEX.json
in CAPTURE-INDEX not WORLD: {'CORRECTION_to_F28', 'correction_to_own_earlier_claim',
                             'F71_AIRCOVER_IS_NOT_SHOWN_AT_THE_DECISION_REFUTES_PRIOR_CLAIM',
                             'method_correction'}
```
All four are real findings with a `claim` field of the literal string `"see capture file"` in
`CAPTURE-INDEX.json` — a generation artifact, not a disagreement. All four are resolved in
`build-dashboard.py`'s `STUB_RESOLUTIONS` dict directly from their named capture file (per the
source manifest's own rule: "where it disagrees with a capture file, the capture file wins"), with
real claim text, confidence, why-it-matters and scope-limit fields quoted from the capture. The Full
evidence index therefore carries all 121 items CAPTURE-INDEX.json counts, none as a placeholder.

**1.4 — The ART-017 focus-ring defect is real, and does not apply here.**
The brief states: `semantic.focus` on `teal.60` is 1.003:1, use the two-tone ring. Measured directly
(`verify-encoding.py`): confirmed, 1.003:1 exactly, reproducing ART-017's own finding. But this board
places no focusable element on a teal (or any ordinal/sequential) colour fill — the one chart it
carries (the five coverage ratios) uses ink-length bars against a bone track, not colour-coded cells
— so the two-tone ring `cf-unit-cell` requires never actually triggers. Recorded explicitly on the
page (Meta) and here, so a reader does not have to guess whether it was overlooked.

---

## 2. Content — what each register carries

| Section | Register | Count | Encoding |
|---|---|---:|---|
| Coverage | — (the caveat itself) | 5 ratios + 5 KPIs | Ink-length bars, direct % labels, click-to-pin |
| Findings | Evidence | 15 curated cards, 5 sub-groups | Plain-bordered cards, confidence chip |
| Pain points | Evidence | 10 cards | Plain-bordered cards, confidence chip |
| Insights | Synthesis | 7 cards | Coral-left-border cards, `Synthesis` chip + weakest-confidence chip |
| Recommendations | Synthesis | 9 cards | Coral-left-border cards, names finding(s), states what it rests on |
| Next steps | Synthesis | 6 cards | Coral-left-border cards |
| Method & corrections | Method (neither register) | 10 cards | Dashed-border cards on a shaded background |
| Full evidence index | Evidence | 121 rows | Grouped-by-theme table, full claim text (never truncated), click-to-pin |

**183 click-to-pin triggers total** (`grep -c 'data-detail='` confirms), each opening
`cf-detail-panel` with full provenance: confidence, scope limit (where one exists), why it matters,
any decision the evidence poses, the verbatim evidence quote, and the exact capture-file path.

**Every recommendation names the finding(s) it rests on and states the weakest confidence among
them explicitly** — e.g. Recommendation 1 (Trainline compensation notification) states "Rests on one
Verified capture, in rail... a single-competitor, single-vertical proof, not a corroborated
pattern"; Recommendation 7 (model the trip as one object) states it inherits F68's weaker compound
confidence rather than the plain-Verified F78/F101 it also cites. No recommendation is silent about
resting on a single capture.

**The coverage asymmetry reaches Recommendations directly**, not only by cross-reference: a
`.reminderbanner` restates the exact numbers (6 of 17 walked to payment, 4 of 17 both browsers, 8 of
119 state observations) at the top of the Recommendations section itself, in the section a reader
taking action is most likely to read without scrolling back up.

---

## 3. Encoding contract — re-derived, not asserted

```
$ python3 verify-encoding.py
```
```
tokens.json canonical sha256: 1926c393fe83742443350f2aa4e8d5dd3d0d6d7393a31c93e2f74317cada1a7f
expected (frozen baseline):   1926c393fe83742443350f2aa4e8d5dd3d0d6d7393a31c93e2f74317cada1a7f
MATCH

Pair                                                              Ratio   Floor  Result
--------------------------------------------------------------------------------------------
ink on ground (body text)                                       15.946:1   4.5:1  PASS
ink-2 on ground (secondary text)                                 6.614:1   4.5:1  PASS
border-strong on ground (structural edges)                       4.253:1   3.0:1  PASS
link on ground                                                   6.598:1   4.5:1  PASS
link on raised                                                   7.795:1   4.5:1  PASS
focus on ground (outer ring)                                     4.234:1   3.0:1  PASS
focus on raised (outer ring)                                     5.002:1   3.0:1  PASS
ink on raised                                                   18.838:1   4.5:1  PASS
ink-2 on raised                                                  7.814:1   4.5:1  PASS
border-strong on raised                                          5.025:1   3.0:1  PASS
ink on rail-bg                                                  17.127:1   4.5:1  PASS
rail-bg on ground (non-text, structural only)                    1.074:1          n/a
coral-text on ground (synthesis-register accent text)            5.175:1   4.5:1  PASS
coral-text on raised                                             6.114:1   4.5:1  PASS
coral fill on ground (decorative border only, non-text)          2.817:1          n/a
ink on layer-accent-01 (chip label)                             14.270:1   4.5:1  PASS
border-strong on layer-accent-01 (chip outline)                  3.806:1   3.0:1  PASS
raised(white) text on gap-90 (method-note dark row)             15.134:1   4.5:1  PASS
border-strong on rail-bg (method-card chip outline)              4.569:1   3.0:1  PASS
ink-2 on rail-bg (method-card secondary text)                    7.104:1   4.5:1  PASS
coral fill on rail-bg (n/a check -- synthesis never sits on rail-bg) 3.026:1        n/a

VERDICT: PASS -- every load-bearing pair clears its WCAG 2.2 AA floor

Checked for the ART-017 defect (semantic.focus at 1.003:1 on palette.teal.60):
  focus vs teal.60 = 1.003:1 -- LOW, confirms the defect is real
  This dashboard places no focusable element on a teal (or any ordinal) fill,
  so the two-tone ring is not required here.
```

`cf-chart-palette` is not used anywhere (`grep -c chart-palette` → 0). No raw hex
(`grep -noE '#[0-9a-fA-F]{3,8}\b' … | grep -v '&#'` → empty — the `$358.59` figure quoted from
Expedia's own confirmshaming copy is a dollar amount and does not match a hex pattern at all). No
raw px on `padding`/`margin`/`gap`/`border-radius`/`border-width` (`grep -noE
'(padding|margin|gap|border-radius|border-width)\s*:\s*[0-9]+px'` → empty; every spacing value is a
`var(--sNN)` custom property resolving to the frozen `spacing.*` scale).

**Every `chip--*` modifier class (`chip--verified`, `chip--qualified`, `chip--method`,
`chip--evidence`, `chip--synthesis`, `chip--likely`) carries zero CSS rules** —
`grep -n '\.chip--'` on the payload finds only `.chip--outline`. This is deliberate: `cf-chip`'s own
contract is "no colour variant by design... every chip looks identical whatever it says," and this
board's confidence/register chips differ by text alone, never by hue, so none of them can be
misread as a colour-coded verdict (D-001).

---

## 4. Interaction — driven live over Chrome DevTools Protocol, not read from source

```
$ "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
    --no-sandbox --remote-debugging-port=9333 --user-data-dir=<scratch-profile> about:blank &
$ node verify-interaction.mjs
```
```json
{
  "clickOpensPanel": { "panelOpen": true, "gridVisible": true,
    "titleText": "The more a product can sell you, the less of the real answer it shows." },
  "focusOnPanel": true,
  "escapeReturnsFocus": { "closed": true, "focusBack": true },
  "enterKeyParity": true,
  "closeButtonWorks": true,
  "indexRowsDistinct": { "count": 121, "allDistinct": true },
  "scrollspy": "#recommendations",
  "noFilterControls": true,
  "structure": { "mainCount": 1, "h1Count": 1, "captionCount": 1,
    "thScopeCount": 137, "dataDetailCount": 183 }
}
```

Two authoring-time false negatives in the **test script itself**, corrected and documented in
`verify-interaction.mjs`'s own comments rather than silently fixed: (1) an early version dispatched
the synthetic `Escape` `KeyboardEvent` on `document` directly — a real keypress can never target the
`Document` node itself, only the focused `Element`, so `document.closest` doesn't exist and the
handler threw before reaching the Escape branch; fixed to dispatch on `document.activeElement`,
which is what a real keypress does. (2) the scrollspy check waited 400ms after `scrollIntoView()`,
which is not long enough for `html{scroll-behavior:smooth}` to finish animating across an
~18,000px-tall page (this board's 121-row appendix makes it long); measured the real animation
duration directly and set the wait to 1800ms, confirmed sufficient. Neither was a defect in the
payload — both are noted so a future reader of this test script does not mistake a fixed harness bug
for a re-introduced one.

`noFilterControls: true` confirms zero real `<select>`/`<input>`/checkbox/radio elements exist in
the live DOM. `grep -inE '<select|<input'` on the raw file does find one textual match — the literal
string `<select>` appearing inside a quoted finding (F13, Booking.com's inert Reserve control) inside
the `#panel-data` JSON block, inside a `<script type="application/json">` element. Per the HTML5
spec, `<script>` content is raw text, not parsed as markup, so this is not an actual DOM element and
the live query above confirms it directly rather than trusting the source-level grep alone.

**Print**, verified with a real render, not asserted from source:
```
$ "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
    --no-sandbox --print-to-pdf=dashboard-print.pdf luma-competitor-research-findings.html
$ python3 -c "import fitz; d=fitz.open('dashboard-print.pdf'); print(d.page_count); ..."
53
has Meta heading: True
has Reviewed by: True
has On confidence tiers: True
has Full evidence index: True
```
Confirms the `beforeprint`/`afterprint` handling that forces the Meta `<details>` open actually
works on a live render (53 pages is expected: a 121-row full evidence index is long in print).

**Heading order** unbroken: 1 `<h1>` (visually hidden, screen-reader only), 10 `<h2>`, 69 `<h3>`
(five findings sub-heads + one per card across 15+10+7+9+6+10 = 57 cards + coverage/index/meta
sub-heads), zero `<h4>` or deeper — no level skipped. Every table carries a real `<caption>`
(2 tables: coverage detail is a row-list not a table; the Full evidence index table has one) and
every header cell carries `scope=` (137 occurrences, `th[scope]` counted live via DOM query).

---

## 5. Gate B — checklist

| Check | Result | Evidence |
|---|---|---|
| Directory named `YYYY-MM-DD__dashboard__<slug>__v<N>` | PASS | `2026-09-04__dashboard__hands-on-findings-and-recommendations__v1` |
| `manifest.json` present and valid | PASS | `id` ART-026, type `dashboard` registered in `_types.json` |
| `validation.md` present and filled in | PASS | this file |
| Every `[E-nnn]` citation resolves | PASS, vacuously | Zero `[E-nnn]` anywhere; ledger holds zero records |
| No raw hex / no raw px | PASS | §3 |
| Palette from tokens.json | PASS | §3, `verify-encoding.py`, frozen hash confirmed unchanged |
| No causal claim from correlational data | PASS | every Finding/Pain point is a count or a verbatim quote; every Insight/Recommendation is stated as reasoning, not as a proven causal chain |
| Component membrane | PASS | zero PascalCase tags anywhere (incl. inside the JSON block); `cf-chip`/`cf-nav-rail`/`cf-detail-panel` are level-1, promoted (ADR-022) — this board instantiates their contract as static HTML/CSS/JS, the only render surface CoForge has at Build Stage 2 |
| Every metric names its source and refresh cadence | PASS | every KPI/ratio carries a `[capture-file-path]` or `[WORLD.json § …]` citation; header states "static, tied to the 2026-09-04 capture session" as the refresh cadence |

## Gate A — human review

| Check | Result |
|---|---|
| Claims labelled Evidenced / Inferred / Assumption | PASS — every card carries an explicit register chip; Insights/Recommendations additionally state "reasoning on the evidence, not through Gate A" in their section intro and per-card |
| Assumptions block present and visible | PASS — Meta, forced open under print |
| Reviewed by: ______ Date: ______ | open — `draft` until a human signs |

---

## 6. Repository audit — before and after, diffed by finding

**Before** (captured with this artifact's own directory moved aside, so it reflects the repository
immediately before this dispatch touched anything):
```
$ python3 validation/audit-system.py
blocker 1 · error 1 · warning 5 · info 6 · skipped 0
VERDICT: FAIL
```

**After** (this directory fully written — payload, `build-dashboard.py`, `verify-encoding.py`,
`verify-interaction.mjs`, `manifest.json`, this file — and the registry rebuilt):
```
$ python3 validation/rebuild-registry.py
$ python3 validation/audit-system.py
blocker 1 · error 1 · warning 5 · info 6 · skipped 0
VERDICT: FAIL
```

**Diffed by `(severity, check, message)`, not by count:**
```
$ diff audit-before.txt audit-after.txt
(no output)
```
(`audit-before.txt` / `audit-after.txt`, captured verbatim, are not shipped inside this artifact
directory to avoid an infinite-regress provenance check on the audit transcripts themselves — the
exact commands above reproduce them.)

**This dispatch introduces zero new findings.** The pre-existing blocker (`ART-022 references
tokens but its manifest declares no tokens_version` — content-comms' file, unrelated to anything
this dispatch touched) and the pre-existing `attestation` error (check 5g —
this dispatch touched no validator, hook, or gate wiring, only files under this artifact's own
directory plus the standard `rebuild-registry.py` regeneration of `artifacts/_registry.json` /
`artifacts/ARTIFACTS.md`) are both named in the "before" run, captured with this directory absent,
proving neither is caused by this dispatch. All five warnings and all six info lines are likewise
identical before and after.

Per the standing instruction, this section is this dispatch's own account, not a substitute for an
independent attack on the result — "the author is the one person who cannot perform this check"
applies here as everywhere else in this repository.

---

## 7. Files in this artifact

| File | Purpose |
|---|---|
| `luma-competitor-research-findings.html` | the payload |
| `manifest.json` | provenance |
| `validation.md` | this file |
| `build-dashboard.py` | the generator — re-run it to reproduce the payload from source data |
| `verify-encoding.py` | re-derives every contrast ratio live from `tokens.json`; §3 |
| `verify-interaction.mjs` | drives the rendered page over CDP; §4 |

---

## Verdict

Gate B: **pass**. Gate A: **pending a named human** — in particular, the register split (Evidence
vs Synthesis) and the confidence-tiering scheme are this board's own encoding decisions (Assumptions
A-2, A-3 on the page) and should be confirmed by someone who can compare them against the full
`captures/` corpus directly. Status stays `draft`.
