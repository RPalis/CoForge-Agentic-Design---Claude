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

```
python3 validation/index-system.py          # .ai/index.json + .ai/index.md
python3 validation/rebuild-registry.py    # artifacts/_registry.json + ARTIFACTS.md
python3 validation/audit-system.py        # whole-repo audit (what CI runs)
```

All three are generated by scanning. Never hand-edit their outputs.
