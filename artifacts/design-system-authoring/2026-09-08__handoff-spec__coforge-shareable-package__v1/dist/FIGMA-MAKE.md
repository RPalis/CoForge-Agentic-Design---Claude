# Rebuilding these screens in Figma Make — at 1:1

Generated 2026-09-08 from `design-system/tokens/tokens.json`
at commit `11a652f`. Every number below is read out of the token file, not transcribed,
so this brief cannot drift from the system it describes.

Paste the **Prompt** section into Figma Make, then hold the result against the
**Acceptance test** at the end. The two HTML files in this folder are the reference —
open them side by side and compare.

---

## What you are building

Two screens, one design language.

1. **Competitor analysis** — a dense evidence board. 17 competitors, 121 findings, every
   row traceable to a source file. Reference: `01-competitor-analysis.html`.
2. **Design system foundations** — the token layer as a page. Reference:
   `02-design-system-foundations.html`.

Both are **documents, not apps**. The reader is scanning and comparing, not completing a
task. Density is a feature. There is no onboarding, no empty state, no hero image.

---

## Prompt

> Build a reference document in a restrained editorial style on a warm off-white ground.
> Single accent, used only for state and emphasis — never for body text. Hairline rules,
> no shadows, no rounded corners, no gradients, no icons. Hierarchy comes from **weight and
> spacing**, not from colour or size alone. Tables are dense and left-aligned; every number
> is right-aligned and set in a monospaced face so columns align. The page should read like
> a well-set annual report, not like a SaaS dashboard.

---

## Colour — the whole palette

Three colours do almost all the work: one ground, one ink, one accent.

| Token | Value | Contrast on ground | Role |
|---|---|---|---|
| `semantic.background` | `#eeece6` | 1.00:1 | Default page background color |
| `semantic.text.primary` | `#041222` | 15.95:1 | Primary |
| `semantic.text.secondary` | `#525252` | 6.61:1 | Secondary |
| `semantic.border.subtle-01` | `#c6c6c6` | 1.45:1 | Subtle border color for layer 01 |
| `semantic.border.strong-01` | `#6f6f6f` | 4.25:1 | Strong border color for layer 01 |
| `semantic.layer.01` | `#f4f4f4` | 1.07:1 | 01 |
| `semantic.accent.container` | `#f15b40` | 2.82:1 | The brand accent as a CONTAINER — fills, large-type CTA backgrounds, the |
| `semantic.accent.text` | `#b03822` | 5.18:1 | The brand accent's TEXT-SAFE role — the only coral value permitted to ca |
| `semantic.focus` | `#0f62fe` | 4.23:1 | Focus indicator color |

**The accent rule, and it is binding.** CoForge coral — accent and CONTAINER role only. Fills shapes, large-type CTAs, the wordmark C. NEVER body text, small labels, captions, legends, table values or form hints, on any ground (brand.md §3 binding rule) — measures 2.82:1 on bone / 3.33:1 on white, below the 4.5:1 AA text floor at every si

In practice: coral fills shapes and marks a selected state. `#b03822` is
the only coral permitted to carry text on the ground. If you find yourself setting a label
in `#f15b40`, the design is wrong, not the rule.

---

## Type — two faces, and only two

Both are Open Font License. Install them, or Figma will substitute and the layout will shift.

- **Anek Latin** — every word. Display *and* body: CoForge is single-family for prose, so
  hierarchy is carried by weight, not by a second typeface.
- **Source Code Pro** — every number, plus code and token values.

**Why numbers are not set in Anek.** Measured in Figma at 28px: ten `1`s in Source Code Pro
occupy 168px and ten `0`s occupy 168px. In Anek Latin the same strings measure 95px and
159px — the `1` is **40.3% narrower**. Anek's digits are proportional, so a column of
figures set in it does not line up. Figma has no `font-variant-numeric`, so the face has to
do the work.

| Level | Size | rem | Weight | Tracking | Face |
|---|---|---|---|---|---|
| `display` | 62px | 3.875rem | 700 | -0.125rem | Anek Latin |
| `h1` | 40px | 2.5rem | 700 | -0.06rem | Anek Latin |
| `h2` | 28px | 1.75rem | 600 | -0.03rem | Anek Latin |
| `h3` | 20px | 1.25rem | 600 | -0.015rem | Anek Latin |
| `body` | 16px | 1rem | 400 | 0rem | Anek Latin |
| `body-sm` | 14px | 0.875rem | 400 | 0.005rem | Anek Latin |
| `caption` | 12px | 0.75rem | 400 | 0.01rem | Anek Latin |
| `code` | 12px | 0.75rem | 400 | 0rem | Source Code Pro |

Negative tracking on the large levels is deliberate and part of the identity — do not let
Figma Make normalise it to 0.

---

## Spacing — 13 steps, and nothing between them

`01` 2px · `02` 4px · `03` 8px · `04` 12px · `05` 16px · `06` 24px · `07` 32px · `08` 40px · `09` 48px · `10` 64px · `11` 80px · `12` 96px · `13` 160px

A value not on this scale is not in the system. Gaps between sections use the upper steps;
gaps inside a row use the lower ones.

---

## Structure

- **Corner radius: 0 everywhere.** No exceptions.
- **Borders: 1px.** A coloured left border thicker than 1px is the single most recognisable
  tell of generated UI — the system forbids it.
- **Shadows:** only `elevation.surface.raised`, and only on a floating panel. Flat by default.
- **Foundations page:** two columns — a 160px-ish sticky nav rail on the left,
  content on the right, collapsing to one column below 960px.
- **Competitor board:** a nav rail, a wide content column, and a detail panel that appears
  on selection. Rows are one repeated shape, never cards.

## Components — the only eleven that exist

A component enters this list by written spec, human approval and a decision record.
Do not invent a twelfth.

| Component | What it is |
|---|---|
| `cf-type-scale` | — |
| `cf-colour-roles` | — |
| `cf-spacing-scale` | — |
| `cf-rule` | — |
| `cf-table` | — |
| `cf-card` | — |
| `cf-chart-palette` | — |
| `cf-badge` | — |
| `cf-chip` | — |
| `cf-nav-rail` | — |
| `cf-detail-panel` | — |

---

## Motion

Durations 70ms–700ms; the workhorse is
`motion.duration.moderate.01` at 150ms. Standard easing is
`cubic-bezier(0.2, 0, 0.38, 0.9)`.
Motion conveys state only — a hover, a selection, a panel arriving. Nothing animates on load.

---

## Acceptance test — how to tell whether it is actually 1:1

Measurable, in order. If any of these fail, it is not a match.

1. **Ground is `#eeece6`** and body text is `#041222` —
   15.95:1.
2. **Every number is Source Code Pro** and every word is Anek Latin. Sample a table column:
   digits must align vertically.
3. **No corner radius anywhere.** Measure a container: 0px.
4. **No border wider than 1px**, and no shadow outside a floating panel.
5. **Body text ≥ 4.5:1** and non-text marks ≥ 3:1 against whatever sits behind them.
6. **Coral appears only as a fill or a state marker** — never as a word.
7. **Every spacing value lands on the scale above.** A 10px or 18px gap means it drifted.
8. **Tracking is negative on display/h1/h2** and matches the table.

## What Figma Make will get wrong if you let it

Named so you can catch them: rounded corners; a drop shadow on every card; an icon set that
was never specified; the accent used for a heading; numbers in the body face; a hero section
the content does not have; and spacing that is *close to* the scale rather than on it.
