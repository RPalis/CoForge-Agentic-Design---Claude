# Pre-start audit — CoForge, 2026-08-27

Run before any real work flows through the pipeline. Read this before restarting the POC.

## Verdict

**The machine is built. It has never run.**

```
Workflow readiness   100%      agent dispatches   0
L1 Foundations        40%      artifacts produced 4 (all written directly)
L2 Complete           38%      gates fired on real work  0
```

Every guardrail has been tested **synthetically** — I planted violations and watched them get
caught. Not one has fired on real work, because no real work has flowed through.

**"Is it ready" is answered by running it, not by auditing it.**

---

## The finding that matters most

`produced_by` in all four artifact manifests claimed `research-synthesizer` or `research-ops`.
**Zero agents had ever been dispatched.** Every artifact was written directly by the main session.

Our own artifacts carried **false provenance** — the exact failure the manifest chain exists to
prevent — produced while building the system to prevent it.

**Nothing caught it.** Not Gate B, not `audit-system.py`, not `readiness-audit.py`. It surfaced
only because a human asked.

**Corrected 2026-08-27:** `produced_by` → `main-session`, original claim preserved in
`produced_by_claimed`, with a `provenance_note`. Nothing was silently rewritten.

**Standing lesson:** a field that nothing validates will eventually hold something false. The
manifest had 18 consistent keys across 5 files *by luck, not enforcement* — there is no
`manifest.schema.json`.

---

## Blind spots — verified, with evidence

| # | Finding | How found | Status |
|---|---|---|---|
| 1 | Zero agent dispatches — workflow 100% present, 0% exercised | transcript scan | **open** |
| 2 | False provenance in 4/4 manifests | manifest read | **fixed** |
| 3 | No `manifest.schema.json` — manifests unvalidated | file scan | **open** |
| 4 | `dashboard/data.json` genuinely stale; CI checks `.ai/` and registry but not it | content diff | **open** |
| 5 | Stop hook has never demonstrably fired | mtime | **open** |
| 6 | 36 of 40 checklists never used · 1 template for 40 types | file count | expected at Stage 0 |
| 7 | No LICENSE | file scan | **open** — Wave 0 |

## Redundancies

- **Real:** `dashboard/data.json` snapshots `.ai/index.json` and adds hand-written nodes. Two
  sources, one drifts — and it has. Should read the index at render time.
- **Acceptable:** `.ai/index.md`, `llms.txt`, `ARTIFACTS.md` are generated views of *different*
  data for *different* readers. Not duplication.
- **`RECONCILIATION.md`** — 256 lines, superseded by ADR-002, still tracked. Keep as history;
  should carry a header saying so.
- **The two audit scripts do not overlap.** `audit-system.py` (17 checks) asks *does it resolve?*
  `readiness-audit.py` (30 checks) asks *does it exist?*

## Corrections made during this audit

Recorded because the audit's own reliability is part of what is being audited:

1. First staleness test flagged `.ai/index.json` and the registry as stale. **Wrong** — it was
   comparing `generated_at` date fields. Both are in sync.
2. "ART-000 has empty provenance" — **wrong**, my glob was catching the generic template.

## Named-but-empty layers found across the whole build

Four, and the pattern is the lesson:

| Layer | Specified in | Had no implementation until |
|---|---|---|
| CI (enforcement layer 3) | CLAUDE.md | ADR-008 |
| Gate B on Bash writes | settings.json matcher | ADR-013 session (Stop hook) |
| Analytics | blueprint §11.2, ADR-005 | ADR-014 |
| **Agent dispatch** | ADR-002 routing table | **still unbuilt** |

**Every one was declared before it existed, and every one read as coverage until probed.**
Assume the next one exists too, and go looking.

## Left to decide before starting

| | Decision | Owner |
|---|---|---|
| 1 | Commit + push (17 files uncommitted, CI never run) | Claude |
| 2 | Move to `~/Projects/coforge`, restart Claude Code there | Claude, then Agentic Designer - RP restarts |
| 3 | **Brand inputs** — the only Wave 0 item Claude cannot do | **Agentic Designer - RP** |
| 4 | Dispatch agents for real (POC link 2) or keep writing directly and say so | Agentic Designer - RP |

## First actions on return

1. `python3 validation/audit-system.py` — confirm the baseline still passes
2. `python3 validation/readiness-audit.py` — L1/L2 scores
3. Read `memory/session-log.md` tail and `memory/open-questions.md`
4. Wave 0: LICENSE · tokens from Carbon themes · the 8 L1 primitives
