# Token axes proposal — spacing, typography, elevation, motion

**Status: SCRATCH. Proposal only — Gate A (suggest-only). No file outside this one was
touched.** `design-system/tokens/tokens.json` was read but not written.
Author: `token-keeper`, 2026-08-27.

**Task.** ADR-011 says the base is "CoForge brand theme layered over Carbon structural
tokens." Colour landed (666 leaves, all `$type: color`). Spacing, typography, elevation
and motion do not exist in `tokens.json` at all. This document establishes, against the
actual published Carbon packages, what exists to import, what does not, and what CoForge
must author — then proposes the DTCG shape.

---

## 0. Method — what was actually checked

No assumption below is carried from ADR-011 or NOTICE without re-verification. For each
package: fetched the npm registry metadata, downloaded the published tarball (`npm pack`
equivalent via the registry `dist.tarball` URL), and listed + inspected its contents
directly. This is the same artefact `npm install` would place on disk — not the GitHub
source tree, which can differ from what ships.

Packages fetched and inspected (exact published versions, 2026-08-27):

| Package | Version resolved | Tarball inspected |
|---|---|---|
| `@carbon/layout` | 11.58.0 | yes — full file listing + `src/tokens.ts` + generated SCSS |
| `@carbon/type` | 11.66.0 | yes — full file listing + `_scale.scss`, `_font-family.scss`, `_styles.scss`, compiled `es/index.js` |
| `@carbon/motion` | 11.51.0 | yes — full file listing + `src/dtcg/motion.json`, `src/dtcg/surfaces.json` (opened in full) |
| `@carbon/themes` | 11.80.0 | yes — full file listing, `src/dtcg/README.md`, `src/dtcg/white.json`, `src/dtcg/g100.json`, `src/dtcg/color-palette.json`, `src/dtcg/components/button.json` |
| `@carbon/styles` | 1.114.0 | yes — full file listing + `scss/utilities/_box-shadow.scss` |
| `@carbon/elements`, `@carbon/grid` | resolved, not needed | registry metadata only — `@carbon/elements` re-exports the above; `@carbon/grid` has no `main`/`module`, layout-only, no token content |

**What I could not verify:** GitHub's code-search API (`api.github.com/search/code`)
returned no usable result unauthenticated, so I did not cross-check against the live
`carbon-design-system/carbon` monorepo source tree directly — only against what npm
actually publishes. For a "does CoForge import this" question the published package is
the correct artefact to check (it is what an install would pull), so I don't consider
this a material gap, but it means I have not separately confirmed the monorepo's
`main` branch matches 11.80.0 byte-for-byte. NOTICE cites `@carbon/themes 11.79.0`; the
current npm `latest` is `11.80.0` — a one-patch drift since Wave 0, not investigated
further here (not this task's job to bump it).

Note on `@carbon/themes`'s own claim, quoted verbatim from `src/dtcg/README.md`: *"All
Carbon themes and component tokens have been migrated to this industry-standard
[DTCG] format."* That sentence is about **colour only** — see §1. It does not extend to
layout, type or motion packages, which live in separate npm packages with separate
release cadences and, as shown below, separate levels of DTCG adoption.

---

## 1. Does Carbon publish DTCG for the non-colour axes? (Q1)

Checked by direct file inspection, not inference from package names or READMEs.

| Axis | Package | `src/dtcg/*.json` present? | What actually ships | `$type`s found |
|---|---|---|---|---|
| **Colour** | `@carbon/themes` 11.80.0 | **Yes** — `color-palette.json`, `white.json`, `g10.json`, `g90.json`, `g100.json`, `components/*.json` | Native DTCG, schema-validated at build (`ajv` against `tr.designtokens.org/format/schema.json` per the package's own README) | `color` only — checked `white.json`, `color-palette.json`, `components/button.json` exhaustively; no other `$type` appears in any of them |
| **Spacing** | `@carbon/layout` 11.58.0 | **No** — zero `dtcg` path in the tarball | `src/tokens.ts` (a bare array of token *names*, no values), `scss/_spacing.scss` / `scss/generated/_spacing.scss` (Sass `!default` variables + a Sass map), compiled `es/index.js`/`lib/index.js`. Values only exist as Sass/JS. | none — not DTCG at all |
| **Typography** | `@carbon/type` 11.66.0 | **No** — zero `dtcg` path in the tarball | `scss/_scale.scss` (a **formula**, `get-type-size($step)`, not a value table — the 23-step ramp is computed at Sass compile time), `scss/_font-family.scss` (Sass map of font stacks), compiled `es/index.js` exposing `fontWeights = {light:300, regular:400, semibold:600}`, `scss/_styles.scss` (54 named composite styles: font-size + font-weight + line-height + letter-spacing, keyed to `heading-01`…`heading-07`, `body-01`, `code-01`, `expressive-heading-*`, `productive-heading-*`, etc.) | none — not DTCG at all |
| **Elevation** | `@carbon/themes` (colour), `@carbon/styles` (recipe) | **Partial, and misleading if read as "elevation is covered."** `white.json`/`g100.json` DTCG *does* include a `shadow` group — but it is `$type: color` only (`semantic.shadow`, `semantic.ai.inner-shadow`, `semantic.ai.drop-shadow`, plus two AI popover-shadow colours). There is **no DTCG `shadow` composite token anywhere in any Carbon package** — no offset, blur or spread is expressed in DTCG at all. The actual box-shadow recipe lives in `@carbon/styles/scss/utilities/_box-shadow.scss`: `box-shadow: 0 2px 6px theme.$shadow;` — a single hardcoded Sass mixin, not a token of any format. | `color` only, and only for the shadow's *tint*, not its geometry |
| **Motion** | `@carbon/motion` 11.51.0 | **Yes** — `src/dtcg/motion.json` and `src/dtcg/surfaces.json`, opened and read in full | Native DTCG. `motion.json`: 6 `duration` tokens (`fast.01/02`, `moderate.01/02`, `slow.01/02`, 70–700ms) and 6 `cubicBezier` tokens under `easing.{standard,entrance,exit}.{productive,expressive}`. `surfaces.json`: composite `transition` tokens (non-standard `$type`, a Carbon extension) that alias the primitives above, e.g. `surface.disclosure.$value.duration = "{duration.moderate.01}"`. | `duration`, `cubicBezier` (both are real DTCG-spec types) — plus a Carbon-only `transition` `$type` that is not in the DTCG spec proper but is structured as a valid composite alias object |

**Answer to Q1, stated plainly:** Carbon publishes real, native, schema-validated DTCG
for exactly **two** of the five axes CoForge needs — **colour** (already imported) and
**motion**. **Spacing and typography are not published as DTCG at all** — they exist
only as Sass source, a Sass-compiled formula, or compiled JS, and importing them
requires conversion (running the Sass/JS and capturing the resolved values), not a file
copy. **Elevation is a false positive if checked carelessly** — the *colour* half of
elevation is DTCG (already sitting in `tokens.json` as `semantic.shadow`), but the
*geometry* half (the numbers that make it a shadow rather than a colour) is not
published in any machine-readable token format — it's one line of hardcoded Sass.

---

## 2. Import, author, or import-then-override? (Q2)

Per-axis, not blanket, as instructed.

### Spacing — **import, with conversion**

Carbon's spacing scale (`spacing-01`…`spacing-13`: 0.125rem → 10rem, an 8px-adjacent
geometric-ish progression) is a structural, unopinionated numeric scale — exactly the
kind of thing ADR-011 assigns to Carbon ("structural tokens") and exactly the kind of
thing brand.md never touches: §2 and §4 argue about *type*, *form*, *density* and
*colour*, and never once argues for a different spacing cadence. There is no brand
signal in "how many rem apart two elements sit." Import it.

But it cannot be a file copy, because no DTCG file exists (§1). The values must be
**extracted from the compiled Sass** (`scss/generated/_spacing.scss`, which is itself
machine-generated by Carbon's own build and therefore a legitimate primary source) and
hand-converted into DTCG `dimension` leaves. This is the one place in this proposal
where "import" means *transcribe verified values*, not *copy a file* — flagged so
nobody mistakes a future PR that types out 13 numbers for an act of authorship. The
values themselves are Carbon's; only the DTCG wrapper is new.

One open mismatch, not resolved here: `component-index.json`'s `spacing-scale` entry
already declares `variants.steps: ["01".."10"]` — **10** steps — while Carbon ships
**13** (plus 4 fluid-spacing and 5+ container/icon sizes CoForge likely doesn't need at
all). Whether CoForge imports all 13 core steps and the index is simply behind, or the
index is right and Carbon's top 3 steps (`spacing-11/12/13`, 5–10rem) are out of scope,
is a token-keeper decision to make when this is promoted — noted, not resolved, because
resolving it means touching `component-index.json`, which is out of scope for this
document.

### Typography — **author, informed by Carbon's numbers, not by Carbon's scale**

Not a blanket "author everything from zero." Specifically:

- **Font-size ramp: author.** Carbon's 23-step formula-generated scale (12px → 156px,
  computed via `get-type-size()`) has no natural stopping points that match brand.md
  §4's demand for **one scale, used at two densities** ("stage" and "document") rather
  than a long undifferentiated ramp. Carbon itself does not even use its own ramp as a
  flat scale — see below.
- **Font-weight range: author, because Carbon's is too narrow.** Carbon exposes exactly
  three weights — `light 300`, `regular 400`, `semibold 600` (verified in compiled
  `es/index.js`). Brand.md §4 requires the display treatment at **weight 700** ("heavy")
  and requires weight, not size, to carry hierarchy — Carbon's ceiling is 100 units
  short of the weight the brand's loudest gesture is built on. Importing Carbon's set
  would make the brand's own display treatment unreachable inside the token system.
- **Tracking: author the curve; do not import Carbon's stepped table.** See §3 — this
  is the sharpest, most evidenced divergence, argued fully there.
- **Font family: neither.** Out of scope per this task's "not your job" — OQ-2 in
  brand.md is unresolved and this proposal does not pick a body face. The DTCG shape in
  §4 is built so either outcome (Anek Latin lighter weights, or IBM Plex Sans, or a third
  candidate) slots in without restructuring anything above the primitive layer.

### Elevation — **author the geometry; alias the colour that already exists**

The colour component of elevation is already correctly in `tokens.json`
(`semantic.shadow`, `semantic-dark.shadow`, both proper `{black.default}` aliases with
an `alphaModifier` extension — 0.3 light, 0.8 dark). That does not need re-doing.

The geometry — offset, blur, spread — has no Carbon token to import at all (§1); the
only artefact is one line of Sass (`0 2px 6px theme.$shadow`). Given there is nothing to
import, and brand.md §2 is explicit and specific ("Elevation is expressed as a single
soft shadow... not more than one depth at a time"), author a **single** elevation
recipe. Carbon's own numbers (`2px` y-offset, `6px` blur, `0` spread) are a reasonable
starting point to test against the brand's warmer, softer visual language (§2: "soft
shadow", pill/rounded forms) — reusing Carbon's geometry is not the same claim as
reusing Carbon's *token*, because no such token exists to alias. Treat the two numbers
as a proposal to verify visually, not as an import.

### Motion — **import, with one restriction to test**

This is the one axis where Carbon ships real DTCG (§1) *and* the content survives a
brand check on inspection. The duration ladder (70ms–700ms) is unopinionated and
structural — no brand signal in "how many milliseconds." The easing curves are the part
worth checking, because they could carry unwanted character: I read all six
`cubicBezier` control points and none produces overshoot or bounce (all four control
values sit within `[0, 1]`, e.g. standard-productive `[0.2, 0, 0.38, 0.9]`,
standard-expressive `[0.4, 0.14, 0.3, 1]` — a cubic-bezier needs a control point outside
`[0,1]` to overshoot past its end value, and none do). That is directly consistent with
brand.md §5's "no bounce, no overshoot, no elastic."

The restriction to test: Carbon ships **two parallel families**, `productive` and
`expressive`, at every duration/easing pair. `expressive` decelerates harder and is
described in Carbon's own docs as suited to being noticed. Brand.md §5 is emphatic that
"motion confirms; it does not perform" and "anything whose purpose is to be noticed is
off-brand" — which reads as a vote for `productive` as CoForge's default surface, with
`expressive` either excluded from the CoForge alias set entirely or kept as an
unaliased, unused-by-default import (present in the mirror, absent from anything an
agent is told to reach for). This is a theming decision at the semantic layer, not a
reason to author new primitives — the values themselves import cleanly.

---

## 3. Where brand.md forces a departure from Carbon (Q3)

Three specific, evidenced points — not a general "Carbon is IBM-flavoured" hand-wave.

**1. Carbon itself ships two competing type systems, which is the exact failure brand.md
names.** `_styles.scss` defines both a `productive-heading-XX` and an
`expressive-heading-XX` family at several of the same nominal steps, with **different
weight and different letter-spacing at the same font-size** (e.g. both a productive and
expressive `heading-07`, one `regular`/0 tracking, the other differently weighted).
Brand.md §4 was written against a different instance of exactly this problem — the
coforge.com site's numeric-ramp-vs-`h1`–`h5` mismatch — and states the rule generally:
*"a name that does not determine a value"* is the failure mode, and *"one scale, not
two."* Importing Carbon's productive/expressive pairing wholesale reintroduces the
named problem with IBM's naming instead of coforge.com's. **Departure: CoForge's
`type-scale` primitive (already registered in `component-index.json` with 8 levels —
`display, h1, h2, h3, body, body-sm, caption, code`) is the only legal name set. Carbon's
productive/expressive split does not surface as a CoForge-facing choice; if it is used
internally at all it collapses to one family per level, decided once, not exposed as a
per-use decision.**

**2. Carbon's negative tracking starts far later than the brand's does.** Reading
`_styles.scss` in full: letter-spacing across Carbon's scale runs positive at the small
end (`0.32px`/`0.16px` at scale steps 1–2, roughly 12–14px), settles to `0` through the
entire middle of the ramp (steps 3 through roughly 13, i.e. 16px through 60px — this
covers essentially all of CoForge's document register and most plausible stage
headings), and only goes negative (`-0.64px`, `-0.96px`) at the top two
`expressive`/`productive` display styles, which correspond to scale steps in the ~17–23
range (92px and up, per the computed ramp in §0's method — I calculated all 23 steps
from the published formula to confirm this: step 17 = 92px, step 23 = 156px). The
brand's evidenced display signal is **`-0.125rem` (`-2px`) tracking at 62px**
(`Evidenced [ART-005 § Type]`, per brand.md §4) — a size that sits at roughly scale step
13 in Carbon's own ramp, squarely inside the region where Carbon's letter-spacing is
still `0`. **Departure: brand.md's rule that "tracking tightens as size grows and
relaxes to normal... at small sizes" needs a curve that starts contracting well below
where Carbon's stepped table does, or the display register's most-evidenced signal
(negative tracking at 62px) is unreachable by importing Carbon's numbers as-is.**

**3. Weight ceiling, restated with the number.** Carbon's heaviest defined weight is
`600` (semibold). Brand.md §4 states the display treatment is `700`, evidenced from the
artefact, and states weight (not size) should carry hierarchy generally — which requires
headroom above 600 to be usable across the document register too, not just at the one
display instance. **Departure: the weight axis needs a value Carbon does not define.**

**The override surface, concretely:** none of this blocks importing Carbon's numeric
*font-size* ramp as raw material (§2 — author is about the curated stopping points, not
about inventing new pixel values from nothing); it blocks importing Carbon's
*font-weight* set and *tracking* table as-is. The override surface is therefore narrow
and nameable: a CoForge-authored `weight` primitive group (adds at minimum a `700`
value Carbon doesn't have) and a CoForge-authored `tracking` function/table keyed to
`type-scale` level rather than to Carbon's raw step number, front-loading the negative
values several steps earlier than Carbon's own table does. Both are new primitive
leaves, not repoints of existing Carbon leaves — this is exactly the "import vs author"
split argued per-axis in §2, made concrete for typography specifically.

---

## 4. Proposed DTCG structure (Q4)

Consistent with the existing `palette` → `semantic` pattern (primitive layer holds
literals with full DTCG value objects; every layer above it holds `{alias}` strings
only — the binding constraint restated from the task). Real, existing paths referenced
throughout; new paths are marked **NEW**.

```
tokens.json
├── palette            (existing — 244 literal colour leaves, unchanged by this proposal)
├── semantic            (existing — colour aliases, unchanged)
├── semantic-dark        (existing — colour aliases, unchanged)
├── spacing              NEW — primitive layer, dimension literals
│   └── 01 … 13           $type: dimension, imported+converted from Carbon (§2)
├── typography           NEW — two sub-groups, primitive + semantic, inside one top-level key
│   ├── size               primitive — $type: dimension, curated stopping points (§2/§3)
│   │   └── 01 … NN
│   ├── weight              primitive — $type: fontWeight, CoForge-authored set incl. 700 (§3)
│   │   └── light / regular / semibold / heavy
│   ├── tracking             primitive — $type: dimension, CoForge-authored curve (§3)
│   │   └── 01 … NN          — same index cardinality as `size`, paired 1:1
│   ├── family                deferred — OQ-2 (body face undecided); see cardinality note below
│   │   └── display / body    both $type: fontFamily, `display` already decided (Anek Latin, brand.md §4); `body` a placeholder alias target only
│   └── scale               semantic — the only layer `type-scale` (component-index.json) may read
│       ├── display           {typography.size.NN} + {typography.weight.heavy} + {typography.tracking.NN} + {typography.family.display}
│       ├── h1 / h2 / h3       likewise, each a named bundle of primitive aliases
│       ├── body / body-sm      likewise, weight → {typography.weight.regular}
│       ├── caption / code       likewise
├── elevation             NEW — primitive + semantic, small
│   ├── shadow              primitive — $type: shadow (DTCG composite: color/offsetX/offsetY/blur/spread)
│   │   ├── none              $value: [] (empty layer array — DTCG's documented way to express "no shadow")
│   │   └── raised            $value: { color: "{semantic.shadow}", offsetX: 0, offsetY: {dimension}, blur: {dimension}, spread: 0 }
│   └── surface              semantic — the only layer `card`'s `elevation` variant may read
│       ├── flat               {elevation.shadow.none}
│       └── raised             {elevation.shadow.raised}
└── motion                NEW — primitive + semantic, mirrors Carbon's own two-tier shape
    ├── duration            primitive — $type: duration, imported from Carbon (§2)
    │   └── fast-01/02, moderate-01/02, slow-01/02
    ├── easing               primitive — $type: cubicBezier, imported from Carbon (§2)
    │   └── standard / entrance / exit, each with only `.productive` imported by default (§2's restriction); `.expressive` mirrored but not aliased-to
    └── transition           semantic — composite, named by intent, the only layer a component may read
        └── e.g. reveal, dismiss, confirm — each aliasing one {motion.duration.*} + one {motion.easing.*.productive}
```

**Alias direction, stated once so it isn't ambiguous:** every leaf under a *semantic*
group (`typography.scale.*`, `elevation.surface.*`, `motion.transition.*`, and the
existing `semantic.*`/`semantic-dark.*`) is a `{primitive.path}` alias string only.
Every leaf under a *primitive* group (`spacing.*`, `typography.size/weight/tracking/
family.*`, `elevation.shadow.*`, `motion.duration/easing.*`, and the existing
`palette.*`) holds a full DTCG value object. Nothing above the primitive layer holds a
number — the binding constraint holds for all four new axes exactly as it holds for
colour today.

**Stage vs document, without duplicating the scale (Q4's specific ask):** brand.md §2 is
explicit that the two registers "differ in space and type scale only, never in colour
role or shape language" and share everything else. The structure above gives them a
*third* group rather than doubling `typography.scale` and `spacing`:

```
├── density              NEW — semantic, two named registers, no new primitives
│   ├── stage
│   │   ├── type-scale     which {typography.scale.*} levels a stage surface may draw from — e.g. permits display/h1/h2, withholds caption/code
│   │   └── spacing-unit   which {spacing.*} step is "one unit" at this density — e.g. {spacing.07}
│   └── document
│       ├── type-scale     the same {typography.scale.*} set, restricted differently — e.g. withholds display, permits caption/code
│       └── spacing-unit   {spacing.03} or similar — a tighter default unit
```

This avoids duplicating the ramp: `density.stage.type-scale` and
`density.document.type-scale` are not two different scales, they are two different
*subsets/defaults* pointing at the one shared `typography.scale` semantic group — which
is the literal DTCG expression of brand.md's "differ in space and type scale only"
sentence, and keeps `type-scale`'s registered `component-index.json` contract
(`tokens_used: ["typography.*"]`) satisfied without a second component.

**Naming note on `typography.family`:** cardinality is deliberately left open at exactly
one place — `family.body` — so that whichever candidate wins OQ-2 (Anek Latin's lighter
weights, or IBM Plex Sans, or a third option) lands as a single value swap at that one
leaf, with zero restructuring above it. `family.display` is not deferred; brand.md §4
already names Anek Latin as decided for display.

---

## 5. The four literal leaks (Q5)

Verified directly against the live `tokens.json` (read-only), and cross-checked against
Carbon's own upstream `@carbon/themes` 11.80.0 source to establish where the fault
actually originates:

| Leaf | `$value` (light) or path | Hex |
|---|---|---|
| `semantic.ai.popover-caret-center` | literal colour object | `#a0c3ff` |
| `semantic.ai.popover-caret-bottom-background` | literal colour object | `#eaf1ff` |
| `semantic.ai.popover-caret-bottom-background-actions` | literal colour object | `#e9effa` |
| `semantic-dark.ai.popover.caret.center` | literal colour object | `#4870b5` |

**Root cause, established, not assumed:** these are not artefacts of CoForge's own
extraction. I opened Carbon's own `src/dtcg/white.json` and `src/dtcg/g100.json`
directly (§0) and found the identical literal objects there, under the identical
descriptions ("AI popover caret center", "Center color for AI popover caret gradient —
creates the vibrant middle of the gradient pointer"). **Carbon's own upstream DTCG
breaks Carbon's own alias convention for exactly these four leaves.** They are described
as gradient stops for a popover caret, which is presumably why they were never aliased
to a ramp step — a gradient midpoint doesn't naturally correspond to one. This is a
genuine defect in IBM's published source, inherited verbatim by CoForge's extraction,
not an extraction bug.

**Fix, and what it needs:** confirmed by direct search — none of the four hex values
(`#a0c3ff`, `#eaf1ff`, `#e9effa`, `#4870b5`) matches any existing `palette.*` leaf
exactly, so **repointing to an existing palette entry is not available; this needs four
new palette entries.** Proposed: a small `palette.ai-gradient` group (or, if
token-keeper prefers to keep `palette` flat like the existing hue ramps, four
standalone leaves alongside the other ramps) holding these four values verbatim —
**unchanged from what already ships**, just relocated to the primitive layer where they
belong — and repointing the four `semantic`/`semantic-dark` leaves to
`{ai-gradient.*}` aliases. Because this creates four new `palette.*` paths that don't
exist today (even though the *values* are already live in the file, merely
misplaced), I am treating this as a **new-token action under Gate A** rather than
auto-sync, on the conservative reading that "new path in the primitive layer" is what
Gate A is checking for, not "new value nobody has seen." Token-keeper should feel free
to reclassify this as mechanical/auto if that reading is wrong — it is a straight
structural relocation of values already present, not a new design decision, and the
distinction is genuinely a judgement call I'm flagging rather than resolving unilaterally.

---

## Summary of calls, one line each

| Axis | DTCG native? | Call |
|---|---|---|
| Spacing | No (Sass/JS only) | **Import**, converted from Carbon's compiled Sass — no brand signal opposes it |
| Typography | No (Sass/JS only) | **Author**, informed by Carbon's numbers but not copying Carbon's scale, weight set, or tracking table — brand.md §4 conflicts with all three on evidence (§3) |
| Elevation | Colour half only | **Alias** the colour (already correct in `tokens.json`); **author** the geometry — nothing exists to import |
| Motion | Yes, natively | **Import**, with `expressive` mirrored but not aliased into CoForge's default semantic set, pending confirmation the "confirms, does not perform" reading of brand.md §5 is correct |

## What this document does not do

No value in `tokens.json` was added, changed, or removed. No new palette entry, no
weight value, no tracking curve, no shadow recipe, no duration or easing value was
authored here — every number named above (Carbon's spacing scale, Carbon's letter-
spacing table, Carbon's motion durations/curves, the two literal-leak hex groups) is
cited from what already exists upstream or in `tokens.json` today, not invented for this
proposal. The body face (OQ-2) is not picked. The exact `spacing.*` step count (10 vs
13, §2) is flagged, not resolved. All of it is Gate A's to accept, reject, or send back.
