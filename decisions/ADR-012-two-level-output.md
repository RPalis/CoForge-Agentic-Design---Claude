# ADR-012 — Two-level output model: L1 Foundations, L2 Complete

**Status:** Accepted · 2026-08-26

## Context

The DS fork (Green / Yellow / Red) treats the design system as one thing you either have
or do not. Under RED, `screen-producer` is wireframe-only and nothing branded ships.

That is too coarse. **Most of what a design team produces is not a product screen.** Decks,
dashboards, journey maps, insight reports and handoff specs are document-shaped. They need
a type scale, a colour system, spacing and a few primitives — a table, a card, a chart
palette. They do not need a Button with five variants and a loading state.

Holding all branded output hostage to a complete component library is a sequencing error.

## Decision

Two output levels, gated on different prerequisites.

### L1 — Foundations
**Branded artifacts: documents, decks, dashboards, diagrams.**

- **Needs:** `tokens.json` populated · `brand.md` approved · a small **level-1 primitive set**
- **Does not need:** the full component library, Code Connect, or the CoForge MCP
- **Produces:** `presentation` · `dashboard` · `data-viz` · `insight-report` · `journey-map`
  · `persona` · `metrics-scorecard` · `release-note` · `handoff-spec` · `competitive-benchmark`
- **Available from:** Build Stage 2, as soon as tokens land

### L2 — Complete
**Responsive web prototypes and product UI.**

- **Needs:** everything L1 needs, plus a populated `component-index.json`, Code Connect
  bindings and the CoForge MCP
- **Produces:** `ui-screen` · `prototype` · hi-fi `wireframe` · `component-spec` · `pattern-spec`
- **Available from:** Build Stage 3

## The level-1 primitive set

Eight primitives, derivable from tokens alone:

`type-scale` · `colour-roles` · `spacing-scale` · `rule` · `table` · `card` · `chart-palette` · `badge`

These are **not** a competing component library. They are the smallest vocabulary in which a
branded document can be expressed on-token.

## How Gate B behaves at each level

This is the part that needed working out, and it is why the decision has teeth.

`component-index.json` entries gain a **`level`** field (`1` or `2`).

| Check | L1 artifact | L2 artifact |
|---|---|---|
| Token enforcement | **applies** — no raw hex, ever | applies |
| Component gate | applies, restricted to **level-1** entries | applies, full index |
| Citation gate | applies | applies |

So an L1 deck using `<Card>` passes; an L1 deck reaching for `<DataTable>` is blocked with a
message naming the level. The gate stays real at both levels instead of being switched off
for documents — which is what would have happened if L1 had simply been exempted.

## Consequences

- **Branded output starts a full build stage earlier.** L1 lands at Stage 2 with tokens,
  rather than waiting for Stage 3.
- `screen-producer`'s "wireframe-only under RED" charter is refined: wireframe-only for **L2**,
  but free to produce L1 artifacts once tokens exist.
- The readiness audit reports **two scores**, not one. A design system can be L1-ready and
  L2-unready, and that distinction is useful when auditing other systems too — most of the
  field is closer to L1-ready than to L2-ready.
- `_types.json` gains a `level` field per artifact type.

## Rejected alternative

**Exempting L1 artifacts from the component gate entirely.** Simpler, and it would have made
documents a hole in the enforcement model — the one place off-system values could accumulate
unchecked. Restricting the vocabulary is stricter than exempting it, and costs one field.
