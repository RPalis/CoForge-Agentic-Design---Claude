# ADR-019 — Self-governance: unchecked is not passed

**Status:** Accepted · 2026-08-28

## Context

On 2026-08-28 an audit of the system found twelve defects. Their details differ; their
shape does not:

| Defect | What was wrong |
|---|---|
| Token counter returned on the first `$value` | 46 tokens invisible; the repo reported 666 while holding 712 |
| 27 nodes in `semantic-dark` were token *and* group | invalid DTCG, would have broken the Figma import |
| Gate B compared kebab-case to PascalCase | blocked **every legitimate component** |
| Nothing walked `design-system/foundations/` | the audit printed `skipped 0 · PASS` on runs that never opened `brand.md` |
| Adapter keyed on directories, not exports | 13 entries not importable, ~230 missing |
| 13 `tokens_used` references resolved to nothing | the component↔token link was never traversed |
| A flatten compared a normalised copy to the real thing | a verification that could not fail |

**Every one was a claim that was asserted, believed, and verified by nothing — and
every check that did exist passed the whole time.** The system reported healthy while
being broken, in eight places.

The repository already knew half of this. `audit-system.py` prints *"skipped ≠ passed"*
because a skipped check is not a passing one. What it lacked was the generalisation:
**a check that does not exist is not a passing check either, and its absence is
invisible.** Silence read as health.

## Decision

Three mechanisms, all machine-checked in `validation/audit-system.py`.

### 1. The correction ledger — `validation/corrections.json`

**A defect is not fixed until a check exists that would have caught it.**

Every entry names its verifying check. The audit **fails** when an entry names a check
that no longer exists — a correction whose check was deleted is a regression, not a
tidy-up — and **warns** for every entry whose check is `null`.

Its prose ancestor, `memory/corrections.md`, was gitignored: nothing it recorded ever
survived a clone. This lives in a tracked path and is read by a machine.

### 2. The coverage ledger — `validation/coverage.json`

**Every load-bearing claim the system makes about itself names its verifier.**

Claims with `verified_by: null` are **reported as uncovered on every run**. This is the
mechanism that would have caught the `foundations/` gap: the claim "Gate B blocks
off-system writes" was true, and the claim "every SSOT file is checked" was not, and
nothing distinguished them.

At adoption: **6 of 16 claims are unverified**, including that work is routed through
the agent roster (it is not — all seven artifacts record `produced_by: main-session`)
and that the autonomy ladder graduates task types (it cannot — nothing counts).

Reporting those is the point. An uncovered claim nobody can see is exactly how the
twelve defects survived.

### 3. `system-keeper` owns the machinery

No routing-table row owned adapters, generators, validators, schemas or hooks. The
largest body of work in the repository had no owning agent, no gate, and no review path.
**The governance system did not govern the work that builds the governance system**, and
every defect in the ledger was found in that unowned surface.

`system-keeper` owns `validation/`, `design-system/contracts/`, `.claude/hooks/` and the
generated indices. Gate B, and Gate A on anything that changes what a gate accepts —
altering an enforcement layer is not a mechanical change.

## Consequences

- **The audit now reports what it does not know.** It went from `no findings · PASS` to
  `PASS` plus nine named gaps. That is a better report, not a worse system.
- **Warnings, not errors, at adoption.** Six unverified claims would fail CI on day one
  and the honest response would be to weaken the check. They are warnings so the number
  is visible and can be driven down.
- **New checks go into an existing audit.** Three already exist and ask three different
  questions — `audit-system` (is the repo legal), `audit-contracts` (is the design system
  coherent), `test-gates` (does enforcement work). A fourth would be the redundancy the
  contract audit exists to find.
- **A check that has never failed is unproven.** `test-gates.py` plants faults and
  requires them to be caught; it found Gate B blocking all legitimate work on its first
  run. Ship every check with its mutation case.

## What this does not fix

It records ignorance; it does not remove it. Six claims are still unverified and two
corrections still have no check — notably that **counts stated in prose are never
compared against the things they count**, which is how four documents came to claim
nine ADRs when there were seventeen.

The mechanism's value is that those are now a number on a dashboard instead of a
discovery waiting to happen.
