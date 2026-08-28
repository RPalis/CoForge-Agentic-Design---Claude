# CoForge Design System

**State: RED** — a *declared* state, not a count (2026-08-28). Foundations are done:
786 tokens across five axes, `brand.md` approved at Gate A, 8 L1 primitives. RED holds
until the component index carries **L2** entries — L1 primitives existing does not make
a design system exist. `screen-producer` is unblocked for L1 output and stays blocked
for L2. See the DS fork in `CLAUDE.md`.

## Structure

| File | What it is | Machine or human |
|---|---|---|
| `llms.txt` | Condensed index for cheap agent context | machine |
| `component-index.json` | The catalogue. Query before you invent. | machine |
| `tokens/tokens.json` | DTCG tokens. The only legal source of colour, spacing, radius, type. | machine |
| `foundations/brand.md` | Voice, visual language, colour rationale, type scale logic | human |
| `components/<Name>.json` | Contract: props, variants, sizes, states, slots, a11y | machine |
| `components/<Name>.md` | Intent, when to use, **when NOT to use** | human |
| `patterns/` `templates/` | Validated structures | both |
| `contracts/figma-code-map.json` | Figma property ↔ code prop ↔ token | machine |
| `a11y/rules.md` | Accessibility rules and thresholds | human |

JSON carries contracts because it is what agents query. Markdown carries intent
because that is what reasoning needs. Both, never one.

## Build order (Build Stage 1B → 2)

| # | Step | State |
|---|---|---|
| 1 | `brand-director` → `foundations/brand.md` (suggest-only, never automatic) | **done** — Gate A 2026-08-27, §4 amended 08-28 |
| 2 | `token-keeper` → `tokens/tokens.json` v0 | **done** — 786 tokens, 5 axes, 0 literals above the primitive layer |
| 3 | push to Figma variables → **ADR-001 inversion** | blocked — no Figma file exists |
| 4 | components → `component-index.json` + per-component contract and intent files | in progress — adapter #1, ADR-013 link 1 |
| 5 | generate `llms.txt` from the index — never hand-written | **done** — `validation/build-llms-txt.py` |

### Open divergence in step 4, recorded not resolved

The structure table above promises **per-component** `<Name>.json` and `<Name>.md`.
Adapter #1 currently writes everything into a single `component-index.json` instead,
and `design-system/components/` is empty.

That is not a small difference. With 96 Carbon components and ~800 props, one file is
a context bomb — and progressive disclosure is the reason this repo has an `llms.txt`
and a `.ai/index.md` at all. The documented shape (a thin index, per-component detail
fetched on demand) is very likely the right one, and the adapter is the thing that
should change. Recorded here so the divergence is a decision rather than a drift.

## Promotion

Nothing enters this folder by accident. A `component-spec` in `artifacts/` is a
proposal; it becomes a component only by explicit human approval recorded as an ADR.
