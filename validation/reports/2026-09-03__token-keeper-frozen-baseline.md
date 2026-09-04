## token-keeper — frozen baseline for the dashboard rebuild (2026-09-03)

**Scope.** Establish a reference baseline of `design-system/tokens/tokens.json` at
release 0.2.0 for the dashboard rebuild, verify the luminance-collision claim that
broke the board's colour encoding twice, and assess (not perform) C-035. No token
value was changed. Only this report file and a scratchpad working file were written;
`tokens.json` and `component-index.json` are unmodified (`git status --short` on both
returns nothing).

**Audit — before.**
```
blocker 0 · error 1 · warning 5 · info 6 · skipped 0
VERDICT: FAIL
```
Full findings: `attestation` error (5g — pre-existing, not produced by this dispatch: I
did not touch any validator, hook, or the wiring that invokes them, so I have nothing
to attest and am not naming a machinery hash here); `provenance` warning on ART-015;
`corrections` warning (C-031/C-033/C-034/C-035 have no check); `coverage` warning
(V-015, V-020 unverified); two `surfaces` staleness warnings (asserted_state_date
behind current commits). None of these belong to token-keeper's remit in this
dispatch except C-035, addressed in Task 3.

**Audit — after.** Re-run at the end of this dispatch, after writing only this report:
identical result — `blocker 0 · error 1 · warning 5 · info 6 · skipped 0`, `VERDICT:
FAIL`. Nothing moved. (Full second run included in the "Verification" section at the
end of this report, per instruction to report both.)

---

## Task 1 — the frozen baseline

### Identity

| | |
|---|---|
| File | `design-system/tokens/tokens.json` |
| `$version` | `0.2.0` |
| Last touched (git) | commit `d03e51f`, 2026-09-03 09:09:37 +0200 ("Clear Gate A on the brand primitives, and stop the generator revoking it") |
| File size | 307,250 bytes / 11,093 lines |
| **Raw-byte SHA-256** | `1c9497b3966cba102b796380886253d89789f8b99a97d694462a3d1a3cc8c152` |
| **Canonical-JSON SHA-256** (keys sorted, no whitespace — survives reformatting) | `1926c393fe83742443350f2aa4e8d5dd3d0d6d7393a31c93e2f74317cada1a7f` |

Record **both** hashes as the frozen baseline. The raw-byte hash is what
`shasum -a 256 design-system/tokens/tokens.json` reproduces directly and is the
cheapest drift check; the canonical hash is the one to trust if the file is ever
re-serialized (different key order, indentation, trailing newline) without a real
content change — the raw hash would false-positive on drift in that case, the
canonical one would not. Recompute canonical form as: `json.dumps(data,
sort_keys=True, separators=(',',':'))` in Python, encoded UTF-8, SHA-256'd.

### Token count

**829 leaf tokens** (nodes carrying both `$type` and `$value`), confirmed by direct
walk of the tree, matching the count declared in `CLAUDE.md`, `.ai/index.json`, and
`design-system/DESIGN-SYSTEM.md`.

### The five axes

The brief's phrasing ("the five axes") is correct, but `tokens.json` has **eight**
top-level keys, not five, and no file states the reconciliation, so I'm recording it
here. Per-key leaf counts:

| Top-level key | Leaf count |
|---|---|
| `palette` | 289 |
| `semantic` | 236 |
| `semantic-dark` | 236 |
| `spacing` | 13 |
| `typography` | 29 |
| `elevation` | 4 |
| `motion` | 18 |
| `density` | 4 |
| **Total** | **829** |

The five axes named in `scratch/brand-extraction/token-axes-proposal.md` (the
document that actually defined them, 2026-08-27) are **Colour, Spacing, Typography,
Elevation, Motion**. Colour is the union of `palette` + `semantic` + `semantic-dark`
(761 leaves); the other four axes map one-to-one onto their top-level keys (13 + 29 +
4 + 18 = 64). `761 + 64 = 825`. The remaining **4 leaves are `density`**, which the
same proposal document explicitly designed as a *sixth, cross-cutting* group — "not a
new primitive axis," a pair of named registers (`stage`, `document`) that only point
at subsets of the existing `typography.scale` and `spacing` axes. So "five axes, 829
tokens" and "eight top-level JSON keys" are both true; `density` is real leaf content
(4 tokens) that sits outside the five-axis count by original design, not by omission.
Worth stating once here so it isn't re-litigated as a discrepancy.

### What the 8 L1 primitives actually reference

`component-index.json`'s 8 `level: 1` entries and their declared `tokens_used`:

| L1 primitive | `tokens_used` |
|---|---|
| `cf-type-scale` | `typography.*` |
| `cf-colour-roles` | `semantic.background`, `semantic.layer.*`, `semantic.text.primary`, `semantic.border.subtle-01` |
| `cf-spacing-scale` | `spacing.*` |
| `cf-rule` | `semantic.border.subtle-01` |
| `cf-table` | `semantic.layer.*`, `semantic.border.subtle-01`, `semantic.text.primary` |
| `cf-card` | `semantic.layer.*`, `semantic.border.subtle-01` |
| `cf-chart-palette` | `palette.blue.60`, `palette.teal.60`, `palette.purple.60`, `palette.magenta.60`, `palette.cyan.40` |
| `cf-badge` | `semantic.support.error`, `semantic.support.success`, `semantic.support.warning`, `semantic.support.info` |

Every declared reference resolves to a real leaf or a real non-empty wildcard prefix
— zero dangling references.

**Direct, literal path matches:** 83 of 829 leaves (36 `semantic`, 29 `typography`,
13 `spacing`, 5 `palette`).

**Alias-resolved (the number that actually matters):** several of those 36 `semantic`
leaves are themselves `{palette.*}` aliases, one hop deeper — e.g. `semantic.background
= {bone.default}` and `semantic.text.primary = {ink.default}`. Chasing every alias
transitively from the 83 directly-declared paths reaches **98 of 829 leaves total**
(36 semantic + 29 typography + 20 palette + 13 spacing; **0** from `elevation`,
`motion`, or `density`).

### Which tokens nothing references at all

**731 of 829 leaves (88%) are not reachable — directly or through any alias chain —
from any of the 8 registered L1 primitives:**

| Group | Total | Unreferenced |
|---|---|---|
| `semantic-dark` | 236 | **236 (100%)** — no L1 primitive names a `semantic-dark.*` path, and light-mode semantic entries do not chain into it (light and dark are parallel trees, not a chain) |
| `palette` | 289 | 269 (93%) |
| `semantic` | 236 | 200 (85%) |
| `motion` | 18 | **18 (100%)** |
| `elevation` | 4 | **4 (100%)** |
| `density` | 4 | **4 (100%)** |
| `spacing` | 13 | 0 |
| `typography` | 29 | 0 |

Inside `semantic`, the largest unreferenced blocks are `semantic.syntax` (88 leaves —
code-syntax highlighting, presumably dead weight for a dashboard), `semantic.ai` (21),
`semantic.chat` (21), `semantic.border` (15 of 16; only `subtle-01` is used),
`semantic.link` (8), `semantic.text` (8 of 9; only `primary` is used), `semantic.icon`
(7), `semantic.support` (7 of 11 — the 4 status colours are used, the hover/inverse
variants are not), `semantic.field` (6).

**The two brand-primitive findings worth flagging, both bearing on Task 3:**
- `palette.bone.default` and `palette.ink.default` — two of the four Gate-A-pending
  primitives — **are** consumed end-to-end: `bone` via `semantic.background`, `ink`
  via `semantic.text.primary`, both of which `cf-colour-roles` and `cf-table`
  declare. They are live, not decorative.
- `palette.coral.default` and `palette.coral.text` — the other two pending primitives
  — are aliased-to by `semantic.accent.container` / `semantic.accent.text` (and
  `semantic-dark.accent.*`), but **no registered L1 primitive references
  `semantic.accent.*` at all.** Coral is wired one hop into the semantic layer and
  then reaches nothing. It is fully unreferenced by anything the component index
  currently exposes, unlike bone and ink.

For the rebuild's binding constraint ("foundations do not move"), this baseline is
the useful artifact: any future diff that changes the 98 reachable leaves is a
functional regression risk for the 8 registered primitives; a diff touching only the
731 unreferenced leaves cannot affect anything currently wired to a component, though
it would still trip the raw byte-hash and should still be treated as drift under
ADR-001 once Figma is the source.

---

## Task 2 — the luminance-ladder claim

**Verified. It holds, more tightly than "no non-colliding second ramp" even implies.**

Method: extracted every numbered-step colour leaf (`10`…`100`) from all 12 hue
families that carry the standard Carbon ramp (`red, magenta, purple, blue, cyan,
teal, green, gray, coolGray, warmGray, yellow, orange`), computed WCAG relative
luminance per family/step from the token's own `$value.components` (sRGB → linear →
`0.2126R + 0.7152G + 0.0722B`), grouped by step number, and computed both the raw
spread and the worst-case pairwise contrast ratio within each step group.

| Step | min L | max L | spread (abs) | worst pairwise contrast |
|---|---|---|---|---|
| 10 | 0.8979 | 0.9071 | 0.0092 | 1.010 : 1 (cyan/teal) |
| 20 | 0.7309 | 0.7588 | 0.0279 | 1.036 : 1 (teal/yellow) |
| 30 | 0.5646 | 0.5736 | 0.0090 | 1.015 : 1 (green/yellow) |
| 40 | 0.3767 | 0.3999 | 0.0232 | 1.055 : 1 (teal/orange) |
| 50 | 0.2617 | 0.2664 | 0.0047 | 1.015 : 1 (gray/warmGray) |
| 60 | 0.1586 | 0.1606 | 0.0020 | 1.010 : 1 (warmGray/yellow) |
| 70 | 0.0823 | 0.0865 | 0.0042 | 1.032 : 1 (magenta/orange) |
| 80 | 0.0397 | 0.0428 | 0.0031 | 1.035 : 1 (blue/orange) |
| 90 | 0.0176 | 0.0196 | 0.0020 | 1.029 : 1 (blue/orange) |
| 100 | 0.0073 | 0.0087 | 0.0015 | 1.026 : 1 (teal/orange) |

Worst case across the entire palette: **1.055 : 1**, roughly a twentieth of WCAG's
3:1 non-text minimum and a fortieth of its 4.5:1 text minimum. Restricting to the
likely narrower "seven hue families" a prior dispatch may have meant (excluding the
three grays, orange, and yellow — `red, magenta, purple, blue, cyan, teal, green`)
tightens it further: worst case **1.025 : 1** (red/teal at step 100). Either grouping
supports the same conclusion: **every hue family sits on one shared lightness ladder;
picking a different hue at the same step number buys essentially zero luminance
separation, regardless of which subset of families you count.** The prior dispatch's
conclusion is confirmed with numbers, not just re-asserted.

I also checked whether any brand-added colour (`bone`, `ink`, `coral.default`,
`coral.text` — the same four from Task 3) escapes the ladder, since they are the one
part of the palette Carbon didn't author. They don't: `coral.default` computes to
L = 0.2655, landing inside the step-50 band (0.2617–0.2664) by coincidence, not
design. `bone` (0.839) and `ink` (0.0057) sit off the standard ramp because they're
single spot colours, not part of an ordinal family — so they don't offer a "second
ramp" either, just two isolated points.

**The concrete, actionable finding: `cf-chart-palette` — a registered L1
primitive — is itself built on this exact collision.** Its five declared tokens are
`blue.60, teal.60, purple.60, magenta.60` (four colours at the identical step) and
`cyan.40` (deliberately a different step). Measured contrast ratios among the four
same-step entries:

| Pair | Contrast |
|---|---|
| blue.60 / purple.60 | 1.0003 : 1 |
| blue.60 / magenta.60 | 1.0013 : 1 |
| blue.60 / teal.60 | 1.0026 : 1 |
| purple.60 / magenta.60 | 1.0010 : 1 |
| teal.60 / purple.60 | 1.0029 : 1 |
| teal.60 / magenta.60 | 1.0039 : 1 |
| any of the four vs. `cyan.40` | ~2.11 : 1 |

Four of the five categories in the system's own chart palette are luminance-identical
(≤0.4% apart); only `cyan.40` is lightness-separable from the rest, and only because
it was deliberately drawn from a different step. This is very likely the direct
mechanism behind "the board's colour encoding broke twice" — it isn't a one-off
misuse, it's built into the one L1 token set the system currently offers for
categorical colour.

**Recommendation, stated once so it doesn't get rediscovered:** the escape hatch this
token set actually has is **step, not hue** — two colours at different steps within
even one hue family separate by >2:1, while two colours at the same step never
separate meaningfully regardless of hue. Any redesign of `cf-chart-palette`, or any
future ordinal/second-channel encoding on this token set, should pick distinct steps
per category (as it already accidentally does for cyan) rather than relying on hue
alone at a fixed step — and per `cf-badge`'s own a11y note, colour should carry a
redundant channel (shape, label, pattern) regardless. This belongs in `brand.md` or
`DESIGN-SYSTEM.md` as a written structural property of the Carbon mirror, not
something each agent re-derives; I'm flagging it here rather than writing it myself,
since amending either file is outside this dispatch's frozen-foundations mandate.

---

## Task 3 — C-035, assessed, not performed

**What's actually in the file**, re-verified directly:

- `$extensions.coforge.brand_primitives_added.gate` (batch level): `"Gate A —
  APPROVED by Agentic Designer - RP, 2026-09-02"`.
- `palette.bone.default.$extensions.coforge.gate`,
  `palette.ink.default.$extensions.coforge.gate`,
  `palette.coral.default.$extensions.coforge.gate`,
  `palette.coral.text.$extensions.coforge.gate` (per-primitive, all four identical):
  `"Gate A — suggested by token-keeper; not counted until a human approves (CLAUDE.md
  Gate table)"`, unchanged since 2026-08-31.

**Assessment (not a decision).** The evidence leans toward propagation being
correct, for one specific reason: the batch note's own `what` field is not a vague
summary — it names the exact scope of what it says was approved: *"palette.bone,
palette.ink, palette.coral (.default + .text) — CoForge's own primitives... (ADR-011)."*
That is the same four paths, named the same way, as the four per-primitive gate
fields that still say "pending." There's no third possibility hiding in the batch
note (e.g. "approved 3 of 4," or "approved the concept but not the values") — the
`$gate_history` field narrates a move from "suggest-only, pending" to "APPROVED" for
this exact set on 2026-09-02, and explicitly ties the approval to a consequence for
measured values (ART-009 assumption A-5). That reads as approval of the values, not
just the act of adding a category.

**What would be touched if propagated:** exactly the four `$extensions.coforge.gate`
string fields listed above, inside `design-system/tokens/tokens.json`, each rewritten
from "not counted until a human approves" to something naming the same approval the
batch note carries (e.g. "Gate A — APPROVED by Agentic Designer - RP, 2026-09-02,
propagated from `$extensions.coforge.brand_primitives_added`"). Nothing else. I
confirmed no validator, hook, or the audit script reads this field's string value to
gate any pass/fail decision — `grep` across `validation/` and `.claude/hooks/` found
no code branching on "not counted" or "APPROVED" inside a token's `gate` field, and
the 829/five-axis counts already include all four primitives regardless of what their
`gate` field says. So propagating this is a **pure documentation-consistency fix with
zero mechanical/CI blast radius** — nothing in the pipeline currently trusts or
distrusts the per-token field's exact wording.

**Why I'm not doing it anyway.** The brief is right that this is a judgement about
*what was approved*, and that judgement is the approving human's to make explicit,
not mine to infer — even a well-evidenced inference is still an inference. Two things
a human confirming this should know, surfaced by this assessment:

1. `coral.default` / `coral.text` are, per Task 1, the two of these four primitives
   that **no L1 primitive in `component-index.json` currently references**, even
   through an alias chain (`bone` and `ink` are both live via `semantic.background`
   and `semantic.text.primary`; coral only reaches `semantic.accent.*`, which nothing
   reads). That doesn't bear on whether the colour values were approved, but it's
   relevant context: propagating "APPROVED" to a token nothing consumes yet is
   approving a value in isolation from any component that uses it.
2. `validation/corrections.json`'s own `verifies` field for C-035 says a check that
   would catch batch/per-token gate disagreement doesn't exist and calls it
   "token-keeper's call." I'd suggest (not implement — machinery is system-keeper's
   territory per the routing table) that once a human resolves this specific case,
   system-keeper add a structural check: any `$extensions.coforge.brand_primitives_added`
   (or equivalent future batch note) whose `gate` says APPROVED should require every
   path named in its own `what` field to carry a matching per-token gate string,
   flagged as a warning otherwise. That would make this exact defect mechanically
   loud instead of dashboard-analyst-shaped luck.

---

## Corrections to this dispatch's brief

- The brief calls `tokens.json`'s eight top-level keys "the five axes." Both are
  correct simultaneously — see Task 1's axes section — but the file itself doesn't
  state the reconciliation anywhere, so I've recorded it here rather than silently
  matching the brief's count to a different structure.
- No other factual claim in the brief needed correction: the batch-vs-per-token gate
  text, the four primitive names, and the "seven hue families" framing for Task 2 all
  matched what's actually in the repo (the seven-family subset is not named anywhere
  I could find as the prior dispatch's literal scope, so I computed both the 12-family
  and a plausible 7-family reading and reported both numbers rather than guessing
  which one the prior dispatch meant).

---

## Verification

**Audit — after** (re-run after writing this report, no other file touched):
```
blocker 0 · error 1 · warning 5 · info 6 · skipped 0
VERDICT: FAIL
```
Identical to "before." The pre-existing `attestation` error (check 5g) is unrelated
to this dispatch — I made no change to any validator, hook, or gate wiring, so there
is no machinery hash for me to record here; that check remains red for whoever last
touched the machinery, not for this report.

**Files read (no writes except this report):**
`design-system/tokens/tokens.json`, `design-system/component-index.json`,
`design-system/DESIGN-SYSTEM.md`, `scratch/brand-extraction/token-axes-proposal.md`,
`validation/corrections.json`, `.ai/index.json`, `.ai/index.md`, `CLAUDE.md`.
