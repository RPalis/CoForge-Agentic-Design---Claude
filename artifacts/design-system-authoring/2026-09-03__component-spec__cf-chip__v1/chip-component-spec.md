# `cf-chip` — component spec

> **THIS IS A PROPOSAL, NOT AN ENTRY.** Nothing in this document is in
> `design-system/component-index.json` and this artifact does not write to it. The only path
> into the index is promotion: explicit human approval, recorded as an ADR (CLAUDE.md, "The
> membrane"). `screen-producer` may file this; it may not promote it. Until an ADR exists,
> `<CfChip>` is a Gate B **blocker**, and correctly so.
>
> This document also contains a **second, separate proposal**: an amendment to the existing
> `cf-badge` entry. That needs its own approval and its own ADR. Approving one does not
> approve the other.

**Type:** `component-spec` · **Owner:** `screen-producer` · **Date:** 2026-09-03
**Proposed level:** 1 · **Proposed status:** `experimental`
**Tokens:** release `0.2.0` — composed from, never extended.

---

## What it is

A small neutral label carrying a **classification**: which evidence tier, which coverage
state, which category. It answers *what kind of thing is this*, never *how is this thing
doing*.

Its defining property is what it does **not** have: **`cf-chip` has no colour variant.**
There is no `kind`, no `tone`, no `severity`, no `intent`. Every chip on a page looks
identical no matter what it says, and the classification is carried by the word inside it.

That is not minimalism. It is the whole component. The moment a chip can be coloured by its
value, someone maps `never profiled` to red, and a scope decision about who the researchers
had time to reach becomes a judgement about the competitor. The coverage board refused that
mapping twice `[ART-016 § The fourteen]`, and a component that makes it possible a third time
would be the defect rather than the fix.

## Why this is not `cf-badge`, measured

`cf-badge` is bound to `semantic.support.error` / `.success` / `.warning` / `.info` — the
reserved good-to-critical scale. Two independent reasons it cannot take this job, the second
of which is worse than the first.

**Reason one: the scale is reserved and it means something.** `cf-colour-roles` already says
it — "do not use support-\* for decoration; they carry meaning and screen readers rely on it."
An evidence tier is not a health state. Putting `never profiled` on a good-to-critical ramp
asserts that not being profiled is *bad*, which is a claim about the competitor that the
underlying data does not support.

**Reason two, found while writing this and not previously recorded: the status scale does not
work.** Against the ground:

| A | B | Ratio |
|---|---|---|
| `semantic.support.error` | `palette.bone.default` | **4.235:1** |
| `semantic.support.success` | `palette.bone.default` | **4.246:1** |
| `semantic.support.warning` | `palette.bone.default` | **4.221:1** |
| `semantic.support.info` | `palette.bone.default` | **6.598:1** |

Error, success and warning are **within 0.025 of each other**. They are luminance-identical:
red `#da1e28` at Y=0.159872, green `#198038` at Y=0.159305, yellow `#8e6a00` at Y=0.160589.
Their entire difference is hue. In greyscale, in a black-and-white print, or to a reader with
deuteranopia or protanopia, a `cf-badge` reading *error* and a `cf-badge` reading *success*
are the same badge.

So `cf-badge` cannot reliably distinguish the four meanings it already has, and extending it
to carry a fifth axis would compound a defect rather than reuse a capability. This is filed
as a finding against `cf-badge` in this artifact's `validation.md`, and as a proposed
amendment below.

Note also that three of those four fail the 4.5:1 text floor: a `cf-badge` label set in
`semantic.support.error` on bone is 4.235:1 and does not meet SC 1.4.3.

## Token resolution

| Token | Resolves to | Y |
|---|---|---|
| `palette.bone.default` | `#eeece6` | 0.838812 |
| `semantic.layer.accent-01` | `#e0e0e0` | 0.745404 |
| `semantic.border.strong-01` | `#6f6f6f` | 0.158961 |
| `semantic.border.subtle-01` | `#c6c6c6` | 0.564712 |
| `semantic.text.primary` | `#041222` | 0.005739 |
| `semantic.text.secondary` | `#525252` | 0.084376 |
| `semantic.support.error` | `#da1e28` | 0.159872 |
| `semantic.support.success` | `#198038` | 0.159305 |
| `semantic.support.warning` | `#8e6a00` | 0.160589 |
| `semantic.support.info` | `#0043ce` | 0.084705 |

## Measured contrast

Ground is `palette.bone.default`, which `semantic.background` aliases. Floors: **4.5:1** text
(SC 1.4.3), **3:1** non-text (SC 1.4.11).

| A | B | Ratio | Floor | Verdict |
|---|---|---|---|---|
| `semantic.text.primary` | `palette.bone.default` | **15.946:1** | 4.5:1 text | PASS — `outline` label |
| `semantic.text.primary` | `semantic.layer.accent-01` | **14.270:1** | 4.5:1 text | PASS — `subtle` label |
| `semantic.border.strong-01` | `palette.bone.default` | **4.253:1** | 3:1 non-text | PASS — `outline` border |
| `semantic.layer.accent-01` | `palette.bone.default` | **1.117:1** | 3:1 non-text | FAIL — see below |
| `semantic.border.subtle-01` | `palette.bone.default` | **1.446:1** | 3:1 non-text | FAIL — forbidden here |
| `semantic.text.secondary` | `semantic.layer.accent-01` | **5.919:1** | 4.5:1 text | PASS — but not used, see below |

**The `subtle` chip's own boundary is 1.117:1 against the ground and is invisible.** That is
recorded rather than fixed, because in the `subtle` variant nothing depends on the boundary:
the classification is the *word*, at 14.270:1, and the surface is a grouping hint. SC 1.4.11
applies to graphical objects "required to understand the content", and this one is not.
The rule that follows is a hard one: **`subtle` may only be used where losing the surface
entirely would cost the reader nothing.** Where the chip's shape must be seen — where it sits
against a busy background, or where its extent separates two adjacent classifications — the
`outline` variant is required, and its border measures 4.253:1.

`semantic.text.secondary` clears the text floor on both surfaces and is deliberately **not**
used: a second text weight inside a chip would be a second channel, and a chip has one job.

## Variants

| Prop | Values | Notes |
|---|---|---|
| `emphasis` | `subtle` · `outline` | Chosen by **layout context**, never by the chip's value. A group of chips is all-`subtle` or all-`outline`; mixing them inside one group re-invents the colour channel this component exists to remove. |
| `size` | `sm` · `md` | `sm` = `typography.scale.caption` + `spacing.02`/`spacing.03` padding. `md` = `typography.scale.body-sm` + `spacing.03`/`spacing.04`. |

There is no third axis. If a design needs one, that is a finding about the design.

## Accessibility contract

- **SC 1.4.1 Use of Colour** — satisfied trivially and permanently: there is no colour
  channel to misuse. Every chip is the same colour, so colour carries no information at all.
- **SC 1.4.3 Contrast (Minimum)** — labels are `semantic.text.primary`: 15.946:1 on the
  ground, 14.270:1 on the `subtle` surface. Both well over 4.5:1.
- **SC 1.4.11 Non-text Contrast** — the `outline` border is 4.253:1. The `subtle` surface is
  1.117:1 and is declared non-load-bearing, with the usage restriction above.
- **SC 2.5.8 Target Size** — does not apply. A chip is not a target; see below.
- **Semantics** — a chip is a `<span>`. It is **not focusable**, has no `tabindex`, no
  `role`, and no keyboard behaviour. Where the classification needs to be announced with its
  subject, the chip carries a visually-hidden prefix (`evidence tier: 1`) so that a screen
  reader hears `evidence tier: 1` rather than a bare `1`.
- **Zoom and reflow** — chips wrap as inline content. No fixed width, no truncation, no
  ellipsis: a truncated classification is an unreadable classification.

**Not checked here, and not claimed:** any render, any screen-reader pass, any forced-colors
render. This spec has no rendering or AT tooling. Skipped is not passed.

## When to use

A short, closed-set classification that is not a status: evidence tier, coverage state,
competitor category, source type, method. One or two words.

## When NOT to use

- **Not for status.** Health, severity, pass/fail, up/down. That is `cf-badge` — with the
  caveat, measured above, that `cf-badge`'s own scale does not survive greyscale.
- **Never as an action.** No click, no focus, no dismiss, no filter. A chip that filters is a
  control, and a control that can hide rows can conceal the eight unprofiled competitors —
  the exact defect D-001 forbids `[ART-016 § What this board does not do]`. If a filter is
  genuinely needed, it is a Carbon `SelectableTag` or `DismissibleTag` at level 2, it is a
  different component, and it needs its own decision about what it is allowed to hide.
- **Never coloured by its value.** No consumer may add a colour prop, a `data-kind` hook, or
  a CSS override keyed to the label text. If a reviewer asks for "red for never profiled",
  the answer is this paragraph.
- **Never with `semantic.border.subtle-01`** for the `outline` border: 1.446:1 on the ground.
- **Not for long text.** One or two words. A sentence in a chip is a sentence in the wrong box.
- **Not `subtle` where the boundary matters** — 1.117:1 against the ground.
- **It is not Carbon `Tag`** (level 2, and it ships `type` colour variants keyed to the same
  semantic hues, which reintroduces exactly the problem above), **not `DismissibleTag`**,
  **not `OperationalTag`**, **not `SelectableTag`** (all actions), and **not `cf-badge`**.

## What it deliberately cannot do

1. **It cannot be coloured.** One treatment, for every value, forever.
2. **It cannot be clicked.** It is not focusable and has no interactive role.
3. **It cannot hide anything.** It is not a filter and has no selected state.
4. **It cannot be rounded.** Release 0.2.0 has no radius axis, and `gate-b.py` blocks
   `border-radius: <n>px` as raw spacing. A rounded chip is not expressible on-token today.
   The chip ships square-cornered. Recorded as a token gap, not worked around.
5. **It cannot count.** `cf-badge` carries counts; a chip carries a class name.

<!-- PROPOSED-INDEX-ENTRY -->
```json
{
  "name": "cf-chip",
  "level": 1,
  "status": "experimental",
  "category": "classification",
  "summary": "A small neutral label carrying a non-status classification — evidence tier, coverage state, category. Has no colour variant by design: every chip looks identical whatever it says, so no classification can be scored good or bad by its treatment.",
  "variants": {
    "emphasis": ["subtle", "outline"],
    "size": ["sm", "md"]
  },
  "tokens_used": [
    "semantic.layer.accent-01",
    "semantic.border.strong-01",
    "semantic.text.primary",
    "spacing.01",
    "spacing.02",
    "spacing.03",
    "spacing.04",
    "typography.scale.caption",
    "typography.scale.body-sm"
  ],
  "a11y": {
    "contrast": "WCAG 2.2 AA — 4.5:1 text, 3:1 non-text. Measured on palette.bone.default: label semantic.text.primary 15.946:1 on the ground and 14.270:1 on semantic.layer.accent-01; outline border semantic.border.strong-01 4.253:1.",
    "note": "There is no colour channel, so SC 1.4.1 cannot be violated by this component. The subtle surface is 1.117:1 against the ground and is deliberately non-load-bearing — use outline wherever the chip's boundary must be seen. Not focusable and not an action."
  },
  "when_to_use": "A short, closed-set classification that is NOT a status: evidence tier, coverage state, category, source type, method. One or two words.",
  "when_not_to_use": "Not for status — that is cf-badge. Never as an action: a chip that filters is a control, and a control that hides rows can conceal missing data (D-001). Never coloured by its value; there is no colour prop and none may be added. Never with semantic.border.subtle-01 for the outline (1.446:1 on bone). Not subtle where the boundary carries meaning (1.117:1). Not Carbon Tag, DismissibleTag, OperationalTag or SelectableTag.",
  "source": "CoForge L1 primitive — authored 2026-09-03 by screen-producer against tokens release 0.2.0. PROPOSAL: not promoted, no ADR."
}
```

## Second proposal — an amendment to the existing `cf-badge` entry

Separate change, separate approval, separate ADR. `cf-badge` is a `stable` entry already in
the index; `screen-producer` does not own it and is not editing it. What follows is the exact
text proposed.

**Replace `cf-badge.when_not_to_use`, currently:**

> Do not use a badge for an action — it is not a button and is not focusable.

**with:**

> Do not use a badge for an action — it is not a button and is not focusable. Do not use it
> for a non-status classification such as an evidence tier, a coverage state or a category:
> the kind axis is the reserved good-to-critical scale, and putting a neutral class name on it
> asserts a judgement the data does not support. Use cf-chip. Note also that on
> palette.bone.default the error, success and warning kinds measure 4.235:1, 4.246:1 and
> 4.221:1 — luminance-identical — so kind alone is a hue-only channel and fails SC 1.4.1 in
> greyscale, in print, and for dichromatic readers. Every badge must carry its meaning in its
> text, never in its colour.

**And add to `cf-badge.a11y.note`:**

> The four kinds are separated by hue only. Measured on palette.bone.default: error 4.235:1,
> success 4.246:1, warning 4.221:1, info 6.598:1 — the first three are within 0.025 of each
> other. Colour is never sufficient; the label must say which state it is.

This amendment does not change any token or any rendered pixel. It records a measured
property of the entry that its own `a11y.note` currently contradicts by implication.

## Claims, labelled

- `Evidenced [ART-016 § The fourteen]`, `[ART-016 § What this board does not do]` — the
  coverage board's tier chips, and D-001, the decision that no control may conceal the eight
  unprofiled competitors. Measurement citations under ADR-017.
- `Measured, this session` — every ratio and hex above, derived from
  `design-system/tokens/tokens.json` `$version` 0.2.0 and re-derivable by `verify-contrast.py`
  in this directory.
- `Inferred from the measurements` — that `cf-badge` cannot take this job; that `subtle` must
  be restricted to contexts where the boundary is not load-bearing; that `emphasis` must be
  chosen per group rather than per value.

## Assumptions

- **A-1.** A classification set small enough to read. This component assumes a reader can
  scan five or six chips; it makes no claim about fifty. At that scale the answer is a table
  column, not a chip.
- **A-2.** Every ratio is against `palette.bone.default`. `semantic-dark` was not measured
  and none of these numbers transfers to it.
- **A-3.** `spacing.01` is used as a **border width**. Release 0.2.0 has no border-width axis;
  `cf-spacing-scale` declares the spacing scale for "margin, padding and gap". This is an
  existing token used off-label, not an invented value, and the human at promotion should
  decide whether a `border.width.*` axis is owed first.
- **A-4.** Square corners are acceptable. This is forced rather than chosen — there is no
  radius token — and it is stated so nobody records it as a style decision.
