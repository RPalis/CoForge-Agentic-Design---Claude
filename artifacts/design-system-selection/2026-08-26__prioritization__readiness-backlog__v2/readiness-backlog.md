# Readiness backlog v2 — resequenced around the two-level output model

**Supersedes ART-003.** v1 assumed one finish line. ADR-012 established two, and the
sequencing changes materially: **34 of 40 artifact types are L1** and do not wait for the
component library.

**Source:** `python3 validation/readiness-audit.py` · 2026-08-26

| Track | Score | What it produces |
|---|---|---|
| **L1 Foundations** | **40%** | docs · decks · dashboards · diagrams · journey maps · personas |
| **L2 Complete** | 22% | responsive web prototypes, product UI |
| Workflow | **100%** | the operating system itself — done |

## What changed from v1

v1 put `component.schema.json` first because it blocks everything. That is still true **for L2**.
But it is not the shortest path to *branded output*, and v1 implied nothing ships until the
index is populated. Three L1 items now come first.

---

## Wave 0 — unblocks L1, no dependencies

| # | Item | Blocks |
|---|---|---|
| 1 | **Brand inputs → `brand.md`** | Everything branded. `brand-director` is suggest-only and cannot invent a visual language |
| 2 | **Tokens: Carbon themes → DTCG** | All L1 output; also stops Gate B's token check reporting SKIPPED |
| 3 | **The 8 level-1 primitives** — `type-scale · colour-roles · spacing-scale · rule · table · card · chart-palette · badge` | Without them L1 has no legal component vocabulary and the gate blocks everything |
| 4 | **LICENSE** | Legal reuse. Two minutes |

**After Wave 0, L1 is live.** Decks, dashboards, journey maps and reports can be produced
on-brand and on-token, with Gate B genuinely enforcing — a full build stage earlier than v1
implied.

## Wave 1 — the L2 keystone

| # | Item | Note |
|---|---|---|
| 5 | **`component.schema.json`** | The DTCG-equivalent for components. Does not exist anywhere in the field |
| 6 | **Adapter #1: Carbon → contract + index** | Reads Apache-2.0 source, never the hosted MCP. Expect it to change the schema — that is why it comes straight after |

## Wave 2 — L2 becomes real

| # | Item | Unlocks |
|---|---|---|
| 7 | **CoForge MCP** — `list_components` · `get_contract` · `get_intent` · `list_tokens` · `check_compliance` | The agnostic premise |
| 8 | **Figma ↔ code map** from Carbon's 157 Code Connect files | ADR-001 inversion; POC link 5 |
| 9 | **Per-component `.md`** | Human-authored. Cannot be generated |

## Wave 3 — durability

| # | Item |
|---|---|
| 10 | **5 skills** — scaffold-component · audit-tokens · check-a11y · migrate-component · review-changes |
| 11 | **Skill evals** (ADR-005) — A/B against a no-skill baseline |

## Wave 4 — proves the premise

| # | Item | Why |
|---|---|---|
| 12 | **Adapter #2** (MUI or Polaris) | The only real test of whether the schema is a standard or a private format |

---

## Two critical paths, not one

```
L1:  brand inputs → tokens → 8 primitives  ────────────────▶  branded output live
L2:  component.schema.json → adapter #1 → index → MCP → adapter #2
```

They are independent until Wave 2. **L1 can ship while L2 is still being built** — which is
the whole point of ADR-012.

## The one thing only you can unblock

Waves 1–4 are work I can do. **Wave 0 item 1 is not** — `brand-director` is suggest-only and
never graduates, by design. Without brand inputs, L1 stays at 40% no matter what else gets built.

## Not on either path

| Item | Status |
|---|---|
| Carbon MCP early access | Reference point only. Our contract comes from source |
| Move off `~/Desktop` | Blocks the live preview server, nothing else |
| Git push / visibility | Pending the reframe — public may now be correct |
