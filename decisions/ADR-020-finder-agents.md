# ADR-020 — Finder agents: scoped Write, and a denominator on every finding

**Status:** Accepted · 2026-08-31

## Context

`a11y-checker` and `design-critic` held `tools: [Read]`. Both **own an artifact type** in
`artifacts/_types.json` — `a11y-audit`, and `design-critique` + `heuristic-review`.

An owner with no `Write` cannot produce the type assigned to it. All three types were
uncreatable, and had been since the taxonomy was written.

`audit-system.py` check 2 verified that a type's owner *existed*. It never asked whether
the owner *could write*. Absolute read-only read as the safer setting and was in fact the
broken one — a guarantee so strong the thing it guarded could never happen.

Found while asking a different question: which agent could produce a registered artifact,
so that coverage claim V-016 ("work is routed through the agent roster") could stop being
false.

## Decision

**1. Finder agents hold `Write`, and never `Edit` or `Bash`.**

The scope is a tool boundary, not a promise. `Write` creates a file; `Edit` changes one
that already exists. A finder can therefore record what it found and **cannot alter a
single existing design file, token or screen**. That is the property its autonomy rests
on, and it is now enforced where it belongs — at the permission layer, not in prose.

CLAUDE.md's own rule applies and is honoured: *"Never solve with prose what a permission
can solve."*

**2. A finding artifact must record what it CHECKED, not only what it FOUND.**

Every finder-owned artifact carries:

```json
"findings": { "findings_by": "<the type's owner>", "checked": <int > 0>, "found": <int> }
```

Zero findings is a legitimate result — an `a11y-audit` that finds nothing wrong is a
pass. But **"0 findings across 47 contrast pairs" and "0 findings" are different claims,
and only one is evidence.** Without a denominator, an audit that never ran is
byte-identical to one that ran clean: the artifact looks complete and is empty of the
thing it is named for.

This is `skipped ≠ passed` one layer up. A check with no denominator did not pass; it
did not happen.

## Rejected

**Orchestrator relays and writes.** Keeps finders absolutely read-only, which is the
stronger-sounding guarantee. Rejected because findings would travel through another
agent's context as text — the lossy step CLAUDE.md's *"handoff is through files, never
chat"* exists to prevent. It trades a failure you can see for one you cannot: a relayed
finding can be truncated or reshaped in transit while the artifact still looks complete,
and the denominator can survive the trip even when the substance behind it does not. It
also required amending "never passes artifact content between agents", which is
load-bearing.

**Reassign the three types to a writing agent.** One field per type, no tool change.
Rejected because nothing would force the writer to consult the finder: `handoff-scribe`
could produce an `a11y-audit` with a11y-checker never running, and it would pass every
gate. The blank becomes undetectable, which is the exact property this ADR exists to
prevent.

## Cost, stated plainly

Two agents gained a capability they did not have. `design-critic` is advisory *because* a
confident wrong critique steers bad revisions, and an artifact in `artifacts/` reads as a
deliverable rather than as advice. That risk is real and is not removed by this ADR — it
is bounded by the absence of `Edit`, and by design-critic remaining at Draft autonomy so
a human weighs its output before anything changes.

## Verification

- Check 2: a type's owner must hold `Write`.
- Check 3: a finder must hold `Write` and must hold neither `Edit` nor `Bash`.
- Check 5a: finder-owned artifacts must carry `findings_by` matching the type owner, an
  integer `checked` greater than zero, and an integer `found`.
- Check 5a negative-tested: a planted audit with `found: 0` and no `checked` produced
  `[BLOCKER] 'checked' is None — no denominator`, and the audit went red.

Recorded as corrections **C-014** and **C-015**.
