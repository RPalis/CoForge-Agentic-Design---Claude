# ADR-005 — Skill evaluation standard

**Status:** Accepted · 2026-08-25
**Standard:** https://agentskills.io/skill-creation/evaluating-skills

## Decision
Skill quality is governed by eval-driven iteration, not by whether a skill seemed to
work once.

- `evals/evals.json` in the skill directory is the **only hand-authored** eval file.
  `grading.json`, `timing.json`, `benchmark.json`, `feedback.json` are generated.
- **Every case runs twice** — `with_skill/` and `without_skill/` (or `old_skill/`
  when comparing versions). Without a baseline you cannot distinguish skill value
  from model capability.
- Each run starts in **clean context** — fresh subagent or separate session.
- **Assertions are written after the first run**, not before.
- Grading requires **concrete evidence quoting the output**. No benefit of the doubt.
- The **benchmark delta** (pass_rate / time / tokens) is the keep-or-cut instrument.
- Start with 2–3 test cases.

## Layout
```
.claude/skills/<skill>/evals/evals.json
validation/skill-evals/<skill>/iteration-N/
    eval-<case>/{with_skill,without_skill}/{outputs,timing.json,grading.json}
    benchmark.json  feedback.json
```

## Convergence with model migration
"Keep the skill lean — remove instructions when results plateau" is the same
instrument as "fix by deletion first" during a model migration. Over-constrained
skills cause both plateaued eval scores and post-migration degradation.
