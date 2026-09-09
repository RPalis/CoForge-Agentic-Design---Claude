# HANDOVER — as of 2026-09-09

Read `CLAUDE.md`, then this. Detail is in `memory/session-log.md` (last entry) and
`validation/corrections.json` (58 entries).

## Where things stand

| | |
|---|---|
| Branch | `capture-round-1` |
| Design-system state | **RED** — unchanged. 208 of 208 L2 rows are `@carbon/react`; 0 authored here |
| Evidence ledger | **empty (0 records)** — Design Loop still not runnable |
| Corrections | 58 · Standing rules 11 (newest **SR-11**) |
| Audit verdict | **FAIL** — 31 blockers, 1 error |

## The 31 blockers, and why 30 of them are one question

30 are `raw colour #......` in artifacts generated on 2026-09-08. They are **not** a
correctness problem: the values match `tokens.json` exactly (verified). They are C-058 —
the raw-colour check matches hex only, so ART-026 v2's **708** literal `color(srgb …)`
values have always passed unseen.

**Do not silence these by switching the generators to `color(srgb …)`.** That changes
nothing real and hides the same practice again. The open question is what "on-token" can
mean for a self-contained file that must open offline with no build step, where a literal
is unavoidable. Likely answer: a generated-from-tokens provenance claim in the manifest
that the check can verify. **Needs an ADR.**

The 31st blocker is **ART-022** (`tokens_version: null`), which predates this session.

## Deliverables live now

- **Figma** — Report 2, section `864:15148` in *AI Workflows for UX*, page *5. Testing
  Round 2 - Raquel Agents*. Frames `866:16971 / 16777 / 16645 / 16523`.
  **Figma is one-way**: re-running the pipeline overwrites, it does not merge.
- **Zip** — `artifacts/design-system-authoring/2026-09-08__handoff-spec__coforge-shareable-package__v1/coforge-artifacts.zip`.
  Rebuild: `python3 build/build_foundations.py && python3 build/build_index.py &&
  python3 build/build_figma_make.py`, then re-zip `dist/`.
- **Board pipeline** — `artifacts/system-operations/2026-09-08__dashboard__…__v1/pipeline/`.
  Reads `board-dataset.frozen.json`; `build-dataset.py` is deliberately OUT of the build
  path so figures cannot move under the report.

## Waiting on the client

1. **Embed the fonts?** The zip falls back to a system sans without Anek Latin and Source
   Code Pro. Embedding needs ~400KB downloaded from Google Fonts (both OFL). Asked, unanswered.
2. **ART-022's `tokens_version`** — I will not declare provenance I did not verify.
3. **C-058** — the ADR above.

## Owed work

- An independent agent must attack **ART-028**; I wrote its pages, generator and checker.
- **W-3**: `audit-system.py` check 5g never descends into `artifacts/`, so
  `verify-charts.mjs`, `verify-widgets.mjs` and `verify-frames.mjs` are outside the
  machinery hash. Closing it invalidates the current attestation and needs a fresh round.
- Round 2 capture: 41 aimed captures across tiers 1+2.

## Two habits this session paid for

- **Delete by explicit id, never by container.** Clearing a Figma section's children
  removed two nodes the client had made, and reported what it deleted only afterwards.
- **Read the output before shipping it.** Reading each frame before import caught five
  hand-written sentences that had drifted from their own charts, and one that was simply
  false. No checker would have caught any of them.
