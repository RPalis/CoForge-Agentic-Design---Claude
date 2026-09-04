# ADR-022 — First promotions through the membrane: cf-chip, cf-nav-rail, cf-detail-panel

**Status:** ACCEPTED — signed off by Agentic Designer - RP, 2026-09-03 (Gate A)
**Date:** 2026-09-03
**Evidence:** ART-018 (`artifacts/design-system-authoring/2026-09-03__component-spec__cf-chip__v1/`),
ART-019 (`…__cf-nav-rail__v1/`), ART-020 (`…__cf-detail-panel__v1/`)
**Related:** ADR-021 (dataviz layer, accepted the same day — governs why ART-017 is
excluded from this ADR); CLAUDE.md "The membrane"; ADR-012 (levels); ADR-018 (namespacing)

## Context

Until today, every entry in `design-system/component-index.json` fell into one of two
buckets: 208 level-2 rows ingested wholesale from `@carbon/react@1.115.0` by
`validation/adapters/carbon-react.py`, and 8 level-1 primitives derived from tokens at
Build Stage 0–2 (`cf-type-scale`, `cf-colour-roles`, `cf-spacing-scale`, `cf-rule`,
`cf-table`, `cf-card`, `cf-chart-palette`, `cf-badge`). **Zero were CoForge-authored
product components promoted by spec → human approval → ADR → index** — the path
CLAUDE.md calls the membrane. That is the fact the DS fork's RED state (ADR-011) has
been measuring since 2026-08-28, and it is unchanged by this ADR: all three promotions
below are **level 1**, and the fork's criterion counts level-2 authorship only.

`screen-producer` filed four component-spec proposals against the coverage-board work
(ART-017–020): `cf-unit-cell`, `cf-chip`, `cf-nav-rail`, `cf-detail-panel`. Each spec
ships a `verify-contrast.py` that re-derives every token resolution and contrast ratio
the payload asserts from `design-system/tokens/tokens.json`, and validates the proposed
index entry against `design-system/contracts/component.schema.json` and against the
index's identity rule (no normalised-name collision).

## Verification, run before promotion

Each verifier was executed by system-keeper against the **pre-promotion** index and
exited clean:

```
cf-chip           — verify-contrast.py — VERDICT: PASS (10 token rows, 10 contrast
                    rows, schema OK, name 'cfchip' — no collision across 216 entries)
cf-nav-rail       — verify-contrast.py — VERDICT: PASS (10 token rows, 10 contrast
                    rows, schema OK, name 'cfnavrail' — no collision across 216 entries)
cf-detail-panel   — verify-contrast.py — VERDICT: PASS (9 token rows, 9 contrast
                    rows, schema OK, name 'cfdetailpanel' — no collision across 216
                    entries)
```

All three: tokens.json `$version` 0.2.0, every asserted hex and luminance re-derived
within tolerance, every contrast ratio re-derived within 0.002, every `tokens_used`
path resolved live against `tokens.json`. Re-run after promotion, all three correctly
report `ALREADY IN THE INDEX` — the verifier's designed signal that a proposal has been
promoted, not a defect.

`cf-unit-cell`'s verifier was **not** run toward promotion, because ADR-021, accepted
the same day, rules it out before verification is the relevant question — see below.

## Decision

**Promote `cf-chip`, `cf-nav-rail` and `cf-detail-panel` into
`design-system/component-index.json`, all at level 1, status `experimental`.**
Authority: human approval (Agentic Designer - RP), Gate A, 2026-09-03, on the exact
JSON entries each spec proposed (`<!-- PROPOSED-INDEX-ENTRY -->` block), unedited
except for `source`, which now records the promotion and this ADR.

**Do not promote `cf-unit-cell` (ART-017).** Under ADR-021, one observation in a unit
chart or dot matrix is chart anatomy — drawn by the chart's own rendering logic — not a
product component. It does not enter the index. The spec stays in `artifacts/` as
documentation of the encoding; it is not superseded, not rejected on its merits, and
not eligible for promotion under the membrane, because the membrane is not the gate
that governs it. Promoting it would be exactly the error ADR-021 exists to prevent.

Index changes made:

| Field | Before | After |
|---|---|---|
| `count` | 216 | 219 |
| `$extensions.coforge.l1_primitives` | 8 | 11 |
| `$extensions.coforge.l2_components` | 208 | 208 (unchanged — nothing promoted at level 2) |

`cf-chart-palette` (an existing, unrelated L1 entry) was separately marked `deprecated`
in this same edit, for the reason recorded in ADR-021 and correction C-036 — not part
of this ADR's authority and noted here only so the index diff is not misread as one
promotion where it is two unrelated changes landing together.

## Why level 1, and why that matters for survival

All three specs proposed level 1. `cf-detail-panel`'s own spec calls this the weakest
classification in its batch — it carries scripted focus management that no existing
L1 primitive has — and names the deciding fact: `validation/adapters/carbon-react.py`
preserves index entries only where `level == 1` and unconditionally deletes every
`.json` under `design-system/components/` before rebuilding level-2 entries from the
vendor tarball. A level-2 entry authored here has no surviving lane through that
adapter (C-038, open, descoped by ADR-021 but not fixed). System-keeper verified this
directly rather than assuming it: read `validation/adapters/carbon-react.py:325`
(`l1 = [c for c in existing["components"] if c.get("level") == 1]`) and confirmed none
of the three new entries have a corresponding file in `design-system/components/`
(that directory holds only the 208 generated L2 contracts — L1 primitives live inline
in `component-index.json` only). **Promoting these three at level 1 is therefore safe
against the next `carbon-react.py --apply`: all three are preserved verbatim, and
there is nothing in `design-system/components/` for the adapter's blind delete to
catch.** This does not close C-038 — a future level-2 promotion still has no surviving
lane — and that gap is recorded, not fixed, in C-038 and in this ADR.

## What this does and does not change

- **DS fork stays RED.** ADR-011's criterion counts level-2 authorship; 0 of 208 L2
  rows are CoForge-authored, unchanged by this ADR. Confirmed: `validation/index-system.py`
  derives `ds_fork` from `l2_authored_here`, which this promotion does not touch.
- **First CoForge-authored entries of any kind to enter the index by the documented
  membrane.** The 8 founding L1 primitives predate the membrane's first exercise;
  these three are the first proposals to travel spec → verification → Gate A → ADR →
  index.
- **Status is `experimental`, not `stable`.** Both proposing specs and this ADR treat
  that as correct: `cf-detail-panel`'s level is contested in its own text, and none of
  the three have been used in a shipped screen yet.
- **The `cf-badge` amendment inside ART-018 is a separate proposal and is NOT approved
  here.** `cf-chip`'s spec proposes rewording `cf-badge.when_not_to_use` and
  `cf-badge.a11y.note` to record that `cf-badge`'s four status kinds are
  luminance-identical (error 4.235:1, success 4.246:1, warning 4.221:1 — within 0.025
  of each other). That finding is filed as a defect against `cf-badge` and is real,
  but it is a change to an existing `stable` entry that `screen-producer` does not own,
  and it needs its own approval and its own ADR. `cf-badge` is unchanged by this ADR.

## Not this agent's job, and not done here

- **cf-unit-cell's encoding is not re-litigated.** ADR-021 already ruled it chart
  anatomy; this ADR only records the consequence for the index.
- **The dataviz token group ADR-021 calls for is not designed here.** That is
  token-keeper's, against C-036, and does not exist yet.
- **C-037 (the component gate's PascalCase-only detector) and C-038 (the adapter's
  destructive rebuild) are assessed, not fixed, in the accompanying system-keeper
  report** (`validation/reports/2026-09-03__system-keeper-adr021-promotion.md`).
  Both would change what Gate B or the adapter accepts, which is Gate A, and neither
  was in the approval this ADR executes.

## Consequences

- `design-system/llms.txt`, `.ai/index.json` and `.ai/index.md` are regenerated to
  reflect 219 components / 11 L1 primitives, per system-keeper's ownership of
  generated indices.
- The next agent proposing an L1 or L2 component now has three worked examples of a
  spec that survived verification and Gate A, in addition to the 8 founding
  primitives.
- `design-system/tokens/tokens.json` is untouched. Canonical SHA-256 (sorted-key,
  no-whitespace form) verified unchanged before and after this ADR:
  `1926c393fe83742443350f2aa4e8d5dd3d0d6d7393a31c93e2f74317cada1a7f`.
