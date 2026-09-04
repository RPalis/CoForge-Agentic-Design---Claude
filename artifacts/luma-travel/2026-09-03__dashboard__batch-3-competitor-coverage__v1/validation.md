# Validation — ART-013 · dashboard · batch-3-competitor-coverage · v1

**Payload:** `luma-competitor-coverage-board.html` · **Produced by:** `dashboard-analyst` ·
**Date:** 2026-09-03 · **Status:** draft · **Gate:** B (automated)

Content inputs: `ART-011` (coverage reconciliation) and `ART-012` (market findings, capped by
ART-011) — nothing else. `research/sources/` was **not** opened; the brief forbids it and
this agent held no mandate to interpret past what the two artifacts already concluded.
Visual inputs: `design-system/tokens/tokens.json` release `0.2.0`, the binding coral rule in
`design-system/foundations/brand.md` §3, and the `dataviz` skill's colour-formula method.

---

## 1. Gate B — checklist

From `validation/checklists/dashboard.md`.

| Check | Result | Evidence |
|---|---|---|
| Directory named `YYYY-MM-DD__dashboard__<slug>__v<N>` | PASS | `2026-09-03__dashboard__batch-3-competitor-coverage__v1` |
| `manifest.json` present and valid | PASS | `id` ART-013, type `dashboard` registered in `_types.json`, owner `dashboard-analyst`, level 1 |
| `validation.md` present and filled in | PASS | this file |
| Every `[E-nnn]` citation resolves | PASS, vacuously | The payload contains **no** ledger citations. `research/evidence-ledger.json` holds 0 records; the study behind ART-011/ART-012 holds no user research, so no `[E-nnn]` could be minted honestly. Gate B's `[INFO] citations: no evidence IDs found` is expected |
| No raw hex / no raw px where the artifact is visual | PASS, on the second attempt — see §5 | `.claude/hooks/gate-b.py` BLOCKED the first write on a raw `#eeece6` left in a CSS **comment** describing the validator surface (not a rendered value). Fixed by naming the token path instead of the hex; see §5 |
| Every metric names its data source and refresh cadence | PASS | Every section carries a `Source:` and `Refresh:` line; the KPI strip and every chart caption repeat it. `Refresh: static` throughout — see §6 for why that is the honest cadence |
| Palette from tokens.json | PASS | §2 — every colour, including the two new ramps, is a token-file hex read by path |
| No causal claim from correlational data | PASS | This board makes no causal claim; every statement is a count or a ratio, cited to its section |

## Gate A — human review

| Check | Result |
|---|---|
| Claims labelled `Evidenced` / `Inferred` / `Assumption` | PASS — every prose claim on the board carries `Evidenced [ART-nnn § …]`, `[D-00n]`, or sits in the `Assumptions` block |
| Assumptions block present and visible | PASS — `Assumptions`, A-1 to A-4, rendered on the board |
| Reviewed by: ______ Date: ______ | open — `draft` until a human signs |

---

## 2. The palette, and the validator's verdict verbatim

Procedure from the `dataviz` skill (`references/color-formula.md` § The six checks, §
Themes, § Scope). Nothing below was eyeballed. The skill was located at
`/private/tmp/claude-501/bundled-skills/2.1.255/b7b8b538567e1767f1716520d52a5ca8/dataviz` —
the same bundled location ART-010 used, confirmed present in this session.

### 2.1 `cf-chart-palette` still fails, and is still not used

Re-confirmed rather than assumed: `cf-chart-palette` is the only data-visualisation entry in
`design-system/component-index.json`, and ART-010 §2.1 already recorded its failure
verbatim on `palette.bone.default` (`teal.60` chroma 0.092, below the 0.10 floor;
`cyan.40` at 2.0:1). Not re-run here because nothing about it has changed since; not used
here for the same reason ART-010 gave.

### 2.2 Two NEW ramps, not ART-010's four hues, and why

This board needs no **categorical** (identity) job at all — competitors are rows, not
colour-coded series, which the brief itself settles. It needs a **sequential** job
(coverage depth, magnitude) and, on reflection, an **ordinal** job (position in the fixed
Tier 1 / Tier 2 ladder) rather than the **status** job the brief's own language suggested —
see §3 for why that substitution was made. Reusing ART-010's blue/orange/purple/magenta four
would have imported a categorical *identity* meaning (found-defect / delivered / refused /
attested, in a sibling artifact) onto a board that has no identity dimension, which risks a
reader conflating two artifacts' colour meanings for no reason. Two single-hue ramps were
enumerated and validated instead, by the same method as ART-010 §2.2:

1. Every `teal.*` and `coolGray.*` step was checked against `palette.bone.default` because
   both hues are candidates already known (ART-009, ART-010) to sit near the chroma/contrast
   edges on this ground, so they were the first tried rather than assumed safe.
2. Neither family is bound to a `semantic.support.*` role (`support.*` uses red, green,
   yellow, blue.70, purple.60 — checked against `design-system/tokens/tokens.json`
   `semantic.support`), so neither can impersonate a status verdict.
3. For the **sequential** ramp, the reference palette's own rule applies: an ordinal/
   sequential ramp's lightest step must still clear 2:1 on the surface it renders on
   (`palette.md` § Sequential hue). `teal.10`–`teal.40` all fall under that floor on bone;
   `teal.50` is the first step that clears it (2.83:1). The floor is therefore
   `teal.50`–`teal.90`, five steps.
4. For the **ordinal** tier ladder, the same floor rule found `coolGray.40` as the lightest
   usable step in isolation, but the two states this board actually needs (Tier 2, Tier 1)
   only required two steps, so `coolGray.60`/`coolGray.80` were taken for a wider, safer
   margin (ΔL and contrast both improve with the wider gap).

### 2.3 The verdicts, verbatim

Sequential ramp (`teal.50, teal.60, teal.70, teal.80, teal.90`), validated `--ordinal`
because the skill's own scope note says the categorical checks **will fail a correct ramp by
design** (it spans the lightness band on purpose) — confirmed as a sanity check in §2.4, not
treated as a real failure:

```
$ node scripts/validate_palette.js "#009d9a,#007d79,#005d5d,#004144,#022b30" \
    --ordinal --mode light --surface "#eeece6"

Palette (light, surface #eeece6, ordinal ramp): 5 slots
  [PASS] Lightness monotone     steps read light→dark
  [PASS] Adjacent ΔL            all gaps >= 0.06
  [PASS] Light-end contrast     #009d9a at 2.83:1 vs surface
  [PASS] Single hue             hue spread 16°

  → ALL CHECKS PASS
```

Re-run against the raised white layer, where the tier chips and legend swatches also render
(cards, zebra rows):

```
$ node scripts/validate_palette.js "#009d9a,#007d79,#005d5d,#004144,#022b30" \
    --ordinal --mode light --surface "#ffffff"
  → ALL CHECKS PASS   (light-end #009d9a at 3.34:1)
```

Ordinal tier ladder (`coolGray.60` Tier 2, `coolGray.80` Tier 1):

```
$ node scripts/validate_palette.js "#697077,#343a3f" --ordinal --mode light --surface "#eeece6"

Palette (light, surface #eeece6, ordinal ramp): 2 slots
  [PASS] Lightness monotone     steps read light→dark
  [PASS] Adjacent ΔL            all gaps >= 0.06
  [PASS] Light-end contrast     #697077 at 4.25:1 vs surface
  [PASS] Single hue             hue spread 5°

  → ALL CHECKS PASS
```

```
$ node scripts/validate_palette.js "#697077,#343a3f" --ordinal --mode light --surface "#ffffff"
  → ALL CHECKS PASS   (light-end #697077 at 5.02:1)
```

### 2.4 Sanity check: the categorical validator on the sequential ramp

Run once, expected to fail, so the failure is on record as expected rather than silently
skipped:

```
$ node scripts/validate_palette.js "#009d9a,#007d79,#005d5d,#004144,#022b30" \
    --mode light --surface "#eeece6"
  [FAIL] Lightness band       outside band: teal.80, teal.90
  [FAIL] Chroma floor         below floor (reads gray): teal.60, teal.70, teal.80, teal.90
  [WARN] CVD separation       worst adjacent ΔE 7.6 (deutan) · tritan 8.0
  [FAIL] Normal-vision floor  worst adjacent ΔE 7.8 — below 15
  [WARN] Contrast vs surface  teal.50 at 2.83 — below 3:1
  → FAILED
```

Per `color-formula.md` § Scope: *"running the categorical validator on a sequential ramp
will FAIL by design ... don't 'fix' a good ramp to satisfy it."* This is that expected
failure, not a defect — recorded so the FAIL is legible as intentional rather than
overlooked.

### 2.5 Text-contrast, every ink role actually used (WCAG text, not the mark floor)

The categorical/ordinal validators check *marks*; text needs the 4.5:1 AA floor, checked
separately, because ART-010 §5 found exactly this gap once already (`warmGray.60` at 4.26:1
used as caption ink). Re-checked here rather than trusted:

| Role | Token | On ground (bone) | On raised (white) | Used as |
|---|---|---|---|---|
| Primary text | `palette.ink.default` | 15.95:1 | 18.84:1 | body, headings |
| Secondary text | `palette.gray.70` | 6.61:1 | 7.81:1 | `.rowlab .task`, `.ink-2` |
| Caption / axis ink | `palette.warmGray.70` | 6.60:1 | 7.80:1 | captions, axis labels, `.blank` placeholder text |
| Text-safe coral | `palette.coral.text` | 5.18:1 | 6.11:1 | declared for links; none rendered on this board |

None of the two new ramps is ever the **colour of a character**. `teal.*` and `coolGray.*`
appear only as swatch fills (`.bar`, `.sw`) or as a glyph rendered in plain `ink` — the same
resolution ART-010 §5 defect 3 reached for `blue.60`/`magenta.60` labels, applied here before
it could become a defect rather than after:

| Mark role | Token | On bone | Note |
|---|---|---|---|
| Sequential floor (`teal.50`) | `palette.teal.50` | 2.83:1 | Clears the ordinal 2:1 floor; below the categorical 3:1 mark threshold, so every bar using it also carries a direct `%` label — the relief the skill requires is shipped, not owed |
| Tier 2 chip (`coolGray.60`) | `palette.coolGray.60` | 4.25:1 | Clears 3:1 with margin |
| Coral, fill only | `palette.coral.default` | 2.82:1 | Unchanged from ART-010; not used as a character colour anywhere |

**The dashed "never evaluated" cell was checked too, because a hatch pattern changes the
background a caption sits on.** `warmGray.70` caption text against the hatch's two stripe
colours: 6.60:1 on the bone stripe, 5.97:1 on the `warmGray.20` stripe — both clear AA.

---

## 3. What the brief got wrong, or left underspecified

Recorded because a brief accepted without challenge is a brief nobody checked, and every
agent dispatched this session has found something in its own brief.

1. **"status — evidence tier" is not what the dataviz skill's own job table means by
   Status.** `color-formula.md` § The four jobs defines Status as *"state (good→critical), a
   small fixed scale, reserved meaning, always icon+label"* and § Status is fixed adds that
   it *"never follows the theme"* and exists specifically so a series never impersonates a
   verdict. Applying that reserved scale to "highest tier reached" would render `never
   profiled` on the same axis as `critical` — exactly the misreading D-001 was decided to
   prevent, and the same class of error ART-010 §9 finding 3 already caught once (`outcome`
   cannot wear status colour, for the identical reason). "Tier reached" is instead the
   **Ordinal** job the same table defines two rows up — *"position in a sequence (funnel
   stage, tier, bucket) → one hue, monotone lightness"* — literally the tier/bucket case
   named in the skill's own example list. Implemented as an ordinal one-hue ramp (§2),
   validated `--ordinal`, not drawn from `semantic.support.*`. The three-way
   profiled/prior-art/never split that the brief's "status" language was actually pointing
   at (D-001/D-002) is rendered with **no hue at all** — shape (`●`/`◐`/`○`) plus word — which
   is the more conservative choice for exactly the same reason.
2. **The brief's phrase "arguably the most consequential thing on the board" is a verdict,
   and this agent's mandate is "present numbers, not verdicts" (CLAUDE.md, dashboard-analyst
   charter).** F-01/F-05 are still given the most visually prominent placement on the board
   (the one `coral`-bordered emphasis card, per brand.md §3's scarce-emphasis rule, echoing
   ART-010's identical use of the same channel for its single most-emphasised figure) — but
   the board states the two figures side by side and lets size and position carry the
   emphasis, rather than asserting in prose that it is the most consequential thing here.
   That editorial claim belongs to research-synthesizer in Phase 11, not to this board.
3. **D-001's own text says "the 6 confirmed-but-never-profiled competitors,"** naming six,
   while ART-011's reconciliation (produced after D-001, and citing it) establishes **eight**
   never-profiled, two of which (Kayak, Skyscanner) D-002 then separately routes to
   "prior-art only" rather than "no evidence anywhere." Read together the two decisions are
   consistent — D-001's "6" is the same six D-002 leaves outside the prior-art carve-out
   (Airbnb, Rentalcars.com, Trainline, Omio, Citymapper, Rome2Rio) — but D-001's own number
   pre-dates the reconciliation that separated the eight into two kinds. This board follows
   ART-011's later, reconciled 8/2/6 split, not D-001's earlier "6," and flags the
   discrepancy here rather than silently picking one.
4. **The brief asks for "98 of 770 feature cells (12.7%) on Tier 1 observation and 189 of
   770 (24.5%) on any evidence" and both check out exactly against ART-011's own arithmetic**
   — re-verified in §4, not just copied.

---

## 4. Every figure, and where it traces to

Nothing on this board was derived from `research/sources/`, which this agent did not open.
Every figure below is either copied verbatim from a named ART-011/ART-012 section or is a
one-step arithmetic transform of numbers those sections already state, shown so the
transform can be re-run by hand.

| Figure on the board | Value | Traces to |
|---|---|---|
| Confirmed / profiled / never | 14 / 6 / 8 | `ART-011 § Coverage` |
| Prior-art-only of the 8 | 2 (Kayak, Skyscanner) | `ART-011 § Coverage`, `D-002` |
| No-evidence-anywhere of the 8 | 6 (Airbnb, Rentalcars.com, Trainline, Omio, Citymapper, Rome2Rio) | `ART-011 § Coverage` |
| Tier 1 feature cells | 98 of 770 = 12.7% | `ART-011 § Evidence reached` — 98/770 = 0.12727, shown rounded |
| Any-evidence feature cells | 189 of 770 = 24.5% | `ART-011 § Evidence reached` — 189/770 = 0.24545, shown rounded |
| Journey stage-cells rated | 37 of 112 = 33% | `ART-011 § Evidence reached` — 37/112 = 0.33036 |
| Designated tests settled | 2 of 5 | `ART-011 § Prior claims · Scoreboard` |
| Tier 3 uses | 0, anywhere in the study | `ART-011 § Evidence reached` |
| Recounted matrix (value axis) | 99 / 55 / 35 / 141 = 330 | `ART-011 § Evidence reached` |
| Recounted matrix (confidence axis) | 98 / 90 / 1 / 141 = 330 | `ART-011 § Evidence reached` |
| Stated matrix (defective) | 86 / 48 / 28 / 113 = 275 | `ART-011 § Arithmetic defects` (F-01) |
| 275 = 55 × 5 | exact | `ART-011 § Arithmetic defects` — re-verified: 55 × 5 = 275 ✓ |
| F-05, same figure in the executive report | verbatim | `ART-011 § Arithmetic defects` |
| Per-cluster Unknown counts (10) | 10/42, 19/60, 15/48, 2/12, 23/42, 19/30, 17/30, 12/18, 8/18, 16/30 | `ART-012 § The feature matrix, across the six profiled` |
| Per-cluster evidenced % (`Derived` here) | 76.2, 68.3, 68.8, 83.3, 45.2, 36.7, 43.3, 33.3, 55.6, 46.7 | `1 − Unknown/total`, computed from the row above; re-verified by hand for all ten, e.g. loyalty (12−2)/12 = 0.8333 → 83.3% |
| Quintile bin assignment | bins of 2, ranked ascending | This board's own binning (A-2); not a source figure |
| Tier-reached per profiled competitor | 5 × Tier 1 (Expedia, Booking.com, Google Travel*, Hopper†, Tripadvisor‡), 1 × Tier 2 (TripIt) | `ART-011 § Evidence reached · Tier reached per competitor` |
| Journey stage table (48 cells) | verbatim | `ART-012 § The journey comparison, across the six profiled` |
| Designated-test scoreboard (5 rows) | verbatim | `ART-011 § Prior claims`, `§ Prior claims · Scoreboard` |
| Footnote text (pre-scoped-but-unprofiled) | verbatim | `ART-011 § Coverage · Two of the eight were pre-scoped` |

---

## 5. The Gate B block, and what it means

The first `Write` of the payload was **blocked** by `.claude/hooks/gate-b.py`:

```
[BLOCKER] tokens: raw colour #eeece6
```

The hex was not a rendered value — it was inside a CSS **comment** explaining which surface
the validator ran against (`"validated against bone #eeece6"`). Gate B's regex matches any
6-hex-digit run anywhere in the file, comments included, which is correct conservatism: a
hex literal in a comment today is one accidental copy-paste from a hex literal in a rule
tomorrow, and the check does not try to be smarter than that. Fixed by naming the token path
instead (`palette.bone.default`) rather than arguing the comment was inert. Recorded here
per the session protocol's standing rule: a check behaving exactly as documented is not a
finding against the check, but silently fixing it and moving on would have hidden a real
first-draft mistake.

---

## 6. Refresh cadence — the dashboard checklist's one type-specific rule

*"Every metric names its data source and refresh cadence"* is read literally: every section
on the board states `Source:` and `Refresh:` inline, not only in this file. The honest
cadence for all of them is **static** — this is a snapshot of a completed (and structurally
incomplete) desk-research pass dated 21 Jul 2026, not a metric with a polling interval. A
dashboard whose "refresh" line claimed anything else (daily, on-demand, live) would assert
freshness the underlying study does not have. The board changes only if: (a) a later phase
profiles one of the eight remaining competitors, (b) ART-011's recount is itself corrected,
or (c) a human resolves F-01 at source rather than leaving ART-011 standing as the
correction.

---

## 7. Form and anti-patterns

Checked against `references/anti-patterns.md` and `references/choosing-a-form.md`.

- **Rows, not columns, for 14 competitors** — `choosing-a-form.md` § Is it even a chart:
  *"More than ~7 classes that all carry meaning → a table"*. 14 exceeds that by a factor of
  two, so competitors are table rows throughout, never a legend of 14 colours.
- **No value-ramp on nominal categories.** The journey Strong/Adequate/Weak/Unknown table
  and the designated-test scoreboard are both colour-free — a judged label is not a
  magnitude, so neither takes the sequential ramp or invents a third one.
- **No status colour on a non-status series.** Confirmed by construction (§2.2, §3): neither
  new ramp is bound to `semantic.support.*`, and the one field that could have been read as
  a verdict (row state) carries no hue at all.
- **Emphasis, not a verdict hue.** F-01/F-05 take the single `coral` left-border emphasis
  card, exactly ART-010's pattern for "the one number that carries" — scarce, per brand.md
  §3, and never used as a second status scale.
- **Series-count / table-view twin.** The 14-row coverage table and the 6×8 journey table are
  both, in full, the colour-free equivalent of every chart above them; nothing on this board
  requires colour to be read correctly.
- **Direct labels mandatory.** Every bar in the cluster chart carries its exact percentage;
  every tier chip carries its word. No mark's meaning depends on matching a swatch to a
  legend from memory.
- **Hairline chrome, solid; texture reserved for the one job it has.** The 45°/135°
  diagonal-hatch treatment is used exactly once, on the "never evaluated" placeholder, which
  is the one place this board needs an accessibility-safe non-colour signal for "genuinely
  absent" — not decorative, and not repeated elsewhere.
- **`tabular-nums` on table/axis figures only**, per `palette.md` § Typeface & figures; the
  KPI hero figures use the default proportional figures, matching ART-010 §6's resolution of
  the same brief language.

Rendered and inspected at 1280px in headless-equivalent review (structural inspection of the
generated markup and computed colour values; no live browser screenshot was taken in this
session — see §9).

---

## 8. Repository audit

```
$ python3 validation/audit-system.py --json
```

Measured, not assumed, the same way ART-010 §8.1 did: captured **before** this artifact
directory existed, then again **after**, then diffed by `(severity, check, message)`.

**Before** (captured prior to writing any file in this artifact):
```
{'blocker': 0, 'error': 1, 'warning': 4, 'info': 6}   verdict FAIL
```

**After** (this artifact's `manifest.json`, `validation.md` and payload all present,
registry rebuilt via `validation/rebuild-registry.py` — `13 artifact(s), 10 live`):
```
{'blocker': 0, 'error': 1, 'warning': 4, 'info': 6}   verdict FAIL
```

The two count sets are identical. Counts alone were not trusted — per the session protocol's
standing rule, a match on totals is not proof of a match on *contents* (two findings could
swap without moving a count). So the two full finding lists were diffed by
`(severity, check, message)`, the same key ART-010 §8.1 used:

```
NEW findings introduced by this artifact:     []
REMOVED findings:                             []
before findings count: 11   after findings count: 11
before skipped: []   after skipped: []
```

### 8.1 Result

- Blockers: **0**, before and after, and confirmed identical at the message level, not only
  the count.
- The one **error**, both before and after, is check `attestation` (5g) — *"the validation
  machinery or its wiring changed and no audit report attests to the current state."* It is
  **not attributable to this artifact**: it concerns `validation/attestation.json` and the
  hash of the validators and their wiring, none of which this artifact touches, reads, or
  writes. Reported per the brief's own instruction to report this rather than treat a
  pre-existing FAIL as this agent's failure.
- The four **warnings**, unchanged: 2 corrections with no check (`corrections`, C-031/C-033),
  2 unverified load-bearing claims (`coverage`, V-015/V-020), and two stale-surface warnings
  (`surfaces`) — none of which this artifact's subject matter (either the two upstream
  artifacts or this board) touches.
- **This artifact introduced zero findings of any severity**, including zero new `info`
  entries — `audit-system.py`'s own checks do not enumerate per-artifact evidence-citation
  results the way the `Write`-time Gate B hook does (that `[INFO] citations: no evidence IDs
  found` line in §5 is Gate B's output, not `audit-system.py`'s, and the two were not
  conflated here).
- **No blocker was introduced at any point**, including during the one Gate B block in §5,
  which was caught and fixed before the write completed — Gate B did its job.

---

## 9. What was NOT checked — skipped is not passed

- **A live browser screenshot.** Layout, wrapping and the print stylesheet were reviewed by
  reading the generated markup and CSS, not by rendering and photographing it. ART-010 §6
  took three rendered passes in headless Chrome; that tool was not exercised in this session.
  If the `blank` cell's diagonal-hatch background or the KPI grid's responsive collapse
  render incorrectly, this validation would not have caught it.
- **Dark mode.** No dark theme is declared; `semantic-dark` was not touched and no palette
  was validated against a dark surface, matching ART-010's identical scope limit.
- **Font rendering in Anek Latin.** No font file exists in this repository; whatever letter-
  forms actually render were not inspected.
- **Keyboard/assistive-technology traversal.** A static, non-interactive page; no controls
  exist, but "no controls" was not verified with an AT pass.
- **Whether ART-011's own recount is itself correct.** This board inherits it as entered
  (A-1) and did not re-run `build_inventory.py`, which this agent has no mandate to open.
- **Whether the study's recommendation should proceed.** Explicitly out of scope — see the
  board's own "What this board does not do," item 5.

**Skipped is not passed.**

---

## Nothing under `research/sources/` was modified, or opened

This agent holds `Read, Write, Bash` and used Bash only for the palette validator, contrast
checks, and `python3 validation/audit-system.py` / `rebuild-registry.py`. No file under
`research/sources/` was read, and none was written to. The 49 sha256-baselined source files
and the two upstream artifacts (`ART-011`, `ART-012`) are untouched.

## Verdict

Gate B: **pass** (one block caught and fixed pre-write, §5). Gate A: **pending a named
human**. Status stays `draft`.
