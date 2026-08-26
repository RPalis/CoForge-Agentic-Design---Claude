# ADR-007 — Figma tooling: grant timing and server duplication

**Status:** Accepted · 2026-08-25

## Context

Three agents are chartered for Figma work but hold no Figma tools:

| Agent | Charter needs | Current `tools:` |
|---|---|---|
| `token-keeper` | ADR-001 inversion: export/import tokens ↔ Figma variables | `[Read, Write, Bash]` |
| `handoff-scribe` | Code Connect — the design↔dev contract | `[Read, Write]` |
| `diagram-cartographer` | FigJam / diagram generation | `[Read, Write]` |

Three Figma MCP namespaces are live, representing **two distinct products**:

1. **Official Figma MCP** (`mcp.figma.com`) — Code Connect (`get`/`add_code_connect_map`,
   `send_code_connect_mappings`), design context, `use_figma`, `get_figjam`,
   `generate_diagram`, assets. **Code Connect exists only here.**
2. **figma-console** (southleft) — the token pipeline (`figma_export_tokens` with 11
   output formats incl. DTCG, `figma_import_tokens`, `figma_setup_design_tokens`,
   `figma_batch_create_variables`), `figma_audit_design_system_report`,
   `figma_lint_design` (WCAG 2.2, 10 rules), `figma_check_design_parity`, `figma_ds_*`.
   Reads tokens via Desktop Bridge, so it works on **any Figma plan** — the Variables
   REST API is Enterprise-gated, this is not.
3. **figma-console, reduced build** — identical descriptions, but missing `figma_ds_*`,
   `audit_design_system`, `search_components`, `browse_tokens` and console diagnostics.

The two products are **complementary, not duplicates**: `figma_export_tokens` →
`figma_import_tokens` *is* the ADR-001 inversion machinery, and Code Connect *is* the
handoff contract. The genuine duplicate is the full vs reduced figma-console.

## Decision 1 — Grant Figma tools at Build Stage 2, not now

Luma is **RED**: no Figma file exists. None of the three agents can exercise a Figma
tool today, so a grant now would be untestable and unverified. Tools are granted at
the moment they are first needed, against real files, and the grant is tested rather
than assumed.

**Planned split when granted** (each agent gets only its charter):

| Agent | Server | Why |
|---|---|---|
| `token-keeper` | figma-console (full) | ADR-001 inversion |
| `handoff-scribe` | Official Figma | Code Connect exists nowhere else |
| `diagram-cartographer` | Official Figma | `get_figjam`, `generate_diagram` |

`a11y-checker` and `design-critic` are read-only; `figma_lint_design` and
`figma_check_design_parity` are read-only and may be granted without widening them.

## Decision 2 — Disconnect the reduced figma-console build

Two builds of the same product create silent misbinding: an agent may bind the reduced
one and lose `figma_ds_*`, audit and search tooling with no error. One is removed.

**This cannot be done from a non-interactive session** — connector changes require the
claude.ai connector settings UI, or `claude mcp` / `/mcp` in an interactive terminal.
Owner: Raquel. Blocks: nothing today; **must be done before Build Stage 2.**

## Consequence

Until both are done, `screen-producer` stays wireframe-only (correct for RED anyway),
and Build Stage 2 cannot begin.
