# `cf-unit-cell` — component spec

> **THIS IS A PROPOSAL, NOT AN ENTRY.** Nothing in this document is in
> `design-system/component-index.json` and this artifact does not write to it. The only
> path into the index is promotion: explicit human approval, recorded as an ADR
> (CLAUDE.md, "The membrane"). `screen-producer` may file this; it may not promote it.
> Until an ADR exists, `<CfUnitCell>` is a Gate B **blocker**, and correctly so.

**Type:** `component-spec` · **Owner:** `screen-producer` · **Date:** 2026-09-03
**Proposed level:** 1 · **Proposed status:** `experimental`
**Tokens:** release `0.2.0` — composed from, never extended.

---

## What it is

The atom of a unit chart / dot matrix. One cell = one observation. A grid of them is read
as a *pattern*, and the finding lives in where the pattern **breaks**, not in where it is
darkest. That inversion is the whole reason this component is not `cf-badge` with a smaller
box: a badge asserts a state, a unit cell asserts a *census*, and a census is only honest if
the cells nobody counted are as visible as the cells somebody did.

It serves two objects on the coverage board `[ART-016 § The fourteen]`: a 770-cell coverage
grid (55 capability rows × 14 competitors) and a 112-cell journey matrix (14 competitors ×
8 stages) `[ART-016 § The journey]`.

## The three states, and why absence is the default

| State | Means | Ink | Fill | Border |
|---|---|---|---|---|
| `value` | An observation exists, at an ordinal step | 100% | solid, ordinal step | `spacing.01` **solid**, *same colour as the fill* |
| `prior-art` | Evidence exists only in an earlier, superseded framing (D-002) | ~56% dense / ~30% comfortable | none | `spacing.01` **dashed**, `semantic.border.strong-01` |
| `no-data` | **No data was collected.** Nobody looked. | 0% | none | none |

`no-data` is drawn as **nothing at all** — the ground shows through and the pattern has a
literal hole in it. That is not a stylistic preference; it is the only one of the three that
cannot be mistaken for a low value, because a low value is still ink and this is the absence
of ink. It is also the direct answer to the board's headline finding: eight of fourteen
competitors were never profiled, and eight empty columns in a 770-cell grid say that without
a single word `[ART-016 § Disclaimer]`.

**The distinguishing channel is ink footprint, not colour and not pattern.** 100% / ~56% /
0% of the cell's area, at every density, in every colour, on every output surface. Hatching
and texture were rejected before they were drawn: at the 12px dense cell they collapse into
moiré, and a channel that only works above 8px is not a channel for a 770-cell grid.

Consequence, stated plainly: **this component satisfies WCAG 2.2 SC 1.4.1 (Use of Colour)
by construction.** Remove every colour from the grid and all three states still read. That
is testable by rendering it in greyscale, and it is the one property no reviewer should take
on trust.

## Token resolution — every value this spec uses, resolved through the alias chain

Re-derived by `verify-contrast.py` in this directory. `Y` is WCAG relative luminance,
`Y = 0.2126R + 0.7152G + 0.0722B` on linearised sRGB.

| Token | Resolves to | Y |
|---|---|---|
| `palette.bone.default` | `#eeece6` | 0.838812 |
| `palette.teal.60` | `#007d79` | 0.160477 |
| `palette.teal.70` | `#005d5d` | 0.086190 |
| `palette.teal.90` | `#022b30` | 0.019541 |
| `semantic.background` | `#eeece6` | 0.838812 |
| `semantic.border.strong-01` | `#6f6f6f` | 0.158961 |
| `semantic.border.subtle-01` | `#c6c6c6` | 0.564712 |
| `semantic.focus` | `#0f62fe` | 0.159927 |
| `semantic.focus-inset` | `#ffffff` | 1.000000 |
| `semantic.text.primary` | `#041222` | 0.005739 |

## Measured contrast — computed, not asserted

Ground is `palette.bone.default`, which is what `semantic.background` aliases and therefore
the surface every one of these marks is actually drawn on. WCAG 2.2 AA floors: **3:1** for
non-text graphical objects and UI boundaries (SC 1.4.11), **4.5:1** for normal text (SC 1.4.3).

### Every mark against the ground

| A | B | Ratio | Floor | Verdict |
|---|---|---|---|---|
| `palette.teal.60` | `palette.bone.default` | **4.223:1** | 3:1 non-text | PASS |
| `palette.teal.70` | `palette.bone.default` | **6.526:1** | 3:1 non-text | PASS |
| `palette.teal.90` | `palette.bone.default` | **12.781:1** | 3:1 non-text | PASS |
| `semantic.border.strong-01` | `palette.bone.default` | **4.253:1** | 3:1 non-text | PASS |
| `semantic.focus` | `palette.bone.default` | **4.234:1** | 3:1 non-text | PASS |
| `semantic.text.primary` | `palette.bone.default` | **15.946:1** | 4.5:1 text | PASS |
| `semantic.border.subtle-01` | `palette.bone.default` | **1.446:1** | 3:1 non-text | **FAIL — forbidden here** |

### The finding that shaped the component: adjacent ordinal steps do not clear 3:1

| A | B | Ratio | Floor | Verdict |
|---|---|---|---|---|
| `palette.teal.60` | `palette.teal.70` | **1.545:1** | 3:1 adjacent non-text | **FAIL** |
| `palette.teal.70` | `palette.teal.90` | **1.958:1** | 3:1 adjacent non-text | **FAIL** |
| `palette.teal.60` | `palette.teal.90` | **3.027:1** | 3:1 adjacent non-text | PASS, barely |

Two cells of *different* ordinal value, touching, are 1.545:1 apart. That is under the SC
1.4.11 floor for graphical objects that must be told apart, and no choice of hue fixes it:
release 0.2.0 mirrors Carbon's cross-hue lightness parity, so step 60 is Y≈0.160 and step 70
is Y≈0.086 in *every* family. Picking blue instead of teal changes nothing — measured
independently below.

This is not a property of teal, or of the three steps chosen. Measured across **all 12 hue
families that carry a full 10-step ramp** — blue, coolGray, cyan, gray, green, magenta,
orange, purple, red, teal, warmGray, yellow — there are 108 adjacent-step pairs, and:

```
adjacent-step pairs, all 12 families:  n=108   min 1.181:1   max 1.579:1   mean 1.371:1
  clearing 3:1 : 0 of 108
  clearing 2:1 : 0 of 108
```

**No two adjacent steps anywhere in this token set clear even 2:1.** On the teal ladder a
pair must be at least three steps apart before it reaches 3:1 (`teal.60` to `teal.90`,
3.027:1), and how far apart depends on where you are on the ladder, because contrast ratios
compress at both ends.

Pushed to its limit: the largest set of steps within one hue that is **mutually** 3:1 is
three (`10`, `50`, `80` and six other such triples) — but every one of those triples contains
a step that is invisible on the bone ground. **The largest set that is both mutually 3:1 and
individually ≥3:1 on bone is TWO steps: `60` and `90`.** Identical result in blue, gray and
coolGray, checked.

| A | B | Ratio | What it shows |
|---|---|---|---|
| `palette.teal.70` | `palette.teal.80` | **1.481:1** | adjacent, mid-ladder |
| `palette.teal.80` | `palette.teal.90` | **1.323:1** | adjacent, dark end |
| `palette.blue.60` | `palette.blue.70` | **1.558:1** | the best adjacent pair in blue |
| `palette.orange.60` | `palette.orange.70` | **1.579:1** | the widest adjacent pair in the entire token set |

So an ordinal encoding on release 0.2.0 has exactly two honest shapes: **two steps whose
fills may touch**, or **three steps that must never touch**. This component takes the second,
which is why the gutter is not negotiable.

**Therefore the gutter is part of the contract, not a layout preference.** Every cell is
separated from every neighbour by `spacing.01` of `semantic.background`. With the gutter, a
fill's adjacent colour is the ground, not the neighbour, and the worst case becomes
`palette.teal.60` vs `palette.bone.default` = **4.223:1**. A `cf-unit-cell` grid rendered
without the gutter is off-contract and its ordinal steps do not meet AA.

### Why the focus ring is two-tone and `semantic.focus-inset` is mandatory

| A | B | Ratio | What it is |
|---|---|---|---|
| `semantic.focus` | `palette.teal.60` | **1.003:1** | outer ring against a `value` cell at step 1 — **invisible** |
| `semantic.focus-inset` | `palette.teal.60` | **4.989:1** | inner ring against the same cell |
| `semantic.focus-inset` | `palette.teal.70` | **7.710:1** | inner ring, step 2 |
| `semantic.focus-inset` | `palette.teal.90` | **15.099:1** | inner ring, step 3 |
| `semantic.focus` | `palette.bone.default` | **4.234:1** | outer ring against the gutter and against a `no-data` cell |

`semantic.focus` is `palette.blue.60`; `palette.teal.60` is the lightest ordinal fill. On the
universal ladder both sit at Y≈0.160, so a blue focus ring on a teal cell measures **1.003:1**
— the focus indicator disappears exactly where a keyboard user most needs it. A single-colour
focus ring cannot be made to work here from release 0.2.0 by any token substitution.

The indicator is therefore **two rings**: `semantic.focus` outward into the gutter (4.234:1
against the ground) and `semantic.focus-inset` inward onto the fill (4.989:1 worst case). One
of the two always clears 3:1 against whatever it abuts. Dropping either half breaks SC 1.4.11
on one state or the other.

### The isoluminance is not a teal problem

| A | B | Ratio |
|---|---|---|
| `palette.blue.60` | `palette.bone.default` | **4.234:1** |
| `palette.purple.60` | `palette.bone.default` | **4.235:1** |
| `palette.magenta.60` | `palette.bone.default` | **4.239:1** |
| `palette.teal.60` | `palette.bone.default` | **4.223:1** |
| `palette.cyan.40` | `palette.bone.default` | **2.003:1** |

Four different hues at step 60, all within 0.016 of each other against the ground. Any two of
them are luminance-identical. This is why the ordinal channel is a **single hue at three
steps** and never a hue rotation.

## Variants

| Prop | Values | Notes |
|---|---|---|
| `state` | `value` · `prior-art` · `no-data` | Closed. There is no fourth. |
| `value-step` | `1` · `2` · `3` | `palette.teal.60` / `.70` / `.90`. Only meaningful when `state` is `value`. |
| `density` | `dense` · `comfortable` | `dense` = `spacing.04` cell + `spacing.01` gutter (12px + 2px at a 16px root). `comfortable` = `spacing.06` cell + `spacing.02` gutter (24px + 4px). |
| `interactive` | `true` · `false` | `true` is **forbidden at `dense`** — see Target size. |

**Three ordinal steps is the ceiling, and only with the gutter.** A fourth step would have to
come from `palette.teal.50` (2.826:1 against the ground, under the 3:1 non-text floor) or
from an intermediate that does not exist. And if the gutter is ever removed, the ceiling drops
to **two** — `60` and `90` are the only pair on this ladder that is both mutually 3:1 and
individually visible on bone. If a dataset needs four ordinal levels, the finding is that the
token layer cannot express it — not that a step should be invented.

## Composition — it is a `<td>`, not a new grid

At `dense` the grid is a real `<table>`, which is `cf-table`, with `<th scope="col">` for
competitors and `<th scope="row">` for capabilities. Each `cf-unit-cell` is the content of a
`<td>`. This is deliberate: it means the cell's meaning is carried by its row and column
headers, which assistive technology already announces, rather than by 770 hand-written
labels. Each cell additionally carries a visually-hidden state word (`rated 2 of 3`,
`prior art only`, `not evaluated`) so the state is spoken, not inferred from a fill.

`cf-unit-cell` does **not** introduce a grid, a layout engine, or a chart container. It is a
mark. The container is `cf-table`.

## Accessibility contract

- **SC 1.4.1 Use of Colour** — satisfied structurally. States differ by ink footprint
  (100% / ~56% / 0%); ordinal steps differ by lightness within one hue *and* by the
  visually-hidden state word. A greyscale render loses nothing.
- **SC 1.4.11 Non-text Contrast** — every mark ≥ 3:1 against the ground (worst case
  4.223:1). Adjacent-cell contrast is met via the mandatory gutter, not via the fills.
- **SC 1.4.3 Contrast (Minimum)** — no text is ever set in an ordinal fill colour.
  `palette.teal.60` measures 4.223:1, **below** the 4.5:1 text floor. Labels and legends use
  `semantic.text.primary` (15.946:1). This is a hard prohibition, and it is the most likely
  way a future consumer will break this component.
- **SC 2.5.8 Target Size (Minimum)** — at `comfortable`, the cell is `spacing.06` = 24px at
  a 16px root, meeting the 24×24 minimum exactly. At `dense` the pitch is 14px and the
  minimum **cannot** be met, so `interactive` is forbidden there: dense cells are keyboard-
  reachable (one tab stop, roving `tabindex`, arrow-key movement, `role="grid"`) but are not
  pointer targets. Any board that offers cell-level detail on pointer must render that data
  at `comfortable` somewhere on the same page.
- **Focus** — two-tone, as measured above. Never suppressed, never `outline: none`.
- **Forced colours** (`forced-colors: active`) — backgrounds are remapped by the UA, so the
  fill channel collapses. The border channel survives: `value` keeps a solid border in its
  own fill colour (invisible in normal rendering, `CanvasText` in forced colours),
  `prior-art` is dashed, `no-data` has none. Three states, still three appearances. No system
  colour keyword is written by this component.
- **Print** — same mechanism. If the reader's Print dialog drops background graphics, the
  borders still print and the three states remain distinct.
- **Colour vision deficiency** — the ordinal ramp is one hue at three lightness steps, so it
  is unaffected by any dichromacy. This is a consequence of the single-hue rule, not a
  separate mitigation.

**Not checked here, and not claimed:** an actual screen-reader pass, a real forced-colors
render, a 400% zoom reflow of a 770-cell grid, and a printed page. This spec has no rendering
or AT tooling. Skipped is not passed.

## When to use

A census where the count of *missing* observations is part of the finding. Coverage matrices,
evaluation grids, isotype-style unit charts. Use it when a reader must be able to see, without
reading a number, that a region of the data was never collected.

## When NOT to use

- **Not for status.** A cell is an observation, not a health state. `cf-badge` owns status.
- **Not as a heat map with a continuous scale.** Three ordinal steps is the ceiling release
  0.2.0 supports; a continuous ramp would need steps that fail 3:1 against each other.
- **Not without the gutter.** Ungutted, adjacent ordinal steps measure 1.545:1 and the grid
  fails SC 1.4.11.
- **Not as a pointer target at `dense`.** 14px pitch cannot meet SC 2.5.8.
- **Never with `semantic.border.subtle-01`** for the `prior-art` outline: 1.446:1 on the
  ground. The outline *is* the meaning of that state; drawing it in a colour a reader cannot
  see deletes the state.
- **Not for text.** No label is ever set in `palette.teal.60` (4.223:1, under 4.5:1).
- **It is not `cf-chart-palette`.** That primitive is categorical — five hues, four of which
  are luminance-identical at step 60 (4.223–4.239:1 against the ground) and one of which,
  `palette.cyan.40`, measures 2.003:1 and misses the 3:1 non-text floor outright. It cannot
  express an ordinal ramp; its `tokens_used` lists one step per hue, so the `sequential` and
  `diverging` variants it advertises have no values behind them.
- **It is not `cf-table`** (the container), **not `Tile` / `ClickableTile`** (Carbon, level 2,
  a content surface with padding and elevation), and **not `cf-badge`**.

## What it deliberately cannot do

1. **It cannot hide.** There is no `collapsed`, no `hidden`, no "omit empty cells" mode. A
   control that removes the blanks removes the finding (D-001) `[ART-016 § What this board does not do]`.
2. **It cannot carry a fourth ordinal step.** See Variants.
3. **It cannot be interactive at `dense`.** See SC 2.5.8.
4. **It cannot encode two variables at once.** One cell, one observation, one ordinal step.
   Value-suppressed-by-uncertainty is explicitly out of scope: two ordinal ramps on this token
   ladder are luminance-identical at matching step numbers, so the second variable would be
   unreadable. If confidence must be shown, it belongs on a different channel entirely
   (a border treatment on the *row*, or a separate legend), not inside this component.
5. **It cannot label itself.** No text ever renders inside the cell at `dense` — 12px leaves
   no room, and the accessible name does the work instead.

<!-- PROPOSED-INDEX-ENTRY -->
```json
{
  "name": "cf-unit-cell",
  "level": 1,
  "status": "experimental",
  "category": "data",
  "summary": "One observation in a unit chart or dot matrix. Three states — a filled ordinal value, a dashed outline for prior-art-only evidence, and nothing at all for no data collected — distinguished by ink footprint, never by colour alone.",
  "variants": {
    "state": ["value", "prior-art", "no-data"],
    "value-step": ["1", "2", "3"],
    "density": ["dense", "comfortable"],
    "interactive": ["true", "false"]
  },
  "tokens_used": [
    "palette.teal.60",
    "palette.teal.70",
    "palette.teal.90",
    "semantic.background",
    "semantic.border.strong-01",
    "semantic.focus",
    "semantic.focus-inset",
    "semantic.text.primary",
    "spacing.01",
    "spacing.02",
    "spacing.04",
    "spacing.06",
    "typography.scale.caption"
  ],
  "a11y": {
    "contrast": "WCAG 2.2 AA — 4.5:1 text, 3:1 non-text. Measured on palette.bone.default: teal.60 4.223:1, teal.70 6.526:1, teal.90 12.781:1, border.strong-01 4.253:1, focus 4.234:1.",
    "note": "Absence is drawn as no ink, not as a colour: SC 1.4.1 is met structurally and a greyscale render loses nothing. The spacing.01 gutter is mandatory — adjacent ordinal steps measure 1.545:1 and only clear 3:1 against the ground. Focus is two-tone (semantic.focus outward, semantic.focus-inset inward) because semantic.focus measures 1.003:1 on palette.teal.60. interactive is forbidden at dense: the 14px pitch cannot meet SC 2.5.8."
  },
  "when_to_use": "A census where the number of MISSING observations is part of the finding — coverage matrices, evaluation grids, isotype unit charts.",
  "when_not_to_use": "Not for status (that is cf-badge). Not as a continuous heat map — three ordinal steps is the ceiling release 0.2.0 supports. Never without the gutter. Never with semantic.border.subtle-01 (1.446:1 on bone) for the prior-art outline. Never as a pointer target at dense. Never set text in an ordinal fill colour — teal.60 is 4.223:1, under the 4.5:1 text floor.",
  "source": "CoForge L1 primitive — authored 2026-09-03 by screen-producer against tokens release 0.2.0. PROPOSAL: not promoted, no ADR."
}
```

## Claims, labelled

- `Evidenced [ART-016 § The fourteen]`, `[ART-016 § The journey]`, `[ART-016 § Disclaimer]`,
  `[ART-016 § What this board does not do]` — the two grids this serves, the eight unprofiled
  competitors, the D-001 no-hiding decision and the D-002 prior-art state. Measurement
  citations under ADR-017; they resolve to a registered artifact and to real section headings
  in its payload.
- `Measured, this session` — every contrast figure and every hex above. Derived from
  `design-system/tokens/tokens.json` `$version` 0.2.0 by `verify-contrast.py` in this
  directory, which re-derives all of them on demand. None is quoted from another document.
- `Inferred from the measurements` — the mandatory gutter, the two-tone focus ring, the
  three-step ceiling, and the ban on `interactive` at `dense`. Each follows from a number in
  the tables above; each is stated with the number it follows from.

## Assumptions

- **A-1.** A 16px root font size, which is where `spacing.06` resolves to 24 CSS px and meets
  SC 2.5.8. The spacing axis is rem-only and release 0.2.0 has no px-denominated dimension
  token, so **no token can guarantee a CSS-px target size**. If the root shrinks, the target
  shrinks with it and the criterion is missed. Reported as a gap, not worked around.
- **A-2.** The board renders on `semantic.background` (bone). Every ratio here is against
  that ground and none of them transfers to `semantic-dark`, which was not measured.
- **A-3.** The dashed `prior-art` border reads as dashed at a 12px cell with a 2px border
  (roughly one and a half dashes per side). This is a rendering judgement, not a measurement,
  and it has not been rendered. It is the weakest claim in this document.
- **A-4.** `spacing.01` is used as a **border width**. `cf-spacing-scale` declares the
  spacing axis for "margin, padding and gap"; release 0.2.0 has no border-width axis at all.
  This is an existing token used off-label, not a new value — but it is off-label, and the
  human at promotion should decide whether that is acceptable or whether a `border.width.*`
  axis is owed first.
