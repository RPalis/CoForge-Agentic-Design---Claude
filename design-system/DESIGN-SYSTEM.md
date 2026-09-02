# CoForge Design System

**State: RED** — a *declared* state, not a count (2026-08-28). Foundations are done:
829 tokens across five axes, `brand.md` approved at Gate A, 8 L1 primitives. RED holds
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
| 2 | `token-keeper` → `tokens/tokens.json` v0 | **done** — 829 tokens, 5 axes, 0 literals above the primitive layer |
| 3 | push to Figma variables → **ADR-001 inversion** | **pushed, not inverted** — file `ip2wZ3UUQ5sbFc3r902kYK` holds 561 variables across 5 collections. The inversion is NOT reached and must not be attempted; see below |
| 4 | components → `component-index.json` + per-component contract and intent files | in progress — adapter #1, ADR-013 link 1 |
| 5 | generate `llms.txt` from the index — never hand-written | **done** — `validation/build-llms-txt.py` |

### Step 3 — pushed, not inverted

Corrected 2026-09-02. This row read *"blocked — no Figma file exists"* for three days after
a file existed, and no check in this repository could have noticed: check 5e compares
declared counts inside tracked markdown, and a state that names no number is not a
tracked count. Recorded in `validation/corrections.json` C-030 and
`validation/coverage.json` V-018.

**What is true.** Of 829 tokens, **797 are importable as Figma variables**; the other 32
are correctly absent — 12 belong to a Figma *style* rather than a variable, and 20 have no
Figma representation at all. Those 797 rows fold into **561 live variables** because
`semantic` and `semantic-dark` were collapsed into one collection with **Light and Dark
modes**, so the 236 dark rows are a second mode rather than 236 further variables. Live
collections: `palette` 289, `semantic` 236 (two modes), `spacing` 13, `typography` 21,
`density` 2. Derived by `validation/figma-representable.py` and by an independent
re-derivation of the bridge in
`validation/reports/2026-09-02__token-keeper-figma-mirror-audit.md`, which found **0
missing, 0 extra, 0 divergent** across 797 comparisons.

**The push is not the inversion.** ADR-001 makes Figma the owner and this repository the
mirror. That is a one-way door and four grounded reasons say it is not open yet:

1. **32 tokens have no Figma variable form.** An export-driven mirror deletes or degrades
   them — C-017's class exactly.
2. **The rem→px conversion is deliberately one-way.** A mirror needs an inverse that
   nobody has written or tested.
3. **The mode collapse means an export produces a shape `tokens.json` does not have** —
   one collection with two modes, against two parallel top-level groups here.
4. **`figma_export_tokens` is on record as unreliable** (C-020): it reported 8 collections
   when 6 existed and re-emitted 14 deleted variables.

There is a fifth, softer reason: the descriptions. A Figma variable holds one description,
not one per mode, so 161 dark-side descriptions live only here. They survive because this
side is still upstream, and they stop surviving the moment it is not.

**Before anything about this row changes**, `validation/check-figma-live.py` has to read 0
blockers and 0 uncompared. It currently reads FAIL, because it has no concept of modes —
that is C-030, and the repair is Phase 2 of
`validation/reports/2026-09-02__plan-foundations-figma-migration.md`. The recommendation
there is an ADR-001 amendment that defers the inversion with those four as explicit entry
criteria: a deferral with a test, rather than a deferral by silence.

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
