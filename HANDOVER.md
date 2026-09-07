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

## Status of the coverage figures — C-052 was largely WITHDRAWN

An earlier claim that all five coverage ratios fail to derive was **wrong and is withdrawn**.
Re-checked properly: *payment gate 6 of 17* derives to exactly 6, *both browser surfaces 4 of
17* derives to exactly 4, and *states 8 of 119* and *booking types 47 of 68* are not
contradicted. The original derivation searched capture titles instead of file contents.

**What remains open is narrow.** ART-024 §3.2 enumerates **fifteen** stage-units; the row
*Journey stages 25 of 136* is built from **eight** stages × 17. The board reports the booking-type
decomposition as its own separate row, so this may be a deliberate split — but the chart caption
says every bar is "measured against what the research plan specified", and that specific claim is
unverified. **A caption to fix or a split to document. Not a number to change.**

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
