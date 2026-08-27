# ADR-016 — Repository location: off ~/Desktop

**Status:** Accepted · 2026-08-27
**Amends:** ADR-009, which recorded the working directory as `~/Desktop/Luma Claude`

## Context
macOS TCC protects `~/Desktop`, `~/Documents` and `~/Downloads`. The preview server could not
read its own files there — verified: an identical script failed with `EPERM` from Desktop and
started instantly from an unprotected directory.

## Decision
`/Users/raquelpalis/Projects/coforge`. No space in the path — the space in "Luma Claude"
required quoting in every script and was a standing source of breakage.

## Two things this surfaced
Moving re-ran everything from a new root, and two silent inconsistencies fell out:

1. **`llms.txt` said 666 tokens, `.ai/index.json` said 59.** The index counted top-level DTCG
   groups; `llms.txt` counted leaves. Two generated views of one source disagreeing — exactly
   the drift generated files are supposed to eliminate. Both now count leaves.
2. **The DS fork flipped RED → YELLOW on its own**, because the index inferred it from
   `components` being non-empty. Eight L1 primitives existing does not mean a design system
   exists. **The fork is a decision, not a heuristic** — it is now declared, with the count
   reported alongside rather than driving it.

Neither was caused by the move. The move only made them visible, which is an argument for
running the full toolchain from a clean root more often.

## Consequence
ADR-009's statement that the directory "is still `~/Desktop/Luma Claude`" is superseded here
rather than edited, per the standing rule that ADRs are historical record.
