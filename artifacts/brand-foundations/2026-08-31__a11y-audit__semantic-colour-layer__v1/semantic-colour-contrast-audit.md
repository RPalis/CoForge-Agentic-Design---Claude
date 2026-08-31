# Semantic colour layer — WCAG 2.2 AA contrast audit

**Artifact:** ART-008 · **Type:** `a11y-audit` · **Version:** 1 · **Date:** 2026-08-31
**Produced by:** `a11y-checker` (read-only, Gate B, auto)
**Subject:** `design-system/tokens/tokens.json` — `semantic.*` (234 light aliases) and
`semantic-dark.*` (234 dark aliases) resolving into a 250-entry `palette`.
**Rulebook:** `design-system/a11y/rules.md` · **Floor:** WCAG 2.2 AA.

> **First filter, not the verdict.** This audit is a mechanical pass over computed
> numbers. A human still reviews at Gate A. Nothing below is a design decision and
> nothing below was changed — `a11y-checker` holds no `Edit` and no `Bash`.

**Headline:** 58 pairs computed · 11 measurements below threshold · 13 findings ·
432 of 468 colour aliases **skipped, not passed**.

---

## 1. Scope — what was computed, and why this set

The colour layer is 468 semantic aliases. Auditing "468 aliases" is not meaningful:
an alias is not a contrast pair. Contrast is a property of a **foreground against a
named ground**, and most aliases name neither.

The scope was therefore driven by the `tokens_used` declarations of the eight L1
primitives in `design-system/component-index.json`, which are the only entries that
name specific semantic tokens:

| Primitive | `tokens_used` | What it pins down |
|---|---|---|
| `cf-colour-roles` | `semantic.background`, `semantic.layer.*`, `semantic.text.primary`, `semantic.border.subtle-01` | The grounds and the default ink |
| `cf-table` | `semantic.layer.*`, `semantic.border.subtle-01`, `semantic.text.primary` | Text on layer surfaces; rules between rows |
| `cf-card` | `semantic.layer.*`, `semantic.border.subtle-01` | Card surface and its boundary |
| `cf-rule` | `semantic.border.subtle-01` | A divider |
| `cf-badge` | `semantic.support.{error,success,warning,info}` | Status colour — see the ambiguity note below |
| `cf-chart-palette` | `palette.{blue.60, teal.60, purple.60, magenta.60, cyan.40}` | Five ordered series marks |
| `cf-type-scale`, `cf-spacing-scale` | `typography.*`, `spacing.*` | No colour — out of scope |

The 208 L2 (Carbon) entries all declare the wildcard `semantic.*`. A wildcard names no
pairing, so it cannot generate a checkable pair and did not contribute to scope.

**Grounds used.** After alias resolution the light theme has exactly two distinct
surface values, not three: `semantic.background` and `semantic.layer.02` both resolve
to `{white.default}` = `#ffffff`, and `semantic.layer.01` and `semantic.layer.03` both
resolve to `{gray.10}` = `#f4f4f4`. Every light measurement is therefore taken against
`#ffffff` **or** `#f4f4f4`. Dark uses `semantic-dark.background` = `{gray.100}` =
`#161616` and `semantic-dark.layer.01` = `{gray.90}` = `#262626`.

**Six sets, 58 pairs:**

| Set | Content | Threshold | Pairs |
|---|---|---|---|
| 1 | Light text foregrounds × 2 light grounds | 4.5:1 (normal text) | 14 |
| 2 | Dark text foregrounds × 2 dark grounds | 4.5:1 | 14 |
| 3 | Text on inverse and brand grounds | 4.5:1 | 3 |
| 4 | `support.*` status colours as non-text × 2 light grounds | 3:1 | 12 |
| 5 | Borders and focus indicators as non-text | 3:1 | 10 |
| 6 | `cf-chart-palette` series marks against `semantic.background` | 3:1 | 5 |
| | | **total** | **58** |

**Method.** Each ratio is computed from the resolved sRGB hex by the WCAG 2.x formula:
channel values are normalised to 0–1, linearised (`c/12.92` where `c ≤ 0.04045`, else
`((c+0.055)/1.055)^2.4`), combined as `L = 0.2126R + 0.7152G + 0.0722B`, and the ratio
taken as `(L_lighter + 0.05) / (L_darker + 0.05)`. Ratios are reported to two decimal
places, truncated toward the threshold — a value shown as 3.02:1 is not rounded up from
below 3.0. No script was run; there is no `Bash` in this agent's tool set. Every number
below can be re-derived from the hex pair stated beside it.

**Large-text allowance not used.** `rules.md` permits 3:1 for text ≥ 24px or ≥ 18.66px
bold. A colour token does not carry a size, so no token was granted the large-text
threshold. Every text pair is judged at 4.5:1. This is the conservative reading and it
is stated so a reviewer can see it was a choice, not an oversight.

---

## 2. Finding register

13 findings. Seven are measurement failures (covering 11 of the 58 computed pairs), two
are thin-margin passes flagged for a human, one is an escalated skip, and three are
structural findings about the layer itself.

Fixing any of these is **`token-keeper`'s** work, not this agent's. Changing the brand
position is **`brand-director`'s**. This register records; it does not propose values.

### Measurement failures

| ID | Severity | Token → ground | Computed | Threshold | Verdict |
|---|---|---|---|---|---|
| **F-01** | error | `semantic.support.warning` `{yellow.30}` `#f1c21b` → `semantic.background` `#ffffff` | **1.68:1** | 3:1 non-text | FAIL |
| | | same → `semantic.layer.01` `#f4f4f4` | **1.53:1** | 3:1 | FAIL |
| **F-02** | error | `semantic.support.caution-minor` `{yellow.30}` `#f1c21b` → `#ffffff` | **1.68:1** | 3:1 | FAIL |
| | | same → `#f4f4f4` | **1.53:1** | 3:1 | FAIL |
| **F-03** | error | `semantic.support.caution-major` `{orange.40}` `#ff832b` → `#ffffff` | **2.46:1** | 3:1 | FAIL |
| | | same → `#f4f4f4` | **2.24:1** | 3:1 | FAIL |
| **F-04** | warning | `semantic.border.subtle-00` `{gray.20}` `#e0e0e0` → `#ffffff` | **1.32:1** | 3:1 | FAIL |
| **F-05** | warning | `semantic.border.subtle-01` `{gray.30}` `#c6c6c6` → `#ffffff` | **1.71:1** | 3:1 | FAIL |
| | | same → `#f4f4f4` | **1.55:1** | 3:1 | FAIL |
| **F-06** | warning | `semantic.border.tile-02` `{gray.40}` `#a8a8a8` → `#ffffff` | **2.38:1** | 3:1 | FAIL |
| **F-07** | error | `cf-chart-palette` series 5, `palette.cyan.40` `#33b1ff` → `semantic.background` `#ffffff` | **2.37:1** | 3:1 | FAIL |

**F-01 / F-02 — the yellow is the worst number in the layer.** `{yellow.30}` reaches
1.68:1 on the page ground. It is reached by two separately named tokens, `support.warning`
and `support.caution-minor`, which resolve to the same palette entry, so a designer can
arrive at the same failure from two directions. `cf-badge` names `semantic.support.warning`
directly. Note that the same token's own contract in `component-index.json` asserts
"WCAG 2.2 AA — 4.5:1 text, 3:1 non-text"; that assertion is not currently true of this
value on either light ground.

**F-04 / F-05 / F-06 — borders, with a judgement a human must make.** WCAG 1.4.11 applies
to visual information required to identify a UI component or its state. It does not apply
to purely decorative boundaries. So the verdict here is conditional and I am not closing
it: where `border.subtle-01` is a `cf-rule` divider between sections that are already
distinguishable by spacing, 1.71:1 is arguably outside 1.4.11's scope; where it is the
**only** thing marking a `cf-card` boundary or a `cf-table` cell edge, it is inside scope
and it fails. That distinction is made per screen, not per token, which is why this is
filed as `warning` rather than `error` and why it is exactly the kind of call Gate A
exists for. `semantic.border.strong-01` passes at 3.32:1 and 3.02:1 and is the token that
satisfies 1.4.11 today — see F-10.

**F-07 — one chart series in five cannot carry a mark.** Four of the five ordered series
sit within 0.02 of 5.00:1 on the page ground; the fifth is at 2.37:1. `cf-chart-palette`
says "series colours are ordered — use them in order", so a five-series chart reaches this
value by following the contract correctly. A thin line or a small point in `cyan.40` on
`#ffffff` is not distinguishable to the AA floor.

### Thin-margin passes — flagged, not failed

| ID | Severity | Token → ground | Computed | Threshold | Margin |
|---|---|---|---|---|---|
| **F-08** | info | `semantic.border.strong-01` `{gray.50}` `#8d8d8d` → `semantic.layer.01` `#f4f4f4` | **3.02:1** | 3:1 | +0.02 |
| **F-09** | info | `semantic.support.success` `{green.50}` `#24a148` → `semantic.layer.01` `#f4f4f4` | **3.05:1** | 3:1 | +0.05 |

These **pass**. They are recorded because the margin is inside the width of a rounding
error, so any future nudge to either the token or the layer value flips them without
anyone noticing. `border.strong-01` in particular is the token that currently rescues
F-05, and it rescues it by 0.02.

### Escalated skip

**F-10 — `semantic.text.placeholder` cannot be evaluated, and one of its two readings is
a hard failure.** The token's DTCG `$value` is `{gray.100}` (`#161616`, opaque), but it
carries `$extensions."org.carbon".alphaModifier: 0.4`. Two defensible readings:

- opaque `#161616` on `#ffffff` → **18.10:1**, passes 4.5:1 comfortably;
- composited at 40% over `#ffffff` → effective `#a2a2a2` → **2.56:1**, fails 4.5:1 badly.

Nothing in the token layer determines which a consumer applies, so this is recorded as
**skipped, not passed** (it is one of the 21 alpha-modified aliases in bucket S3 below).
It is escalated here because the downside reading is placeholder text at 2.56:1, and
`rules.md` separately notes that placeholder is not a label. This is the single highest-value
item for a human to resolve, and resolving it is `token-keeper`'s call on how
`alphaModifier` is meant to be consumed — not a contrast question at all.

### Structural findings

**F-11 — severity: error (brand, not WCAG). `semantic.background` is `#ffffff`.**
`brand.md` §3 states the ground is warm bone `#eeece6` — "the single most recognisable
thing about the identity at a glance" — and §6 names the drift explicitly: *"A drift to
`#ffffff` as the default page is a drift out of the brand."* The token layer resolves the
default page surface to `{white.default}` = `#ffffff`. This is not an accessibility
failure (white is the most forgiving ground there is) but it is load-bearing for this
audit, because **every light-theme ratio in §4 is measured against a ground the brand
does not sanction.** If the ground moves to `#eeece6` the entire light column must be
recomputed; the numbers here would all shift down slightly, and the thin-margin passes
F-08 and F-09 would be the first to break. Recorded so no one reads a PASS in this
document as durable across that change.

**F-12 — severity: info. There is no coral token, so `brand.md` §3's binding rule is
upheld vacuously, and its required counterpart does not exist.** Enumerating all 250
palette entries: `ai` (6), `black` (2), `blue`, `coolGray`, `cyan`, `gray`, `green`,
`magenta`, `orange`, `purple`, `red`, `teal`, `warmGray`, `yellow` (20 each), `white` (2)
— total 250. Brand coral `#f15b40` is **not** among them, and neither is the text-safe
accent `#b03822`, the bone `#eeece6`, or the navy `#041222`. Consequences, stated
plainly:

- The §3 rule — *"the brand coral never carries body text, small labels, captions,
  legends, table values, form hints, or any text below large-text size — on any ground"* —
  **is not violated anywhere in the semantic colour layer, because no token resolves to
  coral.** That is a pass, but it is a pass by absence, not by design, and it should be
  read as "the rule has nothing to bind to yet" rather than "the rule is enforced."
- `brand.md` §3 consequence 1 requires that where coral appears as text, a *separate,
  darker text-coral* exists as its own role. No such token exists. **OQ-6 ("Text-coral
  value — `token-keeper`'s to measure and choose") is therefore still open**, confirmed
  by enumeration rather than assumed.
- No token in the layer can currently be used contrary to the coral rule. The first
  coral token added is the moment this audit needs re-running.

**F-13 — severity: info. The semantic layer is Carbon's `white.json` and `g100.json`
carried through verbatim; it encodes no CoForge colour decision.** Every one of the 468
aliases resolves into Carbon's palette, and the `$extensions.coforge` block on each
carries only a `theme` marker. The four brand decisions in `brand.md` §3 — warm bone
ground, deep navy ink, one hot coral accent, and the two-coral-roles rule — have **no
representation in the colour layer at all**. This corroborates the declared
design-system state **RED** (CLAUDE.md, ADR-011) at the colour axis specifically: 786
tokens exist, and none of the colour ones are ours yet. It also explains why this audit
reads like a Carbon audit — because at the colour layer, it is one.

---

## 3. What was skipped — 432 of 468 aliases

**Skipped is not passed.** These aliases were not evaluated. No claim is made about
their contrast in either direction.

Of the 468 semantic colour aliases, 36 appear on one side of a computed pair
(26 in `semantic.*`, 10 in `semantic-dark.*`). The remaining **432** are skipped, in four
buckets:

| Bucket | Count | Reason |
|---|---|---|
| **S1** — `syntax.*` (88 light + 88 dark) | **176** | Code-editor foreground set. There is no `semantic.syntax.background` token, so these foregrounds have **no defined ground** in the token layer to be measured against. `typography.scale.code` names the face, not a surface. Unevaluable, not passing. |
| **S2** — `ai.*` and `chat.*` (42 light + 42 dark) | **84** | Outside the declared L1 scope: no `cf-*` primitive's `tokens_used` names them, and the L2 entries that would use them declare only the wildcard `semantic.*`. Several also carry `alphaModifier`. **Note for the next run:** `chat.*` is the highest-value extension of this scope, because unlike everything else here it declares explicit foreground/background pairs by name (`bubble-agent-text` on `bubble-agent`, `header-text` on `header-background`, `prompt-text` on `prompt-background`). Those are genuinely checkable and were skipped for scope, not for ambiguity. |
| **S3** — alpha-modified aliases (9 light + 12 dark) | **21** | Carries `$extensions."org.carbon".alphaModifier`, while the DTCG `$value` resolves to an opaque hex. The token has two defensible readings and the composite depends on a ground the token does not name. Includes `text.placeholder`, `text.disabled`, `icon.disabled`, `overlay`, `shadow`, `background-{hover,active,selected,selected-hover}` and their dark counterparts. See F-10. |
| **S4** — state and layer variants (69 light + 82 dark) | **151** | Hover / active / selected / disabled / `-02` / `-03` / `-inverse` variants whose "ground" is a *state* of a surface rather than a surface, and which no L1 primitive pins to a specific pairing. Several are value-identical to a token that **was** computed — `border.tile-01`, `border.subtle-selected-01` and `border.disabled` all resolve to `{gray.30}`, the same value as `border.subtle-01` at 1.71:1 — and a reader may reasonably expect the same ratio. **That expectation is an inference, not a measurement, and this audit does not report inferred ratios as checked.** |
| | **432** | |

Arithmetic: 176 + 84 + 21 + 151 = 432; 432 + 36 = 468. The light-theme count of 234 was
verified by enumerating every leaf in `semantic.*` (8 top-level scalars + 29 `layer` + 6
`field` + 16 `border` + 9 `text` + 8 `link` + 7 `icon` + 11 `support` + 8 scalars + 2
`skeleton` + 88 `syntax` + 21 `ai` + 21 `chat` = 234). `semantic-dark.*` mirrors the same
group structure.

**Also out of scope, stated so it is not mistaken for coverage:** target size (24×24 CSS
px), focus order, programmatic labels, `prefers-reduced-motion`, and heading structure —
all five are checks in `rules.md` that a **token file cannot answer**. They are properties
of a rendered screen. They were not run here and must be run against a `ui-screen`
artifact before the Phase 4 a11y filter can be called complete for any screen.

---

## 4. Measurements

Every row states the resolved hex on both sides and the ground it was measured against.

### Set 1 — light text foregrounds (threshold 4.5:1)

| Foreground token | Resolves to | vs `background` `#ffffff` | vs `layer.01` `#f4f4f4` |
|---|---|---|---|
| `semantic.text.primary` | `{gray.100}` `#161616` | **18.10:1** PASS | **16.45:1** PASS |
| `semantic.text.secondary` | `{gray.70}` `#525252` | **7.81:1** PASS | **7.10:1** PASS |
| `semantic.text.helper` | `{gray.60}` `#6f6f6f` | **5.02:1** PASS | **4.57:1** PASS |
| `semantic.text.error` | `{red.60}` `#da1e28` | **5.00:1** PASS | **4.55:1** PASS |
| `semantic.link.primary` | `{blue.60}` `#0f62fe` | **5.00:1** PASS | **4.55:1** PASS |
| `semantic.link.secondary` | `{blue.70}` `#0043ce` | **7.79:1** PASS | **7.09:1** PASS |
| `semantic.link.visited` | `{purple.60}` `#8a3ffc` | **5.00:1** PASS | **4.55:1** PASS |

14 pairs, 0 failures. Note the cluster at 4.55:1 on `layer.01`: Carbon's `60` steps are
tuned to clear 4.5:1 on pure white by roughly 0.5, which leaves ~0.05 of margin once the
ground drops to `#f4f4f4`. They pass. They pass narrowly, and F-11 is the reason that
matters.

### Set 2 — dark text foregrounds (threshold 4.5:1)

| Foreground token | Resolves to | vs `background` `#161616` | vs `layer.01` `#262626` |
|---|---|---|---|
| `semantic-dark.text.primary` | `{gray.10}` `#f4f4f4` | **16.45:1** PASS | **13.76:1** PASS |
| `semantic-dark.text.secondary` | `{gray.30}` `#c6c6c6` | **10.59:1** PASS | **8.86:1** PASS |
| `semantic-dark.text.helper` | `{gray.40}` `#a8a8a8` | **7.61:1** PASS | **6.36:1** PASS |
| `semantic-dark.text.error` | `{red.40}` `#ff8389` | **7.63:1** PASS | **6.38:1** PASS |
| `semantic-dark.link.primary` | `{blue.40}` `#78a9ff` | **7.68:1** PASS | **6.43:1** PASS |
| `semantic-dark.link.secondary` | `{blue.30}` `#a6c8ff` | **10.62:1** PASS | **8.88:1** PASS |
| `semantic-dark.link.visited` | `{purple.40}` `#be95ff` | **7.70:1** PASS | **6.44:1** PASS |

14 pairs, 0 failures. The dark theme has materially more headroom than the light theme —
its tightest text pair is 6.36:1 against light's 4.55:1.

### Set 3 — text on inverse and brand grounds (threshold 4.5:1)

| Pair | Resolves to | Computed | Verdict |
|---|---|---|---|
| `semantic.text.inverse` → `semantic.background-inverse` | `#ffffff` on `{gray.80}` `#393939` | **11.55:1** | PASS |
| `semantic.text.on-color` → `semantic.background-brand` | `#ffffff` on `{blue.60}` `#0f62fe` | **5.00:1** | PASS |
| `semantic.link.inverse` → `semantic.background-inverse` | `{blue.40}` `#78a9ff` on `#393939` | **4.90:1** | PASS |

3 pairs, 0 failures.

### Set 4 — `support.*` as non-text / status fill (threshold 3:1)

Judged at the non-text threshold. See the ambiguity note below the table.

| Token | Resolves to | vs `#ffffff` | vs `#f4f4f4` |
|---|---|---|---|
| `semantic.support.error` | `{red.60}` `#da1e28` | **5.00:1** PASS | **4.55:1** PASS |
| `semantic.support.success` | `{green.50}` `#24a148` | **3.35:1** PASS | **3.05:1** PASS (F-09) |
| `semantic.support.warning` | `{yellow.30}` `#f1c21b` | **1.68:1** FAIL | **1.53:1** FAIL (F-01) |
| `semantic.support.info` | `{blue.70}` `#0043ce` | **7.79:1** PASS | **7.09:1** PASS |
| `semantic.support.caution-minor` | `{yellow.30}` `#f1c21b` | **1.68:1** FAIL | **1.53:1** FAIL (F-02) |
| `semantic.support.caution-major` | `{orange.40}` `#ff832b` | **2.46:1** FAIL | **2.24:1** FAIL (F-03) |

12 pairs, 6 failures.

**Ambiguity, recorded rather than resolved.** `cf-badge` declares only these four
`support.*` tokens in `tokens_used`. It declares **no paired text colour and no paired
fill colour**, so whether `support.warning` is the badge's *fill* (with some unnamed label
colour on top) or the badge's *label* (on some unnamed fill) is undetermined by the
system. The non-text reading above is the one that holds either way — a status colour must
at minimum be distinguishable from the surface it sits on. **The text reading — these
colours used as a small label at 4.5:1 — was not computed and is not claimed.** If
`support.warning` is ever a label colour, it is at 1.68:1 and the failure is far worse
than what is recorded above. That is a component-contract gap for `token-keeper` and the
index, not something this audit can settle.

### Set 5 — borders and focus as non-text (threshold 3:1)

| Pair | Resolves to | Computed | Verdict |
|---|---|---|---|
| `semantic.border.subtle-00` → `background` | `{gray.20}` `#e0e0e0` on `#ffffff` | **1.32:1** | FAIL (F-04) |
| `semantic.border.subtle-01` → `background` | `{gray.30}` `#c6c6c6` on `#ffffff` | **1.71:1** | FAIL (F-05) |
| `semantic.border.subtle-01` → `layer.01` | `#c6c6c6` on `#f4f4f4` | **1.55:1** | FAIL (F-05) |
| `semantic.border.strong-01` → `background` | `{gray.50}` `#8d8d8d` on `#ffffff` | **3.32:1** | PASS |
| `semantic.border.strong-01` → `layer.01` | `#8d8d8d` on `#f4f4f4` | **3.02:1** | PASS (F-08) |
| `semantic.border.tile-02` → `background` | `{gray.40}` `#a8a8a8` on `#ffffff` | **2.38:1** | FAIL (F-06) |
| `semantic.border.interactive` → `background` | `{blue.60}` `#0f62fe` on `#ffffff` | **5.00:1** | PASS |
| `semantic.focus` → `background` | `{blue.60}` `#0f62fe` on `#ffffff` | **5.00:1** | PASS |
| `semantic.focus` → `layer.01` | `#0f62fe` on `#f4f4f4` | **4.55:1** | PASS |
| `semantic-dark.focus` → `semantic-dark.background` | `{white.default}` `#ffffff` on `{gray.100}` `#161616` | **18.10:1** | PASS |

10 pairs, 4 failures. **The focus indicator colour passes on every ground tested, in both
themes, with margin.** `rules.md` also requires that focus is *always visible and never
suppressed* and that focus order follows reading order — neither is a token property and
neither was checked here (see §3, out of scope).

### Set 6 — `cf-chart-palette` series marks (threshold 3:1)

Measured against `semantic.background` `#ffffff` only. The `layer.01` ground was **not**
computed for this set; a chart on a `#f4f4f4` card would sit ~0.05 lower on every row and
those numbers are not claimed here.

| Series | Token | Resolves to | vs `#ffffff` | Verdict |
|---|---|---|---|---|
| 1 | `palette.blue.60` | `#0f62fe` | **5.00:1** | PASS |
| 2 | `palette.teal.60` | `#007d79` | **4.99:1** | PASS |
| 3 | `palette.purple.60` | `#8a3ffc` | **5.00:1** | PASS |
| 4 | `palette.magenta.60` | `#d02670` | **5.01:1** | PASS |
| 5 | `palette.cyan.40` | `#33b1ff` | **2.37:1** | FAIL (F-07) |

5 pairs, 1 failure.

---

## 5. Claims

Per `brand.md` §1, every claim carries its ground.

- **Evidenced [ART-008 § 4. Measurements]** — every ratio in this document. These are
  measurements of token values, not testimony; per ADR-017 they take the artifact form,
  never a ledger ID. No `[E-nnn]` appears in this artifact and none was minted:
  `research/evidence-ledger.json` is empty, no user was asked about any of this, and a
  contrast ratio is not something a person said.
- **Evidenced** (by direct enumeration of `design-system/tokens/tokens.json`) — the palette
  contains exactly 250 entries across 15 groups and includes no coral, bone, navy or
  text-coral value (F-12); `semantic.*` contains exactly 234 leaves (§3); the light theme
  resolves to exactly two distinct surface values (§1).
- **Evidenced** (by direct reading of `design-system/foundations/brand.md`) — the §3 coral
  rule, the §3 bone ground, the §6 "drift to `#ffffff`" line, and OQ-6. Quoted from that
  file, which is itself Gate A-approved. This audit does **not** re-cite `ART-005`; it did
  not read ART-005, and citing an artifact one has not opened is exactly the failure the
  claim format exists to prevent.
- **Inferred** — that `border.subtle-01`'s failure does or does not engage WCAG 1.4.11
  (F-05). *Inferred from* the text of 1.4.11, which scopes to information required to
  identify components and states. Not decidable from a token; needs a screen.
- **Inferred** — that the four value-identical border tokens in bucket S4 would return the
  same ratio as `border.subtle-01`. Not measured, therefore not counted as checked.

## 6. Assumptions

Visible and arguable. None is settled by appearing here.

- **A-1.** Assumed the two light grounds (`#ffffff`, `#f4f4f4`) are the surfaces text
  actually lands on, because `cf-colour-roles` and `cf-table` name `semantic.layer.*` and
  `semantic.background` and nothing else. If L1 output composites text over
  `layer.accent-*`, `field.*` or a `-hover` state, those pairs are unmeasured (bucket S4).
- **A-2.** Assumed `alphaModifier` is **not** applied when resolving a token to a value,
  which is why the 21 alpha-modified aliases are skipped rather than composited. If
  `token-keeper` confirms it *is* applied, F-10 becomes a hard failure and bucket S3 needs
  a full re-run, not a re-read.
- **A-3.** Assumed `semantic-dark.*` contains 234 leaves mirroring `semantic.*`. The light
  count was enumerated leaf by leaf; the dark count was read as structurally mirroring it
  and was **not** independently enumerated. If the dark theme has a different leaf count,
  the skipped total of 432 moves by that difference.
- **A-4.** Assumed sRGB throughout. Every `$value` declares `"colorSpace": "srgb"`, so this
  is well supported, but no display profile was considered and none is encoded.
- **A-5.** Assumed the ground stays `#ffffff`. It should not, per F-11. Every light-theme
  number in §4 expires the day the bone ground lands.

## 7. What this audit does not say

- It does not say the colour layer is accessible. It says 58 named pairs were computed,
  11 fell below threshold, and 432 aliases were not examined.
- It does not clear any screen. Target size, focus order and visibility, labels, motion
  and heading structure are all in `rules.md` and none of them can be checked against a
  token file.
- It does not propose token values. Where a value fails, the finding is the record;
  choosing a replacement is `token-keeper`'s, and choosing whether the brand tolerates it
  is `brand-director`'s.
- It is not the verdict. Gate A is.

---

**For Gate A.** Three things are worth a person's attention before anything else:
**F-01/F-02** (a status colour reachable by two token names at 1.68:1),
**F-10** (`text.placeholder` is either 18.10:1 or 2.56:1 and the token layer does not say
which), and **F-11/F-13** (every light-theme number above is measured against `#ffffff`,
a ground `brand.md` §6 explicitly rules out — so these passes are provisional on a
decision that has not been made yet).
