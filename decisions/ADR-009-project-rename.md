# ADR-009 — Project renamed: Luma → CoForge

**Status:** Accepted · 2026-08-26

## Decision

The system is now **CoForge**. The dashboard is titled *CoForge Agentic Design*;
the page heading reads *CoForge — Agentic Design System*.

## What was renamed

Live, operational documents — the ones that describe the system as it is now:
`CLAUDE.md`, `architecture.md`, `AGENTS.md`, `design-system/DESIGN-SYSTEM.md`,
`design-system/llms.txt`, `tokens.json`, the `orchestrator` and `token-keeper`
agent definitions, `memory/open-questions.md`, and the dashboard generator.

## What was deliberately NOT renamed

**ADR-001 through ADR-008, `memory/session-log.md`, and `RECONCILIATION.md`.**

These are the historical record. They describe decisions taken, and work done, when
the project was called Luma — and that was true at the time. Rewriting them would
make the record say something that never happened, which is the same failure mode
the evidence ledger exists to prevent upstream. Our own precedent is ADR-006: a
wrong citation was corrected by writing a *new* ADR, not by editing the old one.

This ADR is the pointer. A reader who finds "Luma" in ADR-003 finds it here.

The blueprint `Luma-Agentic-Design-System-Blueprint.docx` is also unchanged — it was
prepared for a specific audience and may already have been circulated. Renaming a
document someone already holds a copy of creates two versions with one name.

## Filenames

Two files carried the project name and were renamed to drop it:

| Before | After |
|---|---|
| `validation/index-luma.py` | `validation/index-system.py` |
| `dashboard/luma-dashboard.html` | `dashboard/index.html` |

Encoding a project name in a path has already broken two build scripts in this
repository (the `Desktop/Luma` → `Desktop/Luma Claude` rename, ADR-008 session).
A neutral name survives the next rename. `index.html` also means the local
preview server resolves it at the root URL with no path.

## Not changed

The working directory is still `~/Desktop/Luma Claude`. Renaming it would break
hardcoded paths again for no functional gain, and it is separately a candidate to
move off the Desktop entirely (macOS TCC blocks the preview server there).
