# ADR-013 — POC acceptance criteria: the 8 links, and how each is passed

**Status:** Accepted · 2026-08-27

## Why this exists

"It works" is not measurable. Without criteria fixed *before* building, the definition of
success drifts to match whatever gets built — and this POC's entire output is a claim about
what "agent-ready" means. If the bar moves to fit the result, the finding is worthless.

Each criterion below states **what passes**, **how we get there**, and **what breaks if it fails**.

---

## 1 · INGEST — Carbon source becomes our contract

**Passes when** `component-index.json` is generated from Carbon's published packages with no
hand-editing, and regenerating produces an identical file.

**How** Adapter #1 reads `@carbon/react` TypeScript prop types plus the 157 `.figma.tsx`
Code Connect files. Apache-2.0 source only — **never** the hosted MCP, which the Terms exclude.

**If it fails** Every downstream link fails. This is the foundation.
**Fallback** If types prove unparseable, fall back to Code Connect files alone — they carry
prop names and variants, just not full type unions.

## 2 · QUERY — an agent can ask the contract, not the docs

**Passes when** the CoForge MCP answers `list_components` and `get_contract("Button")` with
structured data, and a fresh agent uses it without reading any documentation.

**How** Build five tools over `component-index.json`: `list_components` · `get_contract` ·
`get_intent` · `list_tokens` · `check_compliance`.

**If it fails** We are doing doc search, which is what Carbon already does and what we
identified as the industry's ceiling. The POC would prove nothing new.

## 3 · CONSTRAIN — the gate actually blocks

**Passes when** Gate B blocks a component absent from the index and a raw hex, **and** the
same violation written via a Bash heredoc is caught by the Stop backstop.

**How** Already built. Currently reports SKIPPED because both sources of truth are empty; it
becomes live the moment link 1 lands.

**If it fails** The system is advisory, not enforcing — the exact failure it was built to avoid.
**Known risk** Gate B did not fire for this entire session because Bash bypasses `Write|Edit`.
Closed 2026-08-27 with a Stop hook. **The test must exercise both paths.**

## 4 · PRODUCE — a real artifact, on-system

**Passes when** `screen-producer` builds a responsive screen using only indexed components and
tokens, and it survives the audit with zero blockers.

**How** L2 output per ADR-012. L1 artifacts can be produced earlier and prove less.

**If it fails** Either the contract is missing something screens need, or the gate is too strict.
Both are findings worth having.

## 5 · BIND — Figma and code are the same object

**Passes when** a Figma component and its code component resolve to one identity via Code
Connect, and changing the Figma component surfaces as a detectable difference.

**How** Import Carbon's 157 Code Connect files into `contracts/figma-code-map.json`.

**If it fails** ADR-001's inversion has no enforcement at the component layer and drift becomes
something a human must notice. **This is the link no other candidate system could pass at all.**

## 6 · INVERT — tokens round-trip

**Passes when** tokens go repo → Figma variables → export → repo and the drift check reports
no divergence.

**How** ADR-001: seed DTCG from Carbon themes, push via `figma_setup_design_tokens`, export
back via `figma_export_tokens`, diff.

**If it fails** Figma cannot own tokens and ADR-001 needs reversing.
**Known risk** Requires a real Figma file. None exists yet.

## 7 · VALIDATE — it passes without a human vouching

**Passes when** `a11y-checker` and `audit-system.py` both pass the produced screen, with every
skipped check named.

**How** Already built. The a11y floor is WCAG 2.2 AA per `design-system/a11y/rules.md`.

**If it fails** Output needs human review to be trusted, which does not scale.

## 8 · TRACE — provenance resolves end to end

**Passes when** the artifact's `manifest.json` chains to a real token version and every
`[E-nnn]` resolves in the ledger — and deliberately breaking one is caught.

**How** Already built. Needs a populated ledger, which needs research sources.

**If it fails** Claims cannot be audited, and the upstream half of the architecture is decorative.

---

## Dependency order

```
1 INGEST ──▶ 2 QUERY ──▶ 4 PRODUCE ──▶ 7 VALIDATE
     └──────▶ 3 CONSTRAIN ──┘              │
5 BIND ──▶ 6 INVERT                        │
8 TRACE ◀──────────────────────────────────┘
```

Links 3, 7 and 8 are **already built** and currently inert — they report SKIPPED because their
sources of truth are empty. They activate as a side effect of link 1, not as separate work.

**Real remaining work: links 1, 2, 5, 6.** Four, not eight.

## The two links we cannot pass alone

| Link | Blocked by | Owner |
|---|---|---|
| **6 INVERT** | No Figma file exists | Agentic Designer - RP |
| **8 TRACE** | No research sources — ledger is empty | Agentic Designer - RP |

## What a partial pass means

A POC that passes 1, 2, 3, 4, 5, 7 but not 6 and 8 has still proven the **component** half of
the loop end to end. That is a publishable result, stated as such — not a failure dressed up.

Recording that now, before we know the outcome, so a partial result cannot be quietly
relabelled as a complete one.
