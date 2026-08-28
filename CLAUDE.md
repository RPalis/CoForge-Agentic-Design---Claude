# CLAUDE.md — CoForge Master Plan

> Read at the start of every session. Loaded on every turn, so it stays short and
> points to files for detail. Detail lives in agent definitions and the sources of
> truth, not here.

## What CoForge is

A design operating system where AI agents produce research, journey maps, IA,
wireframes, UI, prototypes and handoff — under gates that make fabricated evidence
and off-system output impossible, not merely discouraged.

**Design-system state: RED** — a *declared* state, not a count. Tokens (786) and
`brand.md` exist; RED holds until L2 components land (ADR-011). See "DS fork" below.

## The two prohibitions

The only rules written here. Prose is the weakest enforcement layer, so this list
stays at two.

1. Never create a component that is not in `design-system/component-index.json`.
   File a proposal in `decisions/` instead.
2. Never write a user quote that is not in `research/evidence-ledger.json`.

Everything stronger is enforced by tools, hooks and CI — not by prose.

## The two sources of truth

| | Evidence (upstream) | System (downstream) |
|---|---|---|
| File | `research/evidence-ledger.json` | `design-system/tokens/tokens.json` + `component-index.json` |
| Owner | evidence-clerk | token-keeper |
| Gate | No claim without a resolvable evidence ID | No component outside the index, no value outside tokens |
| Prevents | Invented users, fabricated quotes | Invented components, raw hex, off-system UI |

## Two clocks — do not confuse them

- **Build Stages 0–5** — how we build this system. Linear, one-time. See `decisions/ADR-004-two-clocks.md`.
- **Design Loop Phases 1–11** — what the system does once built. Cyclical.

Current position (2026-08-28): **Build Stage 0–2 complete for foundations.**
`brand.md` approved at Gate A; 786 tokens across five axes; 8 L1 primitives.
**Design Loop still not runnable** — it needs the evidence spine (ledger is empty)
and L2 components (adapter #1, ADR-013 link 1, in progress).

## Orchestration — plan-and-execute

The orchestrator is thin. It does no design work and never passes artifact content
between agents. It reads this plan, the current phase and the last gate result;
walks the routing table; dispatches the one agent whose turn it is with an
objective, input paths, output path and explicit "not your job" boundaries; reads
the returned summary; checks the gate; advances or returns the failure.

Handoff is through files, never chat. Each agent reads only its declared inputs and
writes only its declared outputs.

## The gates

- **Gate A — human approval.** Judgment: research conclusions, severity, priority,
  release, anything public-facing.
- **Gate B — system check.** Structural, automatic: citations resolve, values are
  on-token, components exist in the index. Runs as PreToolUse hooks and in CI.

Gate B first (cheap, mechanical), then Gate A for calls that need a person.

## Enforcement layers (hardest to softest)

| # | Layer | Implemented by |
|---|---|---|
| 1 | Impossible | `.claude/settings.json` + per-agent `tools:` |
| 2 | Blocked | `.claude/hooks/gate-b.py` (PreToolUse on Write\|Edit) |
| 2b | Backstop | `.claude/hooks/session-check.py` (Stop) — **Gate B does NOT fire on Bash writes**; this catches them |
| 3 | Failed | `.github/workflows/ci.yml` → `validation/audit-system.py` |
| 4 | Visible | `validation/reports/*__system-audit.md` |
| 5 | Written | the two prohibitions above |

Every layer names a file. A layer with no implementation is worse than no layer — it
reads as coverage. Findings are severity-ranked (blocker/error/warning/info) and carry
a suggested fix. **Skipped checks are always reported: skipped is not passed.**

Tool-gating outranks prohibition. Never solve with prose what a permission can solve.

## Two output levels (ADR-012)

- **L1 Foundations** — branded documents, decks, dashboards, diagrams. Needs tokens +
  `brand.md` + the 8 level-1 primitives. **34 of 40 artifact types.** Available at Build Stage 2.
- **L2 Complete** — responsive web prototypes and product UI. Needs the full component index,
  Code Connect and the CoForge MCP. 6 artifact types. Build Stage 3.

Gate B applies at both levels. L1 is not exempt — its component vocabulary is *restricted to
level-1 entries*, which is stricter than exempting it and costs one field in the index.

## The DS fork

- **Green** — DS in code: screen-producer targets Claude Code + Figma MCP + Code Connect.
- **Yellow** — DS exists, not in code: match components, review consistency, feed gaps to token-keeper.
- **Red** — no *component* DS: token-keeper builds the foundations before **L2** screens are
  produced. **CoForge is here** — tokens and brand are done, so L1 output is unblocked; RED
  persists until the component index carries L2 entries. The fork is a **declared** state:
  L1 primitives existing does not make a design system exist, and the declared value wins
  over any count.

## Routing table

Phase filters; task type / gate result is the match key. Exactly one agent should
match any (phase, task) pair.

| Phase | Trigger | Agent | Reads | Writes | Gate | Not this agent when |
|---|---|---|---|---|---|---|
| 1 Research | new sources to log | evidence-clerk | research/sources/ | evidence-ledger.json | B+A | interpreting (synthesizer) |
| 1 Research | synthesise findings | research-synthesizer | evidence-ledger.json | artifacts/…/insight-report | A | logging quotes (clerk) |
| 2 Define | persona / problem / story | research-synthesizer | evidence-ledger.json | artifacts/…/persona | A | diagrams (cartographer) |
| 2 Define | journey / empathy map | diagram-cartographer | evidence-ledger.json | artifacts/…/journey-map | A | prose synthesis |
| 3 Ideation | IA / site map / flow | diagram-cartographer | artifacts/…/insight-report | artifacts/…/ia-map | A | screens (screen-producer) |
| 3 Ideation | sketches / concepts | screen-producer | artifacts/…/ia-map | artifacts/…/wireframe | B | tokens (token-keeper) |
| 4 Design | wireframe → hi-fi / proto | screen-producer | component-index, tokens | artifacts/…/ui-screen | B→A | data viz (dashboard-analyst) |
| 4 Design | a11y first filter | a11y-checker | artifacts/…/ui-screen | validation/…/a11y | B | writing anything (read-only) |
| 5 Test | test plan / feedback / RICE | research-ops | prototype, ledger | artifacts/…/test-report | A | design changes |
| 6 Handoff | spec / redline / ticket | handoff-scribe | ui-screen, component-index | artifacts/…/handoff-spec | A | code review |
| 7 Implementation | design-vs-build audit | design-critic | ui-screen, built UI | validation/…/audit | B (A on change) | writing fixes (advisory) |
| 8 QA | UI diff / a11y / flow | design-critic + a11y-checker | build, design | validation/…/qa | A | shipping (human gate) |
| 9 Launch | release notes / comms / docs | content-comms | approved artifacts | artifacts/…/release-note | A | metrics (dashboard) |
| 10 Monitor | usage / KPIs / metrics | dashboard-analyst | connectors, tokens | artifacts/…/metrics-scorecard | B | conclusions (synthesizer) |
| 11 Improve | roadmap / hypotheses | research-synthesizer | metrics, ledger | artifacts/…/prioritization | A | — → loops to Phase 1 |
| any | brand voice / visual language | brand-director | brand inputs | foundations/brand.md | A (suggest-only) | never graduates |
| any | token sync / drift | token-keeper | Figma variables, tokens.json | tokens.json | auto sync / suggest new | — |

## Autonomy ladder

- Everything that can write starts at **Draft** (Gate A before it counts).
- Graduates to **Auto** (Gate B only) after **3 consecutive clean reviews**, logged in
  `memory/corrections.md`. The orchestrator counts.
- **Demotion:** one hard fail in Auto drops the task type back to Draft.
- **Never graduate:** brand-director; research-synthesizer conclusions.
- **Auto from day one:** a11y-checker, evidence-clerk's structural check — verifiable,
  read-only, small blast radius.
- **Advisory, not auto:** design-critic. Read-only is not zero blast radius when the
  output's purpose is to change what a human does next.

## Artifacts

Everything generated for a human to look at lives in `artifacts/`. Every artifact is
a **directory** — no exceptions:

```
artifacts/<workstream>/YYYY-MM-DD__<type>__<slug>__v<N>/
    <descriptive-name>.<ext>   the thing itself — named for a human (ADR-010)
    manifest.json              provenance; "file" names the payload
    validation.md              proof it passed, before a human saw it
```

- Type must exist in `artifacts/_types.json` (41 types). Unregistered type = no artifact.
- `manifest.json` chains `inputs.evidence` to ledger IDs and `inputs.tokens_version`
  to a token release. Any claim auditable; any token change traceable.
- Lifecycle: `draft → validated → in-review → approved → superseded → archived`.
  Versions immutable — changes make v2, v1 becomes superseded.
- **Nothing enters `artifacts/` until it passes validation.** Failures stay in `scratch/`.
- `_registry.json` is generated by scanning, never hand-edited.

## Claim format

Two evidenced forms. They are not interchangeable — one rests on a person, the other on an
instrument, and the notation must not let them blur (ADR-017).

- `Evidenced [E-nnn]` — **testimony.** Resolves in `research/evidence-ledger.json`.
- `Evidenced [ART-nnn § Section]` — **measurement.** Resolves to a registered artifact and
  a real section heading in its payload.
- Either form that does not resolve **strips** the claim, not softens it.
- `Inferred` — must name what it is inferred from.
- `Assumption` — collected in a visible Assumptions block.

Never mint a ledger ID for a measurement. Once the ledger holds things nobody said,
"every quote resolves" stops meaning "no user was invented."

## Boundaries

| Folder | Holds | Never holds |
|---|---|---|
| `research/sources/` | Raw, immutable inputs | Anything generated |
| `research/evidence-ledger.json` | Verbatim quotes with IDs | Interpretation |
| `artifacts/` | Every generated deliverable | Raw sources · SSOT definitions |
| `design-system/` | The reusable system | One-off screens · project work |
| `decisions/` | ADRs | Deliverables |
| `validation/` | Checklists, reports, skill-evals | The artifacts themselves |
| `memory/` | Continuity and corrections | Work product |
| `scratch/` | Drafts, failures, experiments | Anything approved |

**The membrane:** a `component-spec` in `artifacts/` is a *proposal*. It enters
`component-index.json` only by promotion — explicit human approval, recorded as an
ADR. Promotion is the only path into the design system.

## Skill evaluation

Skills follow the eval-driven standard (agentskills.io).
`.claude/skills/<skill>/evals/evals.json` is the only hand-authored file (ADR-005 —
it lives *inside* the skill, not at the repository root). Every case runs twice — with skill and without — because
without a baseline you cannot tell whether the skill helped. Assertions are written
**after** the first run. Grading requires evidence quoting the output. Workspaces in
`validation/skill-evals/<skill>/iteration-N/`. See `decisions/ADR-005-skill-evals.md`.

## Session protocol

- **Start:** this file → **`.ai/index.md`** (load once, keep in context, fetch detail on
  demand) → `memory/corrections.md` → tail of `memory/session-log.md` →
  `memory/open-questions.md`.
- **End:** run `python3 validation/audit-system.py` (the Stop hook does this automatically),
  then append what was produced, what changed in either source of truth, what is blocked,
  and the single next action.
- **Never assume a gate ran.** Gate B fires on Write/Edit only. Bash heredocs bypass it —
  that is how this repository was actually built, and it went unnoticed for a full session.
- A correction that recurs twice is promoted into this file as a standing rule.

## Output surfaces

Propose a surface with a reason and confirm before publishing — never pick silently.
Claude Design → Figma is **one-way**; no automated diff-back. Once a design lands in
Figma, Figma owns it. Flag that boundary every time it is crossed.

## Repository map

```
CLAUDE.md              this file            architecture.md  the system map
AGENTS.md              vendor-neutral        .ai/index.md     generated index
.claude/agents/        13 definitions       .claude/settings.json  the tool gate
.claude/hooks/         Gate B validators    .claude/skills/        our own recipes
research/              evidence SSOT        design-system/         system SSOT
artifacts/             deliverables         decisions/             ADRs
validation/            reports + evals      memory/                continuity
.github/workflows/     CI (layer 3)         scratch/               nothing approved
```
