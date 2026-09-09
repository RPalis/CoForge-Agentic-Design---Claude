# Validation — ART-010 · metrics-scorecard · agent-cost · v1

**Payload:** `agent-cost-scorecard.html` · **Produced by:** `dashboard-analyst` ·
**Date:** 2026-09-03 · **Status:** draft · **Gate:** B (automated)

Sole data input: `validation/agent-runs.json`.
Sole visual input: `design-system/tokens/tokens.json` release `0.2.0`, plus the binding
colour rule in `design-system/foundations/brand.md` §3.

---

## 1. Gate B — checklist

From `validation/checklists/metrics-scorecard.md`.

| Check | Result | Evidence |
|---|---|---|
| Directory named `YYYY-MM-DD__metrics-scorecard__<slug>__v<N>` | PASS | `2026-09-03__metrics-scorecard__agent-cost__v1` |
| `manifest.json` present and valid | PASS | parses; `id` ART-010, type registered in `_types.json` |
| `validation.md` present and filled in | PASS | this file |
| Every `E-nnn` citation resolves | PASS, vacuously | the payload contains none, and none was minted. `research/evidence-ledger.json` holds **0** entries; no user was asked anything and no person is quoted. See §7. |
| No raw hex / no raw px where the artifact is visual | PASS | 0 hex literals and 0 raw `padding`/`margin`/`gap`/`border-radius` px in the payload, asserted by the generator's own post-write scan. Read §4 before treating that as sufficient. |
| Claims labelled Evidenced / Inferred / Assumption | PASS | payload §"Claim format" and §"Assumptions" |
| Assumptions block present and visible | PASS | five assumptions, A-1..A-5, rendered on the board — not in a footnote |

Repository audit: `python3 validation/audit-system.py` — see §8.

---

## 2. The palette, and the validator's verdict verbatim

Procedure from the `dataviz` skill (`references/color-formula.md` § The six checks,
§ Snap-to-passing, § Themes). Nothing below was eyeballed.

### 2.1 The indexed palette fails on our own ground

`cf-chart-palette` is the only data-visualisation entry in
`design-system/component-index.json`. It is **not used here.** Verbatim:

```
$ node scripts/validate_palette.js "#0f62fe,#007d79,#8a3ffc,#ee5396,#33b1ff" \
    --mode light --surface "#eeece6"

Palette (light, surface #eeece6, categorical): 5 slots
  [PASS] Lightness band         all 5 inside L 0.43–0.77
  [FAIL] Chroma floor           below floor (reads gray): [["#007d79",0.092]]
  [PASS] CVD separation         worst adjacent #33b1ff↔#ee5396 ΔE 15.8 (deutan) · tritan 6.8
  [PASS] Normal-vision floor    worst adjacent #007d79↔#0f62fe ΔE 23.2 (normal)
  [WARN] Contrast vs surface    below 3:1 — relief required (visible labels or table view): [["#ee5396",2.82],["#33b1ff",2]]

  → FAILED — fix the marked checks
exit=1
```

The brief's claim is confirmed in every particular: `teal.60` at chroma 0.092, `cyan.40`
at 2.0:1, tritan 6.8 inside the 6–8 band. ART-009 F-07 recorded part of this
independently.

**This is a gap, and this artifact did not close it.** No validated chart palette exists
in the index. The four fills used below were derived *for this board* and are not a
component, not a promotion, and not a proposal. A `component-spec` for a bone-ground chart
palette is `token-keeper`'s to file and the membrane's to admit — spec, human approval,
ADR, index. `dashboard-analyst` does not enter that path.

### 2.2 How the four fills were chosen

Not by eye and not by taste. By enumeration, per `color-formula.md` § Themes
("Deriving an order when a system has no theme yet: don't guess").

1. Every non-alpha, non-hover palette leaf in `tokens.json` — 123 candidates — was run
   singly against the bone surface `#eeece6`. **15** cleared band, chroma floor and the
   3:1 mark threshold.
2. The `red.*` and `green.*` families were removed from the pool **before** ordering.
   Rule 1 of the brief is that a refusal must not read as a failure; a red or a green fill
   would smuggle a verdict back in through the hue channel, whatever the label said.
3. Every value already bound to a `semantic.support.*` status role was also removed —
   `yellow.60`, `blue.70`, `purple.60`, plus the red and green steps. This is the skill's
   collision rule: a series colour must never impersonate a status colour. It costs three
   otherwise-passing candidates.
4. `coral.text` was withheld from the categorical pool so coral stays scarce and keeps its
   one job on this board: the emphasis marker (brand.md §3, "its power comes entirely
   from scarcity").
5. That leaves a pool of 8. All 70 four-subsets were validated **all-pairs** — the harder
   pairlist, chosen because outcome swatches appear scattered through a table where any
   two can be neighbours. **4** sets passed. The one with the best worst-pair margins was
   taken.

### 2.3 The verdict, verbatim

```
$ node scripts/validate_palette.js "#0f62fe,#8a3800,#6929c4,#d02670" \
    --mode light --surface "#eeece6" --pairs all

Palette (light, surface #eeece6, categorical): 4 slots
  [PASS] Lightness band         all 4 inside L 0.43–0.77
  [PASS] Chroma floor           all 4 >= 0.1
  [PASS] CVD separation         worst all-pairs #6929c4↔#0f62fe ΔE 10.3 (deutan) · tritan 15.1
  [PASS] Normal-vision floor    worst all-pairs #6929c4↔#0f62fe ΔE 16.0 (normal)
  [PASS] Contrast vs surface    all 4 >= 3:1

  → ALL CHECKS PASS
exit=0
```

Adjacent pairlist on the same surface, for completeness:

```
  [PASS] CVD separation         worst adjacent #d02670↔#6929c4 ΔE 15.6 (protan) · tritan 17.6
  [PASS] Normal-vision floor    worst adjacent #d02670↔#6929c4 ΔE 25.4 (normal)
  → ALL CHECKS PASS   (exit=0)
```

And on the raised white layer `#ffffff`, where badges sit on zebra rows and inside cards
— re-run because a result is only meaningful against the surface the marks actually
render on:

```
$ node scripts/validate_palette.js "#0f62fe,#8a3800,#6929c4,#d02670" \
    --mode light --surface "#ffffff" --pairs all
  → ALL CHECKS PASS   (worst all-pairs ΔE 10.3 deutan · tritan 15.1 · normal 16.0)
exit=0
```

No WARN anywhere, so no relief obligation is outstanding. Direct value labels and the
full table view are shipped regardless.

### 2.4 The slots

| Outcome | Token path | Value | Glyph | On bone | On white |
|---|---|---|---|---|---|
| `found-defect` | `palette.blue.60` | `#0f62fe` | ◆ | 4.23:1 | 5.00:1 |
| `delivered` | `palette.orange.70` | `#8a3800` | ● | 6.72:1 | 7.94:1 |
| `refused` | `palette.purple.70` | `#6929c4` | ■ | 6.55:1 | 7.74:1 |
| `attested` | `palette.magenta.60` | `#d02670` | ▲ | 4.24:1 | 5.01:1 |

Assignment within the set is free: the all-pairs pairlist does not depend on order, so no
permutation can weaken a gate. It was chosen to keep verdict-shaped readings out —
`refused` takes violet, the most convention-free hue in the set.

### 2.5 Chrome

| Role | Token path | Value | On bone |
|---|---|---|---|
| ground | `palette.bone.default` (= `semantic.background`) | `#eeece6` | — |
| raised | `palette.white.default` (= `semantic.layer.02`) | `#ffffff` | — |
| primary ink | `palette.ink.default` (= `semantic.text.primary`) | `#041222` | 15.95:1 |
| secondary ink | `palette.gray.70` (= `semantic.text.secondary`) | `#525252` | 6.61:1 |
| caption / axis ink | `palette.warmGray.70` | `#565151` | 6.60:1 |
| hairline | `palette.gray.30` (= `semantic.border.subtle-01`) | `#c6c6c6` | 1.45:1 |
| gridline | `palette.warmGray.20` | `#e5e0df` | 1.11:1 |
| emphasis marker, **fill only** | `palette.coral.default` | `#f15b40` | 2.82:1 |
| coral as text | `palette.coral.text` | `#b03822` | 5.18:1 |

The coral rule in brand.md §3 is binding and is obeyed literally. `#f15b40` measures
2.82:1 on bone and appears **only** as a filled shape: a 2px left border on two cards and
one 8px round dot. It never sets a character. Every coral character on the board is
`coral.text` at 5.18:1.

---

## 3. Every figure, and how it was derived

All from `validation/agent-runs.json`. Recompute with two lines of Python:
`r = json.load(open('validation/agent-runs.json'))['runs']`.

| Figure on the board | Value | Derivation |
|---|---|---|
| dispatches | 14 | `len(r)` |
| tokens | 1,590,156 | `sum(x['tokens'] for x in r)` |
| tool calls | 626 | `sum(x['tool_uses'] for x in r)` |
| agent wall-clock | 2 h 55 m | `sum(x['duration_ms'] for x in r)` = 10,541,675 ms |
| mean tokens | 113,583 | 1,590,156 / 14 = 113,582.57, rounded |
| median tokens | 101,205.5 | 14 is even: mean of the 7th and 8th sorted values, 101,151 and 101,260 |
| range | 63,139–248,428 | min and max of `tokens` |
| largest dispatch | 248,428 | `runs[5]` — a11y-checker, 2026-09-02 |
| its share of the floor | 15.6% | 248,428 / 1,590,156 = 15.62% |
| its tool calls | 30, joint-fewest | 30 is the minimum of `tool_uses`; `runs[4]` also has 30 |
| tokens per tool call, all agents | 2,540 | 1,590,156 / 626 |
| a11y-checker | 8,281 | 248,428 / 30 |
| Plan | 2,513 | 145,734 / 58 |
| system-keeper | 2,234 | 808,759 / 362 |
| token-keeper | 2,200 | 387,235 / 176 |
| "3.3× the all-agent rate" | 3.3 | 8,280.93 / 2,540.19, computed at render, not typed |
| outcome counts | 6 / 5 / 2 / 1 | tally of the literal `outcome` values |
| tokens by outcome | 683,366 / 625,837 / 202,411 / 78,542 | `found-defect` / `delivered` / `refused` / `attested` |
| tokens by agent | 808,759 / 387,235 / 248,428 / 145,734 | system-keeper / token-keeper / a11y-checker / Plan |
| days covered | 2 | `{x['date'] for x in r}` = {2026-09-01, 2026-09-02} |

**Nothing is derived from `found`.** It is free text. It is reproduced verbatim in the
table and in one callout, and it is never counted, ranked or scored. Counting defects out
of sentences would be an interpretation, and interpretation is Phase 11's.

**No currency figure appears.** `runs[]` records one undifferentiated `tokens` number with
no input/output/cache split and no rate. A dollar figure would have to be invented.

---

## 4. Where the token check does less than it appears to — read this

The payload contains **zero** hex literals, so `.claude/hooks/gate-b.py` §1 and
`audit-system.py` check 6 both pass. That is true and it is not the whole story, and
saying only the first half is the failure mode CLAUDE.md's session protocol names.

Both checks enforce "no raw colour" with **one regular expression that matches hex and
only hex.** Two consequences:

1. A payload full of hand-invented `rgb()` or `hsl()` or `oklch()` values would pass both
   checks untouched. Hex-free is not the same claim as on-token.
2. A payload whose hex was copied faithfully out of `tokens.json` would be **blocked** —
   correct provenance, rejected on notation.

So passing the check is not the reason to believe this payload is on-system. The reason is
the construction: every colour was read out of `tokens.json` **by token path** by a
generator, and is emitted in the sRGB component form the token file itself stores
(`color(srgb 0.058824 0.384314 0.996078)` *is* the array under `palette.blue.60.$value.components`,
not a transcription of its hex). Each custom property in the payload carries its resolving
path in a CSS comment, so any value can be checked against `tokens.json` by path rather
than by eye. Spacing, type sizes, weights and tracking come through the same generator.

I am flagging this rather than banking it. **Not my check to change** — `system-keeper`
owns validators. If it is widened, the widening needs someone other than its author to
attack it, per the standing rule.

Two further limits of the same kind, stated so they are not mistaken for coverage:

- The `gap: 2px` the dataviz skill mandates between stacked segments is a raw px value
  Gate B blocks. It is `spacing.01` (0.125rem = 2px) and is emitted as `var(--s01)`. Same
  rendered pixel, on-token provenance.
- Gate B's spacing regex covers `padding`, `margin`, `gap` and `border-radius` only. Bar
  heights and the plot column width in this payload are in `rem`, not px, but nothing
  would have stopped a raw px `height`.

---

## 5. Defects this artifact found in its own construction

Four, all caught by measurement, all fixed before the payload was written out.

| # | Defect | How it was caught | Fix |
|---|---|---|---|
| 1 | `cf-chart-palette`, the indexed palette, fails on bone | dataviz validator, §2.1 | not used; a four-slot set derived and validated all-pairs |
| 2 | `palette.warmGray.60` as caption and axis ink measures **4.26:1** on bone — below the 4.5:1 AA floor for normal text | contrast check on every chrome role, not just the fills | `palette.warmGray.70`, 6.60:1 |
| 3 | `blue.60` (4.23:1) and `magenta.60` (4.24:1) clear the 3:1 **mark** threshold but not the 4.5:1 **text** threshold on bone | same | colour removed from every badge *label*; hue now sits only on the swatch, a redundant non-text mark, with the word itself in ink at 15.95:1 |
| 4 | the skill's own 2px segment gap is a raw px value Gate B blocks | generator's post-write scan | emitted as `spacing.01` |

Defect 2 is the one worth noticing: it was in the *chrome*, not the palette. Running the
categorical validator and stopping there would have shipped a caption ink that fails AA,
because the categorical six do not check text contrast at all — the skill says so
explicitly under § Scope. Every text role here was checked separately against both grounds.

---

## 6. Form and anti-patterns

Checked against `references/anti-patterns.md` and `references/choosing-a-form.md`.

- **No dual axis.** Cost, work and rate are three separate charts on three separate scales.
- **No value-ramp on nominal categories.** Bar fill encodes `outcome`, a second dimension;
  it never re-encodes bar length. The tokens-per-tool-call chart is one series and takes
  one neutral colour.
- **Emphasis, not eight hues.** The one number that carries — the largest dispatch — is
  marked with a single coral dot and a callout card, not by spending a hue on it.
- **Series count 4.** Inside the categorical range. Direct labels are mandatory at 4 and
  are shipped: every bar carries its value, every fill carries its word.
- **No status colour on a non-status series, and no series colour on a status.** The four
  fills are disjoint from `semantic.support.*` by construction (§2.2 step 3).
- **Table-view twin.** All 14 rows, every field, `found` and `report` verbatim. Every
  value on every chart is readable without colour.
- **Hairline chrome, solid.** No dashed gridlines. Gridline `warmGray.20` at 1.11:1, one
  shade off the surface.
- **2px surface gaps** between stacked segments, no borders drawn around marks.
- **`tabular-nums` where figures align vertically** — table columns, axis ticks, bar-end
  values. **Not** on the four hero figures, which take proportional figures per
  `palette.md` § Typeface & figures. The brief said "figures line up:
  `font-variant-numeric: tabular-nums`"; applied literally to the hero numbers that would
  contradict the skill, which calls tabular figures on a large standalone number an
  anti-pattern ("equal-width digits make `121` look loose at display sizes"). Resolved in
  the skill's favour — see §9.
- **No tooltip carries a value alone.** The only `title` attributes are redundant
  labels on segments whose value is already in the table.
- **Container sized to its content**; no fixed height clips an axis band.
- **No display or serif face on the hero figure**; it is the same sans as the body.

Rendered and inspected at 1280px in headless Chrome across three passes. First pass found
the bar-end callouts overflowing the right edge of the page — fixed by making the track a
two-column grid so a 100% bar can no longer push its own label off the plot.

---

## 7. Claim format

Per ADR-017 these are **measurements**, not testimony, and the notation must not blur the
two. Every figure resolves to `validation/agent-runs.json` and a named field.

No `E-nnn` ID appears on the board and none was minted. `research/evidence-ledger.json`
holds **0** entries; no user was asked anything; no person is quoted. Minting a ledger ID
for an instrument reading is exactly what CLAUDE.md forbids: "once the ledger holds things
nobody said, 'every quote resolves' stops meaning 'no user was invented.'"

The measurement form `[ART-nnn § Section]` is also not used *on the board*, because the
source is a validation ledger rather than a registered artifact. It is cited by path and
field — `validation/agent-runs.json § runs[5].found` — which is resolvable and honest.
Gate B raises an `info` on an artifact with no evidence IDs; that is expected here and is
not a finding.

---

## 8. Repository audit

```
$ python3 validation/audit-system.py
```

Result recorded in §8.1 below. The pre-existing check 5g error about the machinery hash is
**not** attributable to this artifact: it concerns `validation/attestation.json` and the
hash of the validators, none of which this artifact touches. Nothing under `validation/`
was modified. `artifacts/_registry.json` and `artifacts/ARTIFACTS.md` were regenerated
with `validation/rebuild-registry.py`, the sanctioned generator; neither was hand-edited.

### 8.1 Result

The delta was **measured, not assumed.** The artifact directory was moved out, the
registry rebuilt, the audit re-run with `--json`, the artifact restored, the registry
rebuilt again, and the two finding sets compared by `(severity, check, message)`:

```
BEFORE counts: {'blocker': 0, 'error': 1, 'warning': 2, 'info': 7}  verdict FAIL
AFTER  counts: {'blocker': 0, 'error': 1, 'warning': 2, 'info': 7}  verdict FAIL

NEW findings introduced by ART-010: 0
REMOVED:                            0
skipped before/after:               0 / 0
```

- Blockers: **0**.
- The single error is check 5g, the machinery hash, and it is present **identically**
  before and after. It concerns `validation/attestation.json` and the hash of the
  validators; this artifact changed none of them.
- The two warnings (`coverage` V-015/V-020, `surfaces` staleness) are likewise identical
  before and after.
- **Delta introduced by ART-010: 0 blockers, 0 errors, 0 warnings, 0 findings of any
  severity.**

Note that check 5f, provenance, saw this artifact and stayed silent in both directions:
it detected token references in the payload and found `inputs.tokens_version` declared as
`0.2.0`, so it raised neither the blocker for a missing version nor the warning for a
version with no detected use.

---

## 9. What the brief got wrong, or left underspecified

Recorded because a brief accepted without challenge is a brief nobody checked.

1. **`tabular-nums` on the hero figures would have been an anti-pattern.** The brief
   states "Figures line up: `font-variant-numeric: tabular-nums`" without qualification.
   `references/palette.md` § Typeface & figures and `references/anti-patterns.md` both say
   the opposite for large standalone numbers. Applied to columns, ticks and bar-end values;
   **not** to the four stat-tile figures. Flagging rather than silently diverging.

2. **"Four agents is within categorical range" — but the fourth is not an agent.** The
   `agent` field's four values are `system-keeper`, `token-keeper`, `a11y-checker` and
   `Plan`. `Plan` is not a row in CLAUDE.md's routing table and is not one of the 14 agent
   definitions. Counted as the field names it, and recorded as Assumption A-4 on the board.

3. **"Encode outcome as status" cannot be followed literally.** In the dataviz skill,
   *status* is a reserved fixed scale meaning good → warning → serious → critical. Encoding
   `outcome` on it would render `refused` as a failure, which is the exact thing rule 1 of
   the brief forbids. Both instructions cannot hold. Resolved by taking the *intent* —
   fixed slots, reserved meaning, always icon + label — while excluding every red and green
   hue and every value bound to a `semantic.support.*` role, so the fills carry identity
   and never a verdict. The board states this in place, next to the legend.

4. **"No raw hex outside what the tokens declare" describes a check that cannot tell the
   difference.** See §4. The gate matches hex literals only, in both directions wrongly.
   The brief treats passing it as evidence of on-system output; it is weaker than that.

5. **The `dataviz` skill has no `SKILL.md`.** The bundled directory carries `references/`
   and `scripts/` only. The procedure was reconstructed from `color-formula.md`,
   `choosing-a-form.md`, `palette.md` and `anti-patterns.md`. If a `SKILL.md` exists
   elsewhere with steps not in the references, this artifact did not follow them.

6. **`scripts/validate_palette.js` is not at the path the brief gives.** The brief says to
   run `node scripts/validate_palette.js`; there is no `scripts/` directory in this
   repository. The validator was run from the bundled skill directory. A copy of neither
   the validator nor its verdict exists in the repo, so **the palette result here cannot be
   re-verified by CI** — it can only be re-run by hand against the same skill version.
   Worth fixing if data visualisation becomes routine.

7. **Underspecified: the workstream.** Neither existing workstream fits. `system-operations`
   was created; rationale in `manifest.json` § `notes.why_a_new_workstream`.

---

## 10. What was NOT checked — skipped is not passed

- **Dark mode.** The payload declares no dark theme. `semantic-dark` exists in
  `tokens.json` and was not touched, and no palette was validated against a dark surface.
  No claim is made about dark rendering in either direction.
- **The adjacent pairlist as a separate gate.** All-pairs was used, which is strictly
  harder; the adjacent run in §2.3 is reported for completeness but the artifact's claim
  rests on all-pairs.
- **Keyboard focus order, focus visibility, target size, screen-reader traversal.** A
  static render cannot answer these. The board has no interactive controls, but "no
  controls" was not verified by an assistive-technology pass.
- **Print and `forced-colors`.** A `@media print` block exists and was not rendered.
  Texture, the accessibility channel, is not implemented.
- **Font rendering in Anek Latin.** No font file exists in this repository. Every
  screenshot was taken on the fallback face. Size, weight and tracking are on-token
  whatever face resolves; letterform and metrics were not inspected in the intended one.
- **Whether the ledger's own numbers are right.** This board inherits every figure in
  `validation/agent-runs.json` as entered. The file is hand-transcribed with no API behind
  it (its own `$comment` says so). A transcription error would propagate here undetected.
