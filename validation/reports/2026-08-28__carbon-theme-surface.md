# Carbon token layer — theme-surface survey

**Status: SCRATCH. Survey only. No token values changed by this document or its author.**
Produced by token-keeper, 2026-08-27, against `design-system/tokens/tokens.json` as it
stands post-Wave-0 (ADR-011 Carbon extraction). Counts below were computed by walking
the JSON tree in Python, not estimated. Method: any node with a `$value` key is a leaf;
everything else is a group.

## 1. The actual structure

Three top-level groups, **666 leaves total**, verified:

| Group | Leaves | What it is |
|---|---|---|
| `palette` | 244 | Raw Carbon color ramps. 13 hue ramps (`blue`, `coolGray`, `cyan`, `gray`, `green`, `magenta`, `orange`, `purple`, `red`, `teal`, `warmGray`, `yellow`) × 20 steps each (10–100 plus `*Hover` variants), plus `black` and `white` (2 leaves each: `default`, `Hover`). |
| `semantic` | 234 | Light-theme semantic aliases, sourced from Carbon's `white.json`. |
| `semantic-dark` | 188 | Dark-theme semantic aliases, sourced from Carbon's `g100.json`. |

**`$type` in play: exactly one — `color`. 666/666 leaves are `color`.** There are no
`dimension`, `fontFamily`, `fontWeight`, `fontSize`, `lineHeight`, `duration`, `cubicBezier`,
or shadow/composite `$type` leaves anywhere in the file. This matters directly for what
this task was asked to check: **spacing, the type scale, elevation, and motion timing —
the "structural layer" ADR-011 assigns to Carbon — are not represented in `tokens.json`
at all yet.** They exist inside the Carbon npm packages but were not part of this
extraction. `$extensions.coforge.source_files` confirms the scope actually pulled:
`color-palette.json`, `white.json`, `g100.json` — color only. Nothing to report as
"structural tokens" because none have been authored yet; this is a gap for token-keeper's
own backlog, not something brand-director needs to wait on.

`palette` leaves store fully resolved values (`colorSpace`, `components`, `hex`).
`semantic` and `semantic-dark` leaves store **DTCG alias strings** (e.g.
`"$value": "{blue.60}"`), confirmed by direct inspection — not resolved hex. The
`$extensions.coforge.note` in the file header says this is deliberate ("aliases are
preserved rather than resolved so re-theming stays possible"), and the data matches
the stated intent, with one exception noted in §3.

### Semantic subgroup breakdown (light `semantic`, leaf counts)

`ai` 21 · `background`+7 background-* singles (background, background-active,
background-brand, background-hover, background-inverse, background-inverse-hover,
background-selected, background-selected-hover) · `border` 16 · `chat` 21 · `field` 6 ·
`focus`+`focus-inset`+`focus-inverse` (3 singles) · `highlight` 1 · `icon` 7 ·
`interactive` 1 · `layer` 29 · `link` 8 · `overlay` 1 · `shadow` 1 · `skeleton` 2 ·
`support` 11 · `syntax` 88 · `text` 9 · `toggle-off` 1.

`semantic-dark` mirrors most of this (see §3 for the path-grammar catch) but is
genuinely thinner in places — dark drops `background-active`, `background-hover`,
`background-inverse`, `background-inverse-hover`, `background-selected`,
`background-selected-hover`, `background-brand`, `focus-inset`, `focus-inverse`, and
`icon.on-color` / `icon.on-color-disabled` / `text.on-color` / `text.on-color-disabled`
entirely. These look like genuine omissions in Carbon's own `g100.json`, not extraction
bugs — worth flagging but not fixing here.

## 2. The themeable surface — exact paths

**Override these (semantic layer only):**

```
semantic.background, semantic.background-active, semantic.background-brand,
semantic.background-hover, semantic.background-inverse, semantic.background-inverse-hover,
semantic.background-selected, semantic.background-selected-hover
semantic.interactive
semantic.border.interactive
semantic.icon.interactive
semantic.link.primary, semantic.link.primary-hover, semantic.link.secondary,
semantic.link.visited, semantic.link.inverse*
semantic.text.primary, semantic.text.secondary, semantic.text.helper,
semantic.text.error, semantic.text.disabled, semantic.text.placeholder,
semantic.text.inverse, semantic.text.on-color, semantic.text.on-color-disabled
semantic.support.* (error, warning, success, info, caution-* and their *-inverse pairs)
semantic.focus, semantic.focus-inset, semantic.focus-inverse
semantic.highlight
semantic.layer.accent-01/02/03, semantic.layer.accent-active-*, semantic.layer.accent-hover-*
semantic.toggle-off
semantic.chat.* (if chat surfaces ship — 21 leaves)
semantic.ai.* (if AI-flagged surfaces ship — 21 leaves, but see §3, 3 of these are broken)
```
...and the parallel `semantic-dark.*` path for every one of the above that has a dark
counterpart (see the omission list in §1 — some don't).

**Do NOT touch — structural, components depend on the raw value, not the "look":**

```
palette.*  — every ramp, every step. This is the resolved-value substrate. Overriding
             here instead of at the semantic layer breaks re-theming outright: any
             semantic alias not touched by the brand override (e.g. `semantic.support.error`
             → `{red.60}`) would silently inherit whatever the brand happens to do to
             `red.60`, because `red` is a shared Carbon hue name, not a CoForge concept.
semantic.syntax.*  (88 light + 71 dark leaves) — code-syntax-highlighting roles
             (keyword, operator, comment, string...). Not a brand-facing surface;
             recommend explicitly scoping these OUT of the brand theme rather than
             leaving them to accidentally inherit brand hues meant for UI chrome.
semantic.layer.01/02/03, .active-*, .hover-*, .selected-*, .background-01/02/03
             — surface elevation stacking, not brand color. These are Carbon's neutral
             layering system (grays), and swapping them for brand hues would break the
             "layer" mental model components are built against (a card is `layer.01`
             regardless of brand).
semantic.field.*, semantic.border.subtle-*/strong-*/tile-* — structural border/field
             roles keyed to *emphasis level*, not brand identity. These stay tied to
             the neutral ramp so hierarchy reads correctly under any theme.
```
No non-color `$type` groups exist yet to warn off (see §1) — when spacing/type-scale/
elevation/motion tokens are eventually extracted from Carbon, they inherit this same
"do not touch" status by the human's stated decision (Carbon keeps structural).

## 3. Primitive vs semantic — does the separation exist?

**Yes, and it is real, not decorative.** `semantic.*` and `semantic-dark.*` leaves are
DTCG alias strings pointing at `palette.*` (e.g. `semantic.text.primary` →
`"{gray.100}"`, `semantic.interactive` → `"{blue.60}"`). This is exactly the structure a
brand theme needs to attach to: repoint the alias, not the primitive. This is a
meaningfully better starting position than "the semantic layer is missing or thin" —
it is present and reasonably complete (234 + 188 leaves across background, text,
border, icon, link, support, interactive, focus, layer, field, chat, ai, syntax).

Three real problems found in it, worth naming before anyone writes an override:

1. **High fan-out on the single "brand" primitive.** `{blue.60}` is referenced by
   **21 separate `semantic.*` leaf paths** in the light theme (`semantic.interactive`,
   `semantic.background-brand`, `semantic.border.interactive`, `semantic.icon.interactive`,
   `semantic.link.primary`, `semantic.chat.avatar-user`, `semantic.chat.button`,
   `semantic.focus`, `semantic.ai.drop-shadow`, plus 12 `semantic.syntax.*` roles). Dark
   theme references the equivalent role across **28 leaf paths**, but spread over four
   different blue shades (`blue.30/40/50/60`) depending on state. **Retheming "the brand
   color" is not a one-token edit in either mode** — it is a multi-path override, and the
   light/dark shade-stepping convention (60 → 50 → 40 → 30 as theme darkens, roughly)
   has to be replicated for whatever brand hue replaces it, or hover/active states go flat.

2. **Path-grammar inconsistency between `semantic` and `semantic-dark`.** The two trees
   encode multi-part names differently. Example, verified directly:
   `semantic.border.strong-01` (single key `"strong-01"` under `border`) vs.
   `semantic-dark.border.strong.01` (nested: key `"strong"` containing key `"01"`).
   The same pattern repeats across `subtle-*`, `tile-*`, `layer.accent-*`, `chat.*`,
   `ai.*`, `syntax.*`, `field.hover-*`, `text.on-color*`, `icon.on-color*`, `toggle-off`
   vs `toggle.off`. A naive path-based override script written against one tree's shape
   will silently miss its counterpart in the other. This is a real structural defect in
   the current extraction, not a content gap — the *values* mostly exist in both modes,
   the *addressing* doesn't match. Fix this before authoring theme overrides, or before
   any Figma push (see §5).

3. **Four leaves break the alias-only contract.** `semantic.ai.popover-caret-center`,
   `semantic.ai.popover-caret-bottom-background-actions`,
   `semantic.ai.popover-caret-bottom-background` (light), and
   `semantic-dark.ai.popover.caret.center` store resolved `{colorSpace, components, hex}`
   objects directly instead of a `{ramp.step}` alias, contradicting the file's own stated
   principle. If a brand theme repoints palette-adjacent aliases, these four silently
   keep shipping Carbon blue regardless. Small in count, but exactly the kind of
   drift-immune corner that would surface as an unexplained blue smear on an AI-flagged
   surface after the theme lands.

**Verdict for the task's framing:** the semantic layer is not "missing or thin." It
exists, it's structurally sound in its aliasing design, and a brand theme has something
real to attach to. The obstacles are the fan-out (§3.1), the addressing mismatch
between light/dark (§3.2), and the four leaks (§3.3) — all fixable, none of them "start
the semantic layer from scratch."

## 4. The gap — what's missing for the Coforge brand to land as a theme

1. **No CoForge primitive ramp exists.** `palette.*` is 100% Carbon hues (blue, gray,
   cyan, etc.) — there is no `coral`, `oxford`/navy, or `taupe`/bone ramp yet. Landing
   the brand means adding new primitive ramps (with Carbon's 10–100 + `*Hover` step
   convention, so the semantic layer's aliasing pattern keeps working) *before* pointing
   any `semantic.*` alias at them. Hardcoding brand hex straight into `semantic.*`
   instead of adding primitives would repeat problem §3.3 at brand-theme scale.

2. **The text-safe accent must be a second, distinct token — not a second value of the
   same token.** Per `EXTRACTION.md`, brand coral `#f15b40` measures **2.82:1** against
   the bone ground and **3.33:1** even against white — it fails AA for body text and
   small UI labels in every context tested, and only clears AA-large by luck on the live
   CTA. Gate B checks *"is this value on-token,"* not *"does this value pass contrast
   for this usage."* If "the accent" is a single token path, an agent is free to use it
   for both a CTA fill (fine, large-scale, decorative) and a body-copy accent word or a
   small icon label (fails AA, and Gate B would not catch it — the value is on-token by
   construction, exactly the failure mode `EXTRACTION.md` already called out for the
   broken Carbon-side ramps). This needs **two leaf paths**, e.g. something like
   `semantic.background-brand` / `semantic.interactive` (full-saturation coral, for
   fills, large CTA text, illustration) and a new `semantic.text-accent` or
   `semantic.link.brand` (AA-safe dark variant, for anywhere the accent carries body
   text or a small label). `EXTRACTION.md` names `coquelicot-700 #b03822` as the nearest
   *candidate* for the safe variant — untested by a11y-checker, not decided here.

3. **`semantic.text.*` currently has no accent/brand leaf at all.** The full list is
   `disabled, error, helper, inverse, on-color, on-color-disabled, placeholder, primary,
   secondary` — Carbon's own semantic set has no "this text is brand-colored" concept to
   repoint. The AA-safe accent token in point 2 is a **new leaf**, not a redirect of an
   existing one — which puts it under Gate A (new-token, suggest-only), not the auto-sync
   path this agent otherwise has for value changes.

4. **No display-type tokens exist to carry the brand's typographic signal.**
   `EXTRACTION.md` flags CoForge's distinctive display treatment (Anek Latin, weight 700,
   `-0.125rem` tracking) as a real brand signal worth carrying — but since §1 confirmed
   zero `fontFamily`/`fontWeight`/`fontSize` leaves exist in `tokens.json` at all, there
   is nothing to override here. This has to be authored as new leaves from scratch once
   `brand.md` lands, not adjusted from a Carbon starting point.

5. **The `semantic-dark` path-grammar mismatch (§3.2) needs resolving before or during
   theming**, otherwise a script that overrides `semantic.interactive` and
   `semantic.border.strong-01` correctly in light mode will not find the equivalent dark
   leaves under the names it expects.

6. **The four raw-hex leaks (§3.3)** should be converted to aliases (or explicitly
   scoped out of the brand theme) before the override lands, or they will keep shipping
   Carbon blue silently after everything else is coral/navy.

## 5. ADR-001 implications — pre-inversion, repo still authors

We are pre-inversion (`$extensions.coforge.inversion_reached: false`, confirmed in the
file). This theming approach is soundly compatible with the eventual Figma handover in
its *design*, but three things about it will complicate that handover if not addressed
now, while the repo still has the pen:

1. **Alias fidelity across the export.** The whole theming strategy here depends on
   `semantic.*` staying a *reference* (`{blue.60}`) rather than a *resolved value*.
   Figma Variables do support aliasing one variable to another, but ADR-001's step 3
   ("push into Figma variables") and step 5 (`figma_export_tokens` → mirror) need to be
   verified to preserve that reference graph rather than flattening it to hex on either
   side of the round-trip. If the push-to-Figma step resolves aliases, the
   primitive/semantic separation this whole survey is built on disappears the moment it
   crosses into Figma, and every later mirror sync re-imports flat color with no
   brand-vs-structural distinction left to enforce.

2. **Light/dark should be one Figma variable collection with two modes, not two parallel
   trees.** Figma variable modes require a shared variable *name* across modes with a
   per-mode value — which means the `semantic` vs `semantic-dark` path-grammar mismatch
   (§3.2) must be reconciled *before* the push, not after. Pushing the two trees as-is
   would either create two unrelated variable sets in Figma (losing the light/dark
   pairing entirely) or require the push script to paper over the mismatch with guessed
   name-matching — a source of silent drift the drift-check is specifically supposed to
   prevent post-inversion.

3. **New leaves invented now (the AA-safe accent pair, display-type tokens) become
   permanent Figma variable names once pushed.** Post-inversion, this repo cannot rename
   or restructure them — it can only mirror and, per the break-glass path, propose a
   re-author as a logged incident. Naming these well *before* the v0 push (e.g. deciding
   now whether the safe accent lives at `semantic.text-accent` vs `semantic.link.brand`
   vs a new `semantic.accent-safe` group) is cheaper now than after inversion.

4. Genuine mode-only omissions found in §1 (dark theme missing `background-active`,
   `focus-inset`, `icon.on-color`, etc.) should be resolved — either backfilled or
   explicitly documented as intentional per-mode gaps — before the push, since an
   undocumented missing-in-one-mode variable looks identical to drift once the drift
   check is live.

## Not done here (by design)

No values in `tokens.json` were changed. No new primitive ramp, no accent token, no
display-type token was added. The AA-safe-accent value and the brand ramp itself are
brand-director's and a subsequent Gate A proposal's call, not this survey's.
