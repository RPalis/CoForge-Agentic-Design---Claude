# Semantic colour layer — WCAG 2.2 AA contrast audit

**Artifact:** ART-009 · **Type:** `a11y-audit` · **Version:** 2 · **Date:** 2026-09-02
**Supersedes:** ART-008 (v1, 2026-08-31, token release 0.1.0)
**Produced by:** `a11y-checker` (Write-only for this directory; no `Edit`, no `Bash`)
**Subject:** `design-system/tokens/tokens.json` — **release 0.2.0**, 829 tokens.
`semantic.*` (236 light aliases) and `semantic-dark.*` (236 dark aliases) resolving into a
285-entry `palette` (250 opaque Carbon entries + 35 alpha primitives minted for C-021).
**Rulebook:** `design-system/a11y/rules.md` · **Floor:** WCAG 2.2 AA.

> **First filter, not the verdict.** This audit is a mechanical pass over computed numbers.
> A human still reviews at Gate A. Nothing below is a design decision and nothing below was
> changed — this agent holds no `Edit` and no `Bash`.

**Headline:** 121 pairs computed · **38 measurements below threshold**, of which **24 are not
covered by WCAG's inactive-component exception** · 28 findings (22 open, 6 recording a v1
finding now resolved) · **420 of 472 colour aliases skipped, not passed.**

**Why v2 exists.** Between 0.1.0 and 0.2.0 the token layer moved materially in three ways, and
**every ratio below was re-derived from the 0.2.0 file. No number was carried forward from v1.**

1. **C-021 — the alpha repair.** 53 semantic tokens carried
   `$extensions["org.carbon"].alphaModifier`, an opacity that nothing applied; their `$value`
   was a bare alias to an opaque base, so they rendered opaque. 35 alpha-carrying palette
   primitives were minted (`-a30` = 30% alpha) and all 53 tokens repointed onto them. Those
   tokens are now genuinely translucent and their effective contrast is far lower.
2. **The ground moved.** `semantic.background` no longer resolves to `{white.default}`. It
   resolves to `{bone.default}` `#eeece6`. This closes v1's F-11 and **invalidates every
   light-theme number in v1 independently of the alpha repair**, because they were all measured
   against a ground that is no longer the page.
3. **Aliases moved underneath unchanged token names.** `text.primary`, `text.helper`,
   `text.error`, `link.primary`, `link.visited`, `support.success`, `support.warning` and
   `border.strong-01` all point somewhere new in 0.2.0. Seven of v1's numbers would have been
   wrong even if the ground and the alpha had not changed.

---

## 1. Scope — what was computed, and why this set

The colour layer is 472 semantic aliases (up from 468: `semantic.accent.{container,text}` and
their dark counterparts are new). Auditing "472 aliases" is not meaningful — an alias is not a
contrast pair. Contrast is a property of a **foreground against a named ground**, and most
aliases name neither.

Scope is driven, as in v1, by the `tokens_used` declarations of the eight L1 primitives in
`design-system/component-index.json`, which are the only entries naming specific semantic
tokens. The 208 L2 entries all declare the wildcard `semantic.*`; a wildcard names no pairing,
so it generated no pairs.

### 1.1 The grounds — three in light, not two

v1 stated that the light theme had "exactly two distinct surface values". **That was true of
0.1.0 and is not true of 0.2.0.** After alias resolution:

| Ground | Alias | Resolves to | Relative luminance L |
|---|---|---|---|
| **G1** | `semantic.background` | `{bone.default}` `#eeece6` | 0.83883 |
| **G2** | `semantic.layer.01` (= `layer.03`) | `{gray.10}` `#f4f4f4` | 0.90465 |
| **G3** | `semantic.layer.02` | `{white.default}` `#ffffff` | 1.00000 |
| **D1** | `semantic-dark.background` | `{gray.100}` `#161616` | 0.00800 |
| **D2** | `semantic-dark.layer.01` | `{gray.90}` `#262626` | 0.01944 |

Bone is the **darkest** of the three light grounds, so every light foreground contrasts *less*
on the brand ground than on the white it replaced. G3 `#ffffff` is retained as a measured ground
both because `semantic.layer.02` genuinely resolves there and because it is the only ground that
permits a like-for-like delta against v1.

**Dark has four distinct surfaces, not two** — `semantic-dark.layer.02` is `{gray.80}` `#393939`
and `layer.03` is `{gray.70}` `#525252`. Only D1 and D2 were computed, matching v1's dark scope.
The other two are recorded as skipped, not passed (F-25).

### 1.2 The seven sets, 121 pairs

| Set | Content | Threshold | Pairs |
|---|---|---|---|
| 1 | Light opaque text foregrounds × 3 light grounds | 4.5:1 | 24 |
| 2 | Dark opaque text foregrounds × 2 dark grounds | 4.5:1 | 16 |
| 3 | Text on inverse and brand grounds | 4.5:1 | 3 |
| 4 | `support.*` as non-text × 3 light grounds | 3:1 | 21 |
| 5 | Borders, focus and the brand accent as non-text | 3:1 | 23 |
| 6 | `cf-chart-palette` series marks × 3 light grounds | 3:1 | 15 |
| 7 | **Alpha-composited foregrounds** (new in v2) | 4.5:1 / 3:1 | 19 |
| | | **total** | **121** |

### 1.3 Method — how any number below can be re-derived

**Relative luminance.** Each channel is normalised to 0–1, linearised
(`c/12.92` where `c ≤ 0.04045`, else `((c+0.055)/1.055)^2.4`), and combined as
`L = 0.2126·R + 0.7152·G + 0.0722·B`.

**Contrast ratio.** `(L_lighter + 0.05) / (L_darker + 0.05)`.

**Alpha compositing.** A token with alpha is not a colour until it is over a ground. For each
alpha-carrying foreground, the composite is taken **per channel in sRGB** before linearisation:

```
result_channel = alpha × foreground_channel + (1 − alpha) × ground_channel
```

then `L` and the ratio are computed from `result`. Worked example, `semantic.text.placeholder`
= `{gray.100-a40}` (`#161616`, α = 0.40) over `semantic.background` `#eeece6`:

```
R = 0.40×22  + 0.60×238 = 151.6
G = 0.40×22  + 0.60×236 = 150.4
B = 0.40×22  + 0.60×230 = 146.8   →  composite ≈ #98978f, L = 0.30681
ratio = (0.83883 + 0.05) / (0.30681 + 0.05) = 0.88883 / 0.35681 = 2.49:1
```

**Rounding convention — and a difference from v1.** Ratios are **truncated (floored)** to two
decimals, never rounded up, so no PASS is inflated. v1 appears to have rounded to nearest in
several rows. Where §3's delta tables show ±0.01 against an unchanged alias and an unchanged
ground, **that is the convention, not movement** — those rows are marked `0.00 (conv.)`.

**No script was run; there is no `Bash` in this agent's tool set.** Every row states both
resolved hex values so any row can be recomputed by hand.

**Arithmetic checksum against an independent calculation.** `tokens.json` `$description` fields
carry seven contrast ratios computed separately by `token-keeper`. Recomputing them here:
`coral.default` on bone **2.81** (recorded 2.82), on white **3.32** (3.33); `coral.text` on bone
**5.17** (5.18), on white **6.11** (6.11); `ink.default` on bone **15.94** (15.95);
`coral.default` on dark background **5.43** (5.43); `coral.text` on dark background **2.96**
(recorded **2.95**). Six of seven agree within the truncate-vs-round convention. One does not
(F-28). Two independently produced calculations landing on the same numbers is the strongest
available evidence that this audit's luminance model is correct; it is stated here rather than
assumed.

**Large-text allowance not used.** `rules.md` permits 3:1 for text ≥ 24px or ≥ 18.66px bold. A
colour token carries no size, so no text pair was granted it. This is the conservative reading
and it is a choice, stated so it is not mistaken for an oversight.

**The inactive-component exception IS applied, and is named every time.** WCAG 2.2 SC 1.4.3 and
1.4.11 both exempt inactive (disabled) user-interface components. Five findings below sit under
that exemption. Their computed values are reported in full anyway, with the exemption stated,
because the exemption holds **only if the component is genuinely inactive** — and `text.disabled`
used as de-emphasised body text is not an inactive component.

---

## 2. Alpha zero — is a fully transparent foreground in scope?

Six semantic tokens resolve to a primitive with `alpha: 0.0`:

| Token | Resolves to |
|---|---|
| `semantic.ai.aura-end` | `{white.default-a00}` `#ffffff00` |
| `semantic.ai.aura-hover-end` | `{white.default-a00}` |
| `semantic.chat.prompt-border-end` | `{gray.10-a00}` `#f4f4f400` |
| `semantic-dark.ai.aura-end` | `{black.default-a00}` `#00000000` |
| `semantic-dark.ai.aura-hover-end` | `{black.default-a00}` |
| `semantic-dark.chat.prompt-border-end` | `{gray.90-a00}` `#26262600` |

**Decision: out of scope for contrast — excluded by definition, not skipped for lack of
information.** Three reasons, in order of strength:

1. **The composite is the ground, identically.** At α = 0 the formula collapses:
   `result = 0×fg + 1×bg = bg`. The ratio is therefore `(L+0.05)/(L+0.05) = 1.00:1` against
   *every* ground, for *every* one of the six. That number measures nothing about the token —
   it is a restatement of an identity.
2. **Reporting it would manufacture six failures.** 1.00:1 is below both 4.5:1 and 3:1. Putting
   these six in the failure tally would inflate it by 16% with an arithmetic artifact, and a
   reader scanning the table could not tell the artifact from a real defect. That is the
   coverage illusion in miniature.
3. **WCAG has nothing to attach to.** SC 1.4.3 governs text and 1.4.11 governs visual
   information required to identify a component or its state. A fully transparent foreground
   presents no text and no visual information — nothing is drawn. All six are the transparent
   stop of a two-stop gradient (`aura-start` → `aura-end`, `prompt-border-start` →
   `prompt-border-end`); the perceivable part of the gradient is the *other* stop, and that stop
   is opaque and separately named.

**This decision changes no count in this audit.** All six live in `ai.*` / `chat.*`, which are
outside the declared L1 scope and were already in skip bucket S2 (§4). The decision is recorded
so that a future run which extends scope to `chat.*` does not silently start reporting 1.00:1.

**What would change the answer:** if any of the six ever becomes the *sole* carrier of a border
or a state, the finding is not a contrast finding. It is that nothing is drawn at all — a
different defect, filed against a different success criterion.

---

## 3. Movement since v1 — what got better, what got worse

Two delta tables, because two different things moved and conflating them would hide both.

### 3.1 Table A — same named pair, `token → semantic.background`

The ground itself changed (`#ffffff` → `#eeece6`), so this table answers: *what does a designer
who writes "text on the page background" actually get now?*

| Token → `semantic.background` | v1 (on `#ffffff`) | v2 (on `#eeece6`) | Δ | Verdict move |
|---|---|---|---|---|
| `text.primary` | 18.10 | **15.94** | −2.16 | PASS → PASS |
| `text.secondary` | 7.81 | **6.61** | −1.20 | PASS → PASS |
| `text.helper` | 5.02 | **6.61** | +1.59 | PASS → PASS · alias moved |
| `text.error` | 5.00 | **6.59** | +1.59 | PASS → PASS · alias moved |
| `link.primary` | 5.00 | **6.59** | +1.59 | PASS → PASS · alias moved |
| `link.secondary` | 7.79 | **6.59** | −1.20 | PASS → PASS |
| `link.visited` | 5.00 | **6.54** | +1.54 | PASS → PASS · alias moved |
| `support.error` | 5.00 | **4.23** | −0.77 | PASS → PASS |
| `support.success` | 3.35 | **4.24** | +0.89 | PASS → PASS · alias moved |
| `support.warning` | 1.68 | **4.22** | +2.54 | **FAIL → PASS** · alias moved |
| `support.info` | 7.79 | **6.59** | −1.20 | PASS → PASS |
| `support.caution-minor` | 1.68 | **1.42** | −0.26 | FAIL → **FAIL, worse** |
| `support.caution-major` | 2.46 | **2.08** | −0.38 | FAIL → **FAIL, worse** |
| `border.subtle-00` | 1.32 | **1.11** | −0.21 | FAIL → **FAIL, worse** |
| `border.subtle-01` | 1.71 | **1.44** | −0.27 | FAIL → **FAIL, worse** |
| `border.strong-01` | 3.32 | **4.25** | +0.93 | PASS → PASS · alias moved |
| `border.tile-02` | 2.38 | **2.01** | −0.37 | FAIL → **FAIL, worse** |
| `border.interactive` | 5.00 | **4.23** | −0.77 | PASS → PASS |
| `focus` | 5.00 | **4.23** | −0.77 | PASS → PASS |
| chart 1 `blue.60` | 5.00 | **4.23** | −0.77 | PASS → PASS |
| chart 2 `teal.60` | 4.99 | **4.22** | −0.77 | PASS → PASS |
| chart 3 `purple.60` | 5.00 | **4.23** | −0.77 | PASS → PASS |
| chart 4 `magenta.60` | 5.01 | **4.23** | −0.78 | PASS → PASS |
| chart 5 `cyan.40` | 2.37 | **2.00** | −0.37 | FAIL → **FAIL, worse** |

**Reading it.** Every unchanged token lost roughly 0.77 (text) or 0.2–0.4 (already-failing
non-text) simply because bone is darker than white. Every token that *gained* gained because its
alias was darkened one palette step — and the pattern is unmistakable: `blue.60 → blue.70`,
`purple.60 → purple.70`, `red.60 → red.70`, `gray.60 → gray.70`, `gray.50 → gray.60`,
`green.50 → green.60`, `yellow.30 → yellow.60`. *Inferred* — that this was a deliberate
darkening pass to hold 4.5:1 against the new bone ground. The evidence is that `blue.60` as
`link.primary` would measure **4.23:1 on bone and fail**, and `blue.70` measures 6.59. This audit
cannot see the commit history (no `Bash`) and does not attribute the change; it records that
0.1.0 and 0.2.0 hold different aliases under the same names.

### 3.2 Table B — same physical ground `#ffffff` (now `semantic.layer.02`)

Holding the ground constant isolates alias movement from ground movement.

| Foreground | v1 on `#ffffff` | v2 on `#ffffff` | Δ | Cause |
|---|---|---|---|---|
| `text.primary` | 18.10 | **18.83** | +0.73 | `{gray.100}` → `{ink.default}` |
| `text.secondary` | 7.81 | **7.81** | 0.00 | unchanged |
| `text.helper` | 5.02 | **7.81** | +2.79 | `{gray.60}` → `{gray.70}` |
| `text.error` | 5.00 | **7.79** | +2.79 | `{red.60}` → `{red.70}` |
| `link.primary` | 5.00 | **7.79** | +2.79 | `{blue.60}` → `{blue.70}` |
| `link.secondary` | 7.79 | **7.79** | 0.00 | unchanged |
| `link.visited` | 5.00 | **7.73** | +2.73 | `{purple.60}` → `{purple.70}` |
| `support.success` | 3.35 | **5.01** | +1.66 | `{green.50}` → `{green.60}` |
| `support.warning` | 1.68 | **4.98** | +3.30 | `{yellow.30}` → `{yellow.60}` |
| `support.caution-minor` | 1.68 | **1.68** | 0.00 | unchanged |
| `support.caution-major` | 2.46 | **2.46** | 0.00 | unchanged |
| `border.subtle-00` | 1.32 | **1.32** | 0.00 | unchanged |
| `border.subtle-01` | 1.71 | **1.70** | 0.00 (conv.) | unchanged; 1.7082 floored |
| `border.strong-01` | 3.32 | **5.02** | +1.70 | `{gray.50}` → `{gray.60}` |
| `border.tile-02` | 2.38 | **2.37** | 0.00 (conv.) | unchanged; 2.3781 floored |
| chart 2 `teal.60` | 4.99 | **4.98** | 0.00 (conv.) | unchanged; 4.9883 floored |
| chart 4 `magenta.60` | 5.01 | **5.00** | 0.00 (conv.) | unchanged; 5.0074 floored |
| chart 5 `cyan.40` | 2.37 | **2.36** | 0.00 (conv.) | unchanged; 2.3667 floored |

Dark-theme rows are all `0.00` or `0.00 (conv.)`: no dark opaque text alias moved. v1's
6.36 / 8.86 / 8.88 appear here as 6.35 / 8.85 / 8.87 for the same reason.

### 3.3 Table C — the alpha repair, the most important table in this artifact

**Nine alpha-carrying tokens are foregrounds over a named ground and are now measurable.**
"v1 record" is what ART-008 published. "As rendered in 0.1.0" is what a consumer actually got,
because — this is C-021's own finding — nothing applied the modifier, so the token rendered at
full opacity.

| Token | v1 record | As rendered in 0.1.0 (opaque) | v2 (composited) | Threshold |
|---|---|---|---|---|
| `text.placeholder` → bone / f4 / white | **skipped** (F-10) | 15.94 / 17.12 / 18.83 | **2.49 / 2.52 / 2.55** | 4.5 |
| `text.disabled` → bone / f4 / white | **skipped** | 15.94 / 17.12 / 18.83 | **1.70 / 1.71 / 1.73** | 4.5 |
| `icon.disabled` → bone / f4 / white | **skipped** | 15.94 / 17.12 / 18.83 | **1.70 / 1.71 / 1.73** | 3 |
| `semantic-dark.text.placeholder` → D1 / D2 | **skipped** | 16.45 / 13.74 | **3.59 / 3.44** | 4.5 |
| `semantic-dark.text.disabled` → D1 / D2 | **skipped** | 16.45 / 13.74 | **2.15 / 2.17** | 4.5 |
| `semantic-dark.icon.disabled` → D1 / D2 | **skipped** | 16.45 / 13.74 | **2.15 / 2.17** | 3 |
| `semantic-dark.text.on-color-disabled` → brand | **skipped** | 5.00 | **1.50** | 4.5 |
| `semantic-dark.icon.on-color-disabled` → brand | **skipped** | 5.00 | **1.50** | 3 |
| `semantic-dark.border.disabled` → D1 / D2 | **skipped** | 5.45 / 4.55 | **2.29 / 2.17** | 3 |

**Two honest answers to "how many got worse", because they are different questions.**

- **Against v1's published record: zero passes were invalidated.** ART-008 passed none of these.
  It put all 21 alpha aliases in bucket S3, said "skipped, not passed", and escalated
  `text.placeholder` as F-10 with both readings including the failing one. v1's assumption A-2
  ("`alphaModifier` is not applied") is now **falsified by the token file** — and v1's refusal to
  publish a number on that assumption is exactly why nothing has to be retracted. The
  conservative call held.
- **Against what actually rendered in 0.1.0: nine tokens, nineteen pairs, every one falls from a
  comfortable pass to a value below threshold.** The largest single fall is
  `semantic-dark.text.disabled` on `semantic-dark.background`: **16.45 → 2.15**, a drop of 14.30.
  These are not new defects introduced by C-021. They are defects that C-021 made *visible* — the
  translucency was always the designed intent, and until 2026-09-01 the token layer silently
  ignored it.

**Fourteen of those nineteen pairs are exempt** under WCAG 2.2's inactive-component exception
(every `*.disabled` role). **Five are not**: the three light and two dark `text.placeholder`
pairs. Placeholder text is live, active text, and `rules.md` separately notes that placeholder
is not a label.

### 3.4 v1 findings now resolved

| v1 ID | Subject | Status in 0.2.0 |
|---|---|---|
| F-01 | `support.warning` `{yellow.30}` at 1.68:1 | **RESOLVED** — now `{yellow.60}` `#8e6a00`, 4.22 / 4.53 / 4.98, passes 3:1 on all three grounds |
| F-08 | `border.strong-01` thin margin 3.02 (+0.02) | **RESOLVED** — now `{gray.60}` `#6f6f6f`, 4.25 / 4.56 / 5.02 |
| F-09 | `support.success` thin margin 3.05 (+0.05) | **RESOLVED** — now `{green.60}` `#198038`, 4.24 / 4.56 / 5.01 |
| F-10 | `text.placeholder` unevaluable, two readings | **RESOLVED as an ambiguity** — the token layer now says which. Superseded by F-14, which is the measurement |
| F-11 | `semantic.background` is `#ffffff`, a brand drift | **RESOLVED** — now `{bone.default}` `#eeece6` |
| F-12 | No coral token exists; OQ-6 open | **RESOLVED** — `palette.coral.{default,text}` minted and `semantic.accent.{container,text}` added in both themes |

---

## 4. What was skipped — 420 of 472 aliases

**Skipped is not passed.** These aliases were not evaluated. No claim is made about their
contrast in either direction.

Of 472 semantic colour aliases, **52** appear on one side of a computed pair (34 in `semantic.*`,
18 in `semantic-dark.*`). The remaining **420** are skipped, in four buckets:

| Bucket | Count | Reason |
|---|---|---|
| **S1** — `syntax.*` (88 light + 88 dark) | **176** | Code-editor foreground set. There is still no `semantic.syntax.background` token, so these foregrounds have **no defined ground** in the token layer. Verified again in 0.2.0: no `syntax.*` leaf carries alpha, so C-021 did not touch this bucket. Unevaluable, not passing. |
| **S2** — `ai.*` and `chat.*` (42 light + 42 dark) | **84** | Outside the declared L1 scope: no `cf-*` primitive's `tokens_used` names them. **32 of these now carry real alpha** and 6 are the α = 0 tokens of §2. `chat.*` remains the highest-value extension of scope — alone in this file it declares explicit foreground/background pairs by name (`bubble-agent-text` on `bubble-agent`, `header-text` on `header-background`, `prompt-text` on `prompt-background`). Those are genuinely checkable and were skipped for scope, not for ambiguity. |
| **S3** — alpha-carrying **surfaces** (6 light + 6 dark) | **12** | `background-{hover,active,selected,selected-hover}`, `overlay` and `shadow` in both themes. These now composite correctly, but a composited surface is a **ground, not a foreground**: it has no named partner to be measured against. See F-24 — this is the bucket that hides the most risk. |
| **S4** — state and layer variants, and the two uncomputed dark surfaces | **148** | Hover / active / selected / disabled / `-02` / `-03` / `-inverse` variants whose "ground" is a *state* of a surface, plus `semantic-dark.layer.{02,03}` (F-25) and `semantic.accent.container`'s dark twin. Several are value-identical to a token that **was** computed — `border.tile-01`, `border.subtle-selected-01` and `border.disabled` all resolve to `{gray.30}`, the same value as `border.subtle-01` at 1.44:1 on bone. **That expectation is an inference, not a measurement, and this audit does not report inferred ratios as checked.** |
| | **420** | |

Arithmetic: 176 + 84 + 12 + 148 = 420; 420 + 52 = 472.
Light leaves enumerated: 8 top-level scalars + 29 `layer` + 6 `field` + 16 `border` + 9 `text` +
8 `link` + 7 `icon` + 11 `support` + 8 scalars + 2 `skeleton` + 88 `syntax` + 21 `ai` +
21 `chat` + **2 `accent`** = **236**. `semantic-dark.*` mirrors the structure (Assumption A-3).

**Also out of scope, stated so it is not mistaken for coverage:** target size (24×24 CSS px),
focus order, focus visibility, programmatic labels, `prefers-reduced-motion` and heading
structure — five checks in `rules.md` that a **token file cannot answer**. They are properties of
a rendered screen. They were not run and must be run against a `ui-screen` artifact before the
Phase 4 a11y filter is complete for any screen.

---

## 5. Measurements

Every row states the resolved hex on both sides. Grounds: **G1** bone `#eeece6`, **G2**
`#f4f4f4`, **G3** `#ffffff`, **D1** `#161616`, **D2** `#262626`.

### Set 1 — light opaque text foregrounds (threshold 4.5:1)

| Foreground token | Resolves to | G1 bone | G2 `#f4f4f4` | G3 `#ffffff` |
|---|---|---|---|---|
| `text.primary` | `{ink.default}` `#041222` | **15.94** PASS | **17.12** PASS | **18.83** PASS |
| `text.secondary` | `{gray.70}` `#525252` | **6.61** PASS | **7.10** PASS | **7.81** PASS |
| `text.helper` | `{gray.70}` `#525252` | **6.61** PASS | **7.10** PASS | **7.81** PASS |
| `text.error` | `{red.70}` `#a2191f` | **6.59** PASS | **7.08** PASS | **7.79** PASS |
| `link.primary` | `{blue.70}` `#0043ce` | **6.59** PASS | **7.08** PASS | **7.79** PASS |
| `link.secondary` | `{blue.70}` `#0043ce` | **6.59** PASS | **7.08** PASS | **7.79** PASS |
| `link.visited` | `{purple.70}` `#6929c4` | **6.54** PASS | **7.03** PASS | **7.73** PASS |
| `accent.text` | `{coral.text}` `#b03822` | **5.17** PASS | **5.55** PASS | **6.11** PASS |

24 pairs, 0 failures. The light theme now has materially more headroom than in 0.1.0 — its
tightest text pair is 5.17:1 against v1's 4.55:1 — despite a darker ground. That is the
darkening pass in Table B doing its work. See F-26: `text.helper` and `text.secondary` are now
the same value, as are `link.primary` and `link.secondary`.

### Set 2 — dark opaque text foregrounds (threshold 4.5:1)

| Foreground token | Resolves to | D1 `#161616` | D2 `#262626` |
|---|---|---|---|
| `semantic-dark.text.primary` | `{gray.10}` `#f4f4f4` | **16.45** PASS | **13.74** PASS |
| `semantic-dark.text.secondary` | `{gray.30}` `#c6c6c6` | **10.59** PASS | **8.85** PASS |
| `semantic-dark.text.helper` | `{gray.40}` `#a8a8a8` | **7.61** PASS | **6.35** PASS |
| `semantic-dark.text.error` | `{red.40}` `#ff8389` | **7.63** PASS | **6.37** PASS |
| `semantic-dark.link.primary` | `{blue.40}` `#78a9ff` | **7.68** PASS | **6.42** PASS |
| `semantic-dark.link.secondary` | `{blue.30}` `#a6c8ff` | **10.62** PASS | **8.87** PASS |
| `semantic-dark.link.visited` | `{purple.40}` `#be95ff` | **7.70** PASS | **6.43** PASS |
| `semantic-dark.accent.text` | `{coral.default}` `#f15b40` | **5.43** PASS | **4.54** PASS (F-22) |

16 pairs, 0 failures. The dark accent passes on `layer.01` by 0.04 — see F-22.

### Set 3 — text on inverse and brand grounds (threshold 4.5:1)

| Pair | Resolves to | Computed | Verdict |
|---|---|---|---|
| `text.inverse` → `background-inverse` | `#ffffff` on `{gray.80}` `#393939` | **11.54** | PASS |
| `text.on-color` → `background-brand` | `#ffffff` on `{blue.60}` `#0f62fe` | **5.00** | PASS |
| `link.inverse` → `background-inverse` | `{blue.40}` `#78a9ff` on `#393939` | **4.90** | PASS |

3 pairs, 0 failures.

### Set 4 — `support.*` as non-text / status fill (threshold 3:1)

| Token | Resolves to | G1 bone | G2 `#f4f4f4` | G3 `#ffffff` |
|---|---|---|---|---|
| `support.error` | `{red.60}` `#da1e28` | **4.23** PASS | **4.54** PASS | **5.00** PASS |
| `support.success` | `{green.60}` `#198038` | **4.24** PASS | **4.56** PASS | **5.01** PASS |
| `support.warning` | `{yellow.60}` `#8e6a00` | **4.22** PASS | **4.53** PASS | **4.98** PASS |
| `support.info` | `{blue.70}` `#0043ce` | **6.59** PASS | **7.08** PASS | **7.79** PASS |
| `support.caution-minor` | `{yellow.30}` `#f1c21b` | **1.42** FAIL | **1.53** FAIL | **1.68** FAIL (F-02) |
| `support.caution-major` | `{orange.40}` `#ff832b` | **2.08** FAIL | **2.23** FAIL | **2.46** FAIL (F-03) |
| `support.caution-undefined` | `{purple.60}` `#8a3ffc` | **4.23** PASS | **4.54** PASS | **5.00** PASS |

21 pairs, 6 failures. `caution-undefined` is new to scope in v2 and has no v1 counterpart.

**Ambiguity, recorded rather than resolved (carried from v1, still open).** `cf-badge` declares
only `support.{error,success,warning,info}` in `tokens_used`. It declares **no paired text colour
and no paired fill colour**, so whether `support.warning` is the badge's *fill* or its *label* is
undetermined by the system. The non-text reading above is the one that holds either way. **The
text reading — these colours as a small label at 4.5:1 — was not computed and is not claimed.**
All four badge tokens now clear 4.5:1 on every light ground anyway (4.22–7.79), so as of 0.2.0
the ambiguity no longer hides a failure. It still hides a contract gap.

### Set 5 — borders, focus and the brand accent as non-text (threshold 3:1)

| Token | Resolves to | G1 bone | G2 `#f4f4f4` | G3 `#ffffff` |
|---|---|---|---|---|
| `border.subtle-00` | `{gray.20}` `#e0e0e0` | **1.11** FAIL | **1.20** FAIL | **1.32** FAIL (F-04) |
| `border.subtle-01` | `{gray.30}` `#c6c6c6` | **1.44** FAIL | **1.55** FAIL | **1.70** FAIL (F-05) |
| `border.strong-01` | `{gray.60}` `#6f6f6f` | **4.25** PASS | **4.56** PASS | **5.02** PASS |
| `border.tile-02` | `{gray.40}` `#a8a8a8` | **2.01** FAIL | **2.16** FAIL | **2.37** FAIL (F-06) |
| `border.interactive` | `{blue.60}` `#0f62fe` | **4.23** PASS | **4.54** PASS | **5.00** PASS |
| `focus` | `{blue.60}` `#0f62fe` | **4.23** PASS | **4.54** PASS | **5.00** PASS |
| `accent.container` | `{coral.default}` `#f15b40` | **2.81** FAIL (F-21) | **3.02** PASS (F-23) | **3.32** PASS |

| Pair | Resolves to | Computed | Verdict |
|---|---|---|---|
| `semantic-dark.focus` → D1 | `#ffffff` on `#161616` | **18.10** | PASS |
| `semantic-dark.focus` → D2 | `#ffffff` on `#262626` | **15.12** | PASS |

23 pairs, 10 failures. **The focus indicator colour passes on every ground tested, in both
themes, with margin** — and it gained a ground in v2 without breaking. `rules.md` also requires
focus to be *always visible and never suppressed* with focus order following reading order;
neither is a token property and neither was checked (see §4).

### Set 6 — `cf-chart-palette` series marks (threshold 3:1)

v1 computed this set against one ground and said the others were not claimed. All three are
computed here.

| Series | Token | Resolves to | G1 bone | G2 `#f4f4f4` | G3 `#ffffff` |
|---|---|---|---|---|---|
| 1 | `palette.blue.60` | `#0f62fe` | **4.23** PASS | **4.54** PASS | **5.00** PASS |
| 2 | `palette.teal.60` | `#007d79` | **4.22** PASS | **4.53** PASS | **4.98** PASS |
| 3 | `palette.purple.60` | `#8a3ffc` | **4.23** PASS | **4.54** PASS | **5.00** PASS |
| 4 | `palette.magenta.60` | `#d02670` | **4.23** PASS | **4.55** PASS | **5.00** PASS |
| 5 | `palette.cyan.40` | `#33b1ff` | **2.00** FAIL | **2.15** FAIL | **2.36** FAIL (F-07) |

15 pairs, 3 failures. Four of five series sit within 0.03 of each other on any given ground; the
fifth is roughly half. On the brand ground the gap is 4.22 against 2.00.

### Set 7 — alpha-composited foregrounds (thresholds as marked)

**The heart of this artifact.** Every row composites per §1.3 before computing the ratio. The
`α` column is the value now carried by the aliased primitive, not the inert
`org.carbon.alphaModifier` extension.

| Token | Resolves to | α | Ground | Composite | Computed | Thr. | Verdict |
|---|---|---|---|---|---|---|---|
| `text.placeholder` | `{gray.100-a40}` | 0.40 | G1 bone | `#98978f` | **2.49** | 4.5 | FAIL (F-14) |
| `text.placeholder` | | 0.40 | G2 | `#9b9b9b` | **2.52** | 4.5 | FAIL (F-14) |
| `text.placeholder` | | 0.40 | G3 | `#a2a2a2` | **2.55** | 4.5 | FAIL (F-14) |
| `text.disabled` | `{gray.100-a25}` | 0.25 | G1 bone | `#b8b6b2` | **1.70** | 4.5 | FAIL* (F-15) |
| `text.disabled` | | 0.25 | G2 | `#bcbcbc` | **1.71** | 4.5 | FAIL* (F-15) |
| `text.disabled` | | 0.25 | G3 | `#c4c4c4` | **1.73** | 4.5 | FAIL* (F-15) |
| `icon.disabled` | `{gray.100-a25}` | 0.25 | G1 bone | `#b8b6b2` | **1.70** | 3 | FAIL* (F-16) |
| `icon.disabled` | | 0.25 | G2 | `#bcbcbc` | **1.71** | 3 | FAIL* (F-16) |
| `icon.disabled` | | 0.25 | G3 | `#c4c4c4` | **1.73** | 3 | FAIL* (F-16) |
| `dark.text.placeholder` | `{gray.10-a40}` | 0.40 | D1 | `#6f6f6f` | **3.59** | 4.5 | FAIL (F-17) |
| `dark.text.placeholder` | | 0.40 | D2 | `#787878` | **3.44** | 4.5 | FAIL (F-17) |
| `dark.text.disabled` | `{gray.10-a25}` | 0.25 | D1 | `#4e4e4e` | **2.15** | 4.5 | FAIL* (F-18) |
| `dark.text.disabled` | | 0.25 | D2 | `#5a5a5a` | **2.17** | 4.5 | FAIL* (F-18) |
| `dark.icon.disabled` | `{gray.10-a25}` | 0.25 | D1 | `#4e4e4e` | **2.15** | 3 | FAIL* (F-18) |
| `dark.icon.disabled` | | 0.25 | D2 | `#5a5a5a` | **2.17** | 3 | FAIL* (F-18) |
| `dark.text.on-color-disabled` | `{white.default-a25}` | 0.25 | `background-brand` `#0f62fe` | `#4b89fe` | **1.50** | 4.5 | FAIL* (F-19) |
| `dark.icon.on-color-disabled` | `{white.default-a25}` | 0.25 | `background-brand` `#0f62fe` | `#4b89fe` | **1.50** | 3 | FAIL* (F-19) |
| `dark.border.disabled` | `{gray.50-a50}` | 0.50 | D1 | `#525252` | **2.29** | 3 | FAIL* (F-20) |
| `dark.border.disabled` | | 0.50 | D2 | `#5a5a5a` | **2.17** | 3 | FAIL* (F-20) |

19 pairs, **19 below threshold**. `*` marks the 14 that fall under WCAG 2.2's inactive-component
exception (SC 1.4.3 and 1.4.11 both exempt disabled components). The 5 unstarred pairs are
`text.placeholder` in both themes and are **not** exempt.

Composite hexes are rounded to the nearest byte for display; ratios were computed from the exact
unrounded composite, which is why `#a2a2a2` reads 2.55 here and v1's hand-derived `#a2a2a2` read
2.56.

---

## 6. Finding register

28 entries, F-01 to F-28. IDs are carried from ART-008 where the subject is the same, so a
reader can follow one concern across both versions. **6 entries record a v1 finding now
resolved; 22 are open.**

Fixing any of these is **`token-keeper`'s** work. Changing the brand position is
**`brand-director`'s**. This register records; it does not propose values.

### 6.1 Resolved since v1 — no action

**F-01** · resolved · `support.warning` `{yellow.30}` → `{yellow.60}`, 1.68 → 4.22/4.53/4.98.
**F-08** · resolved · `border.strong-01` `{gray.50}` → `{gray.60}`, thin margin gone (4.25 min).
**F-09** · resolved · `support.success` `{green.50}` → `{green.60}`, thin margin gone (4.24 min).
**F-10** · resolved as an ambiguity · `text.placeholder` now has one reading. The reading is a
failure; that is **F-14**, not this entry. Closing an ambiguity is not closing a defect.
**F-11** · resolved · `semantic.background` = `{bone.default}` `#eeece6`. brand.md §6's "drift to
`#ffffff`" no longer describes the token layer.
**F-12** · resolved · coral exists. `palette.coral.default` `#f15b40`, `palette.coral.text`
`#b03822`, surfaced as `semantic.accent.{container,text}` in both themes. **OQ-6 is answered.**
The §3 coral rule is no longer upheld vacuously — it now has something to bind to, and the
binding is expressed in the token layer as two separate roles. See F-21 and F-26.

### 6.2 Measurement failures — open

| ID | Sev | Token → ground | Computed | Thr. | Note |
|---|---|---|---|---|---|
| **F-02** | error | `support.caution-minor` `{yellow.30}` `#f1c21b` → G1/G2/G3 | **1.42 / 1.53 / 1.68** | 3 | worse than v1 on the brand ground |
| **F-03** | error | `support.caution-major` `{orange.40}` `#ff832b` → G1/G2/G3 | **2.08 / 2.23 / 2.46** | 3 | worse than v1 |
| **F-04** | warning | `border.subtle-00` `{gray.20}` `#e0e0e0` → G1/G2/G3 | **1.11 / 1.20 / 1.32** | 3 | 1.4.11 scope call |
| **F-05** | warning | `border.subtle-01` `{gray.30}` `#c6c6c6` → G1/G2/G3 | **1.44 / 1.55 / 1.70** | 3 | 1.4.11 scope call |
| **F-06** | warning | `border.tile-02` `{gray.40}` `#a8a8a8` → G1/G2/G3 | **2.01 / 2.16 / 2.37** | 3 | 1.4.11 scope call |
| **F-07** | error | chart series 5 `palette.cyan.40` `#33b1ff` → G1/G2/G3 | **2.00 / 2.15 / 2.36** | 3 | |
| **F-14** | error | `text.placeholder` `{gray.100-a40}` → G1/G2/G3 | **2.49 / 2.52 / 2.55** | 4.5 | **not exempt** |
| **F-15** | warning | `text.disabled` `{gray.100-a25}` → G1/G2/G3 | **1.70 / 1.71 / 1.73** | 4.5 | exempt *if* inactive |
| **F-16** | warning | `icon.disabled` `{gray.100-a25}` → G1/G2/G3 | **1.70 / 1.71 / 1.73** | 3 | exempt *if* inactive |
| **F-17** | error | `semantic-dark.text.placeholder` `{gray.10-a40}` → D1/D2 | **3.59 / 3.44** | 4.5 | **not exempt** |
| **F-18** | warning | `semantic-dark.{text,icon}.disabled` `{gray.10-a25}` → D1/D2 | **2.15 / 2.17** | 4.5 / 3 | exempt *if* inactive |
| **F-19** | warning | `semantic-dark.{text,icon}.on-color-disabled` `{white.default-a25}` → `background-brand` | **1.50** | 4.5 / 3 | exempt *if* inactive |
| **F-20** | warning | `semantic-dark.border.disabled` `{gray.50-a50}` → D1/D2 | **2.29 / 2.17** | 3 | exempt *if* inactive |
| **F-21** | error | `accent.container` `{coral.default}` `#f15b40` → G1 bone | **2.81** | 3 | brand accent on brand ground |

**F-02 / F-03 — the two `caution-*` tokens are now the worst numbers in the layer, and they are
alone there.** `support.warning` was repaired; `caution-minor` resolves to the same `{yellow.30}`
the warning token used to, and was not. A designer reaching for "a caution colour" now gets
4.22:1 or 1.42:1 depending on which of two adjacent names they pick. Neither is named by
`cf-badge`, which is the only reason this is not worse.

**F-04 / F-05 / F-06 — borders, with a judgement a human must make.** WCAG 1.4.11 applies to
visual information required to identify a UI component or its state. It does not apply to purely
decorative boundaries. Where `border.subtle-01` is a `cf-rule` divider between sections already
separated by whitespace, 1.44:1 is arguably outside 1.4.11's scope; where it is the **only** thing
marking a `cf-card` boundary or a `cf-table` cell edge, it is inside scope and it fails. That
distinction is made per screen, not per token, which is why these are `warning` and why they are
exactly the kind of call Gate A exists for. `border.strong-01` now passes with real margin
(4.25 minimum, against v1's 3.02) and is the token that satisfies 1.4.11 today.

**F-14 / F-17 — placeholder text is the headline defect of release 0.2.0.** The v1 ambiguity is
closed and the answer is the bad one: 2.49:1 on the brand ground in light, 3.44:1 in dark, against
a 4.5:1 floor. This is the only *non-exempt* failure the alpha repair exposed, it appears in both
themes, and `rules.md` separately warns that placeholder is not a label — so a form that leans on
placeholder text is failing twice, in different ways.

**F-15 / F-16 / F-18 / F-19 / F-20 — below threshold, and probably permitted.** WCAG 2.2 exempts
inactive components from both 1.4.3 and 1.4.11. Every one of these tokens names a disabled state,
so the exemption most likely applies and this audit does **not** call them failures of the
standard. They are recorded at full value for one reason: **the exemption is a property of the
component, not of the token.** `text.disabled` at 1.70:1 used as "de-emphasised text" — a
mistake nothing in this repository currently prevents — is not an inactive component and is a
hard failure. That is a screen-level check, not a token-level one, and it belongs to whoever
reviews the first screen that uses these tokens.

**F-21 — the brand accent does not clear 3:1 on the brand ground.** `accent.container` is
`{coral.default}` `#f15b40` and `semantic.background` is `{bone.default}` `#eeece6`: **2.81:1**.
The token's own `$description` states the coral text rule and quotes 2.82 on bone, so the number
is known upstream; what is recorded here is its **consequence for 1.4.11**. If a coral fill is
ever the sole carrier of a control's boundary or state on the page ground, it is below the
non-text floor. If it is a decorative fill with its own text and border, 1.4.11 does not engage.
This is a `brand-director` question before it is a `token-keeper` one, and it is not this agent's
to answer.

### 6.3 Thin-margin passes — flagged, not failed

| ID | Sev | Pair | Computed | Thr. | Margin |
|---|---|---|---|---|---|
| **F-22** | info | `semantic-dark.accent.text` `{coral.default}` `#f15b40` → `semantic-dark.layer.01` `#262626` | **4.54** | 4.5 | +0.04 |
| **F-23** | info | `semantic.accent.container` `{coral.default}` `#f15b40` → `semantic.layer.01` `#f4f4f4` | **3.02** | 3 | +0.02 |

These **pass**. They are recorded because the margin is inside the width of a rounding error, so
any nudge to either side flips them without anyone noticing. F-22 is the more interesting: the
dark accent was chosen on measurement against `semantic-dark.background` (5.43), and the token's
`$description` records that choice — but `layer.01` is also a dark surface, nobody measured it,
and it is where the margin nearly runs out. F-23 is the same coral one ground away from the
2.81:1 failure in F-21.

### 6.4 Structural findings

**F-24 — severity: warning. The alpha repair created composited *surfaces* that no pair names,
and every ratio in Sets 1–6 quietly assumes they are not there.** `background-hover`,
`background-active`, `background-selected` and `background-selected-hover` now composite grey at
12–50% over whatever is beneath them, in both themes — twelve aliases in bucket S3. Each one
produces a **new effective ground** that is darker than the base surface. Every light text ratio
in Set 1 was computed against the *base* surface; a row that is hovered or selected is a
different ground, and no token pairs any foreground with it. In 0.1.0 this did not matter,
because the modifier was inert and these tokens rendered as flat opaque greys. **It matters now.**
This is the single largest piece of unmeasured surface area C-021 created, and closing it needs a
naming decision (which foreground goes on which state) before it can need a measurement.

**F-25 — severity: warning. The dark theme has four distinct surfaces; v1 asserted two, and only
two were computed here.** `semantic-dark.layer.02` is `{gray.80}` `#393939` and `layer.03` is
`{gray.70}` `#525252`. `cf-card`, `cf-table` and `cf-colour-roles` all declare `semantic.layer.*`,
so a card on a card is reachable by contract. Against `#525252` (L = 0.084), `text.helper`
`{gray.40}` would fall to roughly 3.3:1 — **that number is an illustration of the risk, is not a
measurement, and is not counted as checked.** Recorded so that "the dark theme has more headroom"
is not carried forward from v1 as if it had been verified on every dark surface. It was verified
on two of four.

**F-26 — severity: info. Two names, one value, twice.** `text.helper` and `text.secondary` both
resolve to `{gray.70}`; `link.primary` and `link.secondary` both resolve to `{blue.70}`. Both
pairs pass. The finding is not contrast — it is that the layer now offers a distinction it does
not deliver, so a designer who picks `helper` to sit visibly below `secondary` gets no visual
difference and will reach for a raw value to make one. `link.primary-hover` also equals
`link.primary`, so the light theme has no hover feedback on links at the token level. Same class
of defect as the `gray.10Hover` / `white.Hover` duplication that `palette` documents and keeps
deliberately — but this one is not documented, and unlike that one it collapses two roles a
designer must choose between.

**F-27 — severity: warning. The per-component a11y contract in `component-index.json` is still
not true of the tokens those components name.** Every L1 entry declares
`"contrast": "WCAG 2.2 AA — 4.5:1 text, 3:1 non-text"`. `cf-rule` and `cf-card` name
`semantic.border.subtle-01`, which measures **1.44:1 on the page ground**. `cf-chart-palette`
names `palette.cyan.40` at **2.00:1**. The assertion is a claim the index makes about itself and
nothing checks it. Carried and sharpened from v1: the numbers moved, the gap did not.

**F-28 — severity: info. Two contrast ratios recorded in `tokens.json` `$description` fields do
not match recomputation.** `semantic.accent.text`'s description states `{coral.text}` measures
"2.95:1 against semantic-dark.background"; recomputation gives **2.96** (2.9611, which neither
rounds nor truncates to 2.95). The same description states `{coral.default}` measures 5.43 there;
recomputation gives 5.4395 — 5.43 truncated, 5.44 rounded, so that one is convention. Five other
ratios in `palette` descriptions match exactly (§1.3). The discrepancy is 0.01 and changes no
verdict. It is recorded because **a number in a `$description` is documentation, not an audited
measurement**, and if descriptions are treated as evidence the difference between the two stops
being visible. Correcting it is `token-keeper`'s; this agent cannot edit that file.

**F-13 — severity: info (restated from v1, now partly false). The semantic layer is still
mostly Carbon carried through verbatim, but no longer entirely.** v1 recorded that the four brand
decisions in `brand.md` §3 had **no** representation in the colour layer. As of 0.2.0, three of
the four do, through exactly **six** of 472 aliases: `semantic.background` → bone,
`semantic.text.primary` → ink, and `accent.{container,text}` in both themes. The remaining 466
still resolve into Carbon's palette. `semantic-dark.background` is still `{gray.100}`, not a
brand value. This corroborates the declared design-system state **RED** at the colour axis
(CLAUDE.md, ADR-011) while recording that the axis has begun to move: the layer is no longer
purely a Carbon mirror, and the first six exceptions are the ones brand.md §3 names first.

---

## 7. Claims

Per `brand.md` §1, every claim carries its ground.

- **Evidenced [ART-009 § 5. Measurements]** — every ratio in this document. These are
  measurements of token values, not testimony; per ADR-017 they take the artifact form, never a
  ledger ID. **No `[E-nnn]` appears in this artifact and none was minted:**
  `research/evidence-ledger.json` is empty, no user was asked about any of this, and a contrast
  ratio is not something a person said.
- **Evidenced [ART-009 § 3. Movement since v1]** — every delta. v1 values are quoted from
  `artifacts/brand-foundations/2026-08-31__a11y-audit__semantic-colour-layer__v1/semantic-colour-contrast-audit.md`,
  which was read in full for this run; v2 values are recomputed from 0.2.0. No v1 number was
  reused as a v2 number.
- **Evidenced** (by direct enumeration of `design-system/tokens/tokens.json` at release 0.2.0) —
  35 alpha primitives exist (`black` 9, `blue` 11, `gray` 13, `white` 2); exactly 53 semantic
  aliases point at one (24 light: 9 core + 11 `ai` + 4 `chat`; 29 dark: 12 core + 13 `ai` +
  4 `chat`); exactly 6 resolve to an `alpha: 0.0` primitive; `semantic.*` contains 236 leaves;
  the light theme resolves to three distinct surface values and the dark theme to four.
- **Evidenced** (by direct reading of `design-system/component-index.json`) — the `tokens_used`
  declarations that set scope, and the a11y contract string quoted in F-27.
- **Inferred** — that the seven alias moves in Table B were a deliberate darkening pass to hold
  4.5:1 against the bone ground. *Inferred from* the fact that all seven move one step darker in
  the same direction, and that the previous values fail on bone where the new ones pass. This
  agent cannot read commit history (no `Bash`) and does not attribute the change.
- **Inferred** — that `background-brand` is the correct ground for `*.on-color-disabled`
  (F-19). *Inferred from* v1's treatment of `text.on-color → background-brand` as a measured
  pair. The token names no ground; "on-color" names a class of surface, not a surface.
- **Inferred** — that `border.subtle-01`'s failure does or does not engage 1.4.11 (F-05).
  *Inferred from* the text of 1.4.11. Not decidable from a token; needs a screen.
- **Inferred** — that the value-identical tokens in bucket S4 would return the same ratio as
  their measured twin. Not measured, therefore not counted as checked.
- **Inferred** — that the disabled roles in F-15/16/18/19/20 sit under WCAG's inactive-component
  exception. *Inferred from* the token names, which all say `disabled`. Whether the component is
  genuinely inactive is a screen-level fact.

## 8. Assumptions

Visible and arguable. None is settled by appearing here.

- **A-1.** Assumed the three light grounds and two dark grounds in §1.1 are the surfaces text
  actually lands on, because `cf-colour-roles` and `cf-table` name `semantic.layer.*` and
  `semantic.background` and nothing else. If L1 output composites text over `layer.accent-*`,
  `field.*` or a `-hover` state, those pairs are unmeasured — see F-24.
- **A-2 (v1's assumption, now falsified and replaced).** v1 assumed `alphaModifier` was **not**
  applied on resolution. In 0.2.0 the alpha lives on the primitive, in the `$value`, and is
  unambiguous. v2 assumes instead that **a consumer reads `$value.alpha` and composites in
  sRGB**. If a consumer reads only the 8-digit `hex` and ignores the `alpha` field, it gets the
  same answer; if a consumer reads the first 6 digits of `hex` and ignores the rest — which
  `palette`'s own `$description` warns is a live risk ("two consumers here read hex and never
  look at alpha") — it renders opaque and Set 7 is wrong in the *safe* direction.
- **A-3 (carried from v1, narrowed).** Assumed `semantic-dark.*` contains 236 leaves mirroring
  `semantic.*`. The light count was enumerated group by group; the dark theme's `syntax`,
  `layer`, `ai` and `chat` groups were read as mirroring rather than counted leaf by leaf. If the
  dark theme has a different leaf count, the skipped total of 420 moves by that difference.
- **A-4.** Assumed sRGB throughout. Every `$value` declares `"colorSpace": "srgb"`. No display
  profile was considered and none is encoded.
- **A-5.** Assumed the bone ground is now stable. v1's A-5 assumed the opposite of the same
  question and was right to. `bone.default`, `ink.default`, `coral.*` and the four `accent.*`
  aliases all carry `"gate": "Gate A — suggested by token-keeper; not counted until a human
  approves"`. **Every light-theme number in §5 is therefore measured against a ground that has
  not yet been approved.** If Gate A rejects bone, Table A inverts and the G3 column becomes the
  live one.
- **A-6.** Assumed compositing happens in sRGB, not in linear light. This is what browsers do for
  `background-color` with alpha and it is what the brief specifies. Compositing in linear light
  would give different — and generally more favourable — numbers for the mid-alpha tokens. The
  sRGB reading is the conservative one and it is the one that matches what will be rendered.

## 9. What this audit does not say

- It does not say the colour layer is accessible. It says 121 named pairs were computed, 38 fell
  below threshold, 24 of those are not exempt, and 420 aliases were not examined.
- It does not clear any screen. Target size, focus order and visibility, labels, motion and
  heading structure are all in `rules.md` and none can be checked against a token file.
- It does not say the disabled tokens are compliant. It says WCAG exempts inactive components,
  the exemption is a property of the component, and no component has been checked.
- It does not propose token values. Where a value fails, the finding is the record; choosing a
  replacement is `token-keeper`'s, and choosing whether the brand tolerates it is
  `brand-director`'s.
- It does not mark ART-008 superseded. This agent cannot edit that artifact. See the manifest.
- It is not the verdict. Gate A is.

---

**For Gate A.** Four things are worth a person's attention, in order:

1. **F-14 / F-17 — `text.placeholder` at 2.49:1 light and 3.44:1 dark.** The only non-exempt
   failure the alpha repair exposed, present in both themes, against a 4.5:1 floor.
2. **F-24 — twelve composited state surfaces that no pair names.** The repair made
   `background-hover` and its siblings real, and every text ratio in this document assumes the
   base surface instead. This is unmeasured area, not a measured failure, which is exactly why
   it is easy to miss.
3. **F-21 / F-02 / F-03 — three colours below the 3:1 non-text floor on the brand ground**, one
   of which is the brand's own accent at 2.81:1 on the brand's own page.
4. **A-5 — every light-theme number here is measured against an unapproved ground.** Bone, ink
   and coral all carry `gate: Gate A — not counted until a human approves`. This audit measured
   the token file as it stands. If the ground is rejected, the light column is recomputed, not
   adjusted.
