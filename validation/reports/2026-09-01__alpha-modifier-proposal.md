# Proposal — apply the 53 inert alpha modifiers

**Status:** proposal, awaiting Gate A
**Owner (routing table):** token-keeper — *"any · token sync / drift · owns tokens.json"*
**Autonomy:** suggest-new. token-keeper may sync a drifted value automatically; it may
not mint 35 primitives and repoint 53 semantic tokens without a person.
**Raised by:** C-019, which turned out to be one instance of a systemic defect.

---

## 0. This was seen before, and cleared in error

Recorded first because it is the most important fact about this proposal, and because
leaving it out would make the finding look like diligence when it is the opposite.

`validation/reports/2026-08-28__token-axes-proposal.md`, three days before this
document, inspected exactly these tokens and wrote:

> "The colour component of elevation is already correctly in `tokens.json`
> (`semantic.shadow`, `semantic-dark.shadow`, both **proper** `{black.default}` aliases
> with an `alphaModifier` extension — 0.3 light, 0.8 dark). **That does not need
> re-doing.**"

That assessment was wrong. The alias resolves to opaque black; the alpha sits in an
extension and does nothing. The evidence was on screen, quoted accurately, and
misjudged — the presence of the number was read as the application of the number.

It surfaced now only because materialising a Figma effect style forced the value to
actually resolve, and an invented alpha of 0.3 was overridden by the real one. Without
that accident it would still be sitting green.

Two consequences follow, and they are the reason this section exists:

1. **The 53 tokens have rendered opaque since commit `9f4f07b`,** the first token
   commit. Nothing regressed; the defect is as old as the token layer.
2. **A clean audit was never evidence here.** Every check passed for three days across
   a defect affecting 11.2% of the semantic layer, because no check reads
   `$extensions`. This is the coverage premise working exactly as `coverage.json`
   describes it — *unchecked is not passed* — and it is the second time in one week
   that a human-signed "this is correct" was the weakest link in the chain.

---

## 1. What was found

`elevation.shadow.raised` renders as solid black. The immediate cause looked like a
missing brand decision — no opacity had been chosen. It is not that.

```
semantic.shadow
  $value      "{black.default}"                        <- opaque
  $extensions org.carbon.alphaModifier = 0.3           <- read by nothing
```

The alpha *was* transcribed from Carbon. It went into `$extensions`, where it is inert,
while `$value` stayed a bare alias to the opaque base. Every consumer that reads
`$value` — CSS build, Figma import, contrast checker, screen-producer — gets the base
colour at full opacity.

This is not confined to the shadow:

| | |
|---|---|
| Tokens carrying an unapplied `alphaModifier` | **53** |
| Share of the semantic layer (472 leaves) | **11.2%** |
| Distinct (base, alpha) pairs | **35** |
| Tokens whose intended alpha is **0** | **6** |

The six at alpha `0` are the clearest proof that the value is not decorative. They are
meant to be fully transparent — they are the transparent end of a gradient — and they
currently render fully opaque.

Worst-consequence examples:

| Token | Intended | Renders as | Consequence |
|---|---|---|---|
| `semantic.overlay` | black @ 0.6 | opaque black | a modal scrim blacks out the screen |
| `semantic.text.disabled` | `gray.100` @ 0.25 | full strength | disabled text is indistinguishable from enabled |
| `semantic.icon.disabled` | `gray.100` @ 0.25 | full strength | same, for icons |
| `semantic.ai.aura-end` | alpha 0 | opaque white | gradient has a hard edge instead of fading |
| `semantic.shadow` | black @ 0.3 | opaque black | the original C-019 symptom |

## 2. Diagnosis — transcription defect, not a design gap

This matters because it decides who owns the fix.

A design gap would mean the brand never decided an opacity, and `brand-director` would
have to choose one at Gate A. That is not the situation. Carbon's own values are 0.3
light and 0.8 dark for shadow, and the corresponding numbers for the other 51. They
were carried across correctly and then dropped on the floor by the shape of the record.

So the fix **restores a value that was always specified**. It is repair, not a new
design decision — which places it with token-keeper rather than brand-director, and
means it does not need a brand judgement to proceed.

## 3. Why every existing check passed

Worth stating plainly, because "the system reported healthy while broken" is the
failure this repository exists to remove, and it happened again.

| Check | Why it passed |
|---|---|
| `find_literal_leaks` | these are aliases, not literals — correct by that rule |
| `find_unresolved_aliases` | every alias resolves — to the wrong colour |
| `audit-contracts.py` alias tier direction | semantic → palette is the right direction |
| `figma-representable.py` | `color` is representable — it imported fine, just wrong |
| Gate B | no raw hex, no unindexed component |

Nothing anywhere asks: **does an extension that names a value modifier actually modify
the value?** An extension is free-form by DTCG design, so no schema catches it. The
information was present, correct, and load-bearing on nothing.

## 4. Proposed fix

### Constraint

The two rules that bound the solution, from CLAUDE.md and the token contract:

- no value outside `tokens.json`
- **zero literals above the primitive layer** — the semantic layer must alias

DTCG has no "alias with an alpha modifier". An alias carries its target's value
exactly. So the alpha has to exist *somewhere a primitive can hold it*.

### The change

**Mint 35 alpha-carrying palette primitives**, one per distinct (base, alpha) pair,
then repoint the 53 semantic tokens onto them.

```
palette.black.default-a30   = black.default at alpha 0.30    (new primitive, holds a literal)
semantic.shadow             = "{palette.black.default-a30}"  (still a pure alias)
```

DTCG's 2025 colour object carries `alpha` natively, which is the dialect already in
use here, so this needs no extension and no custom `$type`:

```json
{ "$type": "color",
  "$value": { "colorSpace": "srgb", "components": [0, 0, 0], "alpha": 0.3, "hex": "#0000004D" } }
```

**The `hex` must carry the alpha byte.** This example originally read `"#000000"` beside
`"alpha": 0.3` — six digits, which is opaque, so the two fields contradicted each other
and a proposal about values recorded-but-not-applied contained exactly that defect. It
is not cosmetic: two consumers in this repository read `hex` directly and never look at
`alpha` —

    validation/apply-brand-colour-layer.py:255   return node["$value"]["hex"]
    validation/audit-contracts.py:72             if "hex" in value:   # compare on hex only

— so with six digits all 35 new primitives read as byte-identical duplicates of their
bases and `audit-contracts.py --strict` fails with 12 redundancy errors
(*"#000000 reachable by 10 names"*). Eight digits, or omit `hex` entirely. Found by
token-keeper on audit, not by the author.

Properties this preserves:

- the primitive/alias split holds — literals stay at the primitive layer
- `find_literal_leaks` stays green without being weakened
- Figma-representable: a `COLOR` variable holds alpha, so all 35 import as variables
- the `org.carbon.alphaModifier` extension stays, now as *provenance* rather than as an
  instruction nobody follows — and the new check makes it verify rather than decorate

### Generated, not hand-authored

The 35 primitives and the 53 repointings are mechanical: base colour × alpha. They
should be produced by a script in `validation/`, the way every other axis is, so the
mapping is reproducible and reviewable as a diff rather than typed 88 times.

## 5. Alternatives considered

| Option | Rejected because |
|---|---|
| Inline the alpha at the semantic layer | puts literals above the primitive layer; `find_literal_leaks` would fail, and weakening that check to permit it trades a real guarantee for convenience |
| Teach every consumer to read `alphaModifier` | pushes the same rule into the CSS build, the Figma bridge, the contrast checker and screen-producer independently; four chances to forget, and the Figma importer is third-party and cannot be taught at all |
| Leave it, document the extension | the six alpha-`0` tokens make this untenable — they are visibly wrong, not theoretically wrong |
| Drop the alpha and pick opaque equivalents | discards Carbon's actual values and turns a repair into 53 brand decisions |

## 6. Blast radius

**53 semantic tokens change colour.** This is a visible change, and it is the point —
they are currently wrong. But it should be reviewed as a visual diff, not merged blind.

**ART-008's contrast findings need re-checking.** The a11y audit computed contrast
against the opaque values. For the alpha tokens those ratios are wrong in both
directions: `text.disabled` at 0.25 alpha has *far* lower effective contrast than what
was measured, and disabled text is exactly where a wrong pass is dangerous. Per the
artifact lifecycle this means a **v2**, not an edit — versions are immutable.

**Figma:** 35 new variables and 53 changed aliases, applied through the generated
`coforge.figma.tokens.json` and the normal import path.

## 7. The check that stops it recurring

Repair without a check is two of three. Proposed, owned by **system-keeper**:

> Any `$extensions.*` key that names a value modifier — `alphaModifier` today, and any
> future sibling — must be reflected in the token's resolved `$value`, or the token must
> declare the modifier inert with a reason. Unapplied modifiers are a **blocker**.

Generalised, because the class is broader than alpha: *a record that claims to change a
value and does not is worse than no record, because it reads as coverage.* The same
sentence describes C-017, C-018 and this one.

## 8. Decisions required at Gate A

1. **Approve the repair** — mint 35 primitives, repoint 53 tokens, restoring Carbon's values.
2. **Naming.** Proposed suffix `-a30` (alpha × 100, zero-padded): `black.default-a30`,
   `gray.50-a12`. ADR-018 exists because naming affects interoperability, so this should
   be chosen, not defaulted. The alternative worth weighing is `black.default/30%` or
   `black.default-30`; the `-a` prefix is proposed because a bare `-30` reads as a
   palette step, which is the one thing it must not be confused with.
3. **ART-008 v2** — re-run the contrast audit against the corrected values. Recommended
   yes; the current findings for alpha tokens are not reliable.
4. **Separately, and optional — a brand question for `brand-director`.** Should CoForge's
   shadow be Carbon's neutral black, or tinted with CoForge's navy ink? A navy-tinted
   shadow sits differently on the bone ground than a grey one. This is genuinely a
   brand call, it is *suggest-only and never graduates*, and it does **not** block items
   1–3: repair first to Carbon's values, tint later if wanted.

## 9. Not this proposal

- Does not touch `component-index.json` or any component.
- Does not change the primitive/alias contract, only populates it.
- Does not decide the brand question in item 4.
- Does not re-run the a11y audit; it recommends that a person commission it.
