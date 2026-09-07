# Handover — read this first if the context was cleared

**State at 2026-09-07.** Branch `capture-round-1`. Working tree committed.
Everything below is on disk; nothing important lives only in a conversation.

## Where things are

| What | Where |
|---|---|
| The dashboard (11 charts) | `artifacts/luma-hands-on/2026-09-07__dashboard__hands-on-findings-and-recommendations__v2/luma-competitor-research-findings.html` — **local file, never published** |
| Its generator | `build-dashboard.py` + `charts.py`, same directory |
| The evidence | `artifacts/luma-hands-on/2026-09-04__competitive-benchmark__hands-on-capture-round-1__v1/` — 50 captures, 121 findings |
| 52 corrections | `validation/corrections.json` |
| 10 standing rules, in every agent | `validation/standing-rules.json` → all 14 `.claude/agents/*.md` |
| Plans | `V2-ITERATION-PLAN.md`, `ROUND-2-PLAN.md`, `FINAL-CLEANING-PLAN.md` in the v2 directory |
| Capture backlog | `round2-capture-ranked.json` (146 tiered) + `unranked-76-ranked.json` (60 rows) |

## The one decision everything waits on

**All five coverage ratios on the board fail to derive from the record (C-052).**
The board says journey stages 25 of 136, booking types 47 of 68, states 8 of 119, payment
gate 6 of 17, both browser surfaces 4 of 17. Derivation gives 34 of 255, ~10-15 of 68, an
unknown, 3, and 3. Booking types at 69% is the only figure that makes coverage look
adequate anywhere, and no derivation approaches it.

Recomputing and republishing them changes what this round claims about itself. That is
Gate A. **Do not quote any coverage figure until it is settled.**

## Also open, in order

1. `insight-7` and `rec-4` rest on unverifiable quotes (C-050) — re-source before Gate A
2. Ratify `themes.json` (`status: proposed`), and have someone who has NOT read its per-row
   list re-derive `price-honesty`, which its author cut from 29 findings to 6
3. Amend ART-024 §5.2 to a confidence scale that varies (C-042, C-044)
4. Attestation — four validators changed and nobody outside those changes has attacked them
5. Then, and only then, round 2 capture: tiers 1 and 2, 41 aimed captures

## What is true about the content

The observations are sound: all 121 findings resolve to a capture, competitor fields match,
claim text traces. Six confirmed defects among ~62 attributed quotes. **The findings are
largely accurate; the summary statistics about them are not.**

## The rule that earned itself today

Nine of the ten corrections logged were found by someone other than the author. Not one was
found by re-reading. Dispatch a second agent; give it your numbers and tell it to
contradict them.
