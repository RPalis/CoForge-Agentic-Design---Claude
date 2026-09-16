# CoForge Design System — Foundations Reference
**Version:** 0.2.0 · **Status:** L1 Foundations complete, L2 in progress
**For:** Figma Make — paste this document as a design system prompt

---

## Identity

CoForge is an enterprise AI consultancy. The brand says *AI is here, AI is real — is it working for you?* before it sells anything. Visual language: warm, direct, confident, measured.

**What this is not:** no gradients, no glassmorphism, no neon, no violet-to-cyan AI aesthetic. Flat, structured, document-first.

---

## Colour

All colours are roles, not hue names.

| Token | Hex | Role |
|---|---|---|
| `ground` | `#eeece6` | Default page and document surface — warm bone, not white |
| `ink` | `#041222` | Default text, marks, icons — deep navy, not black |
| `ink-2` | `#525252` | Secondary text, labels, captions |
| `coral` | `#f15b40` | Primary accent — fills shapes, marks wordmark, backs large CTA. **Never body text.** |
| `coral-text` | `#b03822` | Darker coral for text on light surfaces only (≥4.5:1) |
| `rule` | `#c6c6c6` | Dividers, borders |
| `white` | `#ffffff` | Raised surfaces — cards, floating nav sit on it (elevation signal) |

### Contrast ratios (on `ground`)
- Ink on ground: **15.95:1** — AAA
- Ink-2 on ground: **5.26:1** — AA
- Coral on ground: **2.82:1** — accent only, never text
- Coral-text on ground: **≥4.5:1** — text on light backgrounds only

### Rules
- Coral is an accent and container colour — fills, wordmark, rules, large-type CTAs
- Coral never carries body text, captions, labels, table values, or any text below large-text size
- Two coral roles: `coral` (accent) and `coral-text` (separate darker value)
- Black (`#000000`) is not in the system
- Pure white is only for raised surfaces, not the page ground
- One hot accent — secondary hues (teal, periwinkle) live only in illustration and charts

---

## Typography

Single variable family for everything except code.

| Role | Family | Weight | Size | Tracking |
|---|---|---|---|---|
| Display / H1 | Anek Latin | 700 Bold | 56px | −0.125rem (tight) |
| H2 | Anek Latin | 700 Bold | 42px | −0.08rem |
| H3 / Section | Anek Latin | 700 Bold | 28px | −0.04rem |
| H4 | Anek Latin | 700 Bold | 20px | 0 |
| Body Large | Anek Latin | 400 Regular | 19px | 0 |
| Body | Anek Latin | 400 Regular | 16px | 0 |
| Body Small | Anek Latin | 400 Regular | 14px | 0 |
| Label / Tag | Source Code Pro | 700 Bold | 15px | 0.08em |
| Step numbers | Source Code Pro | 700 Bold | 20px | 0 |
| ART ref / code | Source Code Pro | 400 Regular | 14px | 0 |
| Caption | Anek Latin | 400 Regular | 14px | 0 |

### Rules
- Tracking tightens as size grows, relaxes to 0 at ≤16px
- Weight carries hierarchy before size — a table header earns rank by weight
- `font-variant-numeric: tabular-nums` is **mandatory** at every level that can carry a number (Anek's digits are proportional by default — columns misalign without it)
- Source Code Pro chosen to be unnoticeable beside Anek Latin (x-height difference: 0.4%)
- Display face is characterful; body face is not — they do not compete

---

## Spacing

4px base grid.

| Token | Value | Use |
|---|---|---|
| `space-1` | 4px | Micro gaps, icon padding |
| `space-2` | 8px | Tight element gaps |
| `space-3` | 12px | Default small padding |
| `space-4` | 16px | Standard component padding |
| `space-5` | 24px | Section gap small |
| `space-6` | 32px | Section gap |
| `space-7` | 48px | Large section gap |
| `space-8` | 64px | Hero / page-level gap |
| `space-9` | 80px | Stage register breathing room |

---

## Radius

One continuous radius language. Scale with the size of the thing.

| Context | Value |
|---|---|
| Small controls (tags, chips, pills) | 9999px (full pill) |
| Inputs, badges | 4px |
| Buttons (standard) | 8px |
| Cards, panels | 16px |
| Large cards, hero cards | 24–28px |
| Modal | 16px |
| True circles | Reserved for genuinely circular affordances only |

**Rule:** one radius vocabulary, continuous — not two overlapping systems with the same values.

---

## Elevation

Expressed as a single soft shadow, not as borders or stacked depths.

| Level | Token | Shadow |
|---|---|---|
| Resting (most things) | `shadow-0` | none |
| Raised (cards, floating nav) | `shadow-1` | `0 2px 6px rgba(4,18,34,0.12)` |
| Modal / dropdown | `shadow-2` | `0 8px 24px rgba(4,18,34,0.18)` |

**Rules:**
- One depth at a time — no nested elevations
- Shapes float rather than stack
- No borders expressing elevation — shadow only

---

## Density registers

The brand runs in two registers (not two themes — same colours, same radius, different space and type scale):

### Stage
Covers, section openers, key figures, hero statements.
- Large type (H1 56px or larger)
- Long silences — generous whitespace
- One idea per surface
- `space-7` to `space-9` between blocks

### Document
Reports, tables, scorecards, specs — the majority of CoForge output (35 of 41 artifact types).
- Tight but not cramped
- `space-4` to `space-6` between blocks
- Whitespace earned per element, not granted by default
- Body at 16px Regular, headers carrying weight not size jumps

---

## Motion

Minimal. Confirms; does not perform.

| Property | Value |
|---|---|
| Duration | 120–200ms |
| Easing | `cubic-bezier(0.2, 0, 0.38, 0.9)` — near-linear, soft landing |
| Properties | Position + opacity only. No scale, no rotate, no bounce |
| Stagger | None — one thing moves at a time |
| Bounce / overshoot | Never |
| `prefers-reduced-motion` | Respect: skip all transitions |

**Rules:**
- The ground never moves — bone is the paper
- Motion is never the only signal — every animated state has a text/position/state equivalent
- L1 output (documents) gets no motion by default

---

## L1 Primitives (available now)

These 11 primitives are available for all L1 output:

| # | Primitive | Notes |
|---|---|---|
| 1 | `type-scale` | Anek Latin + Source Code Pro ramp |
| 2 | `color-palette` | Ground, Ink, Coral + CoForge brand primitives |
| 3 | `spacing-scale` | 4px grid, 9 steps |
| 4 | `radius-scale` | Continuous pill-to-card scale |
| 5 | `shadow-scale` | 3 levels, single soft shadow |
| 6 | `table` | Dense, scannable, tabular-nums enforced |
| 7 | `card` | Raised white surface on bone, shadow-1 |
| 8 | `chart-palette` | Illustration/data only — not UI chrome |
| 9 | `icon-set` | Carbon icons base |
| 10 | `grid` | 12-col, 16px gutter, 4 breakpoints |
| 11 | `divider` | Rule colour #c6c6c6, 1px |

---

## What the brand is **not** (Figma Make constraints)

Do not generate:
- Coral on bone body text or small labels
- Gradient backgrounds or fills
- Glassmorphism, frosted glass, noise
- Neon colours, violet-to-cyan, AI-aesthetic gradients
- Multiple accent colours in UI chrome
- Decorative motion or animation
- Black (#000000) — use Ink (#041222)
- Pure white (#ffffff) as the page ground — use Ground (#eeece6)
- IBM Carbon's visual language — Carbon is the structural base, not the face

---

## Voice rules (for copy in designs)

- Short declaratives. Statement before offer.
- Second person, plain register: "you", "Start the conversation" — not "Request a demo"
- No exclamation marks, no superlatives, no unfalsifiable claims
- Numbers and quotes carry their source inline
- Visible open questions and assumptions — not stripped for polish
- Every sentence that can be shorter, is

---

## Figma Make prompt summary

> Design in the CoForge design system. Background: warm bone #eeece6. Text: deep navy #041222. Accent: coral #f15b40 — fills only, never body text. Typography: Anek Latin (Bold for headings, Regular for body). Monospace: Source Code Pro. One radius language from pill to 28px. Single soft shadow for elevation. Flat, document-first. No gradients, no glass, no neon.
