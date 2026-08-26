# ADR-004 — Two clocks: Build Stages vs Design Loop Phases

**Status:** Accepted · 2026-08-25

## Context
Two phase models existed and appeared to conflict: a 6-phase linear model and an
11-phase cyclical model.

## Decision
They are **orthogonal axes**, and both are kept.

| | Build Stages 0–5 | Design Loop Phases 1–11 |
|---|---|---|
| Answers | How do we build the system? | What does the system do once built? |
| Shape | Linear, one-time, gated | Cyclical, loops to Research |

The Design Loop becomes runnable at **Build Stage 3**. Until then the routing table
exists but most phases have no inputs.

## Consequences
Always say which clock is meant. "Phase 2" is ambiguous; "Build Stage 2" and
"Design Loop Phase 2" are not.

**Current position:** Build Stage 0 complete. Design Loop not yet runnable.
