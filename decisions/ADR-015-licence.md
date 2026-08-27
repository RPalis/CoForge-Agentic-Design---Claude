# ADR-015 — Licence: Apache-2.0

**Status:** Accepted · 2026-08-27

## Decision
CoForge is licensed **Apache-2.0**. `LICENSE` and `NOTICE` at the repository root.

## Why not MIT
Three reasons, in order of weight:

1. **Compatibility with what we build on.** Carbon and `@carbon/themes` are Apache-2.0, and our
   tokens derive from theirs. Matching the upstream licence removes any question about
   redistributing derived work.
2. **Express patent grant (§3).** MIT is silent on patents. For a project proposing a
   specification others are asked to adopt, an explicit grant is a feature — adopters do not
   have to wonder.
3. **§6 trademarks.** Apache-2.0 explicitly grants no right to the licensor's marks. That is
   the clause that lets us build on Carbon and call the result CoForge, and it protects the
   CoForge name the same way in turn.

The cost is four conditions (§4): include the licence, mark modified files, retain notices,
include NOTICE. All satisfied.

## NOTICE
Records that tokens derive from `@carbon/themes` 11.79.0 (IBM, Apache-2.0), that Carbon
publishes DTCG natively so no conversion occurred, and that **CoForge is not affiliated with or
endorsed by IBM** and claims no IBM marks.

## Consequence
Closes the finding from the pre-start audit: we had audited every candidate's licence and
shipped none of our own.
