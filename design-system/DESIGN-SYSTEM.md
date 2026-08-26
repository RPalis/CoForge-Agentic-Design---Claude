# CoForge Design System

**State: RED** — no design system exists yet. `token-keeper` builds one before
`screen-producer` produces hi-fi screens. See the DS fork in `CLAUDE.md`.

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

1. `brand-director` → `foundations/brand.md` (suggest-only, never automatic)
2. `token-keeper` → `tokens/tokens.json` v0
3. push to Figma variables → **ADR-001 inversion**
4. components → `component-index.json` + per-component contract and intent files
5. generate `llms.txt` from the index — never hand-written

## Promotion

Nothing enters this folder by accident. A `component-spec` in `artifacts/` is a
proposal; it becomes a component only by explicit human approval recorded as an ADR.
