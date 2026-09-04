# `cf-detail-panel` — component spec

> **THIS IS A PROPOSAL, NOT AN ENTRY.** Nothing in this document is in
> `design-system/component-index.json` and this artifact does not write to it. The only path
> into the index is promotion: explicit human approval, recorded as an ADR (CLAUDE.md, "The
> membrane"). `screen-producer` may file this; it may not promote it. Until an ADR exists,
> `<CfDetailPanel>` is a Gate B **blocker**, and correctly so.

**Type:** `component-spec` · **Owner:** `screen-producer` · **Date:** 2026-09-03
**Proposed level:** 1 — **contested; see "The level question" below**
**Proposed status:** `experimental` · **Tokens:** release `0.2.0` — composed from, never extended.

---

## What it is

A side panel that reveals the provenance behind one clicked cell or row — which source, which
date, which method, which artifact — **while the grid stays fully visible and fully operable
behind it.**

That last clause is the component, not a preference. On a coverage board the reader's question
is almost always comparative: *why is this cell empty when the one above it is not?* A panel
that covers the grid answers a question the reader is no longer able to ask.

## Click-to-pin, never hover

The panel opens on **activation** — click, `Enter`, or `Space` — and stays open until it is
closed. It never opens on hover, for four reasons, each independently sufficient:

1. **Hover does not exist on touch.** There is no hover state on a phone or a tablet, so a
   hover-only panel makes provenance unreachable for those readers entirely.
2. **Hover is invisible to keyboard users.** A keyboard user moves focus, not a pointer. A
   hover-only panel is a feature they cannot know exists.
3. **A hover panel over a 770-cell grid fires constantly.** Crossing the grid to reach one
   cell passes over dozens. The panel would flicker through a dozen provenances on the way to
   the one the reader wanted.
4. **SC 1.4.13 Content on Hover or Focus** would then apply, requiring the content to be
   dismissable, hoverable and persistent. Meeting all three for a panel this size is possible
   and is entirely wasted work, because click-to-pin satisfies the underlying need better.

## Focus management, stated exactly

This is the part of a disclosure component that is usually left vague, so it is written as a
sequence rather than as a principle.

**Pattern:** disclosure with managed focus. **Not a dialog.** `aria-modal` is never set,
`role="dialog"` is not used, the background is never `inert`, and there is no focus trap —
all four of which exist to make the rest of the page unusable, which is the opposite of this
component's requirement.

- **Markup.** The trigger (a `cf-unit-cell` at `comfortable` density, or a table row) carries
  `aria-expanded` and `aria-controls` pointing at the panel's `id`. The panel is
  `<aside id="…" aria-labelledby="…" tabindex="-1">` placed immediately after the grid in DOM
  order, so tab order is coherent without any scripted reordering.
- **On open.** The panel's content is populated, `aria-expanded` becomes `true`, and focus
  moves to the panel container. Focus moves because the panel is far from the trigger in
  reading order and a reader arriving by keyboard would otherwise have no idea anything
  happened. The container uses `:focus-visible`, so a mouse user sees no focus ring for a
  move they did not make.
- **On changing cells while the panel is open.** The content is replaced and focus moves to
  the panel container again. One rule for both cases, deliberately: a rule that behaves
  differently for mouse and keyboard is a rule nobody can test, and this one is testable.
  Because focus moves on every change, **no `aria-live` region is used** — a live region plus
  a focus move announces the same content twice.
- **Escape.** Closes the panel, sets `aria-expanded` to `false`, and returns focus to the
  trigger that opened it. The handler is delegated to the container so `Escape` works whether
  focus is in the panel or back in the grid.
- **Close button.** Required, not optional — `Escape` is not discoverable. It carries a real
  accessible name (`Close provenance for <cell>`, not `Close`), and its target is at least
  `spacing.06`. Activating it does exactly what `Escape` does, including the focus return.
- **If the trigger no longer exists** when the panel closes (the grid re-rendered), focus goes
  to the grid container rather than to `<body>`. Focus landing on `<body>` loses the reader's
  place completely and is the most common failure of this pattern.
- **Tab from the last element in the panel** continues to the next element on the page. It
  does not cycle. There is no trap.
- **One panel at a time.** Opening a second cell replaces the first panel's content. Two
  provenance panels would be two levels of the same level.

## The two-level disclosure limit is binding

The grid is level one. This panel is level two. **Nothing may nest below it.** Concretely,
inside `cf-detail-panel` there may be no accordion, no second panel, no `<details>`, no
click-to-open tooltip, and no modal.

When the provenance does not fit, the panel **links out** to the full artifact. A link is
navigation, not a third level of disclosure: it takes the reader somewhere with a URL, a back
button and a place in history, rather than burying content under two clicks with no address.

## Token resolution

| Token | Resolves to | Y |
|---|---|---|
| `palette.bone.default` | `#eeece6` | 0.838812 |
| `semantic.layer.02` | `#ffffff` | 1.000000 |
| `semantic.border.strong-01` | `#6f6f6f` | 0.158961 |
| `semantic.border.subtle-01` | `#c6c6c6` | 0.564712 |
| `semantic.text.primary` | `#041222` | 0.005739 |
| `semantic.text.secondary` | `#525252` | 0.084376 |
| `semantic.link.primary` | `#0043ce` | 0.084705 |
| `semantic.focus` | `#0f62fe` | 0.159927 |
| `semantic.focus-inset` | `#ffffff` | 1.000000 |

## Measured contrast

The panel surface is `semantic.layer.02`; the page ground is `palette.bone.default`. Floors:
**4.5:1** text (SC 1.4.3), **3:1** non-text (SC 1.4.11).

| A | B | Ratio | Floor | Verdict |
|---|---|---|---|---|
| `semantic.layer.02` | `palette.bone.default` | **1.181:1** | — | the panel has **no visible edge** on the ground |
| `semantic.border.strong-01` | `palette.bone.default` | **4.253:1** | 3:1 non-text | PASS — the panel edge, and it is required |
| `semantic.border.strong-01` | `semantic.layer.02` | **5.025:1** | 3:1 non-text | PASS |
| `semantic.border.subtle-01` | `semantic.layer.02` | **1.708:1** | 3:1 non-text | **FAIL — forbidden as the panel edge** |
| `semantic.text.primary` | `semantic.layer.02` | **18.838:1** | 4.5:1 text | PASS — heading and body |
| `semantic.text.secondary` | `semantic.layer.02` | **7.814:1** | 4.5:1 text | PASS — labels and metadata |
| `semantic.link.primary` | `semantic.layer.02` | **7.795:1** | 4.5:1 text | PASS — the link out |
| `semantic.focus` | `semantic.layer.02` | **5.002:1** | 3:1 non-text | PASS — outer focus ring |
| `semantic.focus-inset` | `semantic.focus` | **5.002:1** | 3:1 non-text | PASS — inner focus ring |

**The panel has no edge of its own.** `semantic.layer.02` is `#ffffff`; against the bone
ground it measures **1.181:1**. A white panel floating on a warm bone page is, in contrast
terms, not floating on anything. `elevation.surface.raised` contributes a shadow, but a
shadow is an alpha value over the ground and cannot be relied on to carry a boundary. The
panel therefore carries an explicit `spacing.01` border in `semantic.border.strong-01`
(4.253:1 against the ground). Without it, the reader cannot tell where the grid ends and the
provenance begins — which is precisely the distinction the panel exists to make.

## What `semantic.overlay` is, and why it is forbidden here

`semantic.overlay` resolves to `palette.black.default-a60` — black at 60% alpha. It is the
modal scrim, and its purpose is to make everything behind it unreadable so the reader attends
to one thing.

**This component must never use it.** Its requirement is the exact inverse: the grid stays
visible. `semantic.overlay` is listed here, with its meaning, so that a future implementer
reaching for "the token that makes a panel feel like a panel" finds the reason not to,
attached to the token name.

## Variants

| Prop | Values | Notes |
|---|---|---|
| `placement` | `right` · `bottom` | Set by the **page layout**, not by the component, and not by a breakpoint this component owns — release 0.2.0 has no breakpoint axis. |
| `emphasis` | `flat` · `raised` | `elevation.surface.flat` or `elevation.surface.raised`. The border is present either way; elevation never substitutes for it. |

There is no `width` variant. See below.

## The width cannot be expressed on-token, and is not invented

Release 0.2.0's only dimension axis is `spacing`, which tops out at `spacing.13` = 10rem
(160px). There is no layout or size axis. **No token in this release can express a side-panel
width.**

The resolution is not to invent one and not to write a raw value. **The panel has no width of
its own.** It fills the layout column the page gives it (`width: 100%` of its grid area), and
the width decision lives in the page's layout, where a grid fraction is a layout property
rather than a design value. Recorded as a token gap in this artifact's `validation.md`.

## The level question — stated, not resolved

Proposed at **level 1**, and the reviewer should know this is the weakest classification in
the batch.

**For level 1.** ADR-012's own test is what a level needs: L1 needs tokens, `brand.md` and
the primitive set; L2 needs "the full component library, Code Connect and the CoForge MCP."
This component needs none of the three. Every value it uses is a token. It is a single
`<aside>` in a single HTML document, which is exactly the L1 output shape.

**Against level 1.** It carries required scripted behaviour — focus management, `Escape`,
`aria-expanded` — and no existing level-1 primitive does. If "level 1" is read as "static",
this is not level 1.

**A third fact, which decides it for now.** `validation/adapters/carbon-react.py` preserves
index entries where `level == 1` and rebuilds everything else from the Carbon tarball, and it
unconditionally deletes every file in `design-system/components/`. A CoForge-authored
**level 2** entry would be erased on the next adapter run. Level 2 is currently a lossy
destination for anything CoForge authors, so proposing this at level 2 would be proposing to
lose it. That is a defect in the repository, reported in `validation.md`, not a reason level 1
is correct — and the human at promotion should treat it as a constraint to remove rather than
a justification to accept.

## Accessibility contract

- **Pattern** — disclosure with managed focus. `aria-expanded` and `aria-controls` on the
  trigger; `<aside aria-labelledby tabindex="-1">` for the panel. No `role="dialog"`, no
  `aria-modal`, no `inert`, no focus trap, no scrim.
- **SC 1.4.3 Contrast (Minimum)** — heading and body 18.838:1, metadata 7.814:1, link out
  7.795:1. All over 4.5:1.
- **SC 1.4.11 Non-text Contrast** — panel edge 4.253:1 against the ground; focus ring 5.002:1
  on the panel surface. `semantic.layer.02` at 1.181:1 is explicitly not load-bearing.
- **SC 2.1.2 No Keyboard Trap** — satisfied by construction: there is no trap, `Tab` leaves
  the panel, and `Escape` closes it.
- **SC 2.4.3 Focus Order** — the panel sits immediately after the grid in DOM order, so the
  visual order and the tab order agree without scripted reordering.
- **SC 2.4.11 Focus Not Obscured (Minimum)** — at `placement: right` the panel must not
  overlay the focused cell. The grid and the panel share the layout row; the panel takes a
  column, it does not float over one.
- **SC 2.5.8 Target Size (Minimum)** — the close button is at least `spacing.06` (24px at a
  16px root). The panel's triggers are `cf-unit-cell` at `comfortable`, or a table row: both
  meet 24px. `cf-unit-cell` at `dense` is **not** a valid trigger for this panel, because a
  14px pitch cannot meet the criterion.
- **SC 1.4.13 Content on Hover or Focus** — does not apply. The panel never opens on hover.
- **Motion** — open uses `motion.transition.reveal.duration` and `.easing`; close uses
  `motion.transition.dismiss.duration` and `.easing`. Under `prefers-reduced-motion: reduce`
  both are removed and the panel appears and disappears instantly.
- **Print** — the panel prints only if it is open, in place, after the grid. It is never a
  floating layer in print.

**Not checked here, and not claimed:** any render, any keyboard walk, any screen-reader pass,
any forced-colors render, any touch test. Every behaviour above is specified, none is
observed. This spec has no rendering or AT tooling. Skipped is not passed.

## When to use

Level-two provenance for one selected cell or row on an analytical page, where the reader must
keep comparing that cell to its neighbours while reading about it.

## When NOT to use

- **Never on hover.** See the four reasons above.
- **Never as a modal.** No scrim, no `aria-modal`, no `inert` background, no focus trap. If
  the task genuinely requires the rest of the page to be unavailable, that is Carbon `Modal`
  or `ComposedModal` at level 2 — a different component with the opposite requirement.
- **Never with `semantic.overlay`.** It is the modal scrim; it obscures the grid.
- **Never with `semantic.border.subtle-01`** as the panel edge: 1.708:1 on the panel's own
  surface and 1.446:1 on the ground.
- **Never nest anything disclosable inside it.** Two levels is the limit; the panel is level
  two. Overflow links out.
- **Never as the only route to information.** Provenance that exists only behind a click is
  provenance that will not be printed, will not be crawled, and will not survive a screenshot.
  Anything load-bearing belongs on the page.
- **Not triggered from `cf-unit-cell` at `dense`.** SC 2.5.8.
- **It is not Carbon `HeaderPanel`** (application chrome), **not `Tooltip` or
  `DefinitionTooltip`** (hover/focus transient, a few words), **not `TabPanel`** (tabs conceal
  siblings), **not `ExpandableTile`** (in-flow expansion of its own tile), and **not `Modal`
  / `ComposedModal` / `preview__Dialog`**.

## What it deliberately cannot do

1. **It cannot obscure the grid.** No scrim, no full-bleed overlay, no `inert` background.
2. **It cannot trap focus.** `Tab` leaves. `Escape` closes.
3. **It cannot nest a third level.** No accordion, no `<details>`, no second panel, no modal
   launched from inside it.
4. **It cannot open on hover or on focus alone.** Activation only.
5. **It cannot set its own width.** No token in release 0.2.0 can express one, and none was
   invented. The layout owns the width.
6. **It cannot be the only copy of anything.** It reveals provenance; it does not store it.
7. **It cannot open two at once.**

<!-- PROPOSED-INDEX-ENTRY -->
```json
{
  "name": "cf-detail-panel",
  "level": 1,
  "status": "experimental",
  "category": "disclosure",
  "summary": "A side panel revealing provenance for one clicked cell or row while the grid stays fully visible and operable behind it. Click-to-pin, never hover. Level two of a two-level disclosure limit; nothing nests below it.",
  "variants": {
    "placement": ["right", "bottom"],
    "emphasis": ["flat", "raised"]
  },
  "tokens_used": [
    "semantic.layer.02",
    "semantic.border.strong-01",
    "semantic.text.primary",
    "semantic.text.secondary",
    "semantic.link.primary",
    "semantic.focus",
    "semantic.focus-inset",
    "spacing.01",
    "spacing.03",
    "spacing.05",
    "spacing.06",
    "typography.scale.h3",
    "typography.scale.body-sm",
    "typography.scale.caption",
    "typography.scale.code",
    "elevation.surface.flat",
    "elevation.surface.raised",
    "motion.transition.reveal.duration",
    "motion.transition.reveal.easing",
    "motion.transition.dismiss.duration",
    "motion.transition.dismiss.easing"
  ],
  "a11y": {
    "contrast": "WCAG 2.2 AA — 4.5:1 text, 3:1 non-text. Measured on palette.bone.default and semantic.layer.02: heading and body 18.838:1, metadata 7.814:1, link 7.795:1, panel edge 4.253:1 on the ground, focus ring 5.002:1 on the panel.",
    "note": "Disclosure with managed focus, NOT a dialog: no aria-modal, no inert background, no focus trap, no scrim — the grid must stay operable. Trigger carries aria-expanded and aria-controls; panel is <aside aria-labelledby tabindex='-1'> placed after the grid in DOM order. Focus moves to the panel on open and on every content change; Escape closes and returns focus to the trigger, or to the grid container if the trigger is gone. semantic.layer.02 is 1.181:1 against the ground, so the semantic.border.strong-01 edge is mandatory. semantic.overlay is forbidden: it is the modal scrim and would obscure the grid."
  },
  "when_to_use": "Level-two provenance for one selected cell or row, where the reader must keep comparing that cell to its neighbours while reading about it.",
  "when_not_to_use": "Never on hover — unreachable on touch, invisible to keyboard, and it would fire continuously across a dense grid. Never as a modal: no scrim, no aria-modal, no focus trap; if the page must be blocked, that is Carbon Modal at level 2. Never with semantic.overlay. Never with semantic.border.subtle-01 as the edge (1.708:1 on the panel surface). Never nest anything disclosable inside it — this is level two of two; overflow links out. Never the only route to load-bearing information. Not triggered from cf-unit-cell at dense (SC 2.5.8). Not Carbon HeaderPanel, Tooltip, DefinitionTooltip, TabPanel, ExpandableTile, Modal, ComposedModal or preview__Dialog.",
  "source": "CoForge L1 primitive — authored 2026-09-03 by screen-producer against tokens release 0.2.0. PROPOSAL: not promoted, no ADR. Level 1 is contested — see the spec's 'The level question'."
}
```

## Claims, labelled

- `Evidenced [ART-016 § The fourteen]`, `[ART-016 § The journey]` — the grid this panel
  serves and the cells that trigger it. Measurement citations under ADR-017.
- `Measured, this session` — every ratio and hex above, from
  `design-system/tokens/tokens.json` `$version` 0.2.0, re-derivable by `verify-contrast.py`
  in this directory.
- `Inferred from the measurements` — that the panel edge is mandatory (from 1.181:1) and that
  `semantic.border.subtle-01` cannot carry it (from 1.708:1).
- `Inferred from the requirement` — the whole focus-management sequence, the ban on hover, and
  the two-level limit. These follow from "the grid stays visible and operable" and from
  Nielsen's disclosure limit, not from any number in this document. They are the parts a
  reviewer should attack hardest, because nothing mechanical checks them.

## Assumptions

- **A-1.** A 16px root, where `spacing.06` resolves to 24 CSS px and the close button meets
  SC 2.5.8. The spacing axis is rem-only and release 0.2.0 has no px-denominated dimension
  token, so **no token can guarantee a CSS-px target size**.
- **A-2.** Every ratio is against `palette.bone.default` and `semantic.layer.02`.
  `semantic-dark` was not measured and none of these numbers transfers to it.
- **A-3.** Moving focus to the panel on **every** content change is right for both mouse and
  keyboard users. This is the most arguable decision in the document. The alternative — move
  focus only on keyboard activation — was rejected because a behaviour that differs by input
  modality cannot be reliably tested, but no user was asked and no session was observed.
- **A-4.** `spacing.01` is used as a **border width**. Release 0.2.0 has no border-width axis.
  An existing token used off-label, not an invented value.
- **A-5.** The page can give the panel a layout column. If a consuming page cannot, this
  component has no width and no fallback, because none can be written on-token.
- **A-6.** Level 1 is the right classification. Contested in the body; the reviewer decides.
