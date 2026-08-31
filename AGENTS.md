# AGENTS.md

Vendor-neutral pointer. The master plan is `CLAUDE.md` — read it first.

Agent definitions are in `.claude/agents/`: one `orchestrator` (reads the plan and
dispatches) and 13 workers, each owning one artifact type and handing off through
files, never chat.

Orchestration is plan-and-execute: the plan is a file, the filesystem is the
coordination substrate, and execution is a deterministic walk of the routing table
in `CLAUDE.md`.

Two prohibitions, and everything stronger is enforced by tools rather than prose:

1. Never create a component absent from `design-system/component-index.json`.
2. Never write a user quote absent from `research/evidence-ledger.json`.
