# ADR-018 — Component namespacing: `cf-` on our layer, vendor names untouched

**Status:** Accepted · 2026-08-28

## Provenance

Recommended by Claude, accepted by Agentic Designer - RP on the recommendation rather
than on independent technical judgement. Recorded because the naming scheme is load-
bearing for the component layer; "Falsifiers" at the end says what would show it wrong.

## Context

Adapter #1 (ADR-013 link 1) generates 208 L2 components from `@carbon/react`. CoForge
authors 8 L1 primitives of its own. They shared one flat namespace, and
`component-index.json` is what Gate B reads and what the CoForge MCP will answer
`get_contract()` from.

**One exact collision: our `table` vs Carbon's `Table`.**

It was live and dangerous. `<Table />` matched our L1 `table`, **passed Gate B**, and
resolved in code to Carbon's `Table`. The gate went green on off-contract usage — the
precise failure it exists to prevent.

It was also nearly the *wrong* collision. Before the adapter was re-keyed on public
exports it reported `card` vs `Card`, and a rename would have been aimed at a name that
does not collide at all — `Card` is not importable, Carbon ships it as `preview__Card`.
Only correcting the key revealed `table`. **A naming decision taken on the earlier
numbers would have been confidently wrong.**

## Decision

**Every component CoForge authors carries a `cf-` prefix. Vendor component names are
never modified.**

| Ours | Carbon's |
|---|---|
| `cf-type-scale`, `cf-colour-roles`, `cf-spacing-scale`, `cf-rule`, `cf-table`, `cf-card`, `cf-chart-palette`, `cf-badge` | `Table`, `preview__Card`, `BadgeIndicator`, … — byte-identical to what Carbon exports |

The prefix is **mandatory, not collision-triggered**. It applies to everything CoForge
authors whether or not anything currently clashes.

## Why

**Collision becomes structurally impossible rather than merely absent.** Gate B
normalises names, and `cf-table` normalises to `cftable`, which no vendor symbol can
produce. We stop detecting collisions and start precluding them.

**Vendor names stay exactly what Code Connect binds and what a developer types.**
ADR-011 chose Carbon *because* of Code Connect; the 1:1 claim lives at the string level.
Any scheme that rewrites Carbon's names inserts a translation layer between the Figma
component and the code component, dissolving the thing Carbon was adopted for.

**It is what makes the vendor swappable — the POC's actual claim.** Swap Carbon for
Material and Material brings its own `Table`, `Card`, `Badge`. Under rename-on-collision
we rename again, every time, and our names are permanently coupled to whichever vendor
we happen to have. Under a mandatory prefix the vendor layer is the only thing that
moves and every agent reference to `cf-*` survives the swap. One layer stable, one
layer replaceable, is what "design-system-agnostic" has to mean operationally.

**It has direct precedent** — sources and failure cases in
`validation/reports/2026-08-28__namespacing-research.md`. GOV.UK mandates `app-c-` / `gem-c-` and states outright not
to use the `govuk-` namespace — reserve the vendor's space, namespace your own. IBM does
it to itself: `@carbon/ibm-products` ships `Datagrid` and `ProductiveCard`, never a
competing `Card`. Every real-world failure the research surfaced was **partial**
prefixing — prefixing only what clashed.

## Rejected

- **Rename only on collision.** Couples our names to this vendor's namespace and recurs
  on every Carbon release and every vendor swap. The consistent signal across every
  documented convention is that the namespace is mandatory, never triggered.
- **Prefix both layers.** More robust in the abstract; 216 renames instead of 8, breaks
  the string-level Code Connect binding, and needs a resolution step in `gate-b.py`.
  Roughly 13× the cost to defend against a second vendor that does not exist yet.
- **Disambiguate by ADR-012 level.** Works for Gate B, fails for `get_contract("table")`,
  which has no ambient level. `level` is also mutable, so a key built on it is not an
  identity.
- **Alias map / precedence.** Either it resolves to one entry (a rename with indirection)
  or it does not (two things, one name). Ordering is not identity.

## Cost

Eight renames, once. `ADR-012` names the primitives by their old names and is now
historical on that point; this ADR supersedes it for naming only. Our primitives read
less naturally in the index — `cf-table` is uglier than `table`. That is the whole price.

## Falsifiers — what would show this was the wrong call

1. **An agent cannot resolve `cf-*` names reliably.** If `get_contract("cf-table")` proves
   awkward in practice, or agents keep writing `table`, the prefix is fighting how models
   actually reference things. Watch this at ADR-013 link 4, the first real screen.
2. **A second vendor arrives and we still have to rename.** The prefix is justified by
   surviving a vendor swap. If swapping Carbon still forces changes to `cf-*`, the
   reasoning failed.
3. **The 1:1 claim breaks anyway.** If Code Connect binding turns out to need our names
   too, then leaving Carbon's untouched bought nothing.
4. **Nobody honours it.** If CoForge-authored components appear without the prefix, the
   rule has become partial prefixing, which is the documented failure mode — and worse
   than never having started.

Reopen this ADR if any of the four hold.
