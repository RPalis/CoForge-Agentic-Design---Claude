# ADR-001 — Token source of truth and the inversion point

**Status:** Accepted · 2026-08-25

## Context
Luma is greenfield (DS fork state: RED). There are no Figma variables to read, so the
repository must author tokens first. But designers change tokens in Figma day to day,
so Figma must own them long term.

## Decision
Seed-then-invert, in this order:

1. Brand inputs → `design-system/foundations/brand.md`
2. → `design-system/tokens/tokens.json` v0 (repo authors, DTCG format)
3. → push into Figma variables
4. **INVERSION POINT** — from here Figma owns tokens permanently
5. → `figma_export_tokens` → `tokens.json` (repo mirrors only)
6. → drift check fails the build on divergence

## Consequences
- After inversion, `token-keeper` never authors a token again. It mirrors.
- A documented break-glass path exists to re-author if Figma is corrupted; using it
  is a logged incident, not a silent action.
- `inputs.tokens_version` in every artifact manifest chains any pixel to a release.

**Inversion date:** not yet reached. Record it here when it happens.
