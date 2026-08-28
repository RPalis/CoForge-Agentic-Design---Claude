# CoForge — architecture

> What the parts are and how they relate. `CLAUDE.md` is the *plan and the rules*;
> this file is the *map*. Read this to understand the system; read CLAUDE.md to operate it.
> `.ai/index.md` is the machine-cheap version — load that once at session start.

## The six layers

```
┌─ DOCS & AUTOMATION ─────────────────────────────────────────────┐
│  architecture.md · CLAUDE.md · AGENTS.md · decisions/*.md        │
│  .github/workflows/ci.yml · .claude/settings.json                │
│  Rules, documentation and automation. Layer ONE, not an          │
│  afterthought — a rule nothing executes is not a rule.           │
└──────────────────────────────────────────────────────────────────┘
┌─ ORCHESTRATION ─────────────────────────────────────────────────┐
│  orchestrator + 12 workers · routing table · autonomy ladder     │
└──────────────────────────────────────────────────────────────────┘
┌─ INDEXING ──────────────────────────────────────────────────────┐
│  .ai/index.json · .ai/index.md · validation/index-system.py        │
│  Pre-computed structure. Loaded once, not re-derived per session.│
└──────────────────────────────────────────────────────────────────┘
┌─ EVIDENCE (upstream SSOT) ──────┐ ┌─ SYSTEM (downstream SSOT) ───┐
│  research/sources/  immutable   │ │  tokens.json  (DTCG)         │
│  evidence-ledger.json           │ │  component-index.json        │
│  participants.json              │ │  foundations/brand.md        │
│  gate: citations resolve        │ │  gate: on-token, in-index    │
└─────────────────────────────────┘ └──────────────────────────────┘
┌─ ARTIFACTS ─────────────────────────────────────────────────────┐
│  40 registered types · every artifact a directory                │
│  named payload + manifest.json (provenance) + validation.md      │
└──────────────────────────────────────────────────────────────────┘
┌─ AGENTIC LOOP ──────────────────────────────────────────────────┐
│  gate-b.py (per write) · audit-system.py (whole repo, CI)        │
│  severity-ranked · suggested fixes · skipped checks reported     │
└──────────────────────────────────────────────────────────────────┘
```

## How a piece of work flows

```
raw source ──▶ evidence-clerk ──▶ evidence-ledger.json
                                        │ [E-nnn]
                                        ▼
                             research-synthesizer / diagram-cartographer
                                        │
                                        ▼
                          artifacts/<ws>/<date>__<type>__<slug>__v1/
                            ├─ artifact.*      the thing
                            ├─ manifest.json   inputs.evidence → [E-nnn]
                            │                  inputs.tokens_version → release
                            └─ validation.md   proof it passed
                                        │
                    Gate B (hook) ──▶ audit-system.py (CI) ──▶ Gate A (human)
```

Two chains make everything auditable: `manifest.inputs.evidence` answers *"why does
this claim that?"*, and `manifest.inputs.tokens_version` answers *"what breaks if we
change this token?"*

## Enforcement — six layers, all implemented

| # | Layer | Implementation | Bypass |
|---|---|---|---|
| 1 | Impossible | `.claude/settings.json` permissions + per-agent `tools:` | **Bash** — the deny list covers `Write`/`Edit` only |
| 2 | Blocked | `.claude/hooks/gate-b.py` (PreToolUse on Write\|Edit) | Bash writes; edit local config |
| 2b | Backstop | `.claude/hooks/session-check.py` (Stop) | catches what 2 misses |
| 3 | **Failed** | `.github/workflows/ci.yml` → `validation/audit-system.py` | admin only |
| 4 | Visible | `validation/reports/*__system-audit.md` | social |
| 5 | Written | two prohibitions in CLAUDE.md | trivial |

**Layer 1 has a known hole, recorded 2026-08-27.** `settings.json` denies
`Write(./research/sources/**)` and `Edit(./research/sources/**)` — but not `Bash`. A shell
`mv` walks straight into the evidence locker, which is the one directory the whole
no-invented-evidence guarantee rests on. Same gap for `_registry.json` and `ARTIFACTS.md`.
This is the identical blind spot CLAUDE.md already flags for Gate B, in the layer above it.

### What each check actually covers

A layer that names a file is not the same as a check that opens one. Recorded so the
scope is legible rather than assumed:

| Check | Walks | Added |
|---|---|---|
| artifacts | `artifacts/**` — naming, manifest, validation, `[E-nnn]` resolution | ADR-008 |
| foundations | `design-system/foundations/*.md` — `[E-nnn]`, `[ART-nnn § …]`, no `scratch/` deps | ADR-017 |
| tokens | `artifacts/**` + `design-system/components/**` — raw hex, raw px | ADR-008 |
| contracts | `tokens.json` + `component-index.json` — redundancy within an axis, orphans, alias tier direction, component contracts vs the token layer | 2026-08-28 |
| gates | the hooks themselves — plants real violations down the Write path *and* the Bash path | 2026-08-28 |

Three different questions, and a pass on one says nothing about the others:
`audit-system.py` asks whether the repo is **legal**; `audit-contracts.py` asks whether
the design system is **coherent**; `test-gates.py` asks whether the enforcement
**works**. The third exists because a gate nobody has fired is indistinguishable from a
gate that does not — and when it was first run it found Gate B blocking every
*legitimate* component, which no amount of passing the other two would have surfaced.

`foundations/` was covered by **nothing** until ADR-017 — the audit reported
`skipped 0 · PASS` on runs that never opened `brand.md`.

Layer 3 existed only as a sentence until 2026-08-25. A named-but-empty layer is worse
than an absent one, because it reads as coverage.

## Two clocks

- **Build Stages 0–5** — how the system gets built. Linear. Currently: Stage 0 done.
- **Design Loop Phases 1–11** — what it does once built. Cyclical. Currently: not runnable.

Say which clock you mean. "Phase 2" is ambiguous; "Build Stage 2" is not. See ADR-004.

## Where truth lives

| Question | File |
|----------|------|
| What did a user actually say? | `research/evidence-ledger.json` |
| What colour/space/type may I use? | `design-system/tokens/tokens.json` |
| Does this component exist? | `design-system/component-index.json` |
| What artifact types are legal? | `artifacts/_types.json` |
| What exists right now? | `.ai/index.md` (generated) |
| Why was this decided? | `decisions/ADR-*.md` |
| What did we learn / get corrected on? | `memory/corrections.md` |

## Regenerating

**Generated by scanning — never hand-edit the outputs:**

```
python3 validation/index-system.py        # .ai/index.json + .ai/index.md
python3 validation/rebuild-registry.py    # artifacts/_registry.json + ARTIFACTS.md
python3 validation/build-llms-txt.py      # design-system/llms.txt
python3 dashboard/build.py && python3 dashboard/render.py
```

**Authored by script — each refuses to write unless its own checks pass, and each is
idempotent:**

```
python3 validation/build-token-axes.py --apply      # spacing, type, elevation, motion
python3 validation/align-dark-to-light.py --apply   # dark's key set must equal light's
python3 validation/adapters/carbon-react.py         # L2 components from @carbon/react
```

**Checking:**

```
python3 validation/audit-system.py        # structure — what CI runs
python3 validation/audit-contracts.py     # coherence — redundancy, orphans, contracts
python3 validation/test-gates.py          # enforcement — does the gate actually block?
python3 validation/readiness-audit.py     # agent-readiness, scored — POINTS AT ANY SYSTEM
```

`readiness-audit.py` is the one that carries the thesis. The others check CoForge; this
one scores *a* design system against the 7-layer architecture and takes a path argument,
so it runs against anybody's. Findings are PRESENT / PARTIAL / MISSING — never a bare
pass, and never silent about what could not be checked. If the POC produces one durable
artefact, it is a runnable definition of "agent-ready" that the field currently lacks.

**Analytics as a by-product, not a chore:**

```
python3 validation/collect-metrics.py     # run record; joins transcripts, gates, registry
```

Counts and identifiers only — no conversation content, no file contents, no free text,
with a self-check that refuses to emit if free text appears. That constraint became
load-bearing the day the repository went public.

`flatten-dark-tokens.py` is retained but superseded by `align-dark-to-light.py`; its
own docstring records why its equality check was wrong. Kept rather than deleted
because the mistake is worth reading.
