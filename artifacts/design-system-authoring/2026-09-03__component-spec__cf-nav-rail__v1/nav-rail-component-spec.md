# `cf-nav-rail` — component spec

> **THIS IS A PROPOSAL, NOT AN ENTRY.** Nothing in this document is in
> `design-system/component-index.json` and this artifact does not write to it. The only path
> into the index is promotion: explicit human approval, recorded as an ADR (CLAUDE.md, "The
> membrane"). `screen-producer` may file this; it may not promote it. Until an ADR exists,
> `<CfNavRail>` is a Gate B **blocker**, and correctly so.

**Type:** `component-spec` · **Owner:** `screen-producer` · **Date:** 2026-09-03
**Proposed level:** 1 · **Proposed status:** `experimental`
**Tokens:** release `0.2.0` — composed from, never extended.

---

## What it is

Persistent section navigation for a long analytical page. A list of the page's sections that
stays on screen, marks which section the reader is currently in, and lets them jump to any
other one. The coverage board runs to seven top-level sections and five sub-sections
`[ART-016 § The fourteen]`, which is past the point where a reader can hold the structure in
their head while scrolling.

**It navigates. That is the entire permitted behaviour.** It does not filter, sort, hide,
show, collapse, expand, reorder or select. This is not a restraint on scope; it is the
component's safety property, and it is the reason it can be used on this board at all.

## The prohibition, and why it is structural

Decision D-001 forbids any control that can conceal the eight never-profiled competitors
`[ART-016 § What this board does not do]`. Navigation and filtering look similar in a
sidebar and are opposite in effect: navigation moves the reader to data, filtering removes
data from the reader. A rail that could collapse a section would let someone produce a
screenshot of this board with the gap rows gone — and the gap rows *are* the finding.

So the prohibition is enforced by shape, not by instruction:

- Every item is a real `<a href="#section-id">`. An anchor cannot hide anything; it can only
  move the viewport.
- There is no state to persist. No `expanded`, no `selected`, no `checked`, no `hidden`.
  `aria-current` is set by scroll position and is read-only to the user.
- **It is not a tab set.** Tabs show one panel and conceal the rest. On a page whose headline
  finding is what is missing, a tab set is D-001's defect wearing navigation's clothes. If
  someone asks for tabs here, this paragraph is the answer.
- Sub-sections are always visible. Two levels of depth, both rendered, neither collapsible.

## Deep links

A stakeholder needs to send a colleague straight to one section. That requires three things,
all of which are contract, not enhancement:

1. Every target section carries a stable `id`, and every rail item is `<a href="#id">`. The
   URL in the address bar is the shareable link. Right-click → copy link address works with
   no JavaScript and no application code.
2. Every target sets `scroll-margin-top: spacing.09`, so a section arrived at by hash lands
   below any sticky header rather than underneath it. Without this the deep link works and
   the reader still cannot see the heading they were sent to.
3. On load, the rail reads `location.hash` and marks that item current **before** scrollspy
   initialises — otherwise a deep link arrives with nothing marked and the reader has lost
   their place in the structure at the exact moment they were given it.

**Scrollspy is progressive enhancement.** With JavaScript disabled the rail still lists every
section and still navigates to all of them; it simply marks nothing as current. Navigation
never depends on script.

## Token resolution

| Token | Resolves to | Y |
|---|---|---|
| `palette.bone.default` | `#eeece6` | 0.838812 |
| `semantic.layer.01` | `#f4f4f4` | 0.904661 |
| `semantic.layer.selected-01` | `#e0e0e0` | 0.745404 |
| `semantic.border.strong-01` | `#6f6f6f` | 0.158961 |
| `semantic.border.subtle-01` | `#c6c6c6` | 0.564712 |
| `semantic.text.primary` | `#041222` | 0.005739 |
| `semantic.text.secondary` | `#525252` | 0.084376 |
| `semantic.link.primary` | `#0043ce` | 0.084705 |
| `semantic.focus` | `#0f62fe` | 0.159927 |
| `semantic.focus-inset` | `#ffffff` | 1.000000 |

## Measured contrast

The rail sits on `semantic.layer.01`, which sits on the page ground `palette.bone.default`.
Floors: **4.5:1** text (SC 1.4.3), **3:1** non-text (SC 1.4.11).

| A | B | Ratio | Floor | Verdict |
|---|---|---|---|---|
| `semantic.layer.01` | `palette.bone.default` | **1.074:1** | — | the rail has **no visible edge** on the ground |
| `semantic.border.strong-01` | `palette.bone.default` | **4.253:1** | 3:1 non-text | PASS — the rail's edge, and it is required |
| `semantic.border.strong-01` | `semantic.layer.01` | **4.569:1** | 3:1 non-text | PASS |
| `semantic.border.subtle-01` | `palette.bone.default` | **1.446:1** | 3:1 non-text | **FAIL — forbidden as the rail edge** |
| `semantic.text.secondary` | `semantic.layer.01` | **7.104:1** | 4.5:1 text | PASS — idle item |
| `semantic.text.primary` | `semantic.layer.01` | **17.127:1** | 4.5:1 text | PASS — current item and current bar |
| `semantic.link.primary` | `semantic.layer.01` | **7.087:1** | 4.5:1 text | PASS — available, not used by default |
| `semantic.layer.selected-01` | `semantic.layer.01` | **1.200:1** | 3:1 non-text | **FAIL — the reason "current" is not a background** |
| `semantic.focus` | `semantic.layer.01` | **4.548:1** | 3:1 non-text | PASS — outer focus ring |
| `semantic.focus-inset` | `semantic.focus` | **5.002:1** | 3:1 non-text | PASS — inner focus ring |

Two of these determined the design.

**The rail has no edge of its own.** `semantic.layer.01` against the page ground is
**1.074:1** — a difference of about one part in fifteen of a contrast ratio. A rail drawn as
a tinted surface is, on bone, not drawn at all. It therefore carries an explicit
`spacing.01` border in `semantic.border.strong-01` (4.253:1 against the ground). This is not
decoration: without it there is no boundary between navigation and content, and a reader
cannot tell the rail is a rail.

**"Current" cannot be a background.** `semantic.layer.selected-01` against
`semantic.layer.01` is **1.200:1**. The obvious implementation — highlight the current item
with the selected surface — produces a highlight nobody can see. The current item is
therefore marked on three channels, only one of which is colour:

1. a `spacing.01` bar along the leading edge, in `semantic.text.primary` (17.127:1),
2. `typography.weight.semibold` instead of regular,
3. `aria-current="location"`, which is what assistive technology actually announces.

Any one of the three alone would be a single point of failure. Weight alone is weak at
`typography.scale.body-sm`; a bar alone is invisible in forced-colors if it is drawn as a
background; `aria-current` alone is silent to a sighted reader.

## Variants

| Prop | Values | Notes |
|---|---|---|
| `placement` | `left` · `right` | The current-item bar sits on the leading edge and follows placement. |
| `sticky` | `true` · `false` | `true` = the rail stays in view while the page scrolls. `false` = it scrolls away, for short pages and for print. |
| `depth` | `1` · `2` | One level, or top-level plus sub-sections. Both levels are **always rendered**; `2` is not a tree and has no disclosure. |

There is no `collapsed` variant, and there will not be one.

## Accessibility contract

- **Structure** — `<nav aria-label="Sections">` wrapping an ordered list of anchors. It is a
  navigation landmark, so a screen-reader user can jump to it and skip past it. The label is
  required: a page with more than one `<nav>` and no labels gives the user a list of
  identical landmarks.
- **SC 1.4.3 Contrast (Minimum)** — idle items 7.104:1, current item 17.127:1. Both over 4.5:1.
- **SC 1.4.11 Non-text Contrast** — the rail edge 4.253:1 against the ground; the current bar
  17.127:1; the focus ring 4.548:1. The `semantic.layer.01` surface itself is 1.074:1 and is
  explicitly **not** load-bearing, which is why the edge exists.
- **SC 1.4.1 Use of Colour** — current state is carried by weight and a bar and
  `aria-current`, not by colour alone.
- **SC 2.5.8 Target Size (Minimum)** — every item has `min-height: spacing.06` (24px at a
  16px root), meeting the 24×24 minimum. The full item width is the target, not just the text.
- **SC 2.4.1 Bypass Blocks** — the rail *is* a bypass mechanism, and it does not replace a
  skip link. A page still needs one.
- **Keyboard** — anchors in DOM order, one `Tab` stop each. No roving `tabindex`, no arrow-key
  hijacking: this is a list of links, not a widget, and making it a widget would remove
  behaviour keyboard users already have.
- **Focus** — two-tone, `semantic.focus` outward (4.548:1 on the rail surface) and
  `semantic.focus-inset` inward (5.002:1 against the outer ring). Never suppressed.
- **SC 2.4.11 Focus Not Obscured (Minimum)** — when `sticky` is `true` the rail must not
  overlap the focused element in the content area. `scroll-margin-top: spacing.09` on section
  targets is part of this, not only of the deep-link behaviour.
- **Motion** — the current-marker transition uses `motion.duration.fast.02` (110ms) with
  `motion.easing.standard.productive`. Under `prefers-reduced-motion: reduce` the transition
  is removed **and** `scroll-behavior` returns to `auto`, so a hash jump is instant rather
  than a smooth scroll. Smooth scrolling is a vestibular trigger and is never the default for
  a reader who has asked for less motion.
- **Print** — `sticky` is ignored; the rail prints once, in place, as a table of contents.

**Not checked here, and not claimed:** any render, any screen-reader pass, any keyboard walk,
any forced-colors render, any zoom or reflow behaviour. This spec has no rendering or AT
tooling. Skipped is not passed.

## When to use

A single long analytical page with four or more sections that a reader will scroll through
and want to return to, and that a stakeholder will want to link a colleague into.

## When NOT to use

- **Never to filter, sort, hide or show data.** D-001. A control that can conceal the eight
  unprofiled competitors is a defect, not a feature `[ART-016 § What this board does not do]`.
- **Never as a tab set.** Tabs conceal every panel but one.
- **Not for site-level navigation** between documents. This is within-page only. Cross-page
  navigation is Carbon `SideNav` at level 2, and it is a different problem with different
  rules.
- **Not for fewer than four sections.** Below that the rail costs more attention than it saves
  and the headings do the job.
- **Never with `semantic.border.subtle-01`** as the rail edge: 1.446:1 on the ground.
- **Never with `semantic.layer.selected-01`** as the current-item highlight: 1.200:1 on the
  rail surface. This is the single most likely wrong implementation, because the token's name
  says exactly what a developer is looking for.
- **Not deeper than two levels.** Three levels needs disclosure, disclosure means collapsing,
  and collapsing means hiding.
- **It is not Carbon `SideNav` / `SideNavMenu`** (level 2; `SideNavMenu` is collapsible, which
  is the prohibited behaviour), **not `Breadcrumb`** (position in a hierarchy, not sections of
  a page), **not `TreeView`** (expand/collapse), **not `PaginationNav`** (between pages of a
  set), and **not `HeaderNavigation`**.

## What it deliberately cannot do

1. **It cannot hide anything.** No collapse, no filter, no show/hide. There is no prop for it.
2. **It cannot hold state.** Nothing the user does to the rail persists, because there is
   nothing to persist. `aria-current` is derived from scroll position.
3. **It cannot be a tab set.**
4. **It cannot reorder the page.** The rail's order is the document's order, always. A rail
   that could re-sort sections would let a reader see a different document from the one that
   was approved.
5. **It cannot work without stable section `id`s.** If a section has no `id` it cannot be
   linked to, and a rail item pointing at nothing is worse than no rail item. Missing `id`s
   are a build error, not a graceful degradation.
6. **It cannot exceed two levels.**

<!-- PROPOSED-INDEX-ENTRY -->
```json
{
  "name": "cf-nav-rail",
  "level": 1,
  "status": "experimental",
  "category": "navigation",
  "summary": "Persistent within-page section navigation for a long analytical document, with scrollspy and anchored deep links. Navigates only — it cannot filter, sort, collapse or hide, so it can never conceal missing data.",
  "variants": {
    "placement": ["left", "right"],
    "sticky": ["true", "false"],
    "depth": ["1", "2"]
  },
  "tokens_used": [
    "semantic.layer.01",
    "semantic.border.strong-01",
    "semantic.text.primary",
    "semantic.text.secondary",
    "semantic.focus",
    "semantic.focus-inset",
    "spacing.01",
    "spacing.02",
    "spacing.03",
    "spacing.04",
    "spacing.05",
    "spacing.06",
    "spacing.09",
    "typography.scale.body-sm",
    "typography.weight.semibold",
    "motion.duration.fast.02",
    "motion.easing.standard.productive"
  ],
  "a11y": {
    "contrast": "WCAG 2.2 AA — 4.5:1 text, 3:1 non-text. Measured on palette.bone.default and semantic.layer.01: idle item 7.104:1, current item 17.127:1, rail edge 4.253:1 on the ground, focus ring 4.548:1 on the rail.",
    "note": "The rail surface is 1.074:1 against the ground and has no visible edge of its own — the semantic.border.strong-01 edge is mandatory, not decorative. Current state is NEVER a background: semantic.layer.selected-01 is 1.200:1 on semantic.layer.01. It is marked by a spacing.01 leading bar, typography.weight.semibold and aria-current='location'. Items are plain anchors in DOM order, one Tab stop each; scrollspy is progressive enhancement and navigation never depends on script. Under prefers-reduced-motion the transition is removed and scroll-behavior returns to auto."
  },
  "when_to_use": "One long analytical page with four or more sections a reader will scroll through, return to, and want to deep-link a colleague into.",
  "when_not_to_use": "Never to filter, sort, hide or show data (D-001) — a control that can conceal missing rows is a defect. Never as a tab set: tabs conceal every panel but one. Not for cross-page navigation (that is Carbon SideNav at level 2). Not below four sections. Never with semantic.border.subtle-01 as the edge (1.446:1) or semantic.layer.selected-01 as the current highlight (1.200:1). Not deeper than two levels — a third needs disclosure, and disclosure means hiding. Not Carbon SideNav, SideNavMenu, Breadcrumb, TreeView, PaginationNav or HeaderNavigation.",
  "source": "CoForge L1 primitive — authored 2026-09-03 by screen-producer against tokens release 0.2.0. PROPOSAL: not promoted, no ADR."
}
```

## Claims, labelled

- `Evidenced [ART-016 § The fourteen]`, `[ART-016 § What this board does not do]` — the
  board's section count, and D-001, the decision that no control may conceal the eight
  unprofiled competitors. Measurement citations under ADR-017.
- `Measured, this session` — every ratio and hex above, from
  `design-system/tokens/tokens.json` `$version` 0.2.0, re-derivable by `verify-contrast.py`
  in this directory.
- `Inferred from the measurements` — that the rail edge is mandatory (from 1.074:1); that
  the current item cannot be a selected background (from 1.200:1); that the focus ring must
  be two-tone (from the ring/surface pair).
- `Inferred from the prohibition` — that this cannot be a tab set, cannot exceed two levels
  and cannot hold state. These follow from D-001, not from a measurement, and are labelled
  separately so a reviewer can argue with them on their own terms.

## Assumptions

- **A-1.** A 16px root, which is where `spacing.06` resolves to 24 CSS px and the item target
  meets SC 2.5.8. The spacing axis is rem-only; release 0.2.0 has no px-denominated dimension
  token, so **no token can guarantee a CSS-px target size**. Reported as a gap.
- **A-2.** `spacing.09` (3rem / 48px) is enough `scroll-margin-top` to clear a sticky header.
  That depends on the header, which this component does not own. If a page's header is
  taller, the page must set more — and this spec cannot express "taller" on-token, because
  the next step up, `spacing.10`, is 4rem and the choice is not measurable from here.
- **A-3.** Every ratio is against `palette.bone.default` and `semantic.layer.01`.
  `semantic-dark` was not measured.
- **A-4.** `spacing.01` is used as a **border width** for the rail edge and the current bar.
  Release 0.2.0 has no border-width axis. An existing token used off-label, not an invented
  value; the human at promotion should decide whether a `border.width.*` axis is owed first.
- **A-5.** Scrollspy is assumed to be implementable with `IntersectionObserver`. No
  implementation exists and none was written; this spec describes behaviour, not code.
