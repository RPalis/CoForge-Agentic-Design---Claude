# ADR-006 — Correction: token-efficiency benchmark attribution

**Status:** Accepted · 2026-08-25

## Context
Two conflicting attributions existed for the "80% fewer tokens, 5x lower annual cost"
figure: one to a Microsoft 2024 source, one to a benchmark reported by Into Design
Systems.

## Finding
Verified. The correct attribution is **Diana Wolosin's benchmark at Indeed** —
8 MCP configurations, 1,056 prompts, comparing MDX, Markdown, hybrid, JSON variants
and TOON. JSON metadata achieved higher accuracy at 80% fewer tokens and 5x lower
annual cost ($300 vs $1,500). Indeed parsed 77 components from MDX into JSON and
ingested them into a Vectra vector database. Presented at the AI Conference for
Designers 2026, reported via Into Design Systems.

The Microsoft 2024 attribution in `_drafts/build_exec_doc.py` is **incorrect** and
must not be reused.

## Consequence
Any document citing this figure attributes it to the Indeed benchmark.
