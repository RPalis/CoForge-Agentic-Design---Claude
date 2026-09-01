# Token layer audit — independent, 2026-09-01

**Auditor:** token-keeper (owns `design-system/tokens/tokens.json` per the routing table)
**Scope:** true state of the token layer; correctness and completeness of the proposed alpha repair
**Status:** advisory. Nothing was modified. The repair still awaits Gate A.

**Standing instruction for this audit:** the main session's self-assessment has been wrong
twice in the same direction — declaring token state correct when it was not. So nothing
here rests on a claim being written down. Every number below was re-derived from the files,
and where I could not derive it I say so rather than passing it.

---

## Method

Everything numeric was recomputed by walking `tokens.json` directly. The proposed repair was
**executed in a scratch copy** and the four validators were run against the result, so the
claims about what the repair does are observed rather than predicted. The scratch copy lives
outside the repository and no token file was touched.

| | |
|---|---|
| Verified by re-derivation | 53 / 6 / 35 counts · alias resolution of all 53 · every `$extensions` key in the file · rem→px conversion on all 29 dimension tokens · contrast before/after for all 53 · what the repair does to `audit-contracts.py` · which primitives the repair orphans · component-index consumption of the 53 |
| Verified against git | "present since `9f4f07b`, the first token commit" — `git show 9f4f07b:...` returns 53 `alphaModifier` occurrences |
| Verified as quoted | the 2026-08-28 self-clearing quote is accurate, at `2026-08-28__token-axes-proposal.md:130-132` |
| Taken on trust | that Carbon upstream has exactly 53 rgba roles (see "Could not verify") |
| Could not verify | Figma's handling of `alpha` in a DTCG colour object; Figma gradient interpolation; upstream Carbon completeness |

---

## Answer in one line

**53 / 6 / 35 all hold exactly.** The repair's *architecture* is sound and is the only shape
DTCG permits. **The repair as literally written reintroduces the defect it fixes**, and it
lands the restored value in the one place no downstream check inspects. There is a sibling
inert extension in the file today, and the new check cannot see it.

---

## Findings

### BLOCKER

**B-1 — The 53 inert alpha modifiers are real, and the counts are exact.**

Re-derived independently:

| Claim | Re-derived | Verdict |
|---|---|---|
| tokens carrying `org.carbon.alphaModifier` | **53** | correct |
| of which declare alpha `0` | **6** | correct |
| distinct (base, alpha) pairs | **35** | correct |
| share of the 472-leaf semantic layer | 53/472 = **11.23%** | correct |
| alpha applied to any resolved `$value` | **0 of 53** | correct |

Supporting facts the proposal does not state, all of which strengthen it:

- All 53 are `$type: color`. All 53 are pure single-hop aliases — no literals, no chains
  deeper than one, so there is no hidden case.
- **No token anywhere in the file currently carries `alpha` in its `$value`, and no token
  carries an 8-digit hex.** The alpha-bearing colour form is entirely new to this file.
- The 6 at alpha 0 are `semantic{,-dark}.ai.aura-end`, `…ai.aura-hover-end`,
  `…chat.prompt-border-end` — three roles × two themes.
- Only **one** of the 53 says anything about transparency in its `$description`
  (`semantic-dark.ai.aura-end`). The prose layer would not have caught this either.
- 24 light / 29 dark.

*Fix:* proceed with the repair, subject to B-2 and E-1 below.

---

**B-2 — The proposal's own JSON example reintroduces the exact defect it repairs.**

This is the most serious finding in this audit.

§4 of the proposal specifies the new primitives as:

```json
{ "$type": "color",
  "$value": { "colorSpace": "srgb", "components": [0, 0, 0], "alpha": 0.3, "hex": "#000000" } }
```

`"alpha": 0.3` and `"hex": "#000000"` contradict each other. A six-digit hex *is* opaque.
Any consumer that reads `hex` — and DTCG positions `hex` precisely as the fallback a simple
consumer reads — gets full opacity back. That is the same shape as the original defect: a
record that carries the value, sitting beside a field consumers actually read that carries a
different one.

This is not hypothetical. Two consumers in this repository read `hex` and ignore `alpha`:

- `validation/apply-brand-colour-layer.py:255` — `return node["$value"]["hex"]`
- `validation/audit-contracts.py:72` — `if "hex" in value: return ("color", value["hex"].lower())`,
  commented *"DTCG colour — compare on hex only"*

I built the repair both ways in a scratch copy and ran `audit-contracts.py --strict`:

| Form of the new primitives | Result |
|---|---|
| 8-digit hex (`#0000004d`) | `blocker 0 · error 0 · warning 0` — **PASS** |
| 6-digit hex, exactly as §4 writes it | `error 12` — **FAIL** |

The 6-digit form fails because `canonical()` collapses colour to hex, so all 35 new
primitives read as duplicates of their bases:

```
[ERROR] redundancy: #000000 reachable by 10 names: palette.black.default,
        palette.black.default-a00, …-a04, …-a08, …-a12, …-a28, …-a30, …-a50, …-a60, …-a80
[ERROR] redundancy: #8d8d8d reachable by 8 names: palette.gray.50, …-a12 … -a50
        (+10 more)
```

*Fix:* the new primitives must carry an **8-digit hex including the alpha byte**, or omit
`hex` entirely. Add to the Gate A decision list — this is not a formatting preference, it
decides whether the repair works. Recommend 8-digit over omission: omitting `hex` would make
`canonical()` fall through to the `("obj", …)` branch, which happens to work but only by
accident of the alpha field differing.

---

### ERROR

**E-1 — The repair moves the load-bearing value into the one class of value no check compares.**

After the repair, the entire restored meaning of all 53 tokens lives in the `alpha` field of
35 colour literals. `validation/check-figma-live.py` — the only thing that compares Figma
against the source — never compares a colour value:

```python
def num(v):
    if isinstance(v, dict) and "value" in v: return round(float(v["value"]), 4)
    if isinstance(v, (int, float)):          return round(float(v), 4)
    return None                              # <- every DTCG colour object lands here
...
    a, b = num(ours.get("$value")), num(theirs.get("value"))
    if a is not None and b is not None and abs(a - b) > 1e-4:   # <- guarded out
```

Measured against the current generated file: 762 tokens, 474 aliases (compared by target
name), 288 literals — of which **256 are never value-compared** (254 colours, 2 fontFamily).

So the drift check would report `762 of 762 matched, 0 findings` with every alpha in Figma
silently wrong. That is the C-018 failure verbatim: a fix living somewhere nothing can see it.

*Fix:* teach `check-figma-live.py` to compare colours, including alpha, before the repair is
declared closed. This is system-keeper's file — name it in the handoff, do not edit it here.
Until then the repair is unverified downstream and must not be reported as complete.

---

**E-2 — The sibling inert extension exists, and the new check is structurally unable to see it.**

The brief assumed a sibling. There is one.

`$extensions.coforge.fontVariantNumeric = "tabular-nums"` sits on all 8 `typography.scale.*`
tokens. Its own reason field says:

> "Binding per brand.md §4: tabular figures are not a per-screen choice — anything consuming
> this scale level **MUST** apply `font-variant-numeric: tabular-nums`; proportional figures
> are the exception a designer must ask for."

A recorded, binding, load-bearing instruction. Its enforcement, re-derived:

| Path | Does it apply the value? |
|---|---|
| DTCG `typography` composite `$value` | No — no such field exists in the type |
| Figma text style materialisation | No. The token's own `figma_exclusion_reason` lists the fields the text style binds: "family, size, weight and tracking". `fontVariantNumeric` is not among them and is dropped without notice |
| `build-figma-tokens.py` | No — strips `$extensions` wholesale (line: `if key == "$extensions": continue`) |
| Any script in the repo | No. Repo-wide grep finds two hits, both inside `build-token-axes.py`, i.e. the code that *writes* it. Nothing reads it |
| `dashboard/render.py:91` | Hardcodes `font-variant-numeric:tabular-nums` in a CSS rule. Not derived from the token — coincidence, not consumption |
| **`check-value-modifiers.py`** | **No — the key does not end in `"Modifier"`** |

That last row is the important one. The new checker's docstring claims generality —
*"stated generally because the class is broader than alpha"* — but the generality is a
**naming convention**:

```python
for key, declared in body.items():
    if not key.endswith("Modifier"):
        continue
```

A modifier that is not spelled `*Modifier` is invisible. The check currently reports
`53 modifiers verified · 0 declared inert` and says nothing about the eight tokens carrying a
MUST that nothing enforces. The defect class has been closed for keys that happen to be named
after it.

This differs from the alpha case in one way worth stating precisely: `$value` here is not
*wrong*, it is *incomplete*. DTCG genuinely cannot express `font-variant-numeric` in a
`typography` composite. So the honest outcome is an explicit inert declaration, not a repair.

*Fix (system-keeper's file, named not edited):* widen the trigger from a name suffix to the
extension's *shape* — any extension key whose value is a scalar the token's `$value` does not
carry — and require `coforge.modifier_inert` with a reason on `fontVariantNumeric`. The reason
already exists in prose; it needs to be in the field the check reads. Note the check already
has the `modifier_inert` machinery — it is simply never reached for this key.

---

**E-3 — Applying the alpha CREATES a WCAG failure that does not exist today: placeholder text.**

Computed with WCAG 2.x relative luminance, blending each token over its actual surface.

| Token | Surface | Contrast now | After repair | Exempt? |
|---|---|---|---|---|
| `semantic.text.placeholder` | `semantic.field.01` | 16.45:1 | **2.52:1** | **No** |
| `semantic-dark.text.placeholder` | `semantic-dark.field.01` | 13.76:1 | **3.45:1** | **No** |
| `semantic.text.disabled` | `semantic.field.01` | 16.45:1 | 1.72:1 | Yes (1.4.3 inactive-control exemption) |
| `semantic.icon.disabled` | `semantic.background` | 15.32:1 | 1.71:1 | Yes |
| `semantic-dark.text.disabled` | `semantic-dark.field.01` | 13.76:1 | 2.18:1 | Yes |
| `semantic-dark.text.on-color-disabled` | `semantic-dark.background-brand` | 5.00:1 | 1.51:1 | Yes |
| `semantic-dark.icon.on-color-disabled` | `semantic-dark.background-brand` | 5.00:1 | 1.51:1 | Yes |
| `semantic-dark.border.disabled` | `semantic-dark.background` | 5.45:1 | 2.30:1 | Yes |

**Placeholder text is the one that needs a human.** WCAG 1.4.3 exempts text that is part of an
*inactive* user-interface component; a placeholder sits in an *enabled* field and is not
exempt. Both themes drop below 4.5:1 — light to 2.52:1, dark to 3.45:1 (which also fails the
3:1 large-text threshold in the light theme and only clears it in dark).

The framing matters and the proposal does not make it: the repair does not *invent* this
failure, it *reveals* one Carbon has always shipped. Today's 16.45:1 is an artefact of the
defect. But the ART-008 finding for these two tokens flips from pass to fail, and that is a
Gate A judgement, not a token-keeper one.

Largest visual changes, for the visual diff: `semantic.overlay` (opaque black scrim → 5.46:1
relative to ground — the modal becomes usable), `semantic.shadow` 17.78:1 → 2.08:1, the six
alpha-0 gradient ends (hard edge → true fade), and every `background-hover`/`selected`/`active`
state, which currently render as flat grey plates and become tints.

*Fix:* commission ART-008 v2 as the proposal recommends, and flag `text.placeholder` in both
themes as a decision, not a finding. If the answer is "Carbon's value is unacceptable", that
is a **brand-director** call at Gate A (suggest-only), not a token-keeper repair — same
boundary the proposal correctly draws for the navy-tinted shadow.

---

### WARNING

**W-1 — "All 35 import as variables" is asserted, not evidenced.**

The proposal states: *"Figma-representable: a `COLOR` variable holds alpha, so all 35 import
as variables."* The first clause is true. The second does not follow — it depends on whether
the **importer** reads `alpha` out of the DTCG colour object, and that has never been tested
here. `figma-representability.json` is explicit that its provenance is empirical *for types*
("a real import of all 794 tokens … then reading back every created variable's resolvedType
and value"). No token in the file has ever carried alpha, so nothing about alpha was in that
experiment.

`build-figma-tokens.py` passes colour `$value` through untouched, so whatever the importer
does with `alpha` is what happens. Given C-017 and C-020 — silent degradation into a
representable-but-meaningless value, and a tool's self-report being wrong three times in one
session — this cannot be assumed.

*Fix:* import + read-back verification of at least one alpha primitive per distinct alpha
before the repair is signed off. Skipped is not passed; if it is not run, say it was not run.

---

**W-2 — `coforge.theme` is written by one script, read by none, and is 46 tokens incomplete.**

426 tokens carry `$extensions.coforge.theme`. Re-derived: it is written at
`apply-brand-colour-layer.py:134` and **repo-wide grep finds no reader**. Of the 472
semantic leaves, **46 lack it — all of them in `semantic-dark`**, including
`semantic-dark.text.on-color-disabled`, `semantic-dark.icon.on-color-disabled`, all 17
`semantic-dark.syntax.*`, and 6 `semantic-dark.chat.*`. Where present it is always correct
(0 disagreements with the group name).

Not a value modifier, so not the alpha class, and harmless today. It becomes harmful the
moment anyone builds a Figma mode split or a theme filter from it, because it will silently
under-report the dark theme by 46 tokens while looking like 426 tokens of coverage. Same
shape, lower severity: a record that reads as coverage.

*Fix:* either complete it to 472 or delete it. A 90%-complete unread index is the worse of
the three options.

---

**W-3 — Naming: `-a30` inside a Carbon-mirrored group is the weakest of the options.**

Assessed against ADR-018 and against the Figma picker, as asked. Recommendation only.

ADR-018 is about components, but its operative principle transfers directly: *vendor names
byte-identical, CoForge-authored names marked, so one layer is stable and one replaceable.*
`palette.black.default-a30` violates that principle at the token layer. Carbon does not ship
`black.default-a30`. Placed inside `palette.black`, a CoForge-authored primitive becomes
indistinguishable by name from a mirrored one, and a future Carbon merge sees an unknown
sibling in a group it believes it owns. The Carbon mirror stops being comparable to upstream.

| Option | ADR-018 fit | Figma picker |
|---|---|---|
| `palette.black.default-a30` (proposed) | Weak — CoForge authorship invisible inside a mirrored group | `palette/black/default-a30` sorts directly under `default`; a designer sees a clean ladder. Real advantage |
| `palette.alpha.black-default-30` or similar separate group | Strong — mirror stays byte-comparable, derived layer isolated, all 35 in one place | One folder of 35, away from the base ramp. Arguably cleaner; loses the adjacency |
| `palette.black.default/30%` (proposal's alternative) | — | **Likely invalid.** `/` is Figma's variable-group separator. This makes `default` simultaneously a variable and a group in one collection. Verify before considering; I could not test it |
| `palette.black.default.a30` | — | **Reject outright.** Gives a token children — the exact C-002 descent shape, and `default` already has a `$value` |

Two mechanical facts that constrain the choice, both re-derived: the 19 distinct alphas are
`0, .04, .06, .08, .10, .12, .16, .20, .24, .25, .28, .30, .32, .36, .40, .50, .60, .64, .80`
— **every one is an integer when multiplied by 100**, so a two-digit zero-padded suffix is
sufficient and lossless, with no three-digit case and no collisions. And the `-a` prefix is
right for the reason the proposal gives: a bare `-30` reads as a palette step.

*Recommendation:* keep the `a<NN>` token, move the group. Decide at Gate A.

---

**W-4 — The alias dialect is not DTCG-resolvable, which is an interoperability risk under ADR-018's own logic.**

Re-derived: 526 alias occurrences, 99 distinct targets, and **zero use a `palette.` prefix**.
`{gray.10}` means `palette.gray.10` by a bare-name convention held in four separate scripts
(`build-token-axes.py`, `check-value-modifiers.py`, `check-figma-live.py`,
`flatten-dark-tokens.py`, each with its own `ALIAS_ROOTS` tuple). DTCG resolves references
from the document root, where no `gray` group exists. Meanwhile `{typography.family.sans}`
*is* fully qualified — so the file contains two conventions.

Every in-repo consumer handles it. A third-party DTCG tool would not, and after ADR-001
inversion Figma becomes the author of these names. The 35 new primitives are the moment to
decide, because they are new names and can be minted either way.

*Fix:* out of scope for the repair, but name it as an open question. Note that the convention
is documented, which is why this is a warning and not an error.

---

### INFO

**I-1 — rem→px is correct and complete; shadow geometry is not double-converted. Verified.**

Re-derived independently of `--check`:

- 29 dimension tokens: 27 rem literals + 2 aliases (`density.*.spacing-unit`).
- All 27 convert at exactly 16×. **0 mismatches.** The 2 aliases pass through unchanged,
  which is right — their targets are converted.
- Both independent corroborators land exactly: `typography.size.07` → **62px**,
  `typography.tracking.07` → **-2px** [ART-005 § Type; brand.md §4].
- Negative tracking and sub-pixel values survive: `-0.06rem` → `-0.96px`, `0.005rem` → `0.08px`.
  No float noise.
- **Shadow geometry is not double-converted, and cannot be.** All 4 `$type: shadow` tokens are
  dropped as non-representable *before* any conversion runs, so `elevation.shadow.raised`'s
  0/2/6/0 px never reaches `convert_dimension()`. The px guard in that function is a second
  belt behind a brace.
- 762 kept + 32 dropped = 794. The 32 dropped exactly equal the 32 declaring
  `figma_representable: false` — set equality, not just count equality.

C-018 is genuinely closed for the axes it covers.

**I-2 — The repair orphans two primitives.** `palette.black.default` and `palette.blue.100`
lose their last remaining alias, because every semantic token that referenced them did so only
with an alpha. Orphan count 192 → 194. Falls under the existing "Carbon ships a full ramp"
INFO and is not a problem, but `black.default` going unaliased is a fact worth seeing rather
than discovering later.

**I-3 — 35 is minimal, and the four alpha-0 pairs are not redundant.** The alpha-0 group is
`black.default`, `gray.10`, `gray.90`, `white.default` — four primitives that are all fully
transparent and therefore *look* collapsible into one. Do not collapse them. CSS interpolates
gradients in premultiplied alpha, where the base RGB is irrelevant; whether Figma does the
same I could not verify, and if it does not, a fade to transparent-white and a fade to
transparent-black are visibly different. Keeping the base distinct is correct under both
behaviours and costs three primitives.

**I-4 — Blast radius in code today is one token.** Cross-referenced the 53 against every
`tokens_used` entry in `component-index.json` (216 components, 16 distinct token references
including wildcards): **zero of the 53 are consumed by any indexed component.** The only
consumer anywhere in the token layer is `elevation.shadow.raised`, which aliases
`{semantic.shadow}`. `semantic-dark.shadow` is consumed by nothing at all — there is no dark
elevation geometry, which the token's own description already admits.

This is an argument for doing the repair **now**: it is nearly free before the L2 component
layer starts binding these tokens, and it gets steadily more expensive after.

**I-5 — One asymmetry checked and cleared.** Light `semantic.text.on-color-disabled` and
`semantic.icon.on-color-disabled` carry **no** `alphaModifier`, while their dark counterparts
do. This looks like a transcription miss and is not: the light tokens alias `{gray.50}`, which
is Carbon's white-theme value (opaque), whereas the dark ones alias `{white.default}` at 0.25.
Checked, not assumed.

**I-6 — Provenance claims in the proposal are accurate.** `git show 9f4f07b:design-system/tokens/tokens.json`
returns 53 `alphaModifier` occurrences, confirming "present since the first token commit". The
self-clearing quote in §0 is verbatim from `2026-08-28__token-axes-proposal.md:130-132`. The
proposal's §0 is not overstated.

---

## Verdict on the proposed repair

**Architecturally sound, and it is the only shape DTCG allows.** I checked for a mechanism the
proposal overlooked and there is none. DTCG has no alias-with-modifier, no computed tokens and
no derived values; `color` is not a composite type, so unlike `shadow` or `typography` it
cannot carry per-field aliases. Alpha can only live in a colour literal, and the contract puts
literals only at the primitive layer. "Mint alpha-carrying primitives, repoint the aliases" is
forced, not chosen. The four rejected alternatives in §5 are rejected for the right reasons.

Confirmed by execution, not prediction — the repair built into a scratch copy yields:

```
check-value-modifiers.py   829 scanned · 53 verified · 0 inert · PASS   (was FAIL, 53 blockers)
audit-contracts.py --strict  blocker 0 · error 0 · warning 0 · PASS     (with 8-digit hex)
figma-representable.py     no findings · PASS
build-figma-tokens.py      797 kept · 27 converted · 32 dropped
```

The primitive/alias contract holds: zero literals above the primitive layer, `find_literal_leaks`
stays green without being weakened, and the semantic tokens remain pure aliases.

**Three conditions before it can be called done:**

1. 8-digit hex on the 35 new primitives (B-2). Without this it fails `audit-contracts --strict`
   *and* re-creates the defect for any hex-reading consumer.
2. Colour comparison in `check-figma-live.py` (E-1), or an explicit written statement that the
   Figma side of this repair is unverified.
3. A real import and read-back proving Figma honours `alpha` (W-1).

Plus one Gate A judgement that is not token-keeper's: **`text.placeholder` in both themes**
(E-3).

## Could not verify

- **Whether Figma's DTCG importer reads `alpha` from the colour object.** No Figma access in
  this audit. Untested, and W-1 is the reason it must not be assumed.
- **Whether Figma interpolates gradients in premultiplied alpha.** Affects only whether the
  four alpha-0 primitives could be collapsed. Recommendation is unchanged either way.
- **Whether 53 is the complete set of Carbon rgba roles.** There is no vendored
  `@carbon/themes` in the repository — `scratch/carbon-cache/` holds `@carbon/react` Code
  Connect `.tsx` files only. I verified internal consistency and cleared one apparent
  asymmetry (I-5), but "Carbon has exactly 53" is taken on trust from the transcription. If
  Carbon ships a 54th rgba role, nothing in this repository would currently notice.
- **Whether `palette.black.default/30%` is a legal Figma variable name.** Assessed as likely
  invalid on the group-separator argument; not tested.

## Handoffs

- **Gate A (human):** approve the repair with the 8-digit-hex correction · choose the naming
  group (W-3) · commission ART-008 v2 · rule on `text.placeholder` (E-3).
- **system-keeper:** `check-figma-live.py` colour comparison (E-1) · widen
  `check-value-modifiers.py` beyond the `*Modifier` suffix (E-2). Named here, not edited —
  those files are not token-keeper's.
- **brand-director (suggest-only, Gate A):** the navy-tinted shadow question the proposal
  raises, and — only if Carbon's placeholder value is judged unacceptable — the placeholder
  opacity. Neither blocks the repair.
