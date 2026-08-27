# Readiness backlog — what CoForge is missing, in build order

**Source:** `python3 validation/readiness-audit.py` · 2026-08-26 · **54% ready**
(present 12 · partial 1 · missing 10)

Re-run the audit at any point; this list is derived from it, not maintained by hand.

## The shape of the gap

| | Result |
|---|---|
| **Workflow layer** (ours) | **9 / 9 present** — CLAUDE.md, architecture.md, `.ai/` index, 13 agents, 11 ADRs, all 5 enforcement layers |
| **Design-system layers** | almost entirely missing |

That split is correct, not alarming. The workflow was Build Stage 0's job and it is done.
The design system is DS-state **RED** by definition — there is nothing there yet.

## The keystone

**`component.schema.json` blocks almost everything else.** Without it there is no definition
of what a component contract must contain, so every adapter would invent its own shape and
nothing could validate any of them. It is also the piece the whole field is missing — tokens
have W3C DTCG, components have no equivalent from any standards body.

Build it first. It is specification work, needs no Carbon access, and costs a day.

---

## Wave 0 — no dependencies, buildable now

| # | Item | Why now | Consequence of not doing it |
|---|---|---|---|
| 1 | **`component.schema.json`** | Keystone. Everything downstream validates against it | Every adapter invents its own shape |
| 2 | **LICENSE** | Two-minute job | Nobody may legally reuse CoForge — and we audited everyone else's licence while shipping none |

## Wave 1 — needs the schema

| # | Item | Depends on |
|---|---|---|
| 3 | **Adapter #1: Carbon → contract + index** | Wave 0 · reads Apache-2.0 source, never the hosted MCP |
| 4 | **Tokens: Carbon themes → DTCG** | Wave 0 |

Adapter #1 is where the schema gets tested against reality. Expect it to change the schema —
that is the point of building it early rather than designing in the abstract.

## Wave 2 — needs a populated contract

| # | Item | Unlocks |
|---|---|---|
| 5 | **CoForge MCP** — `list_components` · `get_contract` · `get_intent` · `list_tokens` · `check_compliance` | The agnostic premise. This is what makes the design system swappable |
| 6 | **Figma ↔ code map** from Carbon's 157 Code Connect files | ADR-001 inversion, POC link 5 |

**Two Gate B checks stop reporting SKIPPED the moment Wave 1 lands** — token enforcement and
the component gate both currently pass everything silently because their sources of truth are
empty. That is not a bug; the hook reports it honestly. But it means the gate is not actually
guarding anything yet.

## Wave 3 — needs a working loop

| # | Item | Note |
|---|---|---|
| 7 | **5 skills** — scaffold-component · audit-tokens · check-a11y · migrate-component · review-changes | Generalised from Carbon's 13 reference files |
| 8 | **Per-component `.md`** — when to use, when NOT to | **Human-authored. Cannot be generated** — it is the judgment layer |
| 9 | **Skill evals** (ADR-005) | `evals/evals.json` per skill, A/B against a no-skill baseline |

## Wave 4 — proves the premise

| # | Item | Why it matters |
|---|---|---|
| 10 | **Adapter #2** (MUI or Polaris) | The only real test of whether the schema is a standard or a private format. If adapter #2 fits without changing the schema, the schema is real |

## Not on the critical path

| Item | Status |
|---|---|
| Carbon MCP early access | Reference point only. Our contract comes from Apache-2.0 source, so this never blocks |
| Move project off `~/Desktop` | Blocks the live preview server (macOS TCC), nothing else |
| Git push / repo visibility | Decision pending the reframe — public may now be correct |

## Critical path

```
component.schema.json → adapter #1 → component-index.json → CoForge MCP → adapter #2
```

Five items. Everything else is parallel or downstream.
